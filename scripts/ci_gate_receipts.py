#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Record actual step outcomes and refuse an incomplete parallel gate union."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import sys

from ci_case_receipts import source_identity
from ci_gate_workflows import CARRIERS, ROOT, TEMPLATES, case_inventory, load_template, worker_id
from ci_manifest import canonical, read, unique_object

SCOPE_CONDITION = "${{ steps.scope.outputs.rtl == 'true' }}"
SHA = re.compile(r"[0-9a-f]{40}\Z")


@dataclass(frozen=True)
class StepContext:
    """Actual step outcomes and the existing scope step's recorded output."""

    steps: dict
    scope: str


def record(name: str, leg: int, source: dict, identity: tuple[str, str], digest: str,
           context: StepContext) -> dict:
    """Transport reported outcomes without substituting success for missing execution."""
    cases = case_inventory(name, source)
    rows = []
    for case in cases:
        if case["leg"] != leg:
            continue
        result = context.steps.get(case["id"], {})
        if not isinstance(result, dict):
            result = {}
        rows.append({"case": case["id"], "name": case["name"],
                     "outcome": result.get("outcome"), "conclusion": result.get("conclusion")})
    return {"schema": 1, "workflow": name, "leg": leg, "head": identity[0], "tree": identity[1],
            "template_sha256": digest, "inventory": [case["id"] for case in cases],
            "scope": context.scope, "results": rows}


def verify(name: str, source: dict, identity: tuple[str, str], digest: str,
           receipts: list[dict], needs: dict) -> list[str]:
    """Require each source gate once and every dependent job successful, with exact source binding."""
    expected_jobs = {worker_id(name, leg) for leg in range(2)}
    if set(needs) != expected_jobs:
        raise ValueError("aggregate has a missing or extra dependent job")
    for job in expected_jobs:
        if not isinstance(needs[job], dict) or needs[job].get("result") != "success":
            raise ValueError(job + ": dependent job failed, cancelled or skipped")
    if len(receipts) != 2 or {row.get("leg") for row in receipts} != {0, 1}:
        raise ValueError("missing, duplicate or extra gate leg")
    cases = case_inventory(name, source)
    inventory = [case["id"] for case in cases]
    seen = []
    scopes = set()
    for document in receipts:
        expected = {"schema", "workflow", "leg", "head", "tree", "template_sha256", "inventory", "scope", "results"}
        if set(document) != expected or type(document["schema"]) is not int or document["schema"] != 1:
            raise ValueError("gate receipt schema differs")
        if type(document["leg"]) is not int:
            raise ValueError("gate leg must be an integer")
        for field, value in (("workflow", name), ("head", identity[0]), ("tree", identity[1]),
                             ("template_sha256", digest), ("inventory", inventory)):
            if document[field] != value:
                raise ValueError("gate receipt " + field + " differs from its source")
        selected = [case for case in cases if case["leg"] == document["leg"]]
        rows = document["results"]
        if not isinstance(rows, list) or len(rows) != len(selected):
            raise ValueError("gate leg has missing or extra execution")
        scope = document["scope"]
        if not isinstance(scope, str):
            raise ValueError("scope must be the recorded string output")
        scopes.add(scope)
        for case, row in zip(selected, rows):
            if set(row) != {"case", "name", "outcome", "conclusion"}:
                raise ValueError("gate result schema differs")
            if row["case"] != case["id"] or row["name"] != case["name"]:
                raise ValueError("gate execution differs from its original inventory")
            result = (row["outcome"], row["conclusion"])
            if result != ("success", "success"):
                legitimate_skip = (name == "elaborate" and case["condition"] == SCOPE_CONDITION
                                   and scope == "false" and result == ("skipped", "skipped"))
                if not legitimate_skip:
                    raise ValueError(case["name"] + ": missing, failed, cancelled or unjustifiably skipped")
            elif name == "elaborate" and scope != "true":
                raise ValueError("executed elaboration has inconsistent scope evidence")
            seen.append(case["id"])
    if len(scopes) != 1 or sorted(seen) != sorted(inventory) or len(set(seen)) != len(seen):
        raise ValueError("gate union or scope evidence is inconsistent")
    return seen


def main() -> int:
    """Write worker evidence or verify the downloaded exact-head union."""
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    write = commands.add_parser("record")
    write.add_argument("--workflow", choices=CARRIERS, required=True)
    write.add_argument("--leg", type=int, choices=(0, 1), required=True)
    write.add_argument("--output", type=Path, required=True)
    check = commands.add_parser("verify")
    check.add_argument("--workflow", choices=CARRIERS, required=True)
    check.add_argument("--root", type=Path, required=True)
    check.add_argument("--head", required=True)
    check.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        identity = source_identity(ROOT)
        head = os.environ.get("GITHUB_SHA", "") if args.command == "record" else args.head
        if not SHA.fullmatch(head) or identity[0] != head:
            raise ValueError("checkout HEAD differs from the exact run SHA")
        source = load_template(ROOT, args.workflow)
        digest = hashlib.sha256(ROOT.joinpath(TEMPLATES[args.workflow]).read_bytes()).hexdigest()
        if args.command == "record":
            actual = json.loads(os.environ["CI_GATE_STEPS"], object_pairs_hook=unique_object)
            value = record(args.workflow, args.leg, source, identity, digest, StepContext(
                actual, os.environ.get("CI_GATE_SCOPE", "")))
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open("xb") as stream:
                stream.write(canonical(value) + b"\n")
        else:
            receipts = [read(path) for path in sorted(args.root.rglob("receipt.json"))]
            needs = json.loads(os.environ["CI_GATE_NEEDS"], object_pairs_hook=unique_object)
            names = verify(args.workflow, source, identity, digest, receipts, needs)
            if args.output:
                observed = sorted([row for receipt in receipts for row in receipt["results"]],
                                  key=lambda row: row["case"])
                value = {"suite": "gate/" + args.workflow, "head": identity[0], "tree": identity[1],
                         "inventory": [case["id"] for case in case_inventory(args.workflow, source)],
                         "legs": [{"shard": str(receipt["leg"]) + "/2",
                                   "cases": [row["case"] for row in receipt["results"]]} for receipt in receipts],
                         "union": "pass", "verdicts_sha256": hashlib.sha256(canonical(observed)).hexdigest()}
                args.output.parent.mkdir(parents=True, exist_ok=True)
                args.output.write_bytes(canonical(value) + b"\n")
            print(f"{args.workflow}: {len(names)} source gates exactly once; both jobs successful")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"gate evidence refused: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
