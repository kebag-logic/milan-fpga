#!/usr/bin/env python3
"""follow_ring's mutants.py for a subset, its builds capped at -j8 and two Verilator jobs."""
import subprocess
import sys
sys.path.insert(0, "$LANES/632-phase/tb/verilator/follow_ring")
import mutants as m  # noqa: E402
_run = subprocess.run
def capped(cmd, *a, **k):
    if cmd and cmd[0] == "make":
        cmd = ["-j8" if x == "-j16" else "VERILATOR_JOBS=2" if x == "VERILATOR_JOBS=16" else x for x in cmd]
    return _run(cmd, *a, **k)
m.subprocess.run = capped
sys.argv = ["mutants.py", *sys.argv[1:]]
sys.exit(m.main())
