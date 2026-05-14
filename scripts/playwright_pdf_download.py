#!/usr/bin/env python3
"""
Playwright PDF downloader — connects to your existing Chrome via CDP
to bypass Cloudflare using YOUR live browser session.

Usage:
  1. Close all Chrome windows
  2. Start Chrome with remote debugging:
     "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
  3. In that Chrome, sign in to ScienceDirect via your institution
  4. Run this script:
     python scripts/playwright_pdf_download.py
"""
import asyncio, json, os, re, sys, time
from pathlib import Path

VAULT_ROOT = Path(r"E:\工作区\knowledge-base")
PDF_DIR = VAULT_ROOT / "raw" / "水凝胶" / "pdfs"
PROGRESS_FILE = VAULT_ROOT / "scripts" / "pipeline_progress.json"
PDF_DIR.mkdir(parents=True, exist_ok=True)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

def doi_slug(doi: str) -> str: return doi.replace("/", "_")

def load_review_dois():
    rp = json.loads((VAULT_ROOT / "scripts" / "review_papers.json").read_text("utf-8"))
    return {p["doi"] for p in rp if p.get("doi")}

def load_progress():
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text("utf-8"))
    return {"pdf_done": [], "pdf_failed": []}

def save_progress(p):
    PROGRESS_FILE.write_text(json.dumps(p, ensure_ascii=False, indent=2), "utf-8")

def pdf_path(doi):
    return PDF_DIR / f"{doi_slug(doi)}.pdf"

# ====== Download logic per publisher ======

async def dl_elsevier(page, doi, pii):
    """Download PDF from ScienceDirect via institutional access."""
    # Step 1: Get access key from linkinghub
    lh_url = f"https://linkinghub.elsevier.com/retrieve/pii/{pii}"
    print(f"    LH: {lh_url[:80]}")
    try:
        resp = await page.goto(lh_url, wait_until="domcontentloaded", timeout=15000)
        html = await page.content()
        key_m = re.search(r'name="key"\s+value="([^"]+)"', html)
        redir_m = re.search(r'name="redirectURL"\s+value="([^"]+)"', html)
        if not key_m or not redir_m:
            print(f"    No access key found (status={resp.status if resp else '?'})")
            return False
        key, redirect = key_m.group(1), redir_m.group(1)
        access_url = f"https://linkinghub.elsevier.com/retrieve/articleSelectSinglePerm?Redirect={redirect}&key={key}"
        print(f"    Access URL (key={key[:16]}...)")
    except Exception as e:
        print(f"    LH error: {e}")
        return False

    # Step 2: Follow access redirect to SD — now in user's real browser with real session
    try:
        resp = await page.goto(access_url, wait_until="networkidle", timeout=30000)
        final = page.url
        print(f"    SD: {final[:100]}")
        html = await page.content()

        if "sign in" in html.lower()[:3000]:
            print(f"    -> Sign-in page — cookies expired or not logged in via browser")
            return False
        if "access denied" in html.lower()[:3000] or resp.status in (403, 401):
            print(f"    -> Access denied ({resp.status})")
            return False
        if resp.status == 200:
            # Try pdfft
            pdfft_url = f"https://www.sciencedirect.com/science/article/pii/{pii}/pdfft"
            print(f"    PDFFT: {pdfft_url[:80]}")
            try:
                resp2 = await page.goto(pdfft_url, wait_until="networkidle", timeout=30000)
                if resp2 and resp2.status == 200:
                    # Check if browser shows PDF
                    if "pdf" in page.url.lower():
                        # Get PDF content
                        pdf_data = await page.evaluate("""
                            () => document.body ? document.body.innerText : ''
                        """)
                        # Actually, if the browser navigates to a PDF, we need to download via CDP
                        async with page.expect_download(timeout=10000) as dl_info:
                            pass
                        dl = await dl_info.value
                        await dl.save_as(str(pdf_path(doi)))
                        print(f"    Downloaded OK ({pdf_path(doi).stat().st_size} bytes)")
                        return True
                    # Try clicking download button
                    for btn_text in ["Download", "PDF", "Save PDF", "full text"]:
                        try:
                            btn = page.locator(f'text="{btn_text}"').first
                            if await btn.is_visible(timeout=2000):
                                async with page.expect_download(timeout=15000) as dl_info:
                                    await btn.click()
                                dl = await dl_info.value
                                await dl.save_as(str(pdf_path(doi)))
                                print(f"    Downloaded via '{btn_text}'")
                                return True
                        except:
                            pass
                print(f"    PDFFT status={resp2.status if resp2 else '?'}")
            except Exception as e:
                print(f"    PDFFT error: {e}")
    except Exception as e:
        print(f"    SD error: {e}")
    return False


async def dl_mdpi(page, doi):
    """Download from MDPI (OA publisher)."""
    m = re.search(r'10\.3390/(\w+)(\d+)', doi)
    if not m:
        return False
    journal, aid = m.group(1), m.group(2)
    pdf_url = f"https://www.mdpi.com/{journal}/{aid}/pdf"
    print(f"    MDPI: {pdf_url[:80]}")
    for _ in range(3):
        try:
            resp = await page.goto(pdf_url, wait_until="networkidle", timeout=30000)
            if resp and resp.status == 200:
                if "pdf" in page.url.lower():
                    async with page.expect_download(timeout=10000) as dl_info:
                        pass
                    dl = await dl_info.value
                    await dl.save_as(str(pdf_path(doi)))
                    print(f"    Downloaded OK")
                    return True
                html = await page.content()
                if "access denied" not in html.lower()[:1000]:
                    # Maybe it loaded as HTML — try getting PDF
                    try:
                        async with page.expect_download(timeout=10000) as dl_info:
                            await page.goto(pdf_url, wait_until="load", timeout=30000)
                        dl = await dl_info.value
                        await dl.save_as(str(pdf_path(doi)))
                        return True
                    except:
                        pass
                    break
            elif resp and resp.status == 403:
                html = await page.content()
                if "just a moment" in html.lower():
                    print(f"    CF challenge — waiting...")
                    await asyncio.sleep(10)  # Wait for challenge to resolve
                    continue
                print(f"    403 — access denied")
                break
        except Exception as e:
            print(f"    Error: {type(e).__name__}")
            break
    return False


async def dl_nature(page, doi):
    """Download from Nature."""
    try:
        resp = await page.goto(f"https://doi.org/{doi}", wait_until="networkidle", timeout=15000)
        final = page.url
        print(f"    Nature: {final[:90]}")
        if resp and resp.status == 200:
            pdf_url = final.rstrip("/") + ".pdf"
            resp2 = await page.goto(pdf_url, wait_until="networkidle", timeout=30000)
            if resp2 and resp2.status == 200 and "pdf" in page.url.lower():
                async with page.expect_download(timeout=10000) as dl_info:
                    pass
                dl = await dl_info.value
                await dl.save_as(str(pdf_path(doi)))
                print(f"    Downloaded OK")
                return True
    except Exception as e:
        print(f"    Nature error: {e}")
    return False


async def dl_wiley(page, doi):
    """Download from Wiley."""
    try:
        resp = await page.goto(f"https://doi.org/{doi}", wait_until="networkidle", timeout=15000)
        final = page.url
        print(f"    Wiley: {final[:90]}")
        if resp and resp.status == 200:
            html = await page.content()
            # Look for PDF link
            pdf_links = re.findall(r'href=["\']([^"\']*\.pdf[^"\']*)["\']', html)
            for link in pdf_links:
                if link.startswith("//"):
                    link = "https:" + link
                elif link.startswith("/"):
                    from urllib.parse import urlparse
                    parsed = urlparse(final)
                    link = f"{parsed.scheme}://{parsed.netloc}{link}"
                try:
                    resp2 = await page.goto(link, wait_until="networkidle", timeout=30000)
                    if resp2 and resp2.status == 200 and "pdf" in page.url.lower():
                        async with page.expect_download(timeout=10000) as dl_info:
                            pass
                        dl = await dl_info.value
                        await dl.save_as(str(pdf_path(doi)))
                        print(f"    Downloaded OK")
                        return True
                except:
                    pass
    except Exception as e:
        print(f"    Wiley error: {e}")
    return False


async def dl_acs(page, doi):
    """Download from ACS."""
    try:
        resp = await page.goto(f"https://doi.org/{doi}", wait_until="networkidle", timeout=15000)
        final = page.url
        print(f"    ACS: {final[:90]}")
        if "pubs.acs.org" in final:
            # ACS PDF URL pattern
            pdf_url = final.replace("/abs/", "/pdf/").replace("/full/", "/pdf/").rstrip("/") + ".pdf"
            resp2 = await page.goto(pdf_url, wait_until="networkidle", timeout=30000)
            if resp2 and resp2.status == 200 and "pdf" in page.url.lower():
                async with page.expect_download(timeout=10000) as dl_info:
                    pass
                dl = await dl_info.value
                await dl.save_as(str(pdf_path(doi)))
                print(f"    Downloaded OK")
                return True
    except Exception as e:
        print(f"    ACS error: {e}")
    return False


async def dl_publisher(page, doi):
    """Route to publisher-specific downloader."""
    pii = re.search(r'(S\d{2}\d{4}\d{4}\d{5,6})', doi)
    pii_val = pii.group(0) if pii else None

    if doi.startswith("10.1016"):
        return await dl_elsevier(page, doi, pii_val or doi.split("/")[-1])
    elif doi.startswith("10.3390"):
        return await dl_mdpi(page, doi)
    elif doi.startswith("10.1038"):
        return await dl_nature(page, doi)
    elif doi.startswith("10.1002"):
        return await dl_wiley(page, doi)
    elif doi.startswith("10.1021"):
        return await dl_acs(page, doi)
    else:
        # Generic: try doi.org and look for PDF
        try:
            print(f"    Generic: {doi}")
            resp = await page.goto(f"https://doi.org/{doi}", wait_until="networkidle", timeout=15000)
            html = await page.content()
            pdf_links = re.findall(r'href=["\']([^"\']*\.pdf[^"\']*)["\']', html)
            for link in pdf_links:
                if link.startswith("//"): link = "https:" + link
                try:
                    resp2 = await page.goto(link, wait_until="networkidle", timeout=30000)
                    if resp2 and resp2.status == 200 and "pdf" in page.url.lower():
                        async with page.expect_download(timeout=10000) as dl_info:
                            pass
                        dl = await dl_info.value
                        await dl.save_as(str(pdf_path(doi)))
                        return True
                except:
                    pass
        except:
            pass
        return False


async def main():
    from playwright.async_api import async_playwright

    # Sync progress
    progress = load_progress()
    review_dois = load_review_dois()
    for doi in sorted(review_dois):
        if pdf_path(doi).exists() and doi not in set(progress.get("pdf_done", [])):
            progress["pdf_done"].append(doi)
    save_progress(progress)

    pdf_done = set(progress.get("pdf_done", []))
    pdf_failed = set(progress.get("pdf_failed", []))

    todo = []
    for doi in sorted(review_dois):
        path = pdf_path(doi)
        if not path.exists() and doi not in pdf_done and doi not in pdf_failed:
            todo.append(doi)

    print(f"Review papers: {len(review_dois)}")
    print(f"Already have PDF: {len(pdf_done)}")
    print(f"Previously failed: {len(pdf_failed)}")
    print(f"Need to download: {len(todo)}")
    print(f"\nConnecting to your Chrome via CDP...")
    print(f"Make sure Chrome is running with: --remote-debugging-port=9222")

    if not todo:
        print("All done!")
        return

    async with async_playwright() as pw:
        browser = await pw.chromium.connect_over_cdp("http://localhost:9222")
        print(f"Connected! Contexts: {len(browser.contexts)}")
        context = browser.contexts[0] if browser.contexts else await browser.new_context()
        page = await context.new_page()
        # Check sign-in status
        await page.goto("https://www.sciencedirect.com", wait_until="domcontentloaded", timeout=15000)
        if "sign in" in (await page.content()).lower()[:3000]:
            print("WARNING: SD shows sign-in page. Log in via your browser first.")

        ok, fail = 0, 0
        for i, doi in enumerate(todo, 1):
            path = pdf_path(doi)
            if path.exists():
                progress["pdf_done"].append(doi)
                ok += 1
                continue
            print(f"\n  [{i}/{len(todo)}] {doi}")
            success = await dl_publisher(page, doi)
            if success:
                progress["pdf_done"].append(doi)
                ok += 1
                print(f"  ✓ {doi}")
            else:
                progress["pdf_failed"].append(doi)
                fail += 1
                print(f"  ✗ {doi}")
            save_progress(progress)

        await page.close()
        await browser.close()

    final_count = len(list(PDF_DIR.glob("*.pdf")))
    print(f"\n=== Done ===")
    print(f"OK: {ok}, Failed: {fail}")
    print(f"Total PDFs on disk: {final_count}")


if __name__ == "__main__":
    asyncio.run(main())
