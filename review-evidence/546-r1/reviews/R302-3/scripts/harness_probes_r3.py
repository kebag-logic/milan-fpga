#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Round R302-3 driver: scripts/harness_probes.py (byte-identical to R302-2)
at the round-3 head. Only the head guard is retargeted.

Usage: VERILATOR=<verilator 5.050> python3 harness_probes_r3.py <clone> <packet>
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness_probes as hp  # noqa: E402
hp.HEAD = "0c61d458941088f3847513b7c6fe6589c75b4270"

if __name__ == "__main__":
    raise SystemExit(hp.main())
