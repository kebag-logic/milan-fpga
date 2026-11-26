#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Divide slow fast-workflow jobs without changing their public result bindings.

Issue #1008; REQ-VER-01 and REQ-VER-04. The templates retain complete commands.
Each matrix keeps native fail-fast on every event, including forks. Runtime
receipts and the existing aggregate bind every concrete matrix job.
"""

from __future__ import annotations

import copy


#: Each mutation job's legs, from its campaign step's largest hosted window over the 20 measured runs, under
#: 1276 s a leg with its setup: control 2402 s, AECP 1554 s, SRP 1789 s (docs/testing/CI_WORKFLOWS.md).
CAMPAIGNS = {"firmware-control-mutants": 4, "firmware-aecp-mutants": 2, "firmware-srp-mutants": 2}


def generate(workflow: dict) -> dict:
    """Give each campaign an exhaustive matrix, preserving its job identity."""
    for name, count in CAMPAIGNS.items():
        job = workflow["jobs"][name]
        if "strategy" in job:
            raise ValueError(name + ": unexpected existing strategy")
        job["strategy"] = {"fail-fast": True, "matrix": {"leg": list(range(count))}}
        commands = [step for step in job["steps"] if "--shard " in step.get("run", "")]
        if len(commands) != 1:
            raise ValueError(name + ": expected one complete firmware phase")
        commands[0]["run"] = (commands[0]["run"].rstrip()
                              + ' --campaign-shard "${{ matrix.leg }}" ' + str(count) + "\n")
    census(workflow)
    unit(workflow)
    return workflow


def require_child(workflow: dict, parent: str, child: str) -> None:
    """The fast aggregate must reject a failed child even when its parent was skipped."""
    aggregate = workflow["jobs"]["rtl-fast"]
    aggregate["needs"].insert(aggregate["needs"].index(parent), child)
    step = aggregate["steps"][0]
    parent_env = parent.upper().replace("-", "_") + "_RESULT"
    child_env = child.upper().replace("-", "_") + "_RESULT"
    if parent_env not in step["env"]:
        raise ValueError("fast aggregate lacks the parent's result")
    step["env"] = {key: value for name, binding in step["env"].items()
                   for key, value in ([(child_env, "${{ needs." + child + ".result }}")] if name == parent_env else [])
                   + [(name, binding)]}
    before = '"' + parent + ':$' + parent_env + '" \\'
    lines = step["run"].split("\n")
    found = [index for index, line in enumerate(lines) if line.strip() == before]
    if len(found) != 1:
        raise ValueError("fast aggregate lacks the parent's unique result pair")
    line = lines[found[0]]
    lines.insert(found[0], line[:len(line) - len(line.lstrip())] + '"' + child + ':$' + child_env + '" \\')
    step["run"] = "\n".join(lines)


def census(workflow: dict) -> None:
    """Run complete shapes and self-test legs beside each other, then judge every rule."""
    from pathlib import Path
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "sw/mailbox"))
    from census_legs import LEGS
    jobs = workflow["jobs"]
    parent = jobs["publication-census"]
    child = "publication-census-legs"
    worker = copy.deepcopy(parent)
    worker["strategy"] = {"fail-fast": True, "matrix": {"leg": list(range(LEGS))}}
    command = [step for step in worker["steps"] if "publication_census.py --check" in step.get("run", "")]
    if len(command) != 1:
        raise ValueError("census must have one complete driver command")
    command[0]["run"] = ("set -euo pipefail\npython3 -m pip install --quiet pyyaml\n"
                         'python3 sw/mailbox/census_legs.py run --leg "${{ matrix.leg }}" '
                         '--jobs "$CI_CENSUS_JOBS" --receipt "$RUNNER_TEMP/census-leg-${{ matrix.leg }}.json"\n')
    worker["steps"].append({"name": "Upload executed census arms", "if": "${{ always() }}",
                             "uses": "actions/upload-artifact@v4", "with": {
                                 "name": "census-leg-${{ matrix.leg }}-${{ github.sha }}",
                                 "path": "${{ runner.temp }}/census-leg-${{ matrix.leg }}.json",
                                 "if-no-files-found": "error", "retention-days": 3}})
    # A job of its own, its legs' 30 minutes the owner's hosted budget, scheduled just before its judge.
    worker["timeout-minutes"] = 30
    ordered = {}
    for job_id, job in jobs.items():
        if job_id == "publication-census":
            ordered[child] = worker
        ordered[job_id] = job
    workflow["jobs"] = jobs = ordered
    parent["needs"] = ["changes", child]
    # The judge needs source bytes and the reader only; every elaboration is in the workers.
    parent["steps"] = [copy.deepcopy(step) for step in parent["steps"]
                       if step.get("uses", "").startswith("actions/checkout@")
                       or step.get("name") == "Fetch RTL dependencies"]
    parent["steps"] += [
        {"name": "Install census reader", "run": "python3 -m pip install --quiet pyyaml\n"},
        {"name": "Download executed census arms", "uses": "actions/download-artifact@v4", "with": {
            "pattern": "census-leg-*-${{ github.sha }}", "path": "${{ runner.temp }}/census-results"}},
        {"name": "Judge the complete publication census", "run":
            'python3 sw/mailbox/census_legs.py union --root "$RUNNER_TEMP/census-results"\n'}]
    require_child(workflow, "publication-census", child)


def unit(workflow: dict) -> None:
    """Keep each complete unit/coverage phase on its own matrix worker (#1008)."""
    phases = {
        "Prove the tally reads a failing and a crashing test as failures": 0,
        "Run the control-plane firmware suites and RV32 builds": 0,
        "Run the saved-state store suites and its RV32 build": 1,
        "Hold the firmware coverage ratchet": 2,
    }
    job = workflow["jobs"]["firmware-unit"]
    if "strategy" in job:
        raise ValueError("firmware-unit: unexpected existing strategy")
    found = set()
    for step in job["steps"]:
        name = step.get("name")
        if name in phases:
            if "if" in step:
                raise ValueError(name + ": unexpected existing condition")
            step["if"] = "${{ matrix.leg == " + str(phases[name]) + " }}"
            found.add(name)
    if found != set(phases):
        raise ValueError("firmware-unit: missing complete phase")
    job["strategy"] = {"fail-fast": True, "matrix": {"leg": [0, 1, 2]}}
