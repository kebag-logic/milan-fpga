#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Exercise generated gate scheduling and fail-closed aggregate evidence."""

import copy
import hashlib

from ci_gate_receipts import StepContext, record, verify
from ci_gate_workflows import CARRIERS, ROOT, case_inventory, generate, load_template, setup, worker_id


def main() -> int:
    """Drive the production generator and verifier with independent planted losses."""
    for name, carrier in CARRIERS.items():
        source = load_template(ROOT, name)
        generated = generate(name, source)
        cases = case_inventory(name, source)
        identity = ("a" * 40, "b" * 40)
        digest = hashlib.sha256(name.encode()).hexdigest()
        scope = "true" if name == "elaborate" else ""
        actual = {case["id"]: {"outcome": "success", "conclusion": "success"} for case in cases}
        receipts = [record(name, leg, source, identity, digest, StepContext(actual, scope)) for leg in range(2)]
        needs = {worker_id(name, leg): {"result": "success"} for leg in range(2)}
        assert len(verify(name, source, identity, digest, receipts, needs)) == len(cases)
        assert set(generated["jobs"][carrier]["needs"]) == set(needs)
        original = source["jobs"][carrier]["steps"]
        for case in cases:
            owned = [step for step in generated["jobs"][worker_id(name, case["leg"])]["steps"]
                     if step.get("id") == case["id"]]
            assert len(owned) == 1
            body = copy.deepcopy(owned[0])
            del body["id"]
            assert body == original[case["index"]]
        for leg in range(2):
            steps = generated["jobs"][worker_id(name, leg)]["steps"]
            source_order = [original.index({k: v for k, v in step.items() if k != "id"})
                            for step in steps if str(step.get("id", "")).startswith("gate_")]
            assert source_order == sorted(source_order)
        def refuse(label: str, records: list, jobs: dict) -> None:
            """Every damaged collection must reach the production refusal path."""
            try:
                verify(name, source, identity, digest, records, jobs)
            except (ValueError, KeyError, TypeError):
                print(name + ": refused " + label)
            else:
                raise AssertionError(name + ": accepted " + label)
        for status in ("failure", "cancelled", "skipped", None):
            changed = copy.deepcopy(needs)
            changed[worker_id(name, 0)]["result"] = status
            refuse("dependent job " + str(status), receipts, changed)
        missing = copy.deepcopy(needs)
        missing.pop(worker_id(name, 0))
        refuse("missing dependent job", receipts, missing)
        refuse("missing receipt", receipts[:1], needs)
        refuse("duplicated leg", [receipts[0], receipts[0]], needs)
        for field in ("head", "tree", "template_sha256", "inventory"):
            changed = copy.deepcopy(receipts)
            changed[0][field] = [] if field == "inventory" else "c" * len(changed[0][field])
            refuse("changed " + field, changed, needs)
        for status in ("failure", "cancelled", "skipped", None):
            changed = copy.deepcopy(receipts)
            changed[0]["results"][0]["outcome"] = status
            changed[0]["results"][0]["conclusion"] = status
            refuse("gate outcome " + str(status), changed, needs)
        dropped = cases[-1]["id"]
        changed = copy.deepcopy(receipts)
        for receipt in changed:
            receipt["inventory"].remove(dropped)
            receipt["results"] = [row for row in receipt["results"] if row["case"] != dropped]
        refuse("gate dropped from every leg and claimed inventory", changed, needs)
        if name == "elaborate":
            skipped = {case["id"]: {"outcome": "skipped", "conclusion": "skipped"} for case in cases}
            receipts = [record(name, leg, source, identity, digest, StepContext(skipped, "false")) for leg in range(2)]
            assert len(verify(name, source, identity, digest, receipts, needs)) == len(cases)
            receipts[0]["scope"] = "true"
            refuse("contradictory skip scope", receipts, needs)
        assert len(cases) == sum(not setup(step) for step in original)
        print(f"{name}: {len(cases)} source gates retain their complete original steps")
    print("gate workflow and union controls: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
