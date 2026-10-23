#!/usr/bin/env python3
"""tdm8_render_mutants.py for a named subset of MUTATIONS (clean legs, positive
controls and leg defects as the file runs them; the shape clean controls skipped)."""
import sys
sys.path.insert(0, "$LANES/632-phase/tb/verilator/milan_dp_render")
import tdm8_render_mutants as t  # noqa: E402
names = set(sys.argv[1:])
t.MUTATIONS = [m for m in t.MUTATIONS if m[0] in names]
assert len(t.MUTATIONS) == len(names), [m[0] for m in t.MUTATIONS]
t.CLEAN_CONTROLS = []
sys.argv = ["tdm8_render_mutants.py"]
sys.exit(t.main())
