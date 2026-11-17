"""PageSpeed Insights: real-user Core Web Vitals (Chrome UX Report) and Lighthouse lab scores for a sample of pages.
Works without a key at a low shared quota; set PSI_API_KEY for reliable runs."""
import os
from concurrent.futures import ThreadPoolExecutor
import requests

API = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"


def one(url, key):
    params = [("url", url), ("strategy", "mobile"), ("category", "performance"), ("category", "accessibility")]
    if key:
        params.append(("key", key))
    try:
        r = requests.get(API, params=params, timeout=120)
        if r.status_code != 200:
            return url, {"error": f"HTTP {r.status_code}: {r.text[:160]}"}
        j = r.json()
    except Exception as e:
        return url, {"error": type(e).__name__}
    out, src = {}, "url"
    m = (j.get("loadingExperience") or {}).get("metrics") or {}
    if not m:
        m, src = (j.get("originLoadingExperience") or {}).get("metrics") or {}, "origin"

    def pct(k):
        return (m.get(k) or {}).get("percentile")
    if m:
        cls = pct("CUMULATIVE_LAYOUT_SHIFT_SCORE")
        out.update(field=src, lcp_ms=pct("LARGEST_CONTENTFUL_PAINT_MS"), inp_ms=pct("INTERACTION_TO_NEXT_PAINT"), cls=cls / 100 if cls is not None else None)
    cats = (j.get("lighthouseResult") or {}).get("categories") or {}
    for name, key2 in (("performance", "lab_performance"), ("accessibility", "lab_accessibility")):
        s = (cats.get(name) or {}).get("score")
        if s is not None:
            out[key2] = round(s * 100)
    return url, out


def sample(site, n):
    """Homepage plus the most linked page of each top-level section, then the most linked pages overall."""
    pages = sorted((p for p in site["pages"].values() if p.get("html")), key=lambda p: -(p.get("inlinks") or 0))
    home = site["fetches"].get(site["start"], {}).get("final", site["start"])
    picked, seen = [home], set()
    for p in pages:
        seg = p["url"].split("/")[3] if p["url"].count("/") > 3 else ""
        if p["url"] != home and seg not in seen:
            seen.add(seg)
            picked.append(p["url"])
    picked += [p["url"] for p in pages if p["url"] not in picked]
    return picked[:n]


def collect(site, n=12, log=print):
    key = os.environ.get("PSI_API_KEY", "").strip()
    urls = sample(site, n if key else min(n, 4))
    with ThreadPoolExecutor(3) as ex:
        res = dict(ex.map(lambda u: one(u, key), urls))
    ok = {u: v for u, v in res.items() if "error" not in v}
    site["psi"] = ok
    if not ok:
        site["psi_error"] = "PageSpeed Insights returned no data (" + next(iter(res.values()), {}).get("error", "no pages") + "). " + ("" if key else "Add a PSI_API_KEY secret to the data repository for a reliable quota.")
    log(f"PageSpeed Insights: {len(ok)} of {len(urls)} pages" + ("" if key else " (no API key)"))
