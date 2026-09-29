#!/usr/bin/env python3
"""Compare each suite README's recorded failing-check count for a d3_mutants.py
mutant with the count of FAIL lines in a reviewer run of the in-tree driver.
Usage: readme_vs_run.py <tree> <results.json> [<results.json> ...]"""
import json, re, sys, pathlib

tree = pathlib.Path(sys.argv[1])
run = {}
for f in sys.argv[2:]:
    for r in json.loads(pathlib.Path(f).read_text()):
        if not r["mutant"].startswith("golden-"):
            run[r["mutant"]] = (r["verdict"], len(r.get("failing_checks", [])))
rec = {}
for readme in sorted(tree.glob("tb/*/README.md")):
    for line in readme.read_text().splitlines():
        m = re.match(r"^\| `([A-Za-z0-9_]+)` \|.*\| (\d+) \|\s*$", line)
        if m and m.group(1) in run:
            rec[m.group(1)] = (readme.parent.name, int(m.group(2)))
        m = re.search(r"`([A-Za-z0-9_]+)`.*\((\d+) FAILs?\)", line)
        if m and m.group(1) in run and m.group(1) not in rec:
            rec[m.group(1)] = (readme.parent.name, int(m.group(2)))
killed = sum(v[0] == "KILLED" for v in run.values())
diff = [(n, rec.get(n), run[n][1]) for n in sorted(run) if rec.get(n, (None, None))[1] != run[n][1]]
print(f"mutants run: {len(run)}  KILLED: {killed}  README records found: {len(rec)}")
print(f"equal: {len(run) - len(diff)}  different or unrecorded: {diff}")
