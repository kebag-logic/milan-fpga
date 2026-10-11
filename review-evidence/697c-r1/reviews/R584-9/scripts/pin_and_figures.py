"""R584-9: the boundary self-test's pin controls (every Makefile builder's bench arms included), its README figure
check and figure controls, and the census and Makefile findings, as ctrl_boundary.py --selftest runs them, without
the boundary's own capture and planted-defect campaign.
Usage: python3 -I pin_and_figures.py <checkout with tsn-c-stack at its gitlink> <work dir>"""
import sys
from pathlib import Path

root, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_boundary  # noqa: E402
from ctrl_configs import makefiles  # noqa: E402
from ctrl_pin import makefile_findings, pin_controls, proof_census  # noqa: E402

work.mkdir(parents=True, exist_ok=True)
print("makefiles:", [m.relative_to(root).as_posix() for m in makefiles()], flush=True)
(work / "pins").mkdir(exist_ok=True)
bad, pins = pin_controls(work / "pins", makefiles())
print(f"pin controls: {bad} misbehaved of {pins}", flush=True)
page = ctrl_boundary.README.read_text(encoding="utf-8")
counts = ctrl_boundary.population(pins)
print("population:", counts)
print("figure findings:", ctrl_boundary.figures(page, counts))
fbad, fcount = ctrl_boundary.figure_controls(page, counts)
print(f"figure controls: {fbad} misbehaved of {fcount}")
print("census findings:", proof_census())
print("makefile findings:", makefile_findings(makefiles(), work / "makefiles"))
