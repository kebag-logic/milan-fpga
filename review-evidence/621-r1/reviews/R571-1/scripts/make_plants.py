#!/usr/bin/env python3
"""Write reviewer-planted variants of the donor microcode generator.

Usage: make_plants.py <generator.py> <out-dir>
Each plant replaces exactly one unique anchor; a non-unique anchor aborts.
"""
import sys
from pathlib import Path

PLANTS = {
    # deferred-t1 completion bypasses the epoch gate (pre-fix routing)
    "r571-deferred-bypass": (
        '    p.emit("RDST", rd=RC, imm=RG_SCR | S_T3, fmt=FMT_Q)\n    p.emit("BR", label=LB["PDEPOCH"])\n',
        '    p.emit("RDST", rd=RC, imm=RG_SCR | S_T3, fmt=FMT_Q)\n    p.emit("BR", label=LB["PDPAIR"])\n'),
    # in-order Follow_Up completion bypasses the epoch gate
    "r571-followup-bypass": (
        '    _pdpost_defer_until_t1(p)\n    p.emit("BR", label=LB["PDEPOCH"])\n',
        '    _pdpost_defer_until_t1(p)\n    p.emit("BR", label=LB["PDPAIR"])\n'),
    # a crossing exchange no longer counts as an answered request
    "r571-no-liveness": (
        '    p.emit("WRST", ra=RT, imm=RG_SCR | S_PDGOT, fmt=FMT_Q)\n    p.emit("END")\n    return p\n\n\ndef prog_leg_pdpair',
        '    p.emit("END")\n    return p\n\n\ndef prog_leg_pdpair'),
    # the servo step no longer marks the outstanding exchange
    "r571-step-unmarked": (
        '    p.emit("MOVE", rd=RT, ra=0, imm=1)\n    p.emit("WRST", ra=RT, imm=RG_SCR | S_PDSTEP, fmt=FMT_Q)\n',
        ''),
}

src = Path(sys.argv[1]).read_text()
out = Path(sys.argv[2])
for name, (old, new) in PLANTS.items():
    if src.count(old) != 1:
        sys.exit(f"{name}: anchor count {src.count(old)} != 1")
    d = out / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "gen_gptp_ucode.py").write_text(src.replace(old, new, 1))
    print(f"wrote {name}")
