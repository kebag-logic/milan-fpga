#!/usr/bin/env python3
"""Reproduce the workflow-contract scope conflict without editing workflows."""
import copy
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path.cwd() / "scripts"))
import ci_events

world = ci_events.parse_world(ci_events.read_tree(Path.cwd()))
baseline = ci_events.check(world)
assert not baseline.findings, baseline.findings
results = {"baseline_checked": baseline.checked, "baseline_findings": [], "controls": []}
for workflow, job, key, value in (
    (ci_events.DOCS, "docs-check", "needs", ["docs-shards"]),
    (ci_events.DOCS, "docs-check", "strategy", {"matrix": {"shard": [0, 1]}}),
    (ci_events.ELABORATE, "elaborate", "needs", ["elaborate-shards"]),
    (ci_events.ELABORATE, "elaborate", "strategy", {"matrix": {"shard": [0, 1]}}),
):
    changed = copy.deepcopy(world)
    changed[workflow]["jobs"][job][key] = value
    findings = [s for s in ci_events.check(changed).findings if key in s and job in s]
    assert findings, (workflow, job, key)
    results["controls"].append({"workflow": workflow, "job": job,
                                "change": {key: value}, "findings": findings})
changed = copy.deepcopy(world)
job = changed[ci_events.RTL_FULL]["jobs"]["verilator-shards"]
cache = next(step for step in job["steps"] if step.get("id") == "cache-verilator")
cache["with"]["key"] += "-source-digest-recipe-digest"
findings = [s for s in ci_events.check(changed).findings
            if "cache" in s.lower() or "sequence" in s.lower()]
assert findings
results["controls"].append({"workflow": ci_events.RTL_FULL, "job": "verilator-shards",
                           "change": "append source and recipe digest fields to cache key",
                           "findings": findings})
print(json.dumps(results, indent=2))
