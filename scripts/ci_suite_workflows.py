#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Materialize exhaustive case workers and one executed union job per parent."""

from __future__ import annotations

import copy

from ci_suite_pieces import PIECE_SECONDS
from suite_shards import WORKER_OVERHEAD_SECONDS


def inventory_dependencies() -> dict:
    """Inventory readers need the same pinned source lists as suite workers."""
    return {"name": "Fetch inventory dependencies",
            "run": "git submodule update --init third_party/verilog-axis protocol-processor "
                   "gptp-processor third_party/tsn-c-stack\n"}


def check_inventory_dependencies(source: dict) -> None:
    """Refuse any driver-inventory consumer without earlier pinned preparation."""
    readers = ("scripts/ci_suite_pieces.py", "scripts/ci_suite_collect.py",
               "scripts/ci_runtime_evidence.py collect", "scripts/ci_suite_pieces_selftest.py")
    preparation = inventory_dependencies()["run"].strip()
    for job_id, job in source["jobs"].items():
        prepared = False
        for step in job["steps"]:
            body = step.get("run", "")
            if body.strip() == preparation and "if" not in step and not step.get("continue-on-error"):
                prepared = True
            reads = any(reader in body for reader in readers) or (
                "scripts/run_all_suites.sh" in body and "--ci-pieces" in body)
            if reads and not prepared:
                raise ValueError(job_id + ": inventory reader lacks pinned dependency preparation")


def union_job(suite: str) -> dict:
    """Each union waits for the native matrix containing its driver-derived partitions."""
    needs = ["verilator-shards"]
    return {
        "name": "Union " + suite, "needs": ["full-ci-gate", *needs],
        "if": "${{ always() && needs.full-ci-gate.outputs.run_full == 'true' }}",
        "runs-on": "ubuntu-24.04", "timeout-minutes": 2,
        "steps": [
            {"uses": "actions/checkout@v4"},
            inventory_dependencies(),
            {"name": "Download executed case evidence", "uses": "actions/download-artifact@v4",
             "with": {"pattern": "suite-logs-*", "path": "${{ runner.temp }}/piece-logs"}},
            {"name": "Require successful owners and every case exactly once",
             "env": {"CASE_NEEDS": "${{ toJSON(needs) }}"},
             "run": """python3 - <<'PY'
import json, os
needs = json.loads(os.environ['CASE_NEEDS'])
assert all(row['result'] == 'success' for row in needs.values()), needs
PY
python3 scripts/ci_suite_pieces.py union """ + suite + """ \
  --head "$GITHUB_SHA" --tree "$(git rev-parse 'HEAD^{tree}')" \
  --output "$RUNNER_TEMP/union" "$RUNNER_TEMP"/piece-logs/suite-logs-*
"""},
            {"name": "Upload verified suite union", "uses": "actions/upload-artifact@v4",
             "with": {"name": "suite-union-" + suite, "path": "${{ runner.temp }}/union",
                      "if-no-files-found": "error", "retention-days": 3}},
        ],
    }


PREFLIGHT_JOB = "verilator-preflight"
PREFLIGHT_ARTIFACT = "suite-preflight"
#: The worker setup the preflight keeps: the same checkout and SHA record. Its
#: self-tests read no submodule and need no Verilator, Yosys, sv2v or tsn-gen:
#: `--preflight-only` passes in a tree exported without submodules.
PREFLIGHT_SETUP = ("Record the tree this worker validates",)


def preflight_job(worker: dict) -> dict:
    """The sweep's preflight self-tests once per head, beside the workers, which skip them.

    Every worker ran the same eight self-tests on the same tree before its suites. This job
    runs them once, in parallel with the workers so that its own setup is not on their
    critical path, and verilator-suites requires its success and its SHA record.
    Issue #998; REQ-VER-01 and REQ-VER-04."""
    steps = [{"uses": "actions/checkout@v4"}]
    for step in worker["steps"]:
        if step.get("name") in PREFLIGHT_SETUP:
            kept = copy.deepcopy(step)
            if kept["name"] == "Record the tree this worker validates":
                if kept["run"].count("/suite-logs") != 2:
                    raise ValueError("template worker's SHA record lacks its two suite-logs paths")
                kept["run"] = kept["run"].replace("/suite-logs", "/" + PREFLIGHT_ARTIFACT)
            steps.append(kept)
    if [step.get("name") for step in steps[1:]] != list(PREFLIGHT_SETUP):
        raise ValueError("template worker lacks the preflight's setup steps")
    steps += [
        {"name": "Run the sweep's preflight self-tests once for this head",
         "run": 'scripts/run_all_suites.sh "$RUNNER_TEMP/' + PREFLIGHT_ARTIFACT + '" --preflight-only\n'},
        {"name": "Upload this head's preflight logs", "if": "${{ always() }}",
         "uses": "actions/upload-artifact@v4",
         "with": {"name": PREFLIGHT_ARTIFACT, "path": "${{ runner.temp }}/" + PREFLIGHT_ARTIFACT,
                  "if-no-files-found": "error", "retention-days": 3}},
    ]
    return {"name": "Verilator preflight", "needs": worker["needs"], "if": worker["if"],
            "runs-on": worker["runs-on"], "timeout-minutes": 15, "steps": steps}


def preflight_checks() -> list[dict]:
    """verilator-suites' binding of the preflight: its artifact for this SHA, and its success."""
    return [
        {"name": "Download this head's preflight logs", "uses": "actions/download-artifact@v4",
         "continue-on-error": True,
         "with": {"name": PREFLIGHT_ARTIFACT, "path": "${{ runner.temp }}/" + PREFLIGHT_ARTIFACT}},
        {"name": "Require the preflight to have passed for this run's SHA", "if": "${{ always() }}",
         "env": {"GATE_SHA": "${{ needs.full-ci-gate.outputs.target_sha }}",
                 "PREFLIGHT_RESULT": "${{ needs." + PREFLIGHT_JOB + ".result }}"},
         "run": """python3 scripts/ci_events.py --require-target-sha --expect 1 \\
  --sha gate="$GATE_SHA" --sha run="$GITHUB_SHA" \\
  --sha checkout="$(git rev-parse HEAD)" -- "$RUNNER_TEMP/""" + PREFLIGHT_ARTIFACT + """"
if [ "$PREFLIGHT_RESULT" != success ]; then
  echo "the Verilator preflight ended: $PREFLIGHT_RESULT; no worker ran the self-tests" >&2
  exit 1
fi
echo "verilator-suites: the preflight self-tests passed once at $GITHUB_SHA"
"""},
    ]


def separate_yosys_build(source: dict) -> None:
    """Build the unchanged pinned tool once before the timed synthesis workers."""
    worker = source["jobs"]["yosys-shards"]
    build_names = {"Cache the pinned Yosys build", "Build Yosys from source on cache miss"}
    build_steps = [copy.deepcopy(step) for step in worker["steps"] if step.get("name") in build_names]
    if len(build_steps) != 2:
        raise ValueError("missing Yosys build recipe")
    source["jobs"]["yosys-tool"] = {
        "name": "Prepare pinned Yosys", "runs-on": "ubuntu-24.04", "timeout-minutes": 29,
        "needs": "full-ci-gate", "if": worker["if"],
        "steps": [{"uses": "actions/checkout@v4"}, *build_steps,
                  {"name": "Package the pinned Yosys build",
                   "run": 'tar -C /opt -czf "$RUNNER_TEMP/yosys.tar.gz" yosys\n'},
                  {"name": "Upload the pinned Yosys build", "uses": "actions/upload-artifact@v4",
                   "with": {"name": "pinned-yosys-${{ github.sha }}", "path": "${{ runner.temp }}/yosys.tar.gz",
                            "if-no-files-found": "error", "retention-days": 3}}]}
    worker["needs"] = ["full-ci-gate", "yosys-tool"]
    worker["steps"] = [step for step in worker["steps"] if step.get("name") not in build_names]
    position = next(index for index, step in enumerate(worker["steps"])
                    if step.get("name") == "Install the pinned Yosys and prove the version")
    worker["steps"][position:position] = [
        {"name": "Download the pinned Yosys build", "uses": "actions/download-artifact@v4",
         "with": {"name": "pinned-yosys-${{ github.sha }}", "path": "${{ runner.temp }}/yosys-tool"}},
        {"name": "Restore the pinned Yosys build",
         "run": 'sudo tar -C /opt -xzf "$RUNNER_TEMP/yosys-tool/yosys.tar.gz"\n'}]


def generate(source: dict) -> dict:
    """Retain source gates, install ownership and budgets while exposing case legs."""
    source = copy.deepcopy(source)
    total = len(WORKER_OVERHEAD_SECONDS)
    worker = source["jobs"]["verilator-shards"]
    # The template's own worker count names its dedicated milan_dp arm and verifier.
    template_total = worker["strategy"]["matrix"]["total"][0]
    dedicated_arm = (str(template_total - 1)
                     + ') test "$(cat "$RUNNER_TEMP/owned-suites")" = milan_dp ;;\n')
    template_expect = "--expect " + str(template_total)
    worker["strategy"]["matrix"] = {"shard": list(range(total)), "total": [total]}
    for step in worker["steps"]:
        if step.get("name") == "Prove specialized suite ownership":
            # Literal block indentation is removed by YAML; match the parsed body.
            if step["run"].count("  " + dedicated_arm) != 1:
                raise ValueError("template ownership step lacks its dedicated milan_dp arm")
            step["run"] = step["run"].replace("--shard", "--ci-pieces --shard").replace(
                "  " + dedicated_arm, "")
        if step.get("name") == "Run this exhaustive suite shard":
            step["run"] = step["run"].replace("--shard", "--ci-pieces --no-preflight --shard")
    worker["timeout-minutes"] = "${{ matrix.shard == " + str(total - 1) + " && 60 || 45 }}"
    jobs = {}
    for job_id, job in source["jobs"].items():
        if job_id == "verilator-shards":
            jobs[PREFLIGHT_JOB] = preflight_job(worker)
        jobs[job_id] = job
    source["jobs"] = jobs
    source["jobs"]["yosys-shards"]["timeout-minutes"] = 29
    separate_yosys_build(source)
    for suite in PIECE_SECONDS:
        source["jobs"]["union-" + suite] = union_job(suite)
    aggregate = source["jobs"]["verilator-suites"]
    aggregate["timeout-minutes"] = 3
    aggregate["needs"].extend("union-" + suite for suite in PIECE_SECONDS)
    aggregate["needs"].append(PREFLIGHT_JOB)
    # The original aggregate still verifies every worker's target SHA first.
    for step in aggregate["steps"]:
        if step.get("name") == "Require every shard to have validated this run's SHA":
            if step["run"].count(template_expect + " ") != 1:
                raise ValueError("template verifier lacks its worker-count expectation")
            step["run"] = step["run"].replace(template_expect + " ", "--expect " + str(total) + " ")
        if step.get("name") == "Prove exhaustive ownership and tally every log":
            step["run"] = """python3 scripts/ci_suite_collect.py \
  --workers "$RUNNER_TEMP/all-suite-logs" --unions "$RUNNER_TEMP/suite-unions" \
  --output "$RUNNER_TEMP/complete-suite-logs" --head "$GITHUB_SHA"
python3 scripts/suite_tally.py "$RUNNER_TEMP/complete-suite-logs" --quiet \
  --expect-suite-root tb/verilator
"""
    aggregate["steps"].insert(2, {
        "name": "Download verified suite unions", "uses": "actions/download-artifact@v4",
        "continue-on-error": True,
        "with": {"pattern": "suite-union-*", "path": "${{ runner.temp }}/suite-unions"},
    })
    aggregate["steps"].append({
        "name": "Require every case union to succeed", "if": "${{ always() }}",
        "env": {"UNION_NEEDS": "${{ toJSON(needs) }}"},
        "run": """python3 - <<'PY'
import json, os
needs = json.loads(os.environ['UNION_NEEDS'])
assert all(row['result'] == 'success' for row in needs.values()), needs
PY
""",
    })
    aggregate["steps"].insert(1, inventory_dependencies())
    aggregate["steps"].extend(preflight_checks())
    return source
