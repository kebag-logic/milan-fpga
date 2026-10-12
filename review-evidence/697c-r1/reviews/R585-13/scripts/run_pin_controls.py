#!/usr/bin/env python3
"""Run only the pin controls (ctrl_pin.pin_controls), the proof census and the README figure check of a
milan-fpga checkout whose tsn-c-stack submodule is initialised, without the boundary gate's builds.

usage: run_pin_controls.py <checkout> <empty work dir> [extra import dir, e.g. a pure-Python PyYAML]
Prints every control's verdict line, then a summary; exit 0 only when no control misbehaved, the census is
clean and the README's figures equal the self-test's counts.
"""
import sys
from pathlib import Path

repo, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
sys.path.insert(1, str(repo / "sw/firmware/gtest"))
if len(sys.argv) > 3:
    sys.path.append(str(Path(sys.argv[3]).resolve()))

import ctrl_boundary  # noqa: E402
from ctrl_configs import makefiles  # noqa: E402
from ctrl_pin import pin_controls, proof_census  # noqa: E402

work.mkdir(parents=True, exist_ok=False)
(work / "pins").mkdir()
census = proof_census()
for line in census:
    print(f"  [CENSUS] {line}")
bad, pins = pin_controls(work / "pins", makefiles())
page = ctrl_boundary.README.read_text(encoding="utf-8")
stated = ctrl_boundary.figures(page, ctrl_boundary.population(pins))
fbad, fcount = ctrl_boundary.figure_controls(page, ctrl_boundary.population(pins))
for line in stated:
    print(f"  [FIGURE] {line}")
print(f"SUMMARY pin controls {pins}, misbehaved {bad}; census findings {len(census)}; figure findings "
      f"{len(stated)}; figure controls {fcount}, misbehaved {fbad}")
sys.exit(0 if not (bad or census or stated or fbad) else 1)
