#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted manifest differences and incomplete evidence must never compare equal."""

from copy import deepcopy
import json
from pathlib import Path
import tempfile

from ci_manifest import canonical, compare, envelope, read, validate


def fixture() -> dict:
    """A small complete collection with one job, step and split inventory."""
    return {
        "subject": {"repository": "example/project", "event": "pull_request",
                    "head": "1" * 40, "tree": "2" * 40, "base": "3" * 40, "merge_base": "4" * 40},
        "definitions": {".github/workflows/check.yml": "a" * 64},
        "environment": {"image": "registry.example/ci@sha256:" + "b" * 64,
                        "tools": {"compiler": {"version": "1.0", "source_sha256": "a" * 64,
                                               "recipe_sha256": "b" * 64, "binary_sha256": "c" * 64}},
                        "actions": ["example/checkout@" + "c" * 40]},
        "plan": {"check/test/0": {"workflow": "check", "job": "test", "matrix": {"leg": 0},
                                  "needs": [], "condition": "success()",
                                  "steps": [{"name": "test", "kind": "run", "sha256": "d" * 64,
                                             "condition": "success()"}]}},
        "execution": {"check/test/0": [{"name": "test", "outcome": "success", "skip_reason": None}]},
        "inventories": {"suite": {"expected": ["case"], "legs": {"0/1": ["case"]},
                                  "union": "success", "verdicts_sha256": "e" * 64}},
        "results": {"check/test/0": "success"},
    }


def changed(payload: dict, path: tuple[str, ...], value: object) -> dict:
    """Change one field in an independent collector's payload."""
    result = deepcopy(payload)
    parent = result
    for key in path[:-1]:
        parent = parent[key]
    parent[path[-1]] = value
    return result


def main() -> int:
    """Exercise each compared section, omissions, cancellation and canonical transport."""
    original = fixture()
    left = envelope(original, {"wall_clock": 100, "runner": "local"})
    validate(left)
    assert compare(left, envelope(original, {"wall_clock": 300, "runner": "hosted"})) == []
    controls = [
        (("subject", "head"), "9" * 40),
        (("subject", "tree"), "9" * 40),
        (("subject", "base"), "9" * 40),
        (("definitions", ".github/workflows/check.yml"), "9" * 64),
        (("environment", "image"), "registry.example/other@sha256:" + "9" * 64),
        (("environment", "actions"), ["example/checkout@" + "9" * 40]),
        (("environment", "tools", "compiler", "version"), "2.0"),
        (("environment", "tools", "compiler", "source_sha256"), "9" * 64),
        (("plan", "check/test/0", "matrix"), {"leg": 1}),
        (("plan", "check/test/0", "needs"), ["other"]),
        (("execution", "check/test/0"), []),
        (("execution", "check/test/0"), [{"name": "test", "outcome": "skipped", "skip_reason": "false"}]),
        (("inventories", "suite", "legs"), {"0/1": []}),
        (("inventories", "suite", "legs"), {"0/1": ["case", "case"]}),
        (("inventories", "suite", "verdicts_sha256"), "9" * 64),
        (("results", "check/test/0"), "failure"),
        (("results", "check/test/0"), "cancelled"),
    ]
    for path, value in controls:
        try:
            right = envelope(changed(original, path, value), {})
            refused = bool(compare(left, right))
        except ValueError:
            refused = True
        assert refused, path
        print("manifest difference refused:", ".".join(path))
    for section in ("plan", "execution", "results"):
        mutant = deepcopy(original)
        mutant[section]["extra"] = deepcopy(next(iter(mutant[section].values())))
        altered = envelope(mutant, {})
        try:
            refused = bool(compare(left, altered))
        except ValueError:
            refused = True
        assert refused, section
        print("manifest extra job refused:", section)
    incomplete = envelope(changed(original, ("results", "check/test/0"), "cancelled"), {})
    for reason in (None, "false"):
        skipped = envelope(changed(original, ("execution", "check/test/0"),
                                   [{"name": "test", "outcome": "skipped", "skip_reason": reason}]), {})
        try:
            compare(skipped, deepcopy(skipped))
        except ValueError:
            print("two identical skipped-step collections refused")
        else:
            raise AssertionError("skipped-step collections accepted")
    try:
        compare(incomplete, incomplete)
    except ValueError:
        print("two identical cancelled collections refused")
    else:
        raise AssertionError("cancelled collections accepted")
    incomplete["complete"] = True
    incomplete["incomplete_reasons"] = []
    try:
        validate(incomplete)
    except ValueError:
        print("forged completeness refused")
    else:
        raise AssertionError("forged completeness accepted")
    for bad in (0.5, float("nan"), {1: "non-string key"}):
        try:
            canonical(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("ambiguous JSON accepted")
    with tempfile.TemporaryDirectory(prefix="manifest-controls-") as temporary:
        path = Path(temporary) / "manifest.json"
        path.write_bytes(canonical(left) + b"\n")
        assert compare(left, read(path)) == []
        path.write_text('{"schema": 0, "schema": 1}')
        try:
            read(path)
        except ValueError:
            print("duplicate JSON key refused")
        else:
            raise AssertionError("duplicate key accepted")
    assert canonical(json.loads(canonical(left))) == canonical(left)
    print("manifest comparison controls: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
