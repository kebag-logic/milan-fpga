#!/usr/bin/env python3
"""Reviewer runner: one named owner control from SCRIPTS_DIR/test_suite_cancellation.py.

usage: run_control.py SCRIPTS_DIR CONTROL
"""
import inspect, sys, tempfile, time, traceback
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import test_suite_cancellation as t  # noqa: E402
fn = getattr(t, sys.argv[2])
began = time.monotonic()
try:
    with tempfile.TemporaryDirectory(prefix="r763-3-ctl-") as scratch:
        fn() if not inspect.signature(fn).parameters else fn(Path(scratch))
except BaseException as exc:
    traceback.print_exc()
    print(f"{sys.argv[2]} FAIL {time.monotonic() - began:.1f}s {type(exc).__name__}: {exc}", flush=True)
    sys.exit(1)
print(f"{sys.argv[2]} PASS {time.monotonic() - began:.1f}s", flush=True)
