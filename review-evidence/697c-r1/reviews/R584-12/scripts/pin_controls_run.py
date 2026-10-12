#!/usr/bin/env python3
"""R584-12: run the head's pin controls (ctrl_pin.pin_controls, every arm the boundary gate's --selftest runs as
its pin controls) alone, with the boundary gate's own list of Makefile builders.

Usage: python3 -I -B pin_controls_run.py <test-dir> <work-dir> [extra-sys-path]
(the extra path supplies PyYAML to an interpreter that lacks it)
"""
import sys
from pathlib import Path

test, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(test))
sys.path[1:1] = sys.argv[3:4]
import ctrl_boundary  # noqa: E402
import ctrl_pin  # noqa: E402

work.mkdir(parents=True, exist_ok=True)
bad, count = ctrl_pin.pin_controls(work, ctrl_boundary.makefiles())
print(f"PIN-CONTROLS {count} controls, {bad} misbehaved, python {sys.version.split()[0]}")
sys.exit(1 if bad else 0)
