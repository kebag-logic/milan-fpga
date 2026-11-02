#!/usr/bin/env python3
"""usage: under.py <spinners|ccN> -- COMMAND ...  Scratch only. Runs COMMAND under make -j load in this unit's own CPU
affinity; the load gets its own session and is stopped only by killing that process group."""
import os, signal, subprocess, sys, time
from pathlib import Path
kind, here = sys.argv[1], Path(__file__).resolve().parent
assert sys.argv[2] == "--"
if kind.startswith("cc"):
    argv = ["make", "-s", "-f", "compile.mk", "-j", kind[2:], f"N={kind[2:]}"]
else:
    argv = ["make", "-s", "-j", kind, f"N={kind}"]
load = None
if kind not in ("0", "cc0"):
    load = subprocess.Popen(argv, cwd=here, start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(4)
try:
    rc = subprocess.run(sys.argv[3:]).returncode
finally:
    if load is not None:
        os.killpg(load.pid, signal.SIGKILL)
        load.wait()
sys.exit(rc)
