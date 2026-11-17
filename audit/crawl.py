"""Crawler: fetches robots.txt, sitemaps and pages, and extracts the features the checks need."""
import json, re, time, random, string, gzip
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from urllib import robotparser
from urllib.parse import urljoin, urlparse, urldefrag
from xml.etree import ElementTree

import requests
from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (compatible; SEOAuditDashboard/0.1; +https://github.com/abdelrhmanramadan/seo-geo-audit-dashboard)"
AI_UAS = {
    "OAI-SearchBot": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot",
    "ChatGPT-User": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ChatGPT-User/1.0; +https://openai.com/bot",
    "PerplexityBot": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)",
    "Claude-SearchBot": "Mozilla/5.0 (compatible; Claude-SearchBot/1.0; +https://www.anthropic.com)",
    "bingbot": "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
}
SKIP_EXT = re.compile(r"\.(jpe?g|png|gif|webp|avif|svg|ico|pdf|zip|rar|gz|mp4|mp3|mov|webm|css|js|json|xml|woff2?|ttf|eot|docx?|xlsx?|pptx?)$", re.I)
STOP = set("the and for with that this from your you are our was will have has not but can all more about into their what when how why who which also than then them they its it's been were of to in on is a an as at by or be it we us".split())
TIMEOUT = 15


def host_key(url):
    h = urlparse(url).netloc.lower()
    return h[4:] if h.startswith("www.") else h


def norm(url):
    url = urldefrag(url)[0].strip()
    p = urlparse(url)
    if not p.scheme or not p.netloc:
        return None
    path = p.path or "/"
    return f"{p.scheme.lower()}://{p.netloc.lower()}{path}" + (f"?{p.query}" if p.query else "")


def fetch(session, url, ua=UA, max_hops=10):
    """GET with manual redirect following so the whole chain is recorded."""
    chain, cur, t0 = [], url, time.time()
    try:
        for _ in range(max_hops + 1):
            r = session.get(cur, headers={"User-Agent": ua, "Accept-Encoding": "gzip, deflate, br"}, timeout=TIMEOUT, allow_redirects=False)
            if r.is_redirect or r.status_code in (301, 302, 303, 307, 308):
                nxt = urljoin(cur, r.headers.get("Location", ""))
                chain.append({"from": cur, "status": r.status_code, "to": nxt})
                if nxt == cur or any(c["from"] == nxt for c in chain):
                    return {"url": url, "status": 0, "error": "redirect loop", "chain": chain, "final": cur}
                cur = nxt
                continue
            return {"url": url, "status": r.status_code, "final": cur, "chain": chain, "ttfb": round(r.elapsed.total_seconds() * 1000),
                    "headers": {k.lower(): v for k, v in r.headers.items()}, "body": r.content, "text": r.text if "html" in r.headers.get("Content-Type", "") or "xml" in r.headers.get("Content-Type", "") or "text" in r.headers.get("Content-Type", "") else ""}
        return {"url": url, "status": 0, "error": "too many redirects", "chain": chain, "final": cur}
    except requests.RequestException as e:
        return {"url": url, "status": 0, "error": type(e).__name__, "chain": chain, "final": cur, "ttfb": round((time.time() - t0) * 1000)}


def ld_nodes(obj, out):
    if isinstance(obj, list):
        for o in obj:
            ld_nodes(o, out)
    elif isinstance(obj, dict):
        t = obj.get("@type")
        if t:
            node = {"t": t if isinstance(t, list) else [t], "k": sorted(k for k in obj if not k.startswith("@"))}
            if "sameAs" in obj:
                sa = obj["sameAs"]
                node["sameAs"] = sa if isinstance(sa, list) else [sa]
            for k in ("name", "datePublished", "dateModified"):
                if isinstance(obj.get(k), str):
                    node[k] = obj[k][:200]
            out.append(node)
        for v in obj.values():
            ld_nodes(v, out)


def parse_page(html, url, site_host):
    soup = BeautifulSoup(html, "lxml")
    head = soup.head or soup
    p = {}
    titles = [t.get_text(" ", strip=True) for t in head.find_all("title")]
    p["title"], p["title_count"] = (titles[0] if titles else ""), len(titles)

    def meta(name, attr="name"):
        return [m.get("content", "").strip() for m in soup.find_all("meta", attrs={attr: re.compile(f"^{re.escape(name)}$", re.I)})]

    d = meta("description")
    p["meta_desc"] = d[0] if d else ""
    p["meta_robots"] = [x.lower() for x in meta("robots") + meta("googlebot")]
    p["viewport"] = bool(meta("viewport"))
    p["og"] = {k: (meta(f"og:{k}", "property") or [""])[0] for k in ("title", "description", "image", "url")}
    p["twitter_card"] = bool(meta("twitter:card") or meta("twitter:card", "property"))
    p["msvalidate"] = bool(meta("msvalidate.01"))
    p["canonicals"] = [urljoin(url, l.get("href", "")) for l in soup.find_all("link", rel=lambda r: r and "canonical" in r) if l.get("href")]
    p["canonical_raw_abs"] = all(urlparse(l.get("href", "")).scheme for l in soup.find_all("link", rel=lambda r: r and "canonical" in r))
    p["hreflang"] = [{"lang": l.get("hreflang", "").strip(), "href": norm(urljoin(url, l.get("href", "")))} for l in soup.find_all("link", rel=lambda r: r and "alternate" in r) if l.get("hreflang")]
    p["favicon"] = bool(soup.find("link", rel=lambda r: r and "icon" in " ".join(r).lower()))
    p["feed"] = bool(soup.find("link", attrs={"type": re.compile("rss|atom", re.I)}))
    html_tag = soup.find("html")
    p["lang"] = (html_tag.get("lang", "") if html_tag else "").lower()
    p["dir"] = (html_tag.get("dir", "") if html_tag else "").lower()
    p["analytics"] = bool(re.search(r"googletagmanager\.com|google-analytics\.com|gtag\(", html))
    p["gtm"] = "googletagmanager.com/gtm.js" in html or bool(re.search(r"GTM-[A-Z0-9]{4,}", html))
    p["mixed"] = len(re.findall(r"""(?:src|href)=["']http://[^"']+\.(?:js|css|png|jpe?g|gif|webp|svg|woff2?)""", html, re.I)) if url.startswith("https://") else 0

    nodes, errors = [], 0
    for s in soup.find_all("script", type=re.compile("ld\\+json", re.I)):
        try:
            ld_nodes(json.loads(s.string or s.get_text() or ""), nodes)
        except Exception:
            errors += 1
    p["ld"], p["ld_errors"] = nodes[:60], errors
    p["ld_types"] = sorted({t for n in nodes for t in n["t"]})

    heads = [(int(h.name[1]), h.get_text(" ", strip=True)) for h in soup.find_all(re.compile("^h[1-6]$"))]
    p["headings"] = heads[:80]
    p["h1"] = [t for lv, t in heads if lv == 1]
    p["has_time"] = bool(soup.find("time"))
    p["tel_links"] = len(soup.select('a[href^="tel:"]'))

    imgs = []
    for im in soup.find_all("img"):
        src = im.get("src") or im.get("data-src") or ""
        if not src or src.startswith("data:"):
            continue
        imgs.append({"src": urljoin(url, src), "alt": im.get("alt"), "dims": bool(im.get("width") and im.get("height")), "in_link": bool(im.find_parent("a"))})
    p["images"] = imgs[:150]

    li, le = [], []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith(("mailto:", "tel:", "javascript:", "#")) or not href:
            continue
        u = norm(urljoin(url, href))
        if not u:
            continue
        anchor = a.get_text(" ", strip=True) or (a.find("img").get("alt") or "" if a.find("img") else "")
        rel = " ".join(a.get("rel") or []).lower()
        in_nav = bool(a.find_parent(["nav", "header", "footer"]))
        (li if host_key(u) == site_host else le).append({"href": u, "anchor": anchor[:120], "rel": rel, "nav": in_nav})
    p["links_int"], p["links_ext"] = li[:600], le[:200]

    body = soup.find("main") or soup.find("article") or soup.body or soup
    for t in body.find_all(["script", "style", "noscript", "nav", "header", "footer", "aside", "form"]):
        t.decompose()
    text = body.get_text(" ", strip=True)
    words = text.split()
    p["words"] = len(words)
    p["intro"] = " ".join(words[:120])
    toks = [w.lower().strip(".,:;!?()\"'") for w in words]
    toks = [w for w in toks if len(w) > 3 and w not in STOP]
    if len(toks) >= 200:
        term, n = Counter(toks).most_common(1)[0]
        p["top_term"], p["top_term_share"] = term, round(n / len(toks), 4)
    return p


def read_sitemaps(session, urls, limit_files=30):
    out, files, errors, seen = {}, [], [], set()
    queue = list(urls)
    while queue and len(files) < limit_files:
        u = queue.pop(0)
        if u in seen:
            continue
        seen.add(u)
        r = fetch(session, u)
        files.append({"url": u, "status": r["status"]})
        if r["status"] != 200:
            errors.append(f"{u} returned {r['status'] or r.get('error')}")
            continue
        raw = r["body"]
        try:
            if raw[:2] == b"\x1f\x8b":
                raw = gzip.decompress(raw)
            root = ElementTree.fromstring(raw)
        except Exception:
            errors.append(f"{u} is not valid XML")
            continue
        ns = re.match(r"\{.*\}", root.tag)
        ns = ns.group(0) if ns else ""
        for sm in root.findall(f"{ns}sitemap/{ns}loc"):
            queue.append(sm.text.strip())
        for el in root.findall(f"{ns}url"):
            loc = el.find(f"{ns}loc")
            if loc is None or not loc.text:
                continue
            lm = el.find(f"{ns}lastmod")
            n = norm(loc.text.strip())
            if n:
                out[n] = lm.text.strip() if lm is not None and lm.text else None
    return {"urls": out, "files": files, "errors": errors}


def crawl(start, max_pages=500, workers=5, log=print):
    start = norm(start if "://" in start else "https://" + start)
    root = f"{urlparse(start).scheme}://{urlparse(start).netloc}"
    site_host = host_key(start)
    s = requests.Session()
    site = {"start": start, "root": root, "host": site_host, "crawled_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}

    # robots.txt
    rb = fetch(s, root + "/robots.txt")
    rtxt = rb.get("text", "") if rb["status"] == 200 else ""
    site["robots"] = {"status": rb["status"], "bytes": len(rb.get("body", b"")), "text": rtxt[:20000],
                      "sitemaps": [l.split(":", 1)[1].strip() for l in rtxt.splitlines() if l.lower().startswith("sitemap:")]}
    rp = robotparser.RobotFileParser()
    rp.parse(rtxt.splitlines())
    site["_rp"] = rp

    # sitemaps
    sm = read_sitemaps(s, site["robots"]["sitemaps"] or [root + "/sitemap.xml"])
    sm["declared"] = bool(site["robots"]["sitemaps"])
    site["sitemap"] = sm
    sm_urls = [u for u in sm["urls"] if host_key(u) == site_host]

    # probes
    home = fetch(s, start)
    rnd = root + "/" + "".join(random.choices(string.ascii_lowercase, k=18)) + "-audit-probe"
    p404 = fetch(s, rnd)
    bare = site_host
    variants = {}
    for v in (f"http://{bare}/", f"http://www.{bare}/", f"https://{bare}/", f"https://www.{bare}/"):
        r = fetch(s, v)
        variants[v] = {"status": r["status"], "final": r.get("final"), "hops": len(r.get("chain", []))}
    llms = fetch(s, root + "/llms.txt")
    site["probes"] = {"soft404": {"url": rnd, "status": p404["status"], "final": p404.get("final")}, "variants": variants,
                      "llms_txt": llms["status"],
                      "ai_ua": {name: fetch(s, start, ua=ua)["status"] for name, ua in AI_UAS.items()}}

    # crawl (breadth first from the homepage, then sitemap-only URLs)
    pages, fetches, depth = {}, {}, {start: 0}
    frontier, queued = [start], {start}
    extra = [u for u in sm_urls if u not in queued]

    def work(u):
        if not rp.can_fetch("*", u):
            return u, {"url": u, "status": -1, "error": "blocked by robots.txt", "chain": [], "final": u}
        r = home if u == start else fetch(s, u)
        time.sleep(0.15)
        return u, r

    while (frontier or extra) and len(pages) < max_pages:
        if not frontier:
            frontier = extra[: max_pages - len(pages)]
            extra = extra[len(frontier):]
            for u in frontier:
                queued.add(u)
                depth.setdefault(u, None)
        batch, frontier = frontier[: max_pages - len(pages)], []
        with ThreadPoolExecutor(workers) as ex:
            results = list(ex.map(work, batch))
        for u, r in results:
            final = norm(r.get("final") or u) or u
            fetches[u] = {"status": r["status"], "final": final, "hops": len(r.get("chain", [])), "error": r.get("error")}
            if final in pages:
                continue
            hd = r.get("headers", {})
            page = {"url": final, "requested": u, "status": r["status"], "error": r.get("error"), "hops": len(r.get("chain", [])), "chain": r.get("chain", []),
                    "ttfb": r.get("ttfb"), "bytes": len(r.get("body", b"")), "ctype": hd.get("content-type", ""), "encoding": hd.get("content-encoding", ""),
                    "x_robots": hd.get("x-robots-tag", "").lower(), "hsts": hd.get("strict-transport-security", ""),
                    "cache_control": hd.get("cache-control", ""), "depth": depth.get(u), "in_sitemap": final in sm["urls"] or u in sm["urls"], "html": False}
            if r["status"] == 200 and "html" in page["ctype"] and host_key(final) == site_host:
                page["html"] = True
                page.update(parse_page(r["text"], final, site_host))
                for l in page["links_int"]:
                    t = l["href"]
                    if t not in queued and not SKIP_EXT.search(urlparse(t).path):
                        queued.add(t)
                        depth[t] = (depth.get(u) or 0) + 1
                        frontier.append(t)
            pages[final] = page
        extra = [u for u in extra if u not in queued]
        log(f"crawled {len(pages)} pages, {len(frontier)} queued")

    inl = Counter()
    for p in pages.values():
        for t in {l["href"] for l in p.get("links_int", [])}:
            if t != p["url"]:
                inl[fetches.get(t, {}).get("final", t)] += 1
    for u, p in pages.items():
        p["inlinks"] = inl.get(u, 0)
    site.update(pages=pages, fetches=fetches, truncated=bool(frontier or extra))
    return site
