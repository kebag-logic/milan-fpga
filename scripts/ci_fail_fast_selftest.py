#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Prove first-failure selection, successful completion and fork write refusal."""

import copy
import io
import json
import os
from pathlib import Path
import tempfile
from unittest.mock import patch
from urllib.error import HTTPError, URLError

from ci_fail_fast import API, cancel, observe, same_repository, watch, tail_failed, retry_delay
from ci_gate_workflows import ROOT, generate, load_template
from ci_workflow_plan import expand_workflow
import yaml


def observer_controls() -> None:
    """Rate limits and transport errors are bounded read failures, never cancellation authority."""
    for error in (HTTPError("fixture", 403, "limited", {"Retry-After": "240"}, None),
                  HTTPError("fixture", 429, "limited", {"X-RateLimit-Remaining": "0",
                            "X-RateLimit-Reset": "1300"}, None),
                  HTTPError("fixture", 502, "unavailable", {}, None), TimeoutError("timeout"),
                  URLError("connection refused")):
        with tempfile.TemporaryDirectory(prefix="observer-control-") as directory:
            output = Path(directory) / "output"
            with patch("ci_fail_fast.urlopen", side_effect=error) as opened, \
                    patch("ci_fail_fast.time.sleep") as sleep, patch("ci_fail_fast.time.time", return_value=1000), \
                    patch.dict(os.environ, {"GITHUB_OUTPUT": str(output)}):
                assert watch(API("fixture/project", "fixture"), 1, {"one"}, {}) == 0
                assert 1 < opened.call_count <= 4
                assert all(call.args[0].method == "GET" for call in opened.call_args_list)
                assert sleep.call_count == opened.call_count - 1
                assert output.read_text() == "observer_error=true\n"
                if isinstance(error, HTTPError) and error.code == 403:
                    assert sleep.call_args_list[0].args[0] >= 240
                if isinstance(error, HTTPError) and error.code == 429:
                    assert sleep.call_args_list[0].args[0] >= 301
            assert not tail_failed({"ci-fail-fast": {"result": "failure",
                                   "outputs": {"observer_only_error": "true"}}})
    for code in (400, 401, 404):
        # A refused client request is a genuine watcher failure, never an observer-only outage.
        with tempfile.TemporaryDirectory(prefix="client-error-control-") as directory:
            output = Path(directory) / "output"
            with patch("ci_fail_fast.urlopen", side_effect=HTTPError("fixture", code, "refused", {}, None)) as opened, \
                    patch("ci_fail_fast.time.sleep") as sleep, \
                    patch.dict(os.environ, {"GITHUB_OUTPUT": str(output)}):
                assert watch(API("fixture/project", "fixture"), 1, {"one"}, {}) == 1
            assert opened.call_count == 1 and sleep.call_count == 0
            assert not output.exists()
        assert tail_failed({"ci-fail-fast": {"result": "failure", "outputs": {"observer_only_error": "false"}}})
    with patch("ci_fail_fast.time.time", return_value=0):
        assert retry_delay({"Retry-After": "Thu, 01 Jan 1970 00:05:00 GMT"}, 0) == 300
    response = io.BytesIO(b'{"jobs": []}')
    response.headers = {}
    with patch("ci_fail_fast.urlopen", side_effect=[TimeoutError("once"), response]), \
            patch("ci_fail_fast.time.sleep"):
        assert API("fixture/project", "fixture").pages("jobs", "jobs") == []
    print("Observer controls: 403, 429, 502, timeout, transport, bounded retries and recovery PASS; "
          "400, 401 and 404 fail the watcher")


def graph_controls() -> None:
    """Apply completion and cancellation to generated graphs, including terminal failures."""
    for name in ("docs", "elaborate", "rtl", "rtl-fast"):
        workflow = generate(name, load_template(ROOT, name))
        expand_workflow(".github/workflows/" + name + ".yml", yaml.safe_dump(workflow))
        jobs = workflow["jobs"]
        observer = next(step for step in jobs["ci-fail-fast"]["steps"] if step.get("id") == "ci_observe")
        expected = set(json.loads(observer["env"]["EXPECTED_JOBS"]))
        skipped = json.loads(observer["env"]["SKIPPED_MATRICES"])
        assert "Collect CI manifest" in expected
        assert "ci-fail-fast" not in jobs["ci-manifest"]["needs"]
        assert set(jobs["ci-cancel-tail"]["needs"]) == {"ci-fail-fast", "ci-manifest"}
        assert "head.repo.full_name == github.repository" in jobs["ci-cancel-tail"]["if"]
        ordinary = [{"name": label, "status": "completed", "conclusion": "success"} for label in sorted(expected)]
        assert observe(ordinary, expected, skipped) == (True, None)
        for label in (ordinary[0]["name"], "Collect CI manifest"):
            planted = copy.deepcopy(ordinary)
            failed = next(job for job in planted if job["name"] == label)
            failed["conclusion"] = "failure"
            assert observe(planted, expected, skipped)[1] == failed
            cancellation_control()
        for terminal in ("ci-manifest", "ci-fail-fast"):
            assert tail_failed({terminal: {"result": "failure", "outputs": {}}})
            cancellation_control()
        assert tail_failed({"ci-fail-fast": {"result": "failure", "outputs": {"observer_only_error": "false"}}})
        raw = [job for job in ordinary if not any(job["name"] in rows for rows in skipped.values())]
        raw += [{"name": label, "status": "completed", "conclusion": "skipped"} for label in skipped]
        assert observe(raw, expected, skipped) == (True, None)
        if name == "rtl":
            # Exact raw matrix names and conclusions from hosted run 38273578232.
            assert {"Verilator shard ${{ matrix.shard }}/${{ matrix.total }}",
                    "Yosys shard ${{ matrix.shard }}/${{ matrix.total }}"} <= set(skipped)
            assert observe(raw[:-1], expected, skipped) == (False, None)
        print(name + ": generated graph, collector failure, watcher-tail failure, raw skipped matrices PASS")


class FixtureAPI:
    """Record every requested write, without network or credentials."""

    def __init__(self, runs: list[dict]) -> None:
        self.runs = runs
        self.requests = []

    def pages(self, path: str, field: str) -> list[dict]:
        """A read is observable too: forbidden events must never reach it."""
        self.requests.append(("GET", path))
        assert field == "workflow_runs"
        return self.runs

    def request(self, path: str, method: str = "GET") -> dict:
        """Retain the exact cancellation order."""
        self.requests.append((method, path))
        return {}


def cancellation_control() -> None:
    """A confirmed collector or tail failure reaches all same-head siblings."""
    repository = "fixture/project"
    event = {"repository": {"full_name": repository},
             "pull_request": {"head": {"repo": {"full_name": repository}}}}
    runs = [{"id": index, "head_sha": "a" * 40, "path": ".github/workflows/" + name + ".yml",
             "status": "in_progress", "head_repository": {"full_name": repository}}
            for index, name in enumerate(("docs", "rtl", "elaborate", "rtl-fast"), 1)]
    api = FixtureAPI(runs)
    assert cancel(api, event, "pull_request", repository, 1, "a" * 40) == [2, 3, 4, 1]
    assert [path for method, path in api.requests if method == "POST"] == [
        "runs/2/cancel", "runs/3/cancel", "runs/4/cancel", "runs/1/cancel"]


def main() -> int:
    """Exercise both production decision functions with adverse contexts."""
    observer_controls()
    graph_controls()
    repo = "fixture/project"
    event = {"repository": {"full_name": repo},
             "pull_request": {"head": {"repo": {"full_name": repo}}}}
    assert same_repository(event, "push", repo)
    assert same_repository(event, "pull_request", repo)
    fork = copy.deepcopy(event)
    fork["pull_request"]["head"]["repo"]["full_name"] = "fork/project"
    for context, kind in ((fork, "pull_request"), (event, "workflow_run")):
        api = FixtureAPI([])
        try:
            cancel(api, context, kind, repo, 1, "a" * 40)
        except ValueError:
            assert api.requests == []
        else:
            raise AssertionError("unauthorized event requested writes")
    jobs = [{"name": name, "status": "completed", "conclusion": "success"} for name in ("one", "two")]
    assert observe([], {"one", "two"}) == (False, None)
    assert observe(jobs[:1], {"one", "two"}) == (False, None)
    assert observe(jobs, {"one", "two"}) == (True, None)
    jobs[0]["conclusion"] = "failure"
    jobs[1].update(status="in_progress", conclusion=None)
    assert observe(jobs, {"one", "two"}) == (False, jobs[0])
    for conclusion in ("failure", "cancelled", "timed_out", "action_required"):
        jobs[0]["conclusion"] = conclusion
        assert observe(jobs, {"one", "two"}) == (False, jobs[0])
    runs = [{"id": index, "head_sha": "a" * 40, "path": path, "status": "in_progress",
             "head_repository": {"full_name": repo}}
            for index, path in enumerate((".github/workflows/docs.yml", ".github/workflows/rtl.yml",
                                          ".github/workflows/elaborate.yml", ".github/workflows/rtl-fast.yml"), 1)]
    for field, value in (("head_sha", "b" * 40), ("path", ".github/workflows/other.yml"),
                         ("status", "completed"), ("head_repository", {"full_name": "fork/project"})):
        excluded = copy.deepcopy(runs[0])
        excluded.update(id=len(runs) + 1)
        excluded[field] = value
        runs.append(excluded)
    api = FixtureAPI(runs)
    assert cancel(api, event, "pull_request", repo, 1, "a" * 40) == [2, 3, 4, 1]
    assert [path for method, path in api.requests if method == "POST"] == [f"runs/{n}/cancel" for n in (2, 3, 4, 1)]
    class RacingAPI(FixtureAPI):
        """The first sibling finishes after listing but before cancellation."""

        def request(self, path: str, method: str = "GET") -> dict:
            """Retain all writes even when one target has already completed."""
            self.requests.append((method, path))
            if path == "runs/2/cancel":
                raise HTTPError(path, 409, "already completed", {}, None)
            return {"status": "completed"}

    racing = RacingAPI(runs)
    assert cancel(racing, event, "pull_request", repo, 1, "a" * 40) == [2, 3, 4, 1]
    assert [path for method, path in racing.requests if method == "POST"] == [f"runs/{n}/cancel" for n in (2, 3, 4, 1)]
    print("fail-fast controls: first failure, complete success, sibling selection, fork zero-write PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
