#!/usr/bin/env python3
"""
accept_literature.py — 夜间文献验收脚本

职责:
  1. 扫描 KB wiki (cron-lit 输出) + Obsidian vault
  2. 去重 (基于 state file)
  3. 元数据标准化 → unified JSON schema
  4. arXiv→DOI 解析 (CrossRef API)
  5. 按 topic 分组导出 JSON
  6. 更新 state file + 飞书摘要

Cron: 0 8 * * * cd /root/peach-claw-config && \
      python3 -u scripts/accept_literature.py >> LOGS/accept_literature.log 2>&1
"""

import json, os, re, sys, time, hashlib, urllib.request
from datetime import datetime, date
from pathlib import Path

import requests

# ====== 配置 ======
SCRIPT_DIR = Path(__file__).parent.resolve()
STATE_FILE = SCRIPT_DIR / "../STATE/accept_state.json"
EXPORT_DIR = SCRIPT_DIR / "../EXPORT"
LOG_DIR = SCRIPT_DIR / "../LOGS"

KB_BASE = Path("/root/.openclaw/knowledge-base/wiki")
OBSIDIAN_BASE = Path("/root/obsidian-vault/Literature")

TOPICS = ["水凝胶", "有机膦化学", "化学信息学", "化工设计竞赛"]
# 目录别名 → 标准 topic 名（目录结构权威，frontmatter 不可信）
TOPIC_NORMALIZE = {
    "水凝胶": "水凝胶", "hydrogel": "水凝胶",
    "有机膦化学": "有机膦化学", "有机磷化学": "有机膦化学",
    "化学信息学": "化学信息学", "cheminformatics": "化学信息学",
    "化工设计竞赛": "化工设计竞赛", "化工设计": "化工设计竞赛", "chemdesign": "化工设计竞赛",
}
# topic → ASCII 文件名（避免 SCP 到 Windows 乱码）
TOPIC_FILENAME = {
    "水凝胶": "hydrogel",
    "有机膦化学": "organophosphorus",
    "化学信息学": "cheminformatics",
    "化工设计竞赛": "chemdesign",
}

CROSSREF_URL = "https://api.crossref.org/works"
CROSSREF_MAILTO = "peach@njfu.edu.cn"

# Feishu
FEISHU_APP_ID = "cli_a92c37b572e25cb6"
FEISHU_SECRET = "COGqduOB6EaX6Pb9GvgufgCVdPHwg76k"
FEISHU_CHAT_ID = "oc_6117beeff70df230c47e9ebbf28cd7f9"
FEISHU_PUSH_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"


# ====== 日志 ======
LOG_FILE = LOG_DIR / "accept_literature.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


# ====== Feishu 通知 ======

def feishu_push(text):
    try:
        req = urllib.request.Request(
            FEISHU_PUSH_URL,
            data=json.dumps({"app_id": FEISHU_APP_ID, "app_secret": FEISHU_SECRET}).encode(),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            token_data = json.load(resp)
        token = token_data.get("tenant_access_token", "")
        if not token:
            return
        payload = {
            "receive_id": FEISHU_CHAT_ID,
            "msg_type": "text",
            "content": json.dumps({"text": text}),
        }
        req2 = urllib.request.Request(
            "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
        )
        with urllib.request.urlopen(req2, timeout=5):
            pass
    except Exception as e:
        log(f"  Feishu push failed: {e}")


# ====== State 管理 ======

def load_state():
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {"last_run": None, "processed_dois": [], "processed_arxiv_ids": [], "processed_title_hashes": []}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def title_hash(title):
    return hashlib.md5(title.strip().lower().encode()).hexdigest()


def is_processed(state, doi=None, arxiv_id=None, title=None):
    if doi and doi in state["processed_dois"]:
        return True
    if arxiv_id and arxiv_id in state["processed_arxiv_ids"]:
        return True
    if title and title_hash(title) in state["processed_title_hashes"]:
        return True
    return False


def mark_processed(state, doi=None, arxiv_id=None, title=None):
    if doi and doi not in state["processed_dois"]:
        state["processed_dois"].append(doi)
    if arxiv_id and arxiv_id not in state["processed_arxiv_ids"]:
        state["processed_arxiv_ids"].append(arxiv_id)
    if title:
        h = title_hash(title)
        if h not in state["processed_title_hashes"]:
            state["processed_title_hashes"].append(h)


# ====== KB Wiki 解析 ======

def parse_arxiv_format(text):
    """解析 cron-lit.py 的 key:: value 格式"""
    result = {}
    for line in text.split("\n"):
        m = re.match(r"^(\w[\w\s]+)::\s*(.+)$", line)
        if m:
            result[m.group(1).strip()] = m.group(2).strip()
    parts = text.split("---", 1)
    if len(parts) > 1:
        result["abstract"] = parts[1].strip()[:2000]
    return result


def parse_simple_frontmatter(text):
    """解析 --- 包围的简单 YAML 类 frontmatter"""
    m = re.match(r"^---\s*\n(.*?)\n(?:---|\.\.\.)", text, re.DOTALL)
    if not m:
        return {}
    result = {}
    for line in m.group(1).split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip("\"'")
            if val.startswith("[") and val.endswith("]"):
                val = [v.strip().strip("\"'") for v in val[1:-1].split(",")]
            result[key] = val
    return result


def _resolve_topic(filepath):
    """从目录名推断标准 topic 名（目录权威）"""
    path = str(filepath)
    for dirname, standard in TOPIC_NORMALIZE.items():
        if f"/{dirname}/" in path:
            return standard
    return "unknown"


def _normalize_topic(name):
    """把各种 topic 别名归一化到标准名"""
    return TOPIC_NORMALIZE.get(name, name)


def _parse_int(val):
    if not val:
        return None
    try:
        return int(val)
    except (ValueError, TypeError):
        m = re.search(r"\b(?:19|20)\d{2}\b", str(val))
        return int(m.group()) if m else None


def _extract_abstract(text):
    for header in ["## 中文摘要", "## 摘要", "## Abstract"]:
        m = re.search(rf"{re.escape(header)}\s*\n+(.*?)(?:\n##|\Z)", text, re.DOTALL)
        if m:
            return m.group(1).strip()[:2000]
    for line in text.split("\n"):
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith("---") and len(line) > 30:
            return line[:2000]
    return ""


def _parse_authors(val):
    if isinstance(val, str):
        return [a.strip().rstrip(".").strip() for a in val.split(",") if a.strip()]
    if isinstance(val, list):
        return val
    return []


def parse_kb_file(filepath):
    """解析 KB wiki 单篇文献"""
    text = Path(filepath).read_text(encoding="utf-8", errors="replace")

    # 尝试 arXiv 格式
    meta = parse_arxiv_format(text)
    if meta.get("ID") and meta.get("Type") == "arXiv":
        return {
            "source_pipeline": "cron-lit",
            "source_db": "arXiv",
            "source_topic": _resolve_topic(filepath),
            "arxiv_id": meta["ID"].replace("arXiv:", ""),
            "title": meta.get("Title", ""),
            "authors": _parse_authors(meta.get("Authors", "")),
            "year": _parse_int(meta.get("Year")),
            "url": meta.get("URL", ""),
            "abstract": meta.get("abstract", ""),
            "doi": "",
            "journal": "",
        }

    # 尝试 YAML frontmatter
    front = parse_simple_frontmatter(text)
    if front.get("doi") or front.get("type") == "literature":
        title = front.get("title", "")
        if not title:
            for line in text.split("\n"):
                if line.startswith("# ") and not line.startswith("## "):
                    title = line[2:].strip()
                    break
        return {
            "source_pipeline": "kb-wiki",
            "source_db": front.get("source", ""),
            "source_topic": _resolve_topic(filepath),  # 以目录为准，忽略 frontmatter topic
            "doi": front.get("doi", ""),
            "title": title,
            "title": title,
            "authors": _parse_authors(front.get("authors", "")),
            "year": _parse_int(front.get("year") or front.get("date", "")[:4]),
            "journal": front.get("journal", ""),
            "url": front.get("url", front.get("source_url", "")),
            "abstract": _extract_abstract(text),
            "arxiv_id": "",
        }

    return None


# ====== Obsidian vault 解析 ======

def parse_obsidian_file(filepath):
    """解析 literature_pipeline 输出的深读笔记"""
    text = Path(filepath).read_text(encoding="utf-8", errors="replace")
    front = parse_simple_frontmatter(text)
    if not front.get("doi"):
        return None

    title = front.get("title", "")
    if not title:
        for line in text.split("\n"):
            if line.startswith("# ") and not line.startswith("## "):
                title = line[2:].strip()
                break

    authors = []
    if isinstance(front.get("authors"), str):
        authors = [a.strip() for a in front["authors"].split(";") if a.strip()]
    elif isinstance(front.get("authors"), list):
        authors = front["authors"]

    tags = front.get("tags", [])
    if isinstance(tags, str):
        tags = [t.strip().strip("[]\"'") for t in tags.split(",") if t.strip()]

    return {
        "source_pipeline": "literature_pipeline",
        "source_db": front.get("source", "crossref"),
        "source_topic": "水凝胶",
        "doi": front.get("doi", ""),
        "title": title,
        "authors": authors,
        "year": _parse_int(front.get("year")),
        "journal": front.get("journal", ""),
        "abstract": _extract_abstract(text),
        "url": f"https://doi.org/{front['doi']}" if front.get("doi") else "",
        "arxiv_id": "",
    }


# ====== arXiv->DOI 解析 (CrossRef) ======

def resolve_doi(title):
    if not title or len(title) < 10:
        return None
    params = {
        "query.title": title[:200],
        "rows": 3,
        "sort": "relevance",
        "order": "desc",
        "mailto": CROSSREF_MAILTO,
    }
    headers = {"User-Agent": f"PeachClaw/1.0 (mailto:{CROSSREF_MAILTO})"}
    try:
        r = requests.get(CROSSREF_URL, params=params, headers=headers, timeout=15)
        if r.status_code != 200:
            return None
        items = r.json().get("message", {}).get("items", [])
        if not items:
            return None
        best = items[0]
        best_title = ((best.get("title") or [""])[0] or "").lower().rstrip(".")
        query_title = title.lower().rstrip(".")
        if best_title not in query_title and query_title not in best_title:
            return None
        doi = best.get("DOI", "")
        if not doi:
            return None
        journal = (best.get("container-title") or [""])[0]
        pub_date = best.get("published-print", {}).get("date-parts", [[None]])[0]
        return {"doi": doi, "journal": journal, "year": pub_date[0] if pub_date else None}
    except Exception as e:
        log(f"  CrossRef error: {e}")
        return None


# ====== 扫描 ======

def scan_kb():
    papers = []
    for topic in TOPICS:
        topic_dir = KB_BASE / topic
        if not topic_dir.exists():
            continue
        count = 0
        for f in sorted(topic_dir.glob("*.md")):
            try:
                p = parse_kb_file(f)
                if p:
                    papers.append(p)
                    count += 1
            except Exception as e:
                log(f"  ERROR {f.name}: {e}")
        log(f"  {topic}: {count} 篇")
    return papers


def scan_obsidian():
    papers = []
    if not OBSIDIAN_BASE.exists():
        return papers
    count = 0
    for year_dir in sorted(OBSIDIAN_BASE.glob("*")):
        if not year_dir.is_dir():
            continue
        for f in sorted(year_dir.glob("*.md")):
            try:
                p = parse_obsidian_file(f)
                if p:
                    papers.append(p)
                    count += 1
            except Exception as e:
                log(f"  ERROR {f.name}: {e}")
    log(f"  Obsidian 深读笔记: {count} 篇")
    return papers


# ====== 主流程 ======

def main():
    log("=" * 60)
    log("📋 文献验收启动")
    log(f"  KB: {KB_BASE}")
    log(f"  Obsidian: {OBSIDIAN_BASE}")

    state = load_state()
    log(f"  已有状态: {len(state['processed_dois'])} DOIs, {len(state['processed_arxiv_ids'])} arXiv IDs")

    # 阶段1: 扫描
    log("\n[阶段1] 扫描 KB wiki...")
    kb_papers = scan_kb()

    log("\n[阶段1] 扫描 Obsidian vault...")
    obsidian_papers = scan_obsidian()

    # 去重 (Obsidian pipeline 优先)
    all_papers = kb_papers + obsidian_papers
    seen = {}
    for p in all_papers:
        pid = p.get("doi") or p.get("arxiv_id") or str(id(p))
        if pid in seen:
            if p.get("source_pipeline") == "literature_pipeline":
                seen[pid] = p
        else:
            seen[pid] = p
    deduped = list(seen.values())
    log(f"\n  去重后: {len(deduped)} 篇 (原始 {len(all_papers)})")

    # 阶段2: state 去重
    log("\n[阶段2] 与历史 state 去重...")
    new_papers = []
    for p in deduped:
        if not is_processed(state, doi=p.get("doi"), arxiv_id=p.get("arxiv_id"), title=p.get("title")):
            new_papers.append(p)
    log(f"  新增: {len(new_papers)} 篇")

    if not new_papers:
        state["last_run"] = datetime.now().isoformat()
        save_state(state)
        log("\n✅ 无新增文献")
        return

    # 阶段3: 标准化
    log("\n[阶段3] 元数据标准化...")
    for p in new_papers:
        p.setdefault("doi", "")
        p.setdefault("arxiv_id", "")
        p.setdefault("title", "")
        p.setdefault("journal", "")
        p.setdefault("abstract", "")
        p.setdefault("url", "")
        p.setdefault("authors", [])
        p.setdefault("year", None)

    # 阶段4: arXiv->DOI 解析
    arxiv_no_doi = [p for p in new_papers if p.get("arxiv_id") and not p.get("doi")]
    if arxiv_no_doi:
        log(f"\n[阶段4] arXiv->DOI 解析 ({len(arxiv_no_doi)} 篇)...")
        resolved = 0
        for i, p in enumerate(arxiv_no_doi):
            log(f"  [{i+1}/{len(arxiv_no_doi)}] {p['title'][:50]}...")
            result = resolve_doi(p["title"])
            if result:
                p["doi"] = result["doi"]
                if not p.get("journal"):
                    p["journal"] = result.get("journal", "")
                if not p.get("year"):
                    p["year"] = result.get("year")
                resolved += 1
                log(f"    -> DOI: {result['doi']}")
            else:
                log(f"    -> 无匹配")
            time.sleep(0.2)
        log(f"  解析成功: {resolved}/{len(arxiv_no_doi)}")
    else:
        log("\n[阶段4] 无 arXiv 论文需要解析")

    # 阶段5: 按 topic 导出 JSON
    log("\n[阶段5] 按 topic 导出 JSON...")
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    by_topic = {}
    for p in new_papers:
        topic = _normalize_topic(p.get("source_topic", "unknown"))
        by_topic.setdefault(topic, []).append(p)

    export_files = []
    for topic, papers in sorted(by_topic.items()):
        date_str = date.today().isoformat()
        safe_name = TOPIC_FILENAME.get(topic, topic)
        filename = f"{safe_name}_{date_str}.json"
        filepath = EXPORT_DIR / filename
        records = []
        for p in papers:
            records.append({
                "type": "preprint" if (p.get("arxiv_id") and not p.get("doi")) else "article",
                "title": p["title"],
                "authors": p["authors"],
                "year": p["year"],
                "doi": p.get("doi", ""),
                "arxiv_id": p.get("arxiv_id", ""),
                "journal": p.get("journal", ""),
                "abstract": p.get("abstract", "")[:2000],
                "source_url": p.get("url", ""),
                "source_topic": topic,
                "source_db": p.get("source_db", ""),
                "source_pipeline": p.get("source_pipeline", ""),
            })
        filepath.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
        export_files.append((topic, filename, len(records)))
        log(f"  {topic}: {len(records)} 篇 -> {filename}")

    # 阶段6: 更新 state
    log("\n[阶段6] 更新 state...")
    for p in new_papers:
        mark_processed(state, doi=p.get("doi"), arxiv_id=p.get("arxiv_id"), title=p.get("title"))
    state["last_run"] = datetime.now().isoformat()
    save_state(state)
    log(f"  总记录: {len(state['processed_dois'])} DOIs, {len(state['processed_arxiv_ids'])} arXiv IDs")

    # 阶段7: 摘要 + 飞书推送
    no_doi = [p for p in new_papers if not p.get("doi")]
    no_doi_arxiv = [p for p in no_doi if p.get("arxiv_id")]

    log("\n" + "=" * 60)
    log("📋 验收摘要")
    log(f"  扫描 {len(all_papers)} 篇 -> 新增 {len(new_papers)} 篇")
    if arxiv_no_doi:
        log(f"  arXiv->DOI 成功: {len(arxiv_no_doi) - len(no_doi_arxiv)}/{len(arxiv_no_doi)}")
    if no_doi:
        log(f"  ! {len(no_doi)} 篇无 DOI (arXiv: {len(no_doi_arxiv)})")
        for p in no_doi[:3]:
            log(f"    - {p.get('title','?')[:60]}")
    for topic, fn, cnt in export_files:
        log(f"  EXPORT/{fn}: {cnt} 篇")
    log("完成")

    summary = f"文献验收报告 | {date.today().isoformat()}\n扫描 {len(all_papers)} 篇 -> 新增 {len(new_papers)} 篇"
    for topic, fn, cnt in export_files:
        summary += f"\n  +{cnt} {topic}"
    if no_doi:
        summary += f"\n  ! {len(no_doi)} 篇无 DOI"
    feishu_push(summary)


if __name__ == "__main__":
    main()
