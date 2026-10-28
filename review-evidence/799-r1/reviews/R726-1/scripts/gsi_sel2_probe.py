#!/usr/bin/env python3
"""Reviewer probe: plant a selector-2-only pass-through of processor #206's
unsettled gate (the one arm gsi_mutants.py does not plant alone) and require
milan_dp [GSI] G11's stale-ID stream_id check to fail by name.

Run from tb/verilator/milan_dp of a disposable clone, after `make notify`:
    python3 /path/to/gsi_sel2_probe.py
It reuses gsi_mutants.py's own build/run/verdict machinery unchanged.
"""
import os
import sys

sys.path.insert(0, os.getcwd())
import gsi_mutants as g  # noqa: E402

SEL2 = "          4'd2: aecp_gsi_data_w = 64'd0;"
g.MUTATIONS[:] = [
    ("reviewer probe: the processor passes selector 2 alone through while unsettled (#790)",
     [("pp", SEL2, "          4'd2: begin end")],
     g.G11_STALE + ": stream_id is zero"),
]
sys.argv = [sys.argv[0]]
sys.exit(g.main())
