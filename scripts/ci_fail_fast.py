#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Cancel same-repository runs at the first observed failed job.

Fork events never enter the write-token job. The same check is repeated here
before any API operation. Local replay has its own process-group supervisor.
"""

from __future__ import annotations

import argparse
from email.utils import parsedate_to_datetime
import json
import os
from pathlib import Path
import time
from urllib.parse import urlencode
from urllib.error import HTTPError
from urllib.request import Request, urlopen

WORKFLOWS = {".github/workflows/" + name + ".yml" for name in ("docs", "elaborate", "rtl", "rtl-fast")}
POLL_SECONDS = 120
READ_ATTEMPTS = 4
RETRY_BUDGET_SECONDS = 600
FAILURES = ("failure", "cancelled", "timed_out", "action_required")


def retry_delay(headers: dict, attempt: int) -> float:
    """Respect both rate-limit clocks, including an HTTP-date Retry-After."""
    delay = min(POLL_SECONDS * 2 ** attempt, RETRY_BUDGET_SECONDS)
    values = {key.lower(): value for key, value in headers.items()}
    retry = values.get("retry-after")
    if retry:
        try:
            after = float(retry)
        except ValueError:
            after = parsedate_to_datetime(retry).timestamp() - time.time()
        delay = max(delay, after)
    if values.get("x-ratelimit-remaining") == "0":
        delay = max(delay, float(values["x-ratelimit-reset"]) - time.time() + 1)
    return delay


def same_repository(event: dict, event_name: str, repository: str) -> bool:
    """Only pushes and PR heads belonging to this repository authorize writes."""
    if event.get("repository", {}).get("full_name") != repository:
        return False
    if event_name == "push":
        return True
    return (event_name == "pull_request"
            and event.get("pull_request", {}).get("head", {}).get("repo", {}).get("full_name") == repository)


class API:
    """Use the job token only for this repository's Actions endpoints."""

    def __init__(self, repository: str, token: str, read_budget: float | None = None) -> None:
        self.root = "https://api.github.com/repos/" + repository + "/actions/"
        self.token = token
        self.next_read = 0.0
        self.read_deadline = None if read_budget is None else time.monotonic() + read_budget

    def request(self, path: str, method: str = "GET") -> dict:
        """Return one bounded API response without logging authentication material."""
        request = Request(self.root + path, method=method,
                          headers={"Authorization": "Bearer " + self.token,
                                   "Accept": "application/vnd.github+json",
                                   "X-GitHub-Api-Version": "2022-11-28"})
        deadline = time.monotonic() + RETRY_BUDGET_SECONDS
        if method == "GET" and self.read_deadline is not None:
            deadline = min(deadline, self.read_deadline)
        for attempt in range(READ_ATTEMPTS):
            if method == "GET" and self.next_read > time.time():
                delay = self.next_read - time.time()
                if time.monotonic() + delay > deadline:
                    raise TimeoutError("observer rate-limit wait exceeds retry budget")
                time.sleep(delay)
            try:
                remaining = deadline - time.monotonic()
                if method == "GET" and remaining <= 0:
                    raise TimeoutError("observer read budget exhausted")
                with urlopen(request, timeout=min(30, remaining) if method == "GET" else 30) as response:
                    data = response.read()
                    if response.headers.get("X-RateLimit-Remaining") == "0":
                        self.next_read = float(response.headers["X-RateLimit-Reset"]) + 1
                return json.loads(data) if data else {}
            except (OSError, TimeoutError) as exc:
                transient = not isinstance(exc, HTTPError) or exc.code in (403, 429) or 500 <= exc.code < 600
                if method != "GET" or not transient or attempt == READ_ATTEMPTS - 1:
                    raise
                headers = exc.headers if isinstance(exc, HTTPError) else {}
                delay = retry_delay(headers, attempt)
                if time.monotonic() + delay > deadline:
                    raise
                time.sleep(delay)
        raise RuntimeError("unreachable retry state")

    def pages(self, path: str, field: str) -> list[dict]:
        """No job or sibling run disappears at the first page boundary."""
        rows = []
        for page in range(1, 101):
            joiner = "&" if "?" in path else "?"
            batch = self.request(path + joiner + f"per_page=100&page={page}")[field]
            rows.extend(batch)
            if len(batch) < 100:
                return rows
        raise ValueError("Actions API exceeds bounded pagination")


def observe(jobs: list[dict], expected: set[str],
            skipped: dict[str, list[str]] | None = None) -> tuple[bool, dict | None]:
    """Do not confuse an empty startup response with successful completion."""
    skipped = skipped or {}
    relevant = [job for job in jobs if job["name"] in expected or job["name"] in skipped]
    names = [job["name"] for job in relevant]
    if len(names) != len(set(names)):
        raise ValueError("duplicate current-attempt job names")
    failed = next((job for job in relevant
                   if job.get("conclusion") in FAILURES), None)
    covered = []
    for job in relevant:
        if job["name"] in skipped:
            if job.get("status") == "completed" and job.get("conclusion") == "skipped":
                covered.extend(skipped[job["name"]])
        else:
            covered.append(job["name"])
    if len(covered) != len(set(covered)):
        raise ValueError("expanded and unexpanded matrix jobs overlap")
    complete = set(covered) == expected and all(job["status"] == "completed" for job in relevant)
    return complete, failed


def watch(api: API, run_id: int, expected: set[str], skipped: dict) -> int:
    """Only a confirmed job conclusion is a first failure; observer errors remain distinct."""
    try:
        while True:
            complete, failed = observe(api.pages(f"runs/{run_id}/jobs?filter=latest", "jobs"), expected, skipped)
            if failed:
                print(json.dumps({"first_failure": failed["name"], "conclusion": failed["conclusion"]}))
                return 1
            if complete:
                return 0
            time.sleep(POLL_SECONDS)
    except (OSError, ValueError, KeyError) as exc:
        observer_error(exc)
        return 0


def observer_error(error: Exception) -> None:
    """Publish unavailable observation without creating a failed job conclusion."""
    if os.environ.get("GITHUB_OUTPUT"):
        with Path(os.environ["GITHUB_OUTPUT"]).open("a") as output:
            output.write("observer_error=true\n")
    print("Observer unavailable: " + type(error).__name__)


def tail_failed(needs: dict) -> bool:
    """Ignore only an explicitly identified observer error, never evidence-tail failures."""
    return any(row.get("result") in FAILURES and not (
        job in ("ci-fail-fast", "ci-manifest") and row.get("outputs", {}).get("observer_only_error") == "true")
        for job, row in needs.items())


def cancel(api: API, event: dict, event_name: str, repository: str, run_id: int, head: str) -> list[int]:
    """Cancel active sibling workflows first, then this already failed run."""
    if not same_repository(event, event_name, repository):
        raise ValueError("fork or unsupported event cannot request Actions writes")
    runs = api.pages("runs?" + urlencode({"head_sha": head}), "workflow_runs")
    selected = sorted({run["id"] for run in runs
                       if run["id"] != run_id and run["head_sha"] == head
                       and run["path"].split("@")[0] in WORKFLOWS
                       and run.get("head_repository", {}).get("full_name") == repository
                       and run["status"] != "completed"})
    errors = []
    for target in [*selected, run_id]:
        try:
            api.request(f"runs/{target}/cancel", "POST")
        except HTTPError as exc:
            # Another watcher can finish cancellation between listing and POST.
            # Never let that race prevent requests for the remaining siblings.
            completed = False
            if exc.code == 409:
                try:
                    completed = api.request(f"runs/{target}").get("status") == "completed"
                except OSError:
                    pass
            if not completed:
                errors.append(f"{target}: HTTP {exc.code}")
        except OSError as exc:
            errors.append(f"{target}: {type(exc).__name__}")
    if errors:
        raise ValueError("cancellation requests failed: " + ", ".join(errors))
    return [*selected, run_id]


def main() -> int:
    """Watch actual job results; the workflow's failure-only step performs writes."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("watch", "cancel", "tail"))
    args = parser.parse_args()
    if os.environ.get("ACT", "").lower() == "true":
        print("Local supervisor owns first-failure cancellation")
        return 0
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    repository = os.environ["GITHUB_REPOSITORY"]
    event_name = os.environ["GITHUB_EVENT_NAME"]
    if not same_repository(event, event_name, repository):
        raise ValueError("event cannot enter the write-token cancellation job")
    api = API(repository, os.environ["GH_TOKEN"])
    run_id = int(os.environ["GITHUB_RUN_ID"])
    if args.mode == "tail" and not tail_failed(json.loads(os.environ["CI_TAIL_NEEDS"])):
        print("No confirmed tail failure; no cancellation requested")
        return 0
    if args.mode in ("cancel", "tail"):
        head = event["pull_request"]["head"]["sha"] if event_name == "pull_request" else os.environ["GITHUB_SHA"]
        print("Cancelled runs:", cancel(api, event, event_name, repository, run_id, head))
        return 0
    expected = set(json.loads(os.environ["EXPECTED_JOBS"]))
    if not expected:
        raise ValueError("empty job inventory")
    return watch(api, run_id, expected, json.loads(os.environ["SKIPPED_MATRICES"]))


if __name__ == "__main__":
    raise SystemExit(main())
