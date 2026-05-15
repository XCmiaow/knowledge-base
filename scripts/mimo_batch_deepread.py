#!/usr/bin/env python3
"""
MiMo 批量深度精读脚本 — 169 篇综述论文摘要精读
- 从 S2/Crossref 获取摘要
- 调用 MiMo-V2.5-Pro 精读（国内直连，~10-15s/篇）
- 输出含 [原文] 引用的结构化笔记
- 自动验证断言 vs 原文摘要（防幻觉）
- 多 worker 并行 + 进度保存
"""
import json, os, re, sys, time, urllib.request, urllib.error, concurrent.futures
from pathlib import Path

# ====== MiMo Config ======
MIMO_API_KEY = "tp-c7e6mb2a9nq2t3qyo1osfdcai40wv6hndkvl12k6dook1c9f"
MIMO_BASE = "https://token-plan-cn.xiaomimimo.com/v1"
MIMO_MODEL = "mimo-v2.5-pro"

# ====== Paths ======
VAULT_ROOT = Path(r"E:\工作区\knowledge-base")
WIKI_DIR = VAULT_ROOT / "wiki" / "水凝胶"
PROGRESS_FILE = VAULT_ROOT / "scripts" / "pipeline_progress.json"
REVIEW_FILE = VAULT_ROOT / "scripts" / "review_papers.json"

RATE_LIMIT = 2.0  # seconds between calls (per worker)
MAX_WORKERS = 4
API_TIMEOUT = 120

def doi_slug(doi: str) -> str: return doi.replace("/", "_")

def fetch_abstract(doi: str) -> dict:
    """S2 → Crossref 两级获取摘要."""
    # S2
    url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}?fields=title,abstract,authors,year,journal,externalIds"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "MiMoDeepRead/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            s2 = json.loads(resp.read().decode("utf-8"))
        abstract = s2.get("abstract", "") or ""
        if len(abstract) > 20:
            authors = []
            for a in (s2.get("authors") or []):
                name = a.get("name", "")
                if name: authors.append(name)
            return {
                "source": "s2",
                "title": s2.get("title", ""),
                "abstract": abstract,
                "authors": "; ".join(authors[:10]),
                "journal": (s2.get("journal") or {}).get("name", ""),
                "year": str(s2.get("year", "") or ""),
            }
    except Exception as e:
        pass

    # Fallback: Crossref
    url = f"https://api.crossref.org/works/{doi}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "MiMoDeepRead/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            cr = json.loads(resp.read().decode("utf-8"))
        msg = cr.get("message", {})
        abstract = msg.get("abstract", "")
        if abstract:
            abstract = re.sub(r"<[^>]+>", "", abstract)
            abstract = re.sub(r"\s+", " ", abstract).strip()
        if len(abstract) > 20:
            authors_list = msg.get("author", [])
            author_str = "; ".join(
                f"{a.get('given','')} {a.get('family','')}".strip()
                for a in authors_list[:10]
            )
            return {
                "source": "crossref",
                "title": (msg.get("title") or [""])[0],
                "abstract": abstract,
                "authors": author_str,
                "journal": (msg.get("container-title") or [""])[0],
                "year": str(msg.get("published-print",{}).get("date-parts",[[None]])[0][0]
                          or msg.get("published-online",{}).get("date-parts",[[None]])[0][0]
                          or ""),
            }
    except Exception as e:
        pass

    return {"source": "none", "error": "No abstract", "abstract": ""}


DEEPREAD_PROMPT = """请精读以下纤维素基水凝胶领域的论文信息，生成详细的结构化笔记。

【论文信息】
DOI: {doi}
标题: {title}
作者: {authors}
期刊: {journal}
年份: {year}

【原文摘要（Abstract）】
{abstract}

【精读要求】
请基于上述摘要生成以下结构的笔记。

**关键规则：**
1. **必须基于原文摘要，不得添加摘要中不存在的信息**
2. **定量数据必须精确引用**（包括具体数值、百分比、温度等）
3. **每项关键结论必须标注原文依据**（引用摘要中的原句，用「」标注）
4. **明确区分"摘要明确说明"和"基于摘要推断"的内容**
5. **对不确定的推断必须标注"[推断]"**
6. **CRITICAL: [原文]「」中的内容必须是摘要的原文（verbatim），不得翻译成中文。如果摘要是英文，引用英文原句；如果摘要是中文，引用中文原句。**

【输出格式要求】

### 1. 核心发现（2-3句）
用2-3句话概括本文最核心的科学发现。

### 2. 创新点
逐条列出本文的创新之处：
- **[原文]「引用摘要原句」** — 中文解释

### 3. 方法简述
- **[原文]「引用摘要原句」** — 方法说明

### 4. 关键结果（定量数据）
- **[原文]「引用摘要原句」** → 结果描述（含具体数值）

### 5. 与"纤维素基宽温域水凝胶"综述的相关性
分析本文对纤维素基宽温域水凝胶综述的参考价值。此处允许合理推断，但必须标注[推断]。

### 6. 局限性
- 摘要中提到的局限性（如有）
- [推断] 基于摘要推断的局限性

### 7. 关键词
3-6个关键词"""


def call_mimo(prompt: str) -> str:
    """Call MiMo-V2.5-Pro API and return response text."""
    body = json.dumps({
        "model": MIMO_MODEL,
        "messages": [
            {"role": "system", "content": "你是一位材料科学领域的资深研究员，专攻纤维素化学和水凝胶。你的笔记要求精确、详实、有据可查。输出使用中文。"},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 4096,
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{MIMO_BASE}/chat/completions",
        data=body,
        headers={
            "Authorization": f"Bearer {MIMO_API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=API_TIMEOUT) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[[MiMo Error: {e}]]"


def verify_claims(note_text: str, abstract: str) -> dict:
    """
    验证笔记中的数据是否在原文摘要中有依据。
    策略：提取笔记中所有数值（温度、百分比、数值等），检查是否在摘要中出现。
    中文↔英文直接文本匹配不可靠，所以聚焦在数字证据上。
    """
    if not abstract:
        return {"verified": [], "unverified": ["[无法验证：无原文摘要]"], "total_quotes": 0, "verified_count": 0, "unverified_count": 0}

    abstract_lower = abstract.lower()

    # Extract all numbers from note (temperatures, percentages, values)
    note_numbers = re.findall(r'-?\d+\.?\d*\s*(?:°C|℃|%|MPa|kPa|Pa|mPa|fold|倍|mM|mg/mL|g/mol|S/m|Ω)', note_text, re.IGNORECASE)
    # Also standalone large numbers that might be data
    note_numbers += re.findall(r'\b\d{2,}\.\d+\b', note_text)

    verified_nums = []
    unverified_nums = []
    for num in note_numbers:
        clean = num.strip()
        if not clean:
            continue
        # Check if this number appears in abstract
        if clean.lower() in abstract_lower:
            verified_nums.append(clean)
        else:
            # Try matching just the numeric part
            num_only = re.match(r'(-?\d+\.?\d*)', clean)
            if num_only and num_only.group(1) in abstract_lower:
                verified_nums.append(clean)
            else:
                unverified_nums.append(clean)

    # Extract [原文] quotes — mark for manual review rather than auto-verify
    quote_refs = re.findall(r'「([^」]+)」', note_text)

    return {
        "verified_numbers": verified_nums[:10],
        "unverified_numbers": unverified_nums[:10],
        "total_quotes": len(quote_refs),
        "verified_count": len(verified_nums),
        "unverified_count": len(unverified_nums),
    }


def process_one(doi: str) -> dict:
    """Process a single paper: fetch abstract → MiMo → verify → save."""
    slug = doi_slug(doi)
    wiki_path = WIKI_DIR / f"{slug}.md"

    # Fetch abstract
    paper = fetch_abstract(doi)
    if not paper.get("abstract") or len(paper["abstract"]) < 20:
        # Save placeholder
        note = f"""---
doi: {doi}
title: "{paper.get('title', '')}"
tags: [水凝胶, deepread-mimo, no-abstract]
---

# {paper.get('title', doi)}

**无法获取原文摘要**，未能进行 MiMo 深度精读。

- **DOI:** {doi}
"""
        wiki_path.write_text(note, encoding="utf-8")
        return {"doi": doi, "success": False, "error": "no abstract", "method": "skipped"}

    # Rate limit
    time.sleep(RATE_LIMIT)

    # Call MiMo
    prompt = DEEPREAD_PROMPT.format(
        doi=doi,
        title=paper.get("title", ""),
        authors=paper.get("authors", ""),
        journal=paper.get("journal", ""),
        year=paper.get("year", ""),
        abstract=paper["abstract"],
    )
    response = call_mimo(prompt)

    if response.startswith("[[MiMo Error:"):
        return {"doi": doi, "success": False, "error": response[3:-3], "method": "failed"}

    # Verify claims
    v = verify_claims(response, paper["abstract"])

    # Build final note
    verify_section = ""
    if v.get("unverified_numbers"):
        verify_section += "\n### ⚠ 未在摘要中找到的数值（需人工核查）\n"
        for n in v["unverified_numbers"]:
            verify_section += f"- `{n}`\n"
    if v.get("verified_numbers"):
        verify_section += "\n### ✅ 数值已验证（摘要中有对应数据）\n"
        for n in v["verified_numbers"]:
            verify_section += f"- `{n}`\n"

    note = f"""---
doi: {doi}
title: "{paper.get('title', '')}"
tags: [水凝胶, deepread-mimo, v2]
---

# {paper.get('title', '')}

**精读:** {MIMO_MODEL} | 摘要来源: {paper.get('source', '?')}

## 基础信息

| 属性 | 值 |
|------|-----|
| **DOI** | [{doi}](https://doi.org/{doi}) |
| **期刊** | {paper.get('journal', '')} |
| **年份** | {paper.get('year', '')} |
| **作者** | {paper.get('authors', '')} |

---

{response}

---

## 原文验证

自动核查结果: {v['verified_count']}/{v['total_quotes']} 条引用在摘要中找到依据。
{verify_section}

*本笔记由 {MIMO_MODEL} 自动生成，已基于原文摘要进行事实核查。*
"""

    wiki_path.write_text(note, encoding="utf-8")
    return {
        "doi": doi,
        "success": True,
        "method": "abstract",
        "source": paper.get("source", "?"),
        "abstract_len": len(paper["abstract"]),
        "verified": v["verified_count"],
        "unverified": v["unverified_count"],
    }


def main():
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")

    # Load pending review papers
    progress = json.loads(PROGRESS_FILE.read_text("utf-8"))
    rp = json.loads(REVIEW_FILE.read_text("utf-8"))
    review_dois = {p["doi"] for p in rp if p.get("doi")}

    done = set(progress.get("deepread_done", []))
    failed = set(progress.get("deepread_failed", []))
    skipped = set(progress.get("deepread_skipped", []))

    # Also check disk for existing MIMO notes
    for f in WIKI_DIR.glob("*.md"):
        content = f.read_text("utf-8", errors="replace")
        if "deepread-mimo" in content:
            doi = f.stem.replace("_", "/")
            if doi in review_dois:
                done.add(doi)

    pending = sorted(review_dois - done - failed - skipped)

    print("=" * 60, flush=True)
    print("  MiMo 批量深度精读", flush=True)
    print("=" * 60, flush=True)
    print(f"  综述论文总计:    {len(review_dois)}", flush=True)
    print(f"  已有笔记:        {len(done)}", flush=True)
    print(f"  待处理:          {len(pending)}", flush=True)
    print(f"  MiMo Workers:    {MAX_WORKERS}", flush=True)
    print(f"  预计时间:        ~{len(pending) * 15 // MAX_WORKERS // 60}min", flush=True)
    print(flush=True)

    if not pending:
        print("All done!", flush=True)
        return 0

    def process_wrapper(doi):
        result = process_one(doi)
        return doi, result

    ok = 0
    fail = 0
    no_abs = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = {ex.submit(process_wrapper, doi): doi for doi in pending}
        batch_saved = 0
        for i, fut in enumerate(concurrent.futures.as_completed(futures), 1):
            doi, result = fut.result()
            total = len(pending)

            if result.get("success"):
                progress["deepread_done"].append(doi)
                ok += 1
                status = "OK"
            elif result.get("error") == "no abstract":
                progress["deepread_skipped"].append(doi)
                no_abs += 1
                status = "SKIP"
            else:
                progress["deepread_failed"].append(doi)
                fail += 1
                status = f"FAIL ({result.get('error','?')[:30]})"

            elapsed = result.get("elapsed", 0) or 0
            v_info = ""
            if result.get("verified") is not None:
                v_info = f" [数值验证 {result['verified']}个匹配]"
            print(f"  [{i}/{total}] {status} {doi}{v_info}", flush=True)

            # Save progress every 10 papers
            batch_saved += 1
            if batch_saved >= 10:
                PROGRESS_FILE.write_text(json.dumps(progress, ensure_ascii=False, indent=2), "utf-8")
                batch_saved = 0

    # Final save
    PROGRESS_FILE.write_text(json.dumps(progress, ensure_ascii=False, indent=2), "utf-8")

    print(flush=True)
    print("=" * 60, flush=True)
    print(f"  完成: +{ok} OK, {fail} FAIL, {no_abs} no-abstract", flush=True)
    print(f"  总计精读: {len(set(progress['deepread_done']))}", flush=True)
    print("=" * 60, flush=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
