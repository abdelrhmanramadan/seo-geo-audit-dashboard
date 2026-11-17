"""CLI: python -m audit.run --domain example.com --intake intake.json --out out/ [--sf export.csv] [--max-pages 500]"""
import argparse, json, os, re
from collections import Counter
from urllib.parse import urlparse
from pathlib import Path
from . import crawl, engine, plan, psi, sf_import


KNOWN_LANGS = set("ar en fr de es it pt tr ur fa he ru zh ja ko hi id ms nl sv pl el th vi bn uk ro cs hu da fi no".split())


def detect_languages(site):
    """Language versions from URL prefixes: a first path segment that is a language code and holds at least two pages."""
    seg = Counter()
    for p in site["pages"].values():
        if p.get("html"):
            m = re.match(r"^/([a-z]{2})(?:-[a-z]{2})?(?:/|$)", urlparse(p["url"]).path.lower())
            if m and m.group(1) in KNOWN_LANGS:
                seg[urlparse(p["url"]).path.split("/")[1].lower()] += 1
    langs = [{"code": s[:2], "prefix": "/" + s} for s, n in seg.items() if n >= 2]
    home = site["pages"].get(site["fetches"].get(site["start"], {}).get("final", site["start"]), {})
    root = (home.get("lang") or "")[:2]
    if root in {l["code"] for l in langs}:
        root = ""
    return [{"code": root, "prefix": "/"}] + langs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domain", required=True)
    ap.add_argument("--intake", help="path to the questionnaire answers (JSON); AUDIT_INTAKE env var is used when omitted")
    ap.add_argument("--sf", help="Screaming Frog 'Internal: All' CSV export")
    ap.add_argument("--max-pages", type=int, default=500)
    ap.add_argument("--out", required=True, help="output directory")
    ap.add_argument("--index", help="path to an index.json listing all audits (updated in place)")
    a = ap.parse_args()

    raw = Path(a.intake).read_text(encoding="utf-8") if a.intake else os.environ.get("AUDIT_INTAKE", "{}")
    intake = json.loads(raw or "{}")
    site = crawl.crawl(a.domain, max_pages=a.max_pages)
    if not intake.get("languages"):
        intake["languages"], intake["languages_auto"] = detect_languages(site), True
    if a.sf and Path(a.sf).exists():
        print("merged", sf_import.merge(site, a.sf), "pages from the Screaming Frog export")
    psi.collect(site)
    result = engine.audit(site, intake)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "result.json").write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
    stats = plan.build(result, out / "plan.xlsx")
    print("score", result["scores"]["overall"], "| checks run", result["meta"]["coverage"], "| plan", stats)
    if a.index:
        ip = Path(a.index)
        idx = json.loads(ip.read_text(encoding="utf-8")) if ip.exists() else []
        idx.insert(0, {"domain": site["host"], "date": site["crawled_at"], "path": str(out).replace("\\", "/"), "overall": result["scores"]["overall"],
                       "pages": len(site["pages"]), "pillars": {p["id"]: p["score"] for p in result["scores"]["pillars"]}})
        ip.write_text(json.dumps(idx, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
