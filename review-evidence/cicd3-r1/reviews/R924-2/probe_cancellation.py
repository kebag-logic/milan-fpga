#!/usr/bin/env python3
"""R924: inspect the real matrix and falsify its policy checker in memory."""
import copy
import json
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
sys.dont_write_bytecode = True
sys.path.insert(0, str(root / "scripts"))
import ci_events as policy

world = policy.parse_world(policy.read_tree(root))
workflow = world[policy.RTL_FAST]
job = workflow["jobs"]["firmware-boundary-capture"]
observed = policy.Contract()
policy.check_boundary_legs(observed, workflow, 2)
assert observed.findings == []
changed = copy.deepcopy(workflow)
changed["jobs"]["firmware-boundary-capture"]["strategy"]["fail-fast"] = True
counterfactual = policy.Contract()
policy.check_boundary_legs(counterfactual, changed, 2)
assert any("strategy must be exactly" in finding for finding in counterfactual.findings)
assert job["strategy"]["fail-fast"] is False
watcher = workflow["jobs"]["ci-fail-fast"]
assert "github.event.pull_request.head.repo.full_name" in watcher["if"]
print(json.dumps({"reviewer": "R924", "head": "9c62539365fea8316dae2b9fd7c68defeff5cb31",
                  "capture_matrix": job["strategy"], "watcher_if": watcher["if"],
                  "production_false_findings": observed.findings,
                  "counterfactual_true_findings": counterfactual.findings,
                  "failure_control": "static policy probe; no hosted failure injected"}, indent=2))
