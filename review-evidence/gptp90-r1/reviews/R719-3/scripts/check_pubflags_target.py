#!/usr/bin/env python3
"""Load the generator at <src>/hdl/ucode, build the shipping image, and show
that SRTO's final BR targets PDPAIR's flags write, followed only by COMMIT
and END; also tabulate the gmPresent compare for every priority1/clockClass."""
import importlib.util, sys
src = sys.argv[1]
spec = importlib.util.spec_from_file_location("g", f"{src}/hdl/ucode/gen_gptp_ucode.py")
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
g.set_runtime(2_000_000) if hasattr(g, "set_runtime") else None
try:
    g.build(0x02A1B2C3D4E5)
except TypeError:
    pass
pp = g.prog_leg_pdpair(g.LB["PDPAIR"])
tail = [it for it in pp.items if it[0] != "label"]
addr = pp.address("pubflags")
print("PDPAIR", g.LB["PDPAIR"], "pubflags", addr, "LB[PUBFLAGS]", g.LB["PUBFLAGS"])
n_before = addr - pp.base
print("tail ops from pubflags:", [it[0] for it in tail[n_before:]],
      [it[1].get("imm") for it in tail[n_before:]])
sp = g.prog_leg_srto(g.LB["SRTO"])
ops = [it for it in sp.items if it[0] != "label"]
print("SRTO", g.LB["SRTO"], "words", len(ops), "last:", ops[-1][0], ops[-1][2])
assert ops[-1][2] == addr and tail[n_before][0] == "WRST" and tail[n_before][1]["imm"] == (g.RG_PUB | 2)
assert [it[0] for it in tail[n_before:]] == ["WRST", "COMMIT", "END"]
M = g.SRTO_PASSED_C
bad = 0
for p1 in range(256):
    for cc in range(256):
        v = (p1 << 56) | (cc << 48)
        aged = (v >> 53) < M
        if aged != (p1 < 255): bad += 1
print(f"mark=0x{M:X} flagmask-overlap=0x{M & 0xF:X} (FL_SYNCOK=0x{g.FL_SYNCOK_C:X}) "
      f"compare mismatches over 65536 (p1,class)={bad}")
print("bits cleared by MASK on an unaged elected-peer expiry: 0x%X; defined flag bits 0x%X"
      % (M, g.FL_PRESENT_C | g.FL_AMGM_C | g.FL_ASCAP_C | g.FL_SYNCOK_C))
sys.exit(1 if bad else 0)
