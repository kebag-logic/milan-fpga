#!/usr/bin/env python3
"""stop_table.py <head> <out.md> <not_run.json> <job>...: the rc of every run: step of the job instances named (as
ci_replay.py names them), from each one's result.json, and every step that did not run with its reason; exit 1 on a
missing result or a nonzero step."""
import json
import sys
from pathlib import Path

head, out, not_run, jobs = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4:]
root = Path("/data-2/milan/tmp/665s7-a757b/ci") / head[:12] / "jobs"
lines = [f"head {head}", "", "| Workflow / job | Step | Name | rc | Note |", "|---|---|---|---|---|"]
skipped, failed, ran = [], 0, 0
for name in jobs:
    p = root / name / "result.json"
    if not p.exists():
        lines.append(f"| {name} | | | no result | |")
        failed += 1
        continue
    r = json.loads(p.read_text())
    if r["result"] == "skipped" and not r["steps"]:
        lines.append(f"| {name} | (job) | | skipped | the job's if: is false for this event |")
        skipped.append({"job": name, "reason": "the job's if: is false for a pull_request to dev-soft-core"})
        continue
    for s in r["steps"]:
        if s["kind"] != "run" and not str(s["rc"]).isdigit():
            continue
        note = s.get("reason") or (f"replaced: {s['replaced']}" if s.get("replaced") else "")
        note = note or (f"rewritten: {s['transformed']}" if s.get("transformed") else "")
        lines.append(f"| {name} | {s['step']} | {s['name'][:60]} | {s['rc']} | {note} |")
        if s["rc"] == "not run":
            skipped.append({"step": f"{name}/{s['step']}", "reason": s["reason"]})
        elif isinstance(s["rc"], int):
            ran += 1
            failed += s["rc"] != 0
    lines.append(f"| {name} | (job result) | | {r['result']} | |")
    failed += r["result"] != "success"
lines += ["", f"{len(jobs)} job instances; {ran} run: steps ran, {failed} failed or missing; {len(skipped)} not run, "
          "each with its reason"]
text = "\n".join(lines) + "\n"
for path, mark in (("/data-2/milan/tmp/665s7-a757b", "<scratch>"), ("$WORKSPACE_HOME", "<home>"), ("$VALIDATION_STORAGE", "<data>")):
    text = text.replace(path, mark)
out.write_text(text)
not_run.write_text(json.dumps({"head": head, "not_run": skipped}, indent=1) + "\n")
print(lines[-1])
sys.exit(1 if failed else 0)
