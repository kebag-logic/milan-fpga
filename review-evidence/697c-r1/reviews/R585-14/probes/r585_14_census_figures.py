"""R585-14: the pin proof's census (ctrl_pin.proof_census) and the README's figures checked against a pin-control count.
usage: python3 -I r585_14_census_figures.py <superproject-checkout> <pin-control-count>"""
import sys
from pathlib import Path

top = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(top / "sw/firmware/ctrl/test"))
sys.path.insert(1, str(top / "sw/firmware/gtest"))
import ctrl_boundary  # noqa: E402

census = ctrl_boundary.proof_census()
print(f"census findings: {len(census)}", *census, sep="\n  ")
page = ctrl_boundary.README.read_text(encoding="utf-8")
counts = ctrl_boundary.population(int(sys.argv[2]))
print("population:", counts)
stated = ctrl_boundary.figures(page, counts)
print(f"figure findings: {len(stated)}", *stated, sep="\n  ")
bad, n = ctrl_boundary.figure_controls(page, counts)
print(f"figure controls: {n}, misbehaved {bad}")
sys.exit(1 if census or stated or bad else 0)
