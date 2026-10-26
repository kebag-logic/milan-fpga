#!/usr/bin/env python3
"""Probe: the linked-image receipt. For each point, the base's and the head's
split plan (rom and sram need, tiles against the 56-RAMB36 budget, or the
planner's refusal), the delta, the five largest .bss objects of the head, and
at the largest point the per-symbol growth from base to head.

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
REFUSED = re.compile(r"(\d+) RAMB36 \(rom (\d+) bytes in (\d+), sram (\d+) bytes in (\d+)\)")


def plan(label: str, shape: str, ifs: int) -> dict:
    """The plan's figures, from its JSON or from the planner's refusal."""
    text = (images / f"{label}-{shape}-if{ifs}.plan.txt").read_text()
    try:
        d = json.loads(text)
        return {"rom": d["rom"]["bytes"], "sram": d["sram"]["bytes"], "tiles": d["tiles"], "refused": ""}
    except json.JSONDecodeError:
        m = REFUSED.search(text)
        return {"rom": int(m.group(2)), "sram": int(m.group(4)), "tiles": float(m.group(1)),
                "refused": text.strip()}


def symbols(elf: Path) -> dict:
    """(name, type) -> size of every sized symbol."""
    out = subprocess.run([nm, "-S", "--size-sort", str(elf)], capture_output=True, text=True, check=True).stdout
    return {(p[3], p[2].lower()): int(p[1], 16) for p in (ln.split() for ln in out.splitlines()) if len(p) == 4}


print("linked image, ctrl_srp_image.py --with-aecp --layout split; ctrl_memory.py plan; budget 56 RAMB36")
print(f"{'point':34} {'base rom':>9} {'head rom':>9} {'delta':>7} {'base sram':>9} {'head sram':>9} {'delta':>6}"
      f" {'base tiles':>10} {'head tiles':>10}")
for shape, ifs in POINTS:
    b, h = plan("base", shape, ifs), plan("head", shape, ifs)
    print(f"{shape + ' if' + str(ifs):34} {b['rom']:>9} {h['rom']:>9} {h['rom'] - b['rom']:>+7} {b['sram']:>9}"
          f" {h['sram']:>9} {h['sram'] - b['sram']:>+6} {b['tiles']:>10} {h['tiles']:>10}")
    for which, p in (("base", b), ("head", h)):
        if p["refused"]:
            print(f"  {which}: {p['refused']}")
for shape, ifs in POINTS:
    elf = images / f"head-{shape}-if{ifs}" / "ctrl_app.elf"
    bss = sorted(((s, n) for (n, t), s in symbols(elf).items() if t == "b"), reverse=True)[:5]
    print(f"five largest .bss, head {shape} if{ifs}: " + ", ".join(f"{n} {s}" for s, n in bss))
b = symbols(images / "base-endstation_ax7101_8x8-if2" / "ctrl_app.elf")
h = symbols(images / "head-endstation_ax7101_8x8-if2" / "ctrl_app.elf")
growth = sorted(((h.get(k, 0) - b.get(k, 0), k) for k in set(b) | set(h) if h.get(k, 0) != b.get(k, 0)), reverse=True)
by_type: dict[str, int] = {}
for dv, (_n, t) in growth:
    by_type[t] = by_type.get(t, 0) + dv
print("symbol growth at 8x8 if2, base to head, by nm type: " + ", ".join(f"{t} {v:+}" for t, v in sorted(by_type.items())))
for dv, (n, t) in growth:
    print(f"  {dv:+6} {t} {n}")
