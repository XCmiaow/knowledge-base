#!/usr/bin/env python3
"""
Comprehensive multi-method PDF downloader for all 314 papers.
Priority: EPMC/S2 → Sci-Hub → CDP browser → direct URL patterns.
"""
import json, re, sys, time, urllib.request, ssl, asyncio
from pathlib import Path
from urllib.error import HTTPError, URLError
from collections import Counter
from playwright.async_api import async_playwright

VAULT_ROOT = Path(r"E:\工作区\knowledge-base")
PDF_DIR = VAULT_ROOT / "raw" / "水凝胶" / "pdfs"
PROGRESS_FILE = VAULT_ROOT / "scripts" / "pipeline_progress.json"
PDF_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
CTX = ssl._create_unverified_context()

# Existing SD cookies (already expired but kept for fallback)
SD_COOKIES = [
    {"name": "SD_REMOTEACCESS", "value": "eyJhY2NvdW50SWQiOiI1MzIzOCIsInRpbWVzdGFtcCI6MTc3ODcyMjA1OTIyMn0=", "domain": ".sciencedirect.com", "path": "/"},
    {"name": "wasShibboleth", "value": "true", "domain": ".sciencedirect.com", "path": "/"},
    {"name": "sd_access", "value": "eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiZGlyIn0..MUvz_2xUUobLxHXD2XHJrw.0TKH6dgFuB1_XCYUaeEWEPx3v4nJ8b3EK9gt1Fu520RRQhZTsEUF6n7t24Iovpg-PEQC3EHQ8MbAPdi7ZAu3N6lOlDw2GIg3WZTqfUmcEWMYgcOb0xiGyFO_ptn_LqZAhOEpQekbhh6m9PiOC9twuA.5bD5MKRUS9ZD3FUqDuxePg", "domain": ".sciencedirect.com", "path": "/"},
    {"name": "OptanonAlertBoxClosed", "value": "2026-04-17T05:27:19.966Z", "domain": ".sciencedirect.com", "path": "/"},
]

def doi_slug(doi): return doi.replace("/", "_")

def load_progress():
    p = json.loads(PROGRESS_FILE.read_text("utf-8"))
    return p, set(p.get("pdf_done", [])), set(p.get("pdf_failed", []))

def save_progress(p):
    PROGRESS_FILE.write_text(json.dumps(p, ensure_ascii=False, indent=2), "utf-8")

def dl(url, timeout=60, max_size=50*1024*1024):
    """Download URL and return bytes if it's a valid PDF."""
    req = urllib.request.Request(url, headers=HEADERS)
    resp = urllib.request.urlopen(req, timeout=timeout, context=CTX)
    data = resp.read()
    if data[:4] == b'%PDF' and len(data) > 10000 and len(data) <= max_size:
        return data
    return None

# ====== METHOD 1: EPMC (Europe PMC) ======
def try_epmc(doi):
    slug = doi_slug(doi)
    path = PDF_DIR / f"{slug}.pdf"
    if path.exists():
        return True
    time.sleep(0.3)
    try:
        url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:%22{doi}%22&format=json&resultType=core"
        req = urllib.request.Request(url, headers=HEADERS)
        resp = urllib.request.urlopen(req, timeout=15, context=CTX)
        data = json.loads(resp.read().decode("utf-8"))
        for r in data.get("resultList", {}).get("result", []):
            pmcid = r.get("pmcid", "")
            if pmcid:
                # Try direct EPMC PDF
                pmc_url = f"https://europepmc.org/articles/PMC{pmcid}?pdf=render"
                pdf_data = dl(pmc_url, 60)
                if pdf_data:
                    path.write_bytes(pdf_data)
                    print(f"  OK: {doi} (EPMC, {len(pdf_data)} bytes)")
                    return True
                # Try OA full text URLs
                for ft in r.get("fullTextUrlList", {}).get("fullTextUrl", []):
                    if ft.get("availabilityCode") == "OA" and ft.get("documentStyle") == "pdf":
                        pdf_data = dl(ft["url"], 60)
                        if pdf_data:
                            path.write_bytes(pdf_data)
                            print(f"  OK: {doi} (EPMC OA, {len(pdf_data)} bytes)")
                            return True
    except Exception:
        pass
    return False

# ====== METHOD 2: Semantic Scholar OA ======
def try_s2(doi):
    slug = doi_slug(doi)
    path = PDF_DIR / f"{slug}.pdf"
    if path.exists():
        return True
    time.sleep(1.1)
    try:
        url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}?fields=isOpenAccess,openAccessPdf"
        req = urllib.request.Request(url, headers=HEADERS)
        resp = urllib.request.urlopen(req, timeout=15, context=CTX)
        data = json.loads(resp.read().decode("utf-8"))
        oa = data.get("openAccessPdf") or {}
        if oa and "url" in oa:
            pdf_data = dl(oa["url"], 30)
            if pdf_data:
                path.write_bytes(pdf_data)
                print(f"  OK: {doi} (S2 OA, {len(pdf_data)} bytes)")
                return True
    except Exception:
        pass
    return False

# ====== METHOD 3: Sci-Hub ======
SCI_HUB_DOMAINS = [
    "https://sci-hub.ru",
    "https://sci-hub.st",
    "https://sci-hub.wf",
]

def try_scihub(doi):
    slug = doi_slug(doi)
    path = PDF_DIR / f"{slug}.pdf"
    if path.exists():
        return True

    for domain in SCI_HUB_DOMAINS:
        try:
            # Step 1: Fetch landing page
            req = urllib.request.Request(f"{domain}/{doi}", headers=HEADERS)
            resp = urllib.request.urlopen(req, timeout=30, context=CTX)
            html = resp.read().decode("utf-8", errors="replace")

            # Already a PDF (edge case)
            if html[:4] == '%PDF':
                path.write_bytes(html.encode())
                print(f"  OK: {doi} (Sci-Hub direct)")
                return True

            # Step 2: Extract PDF URL from citation_pdf_url meta tag
            m = re.search(r'<meta\s+name="citation_pdf_url"\s+content="([^"]+)"', html)
            if not m:
                m = re.search(r'<meta\s+content="([^"]+)"\s+name="citation_pdf_url"', html)
            if not m:
                # Try object tag
                m = re.search(r'<object[^>]*data="([^"]+\.pdf[^"]*)"', html)
            if not m:
                # Try download link
                m = re.search(r'class="download"[^>]*><a\s+href="([^"]+\.pdf[^"]*)"', html)

            if m:
                pdf_url = m.group(1)
                if pdf_url.startswith("//"):
                    pdf_url = "https:" + pdf_url
                elif pdf_url.startswith("/"):
                    pdf_url = domain + pdf_url

                pdf_data = dl(pdf_url, 60)
                if pdf_data:
                    path.write_bytes(pdf_data)
                    print(f"  OK: {doi} (Sci-Hub, {len(pdf_data)} bytes)")
                    return True
        except HTTPError as e:
            if e.code == 404:
                continue  # Not in Sci-Hub
        except Exception:
            continue
    return False

# ====== METHOD 4: CDP Browser ======
async def try_cdp(page, doi, sd_only=True):
    """Download via Chrome CDP. sd_only: only try Elsevier/SD papers."""
    slug = doi_slug(doi)
    path = PDF_DIR / f"{slug}.pdf"
    if path.exists():
        return True

    if sd_only and not any(x in doi for x in ["10.1016", "10.1017", "10.3390", "10.1002", "10.1021", "10.1039", "10.1038", "10.1007"]):
        return False

    captured = []
    async def cap_pdf(response):
        try:
            body = await response.body()
            if body[:4] == b'%PDF' and len(body) > 10000:
                captured.append(body)
        except:
            pass

    page.on("response", cap_pdf)
    try:
        # DOI -> SD article page
        try:
            await page.goto(f"https://doi.org/{doi}", wait_until="domcontentloaded", timeout=20000)
        except:
            pass
        await asyncio.sleep(2)

        current_url = page.url
        if "sciencedirect.com" in current_url:
            pii_match = re.search(r'/pii/([A-Za-z]?\d{10,})', current_url)
            if pii_match:
                pii = pii_match.group(1)
                pdfft_url = f"https://www.sciencedirect.com/science/article/pii/{pii}/pdfft"
                for attempt in range(3):
                    try:
                        await page.goto(pdfft_url, wait_until="domcontentloaded", timeout=25000)
                    except:
                        pass
                    for _ in range(15):
                        if captured:
                            path.write_bytes(captured[0])
                            return True
                        if 'pdf.sciencedirectassets.com' in page.url:
                            await asyncio.sleep(3)
                            if captured:
                                path.write_bytes(captured[0])
                                return True
                        await asyncio.sleep(1)
        elif "mdpi.com" in current_url:
            # MDPI OA - try /pdf endpoint
            pdf_url = current_url.rstrip('/') + '/pdf'
            try:
                await page.goto(pdf_url, wait_until="domcontentloaded", timeout=20000)
                await asyncio.sleep(2)
                for _ in range(10):
                    if captured:
                        path.write_bytes(captured[0])
                        return True
                    await asyncio.sleep(1)
            except:
                pass
        elif "wiley.com" in current_url:
            pdf_url = current_url.rstrip('/') + '/pdf'
            try:
                await page.goto(pdf_url, wait_until="domcontentloaded", timeout=20000)
                await asyncio.sleep(2)
                for _ in range(10):
                    if captured:
                        path.write_bytes(captured[0])
                        return True
                    await asyncio.sleep(1)
            except:
                pass
        elif "pubs.acs.org" in current_url:
            pdf_url = current_url.replace("/abs/", "/pdf/").replace("/full/", "/pdf/").rstrip('/') + '.pdf'
            try:
                await page.goto(pdf_url, wait_until="domcontentloaded", timeout=20000)
                await asyncio.sleep(2)
                for _ in range(10):
                    if captured:
                        path.write_bytes(captured[0])
                        return True
                    await asyncio.sleep(1)
            except:
                pass
        elif "pubs.rsc.org" in current_url or "rsc.org" in current_url:
            pdf_url = current_url.rstrip('/') + '.pdf'
            try:
                await page.goto(pdf_url, wait_until="domcontentloaded", timeout=20000)
                await asyncio.sleep(2)
                for _ in range(10):
                    if captured:
                        path.write_bytes(captured[0])
                        return True
                    await asyncio.sleep(1)
            except:
                pass
    except Exception:
        if captured:
            path.write_bytes(captured[0])
            return True
    finally:
        page.remove_listener("response", cap_pdf)
    return False

async def run_cdp_batch(todo_dois):
    """Run CDP browser batch for papers that need browser-based download."""
    if not todo_dois:
        return []

    print(f"\n=== CDP Browser batch: {len(todo_dois)} papers ===")

    async with async_playwright() as pw:
        browser = await pw.chromium.connect_over_cdp("http://127.0.0.1:9226")
        ctx = browser.contexts[0] if browser.contexts else await browser.new_context()
        page = await ctx.new_page()

        # Prime SD session
        try:
            await page.goto("https://www.sciencedirect.com", wait_until="domcontentloaded", timeout=20000)
            await asyncio.sleep(3)
        except:
            pass

        results = []
        for i, doi in enumerate(todo_dois, 1):
            path = PDF_DIR / f"{doi_slug(doi)}.pdf"
            if path.exists():
                results.append(doi)
                continue

            sys.stdout.write(f"  CDP [{i}/{len(todo_dois)}] {doi} ")
            sys.stdout.flush()

            success = await try_cdp(page, doi, sd_only=False)
            if success:
                results.append(doi)
                print("OK")
            else:
                print("FAIL")

        await page.close()

    return results

# ====== MAIN ======
def main():
    progress, pdf_done, pdf_failed = load_progress()

    rp = json.loads((VAULT_ROOT / "scripts" / "review_papers.json").read_text("utf-8"))
    review_dois = {p["doi"] for p in rp if p.get("doi")}

    # Sync existing PDFs
    for doi in sorted(review_dois):
        slug = doi_slug(doi)
        path = PDF_DIR / f"{slug}.pdf"
        if path.exists() and doi not in pdf_done:
            pdf_done.add(doi)
            progress["pdf_done"].append(doi)
    save_progress(progress)

    # Build todo list (not done, not already failed)
    todo = []
    for doi in sorted(review_dois):
        slug = doi_slug(doi)
        path = PDF_DIR / f"{slug}.pdf"
        if not path.exists() and doi not in pdf_done:
            # Don't skip previously failed - try again with new methods
            todo.append(doi)

    # Categorize
    pub_counts = Counter()
    for doi in todo:
        prefix = doi.split('/')[0]
        pub_counts[prefix] += 1

    print(f"Total review papers: {len(review_dois)}")
    print(f"Already have PDF:    {len(pdf_done)} ({len(list(PDF_DIR.glob('*.pdf')))} on disk)")
    print(f"Need to download:    {len(todo)}")
    print("\nBreakdown:")
    for prefix, count in sorted(pub_counts.items(), key=lambda x: -x[1]):
        print(f"  {prefix}: {count}")

    if not todo:
        print("\nAll done!")
        return

    api_ok = 0
    api_fail = 0

    # Phase 1: EPMC + S2 OA APIs (no CF issues, works from China)
    api_todo = [doi for doi in todo[:]]  # shallow copy since we'll iterate

    print(f"\n{'='*60}")
    print(f"PHASE 1: OA APIs (EPMC + S2)")
    print(f"{'='*60}")

    for i, doi in enumerate(api_todo, 1):
        path = PDF_DIR / f"{doi_slug(doi)}.pdf"
        if path.exists():
            continue

        sys.stdout.write(f"  API [{i}/{len(api_todo)}] {doi} ")
        sys.stdout.flush()

        if try_epmc(doi):
            progress["pdf_done"].append(doi)
            pdf_done.add(doi)
            api_ok += 1
        elif try_s2(doi):
            progress["pdf_done"].append(doi)
            pdf_done.add(doi)
            api_ok += 1
        else:
            api_fail += 1

        if (i % 10) == 0:
            save_progress(progress)

    save_progress(progress)
    print(f"\nPhase 1 result: +{api_ok} OK, {api_fail} remaining")

    # Phase 2: Sci-Hub (for older papers, works from China)
    remaining = [doi for doi in review_dois if doi not in pdf_done and
                 not (PDF_DIR / f"{doi_slug(doi)}.pdf").exists()]

    print(f"\n{'='*60}")
    print(f"PHASE 2: Sci-Hub ({len(remaining)} papers)")
    print(f"{'='*60}")

    sh_ok = 0
    sh_fail = 0

    for i, doi in enumerate(remaining, 1):
        path = PDF_DIR / f"{doi_slug(doi)}.pdf"
        if path.exists():
            continue

        sys.stdout.write(f"  SH [{i}/{len(remaining)}] {doi} ")
        sys.stdout.flush()

        if try_scihub(doi):
            progress["pdf_done"].append(doi)
            pdf_done.add(doi)
            sh_ok += 1
            print(f"OK")
        else:
            progress["pdf_failed"].append(doi)
            sh_fail += 1
            print(f"FAIL")

        if (i % 10) == 0:
            save_progress(progress)

    save_progress(progress)
    print(f"\nPhase 2 result: +{sh_ok} OK, {sh_fail} failed")

    # Phase 3: CDP Browser for everything else
    remaining = [doi for doi in review_dois if doi not in pdf_done and
                 not (PDF_DIR / f"{doi_slug(doi)}.pdf").exists()]

    if remaining:
        print(f"\n{'='*60}")
        print(f"PHASE 3: CDP Browser ({len(remaining)} papers)")
        print(f"{'='*60}")
        print("NOTE: SD session expired, need user to re-login in CDP Chrome window.")
        cdp_ok = asyncio.run(run_cdp_batch(remaining))
        for doi in cdp_ok:
            if doi not in pdf_done:
                progress["pdf_done"].append(doi)
                pdf_done.add(doi)
        save_progress(progress)
        print(f"\nPhase 3 result: +{len(cdp_ok)} OK")

    # Final report
    final_pdf = len(list(PDF_DIR.glob("*.pdf")))
    still_need = [doi for doi in review_dois if doi not in pdf_done and
                  not (PDF_DIR / f"{doi_slug(doi)}.pdf").exists()]

    print(f"\n{'='*60}")
    print(f"FINAL RESULT")
    print(f"{'='*60}")
    print(f"PDFs on disk: {final_pdf}")
    print(f"In progress:   {len(pdf_done)}")
    print(f"Still needed:  {len(still_need)}")

    if still_need:
        print("\nRemaining DOIs:")
        pub_rem = Counter()
        for doi in still_need:
            prefix = doi.split('/')[0]
            pub_rem[prefix] += 1
        for prefix, count in sorted(pub_rem.items(), key=lambda x: -x[1]):
            print(f"  {prefix}: {count}")

if __name__ == "__main__":
    import os
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    main()
