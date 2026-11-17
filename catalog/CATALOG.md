# Checks Catalog

Version 0.5.0 · updated 2026-11-11 · generated from `checks.yaml` (do not edit by hand)

## Summary

| Pillar | Weight in overall score | Checks |
|---|---|---|
| SEO | 40% | 154 |
| GEO (Generative Engine Optimization) | 25% | 47 |
| AEO (Answer Engine Optimization) | 15% | 18 |
| Local SEO | 20% | 23 |
| Site-type modules | 15% | 43 |
| **Total** | 100% | **285** |

## Scoring model

- **page scope rule**: For page-scope checks: no failing page = pass, up to 10% of applicable pages failing = warn, more = fail. The report lists the failing URLs.
- **severity floor**: Any failing critical check caps its subsection score at 60 and its pillar score at 75, so a site cannot look healthy while it has a blocking issue.
- **subsection score**: sum(weight x result) / sum(weight of applicable checks) x 100
- **section score**: weighted average of its subsections (subsection weights below)
- **pillar score**: weighted average of its sections (section weights below)
- **overall score**: weighted average of active pillars; N/A pillars (Local for non-local businesses, Site-type modules when none applies) are removed and the weights renormalised to 100
- **per language**: every score is computed per language version and for the project as a whole
- **basis rule**: Only checks with basis 'google' (documented in Google Search Central or Google help pages) count toward scores. Checks with basis 'platform' or 'industry' are run and reported as best practice, unscored.
- **results**: pass = 1, warn = 0.5, fail = 0; N/A and info are excluded from the denominator

## Structure

- **SEO**
  - Technical SEO (40%)
    - Crawlability (18%) — 20 checks
    - Indexability (18%) — 11 checks
    - JavaScript rendering (9%) — 3 checks
    - Page experience & Core Web Vitals (14%) — 7 checks
    - Mobile (8%) — 4 checks
    - Security (9%) — 5 checks
    - International & multilingual (10%) — 11 checks
    - URL structure (4%) — 2 checks
    - Server & delivery (5%) — 5 checks
    - Measurement & verification (5%) — 6 checks
  - On-page SEO (45%)
    - Meta & SERP appearance (18%) — 15 checks
    - Headings (5%) — 4 checks
    - Content quality (25%) — 14 checks
    - Blog & articles (14%) — 11 checks
    - Images & media (9%) — 7 checks
    - Internal linking (9%) — 5 checks
    - Structured data (15%) — 11 checks
    - Accessibility & UX (5%) — 3 checks
  - Off-page SEO (15%)
    - Authority & backlinks (100%) — 10 checks
- **GEO (Generative Engine Optimization)**
  - AI crawler access (20%)
    - Bot access (100%) — 10 checks
  - Machine readability (10%)
    - Server HTML (100%) — 5 checks
  - Brand entity (15%)
    - Entity clarity (100%) — 7 checks
  - E-E-A-T & trust (15%)
    - Trust signals (100%) — 5 checks
  - Citability (15%)
    - Passage quality (100%) — 10 checks
  - AI answer visibility (15%)
    - Mentions & citations (100%) — 5 checks
  - Off-site presence (10%)
    - Platforms AI engines cite (100%) — 5 checks
- **AEO (Answer Engine Optimization)**
  - Answer formats (50%)
    - Snippet-ready content (100%) — 11 checks
  - Question coverage (30%)
    - Question coverage (100%) — 3 checks
  - SERP answer features (20%)
    - Feature ownership (100%) — 4 checks
- **Local SEO**
  - Google Business Profile (35%)
    - Profile (100%) — 12 checks
  - NAP consistency (25%)
    - Name, Address, Phone (100%) — 4 checks
  - Local structured data (15%)
    - LocalBusiness markup (100%) — 2 checks
  - Location pages (15%)
    - Location content (100%) — 2 checks
  - Citations & other maps (10%)
    - Listings (100%) — 3 checks
- **Site-type modules**
  - E-commerce (100%)
    - E-commerce checks (100%) — 15 checks
  - News & publishers (100%)
    - News & publishers checks (100%) — 10 checks
  - SaaS & software (100%)
    - SaaS & software checks (100%) — 10 checks
  - Services & lead generation (100%)
    - Services & lead generation checks (100%) — 8 checks


---

## SEO

### Technical SEO — 40% of SEO

#### Crawlability — 18% of Technical SEO

**TECH-001 · robots.txt reachable**  
`critical` · weight 8 · scope: site · method: crawl · Google official: [Introduction to robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/intro)

- **Test:** GET /robots.txt returns 200 (rules parsed) or 404 (treated as allow-all). 5xx = fail (Google pauses crawling). 3xx chain > 5 hops = fail.
- **Fix:** Serve robots.txt as text/plain with 200. If the server returns 5xx for it, fix the origin/CDN rule first: Google treats a persistent 5xx robots.txt as a full disallow.

**TECH-002 · robots.txt does not block important URLs**  
`critical` · weight 10 · scope: site · method: crawl · Google official: [Introduction to robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/intro)

- **Test:** No URL in the sitemap or main navigation is disallowed for Googlebot.
- **Fix:** Remove or narrow the Disallow rule that matches the listed URLs. Use noindex (not Disallow) for pages that must stay out of the index; a disallowed page cannot have its noindex read.

**TECH-003 · robots.txt does not block CSS/JS/images**  
`high` · weight 6 · scope: site · method: crawl · Google official: [JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics)

- **Test:** Rendering resources referenced by templates (CSS, JS, images, fonts) are not disallowed.
- **Fix:** Allow the asset paths listed in the report. Google must fetch them to render the page as users see it.

**TECH-004 · Sitemap declared in robots.txt**  
`low` · weight 2 · scope: site · method: crawl · Google official: [Build and submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)

- **Test:** robots.txt contains at least one absolute Sitemap: directive.
- **Fix:** Add `Sitemap: https://<domain>/sitemap.xml` to robots.txt and submit the same URL in Search Console.

**TECH-005 · XML sitemap valid**  
`high` · weight 6 · scope: site · method: crawl · Google official: [Build and submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)

- **Test:** Sitemap (or index) returns 200, parses as XML, uses absolute URLs, <= 50,000 URLs and <= 50 MB uncompressed per file.
- **Fix:** Regenerate the sitemap from the CMS; split into a sitemap index if limits are exceeded.

**TECH-006 · Sitemap contains only indexable canonical URLs**  
`medium` · weight 5 · scope: site · method: crawl · Google official: [Build and submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)

- **Test:** Every sitemap URL returns 200, is not noindex, and is its own canonical. > 2% violations = warn, > 10% = fail.
- **Fix:** Remove redirected, 404, noindex and canonicalised-away URLs from the sitemap. Listed in the report with the reason per URL.

**TECH-007 · Sitemap lastmod is accurate**  
`low` · weight 2 · scope: site · method: crawl · Google official: [Build and submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)

- **Test:** lastmod present and not identical for all URLs; not in the future.
- **Fix:** Set lastmod to the date of the last significant content change. Google ignores lastmod when it is consistently unreliable.

**TECH-008 · Internal links are crawlable <a href>**  
`high` · weight 6 · scope: page · method: render · Google official: [Link best practices for Google](https://developers.google.com/search/docs/crawling-indexing/links-crawlable)

- **Test:** Navigation and in-content links use <a href='resolvable URL'>. Links that only exist as onclick/JS handlers or href='#' = fail.
- **Fix:** Replace JS-only navigation with real anchor elements pointing to resolvable URLs.

**TECH-009 · No broken internal links**  
`high` · weight 7 · scope: page · method: crawl · Google official: [How HTTP status codes affect Google's crawlers](https://developers.google.com/crawling/docs/troubleshooting/http-status-codes)

- **Test:** No internal link resolves to 4xx/5xx.
- **Fix:** Update each broken link to the live URL, or 301 the dead URL to its closest equivalent. Report lists source page, anchor text and target.

**TECH-010 · No redirect chains or loops**  
`medium` · weight 4 · scope: site · method: crawl · Google official: [Redirects and Google Search](https://developers.google.com/search/docs/crawling-indexing/301-redirects)

- **Test:** Every redirect resolves in 1 hop. 2 to 10 hops = warn (works, but wasteful). More than 10 hops or a loop = fail: Google's crawlers follow up to 10 redirect hops by default.
- **Fix:** Point the first URL directly at the final destination.

**TECH-011 · Internal links point to final URLs**  
`low` · weight 3 · scope: page · method: crawl · Industry practice: [Redirects and Google Search](https://developers.google.com/search/docs/crawling-indexing/301-redirects)

- **Test:** Internal links do not target URLs that redirect.
- **Fix:** Update internal links to the final destination URL to save crawl and avoid signal loss through hops.

**TECH-012 · No server errors (5xx)**  
`critical` · weight 8 · scope: site · method: crawl · Google official: [How HTTP status codes affect Google's crawlers](https://developers.google.com/crawling/docs/troubleshooting/http-status-codes)

- **Test:** No crawled URL returns 5xx.
- **Fix:** Investigate origin logs for the listed URLs. Persistent 5xx reduces crawl rate and eventually drops URLs from the index.

**TECH-013 · Real 404 status for missing pages (no soft 404)**  
`medium` · weight 4 · scope: site · method: crawl · Google official: [How HTTP status codes affect Google's crawlers](https://developers.google.com/crawling/docs/troubleshooting/http-status-codes)

- **Test:** A random non-existent URL returns 404/410, not 200 or a redirect to the homepage.
- **Fix:** Configure the CMS to return 404 for unknown paths with a helpful custom 404 template.

**TECH-014 · Click depth**  
`medium` · weight 4 · scope: page · method: crawl · Industry practice: [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)

- **Test:** Important pages reachable within 3 clicks from the homepage. 4-5 = warn, > 5 = fail.
- **Fix:** Surface deep pages through hub pages, category pages or contextual links.

**TECH-015 · No orphan pages**  
`medium` · weight 4 · scope: page · method: crawl · Google official: [Link best practices for Google](https://developers.google.com/search/docs/crawling-indexing/links-crawlable)

- **Test:** Every sitemap URL receives at least one internal link from a crawled page.
- **Fix:** Link each orphan from its relevant hub (e.g. solution page -> related blog posts), or remove it from the sitemap if obsolete.

**TECH-016 · Sitemap URLs not blocked by robots.txt**  
`high` · weight 5 · scope: site · method: crawl · Google official: [Build and submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)

- **Test:** No sitemap URL is disallowed in robots.txt.
- **Fix:** Remove the URL from the sitemap or lift the Disallow; conflicting signals waste crawl.

**TECH-017 · robots.txt within size limit**  
`low` · weight 2 · scope: site · method: crawl · Industry practice: [Introduction to robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/intro)

- **Test:** robots.txt <= 500 KiB (Google ignores content after the limit).
- **Fix:** Consolidate rules; use path patterns instead of listing URLs.

**TECH-018 · No crawl traps**  
`medium` · weight 4 · scope: site · method: crawl · Google official: [Managing crawl budget for large sites](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget)

- **Test:** No infinite URL spaces (calendars, faceted combinations, session paths) detected: > 500 URLs differing only by parameters/path repetition = fail.
- **Fix:** Block the trap pattern in robots.txt or stop generating crawlable links to it.

**TECH-019 · No meta refresh or JavaScript redirects**  
`medium` · weight 4 · scope: page · method: render · Google official: [Redirects and Google Search](https://developers.google.com/search/docs/crawling-indexing/301-redirects)

- **Test:** Redirects are server-side 301/308; meta refresh or JS location changes flagged.
- **Fix:** Replace with a server-side 301 (permanent) redirect.

**TECH-019B · Correct redirect type**  
`low` · weight 3 · scope: site · method: crawl · Google official: [Redirects and Google Search](https://developers.google.com/search/docs/crawling-indexing/301-redirects)

- **Test:** Permanent moves use 301/308; 302/307 kept > 30 days on the same URL flagged.
- **Fix:** Switch long-lived temporary redirects to 301.

#### Indexability — 18% of Technical SEO

**TECH-020 · No unintended noindex**  
`critical` · weight 10 · scope: page · method: crawl · Google official: [Robots meta tag, data-nosnippet and X-Robots-Tag](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag)

- **Test:** Pages in the sitemap/navigation carry no noindex in meta robots or X-Robots-Tag.
- **Fix:** Remove the noindex from the listed pages. Check both the HTML meta and the HTTP header (CDN/hosting rules often inject X-Robots-Tag).

**TECH-021 · Canonical tag present**  
`medium` · weight 5 · scope: page · method: crawl · Industry practice: [How to specify a canonical URL](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)

- **Test:** Exactly one rel=canonical with an absolute URL in <head>.
- **Fix:** Add a self-referencing absolute canonical to every indexable template. Remove duplicate canonical tags.

**TECH-022 · Canonical target is valid**  
`high` · weight 7 · scope: page · method: crawl · Industry practice: [How to specify a canonical URL](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)

- **Test:** Canonical target returns 200, is indexable and is not itself canonicalised or redirected.
- **Fix:** Point the canonical at the live, indexable preferred URL.

**TECH-023 · Canonical signals are consistent**  
`medium` · weight 4 · scope: page · method: crawl · Google official: [How to specify a canonical URL](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)

- **Test:** Canonical, sitemap, hreflang and internal links all reference the same preferred URL.
- **Fix:** Align the signals; conflicting signals let Google pick a different canonical than intended.

**TECH-024 · Host and protocol consolidated**  
`high` · weight 6 · scope: site · method: crawl · Google official: [How to specify a canonical URL](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)

- **Test:** http://, https://, www and non-www variants 301 to one preferred host.
- **Fix:** Add 301 rules at the CDN/host so every variant lands on the single preferred https host.

**TECH-025 · Trailing slash and case consistency**  
`low` · weight 2 · scope: site · method: crawl · Google official: [URL structure best practices](https://developers.google.com/search/docs/crawling-indexing/url-structure)

- **Test:** Slash/no-slash and upper/lower-case variants redirect to one form.
- **Fix:** Pick one convention and 301 the other variants to it.

**TECH-026 · No near-duplicate pages**  
`medium` · weight 5 · scope: page · method: crawl · Google official: [How to specify a canonical URL](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)

- **Test:** Main-content similarity between two indexable pages < 90% (SimHash on boilerplate-stripped text).
- **Fix:** Merge the duplicates, differentiate their content, or canonicalise one to the other. Pairs are listed with similarity %.

**TECH-027 · Parameter URLs controlled**  
`low` · weight 3 · scope: site · method: crawl · Google official: [Managing crawl budget for large sites](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget)

- **Test:** Tracking/filter parameter URLs (utm_, sort, session ids) are canonicalised to the clean URL and not linked internally.
- **Fix:** Canonicalise parameter variants to the clean URL and stop linking to them internally.

**TECH-028 · Non-HTML files indexable intentionally**  
`low` · weight 2 · scope: site · method: crawl · Google official: [Robots meta tag, data-nosnippet and X-Robots-Tag](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag)

- **Test:** PDFs/docs that duplicate HTML pages carry X-Robots-Tag noindex or a Link: rel=canonical header.
- **Fix:** Add an HTTP canonical or noindex header for duplicate documents.

**TECH-029 · Archive/tag pages controlled**  
`low` · weight 3 · scope: page · method: crawl · Industry practice: [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

- **Test:** Thin tag, author or date archives (< 3 items or no unique text) are noindexed or not generated.
- **Fix:** Noindex or remove thin archive pages.

**TECH-029B · No conflicting robots directives**  
`medium` · weight 4 · scope: page · method: crawl · Industry practice: [Robots meta tag, data-nosnippet and X-Robots-Tag](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag)

- **Test:** No page has multiple robots meta tags/headers with contradictory values (Google applies the most restrictive).
- **Fix:** Keep one robots directive per page.

#### JavaScript rendering — 9% of Technical SEO

**TECH-030 · Main content present in initial HTML**  
`high` · weight 8 · scope: page · method: render · Google official: [JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics)

- **Test:** Raw HTML contains >= 80% of the rendered main-content text. 50-79% = warn, < 50% = fail.
- **Fix:** Server-render or pre-render the main content. Google can render JS (deferred), but most AI crawlers cannot (see GEO-011).

**TECH-031 · Title, meta, canonical not injected by JS only**  
`medium` · weight 5 · scope: page · method: render · Google official: [JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics)

- **Test:** Title, meta description, canonical and robots meta are identical in raw and rendered HTML.
- **Fix:** Output head tags server-side; do not change canonical or robots via JavaScript.

**TECH-032 · Lazy-loaded content is crawlable**  
`medium` · weight 4 · scope: page · method: render · Google official: [Fix lazy-loaded content](https://developers.google.com/search/docs/crawling-indexing/javascript/lazy-loading)

- **Test:** Lazy-loaded images/sections load without scroll or interaction events (native loading=lazy or IntersectionObserver).
- **Fix:** Use native loading='lazy' or IntersectionObserver; never require scroll/click to inject content.

#### Page experience & Core Web Vitals — 14% of Technical SEO

**TECH-040 · LCP (field data)**  
`high` · weight 7 · scope: site · method: api:psi · Google official: [Core Web Vitals and Google Search](https://developers.google.com/search/docs/appearance/core-web-vitals)

- **Test:** 75th-percentile LCP from the Chrome UX Report (via PageSpeed Insights) on a sample of pages: up to 2.5 s good, up to 4 s needs improvement, above poor. Falls back to origin-level data.
- **Fix:** Report shows the LCP element from Lighthouse. Typical levers: preload/priority-hint the hero image, serve AVIF/WebP at the rendered size, cut server TTFB, remove render-blocking CSS/JS.

**TECH-041 · INP (field data)**  
`high` · weight 7 · scope: site · method: api:psi · Google official: [Core Web Vitals and Google Search](https://developers.google.com/search/docs/appearance/core-web-vitals)

- **Test:** 75th-percentile INP from the Chrome UX Report on a sample of pages: up to 200 ms good, up to 500 ms needs improvement, above poor.
- **Fix:** Break up long tasks, defer third-party scripts (chat widgets, tag managers), reduce main-thread JS. Report lists the heaviest scripts.

**TECH-042 · CLS (field data)**  
`medium` · weight 6 · scope: site · method: api:psi · Google official: [Core Web Vitals and Google Search](https://developers.google.com/search/docs/appearance/core-web-vitals)

- **Test:** 75th-percentile CLS from the Chrome UX Report on a sample of pages: up to 0.1 good, up to 0.25 needs improvement, above poor.
- **Fix:** Set width/height on images and embeds, reserve space for banners/cookie bars, use font-display with size-adjusted fallbacks.

**TECH-043 · Lighthouse performance (lab, mobile)**  
`low` · weight 3 · scope: page · method: api:psi · Industry practice: [Understanding page experience](https://developers.google.com/search/docs/appearance/page-experience)

- **Test:** Mobile performance score >= 90 pass, 50-89 warn, < 50 fail. Diagnostic only; field data (TECH-040-042) outweighs it.
- **Fix:** Follow the top 3 Lighthouse opportunities listed per URL.

**TECH-044 · Server response time (TTFB)**  
`medium` · weight 4 · scope: page · method: crawl · Industry practice: [Managing crawl budget for large sites](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget)

- **Test:** TTFB <= 800 ms pass, <= 1800 ms warn, > 1800 ms fail (measured from the crawler region, repeated 3x).
- **Fix:** Enable CDN HTML caching, review origin/database latency.

**TECH-045 · LCP image not lazy-loaded**  
`medium` · weight 4 · scope: page · method: api:psi · Industry practice: [Fix lazy-loaded content](https://developers.google.com/search/docs/crawling-indexing/javascript/lazy-loading)

- **Test:** The LCP element is not loading='lazy' and has fetchpriority='high' or a preload.
- **Fix:** Remove lazy loading from the hero image and add fetchpriority='high'.

**TECH-046 · No intrusive interstitials**  
`medium` · weight 4 · scope: page · method: render · Google official: [Understanding page experience](https://developers.google.com/search/docs/appearance/page-experience)

- **Test:** No full-screen popup covering main content on mobile at load (cookie/legal notices excepted).
- **Fix:** Replace with a banner using a reasonable share of the screen.

#### Mobile — 8% of Technical SEO

**TECH-050 · Viewport meta tag**  
`high` · weight 6 · scope: page · method: crawl · Industry practice: [Mobile-first indexing best practices](https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing)

- **Test:** <meta name='viewport' content='width=device-width, initial-scale=1'> present.
- **Fix:** Add the viewport tag to the base template.

**TECH-051 · Mobile/desktop content parity**  
`high` · weight 7 · scope: page · method: render · Google official: [Mobile-first indexing best practices](https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing)

- **Test:** Mobile render (Googlebot smartphone UA) contains the same main text, headings, structured data, images/alt and meta as desktop (>= 95% text match).
- **Fix:** Google indexes the mobile version. Do not hide content, links or schema on mobile breakpoints.

**TECH-052 · Structured data and meta on mobile**  
`medium` · weight 4 · scope: page · method: render · Google official: [Mobile-first indexing best practices](https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing)

- **Test:** Mobile HTML contains the same structured data, title, meta description, robots meta and alt text as desktop.
- **Fix:** Output the same head and markup on the mobile version.

**TECH-053 · Mobile usability (lab)**  
`low` · weight 3 · scope: page · method: api:psi · Industry practice: [Mobile-first indexing best practices](https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing)

- **Test:** Lighthouse mobile: legible font sizes, tap targets sized, no horizontal scroll.
- **Fix:** Fix the elements Lighthouse lists.

#### Security — 9% of Technical SEO

**TECH-060 · HTTPS on all pages**  
`high` · weight 8 · scope: site · method: crawl · Google official: [Understanding page experience](https://developers.google.com/search/docs/appearance/page-experience)

- **Test:** All pages served over HTTPS with a valid certificate. Google lists secure serving as one aspect of page experience, which is one of many signals, not a requirement for indexing.
- **Fix:** Install/renew the certificate and 301 all http URLs to https.

**TECH-061 · No mixed content**  
`medium` · weight 4 · scope: page · method: crawl · Google official: [Understanding page experience](https://developers.google.com/search/docs/appearance/page-experience)

- **Test:** No http:// subresources on https pages.
- **Fix:** Update the listed asset URLs to https.

**TECH-062 · HSTS header**  
`low` · weight 2 · scope: site · method: crawl · Industry practice: [Strict-Transport-Security (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security)

- **Test:** Strict-Transport-Security header with max-age >= 31536000.
- **Fix:** Enable HSTS at the CDN after confirming every subdomain serves HTTPS.

**TECH-063 · Not flagged by Safe Browsing**  
`critical` · weight 8 · scope: site · method: api:safebrowsing · Google official: [Google Safe Browsing](https://developers.google.com/safe-browsing)

- **Test:** Domain and sampled URLs not listed as malware, phishing or unwanted software.
- **Fix:** Clean the infection, then request a review in Search Console > Security issues.

**TECH-064 · No hacked spam content**  
`critical` · weight 6 · scope: page · method: crawl · Google official: [Spam policies for Google web search](https://developers.google.com/search/docs/essentials/spam-policies)

- **Test:** No injected spam (pharma/casino/Japanese keyword hack), hidden links or cloaked text detected, including pages only shown to Googlebot UA.
- **Fix:** Remove the injected content, patch the CMS/plugins, and rotate credentials.

#### International & multilingual — 10% of Technical SEO

**TECH-070 · hreflang present on multilingual pages**  
`high` · weight 7 · scope: page · method: crawl · Google official: [Tell Google about localized versions of your page](https://developers.google.com/search/docs/specialty/international/localized-versions)

- **Test:** Every page that has a counterpart in another configured language declares hreflang for all versions (HTML, header or sitemap).
- **Fix:** Add hreflang annotations listing every language version, including the page itself.

**TECH-071 · hreflang return links (reciprocity)**  
`high` · weight 7 · scope: project · method: crawl · Google official: [Tell Google about localized versions of your page](https://developers.google.com/search/docs/specialty/international/localized-versions)

- **Test:** If A references B, B references A. Missing return link = fail for the pair.
- **Fix:** Add the missing return annotation on the listed counterpart; Google ignores non-reciprocal hreflang.

**TECH-072 · hreflang codes valid**  
`medium` · weight 5 · scope: page · method: crawl · Google official: [Tell Google about localized versions of your page](https://developers.google.com/search/docs/specialty/international/localized-versions)

- **Test:** Language in ISO 639-1, optional script in ISO 15924, optional region in ISO 3166-1 alpha-2 (e.g. ar, ar-SA, zh-Hant). Flags common errors such as en-UK.
- **Fix:** Replace the invalid codes listed in the report.

**TECH-073 · hreflang targets are canonical and live**  
`medium` · weight 5 · scope: page · method: crawl · Industry practice: [Tell Google about localized versions of your page](https://developers.google.com/search/docs/specialty/international/localized-versions)

- **Test:** Every hreflang URL returns 200, is indexable and is its own canonical.
- **Fix:** Point hreflang only at the canonical URL of each version.

**TECH-074 · x-default declared**  
`low` · weight 1 · scope: page · method: crawl · Google official: [Tell Google about localized versions of your page](https://developers.google.com/search/docs/specialty/international/localized-versions)

- **Test:** An x-default annotation exists. Google documents x-default as optional (recommended) for unmatched languages.
- **Fix:** Add hreflang='x-default' pointing to the default (or language-selector) version.

**TECH-075 · Every page has its counterpart in each language**  
`medium` · weight 5 · scope: project · method: crawl · Industry practice: [Tell Google about localized versions of your page](https://developers.google.com/search/docs/specialty/international/localized-versions)

- **Test:** For each configured language pair, every page has a translated version (matched via hreflang, then slug).
- **Fix:** Publish the missing translation or remove the link to the non-existent version from the language switcher.

**TECH-076 · Slug consistency across languages**  
`low` · weight 2 · scope: project · method: crawl · Industry practice: [URL structure best practices](https://developers.google.com/search/docs/crawling-indexing/url-structure)

- **Test:** Paired pages share the same slug after the language prefix, or the difference is intentional and declared via hreflang.
- **Fix:** Align the slug (with a 301 from the old one) or confirm the pair through hreflang.

**TECH-077 · Content language matches declared language**  
`medium` · weight 4 · scope: page · method: crawl · Google official: [Managing multi-regional and multilingual sites](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites)

- **Test:** Detected language of main content (title, H1, body) matches the language of its URL group. Mixed-language titles/H1s on /ar/ pages are flagged.
- **Fix:** Translate untranslated elements (titles, H1, navigation, CTAs). Google detects language from visible content, so untranslated templates weaken the version.

**TECH-078 · html lang and dir attributes**  
`low` · weight 2 · scope: page · method: crawl · Industry practice: [W3C: Declaring language in HTML](https://www.w3.org/International/questions/qa-html-language-declarations)

- **Test:** <html lang> matches the version; RTL languages carry dir='rtl'.
- **Fix:** Set lang and dir per locale in the template. Google does not use lang for ranking, but Bing, screen readers and AI parsers do.

**TECH-079 · Language switcher is crawlable**  
`low` · weight 3 · scope: page · method: crawl · Google official: [Managing multi-regional and multilingual sites](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites)

- **Test:** Language switcher links are <a href> to the equivalent page (not the homepage, not JS-only); no automatic redirect by IP/Accept-Language.
- **Fix:** Link each page to its exact counterpart; never force-redirect users or Googlebot by locale.

**TECH-079B · Untranslated duplicate content across languages**  
`medium` · weight 4 · scope: project · method: crawl · Google official: [Managing multi-regional and multilingual sites](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites)

- **Test:** Pages in the /ar/ group whose title/H1/body are still in English (or vice versa) beyond 30% of text.
- **Fix:** Translate the page; untranslated versions are treated as duplicates.

#### URL structure — 4% of Technical SEO

**TECH-080 · Readable URLs (hyphens, no session IDs)**  
`low` · weight 4 · scope: page · method: crawl · Google official: [URL structure best practices](https://developers.google.com/search/docs/crawling-indexing/url-structure)

- **Test:** Path uses hyphens rather than underscores to separate words, and no session IDs in the URL. Google states no URL length limit, so length is not checked.
- **Fix:** Use short, descriptive hyphenated slugs; 301 old URLs when changing them.

**TECH-081 · Lowercase URLs**  
`low` · weight 2 · scope: page · method: crawl · Industry practice: [URL structure best practices](https://developers.google.com/search/docs/crawling-indexing/url-structure)

- **Test:** No uppercase characters in internal URL paths.
- **Fix:** Lower-case the slugs and 301 the old variants.

#### Server & delivery — 5% of Technical SEO

**TECH-090 · Text compression**  
`low` · weight 3 · scope: page · method: crawl · Industry practice: [Understanding page experience](https://developers.google.com/search/docs/appearance/page-experience)

- **Test:** HTML/CSS/JS served with Brotli or gzip.
- **Fix:** Enable compression at the CDN/origin.

**TECH-091 · Caching headers on static assets**  
`low` · weight 3 · scope: page · method: crawl · Industry practice: [Understanding page experience](https://developers.google.com/search/docs/appearance/page-experience)

- **Test:** Static assets have Cache-Control max-age >= 30 days (fingerprinted).
- **Fix:** Set long cache lifetimes with versioned file names.

**TECH-092 · HTML size within Googlebot limit**  
`high` · weight 3 · scope: page · method: crawl · Google official: [What is Googlebot](https://developers.google.com/search/docs/crawling-indexing/googlebot)

- **Test:** Each HTML file is under 2 MB. Google's Googlebot documentation states a 2 MB fetch limit for HTML; content beyond it is not considered. Over 1 MB = warn, over 2 MB = fail.
- **Fix:** Reduce the HTML size: move inline scripts, styles and data out of the document so the main content sits within the first 2 MB.

**TECH-093 · HTTP/2 or HTTP/3**  
`low` · weight 1 · scope: site · method: crawl · Industry practice: [Managing crawl budget for large sites](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget)

- **Test:** Server negotiates h2 or h3.
- **Fix:** Enable HTTP/2+ at the CDN.

**TECH-094 · Availability during crawl**  
`high` · weight 5 · scope: site · method: crawl · Google official: [How HTTP status codes affect Google's crawlers](https://developers.google.com/crawling/docs/troubleshooting/http-status-codes)

- **Test:** Error/timeout rate < 1% across the crawl; DNS resolves consistently.
- **Fix:** Investigate hosting capacity or rate limiting toward crawlers.

#### Measurement & verification — 5% of Technical SEO

**TECH-100 · Search Console connected**  
`high` · weight 6 · scope: site · method: api:gsc · Google official: [Search Console Help](https://support.google.com/webmasters)

- **Test:** Property verified and accessible to the tool (enables index coverage, manual actions, CWV, queries). N/A if not connected.
- **Fix:** Verify the domain property and grant read access to unlock the Search Console checks.

**TECH-101 · No manual actions**  
`critical` · weight 10 · scope: site · method: api:gsc · Google official: [Manual actions report](https://support.google.com/webmasters/answer/9044175)

- **Test:** Search Console manual actions report is empty.
- **Fix:** Fix the stated violation and file a reconsideration request.

**TECH-102 · Indexed vs submitted pages**  
`high` · weight 6 · scope: site · method: api:gsc · Google official: [Search Console Help](https://support.google.com/webmasters)

- **Test:** Share of sitemap URLs indexed >= 90% pass, 70-89% warn, < 70% fail; top 'not indexed' reasons reported.
- **Fix:** Work through the not-indexed reasons listed (crawled-not-indexed usually signals content quality).

**TECH-103 · Analytics installed**  
`low` · weight 2 · scope: site · method: crawl · Industry practice: [Search Console Help](https://support.google.com/webmasters)

- **Test:** GA4 (or equivalent) tag present on all templates.
- **Fix:** Add the tag to the base template to measure organic and AI referral traffic.

**TECH-104 · Bing Webmaster Tools verified**  
`low` · weight 2 · scope: site · method: crawl · Platform official: [Bing Webmaster Guidelines](https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a)

- **Test:** msvalidate.01 meta / BingSiteAuth.xml / DNS verification detected.
- **Fix:** Verify in Bing Webmaster Tools (feeds Copilot and ChatGPT search signals).

**TECH-105 · IndexNow supported**  
`low` · weight 1 · scope: site · method: crawl · Platform official: [IndexNow](https://www.indexnow.org)

- **Test:** IndexNow key file found at the declared location.
- **Fix:** Enable IndexNow (CMS plugin or CDN) to notify Bing/Yandex of changes instantly.

### On-page SEO — 45% of SEO

#### Meta & SERP appearance — 18% of On-page SEO

**META-001 · Title tag present**  
`critical` · weight 10 · scope: page · method: crawl · Google official: [Influencing title links](https://developers.google.com/search/docs/appearance/title-link)

- **Test:** Exactly one non-empty <title>.
- **Fix:** Write a unique, descriptive title for each listed page.

**META-002 · Title unique across the site**  
`high` · weight 7 · scope: page · method: crawl · Google official: [Influencing title links](https://developers.google.com/search/docs/appearance/title-link)

- **Test:** No two indexable pages in the same language share a title.
- **Fix:** Differentiate titles by the page's specific topic; groups of duplicates are listed.

**META-003 · Title length**  
`low` · weight 3 · scope: page · method: crawl · Industry practice: [Influencing title links](https://developers.google.com/search/docs/appearance/title-link)

- **Test:** Rendered width <= 580 px (approx. 50-60 Latin / 45-60 Arabic characters). Google sets no limit but truncates in SERPs; < 15 characters = warn.
- **Fix:** Front-load the primary topic and keep the brand suffix short.

**META-004 · Title is descriptive, not boilerplate**  
`medium` · weight 5 · scope: page · method: ai · Google official: [Influencing title links](https://developers.google.com/search/docs/appearance/title-link)

- **Test:** Title describes the page's topic, is not a slug/placeholder (e.g. 'about-us', 'email-marketing'), not keyword-stuffed, and is spelled correctly.
- **Fix:** Rewrite the listed titles; the report proposes a title per page based on its H1 and content.

**META-005 · Consistent brand suffix**  
`low` · weight 2 · scope: language · method: crawl · Google official: [Influencing title links](https://developers.google.com/search/docs/appearance/title-link)

- **Test:** Brand appears once, in the same form, in titles of each page group (e.g. '| WideBot Blog'). Variants and misspellings are flagged.
- **Fix:** Normalise the suffix in the CMS template.

**META-006 · Title aligns with H1**  
`low` · weight 3 · scope: page · method: crawl · Industry practice: [Influencing title links](https://developers.google.com/search/docs/appearance/title-link)

- **Test:** Title and H1 share the core topic (token overlap >= 50% after stop-word removal).
- **Fix:** Google may rewrite titles that do not match the visible heading; align them.

**META-010 · Meta description present**  
`low` · weight 3 · scope: page · method: crawl · Google official: [Control your snippets in search results](https://developers.google.com/search/docs/appearance/snippet)

- **Test:** Non-empty meta description. Google recommends page-specific descriptions and, at minimum, descriptions for the home page and popular pages; it does not require one on every page.
- **Fix:** Write a page-specific description summarising the page's value.

**META-011 · Meta description unique**  
`medium` · weight 4 · scope: page · method: crawl · Google official: [Control your snippets in search results](https://developers.google.com/search/docs/appearance/snippet)

- **Test:** No duplicate descriptions among indexable pages in the same language.
- **Fix:** Rewrite duplicates so each reflects its page.

**META-012 · Meta description length**  
`low` · weight 2 · scope: page · method: crawl · Industry practice: [Control your snippets in search results](https://developers.google.com/search/docs/appearance/snippet)

- **Test:** 70-160 characters (approx. 920 px).
- **Fix:** Keep the key message in the first 120 characters.

**META-020 · Open Graph tags**  
`low` · weight 3 · scope: page · method: crawl · Industry practice: [The Open Graph protocol](https://ogp.me)

- **Test:** og:title, og:description, og:image (>= 1200x630), og:url present; og:url equals canonical.
- **Fix:** Add the missing OG tags in the template; og:image should be page-specific where possible.

**META-021 · Twitter/X card**  
`low` · weight 1 · scope: page · method: crawl · Industry practice: [X Cards markup](https://developer.x.com/en/docs/x-for-websites/cards/overview/markup)

- **Test:** twitter:card present (summary_large_image recommended).
- **Fix:** Add twitter:card; X falls back to OG for the remaining fields.

**META-030 · Favicon eligible for Search**  
`low` · weight 2 · scope: site · method: crawl · Google official: [Define a favicon to show in search results](https://developers.google.com/search/docs/appearance/favicon-in-search)

- **Test:** A favicon link (rel icon, apple-touch-icon or apple-touch-icon-precomposed) in the head of the home page; the icon must be square and at least 8x8 px (Google recommends larger than 48x48 px), and both the home page and the icon file must be crawlable.
- **Fix:** Provide a 48x48 (or 96/144) square favicon referenced from the homepage head.

**META-031 · Site name declared**  
`low` · weight 2 · scope: site · method: crawl · Google official: [Provide a site name to Google Search](https://developers.google.com/search/docs/appearance/site-names)

- **Test:** WebSite structured data with name and url (optionally alternateName) on the home page. This states a preference; Google may also use og:site_name, the title and headings.
- **Fix:** Add WebSite JSON-LD with the brand name in each language version's homepage.

**META-007 · Titles differ between language versions**  
`medium` · weight 4 · scope: project · method: crawl · Google official: [Influencing title links](https://developers.google.com/search/docs/appearance/title-link)

- **Test:** Paired AR/EN pages do not share an identical (untranslated) title.
- **Fix:** Translate the title of the listed pages.

**META-013 · Description matches page language**  
`low` · weight 2 · scope: page · method: crawl · Google official: [Control your snippets in search results](https://developers.google.com/search/docs/appearance/snippet)

- **Test:** Meta description written in the page's language.
- **Fix:** Translate the description.

#### Headings — 5% of On-page SEO

**HEAD-001 · H1 present**  
`high` · weight 7 · scope: page · method: crawl · Industry practice: [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)

- **Test:** At least one non-empty H1 in the main content.
- **Fix:** Add a visible H1 stating the page topic.

**HEAD-002 · Single H1**  
`low` · weight 2 · scope: page · method: crawl · Industry practice: [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)

- **Test:** Exactly one H1 (multiple H1s are allowed by Google; flagged as warn for clarity).
- **Fix:** Keep one H1 for the main topic and demote the others to H2.

**HEAD-003 · Logical heading hierarchy**  
`low` · weight 3 · scope: page · method: crawl · Industry practice: [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)

- **Test:** No skipped levels (H2 -> H4) and no empty headings.
- **Fix:** Restructure headings so they outline the content.

**HEAD-004 · Headings not used for styling**  
`low` · weight 2 · scope: page · method: crawl · Industry practice: [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)

- **Test:** No heading tags in header/footer/nav templates except the logo-less site title.
- **Fix:** Replace decorative headings in templates with styled paragraphs/spans.

#### Content quality — 25% of On-page SEO

**CONT-001 · Sufficient main content**  
`medium` · weight 5 · scope: page · method: crawl · Industry practice: [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

- **Test:** Main-content word count by page type: blog >= 800, solution/product >= 500, other >= 250. Google sets no minimum; thresholds flag likely thin pages.
- **Fix:** Expand the listed pages with information users need to decide (use cases, specifics, examples) rather than filler.

**CONT-002 · People-first helpfulness**  
`high` · weight 8 · scope: page · method: ai · Google official: [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

- **Test:** AI scores the page against Google's self-assessment questions (original information, complete description of the topic, insight beyond the obvious, satisfies the need). Score >= 70 pass, 50-69 warn, < 50 fail.
- **Fix:** Report lists which questions the page fails and the specific gaps.

**CONT-003 · Clear topic focus**  
`medium` · weight 5 · scope: page · method: ai · Google official: [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)

- **Test:** Primary topic identifiable from title, H1 and first 100 words; one dominant search intent.
- **Fix:** State the topic early and remove sections that serve a different intent (move them to their own page).

**CONT-004 · Keyword repetition**  
`medium` · weight 5 · scope: page · method: crawl · Industry practice: [Spam policies for Google web search](https://developers.google.com/search/docs/essentials/spam-policies)

- **Test:** No single non-stop-word term above 5% of the main content. Reported as a warning to review, since density alone does not prove stuffing.
- **Fix:** Review the listed pages and rewrite unnaturally repeated phrases; use natural synonyms and remove keyword lists.

**CONT-005 · No scaled low-value content**  
`high` · weight 6 · scope: language · method: ai · Google official: [Spam policies for Google web search](https://developers.google.com/search/docs/essentials/spam-policies)

- **Test:** Detects groups of templated pages with near-identical text and little unique value (e.g. city/industry pages differing only by a name).
- **Fix:** Add unique, substantive content per page or consolidate them.

**CONT-006 · Spelling and grammar**  
`medium` · weight 3 · scope: page · method: ai · Google official: [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

- **Test:** No spelling errors in title, meta description, H1-H3; body error rate < 1 per 300 words.
- **Fix:** Correct the listed errors (quoted in context).

**CONT-007 · Content freshness**  
`low` · weight 3 · scope: page · method: crawl · Industry practice: [Influence the byline date in Google Search](https://developers.google.com/search/docs/appearance/publication-dates)

- **Test:** Time-sensitive pages (titles containing a year, 'latest', statistics) updated within 12 months; no stale year in titles.
- **Fix:** Refresh the facts and update dateModified only when the content materially changes.

**CONT-008 · Outbound citations to authoritative sources**  
`low` · weight 3 · scope: page · method: crawl · Industry practice: [Search Quality Rater Guidelines](https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf)

- **Test:** Pages making factual/statistical claims link at least one authoritative external source.
- **Fix:** Cite the primary source for each statistic or regulation mentioned.

**CONT-009 · No broken outbound links**  
`low` · weight 2 · scope: page · method: crawl · Industry practice: [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

- **Test:** External links return 2xx/3xx.
- **Fix:** Replace or remove the dead external links listed.

**CONT-010 · No keyword cannibalisation**  
`medium` · weight 5 · scope: language · method: crawl · Industry practice: [How to specify a canonical URL](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)

- **Test:** No two indexable pages in the same language target the same primary topic (title/H1 similarity > 80%, or same top query when GSC connected).
- **Fix:** Merge, re-target or differentiate the conflicting pages; pairs listed.

**CONT-011 · Primary topic in URL, title, H1 and intro**  
`low` · weight 3 · scope: page · method: crawl · Google official: [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)

- **Test:** The page's main term appears in title, H1 and first 100 words.
- **Fix:** Align the four elements on one topic.

**CONT-012 · Hidden or deceptive content**  
`high` · weight 5 · scope: page · method: render · Google official: [Spam policies for Google web search](https://developers.google.com/search/docs/essentials/spam-policies)

- **Test:** No text hidden via CSS (same color as background, off-screen, font-size 0) to manipulate ranking. Tabs/accordions are fine.
- **Fix:** Remove the hidden text.

**CONT-013 · AI-generated content level (informational)**  
`info` · weight 0 · scope: page · method: ai · Google official: [Google Search's guidance about AI-generated content](https://developers.google.com/search/blog/2023/02/google-search-and-ai-content)

- **Test:** Estimated share of machine-generated text reported. Google does not penalise AI content per se; only low-value scaled content (CONT-005).
- **Fix:** Review high-AI pages for originality and expert input.

**CONT-014 · Ads and CTAs do not dominate**  
`low` · weight 2 · scope: page · method: render · Google official: [Search Quality Rater Guidelines](https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf)

- **Test:** Main content visible above the fold; ads/promotional blocks < 30% of viewport at load.
- **Fix:** Reduce or move the blocks pushing main content down.

#### Blog & articles — 14% of On-page SEO

**BLOG-001 · Visible author byline**  
`high` · weight 6 · scope: page · method: crawl · applies to: blog · Google official: [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

- **Test:** Article shows an author name linked to an author page.
- **Fix:** Add a byline linking to the author's profile page.

**BLOG-002 · Author pages with credentials**  
`medium` · weight 5 · scope: site · method: ai · applies to: blog · Google official: [Search Quality Rater Guidelines](https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf)

- **Test:** Each author page states role, expertise and experience, with links to external profiles.
- **Fix:** Create/complete author pages; add Person schema with sameAs (LinkedIn etc.).

**BLOG-003 · Visible publish and update dates**  
`medium` · weight 4 · scope: page · method: crawl · applies to: blog · Google official: [Influence the byline date in Google Search](https://developers.google.com/search/docs/appearance/publication-dates)

- **Test:** A visible date near the title, consistent with datePublished/dateModified in schema.
- **Fix:** Display 'Published' and 'Updated' dates and keep them consistent with the structured data.

**BLOG-004 · Article/BlogPosting schema complete**  
`low` · weight 5 · scope: page · method: crawl · applies to: blog · Google official: [Article structured data](https://developers.google.com/search/docs/appearance/structured-data/article)

- **Test:** Article/BlogPosting markup with the properties Google recommends: headline, image, datePublished, dateModified, author (name and url). Google lists no required properties.
- **Fix:** Complete the missing properties listed per post.

**BLOG-005 · Contextual links to commercial pages**  
`medium` · weight 4 · scope: page · method: crawl · applies to: blog · Industry practice: [Link best practices for Google](https://developers.google.com/search/docs/crawling-indexing/links-crawlable)

- **Test:** Each post links to >= 1 relevant product/solution page with a descriptive anchor.
- **Fix:** Add contextual links from the post body to the matching product/solution pages (suggestions listed).

**BLOG-006 · Related posts / topic clustering**  
`low` · weight 3 · scope: page · method: crawl · applies to: blog · Industry practice: [Link best practices for Google](https://developers.google.com/search/docs/crawling-indexing/links-crawlable)

- **Test:** Post links to >= 2 other posts on the same topic.
- **Fix:** Add a related-posts module and in-text links within the cluster.

**BLOG-007 · Table of contents on long articles**  
`low` · weight 2 · scope: page · method: crawl · applies to: blog · Industry practice: [Control your snippets in search results](https://developers.google.com/search/docs/appearance/snippet)

- **Test:** Articles > 1,500 words have jump links to H2 sections.
- **Fix:** Add a TOC with anchor links; Google can show these as 'jump to' links.

**BLOG-008 · Blog index crawlable**  
`medium` · weight 4 · scope: site · method: crawl · applies to: blog · Google official: [Pagination, incremental page loading and Google](https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading)

- **Test:** Every post is reachable through paginated <a href> links (not only 'load more' JS).
- **Fix:** Provide crawlable pagination URLs (?page=2) alongside any infinite scroll.

**BLOG-009 · RSS/Atom feed**  
`low` · weight 1 · scope: site · method: crawl · applies to: blog · Google official: [Build and submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)

- **Test:** Feed linked with <link rel='alternate' type='application/rss+xml'>.
- **Fix:** Expose a feed; Google accepts RSS/Atom as a sitemap source for fresh URLs.

**BLOG-010 · Category structure**  
`low` · weight 2 · scope: site · method: crawl · Industry practice: [Link best practices for Google](https://developers.google.com/search/docs/crawling-indexing/links-crawlable)

- **Test:** Posts assigned to topical categories with indexable, content-rich category pages.
- **Fix:** Create topic hubs that summarise and link the cluster.

**BLOG-011 · Featured image and alt per post**  
`low` · weight 2 · scope: page · method: crawl · Google official: [Google image SEO best practices](https://developers.google.com/search/docs/appearance/google-images)

- **Test:** Each post has a primary image (>= 1200 px wide) referenced in Article image and og:image.
- **Fix:** Add a large, relevant featured image.

#### Images & media — 9% of On-page SEO

**IMG-001 · Descriptive alt text**  
`medium` · weight 6 · scope: page · method: crawl · Google official: [Google image SEO best practices](https://developers.google.com/search/docs/appearance/google-images)

- **Test:** Content images have non-empty alt that is not a filename. Decorative images may use alt=''.
- **Fix:** Write alt text describing each listed image in context.

**IMG-002 · Descriptive file names**  
`low` · weight 2 · scope: page · method: crawl · Google official: [Google image SEO best practices](https://developers.google.com/search/docs/appearance/google-images)

- **Test:** File names are words, not IMG_1234 / random hashes.
- **Fix:** Rename on upload to short descriptive names.

**IMG-003 · Modern formats and sizing**  
`medium` · weight 4 · scope: page · method: api:psi · Industry practice: [Core Web Vitals and Google Search](https://developers.google.com/search/docs/appearance/core-web-vitals)

- **Test:** Images served as WebP/AVIF, not > 2x their rendered size, < 200 KB for content images.
- **Fix:** Convert and resize the listed images; use srcset for responsive sizes.

**IMG-004 · Explicit dimensions**  
`low` · weight 3 · scope: page · method: crawl · Industry practice: [Core Web Vitals and Google Search](https://developers.google.com/search/docs/appearance/core-web-vitals)

- **Test:** <img> has width/height attributes or CSS aspect-ratio.
- **Fix:** Add dimensions to prevent layout shift (CLS).

**IMG-005 · Images crawlable**  
`medium` · weight 4 · scope: page · method: render · Google official: [Google image SEO best practices](https://developers.google.com/search/docs/appearance/google-images)

- **Test:** Important images use <img src> (not CSS backgrounds) and are not blocked by robots.txt.
- **Fix:** Move content images from CSS backgrounds to <img> elements.

**IMG-006 · Video discoverability**  
`low` · weight 2 · scope: page · method: crawl · Google official: [Video SEO best practices](https://developers.google.com/search/docs/appearance/video)

- **Test:** Pages with embedded video provide VideoObject schema (name, thumbnailUrl, uploadDate).
- **Fix:** Add VideoObject structured data for each embedded video.

**IMG-007 · Linked images have alt**  
`medium` · weight 3 · scope: page · method: crawl · Google official: [Link best practices for Google](https://developers.google.com/search/docs/crawling-indexing/links-crawlable)

- **Test:** Images used as links have alt describing the destination (it is their anchor text).
- **Fix:** Write alt describing the target page.

#### Internal linking — 9% of On-page SEO

**LINK-001 · Descriptive anchor text**  
`medium` · weight 5 · scope: page · method: crawl · Google official: [Link best practices for Google](https://developers.google.com/search/docs/crawling-indexing/links-crawlable)

- **Test:** No in-content internal links with generic anchors ('click here', 'read more', 'اضغط هنا', 'اقرأ المزيد') or empty anchors.
- **Fix:** Rewrite anchors to describe the target page.

**LINK-002 · Adequate inbound internal links**  
`medium` · weight 5 · scope: page · method: crawl · Industry practice: [Link best practices for Google](https://developers.google.com/search/docs/crawling-indexing/links-crawlable)

- **Test:** Important pages receive >= 3 internal links from distinct pages.
- **Fix:** Add links from related pages; suggestions listed by topical similarity.

**LINK-003 · No nofollow on internal links**  
`low` · weight 3 · scope: page · method: crawl · Industry practice: [Qualify your outbound links](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links)

- **Test:** Internal links do not carry rel=nofollow.
- **Fix:** Remove nofollow from internal links.

**LINK-004 · Outbound link qualification**  
`low` · weight 2 · scope: page · method: crawl · Google official: [Qualify your outbound links](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links)

- **Test:** Paid/affiliate links carry rel='sponsored'; user-generated links rel='ugc'.
- **Fix:** Add the correct rel attribute.

**LINK-005 · Breadcrumb navigation visible**  
`low` · weight 2 · scope: page · method: crawl · Google official: [Breadcrumb structured data](https://developers.google.com/search/docs/appearance/structured-data/breadcrumb)

- **Test:** Non-home pages show a visible breadcrumb trail.
- **Fix:** Add a breadcrumb component reflecting the hierarchy.

#### Structured data — 15% of On-page SEO

**SD-001 · Structured data is valid**  
`high` · weight 7 · scope: page · method: crawl · Google official: [General structured data guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)

- **Test:** All JSON-LD parses; no missing required properties for the declared Google-supported types.
- **Fix:** Fix the parse/validation errors listed (property and path).

**SD-002 · Structured data matches visible content**  
`high` · weight 6 · scope: page · method: ai · Google official: [General structured data guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)

- **Test:** Marked-up facts (names, ratings, FAQs, prices, dates) appear in the visible page.
- **Fix:** Remove markup describing content users cannot see; this violates Google's structured-data policies.

**SD-003 · Organization on homepage**  
`low` · weight 3 · scope: site · method: crawl · Google official: [Organization structured data](https://developers.google.com/search/docs/appearance/structured-data/organization)

- **Test:** Organization markup on the home page (or the about page). Google lists no required properties; name, url and logo are recommended, and the logo must be at least 112x112 px.
- **Fix:** Complete the Organization JSON-LD (see GEO-020 for entity-level detail).

**SD-004 · BreadcrumbList**  
`low` · weight 3 · scope: page · method: crawl · Industry practice: [Breadcrumb structured data](https://developers.google.com/search/docs/appearance/structured-data/breadcrumb)

- **Test:** Non-home pages carry BreadcrumbList matching the visible breadcrumb trail.
- **Fix:** Add BreadcrumbList generated from the site hierarchy.

**SD-005 · Page-type schema present**  
`medium` · weight 4 · scope: page · method: crawl · Industry practice: [Introduction to structured data](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)

- **Test:** Blog -> Article/BlogPosting; product -> SoftwareApplication/Product; contact -> Organization contactPoint; video -> VideoObject.
- **Fix:** Add the type mapped to each page group.

**SD-006 · Deprecated or non-rendering types**  
`info` · weight 0 · scope: page · method: crawl · Google official: [Search documentation updates: removing FAQ rich result](https://developers.google.com/search/updates#removing-faq-rich-result)

- **Test:** Reports pages using FAQPage or HowTo markup. Google's documentation updates state FAQ rich results are no longer shown as of 7 May 2026.
- **Fix:** No removal needed. Do not count on these for SERP enhancements; keep only if the content is genuinely Q&A.

**SD-007 · Logo meets requirements**  
`low` · weight 2 · scope: site · method: crawl · Google official: [Organization structured data](https://developers.google.com/search/docs/appearance/structured-data/organization)

- **Test:** Organization logo >= 112x112 px, crawlable, on a plain background.
- **Fix:** Provide a compliant logo URL.

**SD-008 · No self-serving reviews**  
`high` · weight 4 · scope: page · method: crawl · Google official: [Review snippet structured data (self-serving reviews)](https://developers.google.com/search/docs/appearance/structured-data/review-snippet)

- **Test:** No Review/AggregateRating markup on the business's own Organization/LocalBusiness.
- **Fix:** Remove the rating markup; it is ineligible and may trigger a manual action.

**SD-009 · No conflicting duplicate entities**  
`low` · weight 3 · scope: page · method: crawl · Google official: [General structured data guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)

- **Test:** One Organization entity per page (shared @id), no conflicting values between JSON-LD blocks/microdata.
- **Fix:** Merge into one JSON-LD graph with stable @id values.

**SD-010 · JobPosting on careers**  
`low` · weight 2 · scope: page · method: crawl · applies to: careers · Google official: [Job posting structured data](https://developers.google.com/search/docs/appearance/structured-data/job-posting)

- **Test:** Open roles marked up with JobPosting (title, datePosted, validThrough, hiringOrganization, jobLocation).
- **Fix:** Add JobPosting per vacancy; remove it when filled.

**SD-011 · Software/product markup**  
`low` · weight 3 · scope: page · method: crawl · applies to: products · Google official: [Software app structured data](https://developers.google.com/search/docs/appearance/structured-data/software-app)

- **Test:** Product pages use SoftwareApplication (name, applicationCategory, operatingSystem) or Product.
- **Fix:** Add the type with accurate properties; omit offers/price if pricing is not public.

#### Accessibility & UX — 5% of On-page SEO

**UX-001 · Accessibility basics**  
`low` · weight 4 · scope: page · method: api:psi · Industry practice: [W3C: Declaring language in HTML](https://www.w3.org/International/questions/qa-html-language-declarations)

- **Test:** Lighthouse accessibility >= 90 pass, 70-89 warn; flags missing labels, contrast, lang.
- **Fix:** Fix the listed accessibility failures; they overlap with how parsers read the page.

**UX-002 · Clear primary CTA**  
`low` · weight 3 · scope: page · method: ai · Industry practice: [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

- **Test:** Commercial pages show one clear next step (book demo/contact) above the fold.
- **Fix:** Add or clarify the primary CTA.

**UX-003 · Custom 404 helps users**  
`low` · weight 2 · scope: site · method: crawl · Google official: [How HTTP status codes affect Google's crawlers](https://developers.google.com/crawling/docs/troubleshooting/http-status-codes)

- **Test:** 404 page offers navigation/search back into the site.
- **Fix:** Add links to main sections and search on the 404 template.

### Off-page SEO — 15% of SEO

#### Authority & backlinks — 100% of Off-page SEO

> Free data sources are partial. Scores here are directional; connect Ahrefs/Semrush/Search Console Links for full data.

**OFF-001 · Domain authority proxy**  
`medium` · weight 5 · scope: site · method: api:openpagerank · Industry practice: [Open PageRank](https://www.domcop.com/openpagerank/)

- **Test:** Open PageRank score benchmarked against up to 5 competitor domains entered in the project.
- **Fix:** Gap vs competitors is reported; prioritise earning links from the referring domains competitors share (OFF-004).

**OFF-002 · Referring domains**  
`medium` · weight 5 · scope: site · method: api:commoncrawl · Industry practice: [Common Crawl web graphs](https://commoncrawl.org/web-graphs)

- **Test:** Count of unique linking domains from the latest Common Crawl host graph, vs competitors.
- **Fix:** Digital PR, partner/customer pages, industry associations and original research are the main levers.

**OFF-003 · Backlinks to broken pages**  
`high` · weight 6 · scope: site · method: api:commoncrawl · Google official: [Redirects and Google Search](https://developers.google.com/search/docs/crawling-indexing/301-redirects)

- **Test:** External links pointing to URLs on the domain that now return 4xx.
- **Fix:** 301 each listed URL to its closest live equivalent to recover the link equity.

**OFF-004 · Link gap vs competitors**  
`low` · weight 3 · scope: site · method: api:commoncrawl · Industry practice: [Common Crawl web graphs](https://commoncrawl.org/web-graphs)

- **Test:** Domains linking to >= 2 competitors but not to the project.
- **Fix:** Outreach list generated from the gap.

**OFF-005 · Unnatural link patterns**  
`high` · weight 5 · scope: site · method: api:commoncrawl · Google official: [Spam policies for Google web search](https://developers.google.com/search/docs/essentials/spam-policies)

- **Test:** Flags sitewide footer links from unrelated sites, exact-match commercial anchors > 20% of anchors, links from known link networks.
- **Fix:** Stop the paid/exchanged link practice; qualify sponsored links with rel='sponsored'.

**OFF-006 · Unlinked brand mentions**  
`low` · weight 2 · scope: site · method: ai · Industry practice: [Search Quality Rater Guidelines](https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf)

- **Test:** Web pages mentioning the brand without linking (from search results / news).
- **Fix:** Ask the publishers to add a link to the relevant page.

**OFF-007 · Anchor text diversity**  
`medium` · weight 3 · scope: site · method: api:commoncrawl · Google official: [Spam policies for Google web search](https://developers.google.com/search/docs/essentials/spam-policies)

- **Test:** Branded + URL anchors >= 50% of external anchors.
- **Fix:** Diversify; stop acquiring exact-match commercial anchors.

**OFF-008 · Links from topically relevant sites**  
`medium` · weight 3 · scope: site · method: api:commoncrawl · Industry practice: [Search Quality Rater Guidelines](https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf)

- **Test:** Share of referring domains in related industries/regions.
- **Fix:** Target industry media, partners and regional tech publications.

**OFF-009 · Social profiles linked and active**  
`low` · weight 2 · scope: site · method: crawl · Industry practice: [Organization structured data](https://developers.google.com/search/docs/appearance/structured-data/organization)

- **Test:** Official social profiles linked from the site; last post < 90 days (where public).
- **Fix:** Link active profiles from the footer and sameAs.

**OFF-010 · Brand SERP / knowledge panel (manual)**  
`low` · weight 2 · scope: site · method: manual · Google official: [About knowledge panels](https://support.google.com/knowledgepanel/answer/9163198)

- **Test:** Branded search shows the official site first and a knowledge panel.
- **Fix:** Claim the knowledge panel; strengthen entity signals (GEO-020/021).


---

## GEO (Generative Engine Optimization)

> Google states there are no additional requirements for appearing in AI Overviews / AI Mode beyond normal SEO eligibility (indexed, snippet-eligible). Checks marked `industry` reflect observed behaviour of AI search systems and are labelled as such in the report.

### AI crawler access — 20% of GEO (Generative Engine Optimization)

#### Bot access — 100% of AI crawler access

**GEO-001 · Eligible for Google AI features**  
`critical` · weight 10 · scope: page · method: crawl · Google official: [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)

- **Test:** Page indexable and snippet-eligible: no nosnippet, max-snippet:0, or data-nosnippet over main content.
- **Fix:** Remove the snippet restriction from the listed pages; AI Overviews only use content eligible for a snippet.

**GEO-002 · OAI-SearchBot allowed (ChatGPT search)**  
`high` · weight 8 · scope: site · method: crawl · Platform official: [Overview of OpenAI crawlers](https://platform.openai.com/docs/bots)

- **Test:** robots.txt does not disallow OAI-SearchBot for public pages.
- **Fix:** Allow OAI-SearchBot; blocking it removes the site from ChatGPT search answers and citations.

**GEO-003 · ChatGPT-User allowed**  
`medium` · weight 5 · scope: site · method: crawl · Platform official: [Overview of OpenAI crawlers](https://platform.openai.com/docs/bots)

- **Test:** ChatGPT-User not disallowed (user-initiated fetches).
- **Fix:** Allow ChatGPT-User so pages shared or requested inside ChatGPT can be read.

**GEO-004 · PerplexityBot allowed**  
`high` · weight 6 · scope: site · method: crawl · Platform official: [Perplexity crawlers](https://docs.perplexity.ai/guides/bots)

- **Test:** PerplexityBot not disallowed.
- **Fix:** Allow PerplexityBot to be indexed and cited by Perplexity.

**GEO-005 · Claude crawlers allowed**  
`medium` · weight 5 · scope: site · method: crawl · Platform official: [Anthropic crawlers](https://support.claude.com/en/articles/8896518)

- **Test:** Claude-SearchBot and Claude-User not disallowed. ClaudeBot (training) reported separately as a policy choice.
- **Fix:** Allow Claude-SearchBot/Claude-User for search visibility; decide on ClaudeBot by training policy.

**GEO-006 · Bingbot allowed**  
`high` · weight 6 · scope: site · method: crawl · Platform official: [Bing Webmaster Guidelines](https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a)

- **Test:** Bingbot not disallowed; site returns 200 to Bingbot UA.
- **Fix:** Allow Bingbot; Bing's index feeds Copilot and is used by several AI assistants.

**GEO-007 · Training crawlers policy (informational)**  
`info` · weight 0 · scope: site · method: crawl · Google official: [Google's common crawlers (incl. Google-Extended)](https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers)

- **Test:** Reports the status of GPTBot, Google-Extended, CCBot, ClaudeBot, Applebot-Extended. Note: Google-Extended does not affect Search or AI Overviews.
- **Fix:** Policy decision for the business; the report explains the effect of each.

**GEO-008 · WAF/CDN does not block AI user agents**  
`high` · weight 7 · scope: site · method: crawl · Industry practice: [Overview of OpenAI crawlers](https://platform.openai.com/docs/bots)

- **Test:** Homepage and one key page fetched with each AI search UA return 200 (not 403/429/challenge page).
- **Fix:** Whitelist the verified bot IP ranges in the CDN/bot-protection settings (Cloudflare 'AI bots' setting often blocks them by default).

**GEO-009 · Other AI assistants allowed**  
`low` · weight 3 · scope: site · method: crawl · Platform official: [Applebot documentation](https://support.apple.com/en-us/119829)

- **Test:** Applebot (Siri/Spotlight), Meta-ExternalFetcher, DuckAssistBot, MistralAI-User, Amazonbot not disallowed (training variants reported separately).
- **Fix:** Allow the search/user-fetch agents you want visibility in.

**GEO-010 · Bot access consistent across language versions**  
`medium` · weight 3 · scope: project · method: crawl · Industry practice: [Introduction to robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/intro)

- **Test:** /ar/ and /en paths receive identical AI-bot rules (no locale path accidentally disallowed).
- **Fix:** Align the robots rules for every language prefix.

### Machine readability — 10% of GEO (Generative Engine Optimization)

#### Server HTML — 100% of Machine readability

**GEO-011 · Content readable without JavaScript**  
`high` · weight 8 · scope: page · method: render · Industry practice: [JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics)

- **Test:** Raw HTML (no JS) contains the main content, headings and key facts (>= 80% of rendered text).
- **Fix:** Most AI crawlers do not execute JavaScript. Server-render the content shown in the report as JS-only.

**GEO-012 · Semantic HTML structure**  
`low` · weight 3 · scope: page · method: crawl · Industry practice: [W3C: Declaring language in HTML](https://www.w3.org/International/questions/qa-html-language-declarations)

- **Test:** Main content inside <main>/<article>; lists as <ul>/<ol>; tables as <table> with header cells.
- **Fix:** Use semantic elements so parsers can segment passages reliably.

**GEO-013 · llms.txt (informational)**  
`info` · weight 0 · scope: site · method: crawl · Industry practice: [llms.txt proposal](https://llmstxt.org)

- **Test:** Reports presence and validity of /llms.txt. Not scored: no major AI search system has confirmed using it.
- **Fix:** Optional. Low effort; no expected ranking or citation effect.

**GEO-014 · Video and audio have transcripts**  
`low` · weight 3 · scope: page · method: crawl · Industry practice: [Video SEO best practices](https://developers.google.com/search/docs/appearance/video)

- **Test:** Pages with video/podcast provide a text transcript or detailed summary.
- **Fix:** Publish transcripts; AI systems read text, not media.

**GEO-015 · Key facts not locked in images/PDF only**  
`medium` · weight 4 · scope: page · method: ai · Industry practice: [Google image SEO best practices](https://developers.google.com/search/docs/appearance/google-images)

- **Test:** Statistics, pricing tiers, comparisons available as HTML text, not only inside images or PDFs.
- **Fix:** Reproduce the facts as HTML text/tables.

### Brand entity — 15% of GEO (Generative Engine Optimization)

#### Entity clarity — 100% of Brand entity

**GEO-020 · Complete Organization entity**  
`medium` · weight 7 · scope: site · method: crawl · Google official: [Organization structured data](https://developers.google.com/search/docs/appearance/structured-data/organization)

- **Test:** Organization JSON-LD carries the properties Google recommends: name, alternateName, url, logo, description, foundingDate, address, contactPoint, sameAs. None is required by Google.
- **Fix:** Complete the missing properties; use the same @id across both language versions.

**GEO-021 · sameAs to authoritative profiles**  
`medium` · weight 5 · scope: site · method: crawl · Industry practice: [Organization structured data](https://developers.google.com/search/docs/appearance/structured-data/organization)

- **Test:** sameAs includes LinkedIn plus at least two of: Wikidata, Crunchbase, X, YouTube, GitHub, official registries.
- **Fix:** Add the missing profiles; create a Wikidata item if the brand qualifies for notability.

**GEO-022 · Consistent brand naming**  
`medium` · weight 4 · scope: project · method: crawl · Industry practice: [Provide a site name to Google Search](https://developers.google.com/search/docs/appearance/site-names)

- **Test:** Brand name spelled identically in titles, schema, footer and About across pages and per language (e.g. 'WideBot' / 'وايدبوت'); variants flagged.
- **Fix:** Normalise every listed variant to the official spelling.

**GEO-023 · Fact-rich About page**  
`medium` · weight 5 · scope: site · method: ai · Google official: [Search Quality Rater Guidelines](https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf)

- **Test:** About page states what the company does, founding year, HQ, leadership, scale (customers, markets) in plain declarative sentences.
- **Fix:** Add the missing facts as explicit statements AI systems can quote.

**GEO-024 · Leadership with Person entities**  
`low` · weight 3 · scope: site · method: crawl · Industry practice: [Search Quality Rater Guidelines](https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf)

- **Test:** Leadership page lists people with role, and Person schema with sameAs (LinkedIn).
- **Fix:** Add Person markup linked to the Organization via worksFor/founder.

**GEO-025 · One clear page per product/entity**  
`medium` · weight 4 · scope: language · method: crawl · Industry practice: [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

- **Test:** Each product/service has exactly one canonical page that defines it.
- **Fix:** Consolidate overlapping product pages.

**GEO-026 · Facts consistent across the web**  
`medium` · weight 4 · scope: site · method: ai · Industry practice: [Search Quality Rater Guidelines](https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf)

- **Test:** Founding year, HQ, leadership, offering match between site, LinkedIn, Crunchbase, Wikidata and press.
- **Fix:** Correct outdated facts on the listed external profiles.

### E-E-A-T & trust — 15% of GEO (Generative Engine Optimization)

#### Trust signals — 100% of E-E-A-T & trust

**GEO-030 · Contact transparency**  
`high` · weight 6 · scope: site · method: crawl · Industry practice: [Search Quality Rater Guidelines](https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf)

- **Test:** Contact page with email/phone/address, linked sitewide.
- **Fix:** Add complete contact details and link the page from the footer.

**GEO-031 · Evidence of experience**  
`medium` · weight 6 · scope: language · method: ai · Google official: [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

- **Test:** Case studies/success stories with named clients and measurable outcomes.
- **Fix:** Publish case studies with concrete numbers (before/after, timeframe, client).

**GEO-032 · Third-party validation**  
`medium` · weight 4 · scope: site · method: ai · Google official: [Search Quality Rater Guidelines](https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf)

- **Test:** Certifications, awards, partner badges, press coverage linked to their source.
- **Fix:** Display each credential with a link to the issuing body or article.

**GEO-033 · Editorial and policy pages**  
`low` · weight 3 · scope: site · method: crawl · Industry practice: [Search Quality Rater Guidelines](https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf)

- **Test:** Privacy policy, terms and (for content sites) editorial/AI-use policy reachable.
- **Fix:** Publish and link the missing policies.

**GEO-034 · Author expertise on informational content**  
`medium` · weight 5 · scope: language · method: ai · Google official: [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

- **Test:** Informational articles attributed to identifiable people with relevant expertise (aggregates BLOG-001/002).
- **Fix:** Attribute articles to subject-matter experts and show their credentials.

### Citability — 15% of GEO (Generative Engine Optimization)

#### Passage quality — 100% of Citability

**GEO-040 · Answer-first introductions**  
`high` · weight 7 · scope: page · method: ai · Industry practice: [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)

- **Test:** The first 2-3 sentences answer the page's core question or state its value proposition directly.
- **Fix:** Rewrite the opening of each listed page to lead with the answer; the report shows a proposed opening.

**GEO-041 · Self-contained passages**  
`medium` · weight 6 · scope: page · method: ai · Industry practice: [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)

- **Test:** Sections under each H2 can be understood without surrounding context (no 'as mentioned above', explicit subject names).
- **Fix:** Restate the subject in each section and avoid dangling references.

**GEO-042 · Factual density**  
`medium` · weight 6 · scope: page · method: ai · Industry practice: [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

- **Test:** Concrete, verifiable facts (numbers, dates, named entities) per 100 words vs page-type baseline.
- **Fix:** Replace generic claims with specific figures and named examples.

**GEO-043 · Original information**  
`medium` · weight 5 · scope: page · method: ai · Google official: [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

- **Test:** Page contains first-party data, expert quotes or a distinct point of view not found in competing pages.
- **Fix:** Add proprietary data, customer results or expert commentary.

**GEO-044 · Sourced claims**  
`low` · weight 3 · scope: page · method: ai · Industry practice: [Search Quality Rater Guidelines](https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf)

- **Test:** Statistics and regulatory claims carry a cited source.
- **Fix:** Link each statistic to its primary source.

**GEO-045 · Topic coverage (query fan-out)**  
`medium` · weight 5 · scope: page · method: ai · Industry practice: [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)

- **Test:** AI generates the sub-questions a user would ask about the page topic and checks which are answered.
- **Fix:** Add sections for the unanswered sub-questions listed (or link to pages that answer them).

**GEO-046 · Statistics and data tables**  
`low` · weight 3 · scope: page · method: crawl · Industry practice: [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

- **Test:** Pages with quantitative claims present data in tables/lists with units and dates.
- **Fix:** Structure figures as tables with source and date.

**GEO-047 · Comparison and alternatives content**  
`medium` · weight 4 · scope: language · method: ai · Industry practice: [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

- **Test:** Site covers 'X vs Y', 'best tools for…', 'alternatives to…' queries relevant to its category, fairly and factually.
- **Fix:** Publish honest comparison pages for the top competitor queries.

**GEO-048 · Key takeaways / summary block**  
`low` · weight 3 · scope: page · method: crawl · Industry practice: [Control your snippets in search results](https://developers.google.com/search/docs/appearance/snippet)

- **Test:** Long pages (> 1,200 words) start or end with a short summary/TL;DR.
- **Fix:** Add a 3-5 point summary.

**GEO-049 · Visible last-updated date on informational pages**  
`low` · weight 3 · scope: page · method: crawl · Google official: [Influence the byline date in Google Search](https://developers.google.com/search/docs/appearance/publication-dates)

- **Test:** Informational pages display an updated date.
- **Fix:** Show 'Updated on' and keep it truthful.

### AI answer visibility — 15% of GEO (Generative Engine Optimization)

#### Mentions & citations — 100% of AI answer visibility

**GEO-050 · Brand mentioned in AI answers**  
`high` · weight 8 · scope: language · method: ai · Industry practice: [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)

- **Test:** Share of project prompts where the brand is named in the answer (per engine, per language).
- **Fix:** Prompts where the brand is absent are listed with the competitors named instead.

**GEO-051 · Site cited as a source**  
`high` · weight 8 · scope: language · method: ai · Industry practice: [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)

- **Test:** Share of prompts where a project URL is among cited sources.
- **Fix:** For each missed prompt, the cited pages are listed: compare and close the content gap.

**GEO-052 · AI share of voice vs competitors**  
`medium` · weight 6 · scope: language · method: ai · Industry practice: [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)

- **Test:** Brand mentions / all tracked-brand mentions across prompts.
- **Fix:** Prioritise topics where competitors dominate.

**GEO-053 · Answer accuracy about the brand**  
`medium` · weight 5 · scope: language · method: ai · Industry practice: [Search Quality Rater Guidelines](https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf)

- **Test:** AI descriptions of the brand match the facts on the About page (no wrong product, outdated positioning).
- **Fix:** Correct the source pages AI cites for the wrong facts; strengthen GEO-023/026.

**GEO-054 · AI referral traffic**  
`low` · weight 2 · scope: site · method: api:gsc · Industry practice: [Search Console Help](https://support.google.com/webmasters)

- **Test:** Sessions from chatgpt.com, perplexity.ai, gemini.google.com, copilot.microsoft.com tracked (GA4) and trending.
- **Fix:** Create an 'AI referrals' channel group in GA4.

### Off-site presence — 10% of GEO (Generative Engine Optimization)

#### Platforms AI engines cite — 100% of Off-site presence

**GEO-060 · Wikipedia / Wikidata**  
`medium` · weight 5 · scope: site · method: api:commoncrawl · Industry practice: [Wikidata](https://www.wikidata.org)

- **Test:** Wikidata item exists (and Wikipedia article where notable) with correct facts.
- **Fix:** Create/curate the Wikidata item with references; do not self-write Wikipedia.

**GEO-061 · Review & directory platforms**  
`medium` · weight 5 · scope: site · method: manual · Industry practice: [Search Quality Rater Guidelines](https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf)

- **Test:** Profiles on category-relevant platforms (e.g. G2, Capterra, Clutch, Gartner Peer Insights) with recent reviews.
- **Fix:** Claim profiles and run a review programme.

**GEO-062 · Community discussions**  
`low` · weight 3 · scope: site · method: ai · Industry practice: [Search Quality Rater Guidelines](https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf)

- **Test:** Brand discussed on Reddit, Quora, LinkedIn posts, Stack Overflow for the category.
- **Fix:** Participate transparently; publish expert answers from named staff.

**GEO-063 · YouTube presence**  
`low` · weight 3 · scope: site · method: manual · Industry practice: [Video SEO best practices](https://developers.google.com/search/docs/appearance/video)

- **Test:** Official channel with titled, described, transcribed videos on core topics.
- **Fix:** Publish explainer/demo videos with full descriptions and chapters.

**GEO-064 · Press and analyst coverage**  
`medium` · weight 4 · scope: site · method: ai · Industry practice: [Search Quality Rater Guidelines](https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf)

- **Test:** Recent (12 months) coverage in industry/regional media.
- **Fix:** Digital PR around launches, data and partnerships.


---

## AEO (Answer Engine Optimization)

### Answer formats — 50% of AEO (Answer Engine Optimization)

#### Snippet-ready content — 100% of Answer formats

**AEO-001 · Question-phrased headings**  
`medium` · weight 5 · scope: page · method: crawl · applies to: blog, solutions, products · Industry practice: [Control your snippets in search results](https://developers.google.com/search/docs/appearance/snippet)

- **Test:** At least 2 H2/H3 phrased as natural questions (what/how/why/... / ما/كيف/لماذا/هل...).
- **Fix:** Rephrase section headings that correspond to real user questions.

**AEO-002 · Direct answer under question headings**  
`high` · weight 7 · scope: page · method: crawl · Industry practice: [Control your snippets in search results](https://developers.google.com/search/docs/appearance/snippet)

- **Test:** Paragraph of 40-60 words immediately after each question heading that answers it without preamble.
- **Fix:** Insert a concise answer paragraph right below each listed heading, then elaborate.

**AEO-003 · Definition statement**  
`medium` · weight 5 · scope: page · method: ai · applies to: blog, glossary · Industry practice: [Control your snippets in search results](https://developers.google.com/search/docs/appearance/snippet)

- **Test:** Definitional pages contain an 'X is ...' sentence in the first paragraph.
- **Fix:** Open with a one-sentence definition.

**AEO-004 · Steps as ordered lists**  
`low` · weight 3 · scope: page · method: crawl · Industry practice: [Control your snippets in search results](https://developers.google.com/search/docs/appearance/snippet)

- **Test:** Procedural content (how-to, setup, steps) uses <ol>.
- **Fix:** Convert step sequences written as paragraphs into ordered lists.

**AEO-005 · Comparisons as tables**  
`low` · weight 3 · scope: page · method: crawl · Industry practice: [Control your snippets in search results](https://developers.google.com/search/docs/appearance/snippet)

- **Test:** Comparison content (vs, types, pricing tiers) uses HTML <table>.
- **Fix:** Present comparisons in a real HTML table.

**AEO-006 · FAQ section on commercial pages**  
`medium` · weight 4 · scope: page · method: crawl · applies to: solutions, products · Industry practice: [Search documentation updates: removing FAQ rich result](https://developers.google.com/search/updates#removing-faq-rich-result)

- **Test:** Visible FAQ block answering pre-sales questions. Scored as content; FAQPage markup itself earns no Google rich result.
- **Fix:** Add a FAQ section covering objections and decision questions.

**AEO-007 · Snippet controls not restrictive**  
`high` · weight 6 · scope: page · method: crawl · Google official: [Robots meta tag, data-nosnippet and X-Robots-Tag](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag)

- **Test:** No max-snippet < 50, nosnippet or data-nosnippet on answer content.
- **Fix:** Relax the snippet directive on the listed pages.

**AEO-008 · Jump links to sections**  
`low` · weight 2 · scope: page · method: crawl · Google official: [Control your snippets in search results](https://developers.google.com/search/docs/appearance/snippet)

- **Test:** Long pages have id anchors on H2s linked from a TOC.
- **Fix:** Add anchor ids and a TOC.

**AEO-009 · Video key moments**  
`low` · weight 2 · scope: page · method: crawl · Google official: [Video SEO best practices](https://developers.google.com/search/docs/appearance/video)

- **Test:** Videos expose chapters (Clip or SeekToAction in VideoObject, or YouTube chapters).
- **Fix:** Add chapters/Clip markup.

**AEO-013 · Glossary/definition pages**  
`medium` · weight 4 · scope: language · method: crawl · Industry practice: [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

- **Test:** Category terms have dedicated definition pages (e.g. encyclopedia) linked from related content.
- **Fix:** Create one definition page per core term and link it contextually.

**AEO-014 · Question in title for informational pages**  
`low` · weight 2 · scope: page · method: crawl · applies to: blog · Industry practice: [Influencing title links](https://developers.google.com/search/docs/appearance/title-link)

- **Test:** Informational posts targeting a question use it in the title/H1.
- **Fix:** Use the natural question as the H1 where it matches intent.

### Question coverage — 30% of AEO (Answer Engine Optimization)

#### Question coverage — 100% of Question coverage

**AEO-010 · Long-tail question coverage**  
`medium` · weight 6 · scope: language · method: ai · Industry practice: [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

- **Test:** For each main topic, the share of common who/what/how/why questions answered somewhere on the site.
- **Fix:** Unanswered questions listed with the best page to host each answer.

**AEO-011 · Conversational phrasing**  
`low` · weight 3 · scope: page · method: ai · Industry practice: [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

- **Test:** Answers phrased in natural language that reads well aloud (voice assistants).
- **Fix:** Rewrite jargon-heavy answer paragraphs in plain sentences.

**AEO-012 · QAPage for genuine Q&A**  
`info` · weight 0 · scope: page · method: crawl · Google official: [Q&A structured data](https://developers.google.com/search/docs/appearance/structured-data/qapage)

- **Test:** Reports community/forum Q&A pages lacking QAPage markup.
- **Fix:** Use QAPage only where users submit questions and answers.

### SERP answer features — 20% of AEO (Answer Engine Optimization)

#### Feature ownership — 100% of SERP answer features

**AEO-020 · Featured snippets owned**  
`medium` · weight 5 · scope: language · method: api:serp · Google official: [Featured snippets and your website](https://developers.google.com/search/docs/appearance/featured-snippets)

- **Test:** Queries where the site holds the featured snippet vs queries where it ranks top 5 with a snippet present.
- **Fix:** For each lost snippet, match the format (paragraph/list/table) of the current holder with a better answer.

**AEO-021 · People Also Ask coverage**  
`medium` · weight 5 · scope: language · method: api:serp · Industry practice: [Control your snippets in search results](https://developers.google.com/search/docs/appearance/snippet)

- **Test:** Share of PAA questions on target queries answered on the site.
- **Fix:** Add answers for the unanswered PAA questions listed.

**AEO-022 · AI Overview presence**  
`medium` · weight 5 · scope: language · method: api:serp · Google official: [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)

- **Test:** Target queries showing an AI Overview, and whether the site is cited in it.
- **Fix:** Strengthen the pages for queries where competitors are cited.

**AEO-023 · Queries phrased as questions (GSC)**  
`low` · weight 3 · scope: language · method: api:gsc · Industry practice: [Search Console Help](https://support.google.com/webmasters)

- **Test:** Question-form queries bringing impressions but CTR < 2% identified.
- **Fix:** Add direct answers for these queries on the ranking page.


---

## Local SEO

> Applies when: Project marks the business as having physical locations or serving specific cities/countries. Otherwise N/A.

### Google Business Profile — 35% of Local SEO

#### Profile — 100% of Google Business Profile

> Reviewed manually against the live Google Business Profile; gaps go into the client plan per domain and industry.

**LOC-001 · Profile found for each location**  
`critical` · weight 10 · scope: site · method: manual · Google official: [Guidelines for representing your business on Google](https://support.google.com/business/answer/3038177)

- **Test:** A Places result matches each configured location (name + address).
- **Fix:** Create or claim the profile and verify it in Google Business Profile.

**LOC-002 · Business name compliant**  
`high` · weight 6 · scope: site · method: manual · Google official: [Guidelines for representing your business on Google](https://support.google.com/business/answer/3038177)

- **Test:** Profile name equals the real-world brand name; no added keywords or locations.
- **Fix:** Remove the added descriptors; keyword-stuffed names risk suspension.

**LOC-003 · Relevant primary category**  
`high` · weight 6 · scope: site · method: manual · Google official: [Tips to improve your local ranking on Google](https://support.google.com/business/answer/7091)

- **Test:** Primary type matches the core business (e.g. Software company).
- **Fix:** Change the primary category to the most specific accurate one.

**LOC-004 · Website link points to the right page**  
`medium` · weight 4 · scope: site · method: manual · Industry practice: [Guidelines for representing your business on Google](https://support.google.com/business/answer/3038177)

- **Test:** Profile website URL returns 200 and targets the localized page/language for that location.
- **Fix:** Update the website field (e.g. Riyadh profile -> Arabic site or Saudi location page).

**LOC-005 · Phone and hours set**  
`medium` · weight 4 · scope: site · method: manual · Google official: [Tips to improve your local ranking on Google](https://support.google.com/business/answer/7091)

- **Test:** Phone number and regular opening hours present.
- **Fix:** Complete the missing fields in the profile.

**LOC-006 · Reviews volume and rating**  
`medium` · weight 5 · scope: site · method: manual · Google official: [Tips to improve your local ranking on Google](https://support.google.com/business/answer/7091)

- **Test:** Rating and review count benchmarked against competitors entered in the project; most recent review < 90 days.
- **Fix:** Set up a review-request flow after onboarding/implementation milestones.

**LOC-007 · Photos**  
`low` · weight 2 · scope: site · method: manual · Industry practice: [Guidelines for representing your business on Google](https://support.google.com/business/answer/3038177)

- **Test:** >= 10 photos including logo, office exterior/interior and team.
- **Fix:** Upload current, real photos.

**LOC-008 · Business description**  
`low` · weight 2 · scope: site · method: manual · Google official: [Guidelines for representing your business on Google](https://support.google.com/business/answer/3038177)

- **Test:** Description filled (up to 750 chars), accurate, no links/promos.
- **Fix:** Write a factual description.

**LOC-009 · Services/products listed**  
`low` · weight 2 · scope: site · method: manual · Google official: [Guidelines for representing your business on Google](https://support.google.com/business/answer/3038177)

- **Test:** Services or products section populated.
- **Fix:** Add the core services.

**LOC-009B · Recent posts/updates**  
`low` · weight 2 · scope: site · method: manual · Industry practice: [Tips to improve your local ranking on Google](https://support.google.com/business/answer/7091)

- **Test:** At least one profile update in the last 30 days.
- **Fix:** Post launches, events or news monthly.

**LOC-009C · Owner responses to reviews**  
`medium` · weight 3 · scope: site · method: manual · Google official: [Tips to improve your local ranking on Google](https://support.google.com/business/answer/7091)

- **Test:** Owner replied to >= 80% of reviews from the last 12 months.
- **Fix:** Reply to every review, especially negative ones.

**LOC-009D · Name in both languages where relevant**  
`low` · weight 2 · scope: site · method: manual · Industry practice: [Guidelines for representing your business on Google](https://support.google.com/business/answer/3038177)

- **Test:** For Arabic-market locations, the profile shows the brand consistently in Arabic and English (as used on signage/registration).
- **Fix:** Align the profile name with the official registered/branded form.

### NAP consistency — 25% of Local SEO

#### Name, Address, Phone — 100% of NAP consistency

**LOC-010 · NAP visible on the site**  
`high` · weight 6 · scope: site · method: crawl · Industry practice: [Tips to improve your local ranking on Google](https://support.google.com/business/answer/7091)

- **Test:** Name, address and phone present as text (not image) in footer or contact page.
- **Fix:** Add the NAP block as HTML text.

**LOC-011 · NAP matches the profile**  
`high` · weight 7 · scope: site · method: manual · Industry practice: [Tips to improve your local ranking on Google](https://support.google.com/business/answer/7091)

- **Test:** Site NAP equals the Places data after normalisation (phone in E.164, address tokens).
- **Fix:** Align the listed fields on the site or the profile.

**LOC-012 · NAP consistent across languages**  
`medium` · weight 4 · scope: project · method: crawl · Industry practice: [Tips to improve your local ranking on Google](https://support.google.com/business/answer/7091)

- **Test:** Same phone/address (transliterated) on every language version.
- **Fix:** Use one source for NAP in all templates.

**LOC-013 · Click-to-call**  
`low` · weight 2 · scope: site · method: crawl · Industry practice: [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)

- **Test:** Phone wrapped in tel: link.
- **Fix:** Wrap phone numbers in <a href='tel:+...'>.

### Local structured data — 15% of Local SEO

#### LocalBusiness markup — 100% of Local structured data

**LOC-020 · LocalBusiness/Organization address markup**  
`medium` · weight 6 · scope: site · method: crawl · Google official: [Local business structured data](https://developers.google.com/search/docs/appearance/structured-data/local-business)

- **Test:** LocalBusiness markup with the properties Google requires (name, address); recommended: telephone, url, geo, openingHoursSpecification.
- **Fix:** Add LocalBusiness (or Organization with location) per office.

**LOC-021 · Geo coordinates and hours**  
`low` · weight 3 · scope: site · method: crawl · Google official: [Local business structured data](https://developers.google.com/search/docs/appearance/structured-data/local-business)

- **Test:** geo (latitude/longitude) and openingHoursSpecification present.
- **Fix:** Add coordinates and opening hours consistent with the profile.

### Location pages — 15% of Local SEO

#### Location content — 100% of Location pages

**LOC-030 · Dedicated location pages**  
`medium` · weight 5 · scope: site · method: crawl · Industry practice: [Tips to improve your local ranking on Google](https://support.google.com/business/answer/7091)

- **Test:** Each served city/country has a page with unique content (local clients, team, address, map).
- **Fix:** Create one substantive page per location; avoid templated doorway pages (see CONT-005).

**LOC-031 · Embedded map**  
`low` · weight 1 · scope: site · method: crawl · Industry practice: [Tips to improve your local ranking on Google](https://support.google.com/business/answer/7091)

- **Test:** Contact/location page embeds a map of the address.
- **Fix:** Embed the Google Maps location of the office.

### Citations & other maps — 10% of Local SEO

#### Listings — 100% of Citations & other maps

**LOC-040 · Apple Business Connect / Bing Places**  
`low` · weight 3 · scope: site · method: manual · Platform official: [Bing Places for Business](https://www.bingplaces.com)

- **Test:** Location listed on Apple Maps and Bing Places with the same NAP.
- **Fix:** Claim both listings.

**LOC-041 · Local directories consistency**  
`low` · weight 3 · scope: site · method: manual · Industry practice: [Tips to improve your local ranking on Google](https://support.google.com/business/answer/7091)

- **Test:** Top regional directories/chambers list the business with identical NAP.
- **Fix:** Correct inconsistent listings.

**LOC-042 · Local backlinks**  
`low` · weight 2 · scope: site · method: api:commoncrawl · Industry practice: [Tips to improve your local ranking on Google](https://support.google.com/business/answer/7091)

- **Test:** Links from local media, associations, universities in each served city.
- **Fix:** Pursue local partnerships and sponsorships.


---

## Site-type modules

> Each module runs only when the project site type matches (auto-detected, editable). Active modules are averaged; if none is active the pillar is N/A.

### E-commerce — 100% of Site-type modules

#### E-commerce checks — 100% of E-commerce

> Active only when site type = e-commerce

**ECOM-001 · Product structured data**  
`high` · weight 8 · scope: page · method: crawl · Google official: [Product structured data](https://developers.google.com/search/docs/appearance/structured-data/product)

- **Test:** Product pages carry Product with name, image, and offers (price, priceCurrency, availability).
- **Fix:** Add complete Product JSON-LD generated from the catalogue data.

**ECOM-002 · Merchant listing details**  
`medium` · weight 5 · scope: page · method: crawl · Google official: [Merchant listing structured data](https://developers.google.com/search/docs/appearance/structured-data/merchant-listing)

- **Test:** Offers include shippingDetails and hasMerchantReturnPolicy (or these are declared at Organization level).
- **Fix:** Add shipping and return policy markup, or configure them in Merchant Center.

**ECOM-003 · Markup price and stock match the page**  
`high` · weight 7 · scope: page · method: ai · Google official: [General structured data guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)

- **Test:** Price, currency and availability in JSON-LD equal the visible values.
- **Fix:** Generate markup from the same source as the visible price; mismatches cause disapprovals.

**ECOM-004 · Product reviews markup is genuine**  
`medium` · weight 4 · scope: page · method: crawl · Google official: [Review snippet structured data (self-serving reviews)](https://developers.google.com/search/docs/appearance/structured-data/review-snippet)

- **Test:** AggregateRating/Review only where reviews are visible on the page and collected from customers.
- **Fix:** Remove rating markup with no visible reviews.

**ECOM-005 · Out-of-stock and discontinued handling**  
`high` · weight 6 · scope: page · method: crawl · Google official: [Best practices for ecommerce in Search](https://developers.google.com/search/docs/specialty/ecommerce)

- **Test:** Temporarily unavailable products return 200 with OutOfStock; discontinued ones return 404/410 or 301 to a direct successor, not the homepage.
- **Fix:** Apply the rule per product state; mass redirects to the homepage are treated as soft 404.

**ECOM-006 · Faceted navigation controlled**  
`high` · weight 7 · scope: site · method: crawl · Google official: [Managing crawling of faceted navigation URLs](https://developers.google.com/search/docs/crawling-indexing/crawling-managing-faceted-navigation)

- **Test:** Filter/sort URL combinations are not crawlable at scale (blocked in robots.txt or use URL fragments) and are canonicalised.
- **Fix:** Block low-value facet parameters and keep only facets with search demand as indexable pages.

**ECOM-007 · Category pages have unique content**  
`medium` · weight 5 · scope: page · method: crawl · Industry practice: [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

- **Test:** Category pages are indexable, have a unique H1, intro text and are not near-duplicates of each other.
- **Fix:** Write a short unique intro and buying guidance per category.

**ECOM-008 · Product variants handled**  
`medium` · weight 5 · scope: page · method: crawl · Google official: [Product variant structured data](https://developers.google.com/search/docs/appearance/structured-data/product-variants)

- **Test:** Variants (size, colour) use ProductGroup or one canonical URL; no duplicate indexable page per variant without unique demand.
- **Fix:** Canonicalise variants to the main product or mark them up with ProductGroup.

**ECOM-009 · Unique product descriptions**  
`medium` · weight 5 · scope: page · method: ai · Google official: [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

- **Test:** Descriptions are not copied manufacturer text shared with other retailers (duplicate detection across the site and sampled web results).
- **Fix:** Rewrite descriptions for top-revenue products first.

**ECOM-010 · Category pagination crawlable**  
`medium` · weight 4 · scope: site · method: crawl · Google official: [Pagination, incremental page loading and Google](https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading)

- **Test:** Paginated category pages are reachable through <a href> links and self-canonical.
- **Fix:** Add crawlable pagination links; do not canonicalise page 2+ to page 1.

**ECOM-011 · Product images**  
`low` · weight 3 · scope: page · method: crawl · Google official: [Google image SEO best practices](https://developers.google.com/search/docs/appearance/google-images)

- **Test:** At least one high-resolution image (>= 800 px) per product with descriptive alt; multiple angles recommended.
- **Fix:** Upload larger images and write product-specific alt text.

**ECOM-012 · Merchant Center feed (manual)**  
`medium` · weight 4 · scope: site · method: manual · Google official: [Google Merchant Center Help](https://support.google.com/merchants)

- **Test:** Products submitted to Google Merchant Center with no account-level issues.
- **Fix:** Create the feed and fix disapprovals to appear in free listings.

**ECOM-013 · Internal search pages not indexable**  
`medium` · weight 4 · scope: site · method: crawl · Google official: [Managing crawl budget for large sites](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget)

- **Test:** Internal search result URLs are noindex or disallowed.
- **Fix:** Add noindex to search result templates.

**ECOM-014 · Product breadcrumbs**  
`low` · weight 3 · scope: page · method: crawl · Google official: [Breadcrumb structured data](https://developers.google.com/search/docs/appearance/structured-data/breadcrumb)

- **Test:** Product pages show a breadcrumb to their category, marked up with BreadcrumbList.
- **Fix:** Add category breadcrumbs to the product template.

**ECOM-015 · Shipping, returns and payment pages**  
`medium` · weight 4 · scope: site · method: crawl · Google official: [Search Quality Rater Guidelines](https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf)

- **Test:** Shipping, returns, payment and customer-service information is published and linked sitewide.
- **Fix:** Publish clear policy pages; they are trust requirements for shopping queries.

### News & publishers — 100% of Site-type modules

#### News & publishers checks — 100% of News & publishers

> Active only when site type = news/publisher

**NEWS-001 · NewsArticle structured data**  
`medium` · weight 5 · scope: page · method: crawl · Google official: [Article structured data](https://developers.google.com/search/docs/appearance/structured-data/article)

- **Test:** Articles carry NewsArticle/Article with headline, image, datePublished, dateModified, author.
- **Fix:** Complete the article markup in the CMS template.

**NEWS-002 · Large image previews allowed**  
`high` · weight 6 · scope: page · method: crawl · Google official: [Discover and your website](https://developers.google.com/search/docs/appearance/google-discover)

- **Test:** max-image-preview:large set (meta robots or header).
- **Fix:** Add max-image-preview:large to be eligible for large images in Discover.

**NEWS-003 · Lead images at least 1200 px wide**  
`medium` · weight 5 · scope: page · method: crawl · Google official: [Discover and your website](https://developers.google.com/search/docs/appearance/google-discover)

- **Test:** Each article has an image >= 1200 px wide; the site logo is not used as the article image.
- **Fix:** Supply a large, relevant lead image per article.

**NEWS-004 · News sitemap**  
`medium` · weight 5 · scope: site · method: crawl · Google official: [News sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/news-sitemap)

- **Test:** A news sitemap lists articles from the last 2 days with publication name, language and publication date.
- **Fix:** Generate a news sitemap that updates on publish.

**NEWS-005 · Bylines and dates on every article**  
`high` · weight 6 · scope: page · method: crawl · Google official: [Google News policies](https://support.google.com/news/publisher-center/answer/6204050)

- **Test:** Visible author byline and publication date/time on each article.
- **Fix:** Show byline and timestamps near the headline.

**NEWS-006 · Publisher transparency**  
`high` · weight 6 · scope: site · method: ai · Google official: [Google News policies](https://support.google.com/news/publisher-center/answer/6204050)

- **Test:** About, contact, editorial team and ownership/funding information published.
- **Fix:** Publish masthead, contact details and ownership information.

**NEWS-007 · Paywalled content markup**  
`medium` · weight 4 · scope: page · method: crawl · Google official: [Subscription and paywalled content](https://developers.google.com/search/docs/appearance/structured-data/paywalled-content)

- **Test:** Paywalled articles declare isAccessibleForFree=false with the paywalled section selector.
- **Fix:** Add the paywall markup so gated content is not treated as cloaking.

**NEWS-008 · Headlines match the content**  
`medium` · weight 5 · scope: page · method: ai · Google official: [Discover and your website](https://developers.google.com/search/docs/appearance/google-discover)

- **Test:** Titles are accurate, not exaggerated or withholding key information.
- **Fix:** Rewrite misleading headlines; Discover policies exclude clickbait.

**NEWS-009 · Permanent, unique article URLs**  
`low` · weight 3 · scope: page · method: crawl · Industry practice: [URL structure best practices](https://developers.google.com/search/docs/crawling-indexing/url-structure)

- **Test:** Each article has one stable URL that does not change after publication.
- **Fix:** Stop changing slugs after publish; redirect if unavoidable.

**NEWS-010 · Topic and section hubs**  
`low` · weight 3 · scope: site · method: crawl · Industry practice: [Link best practices for Google](https://developers.google.com/search/docs/crawling-indexing/links-crawlable)

- **Test:** Sections/topics have crawlable hub pages linking recent and evergreen coverage.
- **Fix:** Create topic hubs and link them from articles.

### SaaS & software — 100% of Site-type modules

#### SaaS & software checks — 100% of SaaS & software

> Active only when site type = SaaS/software

**SAAS-001 · Feature pages**  
`medium` · weight 5 · scope: language · method: crawl · Industry practice: [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

- **Test:** Each core feature has its own indexable page (not only a section of the homepage).
- **Fix:** Create one page per feature with use cases, screenshots and proof.

**SAAS-002 · Integration pages**  
`medium` · weight 5 · scope: language · method: crawl · Industry practice: [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

- **Test:** Each supported integration has a page describing what the connection does; no empty templated pages.
- **Fix:** Publish integration pages with real setup and use-case detail.

**SAAS-003 · Comparison pages**  
`medium` · weight 5 · scope: language · method: ai · Industry practice: [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

- **Test:** 'Brand vs competitor' pages exist for main competitors and are factual and current.
- **Fix:** Write fair comparison pages with verifiable feature and pricing facts.

**SAAS-004 · Alternatives pages**  
`medium` · weight 4 · scope: language · method: ai · Industry practice: [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

- **Test:** 'Alternatives to <competitor>' pages exist for competitors with search demand.
- **Fix:** Publish alternatives pages that include the honest trade-offs.

**SAAS-005 · Use-case and industry pages**  
`medium` · weight 5 · scope: language · method: crawl · Industry practice: [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

- **Test:** Dedicated pages per use case and per target industry, each with unique content.
- **Fix:** Build pages per segment; avoid swapping only the industry name.

**SAAS-006 · Pricing information (informational)**  
`info` · weight 0 · scope: site · method: crawl · Industry practice: [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

- **Test:** Reports whether a pricing page exists. Enterprise-only sales models may intentionally have none.
- **Fix:** Optional: publish how pricing works even without numbers.

**SAAS-007 · Programmatic pages pass a quality gate**  
`high` · weight 7 · scope: language · method: ai · Google official: [Spam policies for Google web search](https://developers.google.com/search/docs/essentials/spam-policies)

- **Test:** Template-generated page sets have unique data per page and are not near-duplicates (scaled content / doorway risk).
- **Fix:** Only generate pages where unique data exists; noindex or remove the rest.

**SAAS-008 · Free tools and linkable assets**  
`low` · weight 3 · scope: site · method: manual · Industry practice: [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

- **Test:** Site offers calculators, templates, free tools or original research that earn links.
- **Fix:** Build one tool or data asset aligned with the product.

**SAAS-009 · App, login and docs do not compete with marketing pages**  
`medium` · weight 4 · scope: site · method: crawl · Google official: [Robots meta tag, data-nosnippet and X-Robots-Tag](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag)

- **Test:** App/login/staging subdomains are noindex; help-centre articles do not outrank or duplicate product pages.
- **Fix:** Noindex app surfaces and differentiate docs from marketing content.

**SAAS-010 · Product updates are published**  
`low` · weight 2 · scope: site · method: crawl · Industry practice: [Influence the byline date in Google Search](https://developers.google.com/search/docs/appearance/publication-dates)

- **Test:** Changelog or release notes updated in the last 90 days.
- **Fix:** Publish release notes; they signal an active product.

### Services & lead generation — 100% of Site-type modules

#### Services & lead generation checks — 100% of Services & lead generation

> Active only when site type = services (e.g. logistics, agencies, clinics)

**SERV-001 · One page per service**  
`high` · weight 7 · scope: language · method: crawl · Industry practice: [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

- **Test:** Each service offered has a dedicated indexable page.
- **Fix:** Split combined service lists into individual service pages.

**SERV-002 · Service-area pages are unique**  
`high` · weight 6 · scope: language · method: ai · Google official: [Spam policies for Google web search](https://developers.google.com/search/docs/essentials/spam-policies)

- **Test:** City/area pages contain location-specific content, not the same text with the place name changed (doorway pages).
- **Fix:** Add local proof (projects, coverage, team, pricing) or consolidate the pages.

**SERV-003 · Service structured data**  
`low` · weight 3 · scope: page · method: crawl · Industry practice: [Local business structured data](https://developers.google.com/search/docs/appearance/structured-data/local-business)

- **Test:** Service pages reference the business entity (LocalBusiness subtype or Service with provider and areaServed).
- **Fix:** Add Service markup linked to the organisation.

**SERV-004 · Licences and credentials shown**  
`medium` · weight 5 · scope: site · method: ai · Google official: [Search Quality Rater Guidelines](https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf)

- **Test:** Licences, certifications, insurance or memberships relevant to the service are displayed with issuer.
- **Fix:** Show credentials with numbers/links to the issuing body.

**SERV-005 · Clear conversion path on every service page**  
`medium` · weight 5 · scope: page · method: crawl · Industry practice: [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

- **Test:** Each service page has a visible quote/contact form or click-to-call/WhatsApp link.
- **Fix:** Add a primary enquiry action above the fold.

**SERV-006 · Service pages answer buying questions**  
`medium` · weight 5 · scope: page · method: ai · Google official: [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

- **Test:** Pages explain process, coverage, timelines and pricing approach, with FAQs.
- **Fix:** Add the missing decision information listed per page.

**SERV-007 · Utility pages kept out of the index**  
`medium` · weight 4 · scope: site · method: crawl · Google official: [Robots meta tag, data-nosnippet and X-Robots-Tag](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag)

- **Test:** Tracking, customer portal, login and thank-you pages are noindex.
- **Fix:** Add noindex to utility templates.

**SERV-008 · Proof per service**  
`medium` · weight 4 · scope: language · method: ai · Google official: [Search Quality Rater Guidelines](https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf)

- **Test:** Case studies or testimonials tied to each main service.
- **Fix:** Publish at least one case study per core service.
