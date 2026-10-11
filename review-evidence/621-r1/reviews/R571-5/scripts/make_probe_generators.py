#!/usr/bin/env python3
"""Write mutated copies of the donor gPTP microcode generator for review probes.

usage: make_probe_generators.py <head generator> <output directory>
Each mutation must match its anchor exactly once, or the script stops.
"""
import sys
from pathlib import Path

src = Path(sys.argv[1]).read_text()
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)

STEP_NR3 = '    p.emit("WRST", ra=0, imm=RG_SCR | S_NR3, fmt=FMT_Q)\n    p.emit("MOVE", rd=RT, ra=0, imm=1)\n'
# The ROM has no free packed word. Room-making for one probe: the Follow_Up
# portNumber hardening check (four words), which no step arm exercises; its
# removal alone is run as a positive control ("room-control").
ROOM_OLD = ('    p.emit("RDST", rd=RT, imm=RG_BANK | 7, fmt=FMT_Q)\n'
            '    p.emit("CMP", ra=RT, rb=0, fmt=FMT_W, imm=OUR_PORTNUM_C)\n'
            '    p.emit("BRS", cnd=BRS_Z, label="fu_pn")\n'
            '    p.emit("END")\n'
            '    p.label("fu_pn")\n')
if src.count(ROOM_OLD) != 1:
    sys.exit("room anchor not unique")
room = src.replace(ROOM_OLD, "")
# ... and the cease-resume leg's body (seven words): one responder never
# engages the Milan cease rule in the step regression.
RESUME_OLD = ('    p.emit("WRST", ra=0, imm=RG_SCR | S_CEASE, fmt=FMT_Q)\n'
              '    p.emit("WRST", ra=0, imm=RG_SCR | S_MULTI, fmt=FMT_Q)\n'
              '    p.emit("WRST", ra=0, imm=RG_SCR | S_IVMULTI, fmt=FMT_Q)\n'
              '    p.emit("WRST", ra=0, imm=RG_SCR | S_RSP1, fmt=FMT_Q)\n'
              '    p.emit("WRST", ra=0, imm=RG_SCR | S_PDLOST, fmt=FMT_Q)\n'
              '    p.emit("MOVE", rd=RT, ra=0, imm=1)\n'
              '    p.emit("WRST", ra=RT, imm=RG_SCR | S_PDGOT, fmt=FMT_Q)\n'
              '    p.emit("END")\n    return p\n')
if room.count(RESUME_OLD) != 1:
    sys.exit("resume anchor not unique")
room = room.replace(RESUME_OLD, '    p.emit("END")\n    return p\n')
(out / "room-control.py").write_text(room)
print("wrote room-control")
MUTANTS = {
    # A re-seeded rate window (S_NR3 zero, which a step forces) also discards
    # the retained neighbour rate ratio, so the first clean exchange after a
    # step computes an uncorrected delay. SERVO's home has no free word, so
    # the plant sits on the window's first-exchange branch.
    "zero-nrr-at-step": (
        '    p.emit("BRS", cnd=BRS_Z, label="save")           # first exchange\n',
        '    p.emit("BRS", cnd=BRS_Z, label="r571_first")\n'),
    # The servo never marks the outstanding request as stepped.
    "no-pdstep-set": ('    p.emit("WRST", ra=RT, imm=RG_SCR | S_PDSTEP, fmt=FMT_Q)\n    # the rate estimate',
                      '    # the rate estimate'),
    # The crossing exchange restarts the capability ladder.
    "crossing-resets-ladder": ('    p.emit("WRST", ra=RT, imm=RG_SCR | S_PDGOT, fmt=FMT_Q)\n    p.emit("END")\n    return p\n\n\ndef prog_leg_pdpair',
                               '    p.emit("WRST", ra=RT, imm=RG_SCR | S_PDGOT, fmt=FMT_Q)\n'
                               '    p.emit("WRST", ra=0, imm=RG_SCR | S_PDOK, fmt=FMT_Q)\n'
                               '    p.emit("END")\n    return p\n\n\ndef prog_leg_pdpair'),
}
for name, (old, new) in MUTANTS.items():
    base = room if name == "zero-nrr-at-step" else src
    if base.count(old) != 1:
        sys.exit(f"{name}: anchor matched {base.count(old)} times")
    text = base.replace(old, new)
    if name == "zero-nrr-at-step":
        tail = ('    p.label("save")\n'
                '    p.emit("WRST", ra=RC, imm=RG_SCR | S_NR3, fmt=FMT_Q)\n')
        if text.count(tail) != 1:
            sys.exit("zero-nrr-at-step: tail anchor not unique")
        text = text.replace(tail, '    p.BR_SAVE_PLACEHOLDER\n' + tail)
        text = text.replace('    p.BR_SAVE_PLACEHOLDER\n',
                            '    p.emit("BR", label="save")\n'
                            '    p.label("r571_first")\n'
                            '    p.emit("WRST", ra=0, imm=RG_SCR | S_NRR, fmt=FMT_Q)\n')
    (out / f"{name}.py").write_text(text)
    print(f"wrote {name}")
