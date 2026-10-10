#!/usr/bin/python3
"""Admit at most two Verilator builds at once across this lane; cap each at four make jobs."""
import fcntl
import subprocess
import sys
import time
from pathlib import Path

REAL = {"bin5052": "/usr/bin/verilator",
        "bin5050": "$TOOLS/pinned-verilator-5.050/verilator"}[Path(sys.argv[0]).resolve().parent.name]
args = sys.argv[1:]
building = "--build" in args or any(a.startswith("--build-jobs") for a in args)
for i, arg in enumerate(args[:-1]):
    if arg in ("-j", "--build-jobs") and args[i + 1].isdigit() and int(args[i + 1]) > 4:
        args[i + 1] = "4"
for i, arg in enumerate(args):
    if arg.startswith("-j") and arg[2:].isdigit() and int(arg[2:]) > 4:
        args[i] = "-j4"
held = None
if building:
    slots = [open(f"$SCRATCH/locks/build-slot-{i}.lock", "a") for i in range(2)]
    while held is None:
        for slot in slots:
            try:
                fcntl.flock(slot, fcntl.LOCK_EX | fcntl.LOCK_NB)
                held = slot
                break
            except BlockingIOError:
                pass
        if held is None:
            time.sleep(0.5)
sys.exit(subprocess.call([REAL, *args]))
