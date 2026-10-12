#!/usr/bin/env python3
"""Recompute the split control memory's documented fit from this round's own receipts.

usage: fit_check.py <tree> <links-head> <links-prev> <map-tsv> <size-head> <size-prev>

<links-*> are link_points.sh outputs (split ELF plans and flat logs); <map-tsv> is
ctrl_memory_ooc.tsv from the Vivado run on the head ELFs; <size-*> are
`size -A` outputs of the largest split ELF at head and at the previous revision.
Every figure the three pages state about the fit and ledger is derived here
and compared with the page text. Prints one line per check; exit 1 on any miss.
"""
import json
import re
import sys
from pathlib import Path

tree, lh, lp, tsv, sh, sp = map(Path, sys.argv[1:7])
POINTS = ("1x1_tdm8_i1", "1x1_tdm8_i2", "8x8_i1", "8x8_i2")
TAGS = ("s1i1", "s1i2", "s8i1", "s8i2")
fails = 0


def ok(cond, what):
    global fails
    fails += not cond
    print(("PASS " if cond else "FAIL ") + what)


def plans(d):
    out = {}
    for p in POINTS:
        plan = json.loads((d / f"{p}_split.plan").read_text())
        span = int(re.search(r'"ram_span": (\d+)', (d / f"{p}_flat.log").read_text()).group(1))
        out[p] = (plan, span)
    return out


head, prev = plans(lh), plans(lp)
rows = {}
for line in tsv.read_text().splitlines()[1:]:
    top, r36, r18, lut, ff, _ = line.split("\t")
    rows[top] = tuple(map(int, (r36, r18, lut, ff)))

split = (tree / "docs/design/SPLIT_CONTROL_MEMORY.md").read_text()
plan_md = (tree / "docs/design/MARK_II_AREA_PLAN.md").read_text()
budget_md = (tree / "docs/design/AREA_BUDGET.md").read_text()
fmt = "{:,}".format

mapped, planned = {}, {}
fills = []
for p, t in zip(POINTS, TAGS):
    plan, span = head[p]
    r, s = rows[f"{t}_rom"], rows[f"{t}_sram"]
    r36, r18 = r[0] + s[0], r[1] + s[1]
    tiles = r36 + r18 / 2
    mapped[p], planned[p] = tiles, plan["tiles"]
    for reg in ("rom", "sram"):
        ok(plan[reg]["bytes"] <= sum(plan[reg]["banks"]), f"{p} {reg} banks hold the need")
        fills.append(100 * plan[reg]["bytes"] / sum(plan[reg]["banks"]))
    floor = -(-span // 4096)
    cells = (f"| {fmt(plan['rom']['bytes'])} | {fmt(plan['sram']['bytes'])} | {plan['tiles']:.1f} | "
             f"{r36} / {r18} | {tiles:.1f} | {r[2] + s[2]} / {r[3] + s[3]} | {floor} |")
    ok(cells in split, f"SPLIT_CONTROL_MEMORY table row {p}: {cells}")
    ok(plan["tiles"] <= 56 and tiles <= 56, f"{p} planned {plan['tiles']} and mapped {tiles} within 56 RAMB36")
    ok(span <= 224 * 1024, f"{p} flat span {span} B within 224 KiB (229,376 B); decimal 224,000 B: {span <= 224000}")

lo, hi = min(fills), max(fills)
ok(f"The banks hold {lo:.1f} to {hi:.1f} percent of their bytes." in split, f"fill range {lo:.1f}-{hi:.1f}")
big, big_prev = "8x8_i2", "8x8_i2"
plan = head[big][0]
ok(f"The largest leaves {56 - mapped[big]:g} tiles as mapped." in split, f"largest leaves {56 - mapped[big]:g} tiles as mapped")
slack = sum(sum(plan[r]["banks"]) - plan[r]["bytes"] for r in ("rom", "sram"))
grow = (56 - plan["tiles"]) * 4096
ok(f"its banks can grow {grow / 1024:g} KiB ({56 - plan['tiles']:.1f} tile)" in split and f"{fmt(int(grow + slack))} B." in split,
   f"planned headroom {grow:g} B, with slack {int(grow + slack)} B")

# Earlier revision kept with its source.
prev_planned = " / ".join(f"{prev[p][0]['tiles']:.1f}" for p in POINTS)
ok(f"planned {prev_planned} and mapped" in split, f"ce10328c planned figures {prev_planned}")


def sec(path):
    d = {}
    for line in path.read_text().splitlines():
        f = line.split()
        if len(f) >= 2 and f[0].startswith(".") and f[1].isdigit():
            d[f[0]] = int(f[1])
    return d


a, b = sec(sh), sec(sp)
dt, db = a[".text"] - b[".text"], a[".bss"] - b[".bss"]
ok(f"added {fmt(dt)} B of `.text` and {fmt(db)} B of `.bss` at the largest point" in split, f".text +{dt}, .bss +{db}")
nb, pb = len(plan["rom"]["banks"]), len(prev[big_prev][0]["rom"]["banks"])
ok(nb == 5 and pb == 4 and "its `rom` gained a fifth bank" in split, f"rom banks {pb} -> {nb}")

# Ledger arithmetic, both pages.
T = int(mapped[big])
fw36 = rows["s8i2_rom"][0] + rows["s8i2_sram"][0]
fw18 = rows["s8i2_rom"][1] + rows["s8i2_sram"][1]
pre = 87.5 - 6.5 + 6 - 18 + T + 2
post = pre - 11
row = f"| M8a-1: firmware allocation as mapped, 8x8 with two interfaces | +{fw36} | +{fw18} | +{T} | {87.5 - 6.5 + 6 - 18 + T:g} |"
for name, md in (("MARK_II_AREA_PLAN", plan_md), ("AREA_BUDGET", budget_md)):
    ok(row in md, f"{name} firmware row {row}")
    ok(f"| M2 maximum additional allocation | +2 | 0 | +2 | {pre:g} |" in md, f"{name} M2 row total {pre:g}")
    ok(f"| -10 | -2 | -11 | {post:g} |" in md, f"{name} release row total {post:g}")
    ok(f"`87.5 - 6.5 + 6 - 18 + {T} + 2 = {pre:g}`" in md, f"{name} arithmetic = {pre:g}")
    ok(f"{pre - 121.5:g} tiles over 121.5" in md, f"{name} {pre - 121.5:g} over before release")
    ok(f"{121.5 - post:g} below" in md, f"{name} {121.5 - post:g} below after release")
    ok(f"{pre + 18:g}` and `{post + 18:g}" in md.replace(" and ", "` and `").replace(": ", "`") or
       f"{pre + 18:g} and {post + 18:g}" in md, f"{name} BIOS kept {pre + 18:g} / {post + 18:g}")
    ok(f"`{pre:g} + 6 = {pre + 6:g}`" in md and f"{pre + 6 - 121.5:g}" in md, f"{name} partial {pre + 6:g}, {pre + 6 - 121.5:g} over")
allbram = pre + (planned[big] - T)
ok(f"`{allbram:g}`, and {allbram - 11:g} after the release" in plan_md, f"MARK_II all-BRAM {allbram:g} / {allbram - 11:g}")
ok(f"leaves {121.5 - (allbram - 11):g}." in plan_md and f"or {121.5 - (allbram - 11):g} with every bank in block RAM" in budget_md,
   f"all-BRAM headroom {121.5 - (allbram - 11):g}")
ok(f"{post:g} tiles after the split's release" in split, f"SPLIT page {post:g} after release")
print(f"RESULT: {'PASS' if not fails else 'FAIL'} ({fails} failed)")
sys.exit(1 if fails else 0)
