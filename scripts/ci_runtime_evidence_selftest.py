#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Compare independent API and scheduler observations and plant runtime gaps."""

import copy
import ast
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from urllib.error import HTTPError, URLError
from unittest.mock import patch

from ci_local_manifest import artifact_rows, collect, observations
from ci_manifest import compare, validate
import ci_runtime_evidence as runtime
from ci_runtime_evidence import api_evidence
from ci_runtime_workflows import SAME_REPOSITORY, generate
from ci_workflow_plan import committed_plan, expand_workflow, workflow
from ci_workflow_plan_selftest import PATH, SOURCE, fixture_commit
from ci_fail_fast import observe, tail_failed, watch
from ci_fail_fast import RETRY_BUDGET_SECONDS
from ci_gate_workflows import generate as gate_generate, load_template
import yaml


def collector_fixture(root: Path) -> tuple[dict, dict, dict]:
    """Commit the actual generated RTL graph in an isolated collector checkout."""
    filename = ".github/workflows/rtl.yml"
    generated = gate_generate("rtl", load_template(runtime.ROOT, "rtl"))
    path = root / filename
    path.parent.mkdir(parents=True)
    path.write_text(yaml.safe_dump(generated))
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "add", filename], check=True)
    head = fixture_commit(root, "Create collector graph fixture")
    source = committed_plan(root, head)
    event = root / "event.json"
    event.write_text(json.dumps({"repository": {"full_name": "fixture/project"}}))
    environment = {"GITHUB_EVENT_PATH": str(event), "GITHUB_EVENT_NAME": "push",
                   "GITHUB_REPOSITORY": "fixture/project", "GH_TOKEN": "fixture",
                   "GITHUB_SHA": head, "GITHUB_RUN_ID": "1", "ACT": "false",
                   "GITHUB_OUTPUT": str(root / "outputs")}
    return source, generated, environment


def skipped_collector_control(root: Path) -> None:
    """Retained hosted raw names pass watcher, production collector and terminal graph."""
    source, generated, environment = collector_fixture(root)
    filename = ".github/workflows/rtl.yml"
    # Transport shape read from hosted run 38273578232, not execution evidence.
    raw = [{"name": name + " shard ${{ matrix.shard }}/${{ matrix.total }}",
            "status": "completed", "conclusion": "skipped", "steps": []}
           for name in ("Verilator", "Yosys")]
    observer = next(step for step in generated["jobs"]["ci-fail-fast"]["steps"]
                    if step.get("id") == "ci_observe")
    expected = set(json.loads(observer["env"]["EXPECTED_JOBS"]))
    skipped = json.loads(observer["env"]["SKIPPED_MATRICES"])
    expanded = {label for rows in skipped.values() for label in rows}
    jobs = [{"name": label, "status": "completed", "conclusion": "skipped", "steps": []}
            for label in sorted(expected - expanded)] + raw
    assert observe(jobs, expected, skipped) == (True, None)
    output = root / "manifest.json"
    argv = ["collect", "collect", "--run", "1", "--artifacts", str(root / "artifacts"),
            "--output", str(output)]
    with patch.object(runtime, "ROOT", root), patch.dict(os.environ, environment), \
            patch.object(sys, "argv", argv), \
            patch.object(runtime.API, "request", return_value={"head_sha": source["head"], "path": filename}), \
            patch.object(runtime.API, "pages", return_value=jobs):
        assert runtime.main() == 0
        assert watch(runtime.API("fixture/project", "fixture"), 1, expected, skipped) == 0
    document = json.loads(output.read_text())
    assert not document["complete"]
    assert set(document["payload"]["results"].values()) == {"skipped"}
    for key, label in source["labels"].items():
        if label in expanded:
            assert all(step["outcome"] == "skipped" for step in document["payload"]["execution"][key])
    refused(lambda: compare(document, document), "skipped collection equality")
    assert not tail_failed({job: {"result": "success"} for job in generated["jobs"]["ci-cancel-tail"]["needs"]})
    for field, value in (("name", "unknown"), ("status", "in_progress"), ("conclusion", "success"),
                         ("conclusion", "failure"), ("steps", [{"name": "invented"}])):
        changed = copy.deepcopy(raw)
        changed[0][field] = value
        refused(lambda: api_evidence(source, changed, filename), "raw matrix " + field + " " + str(value))
        refused(lambda: observe(changed, expected, skipped), "watcher raw matrix " + field)
    expanded_job = {"name": skipped[raw[0]["name"]][0], "conclusion": "skipped", "steps": []}
    for rows in ([*raw, expanded_job], [expanded_job, *raw], [*raw, raw[0]]):
        refused(lambda: api_evidence(source, rows, filename), "overlapping raw matrix coverage")
        refused(lambda: observe(rows, expected, skipped), "watcher overlapping raw matrix coverage")
    print("Skipped matrices: collector entry, watcher and terminal graph PASS; no success fabricated")


def observer_collector_controls(root: Path) -> None:
    """Exhaust real collector reads under a virtual clock, then apply the generated graph."""
    source, generated, environment = collector_fixture(root)
    collector = generated["jobs"]["ci-manifest"]
    assert collector["timeout-minutes"] * 60 > RETRY_BUDGET_SECONDS
    assert collector["outputs"]["observer_only_error"] == (
        "${{ steps.ci_collect.outputs.observer_error == 'true' && "
        "steps.ci_collect.outcome == 'success' && steps.ci_upload.outcome == 'success' }}")
    errors = [HTTPError("fixture", code, "unavailable", {"Retry-After": "240"}, None)
              for code in (403, 429, 502)] + [TimeoutError("timeout"),
              HTTPError("fixture", 429, "exhausted", {"Retry-After": "601"}, None),
              URLError("connection refused")]
    for index, error in enumerate(errors):
        clock = [1000.0]
        def sleep(seconds: float) -> None:
            """Advance the real retry loop without waiting on a network outage."""
            clock[0] += seconds
        output = root / (str(index) + ".json")
        Path(environment["GITHUB_OUTPUT"]).unlink(missing_ok=True)
        argv = ["collector", "collect", "--run", "1", "--artifacts", str(root / "artifacts"),
                "--output", str(output)]
        with patch.object(runtime, "ROOT", root), patch.dict(os.environ, environment), \
                patch.object(sys, "argv", argv), patch("ci_fail_fast.urlopen", side_effect=error) as opened, \
                patch("ci_fail_fast.time.monotonic", side_effect=lambda: clock[0]), \
                patch("ci_fail_fast.time.time", side_effect=lambda: clock[0]), \
                patch("ci_fail_fast.time.sleep", side_effect=sleep):
            assert runtime.main() == 0
        assert all(call.args[0].method == "GET" for call in opened.call_args_list)
        elapsed = clock[0] - 1000
        assert elapsed <= RETRY_BUDGET_SECONDS
        if index < 4:
            assert elapsed > 180, "must exercise a wait beyond the old collector limit"
        assert Path(environment["GITHUB_OUTPUT"]).read_text() == "observer_error=true\n"
        document = json.loads(output.read_text())
        assert not document["complete"]
        assert document["observations"]["logs"]["observer_error"] == type(error).__name__
        assert set(document["payload"]["results"].values()) == {"unknown"}
        refused(lambda: compare(document, document), "observer-only equality")
        assert observe([{"name": "Collect CI manifest", "status": "completed", "conclusion": "success"}],
                       {"Collect CI manifest"}) == (True, None)
        assert not tail_failed({"ci-manifest": {"result": "success", "outputs": {"observer_only_error": "true"}}})
        assert not tail_failed({"ci-manifest": {"result": "failure", "outputs": {"observer_only_error": "true"}}})
        print(f"Collector observer control {index}: rc 0, wait {elapsed}s, incomplete, zero writes")
    for code in (400, 401, 404):
        # A refused client request is not an outage: no retry, no observer output, a failed job.
        Path(environment["GITHUB_OUTPUT"]).unlink(missing_ok=True)
        output = root / ("client-" + str(code) + ".json")
        argv = ["collector", "collect", "--run", "1", "--artifacts", str(root / "artifacts"),
                "--output", str(output)]
        error = HTTPError("fixture", code, "refused", {}, None)
        with patch.object(runtime, "ROOT", root), patch.dict(os.environ, environment), \
                patch.object(sys, "argv", argv), patch("ci_fail_fast.urlopen", side_effect=error) as opened, \
                patch("ci_fail_fast.time.sleep") as sleep:
            assert runtime.main() == 1
        assert opened.call_count == 1 and sleep.call_count == 0
        assert not Path(environment["GITHUB_OUTPUT"]).exists() and not output.exists()
        assert tail_failed({"ci-manifest": {"result": "failure", "outputs": {"observer_only_error": "false"}}})
        print(f"Collector client error {code}: rc 1, one request, no observer output")
    # Real collection/evidence failures remain failures even after an observation gap.
    for job in ("ci-manifest", "ci-fail-fast"):
        assert tail_failed({job: {"result": "failure", "outputs": {"observer_only_error": "false"}}})
    with patch.object(runtime, "ROOT", root), patch.dict(os.environ, environment), \
            patch.object(sys, "argv", argv), patch.object(runtime.API, "request", return_value={"head_sha": "b" * 40}):
        assert runtime.main() == 1


def shared_budget_control(root: Path) -> None:
    """A late recovery spends the budget that a later failing read cannot restart."""
    source, _, environment = collector_fixture(root)
    run = json.dumps({"head_sha": source["head"], "path": ".github/workflows/rtl.yml"}).encode()

    def virtual_reads(action: object) -> tuple[float, list[str]]:
        """runs/1 recovers on its third attempt; its jobs page never recovers."""
        clock, opened = [1000.0], []
        def urlopen(request: object, timeout: float) -> object:
            """Answer by URL, so each request keeps its own failure sequence."""
            opened.append(request.full_url.rsplit("/actions/", 1)[1])
            if opened[-1] == "runs/1" and opened.count("runs/1") == 3:
                response = io.BytesIO(run)
                response.headers = {}
                return response
            raise HTTPError(request.full_url, 429, "limited", {"Retry-After": "240"}, None)
        def sleep(seconds: float) -> None:
            """Advance the real retry loop without waiting on the outage."""
            clock[0] += seconds
        with patch("ci_fail_fast.urlopen", side_effect=urlopen), \
                patch("ci_fail_fast.time.monotonic", side_effect=lambda: clock[0]), \
                patch("ci_fail_fast.time.time", side_effect=lambda: clock[0]), \
                patch("ci_fail_fast.time.sleep", side_effect=sleep):
            action()
        return clock[0] - 1000, opened

    def unshared() -> None:
        """The same two reads, each with only its own per-request budget."""
        api = runtime.API("fixture/project", "fixture")
        api.request("runs/1")
        refused_read = None
        try:
            api.pages("runs/1/jobs?filter=latest", "jobs")
        except HTTPError as exc:
            refused_read = exc
        assert refused_read is not None, "the jobs page outage must exhaust its retries"

    output = root / "shared.json"
    argv = ["collector", "collect", "--run", "1", "--artifacts", str(root / "artifacts"),
            "--output", str(output)]
    def collector() -> None:
        """The production collector entry point constructs its own API."""
        with patch.object(runtime, "ROOT", root), patch.dict(os.environ, environment), \
                patch.object(sys, "argv", argv):
            assert runtime.main() == 0

    reference, _ = virtual_reads(unshared)
    assert reference > RETRY_BUDGET_SECONDS, "injected waits must exceed one shared budget"
    elapsed, opened = virtual_reads(collector)
    assert elapsed <= RETRY_BUDGET_SECONDS, f"collector reads took {elapsed}s"
    assert opened == ["runs/1"] * 3 + ["runs/1/jobs?filter=latest&per_page=100&page=1"]
    assert Path(environment["GITHUB_OUTPUT"]).read_text() == "observer_error=true\n"
    document = json.loads(output.read_text())
    assert not document["complete"]
    assert set(document["payload"]["results"].values()) == {"unknown"}
    print(f"Collector shared read budget: {elapsed}s within {RETRY_BUDGET_SECONDS}s; "
          f"the same reads take {reference}s unshared")


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
        skipped_collector_control(root / "skipped")
        observer_collector_controls(root / "observer")
        shared_budget_control(root / "shared-budget")
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
