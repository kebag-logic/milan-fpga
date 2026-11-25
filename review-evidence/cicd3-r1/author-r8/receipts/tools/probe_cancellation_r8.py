#!/usr/bin/env python3
"""Inverse of the R924-2 cancellation probe: the production matrix keeps fail-fast true and passes the production
boundary-leg checker; the same workflow with only fail-fast flipped to false (or the key removed) is refused by it.
Usage: probe_cancellation_r8.py <checkout>"""
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
assert job["strategy"]["fail-fast"] is True, job["strategy"]
observed = policy.Contract()
policy.check_boundary_legs(observed, workflow, 2)
assert observed.findings == [], observed.findings
planted = {}
for label, edit in (("fail-fast false", lambda s: s.__setitem__("fail-fast", False)),
                    ("fail-fast key removed", lambda s: s.pop("fail-fast"))):
    changed = copy.deepcopy(workflow)
    edit(changed["jobs"]["firmware-boundary-capture"]["strategy"])
    c = policy.Contract()
    policy.check_boundary_legs(c, changed, 2)
    assert any("strategy must be exactly" in f for f in c.findings), (label, c.findings)
    planted[label] = c.findings
watcher = workflow["jobs"]["ci-fail-fast"]
assert "github.event.pull_request.head.repo.full_name" in watcher["if"]
judge = workflow["jobs"]["firmware-boundary"]
assert "firmware-boundary-capture" in judge["needs"]
print(json.dumps({"capture_matrix": job["strategy"], "capture_permissions": job.get("permissions"),
                  "watcher_if": watcher["if"], "judge_needs": judge["needs"],
                  "production_findings": observed.findings, "planted_findings": planted}, indent=2))
print("PROBE PASS")
