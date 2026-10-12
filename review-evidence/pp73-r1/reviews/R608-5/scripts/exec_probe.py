#!/usr/bin/env python3
"""Executed half of the traceability gate, restricted to the named suites.

A reviewer subset run cannot satisfy the whole-bank executed half, so this
loads scripts/check-req-tags.py from CLONE, keeps the tags and evidence lines of
SUITES only, and calls the gate's own check_executed on them: once as
recorded, once with every check_observed.py evidence line removed.
usage: exec_probe.py CLONE SUITESLOG EVIDENCE SUITE...
"""
import importlib.util
import sys
from pathlib import Path

root, suites_log, evidence = map(Path, sys.argv[1:4])
keep = set(sys.argv[4:])
spec = importlib.util.spec_from_file_location("check_req_tags", root / "scripts/check-req-tags.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
problems: list[str] = []
rows = gate.read_rows((root / gate.REVIEW).read_text(encoding="utf-8"))
tags = [t for t in gate.read_tags(root, rows, problems) if t.suite in keep]
suites = suites_log.read_text(encoding="utf-8")
lines = [ln for ln in evidence.read_text(encoding="utf-8").splitlines() if ln.split(" ")[0] in keep]
for label, ev in (("as recorded", lines),
                  ("check_observed.py evidence removed", [ln for ln in lines if "check_observed.py:" not in ln])):
    found: list[str] = list(problems)
    ran = gate.check_executed(tags, suites, "\n".join(ev) + ("\n" if ev else ""), found)
    print(f"EXEC {label}: {len(tags)} tags in {sorted(keep)}, {ran} evidence lines, "
          f"{len(found)} problems")
    for p in found:
        print(f"    {p}")
