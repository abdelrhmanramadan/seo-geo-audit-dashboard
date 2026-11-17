# Audit data (private)

Holds the audit runs and client data for the SEO / GEO / AEO audit dashboard. Keep this repository private.

- `.github/workflows/audit.yml` runs an audit when the dashboard (or you, from the Actions tab) starts one
- `audits/index.json` lists every audit; `audits/<domain>/<date>/` holds `result.json` and `plan.xlsx`
- `uploads/` holds Screaming Frog exports sent from the dashboard
