#!/usr/bin/env python3
"""Compute (never run) ci_toolcache_isolation's setup window and gate tail for every
elaborate-gates-N job at a revision. usage: toolcache_plans.py <repo> <rev>"""
import subprocess, sys
from pathlib import Path
repo, rev = Path(sys.argv[1]), sys.argv[2]
sys.path.insert(0, str(repo / "scripts"))
import yaml, ci_toolcache_isolation as t
jobs = yaml.safe_load(subprocess.check_output(["git", "-C", str(repo), "show", f"{rev}:{t.WORKFLOW}"]))["jobs"]
names = sorted(n for n in jobs if t.LEG_JOB.fullmatch(n))
print("legs:", names)
for n in names:
    w = t.window(jobs[n], False); tl = t.tail(jobs[n])
    print(n, "window", len(w), [s.get("name", s.get("uses")) for s in w][-2:], "| tail", [s.get("name") for s in tl], "| modules", t.modules(jobs[n]))
