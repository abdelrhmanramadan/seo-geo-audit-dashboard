"""CLI: python -m audit.run --domain example.com --intake intake.json --out out/ [--sf export.csv] [--max-pages 500]"""
import argparse, json, os, time
from pathlib import Path
from . import crawl, engine, plan, sf_import


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
    if not intake.get("languages"):
        intake["languages"] = [{"code": "", "prefix": "/"}]
    site = crawl.crawl(a.domain, max_pages=a.max_pages)
    if a.sf and Path(a.sf).exists():
        print("merged", sf_import.merge(site, a.sf), "pages from the Screaming Frog export")
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
