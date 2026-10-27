#!/usr/bin/env python3
"""Run only r4_probe's seeded fuzz group R (6000 cases, seed 396004) unchanged.

Usage: python3 -I r_only.py <tools> <dir holding the reviewer's r3_probe.py and r4_probe.py> [jobs]
"""
import sys
TOOLS, HERE = sys.argv[1], sys.argv[2]
JOBS = sys.argv[3] if len(sys.argv) > 3 else "8"
sys.path.insert(0, HERE)
sys.argv = [sys.argv[0], TOOLS, HERE, JOBS]
import r4_probe as q
q.run("R", q.case_r, q.r_cases(6000, 396004))
