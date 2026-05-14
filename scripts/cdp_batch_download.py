#!/usr/bin/env python3
"""
CDP-based batch PDF downloader (optimized).
Phase 1: Sci-Hub via browser for pre-2022 papers
Phase 2: Publisher direct via browser for everything else

Connects to Chrome CDP (port 9226) to bypass Cloudflare.
"""
import asyncio, json, re, sys, urllib.request, ssl
from pathlib import Path
from collections import Counter
from playwright.async_api import async_playwright

VAULT_ROOT = Path(r"E:\工作区\knowledge-base")
PDF_DIR = VAULT_ROOT / "raw" / "水凝胶" / "pdfs"
PROGRESS_FILE = VAULT_ROOT / "scripts" / "pipeline_progress.json"
PDF_DIR.mkdir(parents=True, exist_ok=True)
CDP_PORT = 9226

def doi_slug(doi): return doi.replace("/", "_")

def save_progress(p):
    PROGRESS_FILE.write_text(json.dumps(p, ensure_ascii=False, indent=2), "utf-8")

def get_pending():
    p = json.loads(PROGRESS_FILE.read_text("utf-8"))
    done = set(p.get("pdf_done", []))
    rp = json.loads((VAULT_ROOT / "scripts" / "review_papers.json").read_text("utf-8"))
    all_dois = {pp["doi"] for pp in rp if pp.get("doi")}
    return sorted(d for d in all_dois if d not in done and not (PDF_DIR / f"{doi_slug(d)}.pdf").exists())

def likely_year(doi):
    """Guess publication year from DOI path. Returns year int or 0 if uncertain."""
    m = re.search(r'\.(20\d{2})', doi)
    return int(m.group(1)) if m else 0

async def download_scihub(page, doi) -> bool:
    """Sci-Hub via CDP browser. PDF storage URL is not CAPTCHA-blocked."""
    pdf_path = PDF_DIR / f"{doi_slug(doi)}.pdf"
    if pdf_path.exists():
        return True

    captured = []
    async def cap_pdf(r):
        try:
            b = await r.body()
            if b[:4] == b'%PDF' and len(b) > 5000:
                captured.append(b)
        except:
            pass
    page.on("response", cap_pdf)

    try:
        await page.goto(f"https://sci-hub.ru/{doi}", wait_until="domcontentloaded", timeout=15000)
        await asyncio.sleep(3)

        title = await page.title()
        if "Sci-Hub." not in title or "not in database" in title:
            print(f"  [DBG] title='{title[:60]}'", file=sys.stderr)
            return False

        html = await page.content()
        m = re.search(r'citation_pdf_url[\"\']?\s+content=[\"\']([^\"\'\s>]+)', html)
        if not m:
            print(f"  [DBG] regex failed on {len(html)}b html, first char='{html[:20]}'", file=sys.stderr)
            return False

        pdf_meta = m.group(1)
        pdf_url = "https://sci-hub.ru" + pdf_meta if pdf_meta.startswith("/") else pdf_meta
        await page.goto(pdf_url, wait_until="domcontentloaded", timeout=25000)

        for _ in range(10):
            if captured:
                pdf_path.write_bytes(captured[0])
                return True
            await asyncio.sleep(0.5)
        return False
    except:
        if captured:
            pdf_path.write_bytes(captured[0])
            return True
        return False
    finally:
        page.remove_listener("response", cap_pdf)

async def download_publisher(page, doi) -> bool:
    """Try publisher direct via CDP."""
    pdf_path = PDF_DIR / f"{doi_slug(doi)}.pdf"
    if pdf_path.exists():
        return True

    captured = []
    async def cap_pdf(r):
        try:
            b = await r.body()
            if b[:4] == b'%PDF' and len(b) > 5000:
                captured.append(b)
        except:
            pass
    page.on("response", cap_pdf)

    try:
        await page.goto(f"https://doi.org/{doi}", wait_until="domcontentloaded", timeout=15000)
        await asyncio.sleep(1.5)
        url = page.url

        patterns = []
        if "sciencedirect" in url:
            pii = re.search(r'/pii/([A-Za-z]?\d{10,})', url)
            if pii:
                patterns = [f"https://www.sciencedirect.com/science/article/pii/{pii.group(1)}/pdfft"]
        elif "springer" in url or "link.springer" in url:
            patterns = [url.rstrip("/") + ".pdf",
                        url.replace("/article/", "/content/pdf/") + ".pdf"]
        elif "mdpi.com" in url:
            patterns = [url.rstrip("/") + "/pdf"]
        elif "wiley.com" in url:
            patterns = [url.rstrip("/") + "/pdf"]
        elif "acs.org" in url:
            patterns = [url.replace("/abs/", "/pdf/").rstrip("/") + ".pdf"]
        elif "rsc.org" in url:
            patterns = [url.rstrip("/") + ".pdf"]
        else:
            patterns = [url.rstrip("/") + ".pdf", url.rstrip("/") + "/pdf"]

        for p_url in patterns:
            try:
                await page.goto(p_url, wait_until="domcontentloaded", timeout=15000)
            except:
                pass
            for _ in range(8):
                if captured:
                    pdf_path.write_bytes(captured[0])
                    return True
                await asyncio.sleep(0.5)

        # Check if redirected to login page
        if "login" in page.url.lower() or "signin" in page.url.lower() or "sso" in page.url.lower() or "id.elsevier" in page.url.lower():
            return False  # Need login
        return False
    except:
        if captured:
            pdf_path.write_bytes(captured[0])
            return True
        return False
    finally:
        page.remove_listener("response", cap_pdf)

async def main():
    pending = get_pending()
    print(f"\nPending: {len(pending)}")
    if not pending:
        print("All done!")
        return

    # Split by year
    sh_dois = [d for d in pending if likely_year(d) < 2023 or likely_year(d) == 0]
    pub_dois = [d for d in pending if likely_year(d) >= 2023]
    print(f"Sci-Hub candidates (<2023): {len(sh_dois)}")
    print(f"Publisher direct candidates (2023+): {len(pub_dois)}")

    async with async_playwright() as pw:
        browser = await pw.chromium.connect_over_cdp(f"http://127.0.0.1:{CDP_PORT}")
        progress = json.loads(PROGRESS_FILE.read_text("utf-8"))
        pdf_done = set(progress.get("pdf_done", []))

        # Phase 1: Sci-Hub (each paper gets a fresh context to avoid rate limiting)
        print(f"\n{'='*50}")
        print("Phase 1: Sci-Hub (fresh context per paper)")
        print(f"{'='*50}")
        sh_ok = 0
        for i, doi in enumerate(sh_dois, 1):
            if doi in pdf_done or (PDF_DIR / f"{doi_slug(doi)}.pdf").exists():
                continue
            # Fresh context to avoid Sci-Hub rate limiting
            ctx = await browser.new_context()
            page = await ctx.new_page()
            sys.stdout.write(f"  [{i}/{len(sh_dois)}] {doi} ")
            sys.stdout.flush()
            try:
                if await download_scihub(page, doi):
                    progress["pdf_done"].append(doi)
                    pdf_done.add(doi)
                    sh_ok += 1
                    print("OK")
                else:
                    pub_dois.append(doi)
                    print("N/A")
            except Exception as e:
                pub_dois.append(doi)
                print(f"ERR: {e}")
            finally:
                await page.close()
                await ctx.close()
            if i % 15 == 0:
                save_progress(progress)
        save_progress(progress)
        print(f"\nSci-Hub: +{sh_ok}")

        # Phase 2: Publisher direct
        # Remove already-done from pub_dois
        pub_dois = [d for d in pub_dois if d not in pdf_done and not (PDF_DIR / f"{doi_slug(d)}.pdf").exists()]

        if pub_dois:
            print(f"\n{'='*50}")
            print(f"Phase 2: Publisher direct ({len(pub_dois)})")
            print(f"{'='*50}")
            pub_c = Counter()
            for d in pub_dois:
                pub_c[d.split('/')[0]] += 1
            for k, v in sorted(pub_c.items(), key=lambda x: -x[1]):
                print(f"  {k}: {v}")
            print()

            pub_ok = 0
            need_login = 0
            for i, doi in enumerate(pub_dois, 1):
                if doi in pdf_done or (PDF_DIR / f"{doi_slug(doi)}.pdf").exists():
                    continue
                page = await ctx.new_page()
                sys.stdout.write(f"  [{i}/{len(pub_dois)}] {doi} ")
                sys.stdout.flush()
                try:
                    if await download_publisher(page, doi):
                        progress["pdf_done"].append(doi)
                        pdf_done.add(doi)
                        pub_ok += 1
                        print("OK")
                    else:
                        progress["pdf_failed"].append(doi)
                        need_login += 1
                        print("NEED-LOGIN")
                except Exception as e:
                    progress["pdf_failed"].append(doi)
                    print(f"ERR: {e}")
                finally:
                    await page.close()
                if i % 10 == 0:
                    save_progress(progress)

            # Also try injecting SD cookies and retrying Elsevier
            save_progress(progress)
            print(f"\nPublisher direct: +{pub_ok}, blocked by login: {need_login}")

        # Final
        final_pdf = len(list(PDF_DIR.glob("*.pdf")))
        still = [d for d in pending if d not in pdf_done and not (PDF_DIR / f"{doi_slug(d)}.pdf").exists()]

        print(f"\n{'='*50}")
        print(f"FINAL: {final_pdf} PDFs, still need {len(still)}")
        if still:
            sc = Counter()
            for d in still:
                sc[d.split('/')[0]] += 1
            for k, v in sorted(sc.items(), key=lambda x: -x[1]):
                print(f"  {k}: {v}")

if __name__ == "__main__":
    import os
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    asyncio.run(main())
