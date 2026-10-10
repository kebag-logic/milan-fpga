#!/usr/bin/env python3
"""Write reviewer-derived planted copies of the donor microcode generator.

Usage: make_plants.py <generator.py> <out-dir>

Each plant changes exactly one anchor, which must be unique in its scope.
The copies are run through tb/verilator/gptp_plane/phc_step.py --generator,
so the parent harness and RTL are unchanged.
"""
import sys
from pathlib import Path

CREDIT = '    p.emit("WRST", ra=RT, imm=RG_SCR | S_PDGOT, fmt=FMT_Q)\n'
THRESH = '    p.emit("CMP", ra=RB, rb=0, fmt=FMT_D, imm=LOST_N_C + 1)\n'

PLANTS = {
    # Delete the crossing exchange's liveness credit (reviewer derivation of
    # both review rounds' deletion plants: the only S_PDGOT write in PDEPOCH).
    "rv-credit-deleted": ("prog_leg_pdepoch", CREDIT, ""),
    # Credit written as zero: liveness never recorded, line kept.
    "rv-credit-zero": ("prog_leg_pdepoch", CREDIT,
                       '    p.emit("WRST", ra=0, imm=RG_SCR | S_PDGOT, fmt=FMT_Q)\n'),
    # Loss threshold one early (third unanswered) and one late (fifth).
    "rv-threshold-third": ("_tmr_pdelay_request", THRESH,
                           THRESH.replace("LOST_N_C + 1", "LOST_N_C")),
    "rv-threshold-fifth": ("_tmr_pdelay_request", THRESH,
                           THRESH.replace("LOST_N_C + 1", "LOST_N_C + 2")),
}


def plant(source: str, scope: str, old: str, new: str) -> str:
    start = source.index(f"\ndef {scope}(")
    end = source.find("\ndef ", start + 1)
    end = len(source) if end < 0 else end
    region = source[start:end]
    if region.count(old) != 1:
        raise SystemExit(f"anchor not unique in {scope}")
    return source[:start] + region.replace(old, new) + source[end:]


def main() -> None:
    generator, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    source = generator.read_text()
    for name, (scope, old, new) in PLANTS.items():
        text = plant(source, scope, old, new)
        assert text != source
        (out / f"{name}.py").write_text(text)
        print(name, "written")


if __name__ == "__main__":
    main()
