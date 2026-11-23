#!/usr/bin/env python3
"""Check literal skipped-matrix metadata after documented expression evaluation.

This is a local static-semantics probe, not a hosted Actions execution.
Authority: https://docs.github.com/en/actions/reference/workflows-and-actions/contexts
The matrix context describes the current job; a nonexistent property evaluates
to an empty string. The watcher has no strategy/matrix.
Usage: python3 probe_skipped_matrix.py CHECKOUT PACKET
"""
from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import sys
from unittest.mock import patch
import yaml

root, packet = map(lambda p: Path(p).resolve(), sys.argv[1:])
sys.dont_write_bytecode = True
sys.path.insert(0, str(root / "scripts"))
from ci_fail_fast import observe, watch

jobs = yaml.safe_load((root / ".github/workflows/rtl-fast.yml").read_text())["jobs"]
watcher = jobs["ci-fail-fast"]
assert "strategy" not in watcher
step = next(s for s in watcher["steps"] if s.get("id") == "ci_observe")
value = step["env"]["SKIPPED_MATRICES"]
literal = json.loads(value)
# Evaluate only the two expressions actually present, using the documented
# nonexistent-property result. No general workflow evaluator is claimed here.
evaluated = value.replace("${{ matrix.shard }}", "").replace("${{ matrix.total }}", "")
assert "${{" not in evaluated
runtime = json.loads(evaluated)
expected = set(json.loads(step["env"]["EXPECTED_JOBS"]))
matrix_jobs = {label for labels in literal.values() for label in labels}
rows = [{"name": name, "status": "completed", "conclusion": "success"} for name in sorted(expected - matrix_jobs)]
rows += [{"name": name, "status": "completed", "conclusion": "skipped"} for name in literal]
assert observe(rows, expected, literal) == (True, None)
print("Unevaluated source-level fixture: complete success")
print("Declared skipped name:", next(iter(literal)))
print("Runtime key under documented expression semantics:", next(iter(runtime)))
try:
    observe(rows, expected, runtime)
except ValueError as exc:
    print("Observed refusal:", str(exc))
    assert str(exc) == "API returned an unplanned job name"
else:
    raise AssertionError("probe no longer reproduces")

class API:
    calls = 0
    def pages(self, *args):
        self.calls += 1
        assert self.calls <= 2, "watcher failed to finish after the later failure"
        return [{**row, "status": "in_progress" if self.calls == 1 else "completed",
                 "conclusion": None if self.calls == 1 else "failure"}
                if row["name"] == "bdd-conformance" else dict(row) for row in rows]

out = packet / "scratch" / "watcher-output"
out.unlink(missing_ok=True)
api = API()
with patch("ci_fail_fast.time.sleep"), redirect_stdout(io.StringIO()) as control_output:
    control = API()
    control_rc = watch(control, 1, expected, literal)
assert control_rc == 1 and control.calls == 2
print("Control with preserved literal: continues after pending work, detects the next-read failure, rc=1.")
with patch.dict(os.environ, {"GITHUB_OUTPUT": str(out)}), redirect_stdout(io.StringIO()) as printed:
    rc = watch(api, 1, expected, runtime)
assert rc == 0 and api.calls == 1
assert "observer_error=true" in out.read_text()
print(printed.getvalue().strip())
print("Watcher returns rc=0 after one read with observer_error=true; later failures are no longer watched.")
print("REPRODUCED: newly added skipped matrix metadata is not literal at runtime.")
