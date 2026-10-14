#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Collect actual step contexts and API outcomes without filling gaps with success.

Round-one artifacts are explicitly incomplete while image pins, authenticated
provenance and the final collector's own completed result are unavailable.
The final API readback can collect several completed workflow run IDs together.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

from ci_fail_fast import API, RETRY_BUDGET_SECONDS, observer_error
from ci_manifest import SHA1, canonical, envelope, exact_keys, read, require_digest

ROOT = Path(__file__).resolve().parents[1]
PROBES = {"python3": ["--version"], "verilator": ["--version"], "yosys": ["-V"],
          "make": ["--version"], "g++": ["--version"], "node": ["--version"]}


def git(*args: str) -> str:
    """Read committed identity without treating generated report timestamps as inputs."""
    return subprocess.check_output(["git", "--no-replace-objects", *args], cwd=ROOT, text=True).strip()


def file_digest(path: Path) -> str:
    """Hash large tool binaries with bounded memory."""
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def measured_tools() -> dict:
    """Measure only tools actually present; unknown source provenance stays unknown."""
    results = {}
    for name, arguments in PROBES.items():
        executable = shutil.which(name)
        if not executable:
            continue
        result = subprocess.run([executable, *arguments], capture_output=True, text=True,
                                check=False, timeout=20)
        if result.returncode:
            continue
        version = (result.stdout + result.stderr).splitlines()
        if version:
            results[name] = {"version": version[0], "binary_sha256": file_digest(Path(executable)),
                             "source_sha256": None, "recipe_sha256": None}
    return results


def source_identity() -> dict:
    """Read the actual checkout before a gate intentionally removes its Git metadata."""
    return {"head": git("rev-parse", "HEAD"), "tree": git("rev-parse", "HEAD^{tree}")}


def retained_identity(path: Path, workflow_path: str, job: str) -> dict:
    """Only the no-metadata gate may use its earlier checkout observation."""
    if (workflow_path, job) != (".github/workflows/docs.yml", "docs-check-no-git"):
        raise ValueError("retained identity is only valid for the no-metadata gate")
    value = read(path)
    exact_keys(value, {"head", "tree"}, "retained identity")
    for field in value:
        require_digest(value[field], SHA1, "retained identity." + field)
    if value["head"] != os.environ.get("GITHUB_SHA"):
        raise ValueError("retained checkout identity differs from this run")
    return value


def record(path: Path, workflow_path: str, job: str, identity: Path | None = None) -> None:
    """Retain runtime step outcomes and measured tools before the artifact upload."""
    source = source_identity() if identity is None else retained_identity(identity, workflow_path, job)
    value = {**source,
             "workflow": workflow_path, "job": job,
             "matrix": json.loads(os.environ.get("CI_MATRIX") or "{}") or {},
             "steps": json.loads(os.environ["CI_STEP_RESULTS"]),
             "result": os.environ["CI_JOB_RESULT"], "tools": measured_tools()}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical(value) + b"\n")


def step_records(source: dict, job: dict, observed: dict) -> list[dict]:
    """Join actual contexts by explicit IDs; missing steps remain unknown."""
    result = []
    for definition, step in zip(source["steps"], job["steps"]):
        actual = observed.get(step.get("id", ""), {})
        outcome = actual.get("outcome", "unknown")
        result.append({"name": definition["name"], "outcome": outcome,
                       "skip_reason": definition["condition"] if outcome == "skipped" else None})
    return result


def context_evidence(source: dict, artifacts: Path) -> tuple[dict, dict, dict]:
    """Local execution evidence comes from each job's actual step context."""
    from ci_workflow_plan import workflow
    execution, results, tools = {}, {}, {}
    definitions = {}
    for path in artifacts.rglob("job-evidence.json"):
        receipt = read(path)
        matrix = receipt["matrix"]
        key = receipt["workflow"] + ":" + receipt["job"]
        if matrix:
            key += "[" + canonical(matrix).decode() + "]"
        if key not in source["plan"] or key in execution:
            raise ValueError("unknown or duplicate runtime job receipt: " + key)
        if receipt["head"] != source["head"] or receipt["tree"] != source["tree"]:
            raise ValueError("runtime receipt source identity differs")
        filename = receipt["workflow"]
        if filename not in definitions:
            definitions[filename] = workflow(git("show", source["head"] + ":" + filename))
        job = definitions[filename]["jobs"][receipt["job"]]
        execution[key] = step_records(source["plan"][key], job, receipt["steps"])
        results[key] = receipt["result"]
        if any(step.get("outputs", {}).get("observer_error") == "true" for step in receipt["steps"].values()):
            results[key] = "unknown"
        tools.update({key + "/" + name: value for name, value in receipt["tools"].items()})
    return execution, results, tools


def api_evidence(source: dict, jobs: list[dict], path: str) -> tuple[dict, dict]:
    """Use API conclusions for exact source step names; unknown outcomes stay unknown."""
    execution, results = {}, {}
    labels = {label: key for key, label in source["labels"].items()
              if source["plan"][key]["workflow"] == path}
    skipped = source.get("skipped", {}).get(path, {})
    for job in jobs:
        if job["name"] in skipped:
            if job.get("status") != "completed" or job.get("conclusion") != "skipped" or job.get("steps"):
                raise ValueError("API returned an invalid unexpanded matrix state")
            for label in skipped[job["name"]]:
                key = labels[label]
                if key in results:
                    raise ValueError("API expanded and unexpanded matrix jobs overlap")
                execution[key] = [{"name": step["name"], "outcome": "skipped",
                                   "skip_reason": source["plan"][key]["condition"]}
                                  for step in source["plan"][key]["steps"]]
                results[key] = "skipped"
            continue
        if job["name"] not in labels:
            raise ValueError("API returned an unplanned job: " + job["name"])
        key = labels[job["name"]]
        if key in results:
            raise ValueError("API returned duplicate current-attempt job")
        planned = source["plan"][key]["steps"]
        actual = [step for step in job.get("steps", [])
                  if step["name"] not in ("Set up job", "Complete job")
                  and not step["name"].startswith("Post ")]
        rows = []
        for index, step in enumerate(planned):
            observed = actual[index] if index < len(actual) else {}
            if observed and observed["name"] != step["name"]:
                raise ValueError(key + ": API step ordering or name differs")
            outcome = observed.get("conclusion") or "unknown"
            rows.append({"name": step["name"], "outcome": outcome,
                         "skip_reason": step["condition"] if outcome == "skipped" else None})
        if len(actual) > len(planned):
            raise ValueError(key + ": API returned extra executable steps")
        execution[key] = rows
        results[key] = job.get("conclusion") or "unknown"
    return execution, results


def suite_evidence(source: dict, artifacts: Path) -> dict:
    """Collect completed union receipts; absence can never become an empty success."""
    from ci_suite_pieces import PIECE_SECONDS, inventory
    from ci_gate_workflows import CARRIERS, case_inventory, load_template
    result = {}
    for path in [*artifacts.rglob("union.json"), *artifacts.rglob("gate-union.json")]:
        receipt = read(path)
        suite = receipt["suite"]
        if suite not in {*PIECE_SECONDS, *("gate/" + name for name in CARRIERS)} or suite in result:
            raise ValueError("unknown or duplicated suite union")
        if receipt["head"] != source["head"] or receipt["tree"] != source["tree"]:
            raise ValueError("suite union source identity differs")
        if suite.startswith("gate/"):
            name = suite.removeprefix("gate/")
            expected = [case["id"] for case in case_inventory(name, load_template(ROOT, name))]
        else:
            expected = inventory(suite)
        if receipt["inventory"] != expected:
            raise ValueError("suite union inventory differs from driver")
        result[suite] = {"expected": receipt["inventory"],
                         "legs": {row["shard"]: row["cases"] for row in receipt["legs"]},
                         "union": "success" if receipt["union"] == "pass" else "failure",
                         "verdicts_sha256": receipt["verdicts_sha256"]}
    return result


def collect_api(source: dict, event: dict, run_ids: list[int]) -> tuple[dict, dict]:
    """Bound all API reads together; malformed evidence still fails collection."""
    api = API(os.environ["GITHUB_REPOSITORY"], os.environ["GH_TOKEN"], RETRY_BUDGET_SECONDS)
    execution, results = {}, {}
    for run_id in run_ids:
        run = api.request(f"runs/{run_id}")
        expected = (event["pull_request"]["head"]["sha"]
                    if os.environ["GITHUB_EVENT_NAME"] == "pull_request" else source["head"])
        if run["head_sha"] != expected:
            raise ValueError("API run belongs to another head")
        observed, outcomes = api_evidence(source, api.pages(f"runs/{run_id}/jobs?filter=latest", "jobs"),
                                         run["path"].split("@")[0])
        execution.update(observed)
        results.update(outcomes)
    return execution, results


def collect(artifacts: Path, output: Path, run_ids: list[int]) -> dict:
    """Build one canonical envelope, explicitly retaining incomplete observations."""
    from ci_workflow_plan import committed_plan, workflow
    source = committed_plan(ROOT, git("rev-parse", "HEAD"))
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    subject = {"repository": os.environ["GITHUB_REPOSITORY"], "head": source["head"],
               "tree": source["tree"], "event": os.environ["GITHUB_EVENT_NAME"]}
    if subject["event"] == "pull_request":
        subject["base"] = event["pull_request"]["base"]["sha"]
        subject["merge_base"] = git("merge-base", subject["base"], subject["head"])
    execution, results, tools = context_evidence(source, artifacts)
    observer_jobs = [key for key, result in results.items() if result == "unknown"]
    observation_error = None
    if run_ids:
        try:
            observed, outcomes = collect_api(source, event, run_ids)
            execution.update(observed)
            results.update(outcomes)
        except OSError as exc:
            observer_error(exc)
            observation_error = type(exc).__name__
            # An unobserved terminal result cannot authenticate any completed job.
            results = {key: "unknown" for key in source["plan"]}
    for key in observer_jobs:
        results[key] = "unknown"
    actions = sorted({step["uses"] for path in source["definitions"]
                      for job in workflow(git("show", source["head"] + ":" + path))["jobs"].values()
                      for step in job["steps"] if "uses" in step})
    payload = {"subject": subject, "definitions": source["definitions"], "plan": source["plan"],
               "environment": {"image": None, "tools": tools, "actions": actions},
               "execution": execution, "results": results, "inventories": suite_evidence(source, artifacts)}
    document = envelope(payload, {"logs": {"observer_error": observation_error}} if observation_error else {})
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(canonical(document) + b"\n")
    print("complete manifest" if document["complete"] else "incomplete manifest: " +
          "; ".join(document["incomplete_reasons"]))
    return document


def main() -> int:
    """Record a job or collect completed artifacts/API observations inside the job boundary."""
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_subparsers(dest="mode", required=True)
    identify = modes.add_parser("identify")
    identify.add_argument("--output", type=Path, required=True)
    job = modes.add_parser("record")
    job.add_argument("--workflow", required=True)
    job.add_argument("--job", required=True)
    job.add_argument("--output", type=Path, required=True)
    job.add_argument("--identity", type=Path)
    manifest = modes.add_parser("collect")
    manifest.add_argument("--artifacts", type=Path, required=True)
    manifest.add_argument("--output", type=Path, required=True)
    manifest.add_argument("--run", action="append", type=int, default=[])
    args = parser.parse_args()
    try:
        if args.mode == "identify":
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_bytes(canonical(source_identity()) + b"\n")
        elif args.mode == "record":
            record(args.output, args.workflow, args.job, args.identity)
        else:
            collect(args.artifacts, args.output, [] if os.environ.get("ACT") == "true" else args.run)
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(f"runtime collection refused: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
