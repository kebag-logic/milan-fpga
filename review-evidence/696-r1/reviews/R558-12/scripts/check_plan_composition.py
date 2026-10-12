#!/usr/bin/env python3
"""Composition checks on docs/design/MARK_II_AREA_PLAN.md at a candidate tree.

Usage: python3 -I check_plan_composition.py <candidate checkout>

1. The current-inventory table's three LUT columns equal the recorded
   route-1x1 / ooc-1x1 / ooc-8x8 scope figures.
2. The partial-central figure in the M5 section follows from the plan's
   own partial-central row and the measured M2/M5/M6 savings.
3. The M5 intermediate route passes the current route-1x1 record's
   tolerance, floor and ceiling on every figure the M5 table states.
4. Lists every sentence that names "the `route-1x1` record" or the gate
   record without naming which record, with the base it is compared to.
Prints one line per result; exit 1 if any of checks 1-3 fails.
"""
import json
import re
import sys
from pathlib import Path

tree = Path(sys.argv[1])
plan = (tree / "docs/design/MARK_II_AREA_PLAN.md").read_text().splitlines()
base = json.loads((tree / "syn/ooc/pp_resource_baseline.json").read_text())
fail = 0


def num(text):
    return int(text.replace(",", ""))


def lut(endpoint, scope):
    scopes = base["endpoints"][endpoint]["record"]["scopes"]
    item = scopes.get(scope) or scopes.get(scope.replace("wrapper", "")) or {}
    return item.get("LUT") if isinstance(item, dict) else None


# 1. inventory
start = next(i for i, line in enumerate(plan) if line.startswith("### Current processor inventory"))
rows = []
for line in plan[start:start + 60]:
    m = re.match(r"\| `([^`]+)` \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \|", line)
    if m:
        rows.append((m.group(1), num(m.group(2)), num(m.group(3)), num(m.group(4))))
scopes = base["endpoints"]["route-1x1"]["record"]["scopes"]
print(f"inventory rows: {len(rows)}; recorded route scopes: {len(scopes)}")
sample = next(iter(scopes.items()))
print(f"scope key example: {sample[0]!r} -> {sample[1]}")
diffs = 0
for scope, r, o1, o8 in rows:
    for endpoint, want in (("route-1x1", r), ("ooc-1x1", o1), ("ooc-8x8", o8)):
        sc = base["endpoints"][endpoint]["record"]["scopes"]
        key = None
        for k in sc:
            kn = k.strip("/")
            if kn == scope or kn.endswith("/" + scope) or (scope == "wrapper" and kn in ("", "wrapper", "u_wrapper")):
                key = k
                break
        got = sc[key].get("LUT") if key is not None and isinstance(sc[key], dict) else None
        if got != want:
            diffs += 1
            print(f"  DIFF {endpoint} {scope}: plan {want} record {got} (key {key!r})")
print(f"[{'PASS' if diffs == 0 else 'FAIL'}] inventory: {len(rows) * 3} figures, {diffs} differences")
fail |= diffs != 0

# 2. partial central
text = "\n".join(plan)
partial = num(re.search(r"\| Partial, F5 unqualified \| Central \| ([\d,]+) \|", text).group(1))
central = {k: num(v) for k, v in re.findall(r"\| \d+ \| (M2|M5|M6) \| ([\d,]+) \|", text)}
measured = {"M2": 34, "M5": 121, "M6": 418}
m = re.search(r"partial-central scenario becomes about ([\d,]+), ([\d,]+) over ([\d,]+)", text)
stated, over, bar = num(m.group(1)), num(m.group(2)), num(m.group(3))
calc = partial + sum(central[k] - measured[k] for k in measured)
ok = calc == stated and stated - bar == over
print(f"[{'PASS' if ok else 'FAIL'}] partial central: {partial} + sum(central-measured) "
      f"{ {k: central[k] - measured[k] for k in measured} } = {calc}; stated {stated}, over {bar} by {stated - bar} (stated {over})")
fail |= not ok

# 3. M5 route against the current record
rec = base["endpoints"]["route-1x1"]
fig, tol, floor = rec["record"]["figures"], rec["tolerance"], rec["floor"]
m5 = re.search(r"\| M5 route at `\w+` \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \| (\d+) / (\d+) \| \+([\d.]+) / \+([\d.]+) \|", text)
vals = [num(m5.group(i)) for i in range(1, 6)] + [float(m5.group(6)), float(m5.group(7))]
names = ["LUT", "FF", "SLICE", "RAMB36", "RAMB18"]
ok = True
for name, v in zip(names, vals[:5]):
    good = v - fig[name] <= tol[name]
    ok &= good
    print(f"  {name}: M5 {v} record {fig[name]} growth {v - fig[name]} tol {tol[name]} {'ok' if good else 'FAIL'}")
for name, v in (("WNS_ns", vals[5]), ("WHS_ns", vals[6])):
    good = fig[name] - v <= tol[name] + 1e-9 and v >= floor[name]
    ok &= good
    print(f"  {name}: M5 {v} record {fig[name]} fall {fig[name] - v:.3f} limit {tol[name]} floor {floor[name]} {'ok' if good else 'FAIL'}")
print(f"[{'PASS' if ok else 'FAIL'}] M5 route against the current route-1x1 record (LUT {fig['LUT']})")
fail |= not ok

# 4. unqualified record references
for i, line in enumerate(plan, 1):
    if re.search(r"(equals the `route-1x1` record|Against that record|Against the record|gate record stays unchanged|The base route equals)", line):
        print(f"  ref {i}: {line[:200]}")
sys.exit(1 if fail else 0)
