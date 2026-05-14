#!/usr/bin/env python3
"""
Batch PDF download - tries multiple methods for maximum coverage from China.
"""
import json, os, re, sys, time, urllib.request, ssl
from pathlib import Path
from urllib.error import HTTPError, URLError

VAULT_ROOT = Path(r"E:\工作区\knowledge-base")
PDF_DIR = VAULT_ROOT / "raw" / "水凝胶" / "pdfs"
PROGRESS_FILE = VAULT_ROOT / "scripts" / "pipeline_progress.json"
S2_API = "https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}?fields=title,externalIds,isOpenAccess,openAccessPdf"

PDF_DIR.mkdir(parents=True, exist_ok=True)
ctx = ssl._create_unverified_context()
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def doi_slug(doi):
    return doi.replace("/", "_")

def dl(url, timeout=60):
    req = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
    data = resp.read()
    if data[:4] == b'%PDF' and len(data) > 10000:
        return data
    return None

def try_epmc_direct(doi):
    slug = doi_slug(doi)
    path = PDF_DIR / f"{slug}.pdf"
    if path.exists(): return True
    time.sleep(0.3)
    try:
        url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:%22{doi}%22&format=json&resultType=core"
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=15, context=ctx)
        data = json.loads(resp.read().decode("utf-8"))
        results = data.get("resultList", {}).get("result", [])
        for r in results:
            pmcid = r.get("pmcid", "")
            if pmcid:
                for ft in r.get("fullTextUrlList", {}).get("fullTextUrl", []):
                    if ft.get("availabilityCode") == "OA" and ft.get("documentStyle") == "pdf":
                        pdf_url = ft["url"]
                        try:
                            pdf_data = dl(pdf_url, 60)
                            if pdf_data:
                                path.write_bytes(pdf_data)
                                print(f"  OK: {doi} (EPMC, {len(pdf_data)} bytes)")
                                return True
                        except:
                            pass
                try:
                    pmc_url = f"https://europepmc.org/articles/PMC{pmcid}?pdf=render"
                    pdf_data = dl(pmc_url, 60)
                    if pdf_data:
                        path.write_bytes(pdf_data)
                        print(f"  OK: {doi} (PMC render, {len(pdf_data)} bytes)")
                        return True
                except:
                    pass
    except:
        pass
    return False

def try_mdpi(doi):
    slug = doi_slug(doi)
    path = PDF_DIR / f"{slug}.pdf"
    if path.exists(): return True

    m = re.match(r'^10\.3390/(\w+)(\d+)', doi)
    if not m:
        return False

    journal = m.group(1)
    article_id = m.group(2)

    patterns = [
        f"https://www.mdpi.com/{journal}/{article_id}/pdf",
        f"https://www.mdpi.com/{journal}/{article_id}/pdf-vor",
        f"https://mdpi-res.com/{journal}/{article_id}/pdf",
    ]
    for url in patterns:
        try:
            pdf_data = dl(url, 30)
            if pdf_data:
                path.write_bytes(pdf_data)
                print(f"  OK: {doi} (MDPI, {len(pdf_data)} bytes)")
                return True
        except:
            pass
    return False

def try_rsc(doi):
    slug = doi_slug(doi)
    path = PDF_DIR / f"{slug}.pdf"
    if path.exists(): return True
    if "10.1039" not in doi:
        return False
    try:
        url = f"https://doi.org/{doi}"
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=15, context=ctx)
        final_url = resp.geturl()
        if '/pdf' in final_url.lower():
            pdf_data = dl(final_url, 30)
            if pdf_data:
                path.write_bytes(pdf_data)
                print(f"  OK: {doi} (RSC redirect, {len(pdf_data)} bytes)")
                return True
        pdf_url = final_url.rstrip('/') + '.pdf'
        try:
            pdf_data = dl(pdf_url, 30)
            if pdf_data:
                path.write_bytes(pdf_data)
                print(f"  OK: {doi} (RSC .pdf, {len(pdf_data)} bytes)")
                return True
        except:
            pass
    except:
        pass
    return False

def try_nature(doi):
    slug = doi_slug(doi)
    path = PDF_DIR / f"{slug}.pdf"
    if path.exists(): return True
    if "10.1038" not in doi:
        return False
    try:
        url = f"https://doi.org/{doi}"
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=15, context=ctx)
        final_url = resp.geturl()
        final_url = final_url.rstrip('/')
        for suffix in ['.pdf', '/pdf']:
            try:
                pdf_data = dl(final_url + suffix, 30)
                if pdf_data:
                    path.write_bytes(pdf_data)
                    print(f"  OK: {doi} (Nature, {len(pdf_data)} bytes)")
                    return True
            except:
                pass
    except:
        pass
    return False

def try_acs(doi):
    slug = doi_slug(doi)
    path = PDF_DIR / f"{slug}.pdf"
    if path.exists(): return True
    if "10.1021" not in doi:
        return False
    try:
        url = f"https://doi.org/{doi}"
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=15, context=ctx)
        final_url = resp.geturl()
        pdf_url = final_url.replace("/abs/", "/pdf/").replace("/full/", "/pdf/").rstrip('/')
        if not pdf_url.endswith('.pdf'):
            pdf_url = pdf_url + '.pdf'
        try:
            pdf_data = dl(pdf_url, 60)
            if pdf_data:
                path.write_bytes(pdf_data)
                print(f"  OK: {doi} (ACS, {len(pdf_data)} bytes)")
                return True
        except:
            pass
        if 'pubs.acs.org' in final_url:
            doi_path = doi.replace('/', '%2F')
            pdf_url = f"https://pubs.acs.org/doi/pdf/{doi_path}"
            try:
                pdf_data = dl(pdf_url, 60)
                if pdf_data:
                    path.write_bytes(pdf_data)
                    print(f"  OK: {doi} (ACS pdf/, {len(pdf_data)} bytes)")
                    return True
            except:
                pass
    except:
        pass
    return False

def try_elsevier(doi):
    slug = doi_slug(doi)
    path = PDF_DIR / f"{slug}.pdf"
    if path.exists(): return True
    if not any(x in doi for x in ["10.1016", "10.1017"]):
        return False
    try:
        url = f"https://doi.org/{doi}"
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=15, context=ctx)
        final_url = resp.geturl()
        if 'sciencedirect' in final_url:
            pdf_url = final_url.rstrip('/') + '/pdfft'
            try:
                pdf_data = dl(pdf_url, 60)
                if pdf_data:
                    path.write_bytes(pdf_data)
                    print(f"  OK: {doi} (SD, {len(pdf_data)} bytes)")
                    return True
            except:
                pass
    except:
        pass
    return False

def try_s2_oa(doi):
    slug = doi_slug(doi)
    path = PDF_DIR / f"{slug}.pdf"
    if path.exists(): return True
    time.sleep(1)
    try:
        url = S2_API.format(doi=doi)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=15, context=ctx)
        data = json.loads(resp.read().decode("utf-8"))
        oa = data.get("openAccessPdf") or {}
        if oa and "url" in oa:
            pdf_data = dl(oa["url"], 30)
            if pdf_data:
                path.write_bytes(pdf_data)
                print(f"  OK: {doi} (S2 OA, {len(pdf_data)} bytes)")
                return True
    except:
        pass
    return False

def try_scidown(doi):
    slug = doi_slug(doi)
    path = PDF_DIR / f"{slug}.pdf"
    if path.exists(): return True

    domains = [
        "https://sci-hub.se",
        "https://sci-hub.ru",
        "https://sci-hub.st",
    ]

    for domain in domains:
        url = f"{domain}/{doi}"
        try:
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req, timeout=30, context=ctx)
            content = resp.read()

            if len(content) > 50000 and content[:4] == b'%PDF':
                path.write_bytes(content)
                print(f"  OK: {doi} (Sci-Hub, {len(content)} bytes)")
                return True

            html = content.decode("utf-8", errors="replace")
            pdf_urls = re.findall(r'(?:src|href)=["\']([^"\']+\.pdf[^"\']*)["\']', html)
            for pdf_url in pdf_urls:
                if pdf_url.startswith("//"):
                    pdf_url = "https:" + pdf_url
                elif pdf_url.startswith("/"):
                    pdf_url = domain + pdf_url
                try:
                    pdf_data = dl(pdf_url, 30)
                    if pdf_data:
                        path.write_bytes(pdf_data)
                        print(f"  OK: {doi} (Sci-Hub redirect, {len(pdf_data)} bytes)")
                        return True
                except:
                    continue
        except:
            continue
    return False

def try_all(doi):
    slug = doi_slug(doi)
    path = PDF_DIR / f"{slug}.pdf"
    if path.exists():
        return True

    methods = [
        ("EPMC", try_epmc_direct),
        ("MDPI", try_mdpi),
        ("RSC", try_rsc),
        ("Nature", try_nature),
        ("ACS", try_acs),
        ("Elsevier", try_elsevier),
        ("S2 OA", try_s2_oa),
        ("Sci-Hub", try_scidown),
    ]

    for name, method in methods:
        try:
            if method(doi):
                return True
        except Exception:
            pass
    return False

def save_progress(p):
    PROGRESS_FILE.write_text(json.dumps(p, ensure_ascii=False, indent=2), "utf-8")

def main():
    progress = json.loads(PROGRESS_FILE.read_text("utf-8"))
    pdf_done = set(progress.get("pdf_done", []))
    pdf_failed = set(progress.get("pdf_failed", []))

    rp = json.loads((VAULT_ROOT / "scripts" / "review_papers.json").read_text("utf-8"))
    review_dois = {p["doi"] for p in rp if p.get("doi")}

    # Sync existing PDFs into progress
    for doi in sorted(review_dois):
        slug = doi_slug(doi)
        path = PDF_DIR / f"{slug}.pdf"
        if path.exists() and doi not in pdf_done:
            pdf_done.add(doi)
            progress["pdf_done"].append(doi)
    save_progress(progress)

    todo = []
    for doi in sorted(review_dois):
        slug = doi_slug(doi)
        path = PDF_DIR / f"{slug}.pdf"
        if not path.exists() and doi not in pdf_done and doi not in pdf_failed:
            todo.append(doi)

    print(f"Total review papers: {len(review_dois)}")
    print(f"Already have PDF:    {len(pdf_done)}")
    print(f"Previously failed:   {len(pdf_failed)}")
    print(f"Need to download:    {len(todo)}")

    if not todo:
        print("All done!")
        return

    print(f"\nDownloading {len(todo)} PDFs...\n")

    ok = 0
    fail = 0
    for i, doi in enumerate(todo, 1):
        path = PDF_DIR / f"{doi_slug(doi)}.pdf"
        if path.exists():
            print(f"  [{i}/{len(todo)}] {doi} (exists)")
            progress["pdf_done"].append(doi)
            ok += 1
            continue
        print(f"  [{i}/{len(todo)}] {doi}")
        if try_all(doi):
            progress["pdf_done"].append(doi)
            ok += 1
        else:
            progress["pdf_failed"].append(doi)
            fail += 1
            print(f"  FAIL: {doi}")

        if (i % 5) == 0:
            save_progress(progress)

    save_progress(progress)

    final_pdf = len(list(PDF_DIR.glob("*.pdf")))
    print(f"\n=== Result ===")
    print(f"New OK: {ok}, New Failed: {fail}")
    print(f"Total PDFs on disk: {final_pdf}")

if __name__ == "__main__":
    main()
