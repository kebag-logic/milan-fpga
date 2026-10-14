#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Generate parallel gate jobs from the original, contract-checked step inventory.

Templates retain the ordered commands and setup. The generator schedules existing
steps, assigns receipt identifiers and adds a fail-closed public aggregate.
"""

from __future__ import annotations

import argparse
import copy
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CARRIERS = {"docs": "docs-check", "elaborate": "elaborate"}
TEMPLATES = {name: ".github/ci-templates/" + name + ".yml"
             for name in (*CARRIERS, "rtl", "rtl-fast")}
LONG_GATE = {"docs": "End-station builder gates", "elaborate": "Standalone LiteX simulation aggregate"}
CONTRACT_GATES = {"CI event and SHA contract gate", "Local act runner contract gate"}
VERILATOR_SETUP = {"Cache the pinned Verilator build", "Build Verilator from source on cache miss",
                   "Put Verilator on PATH and prove the version"}
SETUP_PREFIXES = ("Install ", "Cache ", "Fetch ", "Apply ", "Place ", "Put ", "Keep ")


class Dumper(yaml.SafeDumper):
    """Each generated step owns its mapping; never emit YAML reference aliases."""

    def increase_indent(self, flow: bool = False, indentless: bool = False) -> None:
        """Keep source-like nested step indentation for dependency readers."""
        return super().increase_indent(flow, False)

    def ignore_aliases(self, _data: object) -> bool:
        """Keep generated workflow identities explicit."""
        return True


def represent_text(dumper: Dumper, value: str) -> yaml.ScalarNode:
    """Keep full shell scripts as literal blocks, preserving their exact text."""
    return dumper.represent_scalar("tag:yaml.org,2002:str", value,
                                   style="|" if "\n" in value else None)


Dumper.add_representer(str, represent_text)


def setup(step: dict) -> bool:
    """Identify the existing setup steps; all other template steps belong to the union."""
    uses = step.get("uses", "")
    return (uses.startswith(("actions/checkout@", "actions/setup-", "actions/cache@"))
            or step.get("id") == "scope"
            or step.get("name", "").startswith(SETUP_PREFIXES)
            or step.get("name") == "Build Verilator from source on cache miss")


def case_inventory(name: str, template: dict) -> list[dict]:
    """Derive gate identities and leg membership from the original ordered steps."""
    original = template["jobs"][CARRIERS[name]]["steps"]
    cases = [{"id": "gate_" + str(index), "index": index,
              "name": step.get("name", "Run " + step.get("uses", "")),
              "condition": step.get("if", "success()"),
              "leg": (2 if name == "docs" and step.get("name") in CONTRACT_GATES
                      else int(step.get("name") == LONG_GATE[name]))}
             for index, step in enumerate(original) if not setup(step)]
    if sum(case["leg"] == 1 for case in cases) != 1 or not any(case["leg"] == 0 for case in cases):
        raise ValueError(name + ": missing or ambiguous measured long gate")
    if len({case["name"] for case in cases}) != len(cases):
        raise ValueError(name + ": duplicate gate names")
    return cases


def worker_legs(name: str, template: dict) -> list[int]:
    """Derive every required worker from the original gate inventory."""
    return sorted({case["leg"] for case in case_inventory(name, template)})


def worker_id(name: str, leg: int) -> str:
    """A concrete job the public carrier must require."""
    return name + "-gates-" + str(leg)


def collection_steps(name: str, leg: int) -> list[dict]:
    """Observe completed source steps even on failure, then retain the actual evidence."""
    destination = "$RUNNER_TEMP/gate-results/receipt.json"
    return [
        {"name": "Record executed gate outcomes", "if": "${{ always() }}",
         "env": {"CI_GATE_STEPS": "${{ toJSON(steps) }}",
                 "CI_GATE_SCOPE": "${{ steps.scope.outputs.rtl }}"},
         "run": ("python3 scripts/ci_gate_receipts.py record --workflow " + name
                 + " --leg " + str(leg) + ' --output "' + destination + '"\n')},
        {"name": "Upload executed gate outcomes", "if": "${{ always() }}",
         "uses": "actions/upload-artifact@v4",
         "with": {"name": "gate-" + name + "-" + str(leg) + "-${{ github.sha }}",
                  "path": "${{ runner.temp }}/gate-results/receipt.json",
                  "if-no-files-found": "error"}},
    ]


def aggregate(name: str, template: dict) -> dict:
    """Retain the protected name, requiring both successful jobs and the actual union."""
    from ci_runtime_workflows import reader_setup
    checkout = copy.deepcopy(template["jobs"][CARRIERS[name]]["steps"][0])
    if not str(checkout.get("uses", "")).startswith("actions/checkout@"):
        raise ValueError(name + ": original checkout must stay first")
    return {"runs-on": "ubuntu-latest", "timeout-minutes": 3,
            "needs": [worker_id(name, leg) for leg in worker_legs(name, template)], "if": "${{ always() }}",
            "steps": [checkout, *reader_setup(),
                      {"name": "Download executed gate outcomes", "uses": "actions/download-artifact@v4",
                       "continue-on-error": True,
                       "with": {"pattern": "gate-" + name + "-*-${{ github.sha }}",
                                "path": "${{ runner.temp }}/gate-results"}},
                      {"name": "Require every gate exactly once",
                       "env": {"CI_GATE_NEEDS": "${{ toJSON(needs) }}"},
                       "run": ("python3 scripts/ci_gate_receipts.py verify --workflow " + name
                               + ' --root "$RUNNER_TEMP/gate-results" --head "$GITHUB_SHA"'
                               + ' --output "$RUNNER_TEMP/gate-union.json"\n')},
                      {"name": "Upload verified gate union", "uses": "actions/upload-artifact@v4",
                       "with": {"name": "gate-union-" + name + "-${{ github.sha }}",
                                "path": "${{ runner.temp }}/gate-union.json", "if-no-files-found": "error"}}]
            }


def gate_graph(name: str, template: dict) -> dict:
    """Preserve ordered bodies, conditions, bindings and source checkout in each leg."""
    source = copy.deepcopy(template)
    if True in source:
        source["on"] = source.pop(True)
    if name not in CARRIERS:
        if name == "rtl":
            from ci_suite_workflows import generate as suite_workflows
            return suite_workflows(source)
        return source
    original = source["jobs"].pop(CARRIERS[name])
    cases = {case["index"]: case for case in case_inventory(name, template)}
    for leg in worker_legs(name, template):
        worker = {key: copy.deepcopy(value) for key, value in original.items() if key != "steps"}
        worker["timeout-minutes"] = 45
        worker["steps"] = []
        for index, step in enumerate(original["steps"]):
            case = cases.get(index)
            if case and case["leg"] != leg:
                continue
            if name == "elaborate" and step.get("name") in VERILATOR_SETUP and leg != 1:
                continue
            kept = copy.deepcopy(step)
            if case:
                if "id" in kept:
                    raise ValueError(name + ": gate already has an output identifier")
                kept["id"] = case["id"]
            worker["steps"].append(kept)
        worker["steps"].extend(collection_steps(name, leg))
        source["jobs"][worker_id(name, leg)] = worker
    source["jobs"][CARRIERS[name]] = aggregate(name, template)
    return source



def generate(name: str, template: dict) -> dict:
    """Add runtime collection after deriving the unchanged gate schedule."""
    from ci_runtime_workflows import generate as runtime_workflows
    from ci_install_workflows import generate as install_workflows
    from ci_suite_workflows import check_inventory_dependencies
    result = runtime_workflows(name, install_workflows(gate_graph(name, template)))
    check_inventory_dependencies(result)
    return result


def load_template(root: Path, name: str) -> dict:
    """Read the source inventory; the workflow contract also validates every original step."""
    value = yaml.safe_load(root.joinpath(TEMPLATES[name]).read_text())
    if not isinstance(value, dict):
        raise ValueError(name + ": template must be a mapping")
    return value


def rendered(name: str, template: dict) -> str:
    """Only this generator writes the derived hosted workflow."""
    value = generate(name, template)
    if True in value:
        value["on"] = value.pop(True)
    return ("# Generated by scripts/ci_gate_workflows.py from " + TEMPLATES[name] + ".\n"
            + "# Edit the template and regenerate; original commands remain contract-checked.\n"
            + yaml.dump(value, Dumper=Dumper, sort_keys=False, width=100))


def main() -> int:
    """Regenerate, or fail when a checked-in generated workflow has drifted."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    failed = False
    for name in TEMPLATES:
        target = args.root / ".github/workflows" / (name + ".yml")
        expected = rendered(name, load_template(args.root, name))
        if args.check:
            if target.read_text() != expected:
                print(str(target.relative_to(args.root)) + ": regenerate the gate jobs")
                failed = True
        else:
            target.write_text(expected)
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
