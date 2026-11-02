#!/usr/bin/env python3
"""Time the empty-listing verdict at production constants (no resume).

usage: probe_vanish.py SCRIPTS_DIR. Run inside a PID namespace.
"""
import os, sys, time
sys.path.insert(0, sys.argv[1])
import owned_process
owner = owned_process.OwnedProcesses()
with owner:
    gone = 2 ** 22 + 1
    owner._descendants = lambda: {gone: (os.getpid(), "0")}
    owner._reap = lambda: {gone}
    began = time.monotonic()
    try:
        owner._cleanup()
        print("no verdict")
    except RuntimeError as exc:
        print(f"empty-listing verdict after {time.monotonic() - began:.2f} s: {str(exc)[:160]}")
    owner._descendants = owner.__class__._descendants.__get__(owner)
    owner._reap = owner.__class__._reap.__get__(owner)
