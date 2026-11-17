"""Runs the catalog against a crawled site and computes scores."""
from pathlib import Path
import yaml
from .checks import REG, Ctx

ROOT = Path(__file__).resolve().parent.parent
SCORE = {"pass": 1.0, "warn": 0.5, "fail": 0.0}
VERTICAL = {"ecommerce": "vertical.ecommerce", "publisher": "vertical.publisher", "saas": "vertical.saas", "services": "vertical.services"}
WHY = {"ai": "needs the AI content analysis layer (not connected yet)", "manual": "manual review", "render": "needs JavaScript rendering (not built yet)",
       "api:psi": "needs PageSpeed Insights API (not connected yet)", "api:crux": "needs Chrome UX Report API (not connected yet)",
       "api:gsc": "needs Search Console access", "api:serp": "needs a SERP data source", "api:safebrowsing": "needs Safe Browsing API (not connected yet)",
       "api:openpagerank": "needs a backlink data source", "api:commoncrawl": "needs a backlink data source", "crawl": "crawl-based check not implemented yet"}


def load_catalog():
    return yaml.safe_load((ROOT / "catalog" / "checks.yaml").read_text(encoding="utf-8"))


def wavg(pairs):
    pairs = [(w, s) for w, s in pairs if s is not None]
    tw = sum(w for w, _ in pairs)
    return round(sum(w * s for w, s in pairs) / tw, 1) if tw else None


def evaluate(site, intake, pages=None, with_items=True):
    cat, ctx = load_catalog(), Ctx(site, intake, pages)
    src, pw = cat["sources"], cat["scoring"]["pillar_weights"]
    checks, pillars = [], []
    for p in cat["pillars"]:
        p_active = not (p["id"] == "local" and not intake.get("has_locations"))
        sections, p_crit = [], False
        for s in p["sections"]:
            s_active = p_active and not (p["id"] == "vertical" and VERTICAL.get(intake.get("site_type")) != s["id"])
            subs = []
            for ss in s["subsections"]:
                scored, crit, ran = [], False, 0
                for c in ss["checks"]:
                    if not s_active:
                        res = {"status": "na", "summary": "module not active for this project", "items": [], "count": 0}
                    elif c["id"] in REG:
                        try:
                            res = REG[c["id"]](ctx)
                        except Exception as e:  # a broken check must not stop the audit
                            res = {"status": "error", "summary": f"check failed to run: {type(e).__name__}: {e}", "items": [], "count": 0}
                    else:
                        res = {"status": "not_run", "summary": WHY.get(c["method"], "not implemented yet"), "items": [], "count": 0}
                    if res["status"] in SCORE:
                        ran += 1
                        if c["weight"]:
                            scored.append((c["weight"], SCORE[res["status"]] * 100))
                        crit |= res["status"] == "fail" and c["severity"] == "critical"
                    elif res["status"] == "info":
                        ran += 1
                    if not with_items:
                        res = {**res, "items": []}
                    so = src[c["source"]]
                    checks.append({**{k: c[k] for k in ("id", "name", "severity", "weight", "basis", "method", "scope", "test", "fix")},
                                   "pillar": p["id"], "section": s["id"], "subsection": ss["id"], "section_name": s["name"], "subsection_name": ss["name"],
                                   "source_title": so["title"], "source_url": so["url"], **res})
                sc = wavg(scored)
                if sc is not None and crit:
                    sc = min(sc, 60.0)
                p_crit |= crit
                subs.append({"id": ss["id"], "name": ss["name"], "weight": ss["weight"], "score": sc, "ran": ran, "total": len(ss["checks"])})
            sections.append({"id": s["id"], "name": s["name"], "weight": s["weight"], "active": s_active,
                             "score": wavg([(x["weight"], x["score"]) for x in subs]), "subsections": subs})
        ps = wavg([(x["weight"], x["score"]) for x in sections])
        if ps is not None and p_crit:
            ps = min(ps, 75.0)
        pillars.append({"id": p["id"], "name": p["name"].split(" (")[0], "weight": pw[p["id"]], "score": ps, "sections": sections})
    return {"overall": wavg([(x["weight"], x["score"]) for x in pillars]), "pillars": pillars}, checks, ctx


def audit(site, intake):
    scores, checks, ctx = evaluate(site, intake)
    by_lang = {}
    for l in ctx.langs:
        subset = [p for p in site["pages"].values() if ctx.lang_of(p["url"])[0] == l["code"]]
        if subset and len(ctx.langs) > 1:
            sc, _, _ = evaluate(site, intake, subset, with_items=False)
            by_lang[l["code"] or "default (root)"] = {"pages": len(subset), "overall": sc["overall"], "pillars": {p["id"]: p["score"] for p in sc["pillars"]}}
    fails = {}
    for c in checks:
        if c["status"] in ("warn", "fail"):
            for i in c["items"]:
                fails.setdefault(i["url"], []).append(c["id"])
    pages = [{"url": p["url"], "status": p["status"], "title": p.get("title", ""), "words": p.get("words"), "depth": p.get("depth"), "inlinks": p.get("inlinks"),
              "lang": ctx.lang_of(p["url"])[0], "type": ctx.ptype(p) if p.get("html") else "", "source": p.get("source", "crawler"), "issues": fails.get(p["url"], [])}
             for p in site["pages"].values()]
    applicable = [c for c in checks if c["status"] != "na"]
    ran = [c for c in applicable if c["status"] in ("pass", "warn", "fail", "info")]
    cat = load_catalog()
    return {"meta": {"domain": site["host"], "start": site["start"], "crawled_at": site["crawled_at"], "pages_crawled": len(site["pages"]), "truncated": site["truncated"],
                     "catalog_version": cat["version"], "screaming_frog_pages": sum(1 for p in site["pages"].values() if p.get("source") == "screaming_frog"),
                     "coverage": {"ran": len(ran), "applicable": len(applicable), "total": len(checks)}},
            "scores": scores, "by_language": by_lang, "checks": checks, "pages": pages, "intake": intake}
