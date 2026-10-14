#!/usr/bin/env python3
"""For every step of every job in .github/ci-templates/<wf>.yml, look for a step in
the generated .github/workflows/<wf>.yml (same job, or the docs/elaborate gate
workers for the carrier) with identical run/uses/with/env/if/continue-on-error.
Report each template step with no identical generated counterpart, and every
generated step condition that is not in the template. Usage:
  python3 -I template_step_preservation.py <clone-root>"""
import json, sys
from pathlib import Path
import yaml
root = Path(sys.argv[1])
CARRIER = {"docs": "docs-check", "elaborate": "elaborate"}
KEYS = ("run", "uses", "with", "env", "if", "continue-on-error", "shell", "working-directory", "timeout-minutes")
def norm(s): return {k: s.get(k) for k in KEYS}
report = {}
for wf in ("docs", "elaborate", "rtl-fast", "rtl"):
    t = yaml.safe_load((root / f".github/ci-templates/{wf}.yml").read_text())
    g = yaml.safe_load((root / f".github/workflows/{wf}.yml").read_text())
    rows = []
    for job, jv in t["jobs"].items():
        targets = [job]
        if CARRIER.get(wf) == job:
            targets = [f"{wf}-gates-0", f"{wf}-gates-1"]
        gen = [norm(s) for tj in targets for s in g["jobs"].get(tj, {}).get("steps", [])]
        for i, s in enumerate(jv.get("steps", [])):
            if norm(s) not in gen:
                # find a same-named generated step to show what changed
                name = s.get("name")
                cands = [x for tj in targets for x in g["jobs"][tj]["steps"] if x.get("name") == name]
                diff = {}
                if cands:
                    c = cands[0]
                    diff = {k: {"template": s.get(k), "generated": c.get(k)} for k in KEYS if s.get(k) != c.get(k)}
                rows.append({"job": job, "index": i, "name": name or s.get("uses"), "generated_same_name": bool(cands),
                             "changed_fields": sorted(diff), "detail": diff})
    report[wf] = rows
print(json.dumps(report, indent=1, default=str))
