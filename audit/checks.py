"""Check implementations. Each function is registered under its catalog id and returns a result dict.
Checks in the catalog with no function here are reported as "not_run" with the reason."""
import re
from collections import defaultdict
from urllib.parse import urlparse, unquote

REG = {}
RTL = {"ar", "he", "fa", "ur"}
GENERIC_ANCHORS = {"click here", "here", "read more", "learn more", "more", "link", "this", "اضغط هنا", "هنا", "اقرأ المزيد", "المزيد", "اعرف المزيد"}
Q_EN = re.compile(r"^(what|how|why|when|where|who|which|can|does|do|is|are|should|will)\b.*\?$", re.I)
Q_AR = re.compile(r"^(ما|ماذا|كيف|لماذا|متى|أين|اين|من|هل|كم)\s.*[؟?]$")
AI_SEARCH_BOTS = {"GEO-002": "OAI-SearchBot", "GEO-003": "ChatGPT-User", "GEO-004": "PerplexityBot", "GEO-006": "bingbot"}
TRAINING_BOTS = ["GPTBot", "Google-Extended", "CCBot", "ClaudeBot", "Applebot-Extended"]


def check(cid):
    def deco(fn):
        REG[cid] = fn
        return fn
    return deco


def R(status, summary, items=None):
    items = items or []
    return {"status": status, "summary": summary, "items": items[:300], "count": len(items)}


def rate(total, items, what, ok="all pass"):
    """Page-scope rule: no failures = pass, up to 10% of pages = warn, more = fail."""
    if total == 0:
        return R("na", "no applicable pages")
    if not items:
        return R("pass", f"{total} {what} checked, {ok}")
    share = len({i['url'] for i in items}) / total
    return R("warn" if share <= 0.10 else "fail", f"{len({i['url'] for i in items})} of {total} {what} affected", items)


def it(url, detail=""):
    return {"url": url, "detail": str(detail)[:300]}


class Ctx:
    def __init__(self, site, intake, pages=None):
        self.site, self.intake = site, intake
        self.all = site["pages"]
        self.pages = pages if pages is not None else list(self.all.values())
        self.html = [p for p in self.pages if p.get("html")]
        self.indexable = [p for p in self.html if self.is_indexable(p)]
        # indexable pages plus pages known only from a Screaming Frog export (fewer fields available)
        self.basic = self.indexable + [p for p in self.pages if p.get("partial") and p.get("indexable_sf")]
        self.langs = sorted(intake.get("languages") or [], key=lambda l: -len(l["prefix"]))
        self.rp = site["_rp"]
        self.home = self.all.get(site["fetches"].get(site["start"], {}).get("final", site["start"]))

    @staticmethod
    def noindex(p):
        return any("noindex" in r for r in p.get("meta_robots", [])) or "noindex" in p.get("x_robots", "")

    def is_indexable(self, p):
        c = p.get("canonicals") or []
        return p.get("html") and not self.noindex(p) and (not c or c[0].rstrip("/") == p["url"].rstrip("/"))

    def lang_of(self, url):
        path = urlparse(url).path
        for l in self.langs:
            pre = l["prefix"].rstrip("/")
            if pre == "" or path == pre or path.startswith(pre + "/"):
                return l["code"], path[len(pre):] or "/"
        return None, path

    def ptype(self, p):
        path = urlparse(p["url"]).path.lower()
        _, slug = self.lang_of(p["url"])
        if slug in ("/", ""):
            return "home"
        if re.search(r"/(blog|news|articles|insights)/[^/]+", path):
            return "blog"
        if re.search(r"/(products?|features?)/", path):
            return "products"
        if re.search(r"/(solutions?|services?|industries)/", path):
            return "solutions"
        return "other"

    def types(self, p):
        return set(p.get("ld_types", []))


# ---------------- Technical: crawlability ----------------
@check("TECH-001")
def _(c):
    s = c.site["robots"]["status"]
    if s == 200:
        return R("pass", "robots.txt returns 200")
    if s == 404:
        return R("warn", "robots.txt returns 404 (treated as allow all)")
    return R("fail", f"robots.txt returns {s or 'no response'}")


@check("TECH-002")
def _(c):
    targets = set(u for u in c.site["sitemap"]["urls"]) | {l["href"] for l in (c.home or {}).get("links_int", []) if l["nav"]}
    bad = [it(u, "disallowed for Googlebot") for u in sorted(targets) if not c.rp.can_fetch("Googlebot", u)]
    return R("fail" if bad else "pass", f"{len(bad)} sitemap/navigation URLs blocked for Googlebot" if bad else "no important URL is blocked", bad)


@check("TECH-004")
def _(c):
    n = len(c.site["robots"]["sitemaps"])
    return R("pass" if n else "fail", f"{n} Sitemap directive(s) in robots.txt")


@check("TECH-005")
def _(c):
    sm = c.site["sitemap"]
    if not sm["urls"]:
        return R("fail", "no valid XML sitemap found: " + ("; ".join(sm["errors"]) or "none at /sitemap.xml"))
    if sm["errors"]:
        return R("warn", f"{len(sm['urls'])} URLs read, with errors: " + "; ".join(sm["errors"][:5]))
    return R("pass", f"{len(sm['urls'])} URLs in {len(sm['files'])} sitemap file(s)")


@check("TECH-006")
def _(c):
    bad, n = [], 0
    for u in c.site["sitemap"]["urls"]:
        f = c.site["fetches"].get(u)
        if not f:
            continue
        n += 1
        p = c.all.get(f["final"])
        if f["hops"]:
            bad.append(it(u, f"redirects to {f['final']}"))
        elif f["status"] != 200:
            bad.append(it(u, f"status {f['status']}"))
        elif p and c.noindex(p):
            bad.append(it(u, "noindex"))
        elif p and p.get("canonicals") and p["canonicals"][0].rstrip("/") != u.rstrip("/"):
            bad.append(it(u, f"canonical points to {p['canonicals'][0]}"))
    if not n:
        return R("na", "no sitemap URLs crawled")
    share = len(bad) / n
    return R("pass" if share <= 0.02 else "warn" if share <= 0.10 else "fail", f"{len(bad)} of {n} sitemap URLs are not indexable canonical 200 pages", bad)


@check("TECH-009")
def _(c):
    bad = []
    for p in c.html:
        for l in p["links_int"]:
            f = c.site["fetches"].get(l["href"])
            if f and (f["status"] >= 400 or f["status"] == 0):
                bad.append(it(p["url"], f"links to {l['href']} ({f['status'] or f['error']}), anchor: {l['anchor']}"))
    return rate(len(c.html), bad, "pages", "no broken internal links")


@check("TECH-010")
def _(c):
    bad = [it(u, f"{f['hops']} hops to {f['final']}" if f["hops"] else f.get("error")) for u, f in c.site["fetches"].items() if f["hops"] >= 2 or f.get("error") in ("redirect loop", "too many redirects")]
    broken = any(f["hops"] > 10 or f.get("error") in ("redirect loop", "too many redirects") for f in c.site["fetches"].values())
    return R("pass" if not bad else "fail" if broken else "warn", f"{len(bad)} redirect chain(s)" + (", including loops or chains over 10 hops" if broken else "") if bad else "no redirect chains", bad)


@check("TECH-011")
def _(c):
    bad = []
    for p in c.html:
        for l in p["links_int"]:
            f = c.site["fetches"].get(l["href"])
            if f and f["hops"] and f["status"] == 200:
                bad.append(it(p["url"], f"links to {l['href']} which redirects to {f['final']}"))
    return rate(len(c.html), bad, "pages", "internal links point to final URLs")


@check("TECH-012")
def _(c):
    bad = [it(p["url"], f"status {p['status']}") for p in c.pages if p["status"] >= 500]
    return R("fail" if bad else "pass", f"{len(bad)} URL(s) return 5xx" if bad else "no 5xx responses", bad)


@check("TECH-013")
def _(c):
    pr = c.site["probes"]["soft404"]
    return R("pass" if pr["status"] in (404, 410) else "fail", f"non-existent URL returned {pr['status']}" + ("" if pr["final"] == pr["url"] else f" after redirecting to {pr['final']}"))


@check("TECH-014")
def _(c):
    deep = [it(p["url"], f"depth {p['depth']}") for p in c.indexable if p.get("depth") is not None and p["depth"] > 3]
    worst = max([p["depth"] for p in c.indexable if p.get("depth") is not None] or [0])
    return R("pass" if not deep else "warn" if worst <= 5 else "fail", f"{len(deep)} page(s) deeper than 3 clicks (max {worst})" if deep else "all pages within 3 clicks", deep)


@check("TECH-015")
def _(c):
    bad = [it(p["url"], "in sitemap, no internal links found") for p in c.indexable if p.get("in_sitemap") and p.get("inlinks", 0) == 0 and p is not c.home]
    return rate(len([p for p in c.indexable if p.get("in_sitemap")]), bad, "sitemap pages", "no orphan pages")


@check("TECH-016")
def _(c):
    bad = [it(u, "in sitemap but disallowed in robots.txt") for u in c.site["sitemap"]["urls"] if not c.rp.can_fetch("Googlebot", u)]
    return R("fail" if bad else "pass", f"{len(bad)} sitemap URL(s) blocked by robots.txt" if bad else "no conflict", bad)


@check("TECH-017")
def _(c):
    b = c.site["robots"]["bytes"]
    return R("pass" if b <= 512000 else "fail", f"robots.txt is {b} bytes")


# ---------------- Technical: indexability ----------------
@check("TECH-020")
def _(c):
    bad = [it(p["url"], "noindex on a sitemap page") for p in c.html if p.get("in_sitemap") and c.noindex(p)]
    return R("fail" if bad else "pass", f"{len(bad)} sitemap page(s) carry noindex" if bad else "no unintended noindex", bad)


@check("TECH-021")
def _(c):
    bad = []
    for p in c.html:
        n = len(p["canonicals"])
        if n != 1:
            bad.append(it(p["url"], f"{n} canonical tags"))
        elif not p["canonical_raw_abs"]:
            bad.append(it(p["url"], "canonical is a relative URL"))
    return rate(len(c.html), bad, "pages", "one absolute canonical each")


@check("TECH-022")
def _(c):
    bad = []
    for p in c.html:
        if p["canonicals"]:
            t = p["canonicals"][0]
            f = c.site["fetches"].get(t) or c.site["fetches"].get(t.rstrip("/")) or c.site["fetches"].get(t + "/")
            if f and (f["status"] != 200 or f["hops"]):
                bad.append(it(p["url"], f"canonical {t} returns {f['status']}" + (" via redirect" if f["hops"] else "")))
    return rate(len(c.html), bad, "pages", "canonical targets are live")


@check("TECH-024")
def _(c):
    v = c.site["probes"]["variants"]
    finals = {x["final"] for x in v.values() if x["status"] == 200}
    bad = [it(u, f"status {x['status']}, ends at {x['final']}") for u, x in v.items()]
    if len(finals) == 1:
        return R("pass", f"all host/protocol variants resolve to {finals.pop()}")
    return R("fail", f"variants resolve to {len(finals)} different URLs", bad)


@check("TECH-029B")
def _(c):
    bad = [it(p["url"], "; ".join(p["meta_robots"])) for p in c.html if len(p["meta_robots"]) > 1 and any("noindex" in r for r in p["meta_robots"]) and any("noindex" not in r for r in p["meta_robots"])]
    return rate(len(c.html), bad, "pages", "no conflicting robots directives")


# ---------------- Technical: performance, mobile, security, server ----------------
@check("TECH-044")
def _(c):
    slow = [it(p["url"], f"{p['ttfb']} ms") for p in c.html if (p.get("ttfb") or 0) > 800]
    vslow = [i for i in slow if int(i["detail"].split()[0]) > 1800]
    if not c.html:
        return R("na", "no pages")
    return R("pass" if not slow else "fail" if len(vslow) > len(c.html) * 0.1 else "warn", f"{len(slow)} page(s) over 800 ms, {len(vslow)} over 1800 ms (single measurement from the crawler)", slow)


@check("TECH-050")
def _(c):
    return rate(len(c.html), [it(p["url"], "no viewport meta") for p in c.html if not p["viewport"]], "pages", "viewport present")


@check("TECH-060")
def _(c):
    bad = [it(p["url"], "served over http") for p in c.pages if p["url"].startswith("http://") and p["status"] == 200]
    return R("fail" if bad else "pass", f"{len(bad)} page(s) not on HTTPS" if bad else "all pages on HTTPS", bad)


@check("TECH-061")
def _(c):
    return rate(len(c.html), [it(p["url"], f"{p['mixed']} http resource(s)") for p in c.html if p.get("mixed")], "pages", "no mixed content")


@check("TECH-062")
def _(c):
    h = (c.home or {}).get("hsts", "")
    m = re.search(r"max-age=(\d+)", h)
    ok = m and int(m.group(1)) >= 31536000
    return R("pass" if ok else "warn" if m else "fail", f"Strict-Transport-Security: {h or 'missing'}")


@check("TECH-090")
def _(c):
    bad = [it(p["url"], "no gzip/br") for p in c.html if not p.get("encoding")]
    return rate(len(c.html), bad, "pages", "compressed")


@check("TECH-092")
def _(c):
    big = [it(p["url"], f"{round(p['bytes'] / 1e6, 2)} MB of HTML") for p in c.html if p["bytes"] > 1_000_000]
    over = any(p["bytes"] > 2_000_000 for p in c.html)
    return R("pass" if not big else "fail" if over else "warn", f"{len(big)} HTML file(s) over 1 MB" + (", some over Google's 2 MB limit" if over else "") if big else "all HTML files under 1 MB", big)


@check("TECH-094")
def _(c):
    bad = [it(p["url"], p.get("error") or p["status"]) for p in c.pages if p["status"] == 0]
    n = len(c.pages)
    return R("na", "no pages") if not n else R("pass" if len(bad) / n < 0.01 else "fail", f"{len(bad)} of {n} requests failed or timed out", bad)


@check("TECH-103")
def _(c):
    bad = [it(p["url"], "no Google tag found in the HTML source") for p in c.html if not p.get("analytics")]
    r = rate(len(c.html), bad, "pages", "analytics tag present")
    if bad:
        r["summary"] += " (tags injected only after consent or by a script-delay plugin are not visible to the crawler; confirm in the browser)"
    return r


@check("TECH-104")
def _(c):
    ok = (c.home or {}).get("msvalidate") or c.intake.get("setup", {}).get("bing_webmaster")
    return R("pass" if ok else "fail", "Bing verification found" if ok else "no msvalidate.01 meta on the homepage and not confirmed in the questionnaire (DNS/file verification cannot be seen from outside)")


# ---------------- Core Web Vitals and lab data (PageSpeed Insights) ----------------
def _psi(c):
    if not c.site.get("psi"):
        return None, {"status": "not_run", "summary": c.site.get("psi_error") or "PageSpeed Insights data was not collected in this run", "items": [], "count": 0}
    mine = {p["url"] for p in c.html}
    return {u: v for u, v in c.site["psi"].items() if u in mine} or c.site["psi"], None


def _cwv(cid, key, good, poor, unit, label, lab=None):
    fmt = (lambda x: f"{x / 1000:.1f} s") if unit == "s" else (lambda x: f"{x:.0f} ms") if unit == "ms" else (lambda x: f"{x:.2f}")

    @check(cid)
    def _(c):
        data, miss = _psi(c)
        if miss:
            return miss
        rows = [(u, v) for u, v in data.items() if v.get(key) is not None]
        if not rows:
            labs = [(u, v[lab]) for u, v in data.items() if lab and v.get(lab) is not None]
            note = "the Chrome UX Report has no real-user data for this site (not enough Chrome traffic), so Google has no Core Web Vitals to assess"
            if labs:
                note += f"; Lighthouse lab {label} on {len(labs)} sampled pages for reference, not a ranking signal: worst {fmt(max(x for _, x in labs))}"
            return R("na", note, [it(u, f"lab {label} {fmt(x)}") for u, x in sorted(labs, key=lambda r: -r[1]) if x > good])
        url_rows = [(u, v) for u, v in rows if v.get("field") != "origin"]
        origin = next((v for _, v in rows if v.get("field") == "origin"), None)
        bad = [it(u, f"{label} {fmt(v[key])} at the 75th percentile (this URL's own real-user data)") for u, v in url_rows if v[key] > good]
        vals = [v[key] for _, v in url_rows]
        if origin is not None:
            vals.append(origin[key])
            if origin[key] > good:
                bad.insert(0, it(c.site["root"], f"{label} {fmt(origin[key])} at the 75th percentile for the whole origin; Google has no URL-level data for {len(rows) - len(url_rows)} of the sampled pages, so it uses this origin value for them"))
        worst = max(vals)
        scope = f"{len(url_rows)} page(s) with their own field data" + (", origin-level data for the rest" if origin is not None else "")
        if not bad:
            return R("pass", f"'good' everywhere (worst {fmt(worst)}); {scope}")
        return R("fail" if worst > poor else "warn", f"above Google's 'good' threshold of {fmt(good)}; worst {fmt(worst)}; {scope}", bad)


_cwv("TECH-040", "lcp_ms", 2500, 4000, "s", "LCP", "lab_lcp_ms")
_cwv("TECH-041", "inp_ms", 200, 500, "ms", "INP")
_cwv("TECH-042", "cls", 0.1, 0.25, "", "CLS", "lab_cls")


def _lab(cid, key, label):
    @check(cid)
    def _(c):
        data, miss = _psi(c)
        if miss:
            return miss
        rows = [(u, v[key]) for u, v in data.items() if v.get(key) is not None]
        if not rows:
            return R("na", "no Lighthouse result returned")
        bad = [it(u, f"{label} score {s}") for u, s in rows if s < 90]
        low = min(s for _, s in rows)
        return R("pass" if not bad else "fail" if low < 50 else "warn", f"{len(bad)} of {len(rows)} sampled pages below 90 (lowest {low}); lab test on mobile" if bad else f"all {len(rows)} sampled pages score 90+", bad)


_lab("TECH-043", "lab_performance", "Lighthouse performance")
_lab("UX-001", "lab_accessibility", "Lighthouse accessibility")


@check("AEO-009")
def _(c):
    vids = [p for p in c.html if any("VideoObject" in n["t"] for n in p.get("ld", []))]
    if not vids:
        return R("na", "no page carries VideoObject markup")
    bad = [it(p["url"], "VideoObject without hasPart (Clip) or potentialAction (SeekToAction)") for p in vids
           if not any("VideoObject" in n["t"] and ({"hasPart", "potentialAction"} & set(n["k"])) for n in p["ld"])]
    return rate(len(vids), bad, "video pages", "key moments markup present")


# ---------------- Technical: international ----------------
def pairs(c):
    """slug -> {lang: page} for indexable pages, built from URL prefixes."""
    m = defaultdict(dict)
    for p in [x for x in c.all.values() if x.get("html")]:
        lang, slug = c.lang_of(p["url"])
        if lang:
            m[slug.rstrip("/") or "/"][lang] = p
    return m


def multilingual(c):
    return len(c.langs) > 1


@check("TECH-070")
def _(c):
    if not multilingual(c):
        return R("na", "single-language project")
    mine = {p["url"] for p in c.html}
    bad = [it(p["url"], "has a counterpart but no hreflang annotations") for g in pairs(c).values() if len(g) > 1 for p in g.values() if p["url"] in mine and not p["hreflang"]]
    return rate(len(c.html), bad, "pages", "hreflang present")


@check("TECH-071")
def _(c):
    if not multilingual(c):
        return R("na", "single-language project")
    bad = []
    for p in c.html:
        for h in p["hreflang"]:
            t = c.all.get(h["href"])
            if t and t.get("html") and t["url"] != p["url"] and not any(x["href"] == p["url"] for x in t["hreflang"]):
                bad.append(it(p["url"], f"references {h['href']} ({h['lang']}) which does not link back"))
    return rate(len([p for p in c.html if p["hreflang"]]), bad, "pages with hreflang", "all return links present")


@check("TECH-072")
def _(c):
    ok = re.compile(r"^(x-default|[a-z]{2,3}(-[A-Za-z]{4})?(-[A-Za-z]{2}|-\d{3})?)$")
    known_bad = {"en-uk", "ar-ar", "en-en"}
    bad = [it(p["url"], f"invalid code '{h['lang']}'") for p in c.html for h in p["hreflang"] if not ok.match(h["lang"]) or h["lang"].lower() in known_bad]
    return rate(len([p for p in c.html if p["hreflang"]]), bad, "pages with hreflang", "codes valid")


@check("TECH-073")
def _(c):
    bad = []
    for p in c.html:
        for h in p["hreflang"]:
            f = c.site["fetches"].get(h["href"])
            if f and (f["status"] != 200 or f["hops"]):
                bad.append(it(p["url"], f"hreflang {h['href']} returns {f['status']}" + (" via redirect" if f["hops"] else "")))
    return rate(len([p for p in c.html if p["hreflang"]]), bad, "pages with hreflang", "targets live")


@check("TECH-074")
def _(c):
    if not multilingual(c):
        return R("na", "single-language project")
    w = [p for p in c.html if p["hreflang"]]
    bad = [it(p["url"], "no x-default") for p in w if not any(h["lang"].lower() == "x-default" for h in p["hreflang"])]
    return rate(len(w), bad, "pages with hreflang", "x-default declared")


@check("TECH-075")
def _(c):
    if not multilingual(c):
        return R("na", "single-language project")
    codes = {l["code"] for l in c.langs}
    bad = []
    for slug, g in pairs(c).items():
        for missing in codes - set(g):
            p = next(iter(g.values()))
            linked = [h for h in p["hreflang"] if h["lang"].lower().startswith(missing)]
            if not linked:
                bad.append(it(p["url"], f"no {missing} version found"))
    total = len(pairs(c))
    return R("na", "no pages") if not total else R("pass" if not bad else "warn" if len(bad) / total <= 0.1 else "fail", f"{len(bad)} of {total} pages have no counterpart in another language", bad)


@check("TECH-076")
def _(c):
    if not multilingual(c):
        return R("na", "single-language project")
    bad, seen = [], set()
    for p in c.html:
        _, s1 = c.lang_of(p["url"])
        for h in p["hreflang"]:
            if h["lang"].lower() == "x-default" or not h["href"] or h["href"] == p["url"]:
                continue
            _, s2 = c.lang_of(h["href"])
            key = tuple(sorted((p["url"], h["href"])))
            if s1.rstrip("/") != s2.rstrip("/") and key not in seen:
                seen.add(key)
                bad.append(it(p["url"], f"slug differs from {h['href']}"))
    return R("pass" if not bad else "warn", f"{len(bad)} language pair(s) with different slugs" if bad else "slugs consistent", bad)


@check("TECH-078")
def _(c):
    bad = []
    for p in c.html:
        code, _ = c.lang_of(p["url"])
        if not p["lang"]:
            bad.append(it(p["url"], "html lang missing"))
        elif code and not p["lang"].startswith(code):
            bad.append(it(p["url"], f"html lang='{p['lang']}' on a {code} page"))
        elif (code or p["lang"][:2]) in RTL and p["dir"] != "rtl":
            bad.append(it(p["url"], "RTL language without dir='rtl' on <html>"))
    return rate(len(c.html), bad, "pages", "lang and dir correct")


@check("TECH-080")
def _(c):
    bad = []
    for p in c.html:
        u = urlparse(p["url"])
        if "_" in unquote(u.path):
            bad.append(it(p["url"], "underscores in path (Google recommends hyphens)"))
        elif re.search(r"(sessionid|sid|phpsessid)=", u.query, re.I):
            bad.append(it(p["url"], "session id in URL"))
    return rate(len(c.html), bad, "pages", "URLs readable")


@check("TECH-081")
def _(c):
    return rate(len(c.html), [it(p["url"], "uppercase characters in path") for p in c.html if re.search(r"[A-Z]", unquote(urlparse(p["url"]).path))], "pages", "lowercase URLs")


# ---------------- On-page: meta ----------------
@check("META-001")
def _(c):
    bad = [it(p["url"], "empty or missing title" if not p["title"] else f"{p['title_count']} title tags") for p in c.html if not p["title"] or p["title_count"] != 1]
    return R("na", "no pages") if not c.html else R("pass" if not bad else "fail", f"{len(bad)} page(s) without exactly one title" if bad else "every page has one title", bad)


def dupes(c, key):
    groups = defaultdict(list)
    for p in c.basic:
        v = (p.get(key) or "").strip().lower()
        if v:
            groups[(c.lang_of(p["url"])[0], v)].append(p["url"])
    return [it(u, f"shared by {len(us)} pages: \"{v[:90]}\"") for (_, v), us in groups.items() if len(us) > 1 for u in us]


@check("META-002")
def _(c):
    return rate(len(c.basic), dupes(c, "title"), "indexable pages", "titles unique")


@check("META-003")
def _(c):
    bad = [it(p["url"], f"{len(p['title'])} characters: \"{p['title'][:90]}\"") for p in c.basic if p["title"] and (len(p["title"]) > 60 or len(p["title"]) < 15)]
    return rate(len(c.basic), bad, "indexable pages", "title length fine")


@check("META-006")
def _(c):
    def toks(s):
        return {w for w in re.findall(r"\w+", s.lower()) if len(w) > 2}
    bad = []
    for p in c.basic:
        if p["title"] and p["h1"]:
            a, b = toks(p["title"]), toks(p["h1"][0])
            if a and b and len(a & b) / min(len(a), len(b)) < 0.5:
                bad.append(it(p["url"], f"title \"{p['title'][:60]}\" vs H1 \"{p['h1'][0][:60]}\""))
    return rate(len(c.basic), bad, "indexable pages", "title and H1 aligned")


@check("META-007")
def _(c):
    if not multilingual(c):
        return R("na", "single-language project")
    mine = {p["url"] for p in c.html}
    bad = []
    for g in pairs(c).values():
        ps = list(g.values())
        if len(ps) > 1 and len({p["title"].strip().lower() for p in ps if p["title"]}) == 1 and ps[0]["title"]:
            bad += [it(p["url"], f"same title in every language: \"{p['title'][:80]}\"") for p in ps if p["url"] in mine]
    return rate(len(c.html), bad, "pages", "titles translated")


@check("META-010")
def _(c):
    return rate(len(c.basic), [it(p["url"], "no meta description") for p in c.basic if not p["meta_desc"]], "indexable pages", "descriptions present")


@check("META-011")
def _(c):
    return rate(len(c.basic), dupes(c, "meta_desc"), "indexable pages", "descriptions unique")


@check("META-012")
def _(c):
    bad = [it(p["url"], f"{len(p['meta_desc'])} characters") for p in c.basic if p["meta_desc"] and not 70 <= len(p["meta_desc"]) <= 160]
    return rate(len(c.basic), bad, "indexable pages", "description length fine")


@check("META-020")
def _(c):
    bad = [it(p["url"], "missing og:" + ", og:".join(k for k, v in p["og"].items() if not v)) for p in c.indexable if not all(p["og"].values())]
    return rate(len(c.indexable), bad, "indexable pages", "Open Graph complete")


@check("META-021")
def _(c):
    return rate(len(c.indexable), [it(p["url"], "no twitter:card") for p in c.indexable if not p["twitter_card"]], "indexable pages", "twitter:card present")


@check("META-030")
def _(c):
    return R("na", "homepage not crawled") if not c.home or not c.home.get("html") else R("pass" if c.home["favicon"] else "fail", "favicon link found" if c.home["favicon"] else "no <link rel=icon> on the homepage")


@check("META-031")
def _(c):
    if not c.home or not c.home.get("html"):
        return R("na", "homepage not crawled")
    ok = "WebSite" in c.types(c.home)
    return R("pass" if ok else "fail", "WebSite structured data found" if ok else "no WebSite structured data on the homepage")


# ---------------- On-page: headings, content, blog, images, links, schema ----------------
@check("HEAD-001")
def _(c):
    return rate(len(c.basic), [it(p["url"], "no H1") for p in c.basic if not [h for h in p["h1"] if h]], "indexable pages", "H1 present")


@check("HEAD-002")
def _(c):
    bad = [it(p["url"], f"{len(p['h1'])} H1 tags") for p in c.basic if len(p["h1"]) > 1]
    r = rate(len(c.basic), bad, "indexable pages", "single H1")
    if r["status"] == "fail":
        r["status"] = "warn"
    return r


@check("HEAD-003")
def _(c):
    bad = []
    for p in c.indexable:
        prev = 0
        for lv, t in p["headings"]:
            if not t:
                bad.append(it(p["url"], f"empty H{lv}"))
                break
            if prev and lv > prev + 1:
                bad.append(it(p["url"], f"H{prev} followed by H{lv}: \"{t[:60]}\""))
                break
            prev = lv
    return rate(len(c.indexable), bad, "indexable pages", "hierarchy logical")


@check("CONT-001")
def _(c):
    mins = {"blog": 800, "solutions": 500, "products": 500}
    bad = []
    for p in c.basic:
        t = c.ptype(p)
        need = mins.get(t, 250)
        if p["words"] < need and t != "home":
            bad.append(it(p["url"], f"{p['words']} words (threshold for {t}: {need})"))
    return rate(len(c.basic), bad, "indexable pages", "content length fine")


@check("CONT-004")
def _(c):
    bad = [it(p["url"], f"\"{p['top_term']}\" is {round(p['top_term_share'] * 100, 1)}% of the main text") for p in c.indexable if p.get("top_term_share", 0) > 0.05]
    r = rate(len(c.indexable), bad, "indexable pages", "no single term above 5% of the text")
    if r["status"] == "fail":  # density is a signal to review, not proof of stuffing
        r["status"] = "warn"
    if bad:
        r["summary"] += " (one term above 5% of the text; review for unnatural repetition)"
    return r


def posts(c):
    return [p for p in c.indexable if c.ptype(p) == "blog"]


@check("BLOG-003")
def _(c):
    bad = [it(p["url"], "no <time> element and no datePublished in structured data") for p in posts(c) if not p["has_time"] and not any("datePublished" in n["k"] for n in p["ld"])]
    return rate(len(posts(c)), bad, "blog posts", "dates present")


@check("BLOG-004")
def _(c):
    need = ["headline", "image", "datePublished", "dateModified", "author"]
    bad = []
    for p in posts(c):
        arts = [n for n in p["ld"] if set(n["t"]) & {"Article", "BlogPosting", "NewsArticle"}]
        if not arts:
            bad.append(it(p["url"], "no Article/BlogPosting markup"))
        else:
            miss = [k for k in need if k not in arts[0]["k"]]
            if miss:
                bad.append(it(p["url"], "missing " + ", ".join(miss)))
    return rate(len(posts(c)), bad, "blog posts", "Article markup complete")


@check("BLOG-005")
def _(c):
    bad = []
    for p in posts(c):
        tg = [c.all.get(c.site["fetches"].get(l["href"], {}).get("final", l["href"])) for l in p["links_int"] if not l["nav"]]
        if not any(t and c.ptype(t) in ("products", "solutions") for t in tg):
            bad.append(it(p["url"], "no in-content link to a product/solution page"))
    return rate(len(posts(c)), bad, "blog posts", "all link to commercial pages")


@check("BLOG-009")
def _(c):
    if not posts(c):
        return R("na", "no blog posts found")
    ok = any(p.get("feed") for p in c.html)
    return R("pass" if ok else "fail", "feed link found" if ok else "no RSS/Atom feed link found")


@check("IMG-001")
def _(c):
    bad = []
    for p in c.indexable:
        miss = [i["src"] for i in p["images"] if i["alt"] is None or re.search(r"\.(jpe?g|png|webp|gif|svg)$", i["alt"] or "", re.I)]
        if miss:
            bad.append(it(p["url"], f"{len(miss)} image(s) without usable alt, e.g. {miss[0]}"))
    return rate(len(c.indexable), bad, "indexable pages", "alt text present")


@check("IMG-002")
def _(c):
    pat = re.compile(r"/(IMG|DSC|image|screenshot|untitled)[-_ ]?\d*\.[a-z]+$|/[0-9a-f]{16,}\.[a-z]+$", re.I)
    bad = []
    for p in c.indexable:
        m = [i["src"] for i in p["images"] if pat.search(urlparse(i["src"]).path)]
        if m:
            bad.append(it(p["url"], f"{len(m)} generic file name(s), e.g. {m[0]}"))
    return rate(len(c.indexable), bad, "indexable pages", "file names descriptive")


@check("IMG-004")
def _(c):
    bad = []
    for p in c.indexable:
        m = [i for i in p["images"] if not i["dims"]]
        if m:
            bad.append(it(p["url"], f"{len(m)} of {len(p['images'])} images without width/height attributes"))
    return rate(len(c.indexable), bad, "indexable pages", "dimensions set")


@check("IMG-007")
def _(c):
    bad = []
    for p in c.indexable:
        m = [i["src"] for i in p["images"] if i["in_link"] and not i["alt"]]
        if m:
            bad.append(it(p["url"], f"{len(m)} linked image(s) without alt, e.g. {m[0]}"))
    return rate(len(c.indexable), bad, "indexable pages", "linked images have alt")


@check("LINK-001")
def _(c):
    bad = []
    for p in c.indexable:
        g = [l for l in p["links_int"] if not l["nav"] and (not l["anchor"] or l["anchor"].strip().lower() in GENERIC_ANCHORS)]
        if g:
            bad.append(it(p["url"], f"{len(g)} generic/empty anchor(s), e.g. \"{g[0]['anchor'] or '(empty)'}\" to {g[0]['href']}"))
    return rate(len(c.indexable), bad, "indexable pages", "anchors descriptive")


@check("LINK-002")
def _(c):
    bad = [it(p["url"], f"{p['inlinks']} internal link(s) pointing here") for p in c.indexable if p is not c.home and p.get("inlinks", 0) < 3]
    return rate(len(c.indexable), bad, "indexable pages", "enough inbound links")


@check("LINK-003")
def _(c):
    bad = []
    for p in c.html:
        n = [l for l in p["links_int"] if "nofollow" in l["rel"]]
        if n:
            bad.append(it(p["url"], f"{len(n)} nofollow internal link(s), e.g. {n[0]['href']}"))
    return rate(len(c.html), bad, "pages", "no nofollow on internal links")


@check("SD-001")
def _(c):
    bad = [it(p["url"], f"{p['ld_errors']} JSON-LD block(s) fail to parse") for p in c.html if p["ld_errors"]]
    r = rate(len(c.html), bad, "pages", "JSON-LD parses (required-property validation per type is not implemented yet)")
    return r


def org_node(c):
    if not c.home or not c.home.get("html"):
        return None
    return next((n for n in c.home["ld"] if set(n["t"]) & {"Organization", "Corporation", "LocalBusiness", "ProfessionalService", "OnlineBusiness", "EducationalOrganization", "NewsMediaOrganization"}), None)


@check("SD-003")
def _(c):
    if not c.home or not c.home.get("html"):
        return R("na", "homepage not crawled")
    n = org_node(c)
    if not n:
        return R("fail", "no Organization structured data on the homepage")
    miss = [k for k in ("name", "url", "logo") if k not in n["k"]]
    return R("pass" if not miss else "warn", "Organization present" + (", missing " + ", ".join(miss) if miss else " with name, url, logo"))


@check("SD-004")
def _(c):
    inner = [p for p in c.indexable if c.ptype(p) != "home"]
    return rate(len(inner), [it(p["url"], "no BreadcrumbList") for p in inner if "BreadcrumbList" not in c.types(p)], "inner pages", "BreadcrumbList present")


@check("SD-005")
def _(c):
    bad = [it(p["url"], "blog post without Article/BlogPosting") for p in posts(c) if not c.types(p) & {"Article", "BlogPosting", "NewsArticle"}]
    bad += [it(p["url"], "product page without SoftwareApplication/Product") for p in c.indexable if c.ptype(p) == "products" and not c.types(p) & {"SoftwareApplication", "Product", "WebApplication", "Service"}]
    total = len(posts(c)) + len([p for p in c.indexable if c.ptype(p) == "products"])
    return rate(total, bad, "blog and product pages", "page-type markup present")


@check("SD-006")
def _(c):
    found = [it(p["url"], ", ".join(sorted(c.types(p) & {"FAQPage", "HowTo"}))) for p in c.html if c.types(p) & {"FAQPage", "HowTo"}]
    return R("info", f"{len(found)} page(s) use FAQPage/HowTo (no Google rich result; markup still parsed)", found)


# ---------------- GEO ----------------
@check("GEO-001")
def _(c):
    bad = []
    for p in c.indexable:
        r = " ".join(p["meta_robots"]) + " " + p["x_robots"]
        if "nosnippet" in r or re.search(r"max-snippet:\s*0\b", r):
            bad.append(it(p["url"], "snippet disabled: " + r.strip()))
    return R("na", "no pages") if not c.indexable else R("pass" if not bad else "fail", f"{len(bad)} indexable page(s) not snippet-eligible" if bad else "all indexable pages are snippet-eligible", bad)


def bot_allowed(c, bot):
    return c.rp.can_fetch(bot, c.site["start"])


def _bot(cid, bot):
    @check(cid)
    def _(c):
        ok = bot_allowed(c, bot)
        return R("pass" if ok else "fail", f"{bot} is {'allowed' if ok else 'disallowed'} in robots.txt")


for _cid, _b in AI_SEARCH_BOTS.items():
    _bot(_cid, _b)


@check("GEO-005")
def _(c):
    st = {b: bot_allowed(c, b) for b in ("Claude-SearchBot", "Claude-User")}
    bad = [b for b, ok in st.items() if not ok]
    return R("pass" if not bad else "fail", "Claude-SearchBot and Claude-User allowed" if not bad else "disallowed: " + ", ".join(bad))


@check("GEO-007")
def _(c):
    return R("info", "; ".join(f"{b}: {'allowed' if bot_allowed(c, b) else 'blocked'}" for b in TRAINING_BOTS))


@check("GEO-008")
def _(c):
    st = c.site["probes"]["ai_ua"]
    bad = [it(c.site["start"], f"{b} user agent received {s or 'no response'}") for b, s in st.items() if s != 200]
    if not bad:
        return R("pass", "homepage returns 200 to all AI search user agents")
    return R("warn", f"{len(bad)} of {len(st)} bot user agents were refused when requested from the audit server. Firewalls often refuse bot user agents "
             "coming from unverified IPs, so this is not proof that the real bots are blocked: check the CDN/WAF bot settings and server logs for these user agents", bad)


@check("GEO-013")
def _(c):
    s = c.site["probes"]["llms_txt"]
    return R("info", f"/llms.txt returns {s} (informational, not scored)")


@check("GEO-020")
def _(c):
    if not c.home or not c.home.get("html"):
        return R("na", "homepage not crawled")
    n = org_node(c)
    if not n:
        return R("fail", "no Organization entity on the homepage")
    want = ["name", "alternateName", "url", "logo", "description", "foundingDate", "address", "contactPoint", "sameAs"]
    miss = [k for k in want if k not in n["k"]]
    return R("pass" if not miss else "warn" if len(miss) <= 4 else "fail", "Organization entity complete" if not miss else "Organization missing: " + ", ".join(miss))


@check("GEO-021")
def _(c):
    n = org_node(c)
    if not n:
        return R("fail", "no Organization entity, so no sameAs")
    sa = n.get("sameAs", [])
    hosts = {urlparse(u).netloc.replace("www.", "") for u in sa if isinstance(u, str)}
    strong = hosts & {"linkedin.com", "wikidata.org", "crunchbase.com", "x.com", "twitter.com", "youtube.com", "github.com", "wikipedia.org", "en.wikipedia.org"}
    return R("pass" if "linkedin.com" in hosts and len(strong) >= 3 else "warn" if strong else "fail", f"sameAs lists {len(sa)} profile(s): " + (", ".join(sorted(hosts)) or "none"))


def site_links(c):
    return {l["href"]: l["anchor"] for p in c.html for l in p["links_int"]}


@check("GEO-030")
def _(c):
    hit = [u for u in site_links(c) if re.search(r"contact|تواصل|اتصل", u + " " + site_links(c)[u], re.I)]
    return R("pass" if hit else "fail", f"contact page linked: {hit[0]}" if hit else "no contact page link found (address/phone/email completeness is reviewed manually)")


@check("GEO-033")
def _(c):
    links = site_links(c)
    blob = " ".join(u + " " + a for u, a in links.items()).lower()
    miss = [n for n, pat in (("privacy policy", r"privacy|الخصوصية"), ("terms", r"terms|الشروط")) if not re.search(pat, blob)]
    return R("pass" if not miss else "fail", "privacy and terms pages linked" if not miss else "not found: " + ", ".join(miss))


# ---------------- AEO ----------------
@check("AEO-001")
def _(c):
    tgt = [p for p in c.indexable if c.ptype(p) in ("blog", "solutions", "products")]
    bad = []
    for p in tgt:
        q = [t for lv, t in p["headings"] if lv in (2, 3) and (Q_EN.match(t) or Q_AR.match(t))]
        if len(q) < 2:
            bad.append(it(p["url"], f"{len(q)} question-phrased H2/H3"))
    return rate(len(tgt), bad, "blog/solution/product pages", "question headings present")


@check("AEO-007")
def _(c):
    bad = []
    for p in c.indexable:
        m = re.search(r"max-snippet:\s*(\d+)", " ".join(p["meta_robots"]) + " " + p["x_robots"])
        if m and int(m.group(1)) < 50:
            bad.append(it(p["url"], f"max-snippet:{m.group(1)}"))
    return rate(len(c.indexable), bad, "indexable pages", "no restrictive snippet controls")


# ---------------- Local ----------------
@check("LOC-013")
def _(c):
    ok = any(p.get("tel_links") for p in c.html)
    return R("pass" if ok else "fail", "tel: link found" if ok else "no click-to-call link found on the site")


@check("LOC-020")
def _(c):
    ok = any("PostalAddress" in c.types(p) for p in c.html)
    return R("pass" if ok else "fail", "PostalAddress markup found" if ok else "no PostalAddress in structured data")
