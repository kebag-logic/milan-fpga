#!/usr/bin/env python3
"""Compare each notify mutant's failing-check count (from the campaign's
results.json files) with the leading number of its README record row.
usage: notify_counts.py REPO RESULTS_DIR..."""
import json, pathlib, re, sys
repo = pathlib.Path(sys.argv[1])
rec = {}
for readme in ("tb/pp_top/README.md", "tb/aecp_notify/README.md", "tb/originator/README.md"):
    for line in (repo / readme).read_text().splitlines():
        m = re.match(r"^\| `([a-z0-9_]+)` \|[^|]*\| (\d[\d,]*)", line)
        if m:
            rec.setdefault(m.group(1), (int(m.group(2).replace(",", "")), readme, line[:160]))
res = {}
for d in sys.argv[2:]:
    for r in json.loads((pathlib.Path(d) / "results.json").read_text()):
        if not r["mutant"].startswith("golden-"):
            res[r["mutant"]] = r
bad = 0
for name, r in sorted(res.items()):
    n = len(r["failing_checks"])
    want = rec.get(name)
    ok = want is not None and want[0] == n
    bad += not ok
    print(f"{'OK ' if ok else 'DIFF'} {name}: verdict {r['verdict']}, failing {n}, README {want[0] if want else None}")
print(f"{len(res)} mutants, {sum(r['verdict']=='KILLED' for r in res.values())} KILLED, {bad} count differences")
