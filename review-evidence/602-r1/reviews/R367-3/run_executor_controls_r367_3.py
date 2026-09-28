#!/usr/bin/env python3
"""R367-3: run the candidate's own gmstep_mutants.py runner, restricted to the
five option-off controls and the coincident-suppression control, in a
disposable copy of the candidate. Usage: python3 run_executor_controls_r367_3.py <tree>
PATH must name the pinned Verilator 5.050."""
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "tb/verilator/milan_dp"))
import gmstep_mutants as g  # noqa: E402

g.CONTROLS = [c for c in g.CONTROLS if c.leg == "option-off" or c.name.startswith("a PHC step suppresses")]
print(f"[INFO] running {len(g.CONTROLS)} controls: " + "; ".join(c.name for c in g.CONTROLS))
sys.argv = [sys.argv[0], "--all"]
sys.exit(g.main())
