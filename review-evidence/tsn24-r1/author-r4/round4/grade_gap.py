#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Grade the unchanged review gap replay, including its equivalent control."""
import argparse
import json
from pathlib import Path
from grade_contract import xml_cases, require

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("--repo", required=True, type=Path)
ap.add_argument("--work", required=True, type=Path)
a = ap.parse_args()
w = a.work.resolve()
registry = {p["name"]: p for p in json.loads((a.repo / "tests/mutations.json").read_text())}
plants = {p["name"]: p for p in json.loads((w / "review-scripts/plants_gap.json").read_text())}
required = {"r630-3-listener-range-only", "r630-3-withdrawal-clears-probe", "r630-3-init-keeps-listener"}
results = json.loads((w / "review-gap-results.json").read_text())
require(len(results) == len(plants) == 17, "gap inventory differs")
baseline, failures, _ = xml_cases(w / "contract", "control-control")
require(not failures, "baseline failed")
summary = []
for r in results:
    name = r["plant"]
    cases, failures, receipts = xml_cases(w / "review-gap", name + "-full")
    require(r["build_rc"] == 0 and cases == baseline and r["tests"] == len(baseline)
            and r["skipped"] == r["disabled"] == 0, name + ": incomplete run")
    if name in required:
        plant = registry[name]
        require(all(plant[k] == plants[name][k] for k in ("path", "old", "new")), "changed review plant")
        killer = plant["kills"][0]
        require({key[1] for key in failures} == {killer["test"]}, "wrong failing set")
        require(all(killer["needle"] in msg for msg in failures.values()), "missing needle")
    if not failures:
        require(name == "r630-3-drop-send-clock-reread", "unexpected surviving gap plant")
    summary.append(dict(plant=name, result="CAUGHT" if failures else "EQUIVALENT",
                        registered_requirement=name in required,
                        failures=sorted({key[1] for key in failures}), instances=len(cases), xml=receipts))
(w / "review-gap-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print("Three requested exact plants CAUGHT; 16 of 17 exploratory plants CAUGHT; one unregistered equivalent clock-read control")
