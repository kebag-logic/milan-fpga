#!/usr/bin/env python3
"""Run one owner control with every census pass slowed by DELAY seconds.

Usage: python3 -I slow_census.py SCRIPTS_DIR CONTROL DELAY

Each census pass of OwnedProcesses sleeps DELAY before scanning, so each pass
costs at least DELAY of wall time and min(DELAY, 0.5) s of the owner's clock.
Prints the control's outcome, its last words and its wall time; exit status is
the control's (0 green, 1 red).
"""
import inspect
import sys
import tempfile
import time
import traceback
from pathlib import Path

scripts = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(scripts))
import owned_process  # noqa: E402
import test_suite_cancellation as suite  # noqa: E402

control, delay = sys.argv[2], float(sys.argv[3])
real = owned_process.OwnedProcesses._descendants


def slow(self):
    time.sleep(delay)
    return real(self)


owned_process.OwnedProcesses._descendants = slow
began = time.monotonic()
try:
    function = getattr(suite, control)
    with tempfile.TemporaryDirectory(prefix="slow-census-") as scratch, owned_process.OwnedProcesses():
        function(*([Path(scratch)] if inspect.signature(function).parameters else []))
    status = 0
    print(f"{control} at {delay} s a pass: GREEN in {time.monotonic() - began:.1f} s", flush=True)
except BaseException as exc:  # noqa: BLE001 - the control's own failure is the result
    status = 1
    words = "".join(traceback.format_exception_only(type(exc), exc)).strip().splitlines()[-1][:400]
    print(f"{control} at {delay} s a pass: RED in {time.monotonic() - began:.1f} s: {words}", flush=True)
sys.exit(status)
