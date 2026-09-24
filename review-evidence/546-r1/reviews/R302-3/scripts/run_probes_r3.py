#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Round R302-3 driver: the round-2 campaign, unchanged, at the round-3 head.

Usage: VERILATOR=<verilator 5.050> python3 run_probes_r3.py <clone> <packet>

probes/*.py|cpp and scripts/run_probes_r2.py are byte-identical to the R302-2
packet. This file only imports run_probes_r2 (which applies the round-2
expectation set) and retargets the head guard. No expectation is changed.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_probes_r2  # noqa: E402,F401  (applies the round-2 expectations)
rp = run_probes_r2.rp
rp.HEAD = "0c61d458941088f3847513b7c6fe6589c75b4270"

if __name__ == "__main__":
    raise SystemExit(rp.main())
