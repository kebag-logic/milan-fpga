#!/usr/bin/env python3
"""budgets.py JOBS_TSV WORKFLOW: each hosted firmware job's wall time against 60 % of its timeout-minutes."""
import sys, re
from datetime import datetime
jobs = {}
for line in open(sys.argv[1]):
    jid, name, status, concl, start, end, sha = line.rstrip("\n").split("\t")
    jobs[name] = (status, concl, start, end, sha)
text = open(sys.argv[2]).read()
timeouts = {m.group(1): int(m.group(2)) for m in re.finditer(r"^  ([a-z0-9-]+):\n(?:    .*\n)*?    timeout-minutes: (\d+)", text, re.M)}
ok = True
for name in ("firmware-unit", "firmware-control-mutants", "firmware-aecp-mutants", "firmware-srp-mutants",
             "firmware-boundary", "firmware-verilator"):
    status, concl, start, end, sha = jobs[name]
    t = lambda s: datetime.fromisoformat(s.replace("Z", "+00:00"))
    secs = (t(end) - t(start)).total_seconds()
    budget = timeouts[name] * 60
    frac = secs / budget
    ok &= concl == "success" and frac <= 0.60
    print(f"{name:26s} {concl:8s} {secs:5.0f} s of {budget:5d} s = {100*frac:5.1f} %  head {sha[:12]}")
print("all within 60 %" if ok else "OVER BUDGET OR NOT SUCCESS")
