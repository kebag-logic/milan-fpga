"""Run every tsn-c-stack pin control of a checkout, with the proof census and the README figure check.

Usage: python3 -I run_pins.py <checkout> <work-dir>
The Git the proof runs is the first `git` on PATH (ctrl_build.GIT), so prepend a PATH entry to select one.
Prints each control's verdict line, then one summary line:
  PINS controls=<n> misbehaved=<n> census=<n> figures_stated=<n> figure_misbehaved=<n>/<n> git=<version>
Exit 0 only when every count of failures is zero.
"""
import subprocess
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
import ctrl_boundary  # noqa: E402
import ctrl_build  # noqa: E402
from ctrl_configs import makefiles  # noqa: E402
from ctrl_pin import pin_controls, proof_census  # noqa: E402

version = subprocess.run([ctrl_build.GIT, "--version"], capture_output=True, text=True, check=True).stdout.strip()
print(f"git program {ctrl_build.GIT}: {version}; python {sys.version.split()[0]}", flush=True)
work.mkdir(parents=True, exist_ok=False)
bad, pins = pin_controls(work, makefiles())
page = ctrl_boundary.README.read_text(encoding="utf-8")
counts = ctrl_boundary.population(pins)
stated = ctrl_boundary.figures(page, counts)
fbad, fcount = ctrl_boundary.figure_controls(page, counts)
census = proof_census()
for line in census + stated:
    print(f"  [FAIL] {line}")
print(f"PINS controls={pins} misbehaved={bad} census={len(census)} figures_stated={len(stated)} "
      f"figure_misbehaved={fbad}/{fcount} git={version}", flush=True)
sys.exit(0 if not (bad or census or stated or fbad) else 1)
