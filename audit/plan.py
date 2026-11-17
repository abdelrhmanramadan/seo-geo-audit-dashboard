"""Builds the client-ready 12-month plan workbook (.xlsx) from audit findings, the questionnaire and the plan template."""
import json
from itertools import cycle
from pathlib import Path
import yaml
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent.parent
SEV = ["critical", "high", "medium", "low"]
SEV_MONTHS = {"critical": [1], "high": [2, 3], "medium": [4, 5, 6], "low": [7, 8, 9, 10, 11, 12]}
FILL = {"critical": "F4CCCC", "high": "FCE5CD", "medium": "FFF2CC", "low": "D9EAF7"}
HEAD = PatternFill("solid", fgColor="1F3A5F")


def workstream_of(cid, streams):
    best = None
    for w in streams:
        for pre in w.get("source_checks", []):
            if cid.startswith(pre) and (best is None or len(pre) > best[0]):
                best = (len(pre), w["name"])
    return best[1] if best else "Other"


def effort(c):
    if c["scope"] != "page":
        return "S"
    return "S" if c["count"] <= 10 else "M" if c["count"] <= 50 else "L"


def sheet(wb, title, header, rows, widths, sev_col=None):
    ws = wb.create_sheet(title)
    ws.append(header)
    for c in ws[1]:
        c.font, c.fill, c.alignment = Font(bold=True, color="FFFFFF"), HEAD, Alignment(vertical="center", wrap_text=True)
    for r in rows:
        ws.append(["'" + v if isinstance(v, str) and v[:1] in "=+-@" else v for v in r])
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(vertical="top", wrap_text=True)
        if sev_col is not None:
            v = str(row[sev_col].value or "").lower()
            if v in FILL:
                row[sev_col].fill = PatternFill("solid", fgColor=FILL[v])
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    return ws


def build(result, out_path):
    tpl = yaml.safe_load((ROOT / "plan" / "plan-template.yaml").read_text(encoding="utf-8"))
    questions = json.loads((ROOT / "intake" / "questions.json").read_text(encoding="utf-8"))
    intake, meta, streams = result["intake"], result["meta"], tpl["workstreams"]
    flags = {"multilingual": len(intake.get("languages") or []) > 1, "has_locations": bool(intake.get("has_locations")),
             "site_type": intake.get("site_type") not in (None, "", "other"), "traffic_drop": bool(intake.get("traffic_drop"))}
    n_articles = int(intake.get("articles_per_month") or 4)
    road = []  # month, workstream, task, details, severity, affected, effort, source, check id, reference

    # 1. setup items left unticked in the questionnaire
    setup_rows = []
    for item in next(s for s in questions["sections"] if s["id"] == "setup")["items"]:
        cond = item.get("only_if", {})
        if any(intake.get(k) != v for k, v in cond.items()):
            continue
        exists = bool(intake.get("setup", {}).get(item["id"]))
        setup_rows.append([item["label"], "Yes" if exists else "No", "Connect to the dashboard / confirm access" if exists else item["task"]])
        if not exists:
            road.append([1, "SEO Analytics and Reporting", item["task"], "Not in place according to the questionnaire", "High", "", "S", "Setup", "", ""])

    # 2. audit findings
    findings = [c for c in result["checks"] if c["status"] in ("fail", "warn") and c["severity"] in SEV]
    findings.sort(key=lambda c: (SEV.index(c["severity"]), c["status"] != "fail", -c["count"]))
    rot = {s: cycle(m) for s, m in SEV_MONTHS.items()}
    for c in findings:
        road.append([next(rot[c["severity"]]), workstream_of(c["id"], streams), c["fix"], f"{c['name']}: {c['summary']}", c["severity"].capitalize(),
                     c["count"] or "", effort(c), "Audit finding", c["id"], c["source_url"]])

    # 3. baseline work no audit can detect
    for w in streams:
        if w["id"] == "local" and not flags["has_locations"]:
            continue
        for b in w.get("baseline_tasks", []):
            if b.get("when") and not flags.get(b["when"]):
                continue
            for m in b["months"]:
                road.append([m, w["name"], b["task"].replace("{n}", str(n_articles)), "", "", "", "", "Planned work", "", ""])

    # 4. manual checks
    manual = [c for c in result["checks"] if c["status"] == "not_run"]
    road.sort(key=lambda r: (r[0], SEV.index(r[4].lower()) if r[4] else 9, r[1]))
    phase = {m: p["name"] for p in tpl["phases"] for m in p["months"]}

    wb = Workbook()
    ws = wb.active
    ws.title = "Summary"
    counts = {s: sum(1 for c in findings if c["severity"] == s) for s in SEV}
    lines = [["SEO / GEO / AEO audit and 12-month plan"], [meta["domain"]], [],
             ["Audit date", meta["crawled_at"][:10]], ["Pages analysed", meta["pages_crawled"]],
             ["Checks run", f"{meta['coverage']['ran']} of {meta['coverage']['applicable']} applicable checks"],
             ["Note", "Scores cover only the checks that ran. Checks listed in 'Manual review' still need to be completed."], [],
             ["Overall score", result["scores"]["overall"]], [], ["Area", "Score (0-100)"]]
    for p in result["scores"]["pillars"]:
        if p["score"] is not None:
            lines.append([p["name"], p["score"]])
            lines += [["   " + s["name"], s["score"]] for s in p["sections"] if s["score"] is not None]
    lines += [[], ["Issues found", "Count"]] + [[s.capitalize(), counts[s]] for s in SEV]
    if result.get("by_language"):
        lines += [[], ["Language", "Overall score", "Pages"]] + [[k, v["overall"], v["pages"]] for k, v in result["by_language"].items()]
    for l in lines:
        ws.append(l)
    ws["A1"].font, ws["A2"].font = Font(bold=True, size=16), Font(bold=True, size=13)
    for r in ws.iter_rows(min_row=9):
        if r[0].value in ("Overall score", "Area", "Issues found", "Language"):
            for c in r:
                c.font = Font(bold=True)
    ws.column_dimensions["A"].width, ws.column_dimensions["B"].width = 44, 60

    sheet(wb, "12-month roadmap", ["Month", "Phase", "Workstream", "Task", "What was found", "Severity", "Affected URLs", "Effort", "Type", "Check ID", "Reference", "Owner", "Status"],
          [[f"Month {r[0]}", phase[r[0]], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], "", "Not started"] for r in road],
          [10, 22, 24, 60, 50, 11, 10, 8, 14, 11, 40, 14, 13], sev_col=5)
    sheet(wb, "Issues", ["Severity", "Result", "Check ID", "Area", "Issue", "What was found", "Affected URLs", "How to fix", "Basis", "Reference"],
          [[c["severity"].capitalize(), c["status"], c["id"], f"{c['section_name']} / {c['subsection_name']}", c["name"], c["summary"], c["count"] or "", c["fix"],
            {"google": "Google official", "platform": "Platform official", "industry": "Industry practice"}[c["basis"]], c["source_url"]] for c in findings],
          [11, 8, 11, 34, 36, 50, 10, 60, 16, 40], sev_col=0)
    quick = [c for c in findings if effort(c) == "S" and c["severity"] in ("critical", "high")]
    sheet(wb, "Quick wins", ["Severity", "Check ID", "Issue", "What was found", "How to fix"],
          [[c["severity"].capitalize(), c["id"], c["name"], c["summary"], c["fix"]] for c in quick], [11, 11, 40, 55, 65], sev_col=0)
    sheet(wb, "Setup checklist", ["Tool / access", "In place", "Action"], setup_rows, [42, 10, 90])
    cal = [[f"Month {m}", i + 1, "Article", "", "", "", "Planned"] for m in range(2, 13) for i in range(n_articles)]
    sheet(wb, "Content calendar", ["Month", "#", "Type", "Topic (from keyword research)", "Target keyword", "Target page / cluster", "Status"], cal, [10, 5, 10, 50, 30, 34, 12])
    sheet(wb, "Manual review", ["Check ID", "Area", "Check", "Severity", "Why it was not automated", "What to verify"],
          [[c["id"], f"{c['section_name']} / {c['subsection_name']}", c["name"], c["severity"].capitalize(), c["summary"], c["test"]] for c in manual],
          [11, 34, 38, 11, 40, 70], sev_col=3)
    detail = [[c["id"], c["name"], i["url"], i["detail"]] for c in findings for i in c["items"]]
    sheet(wb, "Affected URLs", ["Check ID", "Issue", "URL", "Detail"], detail[:20000], [11, 38, 60, 70])
    wb.save(out_path)
    return {"roadmap_rows": len(road), "findings": len(findings), "manual": len(manual)}
