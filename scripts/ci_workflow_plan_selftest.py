#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Prove exact matrix, dependency and step planning from immutable Git inputs."""

import copy
import hashlib
from pathlib import Path
import subprocess
import tempfile

import yaml

from ci_workflow_plan import committed_plan, expand_workflow, verify_bound_plan

SOURCE = """name: fixtures
on: [push, pull_request]
jobs:
  start:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@0123456789012345678901234567890123456789
  workers:
    name: Worker ${{ matrix.index }}/${{ matrix.total }}
    needs: start
    strategy:
      matrix:
        index: [0, 1, 2, 3]
        total: [4]
    runs-on: ubuntu-24.04
    steps:
      - name: Check original values
        run: |
          printf 'original values\\n'
          exit 0
  verdict:
    needs: workers
    if: ${{ always() }}
    runs-on: ubuntu-24.04
    steps:
      - name: Verify every leg
        run: python3 verify.py
"""
PATH = ".github/workflows/control.yml"


def fixture_commit(root: Path, subject: str, parent: str | None = None) -> str:
    """Create fixture objects using source attribution without changing Git configuration."""
    source = Path(__file__).resolve().parents[1]
    original = subprocess.check_output(["git", "-C", str(source), "cat-file", "commit", "HEAD"])
    attribution = [line for line in original.split(b"\n\n", 1)[0].splitlines()
                   if line.startswith((b"author ", b"committer "))]
    if len(attribution) != 2:
        raise ValueError("source commit has ambiguous attribution")
    tree = subprocess.check_output(["git", "-C", str(root), "write-tree"]).strip()
    headers = [b"tree " + tree] + ([b"parent " + parent.encode()] if parent else []) + attribution
    content = b"\n".join(headers) + b"\n\n" + subject.encode() + b"\n"
    head = subprocess.check_output(["git", "-C", str(root), "hash-object", "-w", "-t", "commit", "--stdin"],
                                   input=content).decode().strip()
    subprocess.run(["git", "-C", str(root), "update-ref", "HEAD", head], check=True)
    return head


def main() -> int:
    """Use the production planner for positive, corrupt and Git-byte controls."""
    plan, labels = expand_workflow(PATH, SOURCE)
    assert len(plan) == 6
    workers = [key for key, row in plan.items() if row["job"] == "workers"]
    assert len(workers) == 4
    assert {labels[key] for key in workers} == {f"Worker {index}/4" for index in range(4)}
    assert plan[PATH + ":verdict"]["needs"] == workers
    assert all(plan[key]["needs"] == [PATH + ":start"] for key in workers)
    text = "printf 'original values\\n'\nexit 0\n"
    assert plan[workers[0]]["steps"][0]["sha256"] == hashlib.sha256(text.encode()).hexdigest()
    for old, new in (("original values", "changed values"), ("exit 0", "exit 1"),
                     ("index: [0, 1, 2, 3]", "index: [0, 1, 2]"),
                     ("needs: workers", "needs: start"), ("always()", "failure()")):
        altered, _ = expand_workflow(PATH, SOURCE.replace(old, new))
        assert altered != plan, (old, new)
        print(f"plan control: changed {old!r} changes the bound plan")
    invalid = {
        "duplicate key": SOURCE.replace("    needs: start", "    needs: start\n    needs: verdict"),
        "unhashable dependency": SOURCE.replace("needs: start", "needs: [{bad: value}]"),
        "missing dependency": SOURCE.replace("needs: start", "needs: absent"),
        "cycle": SOURCE.replace("needs: start", "needs: verdict"),
        "dynamic matrix": SOURCE.replace("[0, 1, 2, 3]", "\"${{ fromJSON(needs.start.outputs.matrix) }}\""),
        "float coordinate": SOURCE.replace("[0, 1, 2, 3]", "[0, 1.5]"),
        "duplicate coordinate": SOURCE.replace("[0, 1, 2, 3]", "[0, 0]"),
        "empty coordinate": SOURCE.replace("[0, 1, 2, 3]", "[]"),
        "name expression": SOURCE.replace("matrix.index", "github.sha"),
        "name collision": SOURCE.replace("Worker ${{ matrix.index }}/${{ matrix.total }}", "Worker"),
        "missing body": SOURCE.replace("        run: python3 verify.py", "        id: no-body"),
        "alias": SOURCE.replace("index: [0, 1, 2, 3]", "index: &indices [0, 1, 2, 3]"),
    }
    for label, text in invalid.items():
        try:
            expand_workflow(PATH, text)
        except (ValueError, yaml.YAMLError):
            print(f"plan control: {label} refused")
        else:
            raise AssertionError(f"invalid plan accepted: {label}")
    with tempfile.TemporaryDirectory(prefix="workflow-plan-") as temporary:
        root = Path(temporary)
        def git(*args: str) -> str:
            """Fixture commits use the configured identity and one-line subjects."""
            return subprocess.check_output(["git", "-C", str(root), *args], text=True,
                                           stderr=subprocess.STDOUT).strip()
        git("init", "-q")
        target = root / PATH
        target.parent.mkdir(parents=True)
        target.write_text(SOURCE)
        git("add", PATH)
        head = fixture_commit(root, "Create immutable workflow fixture")
        original = committed_plan(root, head)
        assert original["plan"] == plan
        payload = {"subject": {"head": head, "tree": original["tree"]},
                   "definitions": original["definitions"], "plan": original["plan"]}
        assert verify_bound_plan(root, payload) == original
        for section in ("definitions", "plan", "tree"):
            changed = copy.deepcopy(payload)
            if section == "tree":
                changed["subject"]["tree"] = "0" * 40
            else:
                changed[section].pop(next(iter(changed[section])))
            try:
                verify_bound_plan(root, changed)
            except ValueError:
                print(f"plan control: forged {section} refused against committed source")
            else:
                raise AssertionError("forged source plan accepted: " + section)
        assert original["definitions"][PATH] == hashlib.sha256(SOURCE.encode()).hexdigest()
        target.write_text(SOURCE.replace("exit 0", "exit 1"))
        assert committed_plan(root, head) == original
        git("add", PATH)
        fixture_commit(root, "Change the fixture workflow", head)
        revised = committed_plan(root, git("rev-parse", "HEAD"))
        for key in ("head", "tree", "definitions", "plan"):
            assert revised[key] != original[key], key
        assert committed_plan(root, head) == original
        print("plan control: dirty bytes and another head cannot redefine committed inputs")
    print("workflow planner: all controls pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
