#!/usr/bin/env python3
"""Run a tree's own pin controls (ctrl_pin.pin_controls over ctrl_configs.makefiles()) and its census.
usage: pin_controls.py <tree root> <work dir>"""
import sys
from pathlib import Path
root, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path[:0] = [str(root / "sw/firmware/ctrl/test"), str(root / "sw/firmware/gtest")]
import ctrl_configs, ctrl_pin  # noqa: E401,E402
work.mkdir(parents=True, exist_ok=True)
census = ctrl_pin.proof_census()
print(f"proof census findings: {len(census)}")
for line in census:
    print("  ", line)
bad, count = ctrl_pin.pin_controls(work, ctrl_configs.makefiles())
print(f"pin controls: {count}, misbehaved: {bad}")
sys.exit(1 if bad or census else 0)
