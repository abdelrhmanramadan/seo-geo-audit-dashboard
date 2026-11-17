"""Merge a Screaming Frog 'Internal: All' CSV export into the crawl.
Pages the built-in crawler did not reach are added with the fields Screaming Frog provides; they are marked
partial and only feed the checks that need those fields (titles, descriptions, H1, word count, status, depth)."""
import csv
from .crawl import norm, host_key


def merge(site, path):
    added = 0
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    hi = next((i for i, r in enumerate(rows[:5]) if "Address" in r), None)
    if hi is None:
        raise ValueError("Not a Screaming Frog internal export: no 'Address' column found")
    head = rows[hi]
    for r in rows[hi + 1:]:
        d = dict(zip(head, r))
        url = norm(d.get("Address", ""))
        if not url or host_key(url) != site["host"] or url in site["pages"]:
            continue

        def num(k):
            try:
                return float(d.get(k) or 0)
            except ValueError:
                return 0
        status = int(num("Status Code"))
        html = "html" in d.get("Content Type", "").lower()
        canon = d.get("Canonical Link Element 1", "")
        site["pages"][url] = {"url": url, "requested": url, "status": status, "hops": 0, "chain": [], "html": False, "partial": html and status == 200,
                              "source": "screaming_frog", "indexable_sf": d.get("Indexability", "").lower() == "indexable", "bytes": int(num("Size (bytes)")),
                              "title": d.get("Title 1", ""), "title_count": 1 if d.get("Title 1") else 0, "meta_desc": d.get("Meta Description 1", ""),
                              "h1": [h for h in (d.get("H1-1", ""), d.get("H1-2", "")) if h], "words": int(num("Word Count")),
                              "depth": int(num("Crawl Depth")) if d.get("Crawl Depth") else None, "inlinks": int(num("Unique Inlinks") or num("Inlinks")),
                              "ttfb": round(num("Response Time") * 1000) or None, "canonicals": [canon] if canon else [], "meta_robots": [d.get("Meta Robots 1", "").lower()],
                              "x_robots": d.get("X-Robots-Tag 1", "").lower(), "in_sitemap": url in site["sitemap"]["urls"]}
        site["fetches"].setdefault(url, {"status": status, "final": url, "hops": 0, "error": None})
        added += 1
    return added
