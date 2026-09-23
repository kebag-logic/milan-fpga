#!/usr/bin/env python3
"""Simulate hosts lacking the owner's process facilities and report how the
production owner entry point exits (documented: refused before commands start).
Usage: probe_unsupported.py <checkout> <no-prctl|no-pidfd|prctl-fails>"""
import ctypes, os, runpy, sys
checkout, mode = sys.argv[1], sys.argv[2]
marker = os.path.join(os.environ["TMPDIR"], "command-started-" + mode)
if mode == "no-prctl":
    class NoPrctl:  # a C library without prctl, as on non-Linux hosts
        pass
    ctypes.CDLL = lambda *a, **k: NoPrctl()
elif mode == "no-pidfd":
    del os.pidfd_open
elif mode == "prctl-fails":
    class Failing:
        def prctl(self, *a):
            return -1
    ctypes.CDLL = lambda *a, **k: Failing()
sys.argv = ["owned_process.py", "--", "touch", marker]
try:
    runpy.run_path(os.path.join(checkout, "scripts/owned_process.py"), run_name="__main__")
except SystemExit as exc:
    print(f"{mode}: exit={exc.code} command_started={os.path.exists(marker)}")
    raise
