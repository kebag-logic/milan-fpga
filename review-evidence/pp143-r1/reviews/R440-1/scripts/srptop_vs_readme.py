#!/usr/bin/env python3
"""Compare srp_top mutants.py summary rows (label, failures, tags) with tb/srp_top/README.md's arm table, in order."""
import re
import sys
readme, summary = open(sys.argv[1]).read(), open(sys.argv[2]).read()
rows = [(m[0], int(m[1])) for m in re.findall(r"^\| `([\w-]+)` \| [\w ]+ \| (\d+) \|", readme, re.M)]
run = [(m[0], int(m[1])) for m in re.findall(r"^([\w-]+): rc=\d+ failures=(\d+) KILLED", summary, re.M)]
print(f"README arm rows {len(rows)}, KILLED runs {len(run)}, same rows in the same order: {rows == run}")
if rows != run:
    print("README-only:", sorted(set(rows) - set(run)), "run-only:", sorted(set(run) - set(rows)))
