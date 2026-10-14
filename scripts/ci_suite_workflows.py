#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Materialize exhaustive case workers and one executed union job per parent."""

from __future__ import annotations

import copy

from ci_suite_pieces import PIECE_SECONDS
from suite_shards import WORKER_OVERHEAD_SECONDS


def union_job(suite: str) -> dict:
    """Each union waits for the native matrix containing its driver-derived partitions."""
    needs = ["verilator-shards"]
    return {
        "name": "Union " + suite, "needs": ["full-ci-gate", *needs],
        "if": "${{ always() && needs.full-ci-gate.outputs.run_full == 'true' }}",
        "runs-on": "ubuntu-latest", "timeout-minutes": 2,
        "steps": [
            {"uses": "actions/checkout@v4"},
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


def generate(source: dict) -> dict:
    """Retain source gates, install ownership and budgets while exposing case legs."""
    source = copy.deepcopy(source)
    total = len(WORKER_OVERHEAD_SECONDS)
    worker = source["jobs"]["verilator-shards"]
    worker["strategy"]["matrix"] = {"shard": list(range(total)), "total": [total]}
    for step in worker["steps"]:
        if step.get("name") == "Prove specialized suite ownership":
            step["run"] = step["run"].replace("--shard", "--ci-pieces --shard").replace(
                '            4) test "$(cat "$RUNNER_TEMP/owned-suites")" = milan_dp ;;\n', "")
            # Literal block indentation is removed by YAML; match the parsed body.
            step["run"] = step["run"].replace(
                '  4) test "$(cat "$RUNNER_TEMP/owned-suites")" = milan_dp ;;\n', "")
        if step.get("name") == "Run this exhaustive suite shard":
            step["run"] = step["run"].replace("--shard", "--ci-pieces --shard")
    worker["timeout-minutes"] = "${{ matrix.shard == " + str(total - 1) + " && 60 || 29 }}"
    source["jobs"]["yosys-shards"]["timeout-minutes"] = 29
    for suite in PIECE_SECONDS:
        source["jobs"]["union-" + suite] = union_job(suite)
    aggregate = source["jobs"]["verilator-suites"]
    aggregate["timeout-minutes"] = 3
    aggregate["needs"].extend("union-" + suite for suite in PIECE_SECONDS)
    # The original aggregate still verifies every worker's target SHA first.
    for step in aggregate["steps"]:
        if step.get("name") == "Require every shard to have validated this run's SHA":
            step["run"] = step["run"].replace("--expect 5", "--expect " + str(total))
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
    return source
