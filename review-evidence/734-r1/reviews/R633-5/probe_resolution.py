#!/usr/bin/env python3
"""Delete each retained conflict input, then require the contract to reject it."""
import argparse
import ast
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()
    root, packet = args.root.resolve(), args.packet.resolve()
    scratch = packet / "scratch" / "resolution"
    scratch.mkdir(parents=True, exist_ok=True)
    archive = subprocess.check_output(["git", "-C", str(root), "archive", "HEAD"])
    with tarfile.open(fileobj=io.BytesIO(archive)) as stream:
        stream.extractall(scratch, filter="data")
    script = scratch / "scripts/ci_events.py"
    pristine = script.read_text()
    assignment = next(n for n in ast.parse(pristine).body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "INHERITED_STEP_ENV" for t in n.targets))
    lines = pristine.splitlines(keepends=True)
    before, region, after = "".join(lines[:assignment.lineno-1]), "".join(lines[assignment.lineno-1:assignment.end_lineno]), "".join(lines[assignment.end_lineno:])
    cases = [("clean", None)] + [(name.lower().replace("_", "-"), name) for name in ("PR_BASE_REF", "PR_HEAD_SHA", "FIRMWARE_BOUNDARY_RESULT", "FIRMWARE_VERILATOR_RESULT")]
    results = []
    for name, token in cases:
        changed = region
        if token and token.startswith("PR_"):
            old = '(RTL_FAST, "changes"): ("EVENT_NAME", "PR_BASE_REF", "PR_HEAD_SHA", "PUSH_BEFORE_SHA")'
            assert changed.count(old) == 1
            changed = changed.replace(old, old.replace(f'"{token}", ', ""))
        elif token:
            assert changed.count(f'"{token}",') == 1
            changed = changed.replace(f'"{token}",', "")
        if token:
            assert changed != region, f"mutation did not change {token}"
        script.write_text(before + changed + after)
        command = ["python3", "-B", "scripts/ci_events.py", "--check"]
        env = dict(os.environ, TMPDIR=str(packet / "scratch"), PYTHONDONTWRITEBYTECODE="1")
        outcome = subprocess.run(command, cwd=scratch, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=60)
        log = outcome.stdout.replace(str(scratch), "<probe>")
        (packet / f"resolution-{name}.log").write_text(log)
        (packet / f"resolution-{name}.rc").write_text(str(outcome.returncode) + "\n")
        accepted = outcome.returncode == 0 if token is None else outcome.returncode == 1 and token in log and "outside this job's allowlist" in log
        results.append({"case": name, "removed_from": "INHERITED_STEP_ENV", "token": token, "returncode": outcome.returncode, "expected_outcome_observed": accepted})
    script.write_text(pristine)
    (packet / "resolution-probes.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
    assert all(row["expected_outcome_observed"] for row in results)


if __name__ == "__main__":
    main()
