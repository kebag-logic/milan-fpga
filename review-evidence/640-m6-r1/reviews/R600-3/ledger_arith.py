#!/usr/bin/env python3
"""Recompute the Mark II ledger figures that lanes M2 and M6 both touch.

Usage: ledger_arith.py <MARK_II_AREA_PLAN.md> <AREA_BUDGET.md>
Prints one line per check and exits 1 if any check fails.
"""
import re
import sys

plan_path, budget_path = sys.argv[1], sys.argv[2]
plan = open(plan_path, encoding="utf-8").read()
budget = open(budget_path, encoding="utf-8").read()
fails = 0


def check(name, got, want):
    global fails
    ok = got == want
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} {name}: got {got!r} want {want!r}")


def num(s):
    return int(s.replace(",", "").replace("+", ""))


def section(text, heading):
    m = re.search(rf"^### {re.escape(heading)}\n(.*?)(?=^### |\Z)", text, re.M | re.S)
    if not m:
        raise SystemExit(f"missing section {heading}")
    return m.group(1)


def rows(text, first):
    return [l for l in text.splitlines() if l.startswith(f"| {first}")]


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


for lane, routed, synth in (("M2", 128, 34), ("M6", 706, 524)):
    sec = section(plan, f"{lane} intermediate measurement")
    base = cells(rows(sec, "Base route")[0])
    route = cells(rows(sec, f"{lane} route")[0])
    delta = cells(rows(sec, "Routed delta")[0])
    for i, name in ((1, "LUT"), (2, "FF"), (3, "Slices")):
        check(f"{lane} routed delta {name}", num(route[i]) - num(base[i]), num(delta[i]))
    check(f"{lane} base row equals record 50,267 LUT", base[1], "50,267")
    bw, bh = (float(x) for x in base[5].split(" / "))
    rw, rh = (float(x) for x in route[5].split(" / "))
    dw, dh = (float(x) for x in delta[5].split(" / "))
    check(f"{lane} WNS delta", round(rw - bw, 3), dw)
    check(f"{lane} WHS delta", round(rh - bh, 3), dh)
    check(f"{lane} routed LUT delta stated", -num(delta[1]), routed)
    syn = cells(rows(sec, "Post-synthesis delta")[0])
    check(f"{lane} post-synthesis delta stated", -num(syn[1]), synth)

m6 = section(plan, "M6 intermediate measurement")
credit_r = credit_s = 0
for blk in ("Listener monitor", "Channel-map capture"):
    c = cells(rows(m6, blk)[0])
    r0, r1 = (num(x) for x in c[1].split(" -> "))
    s0, s1 = (num(x) for x in c[2].split(" -> "))
    credit_r += r0 - r1
    credit_s += s0 - s1
check("M6 credited routed saving", credit_r, 468)
check("M6 credited post-synthesis saving", credit_s, 418)
check("M6 text states 418/468", "The reproducible saving is 418 LUTs post-synthesis, 468 routed." in m6, True)
check("M2 text states 34", "The reproducible saving is 34 LUTs" in section(plan, "M2 intermediate measurement"), True)
check("AREA_BUDGET M2 note", "M2 has measured its lane: 34 LUTs post-synthesis, 128 routed" in budget, True)
check("AREA_BUDGET M6 note", "M6 has measured its lane: 418 LUTs post-synthesis, 468 routed in its blocks" in budget, True)
check("plan L3 M2 pointer", "M2 measured 34 LUTs post-synthesis and no extra tile" in plan, True)
check("plan L9 M6 pointer", "M6 measured 418 LUTs post-synthesis and no extra tile" in plan, True)

# Cumulative table: each image = previous image - saving (central column);
# the table keeps planning savings, so recompute it from its own rows.
cum = section(plan, "Cumulative default-image estimates")
prev = None
for line in cum.splitlines():
    if not re.match(r"\| \d+ \|", line):
        continue
    c = cells(line)
    if c[3] == "Measure":
        continue
    img = num(c[3])
    if prev is not None:
        check(f"cumulative row {c[0]} {c[1]}", prev - num(c[2]), img)
    prev = img
lanes = [cells(l)[1] for l in cum.splitlines() if re.match(r"\| \d+ \|", l)]
for lane in ("M2", "M6"):
    check(f"cumulative table lists {lane} once", lanes.count(lane), 1)
check("central headroom", 38040 - prev, 6373)

# AREA_BUDGET lane table: same recomputation.
prev = None
seen = []
for line in budget.splitlines():
    m = re.match(r"\| (F0-F5 split|M\d+\w* [^|]*?) \| ([\d,]+) \| ([\d,]+) \|", line)
    if not m:
        continue
    seen.append(m.group(1).split()[0])
    img = num(m.group(3))
    if prev is not None:
        check(f"budget lane row {m.group(1)}", prev - num(m.group(2)), img)
    prev = img
for lane in ("M2", "M6"):
    check(f"budget lane table lists {lane} once", seen.count(lane), 1)

print(f"{'FAIL' if fails else 'PASS'}: {fails} failure(s)")
sys.exit(1 if fails else 0)
