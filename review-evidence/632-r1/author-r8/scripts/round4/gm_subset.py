#!/usr/bin/env python3
"""Run a named subset of gmstep_mutants.CONTROLS through its own main()."""
import sys
sys.path.insert(0, "$LANES/632-phase/tb/verilator/milan_dp_gm_steps")
import gmstep_mutants as g  # noqa: E402
names = set(sys.argv[1:])
g.CONTROLS = [c._replace(acceptance=True) for c in g.CONTROLS if c.name in names]
assert len(g.CONTROLS) == len(names), [c.name for c in g.CONTROLS]
sys.argv = ["gmstep_mutants.py", "--no-small-steps"]
sys.exit(g.main())
