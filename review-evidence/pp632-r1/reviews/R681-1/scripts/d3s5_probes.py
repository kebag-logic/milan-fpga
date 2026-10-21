#!/usr/bin/env python3
"""Reviewer probes on D3S5's setup (tb/pp_top/d3_phases.hpp), run through
d3_mutants.py's own harness (private copy, --d3-only). Disposable.

  r_d3s5_unprimed       : the head's priming SET removed (the 0b097460 setup):
                          the latency is measured on the never-set arm, so the
                          premise must fail by one cycle.
  r_d3s5_primed_other   : the priming SET moved to output 1, so output 0's
                          latency is again measured on the never-set arm: the
                          premise must fail (priming the right row matters).

usage: d3s5_probes.py REPO_ROOT OUTPUT_DIR VERILATOR JOBS
"""
import concurrent.futures
import json
import sys
from pathlib import Path

root, output, verilator, jobs = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3], int(sys.argv[4])
sys.path.insert(0, str(root / "tb/pp_top"))
import d3_mutants as dm  # noqa: E402

D3 = "tb/pp_top/d3_phases.hpp"
PRIME = "    const bool primed = set_ok(AEM_SET_STREAM_INFO, pl_ptof(0, 3999999));\n"
PROBES = (
    ("r_d3s5_unprimed", ((D3, PRIME, "    const bool primed = true;\n"),), ("D3S5 premise",)),
    ("r_d3s5_primed_other", ((D3, PRIME, PRIME.replace("pl_ptof(0,", "pl_ptof(1,")),), ("D3S5 premise",)),
)
output.mkdir(parents=True, exist_ok=True)
work = (root, output, verilator)
records = []
with concurrent.futures.ThreadPoolExecutor(max(1, jobs)) as pool:
    for rec in pool.map(lambda p: dm.judge(p[0], dm.PP_TOP, p[1], p[2], work), PROBES):
        records.append(rec)
        print(json.dumps({k: rec.get(k) for k in ("mutant", "verdict", "missing", "failing_checks")}), flush=True)
(output / "results.json").write_text(json.dumps(records, indent=1) + "\n")
print(f"D3S5 probes: {sum(r['verdict'] == 'KILLED' for r in records)} of {len(records)} KILLED")
