#!/usr/bin/env python3
"""Run a tree's owner_shell_window with every census pass slowed, as a starved owner's are.

Usage: python3 -I slow_census_probe.py <tree> <seconds added to each census pass>
The product's own comment (owned_process.py:41-42) records 1.75 s a pass at 16
runnable tasks per CPU. Exit 0 if the control passes, 1 with its error otherwise.
"""
import sys
import tempfile
import time
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]) / "scripts"))
import test_suite_cancellation as t  # noqa: E402
from owned_process import OwnedProcesses  # noqa: E402

delay = float(sys.argv[2])
real = OwnedProcesses._descendants


def slow(self):
    """One census pass that takes `delay` longer, as under host load."""
    time.sleep(delay)
    return real(self)


OwnedProcesses._descendants = slow
began = time.monotonic()
with tempfile.TemporaryDirectory(prefix="slow-census-") as scratch:
    try:
        with OwnedProcesses():
            OwnedProcesses._descendants = slow
            t.owner_shell_window(Path(scratch))
        status = 0
        print(f"delay {delay}: owner_shell_window PASS in {time.monotonic() - began:.1f} s")
    except Exception as exc:  # report any failure of the control
        OwnedProcesses._descendants = real
        print(f"delay {delay}: owner_shell_window FAIL in {time.monotonic() - began:.1f} s: "
              f"{type(exc).__name__}: {str(exc)[:400]}")
        traceback.print_exc(limit=3)
        status = 1
sys.exit(status)
