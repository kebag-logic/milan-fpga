#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe (round 5): are two surviving name mutants of probe_r5_names.py exit-equivalent at head?

Two baselines, each a copy of the committed one with one edit, go through check-baseline with three gates: the
head's, and the mutated copies probe_r5_names.py left under <names-scratch> for "walk: every level below the
scopes object also scope" and "SCOPES: any top-level key".
  b: a bracketed key, FF[0], in the first route-1x1 scope's counts (one level below the scopes object);
  c: a description note shaped as a record, {"x": {"record": {"scopes": {"a[1]": 1}}}}.
The ruling implies exit 2 for both. A mutant giving 2 for both is exit-equivalent on these inputs.

Usage: probe_r5_equiv.py <checkout> <names-scratch> <scratch-dir>
"""

import json
from pathlib import Path
import subprocess
import sys

REPO, NAMES, SCRATCH = (Path(arg).resolve() for arg in sys.argv[1:4])
SCRATCH.mkdir(parents=True, exist_ok=True)
committed = (REPO / "syn/ooc/pp_resource_baseline.json").read_text()
b = json.loads(committed)
next(iter(b["endpoints"]["route-1x1"]["record"]["scopes"].values()))["FF[0]"] = 1
(SCRATCH / "b.json").write_text(json.dumps(b, indent=1))
c = json.loads(committed)
c["description"] = {"x": {"record": {"scopes": {"a[1]": 1}}}}
(SCRATCH / "c.json").write_text(json.dumps(c, indent=1))
for label, folder in (("head", REPO / "syn/ooc"),
                      ("mutant every-level", NAMES / "walk__every_level_below_the_scopes_object_also_scope"),
                      ("mutant SCOPES top-level wildcard", NAMES / "SCOPES__any_top_level_key")):
    for case in ("b", "c"):
        run = subprocess.run([sys.executable, "-B", str(folder / "pp_resource_gate.py"), "check-baseline",
                              "--baseline", str(SCRATCH / f"{case}.json"), "--budget",
                              str(REPO / "docs/design/AREA_BUDGET.md")], capture_output=True, text=True)
        tail = run.stdout.strip().splitlines()[-1] if run.stdout.strip() else run.stderr.strip()[-120:]
        print(f"{label:34} case {case} rc={run.returncode} | {tail.replace(str(SCRATCH), '<scratch>')[-150:]}")
