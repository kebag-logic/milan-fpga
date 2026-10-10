#!/usr/bin/env python3
"""Write reviewer-owned planted copies of the donor microcode generator.

Usage: make_plants.py <generator.py> <out-dir>
Each plant edits one statement inside one named function, refusing if the
anchor is not unique inside that function.
"""
import sys
from pathlib import Path
src = Path(sys.argv[1]).read_text()
out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)

def in_function(text, func, old, new):
    start = text.index(f"def {func}(")
    end = text.index("\ndef ", start + 1)
    body = text[start:end]
    if body.count(old) != 1:
        raise SystemExit(f"{func}: anchor count {body.count(old)}")
    return text[:start] + body.replace(old, new) + text[end:]

plants = {
    # crossing exchange no longer marks the interval answered (liveness)
    "liveness-not-marked": ("prog_leg_pdepoch",
        '    p.emit("WRST", ra=RT, imm=RG_SCR | S_PDGOT, fmt=FMT_Q)\n', ""),
    # the step discards the retained neighbour rate ratio
    "drop-ratio-at-step": ("prog_leg_servo",
        '    p.emit("WRST", ra=0, imm=RG_SCR | S_NR3, fmt=FMT_Q)\n',
        '    p.emit("WRST", ra=0, imm=RG_SCR | S_NR3, fmt=FMT_Q)\n'
        '    p.emit("WRST", ra=0, imm=RG_SCR | S_NRR, fmt=FMT_Q)\n'),
    # the step never marks the outstanding exchange as crossing
    "step-not-flagged": ("prog_leg_servo",
        '    p.emit("WRST", ra=RT, imm=RG_SCR | S_PDSTEP, fmt=FMT_Q)\n', ""),
}
for name, (func, old, new) in plants.items():
    (out / f"gen_{name}.py").write_text(in_function(src, func, old, new))
    print("wrote", name)
