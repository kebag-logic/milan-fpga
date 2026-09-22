#!/usr/bin/env python3
"""Explicit #439 regressions; no workflow commands are executed."""
import copy
from pathlib import Path
import sys
sys.path.insert(0, str(Path.cwd() / "scripts"))
import ci_events as ci
pristine = ci.parse_world(ci.read_tree(Path.cwd()))
step = next(s for s in ci.steps(ci.jobs(pristine[ci.RTL_FULL])[ci.GATE_JOB]) if s.get("id") == ci.PIN_STEP_ID)
lines = ci.normalize_script(step["run"])
start = lines.index('if [ "$head" != "$GITHUB_SHA" ]; then')
end = lines.index("fi", start)
exit_at = lines.index("exit 1", start)
controls = [
    ("delete checkout HEAD mismatch assertion", lines[:start] + lines[end+1:], start+1),
    ("replace exit 1 with true", lines[:exit_at] + ["true"] + lines[exit_at+1:], exit_at+1),
]
failures = 0
for label, edited, differing in controls:
    world = copy.deepcopy(pristine)
    target = next(s for s in ci.steps(ci.jobs(world[ci.RTL_FULL])[ci.GATE_JOB]) if s.get("id") == ci.PIN_STEP_ID)
    target["run"] = "\n".join(edited)
    findings = ci.check(world).findings
    want = f"job `full-ci-gate` step 2 (`{step['name']}`) script is not the canonical form: line {differing} must be {lines[differing-1]!r}"
    caught = any(want in finding for finding in findings)
    print(f"{label}: {'PASS' if caught else 'FAIL'}; expected={want!r}; findings={findings!r}")
    failures += not caught
print(f"explicit SHA controls: {2-failures}/2 caught")
sys.exit(bool(failures))
