#!/usr/bin/env python3
"""Batch import new DOIs: create raw JSON files → batch_ingest → wiki pages.

Usage:
  python scripts/batch_import_dois.py < dois.txt         # read DOIs from stdin
  python scripts/batch_import_dois.py --dois "doi1,doi2"  # inline DOIs
  python scripts/batch_import_dois.py --check             # just check what's pending
"""

import json, os, sys, time
from pathlib import Path
from datetime import date

sys.stdout.reconfigure(encoding='utf-8')

RAW_DIR = Path("E:/工作区/knowledge-base/raw/水凝胶")
EXISTING_DOIS_FILE = "C:/Users/23327/AppData/Local/Temp/existing_dois.txt"
BATCH_SCRIPT = Path("E:/工作区/knowledge-base/scripts/batch_ingest.py")


def load_existing_dois():
    """Load existing KB DOIs to avoid duplicates."""
    if not os.path.exists(EXISTING_DOIS_FILE):
        return set()
    with open(EXISTING_DOIS_FILE, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f if line.strip())


def check_raw_duplicates(dois):
    """Check which DOIs already have raw JSON files."""
    existing_raw = set()
    for f in RAW_DIR.glob("*.json"):
        try:
            data = json.loads(f.read_text(encoding='utf-8'))
            if data.get("doi"):
                existing_raw.add(data["doi"].strip())
        except:
            pass
    return existing_raw


def create_raw_json(doi, source="search"):
    """Create minimal raw JSON for a DOI."""
    doi_slug = doi.replace("/", "_")
    fpath = RAW_DIR / f"{doi_slug}.json"
    if fpath.exists():
        return False  # already exists

    data = {
        "doi": doi,
        "title_en": "pending",
        "source": source,
        "status": "pending",
        "date": date.today().isoformat()
    }
    fpath.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    return True


def main():
    if "--check" in sys.argv:
        existing = load_existing_dois()
        raw_existing = check_raw_duplicates([])
        print(f"Existing KB DOIs: {len(existing)}")
        print(f"Existing raw JSONs: {len(raw_existing)}")
        return

    # Read DOIs
    dois = []
    if "--dois" in sys.argv:
        idx = sys.argv.index("--dois")
        raw = sys.argv[idx + 1]
        dois = [d.strip() for d in raw.split(",") if d.strip()]
    else:
        dois = [line.strip() for line in sys.stdin if line.strip()]

    print(f"Received {len(dois)} DOIs")

    # Filter
    existing_kb = load_existing_dois()
    existing_raw = check_raw_duplicates(dois)

    new_dois = []
    skipped_kb = 0
    skipped_raw = 0
    for doi in dois:
        if doi in existing_kb:
            skipped_kb += 1
            continue
        if doi in existing_raw:
            skipped_raw += 1
            continue
        new_dois.append(doi)

    print(f"  - {skipped_kb} already in KB (wiki)")
    print(f"  - {skipped_raw} already in raw/")
    print(f"  - {len(new_dois)} new to import")

    if not new_dois:
        print("Nothing to do.")
        return

    # Create raw JSONs
    created = 0
    for doi in new_dois:
        if create_raw_json(doi):
            created += 1

    print(f"Created {created} raw JSON files in raw/水凝胶/")
    print(f"\nNow run: python scripts/batch_ingest.py")
    print(f"  (from E:\\工作区\\knowledge-base)")


if __name__ == "__main__":
    main()
