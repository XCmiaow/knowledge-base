#!/usr/bin/env python3
"""
hydrogel_batch_pipeline — 水凝胶全覆盖多并行 Pipeline

Phase 0: 清单编制（分类所有文献状态）
Phase 1: PDF 并行下载
Phase 2: Codex 多并行精读 → wiki 笔记
Phase 3: 验证 + 汇总

Usage:
  python scripts/hydrogel_batch_pipeline.py inventory   # 只看清单
  python scripts/hydrogel_batch_pipeline.py pdf         # 只下 PDF
  python scripts/hydrogel_batch_pipeline.py deepread     # 只精读
  python scripts/hydrogel_batch_pipeline.py all          # 全流程
  python scripts/hydrogel_batch_pipeline.py all --force  # 强制重读已有 deepread-codex
  python scripts/hydrogel_batch_pipeline.py all --workers 6
"""

import concurrent.futures, json, os, re, subprocess, sys, time, urllib.request, tempfile
from pathlib import Path

# Ensure codex_deepread is importable
sys.path.insert(0, str(Path(r"C:\Users\23327\.claude\skills\paper-ingest\scripts").resolve()))
try:
    from codex_deepread import check_codex, _codex_cmd, fetch_best_abstract
except ImportError:
    def check_codex():
        try:
            return subprocess.run(["codex", "--version"], capture_output=True, text=True, timeout=10).returncode == 0
        except Exception:
            return False
    def _codex_cmd(args):
        return ["codex"] + args
    fetch_best_abstract = None

# ====== Config ======
VAULT_ROOT = Path(r"E:\工作区\knowledge-base")
WIKI_DIR = VAULT_ROOT / "wiki" / "水凝胶"
RAW_DIR = VAULT_ROOT / "raw" / "水凝胶"
PDF_DIR = RAW_DIR / "pdfs"
PROGRESS_FILE = VAULT_ROOT / "scripts" / "pipeline_progress.json"

SCRIPT_DIR = Path(r"C:\Users\23327\.claude\skills\paper-ingest\scripts")
CODEX_SCRIPT = SCRIPT_DIR / "codex_deepread.py"

class Config:
    """Mutable global config."""
    workers = 4  # Parallel Codex instances
    review_only = False  # Only process review-relevant papers
    review_dois: set = set()
CODEX_TIMEOUT = 400  # Must be >= codex_deepread.py CODEX_TIMEOUT (360s) to allow full-text + fallback
S2_API = "https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}?fields=title,abstract,authors,year,journal,externalIds,isOpenAccess,openAccessPdf"

# ====== Progress helpers ======

def load_review_list():
    """Load review-relevant DOIs from review_papers.json."""
    rp = VAULT_ROOT / "scripts" / "review_papers.json"
    if not rp.exists():
        return set()
    data = json.loads(rp.read_text(encoding="utf-8"))
    return {p["doi"] for p in data if p.get("doi")}

def load_progress():
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    return {"pdf_done": [], "pdf_failed": [], "deepread_done": [], "deepread_failed": [], "deepread_skipped": []}

def save_progress(p):
    PROGRESS_FILE.write_text(json.dumps(p, ensure_ascii=False, indent=2), encoding="utf-8")

# ====== Phase 0: Inventory ======

def doi_slug(doi: str) -> str:
    return doi.replace("/", "_")

def extract_paper_id(path: Path) -> tuple[str, str] | None:
    """
    Extract paper identifier from file.
    Returns (id, id_type) where id_type is 'doi' or 'arxiv'.
    """
    content = path.read_text(encoding="utf-8", errors="replace")

    # Try YAML frontmatter first
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            fm = content[3:end]
            doi_val = None
            arxiv_val = None
            source_type = None
            for line in fm.splitlines():
                stripped = line.strip()
                if stripped.startswith("doi:"):
                    doi_val = stripped.split(":", 1)[1].strip().strip('"').strip("'")
                elif stripped.startswith("arxiv_id:"):
                    arxiv_val = stripped.split(":", 1)[1].strip().strip('"').strip("'")
                elif stripped.startswith("source_type:"):
                    source_type = stripped.split(":", 1)[1].strip().strip('"').strip("'")
            if doi_val:
                return (doi_val, "doi")
            if arxiv_val and source_type == "arxiv":
                return (f"arxiv:{arxiv_val}", "arxiv")
            if arxiv_val:
                return (f"arxiv:{arxiv_val}", "arxiv")

    # Try JSON (raw files)
    try:
        data = json.loads(content)
        doi = data.get("doi", "")
        if doi:
            return (doi, "doi")
    except json.JSONDecodeError:
        pass

    return None

def has_tag_in_file(path: Path, tag: str) -> bool:
    content = path.read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return False
    end = content.find("---", 3)
    if end == -1:
        return False
    return tag in content[:end]

def classify_paper(pid: str, wiki_path: Path | None):
    """Classify a paper's current state by ID."""
    if wiki_path is None:
        return "new_raw"
    if has_tag_in_file(wiki_path, "deepread-codex"):
        return "deepread_done"
    if has_tag_in_file(wiki_path, "deepread-mimo"):
        return "needs_upgrade"
    return "needs_first_deepread"

def build_inventory():
    """Build complete inventory of all papers and their status (recursive)."""
    print("[INVENTORY] Scanning wiki (recursive) and raw directories...", file=sys.stderr)

    # Collect all wiki .md files recursively
    wiki_papers = {}
    if WIKI_DIR.exists():
        for f in sorted(WIKI_DIR.rglob("*.md")):
            pid_info = extract_paper_id(f)
            if pid_info:
                pid, id_type = pid_info
                wiki_papers[pid] = {"path": f, "type": id_type}
            else:
                # Fallback: use filename without extension
                pid = f.stem
                wiki_papers[pid] = {"path": f, "type": "filename"}

    # Collect raw JSON files
    raw_papers = {}
    if RAW_DIR.exists():
        for f in RAW_DIR.glob("*.json"):
            pid_info = extract_paper_id(f)
            if pid_info:
                pid, id_type = pid_info
                raw_papers[pid] = {"path": f, "type": id_type}

    # Collect existing PDFs (by slug)
    existing_pdfs = set()
    if PDF_DIR.exists():
        for f in PDF_DIR.glob("*.pdf"):
            existing_pdfs.add(f.stem)

    # Classify all papers
    all_pids = set(wiki_papers.keys()) | set(raw_papers.keys())
    classified = {"new_raw": [], "needs_upgrade": [], "needs_first_deepread": [], "deepread_done": [], "total": len(all_pids)}

    for pid in sorted(all_pids):
        wiki_info = wiki_papers.get(pid)
        wiki_path = wiki_info["path"] if wiki_info else None
        category = classify_paper(pid, wiki_path)
        has_pdf = (pid.startswith("arxiv:") and f"arxiv_{pid.split(':')[1]}" in existing_pdfs) or (doi_slug(pid) in existing_pdfs)
        classified[category].append({"id": pid, "wiki": str(wiki_path) if wiki_path else None, "raw": str(raw_papers.get(pid, {}).get("path", "")), "has_pdf": has_pdf})

    # Stats
    pdf_total = sum(1 for c in classified.values() if isinstance(c, list) for p in c if p['has_pdf'])
    print(f"\n===== Inventory Report =====", file=sys.stderr)
    print(f"  Total papers:           {classified['total']}", file=sys.stderr)
    print(f"  deepread-codex (done):  {len(classified['deepread_done'])}", file=sys.stderr)
    print(f"  deepread-mimo (upgrade):{len(classified['needs_upgrade'])}", file=sys.stderr)
    print(f"  needs first deepread:   {len(classified['needs_first_deepread'])}", file=sys.stderr)
    print(f"  new raw (no wiki):      {len(classified['new_raw'])}", file=sys.stderr)
    print(f"  have PDFs:              {pdf_total}", file=sys.stderr)
    print(f"===========================\n", file=sys.stderr)

    return classified

def cmd_inventory():
    classified = build_inventory()
    # Apply review filter for display
    if Config.review_only and Config.review_dois:
        total = sum(len(v) for v in classified.values() if isinstance(v, list))
        filtered = sum(len([p for p in v if p["id"] in Config.review_dois]) for v in classified.values() if isinstance(v, list))
        print(f"\n[REVIEW] {filtered}/{total} papers match review scope\n", file=sys.stderr)

# ====== Phase 1: PDF Download ======

def try_scidown(doi: str) -> bool:
    """Try Sci-Hub to download PDF. Returns True if successful."""
    slug = doi_slug(doi)
    pdf_path = PDF_DIR / f"{slug}.pdf"
    if pdf_path.exists():
        return True

    PDF_DIR.mkdir(parents=True, exist_ok=True)

    scihub_domains = [
        "https://sci-hub.se",
        "https://sci-hub.ru",
        "https://sci-hub.st",
    ]

    for domain in scihub_domains:
        url = f"{domain}/{doi}"
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            resp = urllib.request.urlopen(req, timeout=30)
            content = resp.read()

            if len(content) > 50000 and content[:4] == b'%PDF':
                pdf_path.write_bytes(content)
                return True

            # Try to find PDF redirect
            html = content.decode("utf-8", errors="replace")
            # Look for embed/iframe/pdf url patterns
            pdf_urls = re.findall(r'(?:src|href)=["\']([^"\']+\.pdf[^"\']*)["\']', html)
            for pdf_url in pdf_urls:
                if pdf_url.startswith("//"):
                    pdf_url = "https:" + pdf_url
                elif pdf_url.startswith("/"):
                    pdf_url = domain + pdf_url
                try:
                    req2 = urllib.request.Request(pdf_url, headers={"User-Agent": "Mozilla/5.0"})
                    resp2 = urllib.request.urlopen(req2, timeout=30)
                    content2 = resp2.read()
                    if content2[:4] == b'%PDF':
                        pdf_path.write_bytes(content2)
                        return True
                except Exception:
                    continue
        except Exception:
            continue
    return False

def try_semantic_scholar_pdf(doi: str) -> bool:
    """Try Semantic Scholar OA PDF link."""
    slug = doi_slug(doi)
    pdf_path = PDF_DIR / f"{slug}.pdf"
    if pdf_path.exists():
        return True

    PDF_DIR.mkdir(parents=True, exist_ok=True)

    url = S2_API.format(doi=doi)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "CodexPipeline/1.0"})
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read().decode("utf-8"))

        oa = data.get("openAccessPdf") or {}
        if oa and "url" in oa:
            pdf_url = oa["url"]
            req2 = urllib.request.Request(pdf_url, headers={"User-Agent": "Mozilla/5.0"})
            resp2 = urllib.request.urlopen(req2, timeout=30)
            content = resp2.read()
            if len(content) > 50000 and content[:4] == b'%PDF':
                pdf_path.write_bytes(content)
                return True
    except Exception:
        pass
    return False

def try_europe_pmc_pdf(doi: str) -> bool:
    """Download OA PDF via Europe PMC REST API (accessible from China)."""
    slug = doi_slug(doi)
    pdf_path = PDF_DIR / f"{slug}.pdf"
    if pdf_path.exists():
        return True
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    try:
        # Get PMCID via S2 API
        s2_url = S2_API.format(doi=doi)
        req = urllib.request.Request(s2_url, headers={"User-Agent": "Mozilla/5.0"})
        import ssl
        ctx = ssl._create_unverified_context()
        resp = urllib.request.urlopen(req, timeout=15, context=ctx)
        data = json.loads(resp.read().decode("utf-8"))
        pmcid = data.get("externalIds", {}).get("PubMedCentral", "")
        if not pmcid:
            return False
        # Query Europe PMC for PDF URL
        ep_url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=PMCID:PMC{pmcid}&format=json&resultType=core"
        req2 = urllib.request.Request(ep_url, headers={"User-Agent": "Mozilla/5.0"})
        resp2 = urllib.request.urlopen(req2, timeout=15, context=ctx)
        ep_data = json.loads(resp2.read().decode("utf-8"))
        results = ep_data.get("resultList", {}).get("result", [])
        for r in results:
            for ft in r.get("fullTextUrlList", {}).get("fullTextUrl", []):
                if ft.get("availabilityCode") == "OA" and ft.get("documentStyle") == "pdf":
                    pdf_url = ft["url"]
                    req3 = urllib.request.Request(pdf_url, headers={"User-Agent": "Mozilla/5.0"})
                    resp3 = urllib.request.urlopen(req3, timeout=60, context=ctx)
                    content = resp3.read()
                    if content[:4] == b'%PDF':
                        pdf_path.write_bytes(content)
                        return True
    except Exception:
        pass
    return False

def download_pdf_for_paper(doi: str) -> bool:
    """Try multiple methods to download PDF."""
    slug = doi_slug(doi)
    pdf_path = PDF_DIR / f"{slug}.pdf"
    if pdf_path.exists():
        return True

    # Try Europe PMC first (accessible from China)
    if try_europe_pmc_pdf(doi):
        return True

    # Try S2 OA
    if try_semantic_scholar_pdf(doi):
        return True

    # Try Sci-Hub
    if try_scidown(doi):
        return True

    return False

def cmd_pdf():
    """Phase 1: Download PDFs in parallel."""
    progress = load_progress()
    pdf_done = set(progress.get("pdf_done", []))
    pdf_failed = set(progress.get("pdf_failed", []))

    classified = build_inventory()

    # Filter to review papers if --review flag
    if Config.review_only and Config.review_dois:
        for cat in classified:
            if isinstance(classified[cat], list):
                classified[cat] = [p for p in classified[cat] if p["id"] in Config.review_dois]
        print(f"[REVIEW] Filtered to {sum(len(v) for v in classified.values() if isinstance(v, list))} review papers", file=sys.stderr)

    # Collect all papers needing PDF (DOI papers only, arXiv handled separately)
    all_needed = []
    for cat in ["new_raw", "needs_upgrade", "needs_first_deepread", "deepread_done"]:
        for p in classified.get(cat, []):
            pid = p["id"]
            if pid.startswith("arxiv:"):
                continue  # Skip arXiv for now
            if not p["has_pdf"] and pid not in pdf_done and pid not in pdf_failed:
                all_needed.append(pid)

    if not all_needed:
        print("[PDF] All PDFs already downloaded or attempted.", file=sys.stderr)
        return

    print(f"[PDF] Downloading {len(all_needed)} PDFs with {Config.workers} workers...", file=sys.stderr)

    def dl(pid):
        ok = download_pdf_for_paper(pid)
        return pid, ok

    done_count = len(pdf_done)
    with concurrent.futures.ThreadPoolExecutor(max_workers=Config.workers) as ex:
        futures = {ex.submit(dl, pid): pid for pid in all_needed}
        for i, fut in enumerate(concurrent.futures.as_completed(futures), 1):
            pid, ok = fut.result()
            if ok:
                progress["pdf_done"].append(pid)
                done_count += 1
            else:
                progress["pdf_failed"].append(pid)
            save_progress(progress)

            total = len(all_needed)
            status = "✓" if ok else "✗"
            print(f"  [{i}/{total}] {status} {pid}", file=sys.stderr)

    print(f"\n[PDF] Done: {done_count} OK, {len(progress['pdf_failed'])} failed", file=sys.stderr)

# ====== Phase 2: Codex Deep Read (Parallel) ======

def validate_deepread_output(markdown: str) -> dict:
    """Check if Codex output has proper deepread format."""
    result = {"valid": True, "warnings": []}
    if not markdown or len(markdown) < 100:
        return {"valid": False, "warnings": ["Output too short or empty"]}
    if "[原文]" not in markdown:
        result["warnings"].append("No [原文] claims")
    if "[推断]" not in markdown:
        result["warnings"].append("No [推断] markers")
    # Check for error content pollution
    error_lines = [l for l in markdown.splitlines() if "ERROR:" in l]
    if error_lines:
        result["valid"] = False
        result["warnings"].append(f"Contains {len(error_lines)} GFW error log lines")
    if result["warnings"]:
        result["valid"] = False
    return result


def run_codex_deepread_for_paper(doi: str, topic: str = "水凝胶", max_retries: int = 2) -> dict:
    """
    Run Codex deep read for a single paper with retry logic.
    Uses existing codex_deepread.py script.
    """
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    last_error = ""

    for attempt in range(1, max_retries + 2):
        start = time.time()
        is_last = (attempt > max_retries)

        try:
            result = subprocess.run(
                [sys.executable, str(CODEX_SCRIPT), "read", doi, topic],
                capture_output=True, text=True, encoding="utf-8",
                timeout=CODEX_TIMEOUT, env=env,
            )
            elapsed = time.time() - start
        except subprocess.TimeoutExpired:
            elapsed = time.time() - start
            if not is_last:
                print(f"  [RETRY {attempt}/{max_retries}] {doi} (timeout, {elapsed:.0f}s)", file=sys.stderr)
                time.sleep(2)
                continue
            return {"doi": doi, "success": False, "elapsed": round(elapsed, 1), "error": "timeout", "method": "abstract"}
        except FileNotFoundError:
            elapsed = time.time() - start
            if not is_last:
                print(f"  [RETRY {attempt}/{max_retries}] {doi} (codex not found)", file=sys.stderr)
                time.sleep(2)
                continue
            return {"doi": doi, "success": False, "elapsed": round(elapsed, 1), "error": "codex not found", "method": "abstract"}
        except Exception as e:
            elapsed = time.time() - start
            if not is_last:
                print(f"  [RETRY {attempt}/{max_retries}] {doi} ({type(e).__name__}: {e})", file=sys.stderr)
                time.sleep(2)
                continue
            return {"doi": doi, "success": False, "elapsed": round(elapsed, 1), "error": str(e), "method": "abstract"}

        if result.returncode != 0:
            last_error = f"exit={result.returncode}"
            # Check for expected non-retryable failures
            stderr_lower = (result.stderr or "").lower()
            no_abstract = "no abstract" in stderr_lower
            is_timeout = "timeout" in stderr_lower
            if no_abstract or is_timeout:
                skip_reason = "timeout" if is_timeout else "no abstract"
                if is_last:
                    return {"doi": doi, "success": False, "elapsed": round(elapsed, 1), "error": skip_reason, "method": "abstract"}
                print(f"  [SKIP] {doi} ({skip_reason}, {elapsed:.0f}s)", file=sys.stderr)
                return {"doi": doi, "success": False, "elapsed": round(elapsed, 1), "error": skip_reason, "method": "abstract", "skipped": True}
            if not is_last:
                print(f"  [RETRY {attempt}/{max_retries}] {doi} ({last_error}, {elapsed:.0f}s)", file=sys.stderr)
                time.sleep(2)
                continue
            return {"doi": doi, "success": False, "elapsed": round(elapsed, 1), "error": last_error, "method": "abstract"}

        # Validate saved wiki page
        wiki_path = WIKI_DIR / f"{doi_slug(doi)}.md"
        valid = True
        if wiki_path.exists():
            note = wiki_path.read_text(encoding="utf-8", errors="replace")
            v = validate_deepread_output(note)
            if not v["valid"]:
                valid = False
                last_error = f"validation: {v['warnings']}"
                if not is_last:
                    print(f"  [RETRY {attempt}/{max_retries}] {doi} ({last_error})", file=sys.stderr)
                    time.sleep(2)
                    continue

        if valid:
            return {"doi": doi, "success": True, "elapsed": round(elapsed, 1), "method": "abstract", "exit_code": result.returncode}

    # All attempts exhausted without success
    return {"doi": doi, "success": False, "error": last_error or "max retries", "method": "abstract"}

def _run_abstract_deepread(doi: str, topic: str, env: dict) -> dict:
    """Use existing codex_deepread.py for abstract-based reading."""
    start = time.time()
    result = subprocess.run(
        [sys.executable, str(CODEX_SCRIPT), "read", doi, topic],
        capture_output=True, text=True, encoding="utf-8",
        timeout=CODEX_TIMEOUT, env=env,
    )
    elapsed = time.time() - start

    # Parse stdout for JSON result
    output_text = result.stdout.strip()
    json_match = re.search(r'\{.*\}', output_text, re.DOTALL)
    parsed = {}
    if json_match:
        try:
            parsed = json.loads(json_match.group())
        except json.JSONDecodeError:
            pass

    return {
        "doi": doi,
        "success": result.returncode == 0,
        "elapsed": round(elapsed, 1),
        "method": "abstract",
        "exit_code": result.returncode,
        "details": parsed,
        "stderr": result.stderr[-500:] if result.stderr else "",
    }

def _run_fulltext_deepread(doi: str, pdf_path: Path, topic: str, env: dict) -> dict:
    """
    Full-text deep read: extract PDF text → feed to Codex via temp file.
    Uses a comprehensive prompt that covers the full paper structure.
    """
    try:
        import fitz
        doc = fitz.open(str(pdf_path))
        full_text = ""
        for page in doc:
            full_text += page.get_text() + "\n"
        doc.close()
        # Limit to avoid token limits (roughly first 15000 chars of content)
        if len(full_text) > 20000:
            full_text = full_text[:20000] + "\n\n[...truncated at 20000 chars...]"
    except Exception:
        return {"doi": doi, "success": False, "error": "PDF text extraction failed", "method": "fulltext"}

    if not full_text.strip():
        return {"doi": doi, "success": False, "error": "Empty text from PDF", "method": "fulltext"}

    # Check Codex availability
    if not check_codex():
        return {"doi": doi, "success": False, "error": "Codex CLI not available", "method": "fulltext"}

    # Write text to temp file
    text_file = tempfile.mktemp(suffix=".txt", prefix=f"paper_{doi_slug(doi)}_")
    with open(text_file, "w", encoding="utf-8") as f:
        f.write(full_text)

    format_prompt = (
        f"You MUST output ONLY a markdown deep-reading note. No conversation. No commentary. No JSON wrapper.\n\n"
        f"---\n"
        f"doi: {doi}\n"
        f"title: \"(from full text)\"\n"
        f"tags: [水凝胶, deepread-codex, v2]\n"
        f"---\n\n"
        f"# Title (from paper)\n\n"
        f"**中文标题**:\n\n"
        f"## 基础信息\n\n"
        f"| 属性 | 值 |\n"
        f"|------|-----|\n"
        f"| **DOI** | [{doi}](https://doi.org/{doi}) |\n"
        f"| **精读方式** | 全文 |\n\n"
        f"## 摘要\n\n"
        f"> 2-3 sentence Chinese summary based on full text\n\n"
        f"## 核心贡献\n\n"
        f"- **[原文]「direct quote from text」** — Chinese explanation\n\n"
        f"## 方法\n\n"
        f"- **[原文]「quote describing method / experimental design」** — Chinese explanation\n\n"
        f"## 关键发现\n\n"
        f"- **[原文]「exact quote with quantitative data」** → Chinese explanation\n\n"
        f"## 图表要点\n\n"
        f"- **[原文]「key figure/table finding」** — Chinese interpretation\n\n"
        f"## 不足与展望\n\n"
        f"- **[推断]** limitation or future direction\n\n"
        f"## 与我课题的关联\n\n"
        f"- How this relates to hydrogel review\n\n"
        f"## CRITICAL RULES\n"
        f"1. Every factual claim needs `[原文]「exact quote」`\n"
        f"2. Every inference needs `[推断]` marker\n"
        f"3. Include ALL numbers, percentages\n"
        f"4. Use Chinese for explanations\n"
        f"5. Output NOTHING except raw markdown starting with `---`\n"
        f"6. Do NOT add ANY text before or after the markdown"
    )

    fmt_file = tempfile.mktemp(suffix=".md", prefix="format_fulltext_")
    with open(fmt_file, "w", encoding="utf-8") as f:
        f.write(format_prompt)

    prompt = (
        f"Read the format guide at {fmt_file} and the paper full text at {text_file}. "
        f"Generate a deep-reading note following the format exactly. "
        f"Output ONLY the raw markdown starting with ---. "
        f"No conversation, no commentary, no JSON wrapper."
    )

    out_file = tempfile.mktemp(suffix=".txt", prefix=f"codex_ft_{doi_slug(doi)}_")

    cmd = _codex_cmd(["exec", "--skip-git-repo-check", "--ephemeral", f"--output-last-message={out_file}", prompt])

    start = time.time()
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", timeout=CODEX_TIMEOUT)
        elapsed = time.time() - start

        for f in [text_file, fmt_file]:
            if os.path.exists(f): os.unlink(f)

        output_text = ""
        if os.path.exists(out_file):
            with open(out_file, encoding="utf-8") as f:
                output_text = f.read().strip()
            os.unlink(out_file)

        if not output_text and result.stdout:
            output_text = result.stdout.strip()

        if not output_text:
            return {"doi": doi, "success": False, "error": "Empty Codex response", "method": "fulltext", "elapsed": round(elapsed, 1)}

        # Save to wiki
        if output_text.startswith("```"):
            output_text = re.sub(r"^```(?:markdown)?\s*", "", output_text)
            output_text = re.sub(r"\s*```\s*$", "", output_text)

        wiki_path = WIKI_DIR / f"{doi_slug(doi)}.md"

        # Ensure frontmatter
        if not output_text.strip().startswith("---"):
            output_text = f"""---
doi: {doi}
tags: [水凝胶, deepread-codex, v2]
---

{output_text}"""

        wiki_path.write_text(output_text, encoding="utf-8")

        return {"doi": doi, "success": True, "elapsed": round(elapsed, 1), "method": "fulltext", "size": len(output_text)}

    except subprocess.TimeoutExpired:
        for f in [text_file, fmt_file]:
            if os.path.exists(f): os.unlink(f)
        return {"doi": doi, "success": False, "error": f"Codex timeout {CODEX_TIMEOUT}s", "method": "fulltext"}
    except Exception as e:
        for f in [text_file, fmt_file]:
            if os.path.exists(f): os.unlink(f)
        return {"doi": doi, "success": False, "error": str(e), "method": "fulltext"}

def cmd_deepread(force: bool = False):
    """Phase 2: Parallel Codex deep read."""
    progress = load_progress()
    deepread_done = set(progress.get("deepread_done", []))
    deepread_failed = set(progress.get("deepread_failed", []))
    deepread_skipped = set(progress.get("deepread_skipped", []))

    classified = build_inventory()

    # Filter to review papers if --review flag
    if Config.review_only and Config.review_dois:
        for cat in classified:
            if isinstance(classified[cat], list):
                classified[cat] = [p for p in classified[cat] if p["id"] in Config.review_dois]
        print(f"[REVIEW] Filtered to {sum(len(v) for v in classified.values() if isinstance(v, list))} review papers", file=sys.stderr)

    # Collect papers needing deepread (DOI only, arXiv skipped for now)
    todo = []
    for cat in ["new_raw", "needs_upgrade", "needs_first_deepread"]:
        for p in classified.get(cat, []):
            pid = p["id"]
            if pid.startswith("arxiv:"):
                continue  # Skip arXiv for now
            if pid in deepread_done:
                continue
            if pid in deepread_failed:
                continue
            if pid in deepread_skipped:
                continue
            todo.append(pid)

    if force:
        # Add already-done papers for re-read
        for p in classified.get("deepread_done", []):
            pid = p["id"]
            if pid.startswith("arxiv:"):
                continue
            if pid not in deepread_done:
                todo.append(pid)

    if not todo:
        print("[DEEPREAD] All papers already processed. Use --force to re-read.", file=sys.stderr)
        return

    print(f"[DEEPREAD] Processing {len(todo)} papers with {Config.workers} parallel Codex workers...", file=sys.stderr)
    print(f"[DEEPREAD] Estimated time: ~{len(todo) * 90 // Config.workers // 60}min", file=sys.stderr)
    print(f"[DEEPREAD] Papers will use {'full text (PDF)' if PDF_DIR.exists() and any(PDF_DIR.glob('*.pdf')) else 'abstract'} where available", file=sys.stderr)

    def process(doi):
        result = run_codex_deepread_for_paper(doi)
        return doi, result

    done_count = 0
    fail_count = len(deepread_failed)

    with concurrent.futures.ThreadPoolExecutor(max_workers=Config.workers) as ex:
        futures = {ex.submit(process, doi): doi for doi in todo}

        for i, fut in enumerate(concurrent.futures.as_completed(futures), 1):
            doi, result = fut.result()
            total = len(todo)

            if result.get("success"):
                progress["deepread_done"].append(doi)
                done_count += 1
                status = "✓"
            elif result.get("skipped"):
                progress["deepread_skipped"].append(doi)
                status = "–"
            else:
                progress["deepread_failed"].append(doi)
                fail_count += 1
                status = "✗"

            save_progress(progress)

            method = result.get("method", "abstract")
            elapsed = result.get("elapsed", 0)
            err = result.get("error", "")
            err_suffix = f" | {err}" if err else ""
            print(f"  [{i}/{total}] {status} {doi} ({method}, {elapsed}s){err_suffix}", file=sys.stderr)

    print(f"\n[DEEPREAD] Done: {done_count} OK, {fail_count} failed", file=sys.stderr)

# ====== Phase 3: Verify ======

def cmd_verify():
    """Phase 3: Verify all papers have deepread-codex notes."""
    classified = build_inventory()

    needs_work = []
    for cat in ["new_raw", "needs_upgrade", "needs_first_deepread"]:
        needs_work.extend(classified.get(cat, []))

    print(f"\n===== Verification =====", file=sys.stderr)
    print(f"  deepread-codex (done): {len(classified['deepread_done'])}", file=sys.stderr)
    print(f"  still needs work:      {len(needs_work)}", file=sys.stderr)
    print(f"  progress:              {len(classified['deepread_done'])}/{classified['total']} ({len(classified['deepread_done'])*100//max(classified['total'],1)}%)", file=sys.stderr)

    if needs_work:
        print(f"\n  Remaining papers:", file=sys.stderr)
        for p in needs_work[:10]:
            print(f"    - {p['id']}", file=sys.stderr)
        if len(needs_work) > 10:
            print(f"    ... and {len(needs_work)-10} more", file=sys.stderr)

    # Check PDF status
    pdf_count = 0
    if PDF_DIR.exists():
        pdf_count = len(list(PDF_DIR.glob("*.pdf")))
    print(f"\n  PDFs downloaded: {pdf_count}/{classified['total']}", file=sys.stderr)

    return needs_work

# ====== Main ======

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Hydrogel Batch Pipeline")
    parser.add_argument("command", choices=["inventory", "pdf", "deepread", "verify", "all"])
    parser.add_argument("--force", action="store_true", help="Force re-read existing deepread-codex papers")
    parser.add_argument("--workers", type=int, default=Config.workers, help=f"Parallel workers (default: {Config.workers})")
    parser.add_argument("--review", action="store_true", help="Only process review-relevant papers (纤维素+抗冻)")
    args = parser.parse_args()

    Config.workers = args.workers
    if args.review:
        Config.review_only = True
        Config.review_dois = load_review_list()
        print(f"[CONFIG] Review mode: {len(Config.review_dois)} papers in scope", file=sys.stderr)

    if args.command == "inventory":
        return cmd_inventory()
    elif args.command == "pdf":
        return cmd_pdf()
    elif args.command == "deepread":
        return cmd_deepread(force=args.force)
    elif args.command == "verify":
        return cmd_verify()
    elif args.command == "all":
        print("\n========== Phase 0: Inventory ==========\n", file=sys.stderr)
        cmd_inventory()
        print("\n========== Phase 1: PDF Download ==========\n", file=sys.stderr)
        cmd_pdf()
        print("\n========== Phase 2: Codex Deep Read ==========\n", file=sys.stderr)
        cmd_deepread(force=args.force)
        print("\n========== Phase 3: Verify ==========\n", file=sys.stderr)
        cmd_verify()
        print("\n========== All phases complete ==========\n", file=sys.stderr)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
