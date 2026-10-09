#!/usr/bin/env python3
"""R580-2 probe P5b: the head gate's reason for each named fuzz case number.

Usage: probe_fuzz_reasons.py <syn/ooc directory> <cases> <seed> <case numbers comma-separated>
Wraps the gate's run_case to print the first NOT COMPARABLE/RESULT line of each listed case
together with the changed file's diff against the fixture's hierarchy (role rows only).
"""
import contextlib
import io
import sys
from pathlib import Path

folder, cases, seed = Path(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
wanted = {int(n) for n in sys.argv[4].split(",")}
sys.path.insert(0, str(folder))
import pp_resource_gate as gate  # noqa: E402
import pp_placement  # noqa: E402

counter = {"n": -3}
original = gate.run_case


def wrapped(work, target, files, baseline, audit):
    counter["n"] += 1
    runs = original(work, target, files, baseline, audit)
    if counter["n"] in wanted:
        reason = next((line for line in runs[0][2] if "NOT COMPARABLE" in line or "RESULT" in line), "")
        changed = files.get("baseline_hierarchy.rpt")
        roles = ""
        if changed is not None:
            pristine = (target[0] / "baseline_hierarchy.rpt").read_text().splitlines()
            after = changed.decode(errors="replace").splitlines()
            lost = [line.split("|")[2].strip() for line in pristine if line not in after and len(line.split("|")) > 3]
            roles = f" lost rows' modules={lost}"
        sys.__stdout__.write(f"case {counter['n']}: exit {runs[0][1]}: {reason[:220]}{roles}\n")
    return runs


gate.run_case = wrapped
with contextlib.redirect_stdout(io.StringIO()):
    gate.fuzz(cases, seed, None, None, gate.BASELINE, gate.BUDGET)
