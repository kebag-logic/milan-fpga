#!/usr/bin/env python3
"""Run one owner control from a (possibly mutated) copy of the sweep test.

Usage: run_control.py SCRIPTS_DIR CONTROL   (CONTROL is an owner_* function name)
Prints CONTROL PASS or CONTROL FAIL <exception>; exit 0 or 1. Run it inside its
own PID namespace so nothing it plants can outlive it.
"""
import sys, tempfile, time, traceback
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import test_suite_cancellation as t
from owned_process import OwnedProcesses
name = sys.argv[2]
start = time.monotonic()
try:
    with tempfile.TemporaryDirectory(prefix="r763-ctl-") as scratch:
        with OwnedProcesses():
            fn = getattr(t, name)
            fn() if name == "owner_vanishing" else fn(Path(scratch))
except BaseException as exc:
    traceback.print_exc()
    print(f"{name} FAIL {time.monotonic() - start:.1f}s {type(exc).__name__}: {str(exc)[:400]}", flush=True)
    sys.exit(1)
print(f"{name} PASS {time.monotonic() - start:.1f}s", flush=True)
