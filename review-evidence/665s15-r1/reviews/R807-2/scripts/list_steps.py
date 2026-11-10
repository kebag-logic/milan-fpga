#!/usr/bin/env python3
"""List every run: step of the given workflow files as job/step/first lines; filter by regex."""
import re, sys, yaml
pat = re.compile(sys.argv[1]) if len(sys.argv) > 2 else None
for wf in sys.argv[2:] if pat else sys.argv[1:]:
    d = yaml.safe_load(open(wf))
    for job, j in d.get("jobs", {}).items():
        for i, s in enumerate(j.get("steps", [])):
            r = s.get("run")
            if not r:
                continue
            if pat and not pat.search(r):
                continue
            print(f"== {wf.split('/')[-1]} :: {job} :: #{i} {s.get('name','')}")
            print("   " + r.strip().replace("\n", "\n   ")[:1500])
