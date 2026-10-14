#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Compare independent API and scheduler observations and plant runtime gaps."""

import copy
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from unittest.mock import patch

from ci_local_manifest import artifact_rows, collect, observations
from ci_manifest import compare, validate
import ci_runtime_evidence as runtime
from ci_runtime_evidence import api_evidence
from ci_runtime_workflows import SAME_REPOSITORY, generate
from ci_workflow_plan import committed_plan, expand_workflow, workflow
from ci_workflow_plan_selftest import PATH, SOURCE, fixture_commit


def streams(source: dict) -> tuple[list[dict], list[dict]]:
    """Independent transports report the same declared jobs and completed steps."""
    events, api = [], []
    for key, entry in source["plan"].items():
        label = source["labels"][key]
        row = {"job": "fixtures/" + label, "jobID": entry["job"], "matrix": entry["matrix"]}
        steps = []
        for index, step in enumerate(entry["steps"]):
            events.append({**row, "stepID": [str(index)], "stage": "Main", "stepResult": "success"})
            steps.append({"name": step["name"], "conclusion": "success"})
        events.append({**row, "jobResult": "success"})
        api.append({"name": label, "conclusion": "success",
                    "steps": [{"name": "Set up job", "conclusion": "success"}, *steps,
                              {"name": "Complete job", "conclusion": "success"}]})
    return events, api


def refused(action: object, label: str) -> None:
    """A planted transport change must reach a production refusal."""
    try:
        action()
    except (ValueError, KeyError):
        print("runtime control refused:", label)
    else:
        raise AssertionError("accepted " + label)


def transport_controls(source: dict) -> None:
    """No duplicate, extra, missing or reordered observation can become success."""
    events, api = streams(source)
    definitions = {PATH: workflow(SOURCE)}
    execution, results = observations(source, definitions, events, False)
    assert (execution, results) == api_evidence(source, api, PATH)
    for key, value in (("jobID", "extra"), ("matrix", {"index": 99}), ("job", "other/start")):
        changed = copy.deepcopy(events)
        changed[0][key] = value
        refused(lambda: observations(source, definitions, changed, False), "scheduler " + key)
    refused(lambda: observations(source, definitions, events + [events[-1]], False), "duplicate job conclusion")
    refused(lambda: observations(source, definitions, events + [events[0]], False), "duplicate step conclusion")
    for change in ("extra", "name", "duplicate"):
        changed = copy.deepcopy(api)
        if change == "extra":
            changed[0]["steps"].insert(1, {"name": "unplanned command", "conclusion": "success"})
        elif change == "name":
            changed[0]["name"] = "unplanned job"
        else:
            changed.append(changed[0])
        refused(lambda: api_evidence(source, changed, PATH), "API " + change)
    missing = copy.deepcopy(api)
    missing[0]["steps"] = []
    assert api_evidence(source, missing, PATH)[0][next(iter(source["plan"]))][0]["outcome"] == "unknown"
    partial = [events[0], {**events[1], "jobResult": "failure"}, events[2]]
    _, incomplete = observations(source, definitions, partial, True)
    assert list(incomplete.values()).count("failure") == 1
    assert list(incomplete.values()).count("cancelled") == 1
    assert list(incomplete.values()).count("not_run") == len(source["plan"]) - 2
    started = {key: events[2][key] for key in ("job", "jobID", "matrix")}
    _, before_step = observations(source, definitions, [partial[1], {**started, "jobStarted": True}], True)
    assert list(before_step.values()).count("cancelled") == 1
    assert list(before_step.values()).count("failure") == 1
    print("runtime controls: API and scheduler agree; cancellation retains missing work")


def isolated_reader(root: Path, subject: dict, events: Path, artifacts: Path, expected: dict) -> None:
    """Execute the pinned reader with hostile candidate import paths and a changed-helper control."""
    source = Path(__file__).resolve().parent
    syntax = ast.parse(source.joinpath("act_ci.py").read_text())
    assignment = next(node for node in syntax.body if isinstance(node, ast.Assign)
                      and any(isinstance(target, ast.Name) and target.id == "EVIDENCE_HELPERS"
                              for target in node.targets))
    pins = ast.literal_eval(assignment.value)
    directory = root / "readers"
    directory.mkdir()
    for name, digest in pins.items():
        raw = source.joinpath(name).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == digest
        directory.joinpath(name).write_bytes(raw)
    pin_file, subject_file, output = directory / "pins.json", directory / "subject.json", directory / "result.json"
    pin_file.write_text(json.dumps(pins))
    subject_file.write_text(json.dumps(subject))
    poison = root / "candidate-imports"
    poison.mkdir()
    poison.joinpath("ci_manifest.py").write_text("raise RuntimeError('candidate code executed on collector')\n")
    command = [sys.executable, "-I", "-X", "pycache_prefix=" + str(directory / "cache"),
               str(directory / "ci_local_manifest.py"), "--pins", str(pin_file), "--subject", str(subject_file),
               "--root", str(root), "--events", str(events), "--artifacts", str(artifacts), "--output", str(output)]
    environment = dict(os.environ, PYTHONPATH=str(poison))
    subprocess.run(command, cwd=poison, env=environment, check=True, capture_output=True, text=True)
    assert json.loads(output.read_text()) == expected
    helper = directory / "ci_manifest.py"
    helper.write_bytes(helper.read_bytes() + b"\n# changed helper\n")
    refused_run = subprocess.run(command, cwd=poison, env=environment, check=False, capture_output=True, text=True)
    assert refused_run.returncode != 0 and "helper digest differs" in refused_run.stderr
    print("isolated collector: candidate imports excluded; changed helper refused")


def no_metadata_control(root: Path) -> None:
    """Retain real Git identity, remove metadata, then record unchanged observed outcomes."""
    filename, job = ".github/workflows/docs.yml", "docs-check-no-git"
    source = {"jobs": {job: {"steps": [{"uses": "actions/checkout@v4"},
                                       {"name": "Strip metadata", "run": "rm -rf .git"}]}}}
    generated = generate("docs", source)["jobs"][job]["steps"]
    assert " identify " in generated[1]["run"]
    assert generated[2]["name"] == "Set CPU-derived job budgets"
    assert generated[3]["run"] == source["jobs"][job]["steps"][1]["run"]
    with patch.object(runtime, "ROOT", root):
        identity = runtime.source_identity()
        retained = root / "retained.json"
        retained.write_text(json.dumps(identity))
        shutil.rmtree(root / ".git")
        assert not (root / ".git").exists()
        output = root / "no-metadata" / "job-evidence.json"
        steps = {generated[3]["id"]: {"outcome": "failure", "conclusion": "failure"}}
        environment = {"GITHUB_SHA": identity["head"], "CI_JOB_RESULT": "failure",
                       "CI_STEP_RESULTS": json.dumps(steps), "CI_MATRIX": "{}"}
        with patch.dict(os.environ, environment):
            runtime.record(output, filename, job, retained)
            result = json.loads(output.read_text())
            assert result["head"] == identity["head"] and result["tree"] == identity["tree"]
            assert result["steps"] == steps and result["result"] == "failure"
            refused(lambda: runtime.retained_identity(retained, filename, "another-job"), "other identity consumer")
            retained.write_text(json.dumps({**identity, "head": "a" * 40}))
            refused(lambda: runtime.retained_identity(retained, filename, job), "another retained head")
            retained.write_text(json.dumps({"head": identity["head"]}))
            refused(lambda: runtime.retained_identity(retained, filename, job), "missing retained tree")
            key = filename + ":" + job
            result["tree"] = "b" * 40
            output.write_text(json.dumps(result))
            source = {**identity, "plan": {key: {}}}
            refused(lambda: runtime.context_evidence(source, output.parent), "changed retained tree")
    print("no-metadata recorder: actual checkout retained; failure remains failure")


def main() -> int:
    """Exercise real Git input binding and incomplete manifest comparison."""
    plan, labels = expand_workflow(PATH, SOURCE)
    transport_controls({"plan": plan, "labels": labels})
    generated = generate("control", workflow(SOURCE))
    writes = [job for job in generated["jobs"].values() if job.get("permissions", {}).get("actions") == "write"]
    assert len(writes) == 2
    assert generated["jobs"]["ci-fail-fast"]["if"] == SAME_REPOSITORY
    assert generated["jobs"]["ci-cancel-tail"]["if"] == "${{ always() && (" + SAME_REPOSITORY[4:-3] + ") }}"
    original_matrix = workflow(SOURCE)["jobs"]["workers"]["strategy"]["matrix"]
    assert generated["jobs"]["workers"]["strategy"]["matrix"] == original_matrix
    with tempfile.TemporaryDirectory(prefix="runtime-evidence-") as directory:
        root = Path(directory)
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        path = root / PATH
        path.parent.mkdir(parents=True)
        path.write_text(SOURCE)
        subprocess.run(["git", "-C", str(root), "add", PATH], check=True)
        head = fixture_commit(root, "Create runtime evidence fixture")
        source = committed_plan(root, head)
        events, _ = streams(source)
        event_path = root / "events.jsonl"
        event_path.write_text("".join(json.dumps(row) + "\n" for row in events))
        artifacts = root / "artifacts"
        artifacts.mkdir()
        subject = {"repository": "fixture/project", "head": head, "tree": source["tree"], "event": "push"}
        document = collect(root, subject, event_path, artifacts, False)
        assert not document["complete"] and all(value == "success" for value in document["payload"]["results"].values())
        refused(lambda: validate(document), "unknown tool and image provenance")
        refused(lambda: compare(document, copy.deepcopy(document)), "identical incomplete collections")
        isolated_reader(root, subject, event_path, artifacts, document)
        (artifacts / "partial.zip").write_bytes(b"interrupted upload")
        assert artifact_rows(artifacts, "union.json", True) == []
        event_path.write_text(json.dumps({**events[1], "jobResult": "failure"}) + "\n")
        document = collect(root, subject, event_path, artifacts, True)
        assert not document["complete"]
        assert document["observations"]["logs"]["first_failure"] == events[1]["job"]
        no_metadata_control(root)
    print("runtime manifest collectors: all controls PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
