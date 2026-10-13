# Pin control runner: the head's own pin controls, census and figure checks, without the boundary build.
# Usage: python3 -I run_pin_controls.py <clone-root> <work-dir>
# Runs ctrl_pin.pin_controls exactly as ctrl_boundary.py --selftest does (same work layout), then the proof
# census and the README figure checks, and prints the counts. The Git is the first `git` on PATH.
import sys
from pathlib import Path

root, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_boundary  # noqa: E402
from ctrl_configs import makefiles  # noqa: E402
from ctrl_pin import pin_controls, proof_census  # noqa: E402
import ctrl_build  # noqa: E402

print(f"git: {ctrl_build.GIT}; python {sys.version.split()[0]}", flush=True)
(work / "pins").mkdir(parents=True)
misbehaved, pins = pin_controls(work / "pins", makefiles())
census = proof_census()
page = ctrl_boundary.README.read_text(encoding="utf-8")
stated = ctrl_boundary.figures(page, ctrl_boundary.population(pins))
fig_bad, fig_count = ctrl_boundary.figure_controls(page, ctrl_boundary.population(pins))
for line in census + stated:
    print(f"  [FAIL] {line}")
print(f"run_pin_controls: {pins} pin controls, {misbehaved} misbehaved; census {len(census)}; figures {len(stated)}; "
      f"figure controls {fig_count}, {fig_bad} misbehaved")
sys.exit(1 if misbehaved or census or stated or fig_bad else 0)
