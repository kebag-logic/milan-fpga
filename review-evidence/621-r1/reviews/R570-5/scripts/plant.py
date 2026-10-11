#!/usr/bin/env python3
"""Write a planted copy of the donor generator: plant.py <src> <dst> <name>."""
import sys
PLANTS = {
    # servo step no longer marks the outstanding request as crossing
    "no-step-flag": ("prog_leg_servo",
        '    p.emit("MOVE", rd=RT, ra=0, imm=1)\n    p.emit("WRST", ra=RT, imm=RG_SCR | S_PDSTEP, fmt=FMT_Q)\n', ""),
    # servo step resets the retained ratio instead of the rate window
    "ratio-not-window": ("prog_leg_servo",
        '    p.emit("WRST", ra=0, imm=RG_SCR | S_NR3, fmt=FMT_Q)\n',
        '    p.emit("WRST", ra=0, imm=RG_SCR | S_NRR, fmt=FMT_Q)\n'),
}
src, dst, name = sys.argv[1:4]
text = open(src).read()
scope, old, new = PLANTS[name]
start = text.index(f"\ndef {scope}(")
end = text.find("\ndef ", start + 1)
region = text[start:end]
if region.count(old) != 1:
    sys.exit(f"{name}: anchor not unique in {scope}")
open(dst, "w").write(text[:start] + region.replace(old, new) + text[end:])
print(f"planted {name} into {dst}")
