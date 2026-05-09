#!/usr/bin/env python3
"""Batch ingest: raw JSON → wiki literature notes.

Usage:
  python scripts/batch_ingest.py                   # process pending files
  python scripts/batch_ingest.py --mark-only       # just mark as processed
  python scripts/batch_ingest.py --check-only      # just check what's pending
"""

import json, os, sys, time

# Fix GBK encoding on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() in ("gbk", "gb2312"):
    sys.stdout.reconfigure(encoding="utf-8")
from datetime import date
from pathlib import Path

import requests

VAULT = Path("E:/工作区/knowledge-base")
RAW_DIR = VAULT / "raw"
WIKI_DIR = VAULT / "wiki"
TEMPLATE = WIKI_DIR / "templates" / "literature-note.md"
CROSSREF_MAILTO = "peach@njfu.edu.cn"
TOPIC_MAP = {
    "水凝胶": "hydrogel",
    "有机磷化学": "organophosphorus",
    "有机膦化学": "organophosphorus",
    "化学信息学": "cheminformatics",
    "化工设计竞赛": "chemdesign",
}


def get_topic(raw_subdir):
    """Infer topic from raw subdirectory name."""
    name = raw_subdir.name
    for k, v in TOPIC_MAP.items():
        if k in name:
            return v
    return name


def clean_doi(doi):
    return doi.replace("/", "_").replace(".", "_")


def enrich_from_crossref(doi):
    """Fetch metadata from Crossref API."""
    url = f"https://api.crossref.org/works/{doi}"
    headers = {"User-Agent": f"PeachClaw/1.0 (mailto:{CROSSREF_MAILTO})"}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code != 200:
            return None
        msg = r.json().get("message", {})
        title = ((msg.get("title") or [""])[0])
        authors = []
        for a in msg.get("author", []):
            given = a.get("given", "")
            family = a.get("family", "")
            authors.append(f"{family}, {given}" if family else given)
        journal = (msg.get("container-title") or [""])[0]
        year = None
        date_parts = msg.get("published-print", {}).get("date-parts") or \
                     msg.get("issued", {}).get("date-parts") or \
                     msg.get("created", {}).get("date-parts") or []
        if date_parts and date_parts[0]:
            year = date_parts[0][0]
        abstract = msg.get("abstract", "")[:2000] or ""
        return {
            "title": title,
            "authors": authors,
            "journal": journal,
            "year": year,
            "abstract": abstract,
        }
    except Exception as e:
        return None


def load_template():
    if TEMPLATE.exists():
        return TEMPLATE.read_text(encoding="utf-8")
    return None


def build_note(raw_data, enriched, topic):
    """Generate wiki note content."""
    doi = raw_data.get("doi", "")
    title_en = enriched.get("title") or raw_data.get("title_en", "")
    title_zh = raw_data.get("title_zh", "")
    authors = enriched.get("authors") or []
    journal = enriched.get("journal") or ""
    year = enriched.get("year") or ""
    abstract = enriched.get("abstract") or ""
    doi_slug = clean_doi(doi)

    today = date.today().isoformat()
    author_str = "; ".join(authors[:8])
    if len(authors) > 8:
        author_str += " et al."

    lines = []
    lines.append("---")
    lines.append(f"type: literature")
    lines.append(f"doi: {doi}")
    lines.append(f"topic: {topic}")
    lines.append(f"date: {today}")
    lines.append(f"rating: ⭐")
    lines.append(f"_audit: pending")
    lines.append(f"_audit_codex: pending")
    lines.append(f"tags: [{topic}{', deepread-codex' if abstract else ''}]")
    lines.append("---")
    lines.append("")
    lines.append(f"# {title_en}")
    lines.append("")
    lines.append(f"**中文标题**: {title_zh}")
    lines.append("")
    lines.append("## 基本信息")
    lines.append("")
    lines.append("| 属性 | 值 |")
    lines.append("|------|-----|")
    lines.append(f"| **DOI** | [{doi}](https://doi.org/{doi}) |")
    lines.append(f"| **期刊** | {journal} |")
    lines.append(f"| **作者** | {author_str} |")
    lines.append(f"| **年份** | {year} |")
    lines.append("")
    if abstract:
        lines.append("## 摘要")
        lines.append("")
        lines.append(f"> {abstract}")
        lines.append("")
    lines.append("## 核心贡献")
    lines.append("")
    lines.append("- *待补充*")
    lines.append("")
    lines.append("## 方法")
    lines.append("")
    lines.append("- *待补充*")
    lines.append("")
    lines.append("## 关键发现")
    lines.append("")
    lines.append("- *待补充*")
    lines.append("")
    lines.append("## 不足与展望")
    lines.append("")
    lines.append("- *待补充*")
    lines.append("")
    lines.append("## 相关文献")
    lines.append("")
    lines.append("- *待补充*")
    lines.append("")

    return "\n".join(lines)


def scan_pending():
    """Scan raw/ for files with status != processed."""
    pending = []
    for topic_dir in sorted(RAW_DIR.iterdir()):
        if not topic_dir.is_dir():
            continue
        for f in sorted(topic_dir.glob("*.json")):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                if data.get("status") != "processed":
                    pending.append((f, data, topic_dir))
            except Exception as e:
                print(f"  ! Error reading {f.name}: {e}")
    return pending


def mark_processed(filepath):
    """Set status=processed in raw JSON."""
    data = json.loads(filepath.read_text(encoding="utf-8"))
    data["status"] = "processed"
    data["date"] = date.today().isoformat()
    filepath.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  ✅ Marked: {filepath.name}")


def main():
    mode = "process"
    if "--mark-only" in sys.argv:
        mode = "mark"
    elif "--check-only" in sys.argv:
        mode = "check"

    pending = scan_pending()
    if not pending:
        print("No pending files to process.")
        return

    print(f"Found {len(pending)} pending file(s):")
    for f, data, _ in pending:
        doi = data.get("doi", "?")
        title = data.get("title_en", data.get("title", "?"))[:60]
        print(f"  - {f.parent.name}/{f.name}: {doi} | {title}")

    if mode == "check":
        return

    if mode == "mark":
        for f, _, _ in pending:
            mark_processed(f)
        return

    # mode == "process"
    template = load_template()
    if not template:
        print("Warning: template not found, using built-in format")

    for i, (f, data, topic_dir) in enumerate(pending):
        doi = data.get("doi", "")
        title = data.get("title_en", "?")[:60]
        topic = get_topic(topic_dir)
        print(f"\n[{i+1}/{len(pending)}] {title}...")

        # Enrich from Crossref
        enriched = None
        if doi:
            print(f"  Fetching Crossref: {doi}...")
            enriched = enrich_from_crossref(doi)
            time.sleep(0.2)

        if enriched:
            print(f"  Got: {enriched.get('journal', '?')} ({enriched.get('year', '?')})")
        else:
            print(f"  Crossref unavailable, using raw data only")
            enriched = {}

        # Generate wiki note
        content = build_note(data, enriched, topic)
        doi_slug = clean_doi(doi)
        wiki_path = WIKI_DIR / topic_dir.name / f"{doi_slug}.md"
        wiki_path.parent.mkdir(parents=True, exist_ok=True)
        wiki_path.write_text(content, encoding="utf-8")
        print(f"  📝 Written: {wiki_path.relative_to(VAULT)}")

        # Mark as processed
        mark_processed(f)

    print(f"\n✅ Done: {len(pending)} paper(s) ingested")


if __name__ == "__main__":
    main()
