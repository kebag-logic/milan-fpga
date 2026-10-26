#!/usr/bin/env python3
"""Probe: the linked-image receipt at three revisions. For each point, the
split plan (rom and sram need, tiles, or the planner's refusal) of the base
(`base-*`), of round 4's head (`r4-*`) and of this head (`head-*`), the deltas
base to head and round 4 to head, the rom left before the next 2 KiB granule,
and at the largest point the per-symbol growth from round 4 to this head.

Usage: python3 image_receipt.py <images-dir> <nm> > receipt.txt
"""
import json
import re
import subprocess
import sys
from pathlib import Path

images, nm = Path(sys.argv[1]), sys.argv[2]
POINTS = [("endstation_ax7101_1x1_tdm8", 1), ("endstation_ax7101_1x1_tdm8", 2),
          ("endstation_ax7101_8x8", 1), ("endstation_ax7101_8x8", 2)]
REFUSED = re.compile(r"([\d.]+) RAMB36 \(rom (\d+) bytes in (\d+), sram (\d+) bytes in (\d+)\)")
GRANULE = 2048


def plan(label: str, shape: str, ifs: int) -> dict:
    """The plan's figures, from its JSON or from the planner's refusal."""
    text = (images / f"{label}-{shape}-if{ifs}.plan.txt").read_text()
    try:
        d = json.loads(text)
        return {"rom": d["rom"]["bytes"], "sram": d["sram"]["bytes"], "tiles": float(d["tiles"]),
                "held": d.get("ledgered_tiles", d["budget_tiles"]), "refused": ""}
    except json.JSONDecodeError:
        m = REFUSED.search(text)
        return {"rom": int(m.group(2)), "sram": int(m.group(4)), "tiles": float(m.group(1)), "held": None,
                "refused": text.strip()}


def symbols(elf: Path) -> dict:
    """(name, type) -> size of every sized symbol."""
    out = subprocess.run([nm, "-S", "--size-sort", str(elf)], capture_output=True, text=True, check=True).stdout
    return {(p[3], p[2].lower()): int(p[1], 16) for p in (ln.split() for ln in out.splitlines()) if len(p) == 4}


print("linked image, ctrl_srp_image.py --with-aecp --layout split; ctrl_memory.py plan; budget 56 RAMB36")
print("base = e76a755a, r4 = round 4's head 989c9f53, head = this head")
print(f"{'point':31} {'base rom':>8} {'r4 rom':>8} {'head rom':>8} {'r4->h':>6} {'b->h':>6} {'base sram':>9}"
      f" {'r4 sram':>8} {'head sram':>9} {'r4->h':>6} {'b->h':>5} {'base':>5} {'r4':>5} {'head':>5} {'held to':>7}"
      f" {'rom to next granule':>19}")
for shape, ifs in POINTS:
    b, r, h = plan("base", shape, ifs), plan("r4", shape, ifs), plan("head", shape, ifs)
    spare = -(-h["rom"] // GRANULE) * GRANULE - h["rom"]
    print(f"{shape + ' if' + str(ifs):31} {b['rom']:>8} {r['rom']:>8} {h['rom']:>8} {h['rom'] - r['rom']:>+6}"
          f" {h['rom'] - b['rom']:>+6} {b['sram']:>9} {r['sram']:>8} {h['sram']:>9} {h['sram'] - r['sram']:>+6}"
          f" {h['sram'] - b['sram']:>+5} {b['tiles']:>5} {r['tiles']:>5} {h['tiles']:>5} {str(h['held']):>7}"
          f" {spare:>19}")
    for which, p in (("base", b), ("r4", r), ("head", h)):
        if p["refused"]:
            print(f"  {which}: {p['refused']}")
for shape, ifs in POINTS:
    elf = images / f"head-{shape}-if{ifs}" / "ctrl_app.elf"
    bss = sorted(((s, n) for (n, t), s in symbols(elf).items() if t == "b"), reverse=True)[:5]
    print(f"five largest .bss, head {shape} if{ifs}: " + ", ".join(f"{n} {s}" for s, n in bss))
r = symbols(images / "r4-endstation_ax7101_8x8-if2" / "ctrl_app.elf")
h = symbols(images / "head-endstation_ax7101_8x8-if2" / "ctrl_app.elf")
growth = sorted(((h.get(k, 0) - r.get(k, 0), k) for k in set(r) | set(h) if h.get(k, 0) != r.get(k, 0)), reverse=True)
by_type: dict[str, int] = {}
for dv, (_n, t) in growth:
    by_type[t] = by_type.get(t, 0) + dv
print("symbol growth at 8x8 if2, round 4 to head, by nm type: "
      + ", ".join(f"{t} {v:+}" for t, v in sorted(by_type.items())))
for dv, (n, t) in growth:
    print(f"  {dv:+6} {t} {n}")
