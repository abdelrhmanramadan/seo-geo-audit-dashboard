"""Render catalog/checks.yaml into a readable catalog/CATALOG.md."""
import sys, collections, yaml
from pathlib import Path

root = Path(__file__).resolve().parent.parent
d = yaml.safe_load((root / "catalog" / "checks.yaml").read_text(encoding="utf-8"))
src = d["sources"]
basis_label = {"google": "Google official", "platform": "Platform official", "industry": "Industry practice"}
out = []
counts = collections.Counter()
for p in d["pillars"]:
    for s in p["sections"]:
        for ss in s["subsections"]:
            counts[p["name"]] += len(ss["checks"])

out.append("# Checks Catalog\n")
out.append(f"Version {d['version']} · updated {d['updated']} · generated from `checks.yaml` (do not edit by hand)\n")
out.append("## Summary\n")
out.append("| Pillar | Weight in overall score | Checks |\n|---|---|---|")
for p in d["pillars"]:
    out.append(f"| {p['name']} | {d['scoring']['pillar_weights'][p['id']]}% | {counts[p['name']]} |")
out.append(f"| **Total** | 100% | **{sum(counts.values())}** |\n")
out.append("## Scoring model\n")
for k, v in d["scoring"].items():
    if isinstance(v, (str,)):
        out.append(f"- **{k.replace('_',' ')}**: {v.strip()}")
out.append("- **results**: pass = 1, warn = 0.5, fail = 0; N/A and info are excluded from the denominator\n")
out.append("## Structure\n")
for p in d["pillars"]:
    out.append(f"- **{p['name']}**")
    for s in p["sections"]:
        out.append(f"  - {s['name']} ({s['weight']}%)")
        for ss in s["subsections"]:
            out.append(f"    - {ss['name']} ({ss['weight']}%) — {len(ss['checks'])} checks")
out.append("")
for p in d["pillars"]:
    out.append(f"\n---\n\n## {p['name']}\n")
    if p.get("note"): out.append(f"> {p['note'].strip()}\n")
    if p.get("applicable_when"): out.append(f"> Applies when: {p['applicable_when']}\n")
    for s in p["sections"]:
        out.append(f"### {s['name']} — {s['weight']}% of {p['name']}\n")
        for ss in s["subsections"]:
            out.append(f"#### {ss['name']} — {ss['weight']}% of {s['name']}\n")
            if ss.get("note"): out.append(f"> {ss['note']}\n")
            for c in ss["checks"]:
                so = src[c["source"]]
                at = c.get("applies_to")
                at = f" · applies to: {', '.join(at) if isinstance(at, list) else at}" if at else ""
                out.append(f"**{c['id']} · {c['name']}**  ")
                out.append(f"`{c['severity']}` · weight {c['weight']} · scope: {c['scope']} · method: {c['method']}{at} · {basis_label[c['basis']]}: [{so['title']}]({so['url']})\n")
                out.append(f"- **Test:** {c['test']}")
                out.append(f"- **Fix:** {c['fix']}\n")
(root / "catalog" / "CATALOG.md").write_text("\n".join(out), encoding="utf-8")
print("written", sum(counts.values()), "checks")
