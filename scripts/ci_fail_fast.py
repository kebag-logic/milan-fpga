#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Cancel same-repository runs at the first observed failed job.

Fork events never enter the write-token job. The same check is repeated here
before any API operation. Local replay has its own process-group supervisor.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import time
from urllib.parse import urlencode
from urllib.error import HTTPError
from urllib.request import Request, urlopen

WORKFLOWS = {".github/workflows/" + name + ".yml" for name in ("docs", "elaborate", "rtl", "rtl-fast")}


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

    def __init__(self, repository: str, token: str) -> None:
        self.root = "https://api.github.com/repos/" + repository + "/actions/"
        self.token = token

    def request(self, path: str, method: str = "GET") -> dict:
        """Return one bounded API response without logging authentication material."""
        request = Request(self.root + path, method=method,
                          headers={"Authorization": "Bearer " + self.token,
                                   "Accept": "application/vnd.github+json",
                                   "X-GitHub-Api-Version": "2022-11-28"})
        with urlopen(request, timeout=30) as response:
            data = response.read()
        return json.loads(data) if data else {}

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


def observe(jobs: list[dict], expected: set[str]) -> tuple[bool, dict | None]:
    """Do not confuse an empty startup response with successful completion."""
    relevant = [job for job in jobs if job["name"] in expected]
    names = [job["name"] for job in relevant]
    if len(names) != len(set(names)):
        raise ValueError("duplicate current-attempt job names")
    failed = next((job for job in relevant
                   if job.get("conclusion") in ("failure", "cancelled", "timed_out", "action_required")), None)
    complete = set(names) == expected and all(job["status"] == "completed" for job in relevant)
    return complete, failed


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
    parser.add_argument("mode", choices=("watch", "cancel"))
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
    if args.mode == "cancel":
        head = event["pull_request"]["head"]["sha"] if event_name == "pull_request" else os.environ["GITHUB_SHA"]
        print("Cancelled runs:", cancel(api, event, event_name, repository, run_id, head))
        return 0
    expected = set(json.loads(os.environ["EXPECTED_JOBS"]))
    if not expected:
        raise ValueError("empty job inventory")
    while True:
        complete, failed = observe(api.pages(f"runs/{run_id}/jobs?filter=latest", "jobs"), expected)
        if failed:
            print(json.dumps({"first_failure": failed["name"], "conclusion": failed["conclusion"]}))
            return 1
        if complete:
            return 0
        time.sleep(5)


if __name__ == "__main__":
    raise SystemExit(main())
