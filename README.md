# SEO / GEO / AEO Audit Dashboard

Enter a domain, answer a short questionnaire, and get a scored audit across SEO (technical, on-page, off-page), GEO, AEO, Local SEO and site-type modules, plus a client-ready 12-month plan (.xlsx, opens in Google Sheets).

Status: early version. The catalog defines 285 checks; the crawler currently automates the ones that can be decided from HTML, robots.txt, sitemaps and HTTP responses. Every other check is listed in the report as "not run" with the reason (needs AI analysis, an API connection, Search Console access or manual review). Scores only cover the checks that ran.

## How it works

| Part | Where | What it does |
|---|---|---|
| Catalog | `catalog/checks.yaml` | Every check with severity, weight, test, fix and its source (Google official / platform official / industry practice) |
| Audit code | `audit/` | Crawler, check implementations, scoring, Screaming Frog import, plan builder |
| Questionnaire | `intake/questions.json` | Tools checklist and project questions that shape the plan |
| Plan template | `plan/plan-template.yaml` | Workstreams, baseline tasks and their months |
| Dashboard | `index.html` | Static page (GitHub Pages) that starts audits and shows results |
| Private data repo | see `data-repo-template/` | Runs the audit in GitHub Actions and stores results, so client data is never public |

## Setup

1. Create a private repository (for example `seo-audit-data`) and copy `data-repo-template/.github/workflows/audit.yml` into it at the same path.
2. Enable GitHub Pages for this repository (Settings > Pages > Deploy from a branch > `main` / root).
3. Create a fine-grained personal access token limited to the private data repository with: Contents (read and write), Actions (read and write).
4. Open the dashboard, go to Settings, and enter the data repository (`owner/name`) and the token. The token is stored only in your browser.

## Run locally

```
pip install -r requirements.txt
python -m audit.run --domain example.com --intake answers.json --out out/
```

Optional: `--sf internal_all.csv` merges a Screaming Frog "Internal: All" export; `--max-pages 500` sets the crawl limit.

## Credits

The check catalog was informed by the MIT-licensed [claude-seo](https://github.com/AgriciDaniel/claude-seo) project and by Google Search Central documentation, which each check links to.
