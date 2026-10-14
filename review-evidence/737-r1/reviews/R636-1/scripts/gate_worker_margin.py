#!/usr/bin/env python3
"""Project each generated docs/elaborate gate worker from the published hosted
baseline step windows (run at 7032bca5) and compare with its timeout-minutes.
Steps are matched by name to the generated worker's step list. New steps
(budget, receipt record/upload, evidence record/upload) have no baseline and
count 0, so the projection is a lower bound. Usage:
  python3 -I gate_worker_margin.py <clone-root> <baseline-dir>"""
import json, sys
from datetime import datetime
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]) / "scripts"))
import yaml
root, base = Path(sys.argv[1]), Path(sys.argv[2])
def secs(s):
    f = lambda t: datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ")
    return (f(s["completed_at"]) - f(s["started_at"])).total_seconds()
out = []
for wf, carrier in (("docs", "docs-check"), ("elaborate", "elaborate")):
    b = json.loads((base / f"baseline-{wf}.json").read_text())
    job = [j for j in b["jobs"] if j["name"] == carrier][0]
    windows = {s["name"]: secs(s) for s in job["steps"]}
    setup_job = windows.get("Set up job", 0)
    g = yaml.safe_load((root / f".github/workflows/{wf}.yml").read_text())
    for leg in (0, 1):
        w = g["jobs"][f"{wf}-gates-{leg}"]
        names = [s.get("name") or ("Run " + s.get("uses", "")) for s in w["steps"]]
        matched = sum(windows.get(n, 0) for n in names) + setup_job
        out.append({"worker": f"{wf}-gates-{leg}", "timeout_s": w["timeout-minutes"] * 60,
                    "baseline_step_seconds_lower_bound": matched,
                    "margin_s": w["timeout-minutes"] * 60 - matched,
                    "fraction_of_limit": round(matched / (w["timeout-minutes"] * 60), 3),
                    "baseline_job_seconds": job["seconds"]})
print(json.dumps(out, indent=1))
