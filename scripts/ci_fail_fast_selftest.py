#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Prove first-failure selection, successful completion and fork write refusal."""

import copy
from urllib.error import HTTPError

from ci_fail_fast import cancel, observe, same_repository


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


def main() -> int:
    """Exercise both production decision functions with adverse contexts."""
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
