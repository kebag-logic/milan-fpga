"""R585-14: run the pin proof's own pin controls (ctrl_pin.pin_controls) alone, as ctrl_boundary.py --selftest runs
them, and print each verdict line and the totals.
usage: python3 -I r585_14_pin_controls.py <superproject-checkout> <empty-work-dir> [--only SUBSTRING]"""
import sys
from pathlib import Path

top, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(top / "sw/firmware/ctrl/test"))
sys.path.insert(1, str(top / "sw/firmware/gtest"))
import ctrl_boundary  # noqa: E402
import ctrl_pin  # noqa: E402

work.mkdir(parents=True, exist_ok=True)
bad, count = ctrl_pin.pin_controls(work, ctrl_boundary.makefiles())
print(f"PIN CONTROLS: {count} controls, {bad} misbehaved")
sys.exit(1 if bad else 0)
