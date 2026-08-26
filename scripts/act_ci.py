#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run this repository's GitHub workflows locally at one exact PR head.

The command fails before starting ``act`` unless the pull request is open, is
based on ``dev``, and its remote head is the clean local checkout's ``HEAD``.
It builds the pull-request event itself, passes authentication only through a
masked environment-backed secret, and runs without binding the host worktree
into a container. Hosted required contexts still run independently.

Typical use::

    python3 scripts/act_ci.py --pr 268
    python3 scripts/act_ci.py --pr 268 --workflow rtl-full
    python3 scripts/act_ci.py --pr 268 --workflow docs --dry-run

Use ``--sudo`` only on hosts whose Docker socket is unavailable to the current
user. Exit 0 means every selected workflow passed; exit 1 means a workflow
failed; exit 2 is a setup or exact-head refusal.
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import pathlib
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from typing import Iterable, Iterator, Mapping, Sequence


RC_OK, RC_FAILED, RC_REFUSED = 0, 1, 2
ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_BASE = "dev"
RUNNER_IMAGE = "catthehacker/ubuntu:full-latest"
MIN_ACT_VERSION = (0, 2, 89)
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
ACT_VERSION_RE = re.compile(r"\b(\d+)\.(\d+)\.(\d+)\b")

WORKFLOWS: Mapping[str, str] = {
    "docs": ".github/workflows/docs.yml",
    "elaborate": ".github/workflows/elaborate.yml",
    "rtl-fast": ".github/workflows/rtl-fast.yml",
    "rtl-full": ".github/workflows/rtl.yml",
}

PR_FIELDS = (
    "number,state,isDraft,baseRefName,baseRefOid,headRefName,headRefOid,"
    "headRepository,headRepositoryOwner,isCrossRepository,url"
)


class Refusal(RuntimeError):
    """An unsafe, ambiguous, or unavailable validation prerequisite."""


@dataclass(frozen=True)
class PullRequest:
    number: int
    state: str
    draft: bool
    base_ref: str
    base_sha: str
    head_ref: str
    head_sha: str
    head_repo: str
    cross_repo: bool
    url: str

    @classmethod
    def from_json(cls, raw: object) -> "PullRequest":
        if not isinstance(raw, dict):
            raise Refusal("GitHub returned pull-request metadata that is not an object")
        head_repo = raw.get("headRepository")
        if not isinstance(head_repo, dict):
            raise Refusal("GitHub returned no head repository for the pull request")
        values = {
            "number": raw.get("number"),
            "state": raw.get("state"),
            "draft": raw.get("isDraft"),
            "base_ref": raw.get("baseRefName"),
            "base_sha": raw.get("baseRefOid"),
            "head_ref": raw.get("headRefName"),
            "head_sha": raw.get("headRefOid"),
            "head_repo": head_repo.get("nameWithOwner"),
            "cross_repo": raw.get("isCrossRepository"),
            "url": raw.get("url"),
        }
        if not isinstance(values["number"], int) or values["number"] <= 0:
            raise Refusal("GitHub returned an invalid pull-request number")
        for name in ("state", "base_ref", "head_ref", "head_repo", "url"):
            if not isinstance(values[name], str) or not values[name]:
                raise Refusal(f"GitHub returned an invalid pull-request field: {name}")
        for name in ("base_sha", "head_sha"):
            if not isinstance(values[name], str) or not SHA_RE.fullmatch(values[name]):
                raise Refusal(f"GitHub returned an invalid pull-request SHA: {name}")
        if not isinstance(values["draft"], bool):
            raise Refusal("GitHub returned an invalid pull-request draft state")
        if not isinstance(values["cross_repo"], bool):
            raise Refusal("GitHub returned an invalid cross-repository state")
        return cls(**values)  # type: ignore[arg-type]


def require_tool(name: str) -> str:
    found = shutil.which(name)
    if not found:
        raise Refusal(f"required executable is unavailable: {name}")
    return found


def capture(command: Sequence[str], *, cwd: pathlib.Path = ROOT,
            description: str) -> str:
    try:
        result = subprocess.run(command, cwd=cwd, text=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, check=False)
    except OSError as exc:
        raise Refusal(f"cannot run {description}: {exc}") from exc
    if result.returncode != 0:
        detail = result.stderr.strip().splitlines()
        suffix = f": {detail[-1]}" if detail else ""
        raise Refusal(f"{description} failed{suffix}")
    return result.stdout.strip()


def repository_name() -> str:
    raw = capture(
        [require_tool("gh"), "repo", "view", "--json", "nameWithOwner"],
        description="GitHub repository lookup",
    )
    try:
        value = json.loads(raw)["nameWithOwner"]
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        raise Refusal("GitHub returned malformed repository metadata") from exc
    if not isinstance(value, str) or value.count("/") != 1:
        raise Refusal("GitHub returned an invalid repository name")
    return value


def query_pull_request(number: int, repository: str) -> PullRequest:
    raw = capture(
        [require_tool("gh"), "pr", "view", str(number), "--repo", repository,
         "--json", PR_FIELDS],
        description=f"pull request #{number} lookup",
    )
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise Refusal("GitHub returned malformed pull-request metadata") from exc
    return PullRequest.from_json(parsed)


def validate_pull_request(pr: PullRequest) -> None:
    if pr.state != "OPEN":
        raise Refusal(f"pull request #{pr.number} is {pr.state}, not OPEN")
    if pr.base_ref != DEFAULT_BASE:
        raise Refusal(
            f"pull request #{pr.number} targets {pr.base_ref}, not {DEFAULT_BASE}"
        )


def checkout_state() -> tuple[str, str]:
    head = capture([require_tool("git"), "rev-parse", "HEAD"],
                   description="local HEAD lookup")
    dirty = capture(
        [require_tool("git"), "status", "--porcelain=v1", "--untracked-files=all"],
        description="worktree cleanliness check",
    )
    return head, dirty


def validate_checkout_values(pr: PullRequest, local_head: str, dirty: str) -> None:
    if dirty:
        first = dirty.splitlines()[0]
        raise Refusal(f"worktree is dirty (first entry: {first})")
    if not SHA_RE.fullmatch(local_head):
        raise Refusal(f"local HEAD is not a full commit SHA: {local_head!r}")
    if local_head != pr.head_sha:
        raise Refusal(
            f"local HEAD {local_head} is not PR head {pr.head_sha}; fetch and "
            "check out the exact pushed head"
        )


def validate_checkout(pr: PullRequest) -> None:
    validate_checkout_values(pr, *checkout_state())


def build_event(pr: PullRequest, repository: str) -> dict[str, object]:
    """The smallest pull_request payload every repository workflow consumes."""
    action = "synchronize" if pr.draft else "ready_for_review"
    event: dict[str, object] = {
        "action": action,
        "number": pr.number,
        "repository": {
            "full_name": repository,
            "default_branch": DEFAULT_BASE,
        },
        "pull_request": {
            "number": pr.number,
            "draft": pr.draft,
            "html_url": pr.url,
            "base": {
                "ref": pr.base_ref,
                "sha": pr.base_sha,
                "repo": {"full_name": repository},
            },
            "head": {
                "ref": pr.head_ref,
                "sha": pr.head_sha,
                "repo": {"full_name": pr.head_repo},
            },
        },
    }
    return event


def select_workflows(requested: Iterable[str] | None) -> tuple[str, ...]:
    values = list(requested or ["all"])
    if "all" in values:
        if len(values) != 1:
            raise Refusal("--workflow all cannot be combined with another workflow")
        return tuple(WORKFLOWS)
    seen: list[str] = []
    for value in values:
        if value not in WORKFLOWS:
            raise Refusal(f"unknown workflow: {value}")
        if value not in seen:
            seen.append(value)
    if not seen:
        raise Refusal("at least one workflow must be selected")
    return tuple(seen)


def parse_act_version(text: str) -> tuple[int, int, int]:
    found = ACT_VERSION_RE.search(text)
    if not found:
        raise Refusal(f"cannot parse act version from {text!r}")
    return tuple(int(value) for value in found.groups())  # type: ignore[return-value]


def resolve_act_binary(value: str) -> str:
    if os.sep in value:
        path = pathlib.Path(value).expanduser().resolve()
        if not path.is_file() or not os.access(path, os.X_OK):
            raise Refusal(f"act executable is unavailable: {path}")
        return str(path)
    found = shutil.which(value)
    if not found:
        raise Refusal(f"act executable is unavailable: {value}")
    return found


def act_prefix(act_binary: str, use_sudo: bool) -> list[str]:
    if not use_sudo:
        return [act_binary]
    sudo = require_tool("sudo")
    return [sudo, "-n", "--preserve-env=GITHUB_TOKEN", act_binary]


def build_act_command(prefix: Sequence[str], workflow: str,
                      event_path: pathlib.Path, artifact_path: pathlib.Path,
                      action_cache: pathlib.Path,
                      cache_server: pathlib.Path) -> list[str]:
    return [
        *prefix,
        "pull_request",
        "--strict",
        "--no-recurse",
        "--no-skip-checkout",
        "--rm",
        "--directory", str(ROOT),
        "--workflows", str(ROOT / WORKFLOWS[workflow]),
        "--eventpath", str(event_path),
        "--platform", f"ubuntu-latest={RUNNER_IMAGE}",
        "--artifact-server-path", str(artifact_path),
        "--artifact-server-port", "0",
        "--action-cache-path", str(action_cache),
        "--cache-server-path", str(cache_server),
        "--cache-server-port", "0",
        "--secret", "GITHUB_TOKEN",
    ]


def require_runtime(act_binary: str, use_sudo: bool) -> list[str]:
    version_text = capture([act_binary, "--version"], description="act version check")
    version = parse_act_version(version_text)
    if version < MIN_ACT_VERSION:
        want = ".".join(str(part) for part in MIN_ACT_VERSION)
        got = ".".join(str(part) for part in version)
        raise Refusal(f"act {got} is older than the tested minimum {want}")

    docker = require_tool("docker")
    docker_command = [docker, "info", "--format", "{{.ServerVersion}}"]
    if use_sudo:
        docker_command = [require_tool("sudo"), "-n", *docker_command]
    capture(docker_command, description="Docker daemon check")
    return act_prefix(act_binary, use_sudo)


def github_token() -> str:
    gh = require_tool("gh")
    try:
        result = subprocess.run([gh, "auth", "token"], cwd=ROOT, text=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.DEVNULL, check=False)
    except OSError as exc:
        raise Refusal(f"cannot read GitHub authentication: {exc}") from exc
    token = result.stdout.strip() if result.returncode == 0 else ""
    if not token:
        raise Refusal("gh has no usable authentication token")
    return token


def default_cache_dir(use_sudo: bool) -> pathlib.Path:
    base = os.environ.get("XDG_CACHE_HOME")
    root = pathlib.Path(base) if base else pathlib.Path.home() / ".cache"
    return root / "milan-fpga-act" / ("sudo" if use_sudo else "user")


@contextlib.contextmanager
def temporary_run_dir(use_sudo: bool) -> Iterator[pathlib.Path]:
    """Clean an isolated event/artifact directory, including sudo-owned files."""
    path = pathlib.Path(tempfile.mkdtemp(prefix="milan-act-ci-"))
    try:
        yield path
    finally:
        if use_sudo and path.exists():
            subprocess.run(
                [require_tool("sudo"), "-n", "chown", "-R",
                 f"{os.getuid()}:{os.getgid()}", str(path)],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                check=False,
            )
        shutil.rmtree(path, ignore_errors=True)


def run_workflows(pr: PullRequest, repository: str, workflows: Sequence[str],
                  *, act_binary: str, use_sudo: bool,
                  cache_dir: pathlib.Path | None, dry_run: bool) -> int:
    prefix = ([act_binary] if dry_run
              else require_runtime(act_binary, use_sudo))
    token = "" if dry_run else github_token()
    cache = cache_dir or default_cache_dir(use_sudo)
    action_cache, cache_server = cache / "actions", cache / "tool-cache"
    if not dry_run:
        action_cache.mkdir(parents=True, exist_ok=True)
        cache_server.mkdir(parents=True, exist_ok=True)

    event = build_event(pr, repository)
    with temporary_run_dir(use_sudo and not dry_run) as run_dir:
        event_path = run_dir / "event.json"
        event_path.write_text(json.dumps(event, indent=2) + "\n", encoding="utf-8")
        print(f"act-ci: PR #{pr.number} {event['action']} exact head {pr.head_sha}")
        print(f"act-ci: base {pr.base_sha} ({pr.base_ref}), draft={str(pr.draft).lower()}")
        for workflow in workflows:
            artifact_path = run_dir / f"artifacts-{workflow}"
            artifact_path.mkdir()
            command = build_act_command(prefix, workflow, event_path,
                                        artifact_path, action_cache, cache_server)
            if dry_run:
                print(f"act-ci: {workflow}: {shlex.join(command)}")
                continue
            print(f"act-ci: running {workflow} ({WORKFLOWS[workflow]})", flush=True)
            env = os.environ.copy()
            env["GITHUB_TOKEN"] = token
            try:
                result = subprocess.run(command, cwd=ROOT, env=env, check=False)
            except OSError as exc:
                raise Refusal(f"cannot start act for {workflow}: {exc}") from exc
            if result.returncode != 0:
                print(f"act-ci: {workflow}: FAILED ({result.returncode})",
                      file=sys.stderr)
                return RC_FAILED
            validate_checkout(pr)
            print(f"act-ci: {workflow}: PASS at {pr.head_sha}")
    return RC_OK


def expect_refusal(label: str, action) -> bool:
    try:
        action()
    except Refusal:
        print(f"  ok   {label}")
        return True
    print(f"  FAIL {label}")
    return False


def selftest() -> int:
    failures = 0

    def check(label: str, condition: bool) -> None:
        nonlocal failures
        print(f"  {'ok  ' if condition else 'FAIL'} {label}")
        failures += 0 if condition else 1

    base = "1" * 40
    head = "2" * 40
    raw = {
        "number": 268,
        "state": "OPEN",
        "isDraft": False,
        "baseRefName": "dev",
        "baseRefOid": base,
        "headRefName": "268-act-first-validation",
        "headRefOid": head,
        "headRepository": {"nameWithOwner": "kebag-logic/milan-fpga"},
        "headRepositoryOwner": {"login": "kebag-logic"},
        "isCrossRepository": False,
        "url": "https://github.com/kebag-logic/milan-fpga/pull/999",
    }
    pr = PullRequest.from_json(raw)
    validate_pull_request(pr)
    validate_checkout_values(pr, head, "")
    event = build_event(pr, "kebag-logic/milan-fpga")
    event_pr = event["pull_request"]
    assert isinstance(event_pr, dict)
    check("ready event is selected for a non-draft PR",
          event["action"] == "ready_for_review" and event_pr["draft"] is False)
    check("event pins the exact head and base",
          event_pr["head"]["sha"] == head and event_pr["base"]["sha"] == base)

    draft_raw = dict(raw)
    draft_raw["isDraft"] = True
    draft_event = build_event(PullRequest.from_json(draft_raw),
                              "kebag-logic/milan-fpga")
    check("draft event uses synchronize and preserves draft=true",
          draft_event["action"] == "synchronize"
          and draft_event["pull_request"]["draft"] is True)

    check("all selects each workflow once in stable order",
          select_workflows(["all"]) == tuple(WORKFLOWS))
    check("explicit workflow selection de-duplicates",
          select_workflows(["docs", "rtl-full", "docs"])
          == ("docs", "rtl-full"))
    failures += 0 if expect_refusal(
        "all plus another workflow is refused",
        lambda: select_workflows(["all", "docs"]),
    ) else 1
    failures += 0 if expect_refusal(
        "dirty worktree is refused",
        lambda: validate_checkout_values(pr, head, " M AGENTS.md"),
    ) else 1
    failures += 0 if expect_refusal(
        "wrong local head is refused",
        lambda: validate_checkout_values(pr, "3" * 40, ""),
    ) else 1

    closed_raw = dict(raw)
    closed_raw["state"] = "MERGED"
    failures += 0 if expect_refusal(
        "non-open pull request is refused",
        lambda: validate_pull_request(PullRequest.from_json(closed_raw)),
    ) else 1
    wrong_base = dict(raw)
    wrong_base["baseRefName"] = "main"
    failures += 0 if expect_refusal(
        "non-dev pull request is refused",
        lambda: validate_pull_request(PullRequest.from_json(wrong_base)),
    ) else 1
    malformed = dict(raw)
    malformed["headRefOid"] = "short"
    failures += 0 if expect_refusal(
        "malformed GitHub metadata is refused",
        lambda: PullRequest.from_json(malformed),
    ) else 1

    command = build_act_command(
        ["act"], "rtl-full", pathlib.Path("event.json"),
        pathlib.Path("artifacts"), pathlib.Path("actions"),
        pathlib.Path("cache"),
    )
    check("act command is strict and selects the real exhaustive workflow",
          "--strict" in command
          and str(ROOT / WORKFLOWS["rtl-full"]) in command)
    check("act command uses remote checkout and never binds the host tree",
          "--artifact-server-path" in command
          and "--no-skip-checkout" in command
          and "--bind" not in command)
    check("token is environment-backed and never embedded in the command",
          command[-2:] == ["--secret", "GITHUB_TOKEN"]
          and not any("ghp_" in value for value in command))
    check("act version parser accepts the tested version",
          parse_act_version("act version 0.2.89") == MIN_ACT_VERSION)
    failures += 0 if expect_refusal(
        "unparseable act version is refused",
        lambda: parse_act_version("act unknown"),
    ) else 1

    print("selftest:", "PASS" if failures == 0 else f"{failures} FAILURE(S)")
    return RC_OK if failures == 0 else RC_FAILED


def main(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pr", type=int, help="open pull-request number")
    parser.add_argument("--repo", help="OWNER/REPO (default: current gh repository)")
    parser.add_argument(
        "--workflow", action="append",
        choices=("all", *WORKFLOWS),
        help="workflow alias; repeatable (default: all)",
    )
    parser.add_argument("--act-bin", default="act",
                        help="act executable name or path")
    parser.add_argument("--sudo", action="store_true",
                        help="run Docker and act through non-interactive sudo")
    parser.add_argument("--cache-dir", type=pathlib.Path,
                        help="persistent action/tool cache directory")
    parser.add_argument("--dry-run", action="store_true",
                        help="print the exact act commands without running them")
    parser.add_argument("--selftest", action="store_true",
                        help="run offline negative and construction tests")
    args = parser.parse_args(argv[1:])

    if args.selftest:
        if args.pr is not None or args.workflow or args.dry_run:
            parser.error("--selftest cannot be combined with PR-run arguments")
        return selftest()
    if args.pr is None or args.pr <= 0:
        parser.error("--pr requires a positive pull-request number")

    try:
        workflows = select_workflows(args.workflow)
        repository = args.repo or repository_name()
        pr = query_pull_request(args.pr, repository)
        validate_pull_request(pr)
        validate_checkout(pr)
        act_binary = resolve_act_binary(args.act_bin)
        return run_workflows(
            pr, repository, workflows,
            act_binary=act_binary,
            use_sudo=args.sudo,
            cache_dir=args.cache_dir,
            dry_run=args.dry_run,
        )
    except Refusal as exc:
        print(f"act-ci: REFUSED: {exc}", file=sys.stderr)
        return RC_REFUSED


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
