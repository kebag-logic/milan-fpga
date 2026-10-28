#!/usr/bin/env python3
"""Reviewer probe: run tb/verilator/mbx/mutants.py's own controls and machinery
on the contract 2.3 source-entry arms only (every arm whose name carries
"pub-src", and the hole arm whose anchor the change rewrote), plus one
reviewer arm the campaign does not plant: DA_GATE's write losing its
"not a source entry" guard, so a write of source 0's SRC_SID_LO (entry
register 0x0, the same in-block register offset as DA_GATE) would also open
or close the talker gates. Any named failure counts for the reviewer arm.

Run from tb/verilator/mbx of a disposable clone:
    python3 -I /path/to/mbx_src_probe.py --jobs 6
"""
import os
import sys

sys.path.insert(0, os.getcwd())
import mutants as m  # noqa: E402

keep = tuple(a for a in m.ARMS if "pub-src" in a.name or "pub-hole-aliases" in a.name)
GUARD = "      if (!pub_src_w && !pub_sink_w && pub_reg_w == AW2_C'(MBX_PUB_REG_DA_GATE_C))\n"
reviewer = tuple(
    m.Arm(f"reviewer-da-gate-src-guard-dropped{'-axil' if h else ''}", "KL_mbx.sv", GUARD,
          GUARD.replace("!pub_src_w && ", ""), h, "", 1)
    for h in (0, 1))
m.ARMS = keep + reviewer
print(f"reviewer selection: {len(m.ARMS)} arm(s): " + ", ".join(a.name for a in m.ARMS))
sys.exit(m.main(sys.argv[1:]))
