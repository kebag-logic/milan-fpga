#!/usr/bin/env python3
"""Run r3_cluster_probe FB/SB/CF/CB, r3_arm_void_probe, and r4_probe X/C plus 1500 R cases on one planner.

Usage: python3 -I r4_mutant_probe_groups.py <path-to-tb/tools> <scripts dir> [jobs]
"""
import sys
from multiprocessing import get_context

TOOLS, HERE = sys.argv[1], sys.argv[2]
JOBS = int(sys.argv[3]) if len(sys.argv) > 3 else 2
sys.path.insert(0, HERE)
sys.argv = [sys.argv[0], TOOLS, HERE, str(JOBS)]
import r4_probe as q  # noqa: E402

q.run("X", q.case_x, q.x_cases())
q.run("C", q.case_c, q.c_cases())
q.run("R", q.case_r, q.r_cases(1500, 396004))
sys.argv = [sys.argv[0], TOOLS, HERE, str(JOBS)]
import r3_cluster_probe as cl  # noqa: E402
cl.main()
sys.argv = [sys.argv[0], TOOLS, HERE, str(JOBS)]
import r3_arm_void_probe as av  # noqa: E402
av.main()
