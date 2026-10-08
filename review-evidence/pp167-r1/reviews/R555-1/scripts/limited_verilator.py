#!/usr/bin/env python3
"""Limit simultaneous builds to two and compilation to four workers."""
import fcntl, os, pathlib, sys, time
packet=pathlib.Path(__file__).resolve().parents[1]
args=[]; old=iter(sys.argv[1:])
for arg in old:
    if arg in ("-j", "--jobs", "--build-jobs"): next(old); continue
    if arg.startswith("-j") and arg[2:].isdigit(): continue
    if arg.startswith("--jobs=") or arg.startswith("--build-jobs="): continue
    args.append(arg)
args += ["-j", "4"]
while True:
    for n in range(2):
        f=open(packet/"scratch"/f"build-slot-{n}.lock","w")
        try: fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError: f.close(); continue
        os.set_inheritable(f.fileno(),True)
        binary=os.environ.get("REVIEW_VERILATOR", "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator")
        os.execv(binary, ["verilator",*args])
    time.sleep(0.2)
