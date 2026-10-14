#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Append runtime evidence and same-repository cancellation to generated workflows."""

import copy
import json

import yaml

from ci_workflow_plan import expand_workflow, step_plan, matrix_rows, rendered_name

SAME_REPOSITORY = ("${{ github.event_name == 'push' || (github.event_name == 'pull_request' && "
                   "github.event.pull_request.head.repo.full_name == github.repository) }}")


def reader_setup() -> list[dict]:
    """Cache only hash-verified reader packages under their source and recipe identities."""
    return [{"name": "Cache pinned evidence reader downloads", "uses": "actions/cache@v4",
             "with": {"path": "~/.cache/pip",
                      "key": "pyyaml-6.0.2-d584d9ec91ad65861cc08d42e834324ef890a082e591037abe114850ff7bbc3e-"
                             "${{ hashFiles('ci/requirements-evidence.txt', 'scripts/ci_runtime_workflows.py', "
                             "'scripts/ci_gate_workflows.py', '.github/workflows/*.yml') }}-${{ runner.os }}"}},
            {"name": "Install the pinned evidence reader",
             "run": "python3 -m pip install --quiet --require-hashes --no-deps -r ci/requirements-evidence.txt\n"}]


def cpu_budget_step() -> dict:
    """Use each container's own affinity while preserving measured campaign limits."""
    return {"name": "Set CPU-derived job budgets", "run": """set -euo pipefail
cpus="$(nproc)"
test "$cpus" -gt 0
campaign=$(( cpus < 4 ? cpus : 4 ))
simulations=$(( cpus < 4 ? cpus : 4 ))
{
  printf 'CI_BUILD_JOBS=%s\\n' "$cpus"
  printf 'CI_CAMPAIGN_JOBS=%s\\n' "$campaign"
  printf 'VERILATOR_JOBS=%s\\n' "$cpus"
  printf 'SIM_JOBS=%s\\n' "$simulations"
  printf 'MAKEFLAGS=-j1 --no-print-directory\\n'
} >> "$GITHUB_ENV"
"""}


def instrument(path: str, job_id: str, job: dict) -> None:
    """Assign stable IDs without modifying any existing test command or condition."""
    if not any(step.get("uses", "").startswith("actions/checkout@") for step in job["steps"]):
        job["steps"].insert(0, {"uses": "actions/checkout@v4"})
    checkout = next(i for i, step in enumerate(job["steps"])
                    if step.get("uses", "").startswith("actions/checkout@"))
    job["steps"].insert(checkout + 1, cpu_budget_step())
    identity = ""
    if path == ".github/workflows/docs.yml" and job_id == "docs-check-no-git":
        job["steps"].insert(1, {
            "name": "Retain checkout identity before removing metadata",
            "run": 'python3 scripts/ci_runtime_evidence.py identify --output "$RUNNER_TEMP/job-source.json"\n'})
        identity = ' --identity "$RUNNER_TEMP/job-source.json"'
    for index, step in enumerate(job["steps"]):
        step.setdefault("id", "ci_step_" + str(index))
        step.setdefault("name", step_plan(step)["name"])
    slug = path.rsplit("/", 1)[-1].removesuffix(".yml")
    job["steps"].extend([
        {"name": "Record actual job execution", "id": "ci_record", "if": "${{ always() }}",
         "env": {"CI_STEP_RESULTS": "${{ toJSON(steps) }}", "CI_JOB_RESULT": "${{ job.status }}",
                 "CI_MATRIX": "${{ toJSON(matrix) }}"},
         "run": (f"python3 scripts/ci_runtime_evidence.py record --workflow {path} --job {job_id} "
                 '--output "$RUNNER_TEMP/job-evidence.json"' + identity + '\n')},
        {"name": "Upload actual job execution", "id": "ci_upload", "if": "${{ always() }}",
         "uses": "actions/upload-artifact@v4",
         "with": {"name": "job-evidence-" + slug + "-" + job_id + "-${{ strategy.job-index }}-${{ github.sha }}",
                  "path": "${{ runner.temp }}/job-evidence.json", "if-no-files-found": "error",
                  "retention-days": 3}},
    ])


def watcher(labels: list[str], skipped: dict) -> dict:
    """Only this guarded job requests write permission; fork events cannot enter it."""
    return {"name": "Fail fast across this head", "runs-on": "ubuntu-latest", "timeout-minutes": 120,
            "if": SAME_REPOSITORY, "permissions": {"contents": "read", "actions": "write"},
            "outputs": {"observer_only_error": "${{ steps.ci_observe.outputs.observer_error == 'true' && "
                        "steps.ci_record.outcome == 'success' && steps.ci_upload.outcome == 'success' }}"},
            "steps": [{"uses": "actions/checkout@v4"},
                      {"name": "Observe the first failed job", "id": "ci_observe",
                       "env": {"GH_TOKEN": "${{ github.token }}",
                               "EXPECTED_JOBS": json.dumps(labels, separators=(",", ":")),
                               "SKIPPED_MATRICES": json.dumps(skipped, separators=(",", ":"))},
                       "run": "python3 scripts/ci_fail_fast.py watch\n"},
                      {"name": "Cancel this run and sibling workflows",
                       "if": "${{ failure() && steps.ci_observe.outputs.observer_error != 'true' }}",
                       "env": {"GH_TOKEN": "${{ github.token }}"},
                       "run": "python3 scripts/ci_fail_fast.py cancel\n"}]}


def tail_guard() -> dict:
    """Observe terminal jobs after their final evidence steps, with no dependency cycle."""
    return {"name": "Cancel late CI failures", "runs-on": "ubuntu-latest", "timeout-minutes": 3,
            "if": "${{ always() && (github.event_name == 'push' || (github.event_name == 'pull_request' && "
                  "github.event.pull_request.head.repo.full_name == github.repository)) }}",
            "needs": ["ci-fail-fast", "ci-manifest"],
            "permissions": {"contents": "read", "actions": "write"},
            "steps": [{"uses": "actions/checkout@v4"}, cpu_budget_step(),
                      {"name": "Cancel confirmed terminal failures", "if": "${{ always() }}",
                       "env": {"GH_TOKEN": "${{ github.token }}", "CI_TAIL_NEEDS": "${{ toJSON(needs) }}"},
                       "run": "python3 scripts/ci_fail_fast.py tail\n"}]}


def collector(name: str, dependencies: list[str]) -> dict:
    """Use read-only API provenance on hosted runs and actual step receipts locally."""
    from ci_suite_workflows import inventory_dependencies
    return {"name": "Collect CI manifest", "runs-on": "ubuntu-latest", "timeout-minutes": 3,
            "if": "${{ always() && (github.event_name == 'push' || github.event_name == 'pull_request') }}",
            "needs": dependencies,
            "permissions": {"contents": "read", "actions": "read"},
            "steps": [
                {"uses": "actions/checkout@v4", "with": {"fetch-depth": 0}},
                cpu_budget_step(),
                inventory_dependencies(),
                *reader_setup(),
                {"name": "Download completed execution artifacts", "uses": "actions/download-artifact@v4",
                 "continue-on-error": True, "with": {"path": "${{ runner.temp }}/manifest-inputs"}},
                {"name": "Collect actual runtime evidence", "env": {"GH_TOKEN": "${{ github.token }}"},
                 "run": 'python3 scripts/ci_runtime_evidence.py collect --run "$GITHUB_RUN_ID" '
                        '--artifacts "$RUNNER_TEMP/manifest-inputs" --output "$RUNNER_TEMP/ci-manifest.json"\n'},
                {"name": "Upload canonical CI manifest", "if": "${{ always() }}",
                 "uses": "actions/upload-artifact@v4",
                 "with": {"name": "ci-manifest-" + name + "-${{ github.sha }}",
                          "path": "${{ runner.temp }}/ci-manifest.json", "if-no-files-found": "error",
                          "retention-days": 3}},
            ]}


def generate(name: str, source: dict) -> dict:
    """Keep hosted matrices intact and put collection after every original job."""
    source = copy.deepcopy(source)
    path = ".github/workflows/" + name + ".yml"
    source["jobs"]["ci-manifest"] = collector(name, list(source["jobs"]))
    _, labels = expand_workflow(path, yaml.safe_dump(source))
    skipped = {job.get("name", job_id): [rendered_name(job_id, job, row) for row in matrix_rows(job)]
               for job_id, job in source["jobs"].items() if "matrix" in job.get("strategy", {})}
    source["jobs"]["ci-fail-fast"] = watcher(list(labels.values()), skipped)
    for job_id, job in source["jobs"].items():
        if job_id != "ci-manifest":
            instrument(path, job_id, job)
    source["jobs"]["ci-cancel-tail"] = tail_guard()
    return source
