#!/usr/bin/env python3
"""Observer-path probes against the production modules of one exact-head tree.

Usage: observer_probe.py <tree> <output-json>
P1  collector read budget across two requests (production vs. budget removed)
P2  collector classification of non-transient HTTP 401/404
P3  watcher job limit against the longest planned dependency chain it observes
"""
import json
import os
import sys
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "scripts"))
import yaml  # noqa: E402
import ci_fail_fast  # noqa: E402
from ci_fail_fast import API, RETRY_BUDGET_SECONDS, tail_failed  # noqa: E402


def two_requests(read_budget, retry_after=None):
    """runs/<id> needs two transient retries; the jobs page then never recovers."""
    clock = [1000.0]
    calls = []
    headers = {} if retry_after is None else {"Retry-After": str(retry_after)}

    def urlopen(request, timeout):
        calls.append((request.full_url.rsplit("/", 1)[-1], clock[0] - 1000))
        first = sum(1 for url, _ in calls if url == "1")
        if request.full_url.endswith("/runs/1") and first == 3:
            class Response:
                headers = {}
                def read(self):
                    return b'{"head_sha": "x"}'
                def __enter__(self):
                    return self
                def __exit__(self, *exc):
                    return False
            return Response()
        raise HTTPError(request.full_url, 429 if headers else 502, "unavailable", headers, None)

    def sleep(seconds):
        clock[0] += seconds

    with patch("ci_fail_fast.urlopen", side_effect=urlopen), \
            patch("ci_fail_fast.time.monotonic", side_effect=lambda: clock[0]), \
            patch("ci_fail_fast.time.time", side_effect=lambda: clock[0]), \
            patch("ci_fail_fast.time.sleep", side_effect=sleep):
        api = API("fixture/project", "fixture", read_budget)
        outcome = "completed"
        try:
            api.request("runs/1")
            api.pages("runs/1/jobs?filter=latest", "jobs")
        except OSError as exc:
            outcome = type(exc).__name__
    return {"read_budget": read_budget, "retry_after": retry_after, "outcome": outcome,
            "elapsed_seconds": clock[0] - 1000, "requests": len(calls)}


def http_classification(code):
    calls = []

    def urlopen(request, timeout):
        calls.append(request.full_url)
        raise HTTPError(request.full_url, code, "client error", {}, None)

    with patch("ci_fail_fast.urlopen", side_effect=urlopen), patch("ci_fail_fast.time.sleep"):
        api = API("fixture/project", "fixture", RETRY_BUDGET_SECONDS)
        try:
            api.request("runs/1")
            raised = None
        except OSError as exc:
            raised = type(exc).__name__
    # ci_runtime_evidence.collect catches every OSError from collect_api as observer-only.
    return {"http": code, "attempts": len(calls), "raised": raised,
            "collector_except_clause_catches": isinstance(HTTPError("u", code, "m", {}, None), OSError)}


def longest_chain(jobs, job_id, memo, skipped=()):
    if job_id in memo:
        return memo[job_id]
    job = jobs[job_id]
    needs = job.get("needs", [])
    needs = [needs] if isinstance(needs, str) else needs
    limit = job.get("timeout-minutes")
    own = max(45, 60) if isinstance(limit, str) else (limit if limit is not None else 360)
    if job_id in skipped:
        own = 0
    best = max(((longest_chain(jobs, n, memo, skipped)) for n in needs), default=(0, []), key=lambda r: r[0])
    memo[job_id] = (best[0] + own, best[1] + [f"{job_id}:{own}"])
    return memo[job_id]


def watcher_limits():
    """Watcher, collector and tail run only on push/PR, so schedule/dispatch-only jobs are not watched."""
    rows = {}
    for name in ("docs", "elaborate", "rtl", "rtl-fast"):
        jobs = yaml.safe_load((tree / ".github/workflows" / (name + ".yml")).read_text())["jobs"]
        watcher = jobs["ci-fail-fast"]["timeout-minutes"]
        memo = {}
        dispatch_only = [j for j, job in jobs.items()
                         if "github.event_name == 'schedule' || github.event_name == 'workflow_dispatch'"
                         in str(job.get("if", ""))]
        observed = [j for j in jobs if j not in ("ci-fail-fast", "ci-cancel-tail", *dispatch_only)]
        rows.setdefault(name, {})["excluded_schedule_or_dispatch_only"] = dispatch_only
        rows[name]["watcher_if"] = jobs["ci-fail-fast"].get("if")
        total, chain = max((longest_chain(jobs, j, memo, dispatch_only) for j in observed), key=lambda r: r[0])
        rows[name].update({"watcher_limit_minutes": watcher, "longest_push_pr_chain_minutes": total,
                           "chain": chain, "watcher_outlives_chain": watcher > total,
                           "note": "a job without timeout-minutes is counted at the 360-minute platform default"})
    timed_out = {"ci-fail-fast": {"result": "failure", "outputs": {"observer_only_error": "false"}},
                 "ci-manifest": {"result": "success", "outputs": {"observer_only_error": "false"}}}
    no_outputs = {"ci-fail-fast": {"result": "failure", "outputs": {}},
                  "ci-manifest": {"result": "success", "outputs": {}}}
    return {"workflows": rows,
            "tail_cancels_after_watcher_job_timeout": tail_failed(timed_out),
            "tail_cancels_after_watcher_job_timeout_no_outputs": tail_failed(no_outputs)}


result = {"tree_head": os.popen(f"git -C {tree} rev-parse HEAD").read().strip(),
          "P1_shared_read_budget": {"production": two_requests(RETRY_BUDGET_SECONDS),
                                    "budget_removed": two_requests(None),
                                    "production_retry_after_290": two_requests(RETRY_BUDGET_SECONDS, 290),
                                    "budget_removed_retry_after_290": two_requests(None, 290),
                                    "collector_job_limit_seconds": 15 * 60},
          "P2_non_transient_http": [http_classification(code) for code in (401, 404)],
          "P3_watcher_job_limit": watcher_limits()}
Path(sys.argv[2]).write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
