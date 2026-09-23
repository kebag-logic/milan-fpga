#!/usr/bin/env python3
"""Reviewer probe: emulate a host whose C library has no prctl symbol (as on
non-Linux hosts) and run the owner's CLI; record exit status and last line.
Usage: probe_unsupported_platform.py REPO_COPY
"""
import ctypes, runpy, sys
repo = sys.argv[1]
class NoPrctl:
    def __getattr__(self, name):
        raise AttributeError(f"symbol not found: {name}")
ctypes.CDLL = lambda *a, **k: NoPrctl()
sys.argv = ["owned_process.py", "--", "true"]
runpy.run_path(f"{repo}/scripts/owned_process.py", run_name="__main__")
