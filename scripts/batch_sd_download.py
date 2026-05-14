#!/usr/bin/env python3
"""
Batch PDF download from ScienceDirect via Chrome CDP.
For each DOI: resolve via doi.org → SD article page → pdfft.
"""
import asyncio, json, re, sys, time
from pathlib import Path
from playwright.async_api import async_playwright

VAULT_ROOT = Path(r"E:\工作区\knowledge-base")
PDF_DIR = VAULT_ROOT / "raw" / "水凝胶" / "pdfs"
PROGRESS_FILE = VAULT_ROOT / "scripts" / "pipeline_progress.json"
PDF_DIR.mkdir(parents=True, exist_ok=True)

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

async def get_page_text(page, timeout=5):
    """Get page content safely."""
    try:
        return await page.content()
    except:
        return ""

async def prime_session(page):
    """Re-prime SD session to refresh CF clearance."""
    try:
        await page.goto("https://www.sciencedirect.com", wait_until="domcontentloaded", timeout=15000)
        # Wait for CF to resolve
        for _ in range(15):
            url = page.url
            if "sciencedirect.com" in url and "captcha" not in url.lower():
                break
            await asyncio.sleep(1)
        await asyncio.sleep(2)
        return True
    except:
        return False

async def download_sd_pdf(page, doi, pdf_path) -> bool:
    """Download PDF from ScienceDirect via DOI->SD->pdfft chain."""
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
        # Step 1: Resolve DOI -> SD article page
        try:
            await page.goto(f"https://doi.org/{doi}", wait_until="domcontentloaded", timeout=20000)
        except:
            pass
        await asyncio.sleep(2)

        # Step 2: Extract PII from URL
        current_url = page.url
        pii_match = re.search(r'/pii/([A-Za-z]?\d{10,})', current_url)
        pii = pii_match.group(1) if pii_match else None

        if not pii:
            sys.stdout.write(" noPII ")
            sys.stdout.flush()
            return False

        # Step 3: Navigate to pdfft (with retry)
        pdfft_url = f"https://www.sciencedirect.com/science/article/pii/{pii}/pdfft"

        for attempt in range(3):
            try:
                await page.goto(pdfft_url, wait_until="domcontentloaded", timeout=25000)
            except:
                pass

            # Step 4: Wait for PDF / S3 redirect
            for _ in range(15):
                if captured:
                    pdf_path.write_bytes(captured[0])
                    return True
                if 'pdf.sciencedirectassets.com' in page.url:
                    await asyncio.sleep(3)
                    if captured:
                        pdf_path.write_bytes(captured[0])
                        return True
                await asyncio.sleep(1)

            # Check if we got CF challenge
            html = ""
            try: html = await page.content()
            except: pass
            if "tdm-reservation" in html or "captcha" in html.lower():
                # CF challenge - re-prime and retry
                sys.stdout.write(f" CF-{attempt+1} ")
                sys.stdout.flush()
                await prime_session(page)
                continue

        return False

    except Exception as e:
        if captured:
            pdf_path.write_bytes(captured[0])
            return True
        return False
    finally:
        page.remove_listener("response", cap_pdf)


async def main():
    progress, pdf_done, pdf_failed = load_progress()

    rp = json.loads((VAULT_ROOT / "scripts" / "review_papers.json").read_text("utf-8"))
    review_dois = sorted({p["doi"] for p in rp if p.get("doi")})

    # Sync disk
    for doi in review_dois:
        if (PDF_DIR / f"{doi_slug(doi)}.pdf").exists() and doi not in pdf_done:
            pdf_done.add(doi)
            progress["pdf_done"].append(doi)
    save_progress(progress)

    # Only SD-paywalled papers (10.1016, 10.1017)
    todo = []
    for doi in review_dois:
        path = PDF_DIR / f"{doi_slug(doi)}.pdf"
        if not path.exists() and doi not in pdf_done and doi not in pdf_failed:
            if doi.startswith("10.1016"):
                todo.append(doi)

    print(f"Total: {len(review_dois)}, Have: {len(pdf_done)}, SD to download: {len(todo)}")
    if not todo:
        print("All done!")
        return

    async with async_playwright() as pw:
        browser = await pw.chromium.connect_over_cdp("http://127.0.0.1:9226")
        ctx = browser.contexts[0] if browser.contexts else await browser.new_context()
        await ctx.add_cookies(SD_COOKIES)
        page = await ctx.new_page()

        # Prime SD session
        print("Priming SD session...")
        try:
            await page.goto("https://www.sciencedirect.com", wait_until="domcontentloaded", timeout=20000)
            await asyncio.sleep(3)
        except:
            pass
        print(f"Session primed. Downloading {len(todo)} papers...\n")

        ok, fail = len(pdf_done), len(pdf_failed)
        for i, doi in enumerate(todo, 1):
            path = PDF_DIR / f"{doi_slug(doi)}.pdf"
            if path.exists():
                if doi not in pdf_done:
                    progress["pdf_done"].append(doi)
                    ok += 1
                continue

            sys.stdout.write(f"  [{i}/{len(todo)}] {doi} ")
            sys.stdout.flush()

            success = await download_sd_pdf(page, doi, path)

            if success and path.exists():
                progress["pdf_done"].append(doi)
                ok += 1
                print(f" OK {path.stat().st_size} bytes")
            else:
                progress["pdf_failed"].append(doi)
                fail += 1
                print(" FAIL")

            if i % 5 == 0:
                save_progress(progress)

        save_progress(progress)
        await page.close()

    final = len(list(PDF_DIR.glob("*.pdf")))
    print(f"\n=== Done ===")
    print(f"PDFs on disk: {final}")
    print(f"SD downloaded: {ok - 23} new")
    print(f"Failed: {fail}")

if __name__ == "__main__":
    import os
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    asyncio.run(main())
