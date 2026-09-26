#!/usr/bin/env python3
"""Repeat a sim_pool test script under a chosen inherited signal state.

    bp_repeat.py SUITE_DIR SCRIPT MODE COUNT OUTDIR
MODE: default     - SIGINT/SIGTERM/SIGHUP at SIG_DFL, empty mask
      ign-int     - SIGINT inherited as SIG_IGN (the F2 condition)
      ign-all-blk - SIGINT/SIGTERM/SIGHUP inherited as SIG_IGN and blocked
Each run is a fresh exec of the script with that state inherited; the raw
output and exit of every run are kept; the summary is one JSON line per run.
"""
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

SUITE, SCRIPT, MODE, COUNT, OUT = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), Path(sys.argv[5])
SIGS = (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)


def state() -> None:
    for s in SIGS:
        signal.signal(s, signal.SIG_DFL)
    signal.pthread_sigmask(signal.SIG_SETMASK, set())
    if MODE == "ign-int":
        signal.signal(signal.SIGINT, signal.SIG_IGN)
    elif MODE == "ign-all-blk":
        for s in SIGS:
            signal.signal(s, signal.SIG_IGN)
        signal.pthread_sigmask(signal.SIG_BLOCK, set(SIGS))


OUT.mkdir(parents=True, exist_ok=True)
bad = 0
for k in range(1, COUNT + 1):
    t0 = time.monotonic()
    p = subprocess.run([sys.executable, SCRIPT], cwd=SUITE, capture_output=True,
                       text=True, preexec_fn=state)
    log = OUT / f"{MODE}-{k:02d}.log"
    log.write_text(p.stdout + p.stderr)
    lines = (p.stdout + p.stderr).strip().splitlines()
    fails = [l for l in lines if l.startswith("[FAIL]")]
    row = {"mode": MODE, "run": k, "exit": p.returncode, "last": lines[-1] if lines else "",
           "fail_lines": len(fails), "pass_lines": sum(l.startswith("[PASS]") for l in lines),
           "seconds": round(time.monotonic() - t0, 2)}
    bad += p.returncode != 0 or bool(fails)
    print(json.dumps(row), flush=True)
print(json.dumps({"mode": MODE, "runs": COUNT, "bad_runs": bad}))
sys.exit(1 if bad else 0)
