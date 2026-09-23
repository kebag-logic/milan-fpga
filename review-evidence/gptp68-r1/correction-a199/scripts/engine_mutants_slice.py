#!/usr/bin/env python3
"""One slice of the engine suite's mutation arm (tb/verilator/engine/mutants.py).

Runs the arm's own main() -- positive control, then every mutant, verdicts by
tb/mutation_verdict.py -- over MUTATIONS[k::n] only. The n slices together
are exactly the arm's MUTATIONS list, each mutant once. The one change is the
arm's verilator C++ build parallelism, -j 4 -> -j 2, so four slices in
parallel never exceed eight compile jobs; -j does not change what is built.
Nothing is written into the lane tree (the arm stages under a temp dir).

Usage: engine_mutants_slice.py <k> <n>   (run from tb/verilator/engine)
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

LANE = Path(os.environ.get("A199_LANE", "$LANES/gptp68-step-policy"))
ENGINE = LANE / "tb/verilator/engine"
sys.path.insert(0, str(ENGINE))
import mutants as M  # noqa: E402

k, n = int(sys.argv[1]), int(sys.argv[2])
total = len(M.MUTATIONS)
M.MUTATIONS = M.MUTATIONS[k::n]
i = M.VFLAGS.index("-j")
assert M.VFLAGS[i + 1] == "4", M.VFLAGS
M.VFLAGS = M.VFLAGS[:i + 1] + ["2"] + M.VFLAGS[i + 2:]
print(f"slice {k} of {n}: {len(M.MUTATIONS)} of the arm's {total} mutants: "
      + "; ".join(m[0] for m in M.MUTATIONS), flush=True)
sys.exit(M.main())
