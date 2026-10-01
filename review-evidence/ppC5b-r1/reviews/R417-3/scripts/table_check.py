#!/usr/bin/env python3
"""Reviewer check of tb/pp_top/README.md's AECP dispatch mutation table.
1. Every pipe-table row in the README has its header's cell count (a `|` inside a code span
   is reported separately, since GitHub splits on it too).
2. Every arm row of the AECP dispatch table matches the driver's MUTANTS list (arm, named
   check prefix) and its failing-check cell equals the count in the campaign's results.json.
usage: table_check.py <README.md> <aecp_dispatch_mutants.py> <results.json>..."""
import importlib.util, json, re, sys
sys.dont_write_bytecode = True
readme, driver, results = sys.argv[1], sys.argv[2], sys.argv[3:]
lines = open(readme, encoding="utf-8").read().splitlines()
def cells(row):  # GitHub splits on every unescaped |, code spans included
    return [c.strip() for c in re.split(r"(?<!\\)\|", row.strip())[1:-1]]
bad = 0; hdr = None
for n, l in enumerate(lines, 1):
    if not l.startswith("|"):
        hdr = None; continue
    if hdr is None:
        hdr = len(cells(l)); continue
    if re.match(r"^\|[\s:|-]+\|$", l): continue
    if len(cells(l)) != hdr:
        bad += 1; print(f"ROW-SHAPE line {n}: {len(cells(l))} cells under a {hdr}-cell header: {l[:110]}")
print(f"rows off their header: {bad}")
start = next(i for i, l in enumerate(lines) if l.startswith("### AECP dispatch and response negative controls"))
rows = {}
for l in lines[start:]:
    if l.startswith("| `"):
        c = cells(l); rows[c[0].strip("`")] = c
    elif rows and not l.startswith("|"):
        break
spec = importlib.util.spec_from_file_location("drv", driver); drv = importlib.util.module_from_spec(spec); spec.loader.exec_module(drv)
res = {}
for r in results:
    for rec in json.load(open(r)):
        if "patch" in rec: res[rec["arm"]] = rec
diff = 0
for arm, patch, target, expected in drv.MUTANTS:
    row = rows.get(arm)
    got = res.get(arm)
    if row is None: print(f"MISSING ROW {arm}"); diff += 1; continue
    if got is None: print(f"NOT RUN {arm}"); diff += 1; continue
    named = row[2].strip("`")
    pre = named.split("...")[0].rstrip(", ").rstrip()
    name_ok = expected.startswith(pre)
    cnt_ok = row[-1] == str(got["failures"]) and len(row) == 4
    verdict_ok = got["verdict"] == "KILLED"
    flag = "ok" if (name_ok and cnt_ok and verdict_ok) else "DIFF"
    diff += flag == "DIFF"
    print(f"{flag:4} {arm:32} README={row[-1]:>3} campaign={got['failures']:>3} {got['verdict']} named-check-prefix={'ok' if name_ok else 'MISMATCH'}")
extra = set(rows) - {m[0] for m in drv.MUTANTS}
for e in sorted(extra): print(f"EXTRA ROW {e}"); diff += 1
print(f"arms: {len(drv.MUTANTS)}, rows: {len(rows)}, differing: {diff}")
sys.exit(1 if diff else 0)
