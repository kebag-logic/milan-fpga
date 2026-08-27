#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run this repository's GitHub workflows locally at one exact PR head.

The runner is host-side security code. Invoke the copy from a clean trusted
``dev`` worktree, never the copy in the pull request being tested. It refuses
unless that trusted worktree is the PR's current remote base. Candidate files
are fetched without credentials into a fresh per-run repository and are only
executed by ``act`` inside unprivileged containers with no Docker socket,
ambient configuration, host secrets, or persistent writable cache.

Typical use, from the candidate worktree::

    python3 -I /path/to/trusted-dev/scripts/act_ci.py --pr 268
    python3 -I /path/to/trusted-dev/scripts/act_ci.py --pr 268 --workflow rtl-full
    python3 -I /path/to/trusted-dev/scripts/act_ci.py --pr 268 --dry-run

Use ``--sudo`` only on hosts whose Docker socket is unavailable to the current
user. Exit 0 means every selected workflow passed; exit 1 means a workflow
failed; exit 2 is a setup, trust-boundary, cleanup, or exact-head refusal.
"""

from __future__ import annotations

import argparse
import contextlib
import ctypes
import hashlib
import ipaddress
import json
import os
import pathlib
import re
import secrets
import shlex
import shutil
import signal
import socket
import stat
import subprocess
import sys
import tempfile
import threading
import time
from dataclasses import dataclass, fields, replace
from typing import Callable, Iterable, Iterator, Mapping, Sequence


RC_OK, RC_FAILED, RC_REFUSED = 0, 1, 2
ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_BASE = "dev"
RUNNER_IMAGE = "catthehacker/ubuntu:full-latest"
SUPPORTED_ACT_VERSION = (0, 2, 89)
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
REPOSITORY_RE = re.compile(
    r"^[A-Za-z0-9](?:[A-Za-z0-9_.-]{0,98}[A-Za-z0-9])?/"
    r"[A-Za-z0-9](?:[A-Za-z0-9_.-]{0,98}[A-Za-z0-9])?$"
)
ACT_VERSION_RE = re.compile(r"\b(\d+)\.(\d+)\.(\d+)\b")
SAFE_PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
MAX_WORKFLOW_BYTES = 1024 * 1024
MAX_CHECKED_FILE_BYTES = 4 * 1024 * 1024
MAX_GITMODULES_BYTES = 64 * 1024
DOCKER_ID_RE = re.compile(r"^[0-9a-f]{64}$")
DOCKER_OWNER_LABEL = "org.kebag-logic.milan-act-ci.owner"
ACT_TOOLCACHE_VOLUME = "act-toolcache"
ACT_TOOLCACHE_TARGET = "/opt/hostedtoolcache"
DOCKER_COMMAND_TIMEOUT = 30
DOCKER_MUTATION_STABLE_SECONDS = 0.5
RUN_DIRECTORY_RECLAIM_TIMEOUT = 120
HOST_COMMAND_TIMEOUT = 30 * 60
CLEANUP_SIGNALS = (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)

WORKFLOWS: dict[str, str] = {
    "docs": ".github/workflows/docs.yml",
    "elaborate": ".github/workflows/elaborate.yml",
    "rtl-fast": ".github/workflows/rtl-fast.yml",
    "rtl-full": ".github/workflows/rtl.yml",
}
TRUSTED_ACTION_USES = frozenset(
    {
        "actions/cache@v4",
        "actions/checkout@v4",
        "actions/download-artifact@v4",
        "actions/setup-python@v5",
        "actions/upload-artifact@v4",
    }
)
TRUSTED_SUBMODULES = (
    (
        "external",
        "external",
        "git@github.com:kebag-logic/fpga-avb-ethernet.git",
    ),
    (
        "third_party/verilog-axis",
        "third_party/verilog-axis",
        "https://github.com/alexforencich/verilog-axis",
    ),
    (
        "protocol-processor",
        "protocol-processor",
        "https://github.com/Mister-M-alt/"
        "protocol-processor-control-plane-avb-milan.git",
    ),
    (
        "gptp-processor",
        "gptp-processor",
        "https://github.com/Mister-M-alt/FPGA-gPTP.git",
    ),
)
REQUIRED_SUBMODULES = tuple(
    path for name, path, _url in TRUSTED_SUBMODULES if name != "external"
)

PR_FIELDS = (
    "number,state,isDraft,baseRefName,baseRefOid,headRefName,headRefOid,"
    "headRepository,headRepositoryOwner,isCrossRepository,url"
)


class Refusal(RuntimeError):
    """An unsafe, ambiguous, stale, or unavailable validation prerequisite."""


class TerminationRequest(BaseException):
    """A terminal signal translated into a cleanup-bearing Python unwind."""

    def __init__(self, signum: int) -> None:
        self.signum = signum
        super().__init__(signal.Signals(signum).name)


@contextlib.contextmanager
def cleanup_termination_signals() -> Iterator[None]:
    """Make INT/TERM/HUP run cleanup and defer repeats until it completes."""
    watched = CLEANUP_SIGNALS
    previous = {item: signal.getsignal(item) for item in watched}

    def request_cleanup(signum: int, _frame: object) -> None:
        # Ignore repeats while nested finally blocks reclaim Docker and disk state.
        prior_mask = signal.pthread_sigmask(signal.SIG_BLOCK, watched)
        try:
            for item in watched:
                signal.signal(item, signal.SIG_IGN)
        finally:
            signal.pthread_sigmask(signal.SIG_SETMASK, prior_mask)
        raise TerminationRequest(signum)

    for item in watched:
        signal.signal(item, request_cleanup)
    try:
        yield
    finally:
        for item, handler in previous.items():
            signal.signal(item, handler)


@contextlib.contextmanager
def blocked_cleanup_signals() -> Iterator[None]:
    """Defer a first signal that arrives after cleanup has already begun."""
    previous = signal.pthread_sigmask(signal.SIG_BLOCK, CLEANUP_SIGNALS)
    try:
        yield
    finally:
        signal.pthread_sigmask(signal.SIG_SETMASK, previous)


def start_cleanup_safe_thread(thread: threading.Thread) -> None:
    """Start a worker with cleanup signals blocked before it can receive them."""
    previous = signal.pthread_sigmask(signal.SIG_BLOCK, CLEANUP_SIGNALS)
    try:
        thread.start()
    finally:
        signal.pthread_sigmask(signal.SIG_SETMASK, previous)


def start_cleanup_thread_or_refuse(
    thread: threading.Thread, description: str
) -> None:
    try:
        start_cleanup_safe_thread(thread)
    except TerminationRequest:
        raise
    except Exception as exc:
        raise Refusal(f"cannot start {description}") from exc


@contextlib.contextmanager
def deferred_cleanup_signal_delivery() -> Iterator[None]:
    """Latch one parent signal without exporting a blocked mask through exec."""
    previous = {item: signal.getsignal(item) for item in CLEANUP_SIGNALS}
    pending: list[int] = []

    if all(handler == signal.SIG_IGN for handler in previous.values()):
        # A first cleanup signal has already latched and repeats must remain
        # harmless. Use caught no-op handlers so exec resets the child to its
        # default dispositions instead of inheriting SIG_IGN.
        def ignore_repeat(_signum: int, _frame: object) -> None:
            return

        for item in CLEANUP_SIGNALS:
            signal.signal(item, ignore_repeat)
        try:
            yield
        finally:
            with blocked_cleanup_signals():
                for item, handler in previous.items():
                    signal.signal(item, handler)
        return

    def latch(signum: int, _frame: object) -> None:
        if not pending:
            pending.append(signum)

    for item in CLEANUP_SIGNALS:
        signal.signal(item, latch)
    try:
        yield
    finally:
        # The child has already exec'd before this restoration. Blocking only
        # this parent-side handler transition prevents a partially restored
        # disposition set without exporting a mask to the child.
        with blocked_cleanup_signals():
            if pending:
                # Match cleanup_termination_signals.request_cleanup before
                # unwinding: repeats cannot interrupt the cleanup entry/tail.
                for item in CLEANUP_SIGNALS:
                    signal.signal(item, signal.SIG_IGN)
            else:
                for item, handler in previous.items():
                    signal.signal(item, handler)
    if pending:
        raise TerminationRequest(pending[0])


def cancel_and_join_cleanup_threads(
    cancel: threading.Event,
    signal_lock: threading.Lock,
    workers: Sequence[tuple[threading.Thread, threading.Event]],
    problems: list[str],
    *,
    timeout: float = DOCKER_COMMAND_TIMEOUT + 10,
) -> None:
    """Cancel workers and prove them dead before a cleanup boundary can unwind."""
    registered_but_unstarted = False
    with blocked_cleanup_signals():
        with signal_lock:
            cancel.set()
        for worker, completed in workers:
            if worker.ident is None:
                problems.append("interrupt monitor was registered but never started")
                registered_but_unstarted = True
                continue
            worker.join(timeout=timeout)
            if worker.is_alive():
                problems.append("interrupt monitor survived its bounded shutdown")
                # Monitor operations are independently bounded. Do not permit
                # Docker teardown to overlap the worker after a latency error.
                worker.join()
            if worker.is_alive() or not completed.is_set():
                raise Refusal("interrupt monitor termination was not proven")
        if registered_but_unstarted:
            raise Refusal("interrupt monitor was registered but never started")


def run_with_cleanup_signals(action: Callable[[], int]) -> int:
    try:
        with cleanup_termination_signals():
            return action()
    except TerminationRequest as exc:
        name = signal.Signals(exc.signum).name
        print(f"act-ci: interrupted by {name} after cleanup", file=sys.stderr)
        return 128 + exc.signum


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


@dataclass(frozen=True)
class RunDirectory:
    path: pathlib.Path
    parent: pathlib.Path
    device: int
    inode: int


@dataclass
class RunDirectoryLease:
    """Mutable acquisition state registered before a run-directory mutation."""

    parent: pathlib.Path
    path: pathlib.Path | None = None
    run: RunDirectory | None = None
    accepted: bool = False
    released: bool = False


@dataclass(frozen=True)
class RunLayout:
    root: pathlib.Path
    checkout: pathlib.Path
    invocation: pathlib.Path
    home: pathlib.Path
    xdg_config: pathlib.Path
    xdg_cache: pathlib.Path
    xdg_data: pathlib.Path
    temporary: pathlib.Path
    artifacts: pathlib.Path
    action_cache: pathlib.Path
    cache_server: pathlib.Path
    event_path: pathlib.Path
    env_file: pathlib.Path
    secret_file: pathlib.Path
    var_file: pathlib.Path
    input_file: pathlib.Path


@dataclass(frozen=True)
class DockerBoundary:
    """One unpredictable runner-owned Docker network and ephemeral cache slot."""

    token: str
    name: str
    network_id: str | None = None
    gateway: str | None = None
    toolcache_owned: bool = False


@dataclass
class DockerBoundaryLease:
    """Mutable acquisition state registered before any Docker mutation."""

    boundary: DockerBoundary
    complete: bool = False
    released: bool = False


def require_tool(name: str) -> str:
    # Candidate worktrees are commonly the invocation directory. Never resolve
    # a host-side prerequisite through their current directory or PATH entry.
    found = shutil.which(name, path=SAFE_PATH)
    if not found:
        raise Refusal(f"required executable is unavailable: {name}")
    return str(pathlib.Path(found).resolve())


def capture(
    command: Sequence[str],
    *,
    cwd: pathlib.Path,
    description: str,
    env: Mapping[str, str] | None = None,
) -> str:
    try:
        result = run_tracked_process_group_command(
            command,
            cwd=cwd,
            env=dict(os.environ if env is None else env),
            timeout=HOST_COMMAND_TIMEOUT,
            use_sudo=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise Refusal(f"{description} timed out") from exc
    except (OSError, UnicodeError) as exc:
        raise Refusal(f"cannot run {description}: {exc}") from exc
    if result.returncode != 0:
        detail = result.stderr.strip().splitlines()
        suffix = f": {detail[-1]}" if detail else ""
        raise Refusal(f"{description} failed{suffix}")
    return result.stdout.strip()


def repository_name() -> str:
    raw = capture(
        [require_tool("gh"), "repo", "view", "--json", "nameWithOwner"],
        cwd=ROOT,
        description="GitHub repository lookup",
    )
    try:
        value = json.loads(raw)["nameWithOwner"]
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        raise Refusal("GitHub returned malformed repository metadata") from exc
    if not isinstance(value, str) or not REPOSITORY_RE.fullmatch(value):
        raise Refusal("GitHub returned an invalid repository name")
    return value


def query_pull_request(number: int, repository: str) -> PullRequest:
    raw = capture(
        [
            require_tool("gh"),
            "pr",
            "view",
            str(number),
            "--repo",
            repository,
            "--json",
            PR_FIELDS,
        ],
        cwd=ROOT,
        description=f"pull request #{number} lookup",
    )
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise Refusal("GitHub returned malformed pull-request metadata") from exc
    return PullRequest.from_json(parsed)


def validate_pull_request(pr: PullRequest, repository: str) -> None:
    if not REPOSITORY_RE.fullmatch(repository):
        raise Refusal(f"invalid repository name: {repository!r}")
    if pr.state != "OPEN":
        raise Refusal(f"pull request #{pr.number} is {pr.state}, not OPEN")
    if pr.base_ref != DEFAULT_BASE:
        raise Refusal(
            f"pull request #{pr.number} targets {pr.base_ref}, not {DEFAULT_BASE}"
        )
    if pr.cross_repo or pr.head_repo != repository:
        raise Refusal(
            f"pull request #{pr.number} has untrusted head repository "
            f"{pr.head_repo}; only same-repository heads are supported"
        )
    expected_url = f"https://github.com/{repository}/pull/{pr.number}"
    if pr.url != expected_url:
        raise Refusal(
            f"pull request #{pr.number} returned an unexpected URL: {pr.url}"
        )


def changed_pr_fields(expected: PullRequest, current: PullRequest) -> list[str]:
    return [
        item.name
        for item in fields(PullRequest)
        if (
            item.name != "base_sha"
            and getattr(expected, item.name) != getattr(current, item.name)
        )
    ]


def require_live_pull_request(
    expected: PullRequest,
    repository: str,
    query: Callable[[int, str], PullRequest] = query_pull_request,
) -> None:
    current = query(expected.number, repository)
    validate_pull_request(current, repository)
    changed = changed_pr_fields(expected, current)
    if changed:
        raise Refusal(
            f"pull request #{expected.number} changed during validation "
            f"({', '.join(changed)}); discard this run"
        )
    if current.base_sha != expected.base_sha:
        print(
            f"act-ci: NOTE: {expected.base_ref} moved from {expected.base_sha} "
            f"to {current.base_sha} during validation; the unchanged exact-head "
            f"evidence for {expected.head_sha} remains valid",
            flush=True,
        )


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


def require_supported_act_version(version: tuple[int, int, int]) -> None:
    if version != SUPPORTED_ACT_VERSION:
        want = ".".join(str(part) for part in SUPPORTED_ACT_VERSION)
        got = ".".join(str(part) for part in version)
        raise Refusal(
            f"act {got} is not the audited version {want}; review its Docker "
            "tool-cache behavior before changing the pin"
        )


def resolve_act_binary(value: str) -> str:
    if os.sep in value:
        path = pathlib.Path(value).expanduser().resolve()
        if not path.is_file() or not os.access(path, os.X_OK):
            raise Refusal(f"act executable is unavailable: {path}")
        return str(path)
    found = shutil.which(value, path=SAFE_PATH)
    if not found:
        raise Refusal(f"act executable is unavailable: {value}")
    return str(pathlib.Path(found).resolve())


def validate_act_binary(path: str, candidate_worktree: pathlib.Path) -> None:
    resolved = pathlib.Path(path).resolve()
    for untrusted in (candidate_worktree,):
        if resolved == untrusted or resolved.is_relative_to(untrusted):
            raise Refusal(f"act executable is inside the candidate worktree: {resolved}")


def git_environment(home: pathlib.Path) -> dict[str, str]:
    """Return a non-interactive Git environment with no ambient configuration."""
    return {
        "PATH": SAFE_PATH,
        "HOME": str(home),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_ASKPASS": os.devnull,
        "GCM_INTERACTIVE": "never",
        "GIT_NO_REPLACE_OBJECTS": "1",
        "GIT_OPTIONAL_LOCKS": "0",
    }


def git_prefix() -> list[str]:
    return [
        require_tool("git"),
        "-c",
        "core.hooksPath=/dev/null",
        "-c",
        "core.fsmonitor=false",
        "-c",
        "credential.helper=",
        "-c",
        "protocol.allow=never",
        "-c",
        "protocol.https.allow=always",
    ]


def git_capture(
    root: pathlib.Path,
    arguments: Sequence[str],
    *,
    description: str,
    home: pathlib.Path | None = None,
) -> str:
    safe_home = home or root
    return capture(
        [*git_prefix(), "-C", str(root), *arguments],
        cwd=root,
        env=git_environment(safe_home),
        description=description,
    )


def checkout_state(root: pathlib.Path) -> tuple[str, str, str]:
    head = git_capture(
        root,
        ["rev-parse", "--verify", "HEAD"],
        description=f"HEAD lookup in {root}",
    )
    dirty = git_capture(
        root,
        [
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
            "--ignore-submodules=none",
        ],
        description=f"worktree cleanliness check in {root}",
    )
    replacements = git_capture(
        root,
        ["for-each-ref", "--format=%(refname)", "refs/replace"],
        description=f"replacement-object check in {root}",
    )
    return head, dirty, replacements


def blob_oid(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()  # noqa: S324 - Git object ID


def expected_file(root: pathlib.Path, commit: str, relative: str) -> tuple[str, str]:
    raw = git_capture(
        root,
        ["ls-tree", commit, "--", relative],
        description=f"tree lookup for {relative}",
    )
    lines = raw.splitlines()
    if len(lines) != 1 or "\t" not in lines[0]:
        raise Refusal(f"{relative} is not one unambiguous tracked file at {commit}")
    metadata, found_path = lines[0].split("\t", 1)
    parts = metadata.split()
    if len(parts) != 3 or found_path != relative or parts[1] != "blob":
        raise Refusal(f"{relative} is not a regular tracked blob at {commit}")
    mode, _, oid = parts
    if mode not in ("100644", "100755") or not SHA_RE.fullmatch(oid):
        raise Refusal(f"{relative} has unsupported mode or object ID at {commit}")
    return mode, oid


def validate_file_bytes(root: pathlib.Path, commit: str, relative: str) -> None:
    expected_mode, expected_oid = expected_file(root, commit, relative)
    try:
        data, info = read_regular_file_bounded(
            root,
            relative,
            maximum=MAX_CHECKED_FILE_BYTES,
            description="checked-out file",
        )
    except (OSError, ValueError) as exc:
        raise Refusal(f"cannot read checked-out {relative}: {exc}") from exc
    actual_mode = "100755" if info.st_mode & stat.S_IXUSR else "100644"
    if actual_mode != expected_mode or blob_oid(data) != expected_oid:
        raise Refusal(
            f"checked-out {relative} bytes/mode do not match commit {commit}; "
            "index flags cannot hide workflow edits"
        )


def validate_checkout(
    pr: PullRequest,
    root: pathlib.Path,
    workflows: Sequence[str],
    *,
    label: str,
) -> None:
    if not root.is_dir():
        raise Refusal(f"{label} is not a directory: {root}")
    head, dirty, replacements = checkout_state(root)
    if replacements:
        raise Refusal(
            f"{label} has replacement refs ({replacements.splitlines()[0]})"
        )
    if dirty:
        raise Refusal(f"{label} is dirty (first entry: {dirty.splitlines()[0]})")
    if not SHA_RE.fullmatch(head):
        raise Refusal(f"{label} HEAD is not a full commit SHA: {head!r}")
    if head != pr.head_sha:
        raise Refusal(
            f"{label} HEAD {head} is not PR head {pr.head_sha}; fetch and "
            "check out the exact pushed head"
        )
    for workflow in workflows:
        validate_file_bytes(root, pr.head_sha, WORKFLOWS[workflow])


def validate_trusted_runner(pr: PullRequest) -> None:
    """Refuse a runner loaded from the candidate or a modified/stale base."""
    head, dirty, replacements = checkout_state(ROOT)
    if replacements:
        raise Refusal(
            "trusted runner worktree has replacement refs; use a clean dev worktree"
        )
    if dirty:
        raise Refusal(
            "trusted runner worktree is dirty; invoke the exact clean remote dev copy"
        )
    if head != pr.base_sha:
        raise Refusal(
            f"runner was loaded from {head}, not current PR base {pr.base_sha}; "
            "invoke scripts/act_ci.py from a clean trusted dev worktree"
        )
    try:
        relative = pathlib.Path(__file__).resolve().relative_to(ROOT).as_posix()
    except ValueError as exc:
        raise Refusal("runner is not installed beneath its trusted repository") from exc
    validate_file_bytes(ROOT, pr.base_sha, relative)


def validate_installed_runner_file(
    path: pathlib.Path, expected_sha256: str, candidate_worktree: pathlib.Path
) -> None:
    """Validate an independently audited, content-pinned bootstrap install."""
    if not re.fullmatch(r"[0-9a-f]{64}", expected_sha256):
        raise Refusal("--trusted-install-sha256 requires 64 lowercase hex digits")
    absolute = path.absolute()
    try:
        source_info = absolute.lstat()
    except OSError as exc:
        raise Refusal(f"cannot inspect installed runner {absolute}: {exc}") from exc
    if stat.S_ISLNK(source_info.st_mode) or not stat.S_ISREG(source_info.st_mode):
        raise Refusal("installed runner must be a non-symlink regular file")
    resolved = absolute.resolve()
    if resolved == candidate_worktree or resolved.is_relative_to(candidate_worktree):
        raise Refusal("installed runner is inside the candidate worktree")
    if source_info.st_mode & (stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH):
        raise Refusal("installed runner must have no writable mode bits")
    try:
        actual = hashlib.sha256(resolved.read_bytes()).hexdigest()
    except OSError as exc:
        raise Refusal(f"cannot read installed runner {resolved}: {exc}") from exc
    if actual != expected_sha256:
        raise Refusal(
            f"installed runner SHA-256 {actual} does not match audited pin "
            f"{expected_sha256}"
        )


def validate_runner(
    pr: PullRequest,
    candidate_worktree: pathlib.Path,
    trusted_install_sha256: str | None,
) -> None:
    if trusted_install_sha256 is None:
        validate_trusted_runner(pr)
        return
    validate_installed_runner_file(
        pathlib.Path(__file__), trusted_install_sha256, candidate_worktree
    )


def validate_bootstrap_options(
    trusted_install_sha256: str | None,
    repository_argument: str | None,
    worktree_argument: pathlib.Path | None,
) -> None:
    if trusted_install_sha256 is not None and (
        repository_argument is None or worktree_argument is None
    ):
        raise Refusal(
            "--trusted-install-sha256 requires explicit --repo and --worktree"
        )


def make_run_directory(
    lease: RunDirectoryLease | None = None,
    *,
    after_create: Callable[[], None] | None = None,
    inspect_path: Callable[[pathlib.Path], os.stat_result] = pathlib.Path.lstat,
) -> RunDirectory:
    """Acquire a private run directory while its mutable lease is registered."""
    active_lease = lease or RunDirectoryLease(
        pathlib.Path(tempfile.gettempdir()).resolve()
    )
    if (
        active_lease.path is not None
        or active_lease.run is not None
        or active_lease.accepted
        or active_lease.released
    ):
        raise Refusal("refusing to reuse an initialized run-directory lease")
    try:
        # A delivered signal cannot land between mkdir returning and the lease
        # recording that accepted mutation. The caller's pre-registered lease
        # also closes the function-return/CALL-to-STORE handoff window.
        with blocked_cleanup_signals():
            for _attempt in range(128):
                path = active_lease.parent / (
                    f"milan-act-ci-{secrets.token_hex(16)}"
                )
                active_lease.path = path
                try:
                    path.mkdir(mode=0o700)
                except FileExistsError:
                    active_lease.path = None
                    continue
                active_lease.accepted = True
                if after_create is not None:
                    after_create()
                try:
                    info = inspect_path(path)
                except OSError as exc:
                    raise Refusal(
                        f"cannot inspect new temporary run directory {path}: {exc}"
                    ) from exc
                if not stat.S_ISDIR(info.st_mode):
                    raise Refusal("new temporary run path is not a directory")
                run = RunDirectory(
                    path,
                    active_lease.parent,
                    info.st_dev,
                    info.st_ino,
                )
                active_lease.run = run
                return run
        raise Refusal("cannot allocate an unpredictable temporary run directory")
    except BaseException as primary:
        try:
            with blocked_cleanup_signals():
                cleanup_partial_run_directory(active_lease, use_sudo=False)
        except Refusal as cleanup_error:
            raise Refusal(
                f"temporary run-directory setup rollback failed: {cleanup_error}"
            ) from primary
        raise


def cleanup_partial_run_directory(
    lease: RunDirectoryLease,
    use_sudo: bool,
    *,
    run_command: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    remove_tree: Callable[[pathlib.Path], None] = shutil.rmtree,
    sudo_binary: str | None = None,
) -> None:
    """Reconcile an accepted directory even before its identity was returned."""
    if lease.released or not lease.accepted:
        return
    if lease.path is None:
        raise Refusal("accepted temporary run directory has no recorded path")
    run = lease.run
    if run is None:
        try:
            info = lease.path.lstat()
        except OSError as exc:
            raise Refusal(
                f"cannot inspect partial temporary run directory {lease.path}: {exc}"
            ) from exc
        if not stat.S_ISDIR(info.st_mode):
            raise Refusal(
                f"partial temporary run path is not a directory: {lease.path}"
            )
        run = RunDirectory(
            lease.path,
            lease.parent,
            info.st_dev,
            info.st_ino,
        )
        lease.run = run
    cleanup_run_directory(
        run,
        use_sudo,
        run_command=run_command,
        remove_tree=remove_tree,
        sudo_binary=sudo_binary,
    )
    lease.released = True


def cleanup_run_directory(
    run: RunDirectory,
    use_sudo: bool,
    *,
    run_command: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    remove_tree: Callable[[pathlib.Path], None] = shutil.rmtree,
    sudo_binary: str | None = None,
) -> None:
    path = run.path
    if path.parent.resolve() != run.parent or not path.name.startswith("milan-act-ci-"):
        raise Refusal(f"refusing cleanup outside the exact generated run path: {path}")
    if not path.exists() and not path.is_symlink():
        return
    try:
        info = path.lstat()
    except OSError as exc:
        raise Refusal(f"cannot inspect temporary run directory {path}: {exc}") from exc
    if (
        not stat.S_ISDIR(info.st_mode)
        or info.st_dev != run.device
        or info.st_ino != run.inode
    ):
        raise Refusal(f"temporary run directory identity changed; not deleting {path}")
    if use_sudo:
        sudo = sudo_binary or require_tool("sudo")
        command = [
            sudo,
            "-n",
            "--",
            require_tool("chown"),
            "-R",
            f"{os.getuid()}:{os.getgid()}",
            str(path),
        ]
        try:
            if run_command is subprocess.run:
                result = run_tracked_process_group_command(
                    command,
                    cwd=run.parent,
                    env={"PATH": SAFE_PATH, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"},
                    timeout=RUN_DIRECTORY_RECLAIM_TIMEOUT,
                    use_sudo=True,
                )
            else:
                result = run_command(
                    command,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )
        except subprocess.TimeoutExpired as exc:
            raise Refusal(f"sudo ownership recovery timed out for {path}") from exc
        except (OSError, UnicodeError) as exc:
            raise Refusal(
                f"cannot launch or decode sudo ownership recovery for {path}: {exc}"
            ) from exc
        if result.returncode != 0:
            detail = (result.stderr or "").strip().splitlines()
            suffix = f": {detail[-1]}" if detail else ""
            raise Refusal(f"cannot reclaim sudo-owned run data at {path}{suffix}")
    try:
        remove_tree(path)
    except OSError as exc:
        raise Refusal(f"cannot remove temporary run directory {path}: {exc}") from exc
    if path.exists():
        raise Refusal(f"temporary run directory still exists after cleanup: {path}")


@contextlib.contextmanager
def temporary_run_directory(use_sudo: bool) -> Iterator[pathlib.Path]:
    lease = RunDirectoryLease(pathlib.Path(tempfile.gettempdir()).resolve())
    try:
        run = make_run_directory(lease)
        yield run.path
    finally:
        if lease.accepted and not lease.released:
            with blocked_cleanup_signals():
                cleanup_partial_run_directory(lease, use_sudo)


def make_layout(run_root: pathlib.Path, pr: PullRequest) -> RunLayout:
    state = run_root / "state" / pr.head_sha
    layout = RunLayout(
        root=run_root,
        checkout=run_root / "candidate" / pr.head_sha,
        invocation=run_root / "invocation",
        home=run_root / "home",
        xdg_config=run_root / "xdg-config",
        xdg_cache=run_root / "xdg-cache",
        xdg_data=run_root / "xdg-data",
        temporary=run_root / "tmp",
        artifacts=state / "artifacts",
        action_cache=state / "actions",
        cache_server=state / "workflow-cache",
        event_path=state / "event.json",
        env_file=state / "empty.env",
        secret_file=state / "empty.secrets",
        var_file=state / "empty.vars",
        input_file=state / "empty.input",
    )
    for directory in (
        layout.invocation,
        layout.home,
        layout.xdg_config,
        layout.xdg_cache,
        layout.xdg_data,
        layout.temporary,
        layout.artifacts,
        layout.action_cache,
        layout.cache_server,
        layout.event_path.parent,
    ):
        directory.mkdir(parents=True, exist_ok=True)
    for empty_file in (
        layout.env_file,
        layout.secret_file,
        layout.var_file,
        layout.input_file,
    ):
        empty_file.write_text("", encoding="utf-8")
    return layout


def controlled_act_environment(layout: RunLayout) -> dict[str, str]:
    """The complete host environment visible to act; no ambient values survive."""
    return {
        "PATH": SAFE_PATH,
        "HOME": str(layout.home),
        "XDG_CONFIG_HOME": str(layout.xdg_config),
        "XDG_CACHE_HOME": str(layout.xdg_cache),
        "XDG_DATA_HOME": str(layout.xdg_data),
        "TMPDIR": str(layout.temporary),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
    }


def validate_isolation_layout(layout: RunLayout) -> None:
    """Refuse any effective act config/input planted in the private boundary."""
    forbidden = (
        layout.xdg_config / "act" / "actrc",
        layout.home / ".actrc",
        layout.invocation / ".actrc",
        layout.invocation / ".env",
        layout.invocation / ".secrets",
        layout.invocation / ".vars",
        layout.invocation / ".input",
    )
    for path in forbidden:
        if path.exists() or path.is_symlink():
            raise Refusal(f"private act boundary contains ambient input: {path}")
    for path in (
        layout.env_file,
        layout.secret_file,
        layout.var_file,
        layout.input_file,
    ):
        try:
            info = path.lstat()
            content = path.read_bytes()
        except OSError as exc:
            raise Refusal(f"cannot verify explicit empty act input {path}: {exc}") from exc
        if not stat.S_ISREG(info.st_mode) or content:
            raise Refusal(f"explicit act input is not an empty regular file: {path}")


def expected_submodule_config() -> dict[str, str]:
    expected: dict[str, str] = {}
    for name, path, url in TRUSTED_SUBMODULES:
        expected[f"submodule.{name}.path"] = path
        expected[f"submodule.{name}.url"] = url
    return expected


def validate_submodule_manifest(
    checkout: pathlib.Path, commit: str, gitlinks: Sequence[str]
) -> None:
    """Validate the committed manifest before any candidate-directed fetch."""
    _mode, oid = expected_file(checkout, commit, ".gitmodules")
    size_text = git_capture(
        checkout,
        ["cat-file", "-s", oid],
        home=checkout.parent,
        description="candidate .gitmodules size check",
    )
    try:
        size = int(size_text)
    except ValueError as exc:
        raise Refusal("Git returned an invalid .gitmodules blob size") from exc
    if not 0 <= size <= MAX_GITMODULES_BYTES:
        raise Refusal(
            f".gitmodules exceeds the {MAX_GITMODULES_BYTES}-byte safety limit"
        )

    raw = git_capture(
        checkout,
        ["config", "--null", "--list", f"--blob={commit}:.gitmodules"],
        home=checkout.parent,
        description="candidate .gitmodules parse",
    )
    actual: dict[str, str] = {}
    records = raw.split("\0")
    if records and records[-1] == "":
        records.pop()
    for record in records:
        if "\n" not in record:
            raise Refusal("candidate .gitmodules contains a malformed entry")
        key, value = record.split("\n", 1)
        if key in actual:
            raise Refusal(f"candidate .gitmodules repeats {key!r}")
        actual[key] = value

    expected = expected_submodule_config()
    if actual != expected:
        missing = sorted(expected.keys() - actual.keys())
        unexpected = sorted(actual.keys() - expected.keys())
        changed = sorted(
            key
            for key in expected.keys() & actual.keys()
            if expected[key] != actual[key]
        )
        details: list[str] = []
        if missing:
            details.append(f"missing {missing[0]!r}")
        if unexpected:
            details.append(f"unexpected {unexpected[0]!r}")
        if changed:
            details.append(f"changed {changed[0]!r}")
        raise Refusal(
            "candidate .gitmodules differs from the trusted manifest"
            + (f" ({'; '.join(details)})" if details else "")
        )

    expected_gitlinks = {path for _name, path, _url in TRUSTED_SUBMODULES}
    actual_gitlinks = set(gitlinks)
    if actual_gitlinks != expected_gitlinks or len(gitlinks) != len(actual_gitlinks):
        raise Refusal("candidate gitlinks differ from the trusted submodule paths")


def initialize_required_submodules(checkout: pathlib.Path, home: pathlib.Path) -> None:
    """Fetch only the HTTPS dependencies approved by the trusted manifest."""
    capture(
        [
            *git_prefix(),
            "-C",
            str(checkout),
            "submodule",
            "update",
            "--init",
            "--",
            *REQUIRED_SUBMODULES,
        ],
        cwd=checkout,
        env=git_environment(home),
        description="trusted public pinned submodule materialization",
    )


def materialize_remote_head(
    pr: PullRequest, repository: str, layout: RunLayout
) -> pathlib.Path:
    """Fetch the public same-repository refs into a new credential-free repo."""
    checkout = layout.checkout
    checkout.mkdir(parents=True)
    env = git_environment(layout.home)
    prefix = git_prefix()
    capture(
        [*prefix, "init", "--quiet", str(checkout)],
        cwd=layout.root,
        env=env,
        description="isolated candidate repository creation",
    )
    remote_url = f"https://github.com/{repository}.git"
    capture(
        [*prefix, "-C", str(checkout), "remote", "add", "origin", remote_url],
        cwd=layout.root,
        env=env,
        description="isolated candidate remote setup",
    )
    capture(
        [
            *prefix,
            "-C",
            str(checkout),
            "fetch",
            "--force",
            "--no-tags",
            "origin",
            f"refs/heads/{DEFAULT_BASE}:refs/remotes/origin/{DEFAULT_BASE}",
            f"refs/pull/{pr.number}/head:refs/remotes/origin/pr/{pr.number}",
        ],
        cwd=layout.root,
        env=env,
        description="exact remote PR/base fetch",
    )
    fetched_base = git_capture(
        checkout,
        ["rev-parse", f"refs/remotes/origin/{DEFAULT_BASE}^{{commit}}"],
        home=layout.home,
        description="fetched base verification",
    )
    fetched_head = git_capture(
        checkout,
        ["rev-parse", f"refs/remotes/origin/pr/{pr.number}^{{commit}}"],
        home=layout.home,
        description="fetched PR head verification",
    )
    if fetched_base != pr.base_sha or fetched_head != pr.head_sha:
        raise Refusal(
            "remote refs changed between metadata lookup and fetch; discard this run"
        )
    tree = git_capture(
        checkout,
        ["ls-tree", "-r", pr.head_sha],
        home=layout.home,
        description="candidate tree mode check",
    )
    gitlinks: list[str] = []
    for line in tree.splitlines():
        if line.startswith("120000 "):
            path = line.split("\t", 1)[-1]
            raise Refusal(f"candidate tree contains unsupported symlink: {path}")
        if line.startswith("160000 "):
            gitlinks.append(line.split("\t", 1)[-1])
    validate_submodule_manifest(checkout, pr.head_sha, gitlinks)
    capture(
        [*prefix, "-C", str(checkout), "checkout", "--quiet", "--detach", pr.head_sha],
        cwd=layout.root,
        env=env,
        description="exact candidate checkout",
    )
    # A hosted checkout presents each uninitialised gitlink as an empty path;
    # docs link checks intentionally run before selected submodules are fetched.
    # Fresh Git versions may omit those empty directories, so materialise only
    # the checked gitlink paths. Empty directories do not dirty the checkout.
    for relative in gitlinks:
        target = (checkout / relative).resolve()
        if not target.is_relative_to(checkout):
            raise Refusal(f"candidate gitlink escapes the checkout: {relative}")
        target.mkdir(parents=True, exist_ok=True)
    return checkout


def read_regular_file_bounded(
    root: pathlib.Path,
    relative: str,
    *,
    maximum: int,
    description: str,
) -> tuple[bytes, os.stat_result]:
    """Read one regular file beneath root without following any symlink."""
    relative_path = pathlib.PurePosixPath(relative)
    parts = relative_path.parts
    display = root / relative
    if (
        relative_path.is_absolute()
        or not parts
        or any(part in ("", ".", "..") for part in parts)
    ):
        raise Refusal(f"{description} has an unsafe relative path: {relative}")
    directory_flags = os.O_RDONLY | os.O_CLOEXEC | os.O_DIRECTORY | os.O_NOFOLLOW
    file_flags = os.O_RDONLY | os.O_CLOEXEC | os.O_NONBLOCK | os.O_NOFOLLOW
    descriptors: list[int] = []
    try:
        current = os.open(root, directory_flags)
        descriptors.append(current)
        for component in parts[:-1]:
            current = os.open(component, directory_flags, dir_fd=current)
            descriptors.append(current)
        selected = os.open(parts[-1], file_flags, dir_fd=current)
        descriptors.append(selected)
        info = os.fstat(selected)
        if not stat.S_ISREG(info.st_mode):
            raise Refusal(f"{description} is not a regular file: {display}")
        if info.st_size > maximum:
            raise Refusal(
                f"{description} exceeds the {maximum}-byte safety limit: {display}"
            )
        chunks: list[bytes] = []
        total = 0
        while total <= maximum:
            chunk = os.read(selected, min(65536, maximum + 1 - total))
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
        if total > maximum:
            raise Refusal(
                f"{description} exceeds the {maximum}-byte safety limit: {display}"
            )
        return b"".join(chunks), info
    except Refusal:
        raise
    except OSError as exc:
        raise Refusal(f"cannot safely read {description} {display}: {exc}") from exc
    finally:
        for descriptor in reversed(descriptors):
            try:
                os.close(descriptor)
            except OSError:
                pass


def load_workflow(root: pathlib.Path, relative: str) -> dict[str, object]:
    path = root / relative
    try:
        raw, _info = read_regular_file_bounded(
            root,
            relative,
            maximum=MAX_WORKFLOW_BYTES,
            description="workflow",
        )
    except ValueError as exc:
        raise Refusal(f"cannot safely read workflow {path}: {exc}") from exc
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeError as exc:
        raise Refusal(f"workflow is not valid UTF-8: {path}") from exc
    if re.search(r"(^|[\s\[{,])[&*][A-Za-z0-9_-]+", text):
        raise Refusal(f"workflow YAML anchors/aliases are unsupported: {path}")
    try:
        import yaml
        from yaml.constructor import ConstructorError
    except ImportError as exc:
        raise Refusal("PyYAML is required for workflow sandbox validation") from exc

    class UniqueKeyLoader(yaml.BaseLoader):
        def construct_mapping(self, node, deep=False):  # type: ignore[no-untyped-def]
            mapping = {}
            for key_node, value_node in node.value:
                key = self.construct_object(key_node, deep=deep)
                if not isinstance(key, str):
                    raise ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        "workflow mapping keys must be strings",
                        key_node.start_mark,
                    )
                if key in mapping:
                    raise ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate workflow key {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = self.construct_object(value_node, deep=deep)
            return mapping

    UniqueKeyLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        UniqueKeyLoader.construct_mapping,
    )
    try:
        loaded = yaml.load(text, Loader=UniqueKeyLoader)
    except (yaml.YAMLError, UnicodeError) as exc:
        raise Refusal(f"cannot safely parse workflow {path}: {exc}") from exc
    if not isinstance(loaded, dict):
        raise Refusal(f"workflow is not a mapping: {path}")
    return loaded


def validate_workflow_sandbox(root: pathlib.Path, workflows: Sequence[str]) -> None:
    """Reject workflow features that can ask host Docker for extra authority."""
    for workflow in workflows:
        relative = WORKFLOWS[workflow]
        document = load_workflow(root, relative)
        jobs = document.get("jobs")
        if not isinstance(jobs, dict) or not jobs:
            raise Refusal(f"workflow has no jobs mapping: {relative}")
        for job_id, job in jobs.items():
            if not isinstance(job_id, str) or not isinstance(job, dict):
                raise Refusal(f"workflow {relative} has a malformed job")
            if "uses" in job:
                raise Refusal(
                    f"workflow {relative} job {job_id} uses a reusable workflow; "
                    "the trusted sandbox cannot inspect its container policy"
                )
            if job.get("runs-on") != "ubuntu-latest":
                raise Refusal(
                    f"workflow {relative} job {job_id} must use literal ubuntu-latest"
                )
            if "container" in job or "services" in job:
                raise Refusal(
                    f"workflow {relative} job {job_id} requests job/service containers; "
                    "host mounts and container options are not allowed"
                )
            steps = job.get("steps")
            if not isinstance(steps, list) or not steps:
                raise Refusal(f"workflow {relative} job {job_id} has no steps list")
            for step_index, step in enumerate(steps):
                if not isinstance(step, dict):
                    raise Refusal(
                        f"workflow {relative} job {job_id} step {step_index} "
                        "is not a mapping"
                    )
                action = step.get("uses")
                if action is None:
                    continue
                if not isinstance(action, str) or action not in TRUSTED_ACTION_USES:
                    raise Refusal(
                        f"workflow {relative} job {job_id} step {step_index} uses "
                        f"unapproved action {action!r}; local, docker://, and "
                        "unaudited remote actions can execute through the host "
                        "Docker daemon"
                    )


def build_event(pr: PullRequest, repository: str) -> dict[str, object]:
    """The smallest pull_request payload every repository workflow consumes."""
    action = "synchronize" if pr.draft else "ready_for_review"
    return {
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


def isolated_command_prefix(
    executable: str, use_sudo: bool, env: Mapping[str, str]
) -> list[str]:
    if not use_sudo:
        return [executable]
    assignments = [f"{key}={value}" for key, value in sorted(env.items())]
    return [
        require_tool("sudo"),
        "-n",
        "--",
        require_tool("env"),
        "-i",
        *assignments,
        executable,
    ]


def docker_prefix(use_sudo: bool, env: Mapping[str, str]) -> list[str]:
    return isolated_command_prefix(require_tool("docker"), use_sudo, env)


def run_docker(
    arguments: Sequence[str],
    *,
    use_sudo: bool,
    cwd: pathlib.Path,
    env: Mapping[str, str],
    description: str,
    check: bool = True,
    run_command: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> subprocess.CompletedProcess[str]:
    command = [*docker_prefix(use_sudo, env), *arguments]
    try:
        if run_command is subprocess.run:
            result = run_tracked_process_group_command(
                command,
                cwd=cwd,
                env=env,
                timeout=DOCKER_COMMAND_TIMEOUT,
                use_sudo=use_sudo,
            )
        else:
            result = run_command(
                command,
                cwd=cwd,
                env=dict(env),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=DOCKER_COMMAND_TIMEOUT,
                check=False,
            )
    except subprocess.TimeoutExpired as exc:
        raise Refusal(f"{description} timed out") from exc
    except (OSError, UnicodeError) as exc:
        raise Refusal(f"cannot run {description}: {exc}") from exc
    if check and result.returncode != 0:
        detail = (result.stderr or "").strip().splitlines()
        suffix = f": {detail[-1]}" if detail else ""
        raise Refusal(f"{description} failed{suffix}")
    return result


def docker_reports_missing_toolcache(
    result: subprocess.CompletedProcess[str],
) -> bool:
    detail = (result.stderr or "").lower()
    return (
        result.returncode != 0
        and ACT_TOOLCACHE_VOLUME in detail
        and "no such volume" in detail
    )


def docker_reports_missing_network(
    result: subprocess.CompletedProcess[str], target: str
) -> bool:
    detail = (result.stderr or "").lower()
    return (
        result.returncode != 0
        and target.lower() in detail
        and ("no such network" in detail or "not found" in detail)
    )


def decode_act_toolcache_volume(text: str) -> Mapping[str, object]:
    try:
        volumes = json.loads(text)
        volume = volumes[0]
    except (json.JSONDecodeError, IndexError, KeyError, TypeError) as exc:
        raise Refusal("Docker returned malformed act tool-cache metadata") from exc
    if not isinstance(volumes, list) or len(volumes) != 1 or not isinstance(
        volume, dict
    ):
        raise Refusal("Docker returned malformed act tool-cache metadata")
    return volume


def parse_act_toolcache_volume(
    text: str, boundary: DockerBoundary
) -> Mapping[str, object]:
    volume = decode_act_toolcache_volume(text)
    labels = volume.get("Labels")
    if (
        volume.get("Name") != ACT_TOOLCACHE_VOLUME
        or volume.get("Driver") != "local"
        or volume.get("Scope") != "local"
        or not isinstance(labels, dict)
        or labels.get(DOCKER_OWNER_LABEL) != boundary.token
    ):
        raise Refusal("act tool-cache volume identity or ownership changed")
    return volume


def require_act_toolcache_absent(
    *,
    use_sudo: bool,
    cwd: pathlib.Path,
    env: Mapping[str, str],
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
) -> None:
    result = docker_command(
        ["volume", "inspect", ACT_TOOLCACHE_VOLUME],
        use_sudo=use_sudo,
        cwd=cwd,
        env=env,
        description="act tool-cache absence check",
        check=False,
    )
    if result.returncode == 0:
        raise Refusal(
            f"shared Docker volume {ACT_TOOLCACHE_VOLUME!r} already exists; "
            f"inspect its {DOCKER_OWNER_LABEL!r} label; serialize every act "
            "runner and prove no container uses an unlabelled legacy cache "
            "before removal, or remove a labelled cache only after proving no "
            "runner, container, or network with that owner token remains"
        )
    if not docker_reports_missing_toolcache(result):
        detail = (result.stderr or "").strip().splitlines()
        suffix = f": {detail[-1]}" if detail else ""
        raise Refusal(f"cannot verify act tool-cache absence{suffix}")


def inspect_act_toolcache_volume(
    boundary: DockerBoundary,
    *,
    use_sudo: bool,
    cwd: pathlib.Path,
    env: Mapping[str, str],
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
) -> Mapping[str, object]:
    if not boundary.toolcache_owned:
        raise Refusal("Docker boundary has no owned act tool-cache volume")
    result = docker_command(
        ["volume", "inspect", ACT_TOOLCACHE_VOLUME],
        use_sudo=use_sudo,
        cwd=cwd,
        env=env,
        description="act tool-cache inspection",
        check=False,
    )
    if result.returncode != 0:
        if docker_reports_missing_toolcache(result):
            raise Refusal("owned act tool-cache volume disappeared")
        detail = (result.stderr or "").strip().splitlines()
        suffix = f": {detail[-1]}" if detail else ""
        raise Refusal(f"act tool-cache inspection failed{suffix}")
    return parse_act_toolcache_volume(result.stdout, boundary)


def discard_act_toolcache_if_owned(
    boundary: DockerBoundary,
    *,
    use_sudo: bool,
    cwd: pathlib.Path,
    env: Mapping[str, str],
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
    stability_window: float | None = None,
    monotonic: Callable[[], float] = time.monotonic,
    sleep: Callable[[float], None] = time.sleep,
) -> None:
    """Remove an owned cache and require a stable post-CLI absence window."""
    window = (
        DOCKER_MUTATION_STABLE_SECONDS
        if stability_window is None and docker_command is run_docker
        else (stability_window or 0)
    )
    stable_since: float | None = None
    removals = 0
    while True:
        result = docker_command(
            ["volume", "inspect", ACT_TOOLCACHE_VOLUME],
            use_sudo=use_sudo,
            cwd=cwd,
            env=env,
            description="partial act tool-cache inspection",
            check=False,
        )
        if result.returncode != 0:
            if not docker_reports_missing_toolcache(result):
                detail = (result.stderr or "").strip().splitlines()
                suffix = f": {detail[-1]}" if detail else ""
                raise Refusal(f"cannot reconcile partial act tool cache{suffix}")
            now = monotonic()
            if stable_since is None:
                stable_since = now
            remaining = window - (now - stable_since)
            if remaining <= 1e-6:
                return
            sleep(min(0.05, remaining))
            continue
        stable_since = None
        volume = decode_act_toolcache_volume(result.stdout)
        labels = volume.get("Labels")
        if not isinstance(labels, dict):
            raise Refusal("partial act tool cache has malformed ownership labels")
        if labels.get(DOCKER_OWNER_LABEL) != boundary.token:
            return
        parse_act_toolcache_volume(
            result.stdout, replace(boundary, toolcache_owned=True)
        )
        if removals >= 3:
            raise Refusal("owned act tool cache survived repeated rollback")
        removed = docker_command(
            ["volume", "rm", ACT_TOOLCACHE_VOLUME],
            use_sudo=use_sudo,
            cwd=cwd,
            env=env,
            description="partial act tool-cache rollback",
            check=False,
        )
        if removed.returncode != 0:
            detail = (removed.stderr or "").strip().splitlines()
            suffix = f": {detail[-1]}" if detail else ""
            raise Refusal(f"partial act tool-cache rollback failed{suffix}")
        removals += 1


def create_act_toolcache_volume(
    planned: DockerBoundary,
    *,
    use_sudo: bool,
    cwd: pathlib.Path,
    env: Mapping[str, str],
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
) -> DockerBoundary:
    if planned.toolcache_owned:
        raise Refusal("refusing to recreate an initialized act tool-cache volume")
    require_act_toolcache_absent(
        use_sudo=use_sudo, cwd=cwd, env=env, docker_command=docker_command
    )
    boundary = replace(planned, toolcache_owned=True)
    try:
        result = docker_command(
            [
                "volume",
                "create",
                "--driver",
                "local",
                "--label",
                f"{DOCKER_OWNER_LABEL}={planned.token}",
                ACT_TOOLCACHE_VOLUME,
            ],
            use_sudo=use_sudo,
            cwd=cwd,
            env=env,
            description="ephemeral act tool-cache creation",
        )
        if result.stdout.strip() != ACT_TOOLCACHE_VOLUME:
            raise Refusal("Docker returned the wrong act tool-cache volume name")
        inspect_act_toolcache_volume(
            boundary,
            use_sudo=use_sudo,
            cwd=cwd,
            env=env,
            docker_command=docker_command,
        )
    except BaseException as primary:
        try:
            with blocked_cleanup_signals():
                discard_act_toolcache_if_owned(
                    boundary,
                    use_sudo=use_sudo,
                    cwd=cwd,
                    env=env,
                    docker_command=docker_command,
                )
        except Refusal as cleanup_error:
            raise Refusal(
                f"act tool-cache setup rollback failed: {cleanup_error}"
            ) from primary
        raise
    return boundary


def cleanup_act_toolcache_volume(
    boundary: DockerBoundary,
    *,
    use_sudo: bool,
    cwd: pathlib.Path,
    env: Mapping[str, str],
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
) -> None:
    inspect_act_toolcache_volume(
        boundary,
        use_sudo=use_sudo,
        cwd=cwd,
        env=env,
        docker_command=docker_command,
    )
    result = docker_command(
        ["volume", "rm", ACT_TOOLCACHE_VOLUME],
        use_sudo=use_sudo,
        cwd=cwd,
        env=env,
        description="ephemeral act tool-cache removal",
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or "").strip().splitlines()
        suffix = f": {detail[-1]}" if detail else ""
        raise Refusal(f"act tool-cache removal failed{suffix}")
    discard_act_toolcache_if_owned(
        boundary,
        use_sudo=use_sudo,
        cwd=cwd,
        env=env,
        docker_command=docker_command,
    )
    require_act_toolcache_absent(
        use_sudo=use_sudo,
        cwd=cwd,
        env=env,
        docker_command=docker_command,
    )


def new_docker_boundary() -> DockerBoundary:
    token = secrets.token_hex(16)
    if not re.fullmatch(r"[0-9a-f]{32}", token):
        raise Refusal("cannot generate a safe Docker ownership token")
    return DockerBoundary(token=token, name=f"milan-act-ci-{token}")


def inspect_docker_network(
    boundary: DockerBoundary,
    *,
    use_sudo: bool,
    cwd: pathlib.Path,
    env: Mapping[str, str],
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
) -> str:
    if boundary.network_id is None or not DOCKER_ID_RE.fullmatch(boundary.network_id):
        raise Refusal("Docker boundary has no valid network ID")
    result = docker_command(
        ["network", "inspect", boundary.network_id],
        use_sudo=use_sudo,
        cwd=cwd,
        env=env,
        description="Docker boundary inspection",
    )
    try:
        networks = json.loads(result.stdout)
        network = networks[0]
        actual_id = network["Id"]
        actual_name = network["Name"]
        labels = network["Labels"]
        ipam_config = network["IPAM"]["Config"]
    except (json.JSONDecodeError, IndexError, KeyError, TypeError) as exc:
        raise Refusal("Docker returned malformed boundary metadata") from exc
    if not isinstance(labels, dict):
        raise Refusal("Docker boundary has no ownership labels")
    if not isinstance(ipam_config, list):
        raise Refusal("Docker boundary has malformed IPAM configuration")
    gateways: list[str] = []
    for entry in ipam_config:
        if not isinstance(entry, dict) or "Gateway" not in entry:
            continue
        raw_gateway = entry["Gateway"]
        if not isinstance(raw_gateway, str):
            raise Refusal("Docker boundary has a malformed gateway address")
        try:
            gateway_address = ipaddress.ip_address(raw_gateway)
        except ValueError as exc:
            raise Refusal("Docker boundary has an invalid gateway address") from exc
        if gateway_address.version == 4:
            gateways.append(str(gateway_address))
    if len(gateways) != 1:
        raise Refusal(
            "Docker boundary must expose exactly one IPv4 bridge gateway"
        )
    gateway = gateways[0]
    if (
        actual_id != boundary.network_id
        or actual_name != boundary.name
        or labels.get(DOCKER_OWNER_LABEL) != boundary.token
        or (boundary.gateway is not None and boundary.gateway != gateway)
    ):
        raise Refusal("Docker boundary identity, ownership, or gateway changed")
    return gateway


def inspect_docker_boundary(
    boundary: DockerBoundary,
    *,
    use_sudo: bool,
    cwd: pathlib.Path,
    env: Mapping[str, str],
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
) -> str:
    gateway = inspect_docker_network(
        boundary,
        use_sudo=use_sudo,
        cwd=cwd,
        env=env,
        docker_command=docker_command,
    )
    inspect_act_toolcache_volume(
        boundary,
        use_sudo=use_sudo,
        cwd=cwd,
        env=env,
        docker_command=docker_command,
    )
    return gateway


def discard_docker_network_if_owned(
    boundary: DockerBoundary,
    *,
    use_sudo: bool,
    cwd: pathlib.Path,
    env: Mapping[str, str],
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
    stability_window: float | None = None,
    monotonic: Callable[[], float] = time.monotonic,
    sleep: Callable[[float], None] = time.sleep,
) -> None:
    """Remove an owned network and require a stable post-CLI absence window."""
    window = (
        DOCKER_MUTATION_STABLE_SECONDS
        if stability_window is None and docker_command is run_docker
        else (stability_window or 0)
    )
    stable_since: float | None = None
    removals = 0
    while True:
        result = docker_command(
            ["network", "inspect", boundary.name],
            use_sudo=use_sudo,
            cwd=cwd,
            env=env,
            description="partial Docker boundary inspection",
            check=False,
        )
        if result.returncode != 0:
            if not docker_reports_missing_network(result, boundary.name):
                detail = (result.stderr or "").strip().splitlines()
                suffix = f": {detail[-1]}" if detail else ""
                raise Refusal(f"cannot reconcile partial Docker boundary{suffix}")
            now = monotonic()
            if stable_since is None:
                stable_since = now
            remaining = window - (now - stable_since)
            if remaining <= 1e-6:
                return
            sleep(min(0.05, remaining))
            continue
        stable_since = None
        try:
            networks = json.loads(result.stdout)
            network = networks[0]
            network_id = network["Id"]
            name = network["Name"]
            labels = network["Labels"]
        except (json.JSONDecodeError, IndexError, KeyError, TypeError) as exc:
            raise Refusal("Docker returned malformed partial boundary metadata") from exc
        if not isinstance(labels, dict):
            raise Refusal("partial Docker boundary has malformed ownership labels")
        if name != boundary.name or labels.get(DOCKER_OWNER_LABEL) != boundary.token:
            return
        if not isinstance(network_id, str) or not DOCKER_ID_RE.fullmatch(network_id):
            raise Refusal("partial Docker boundary has a malformed network ID")
        if removals >= 3:
            raise Refusal("owned Docker boundary survived repeated rollback")
        removed = docker_command(
            ["network", "rm", network_id],
            use_sudo=use_sudo,
            cwd=cwd,
            env=env,
            description="partial Docker boundary rollback",
            check=False,
        )
        if removed.returncode != 0:
            detail = (removed.stderr or "").strip().splitlines()
            suffix = f": {detail[-1]}" if detail else ""
            raise Refusal(f"partial Docker boundary rollback failed{suffix}")
        removals += 1


def cleanup_partial_docker_boundary(
    boundary: DockerBoundary,
    *,
    use_sudo: bool,
    cwd: pathlib.Path,
    env: Mapping[str, str],
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
) -> None:
    errors: list[str] = []
    for cleanup in (discard_docker_network_if_owned, discard_act_toolcache_if_owned):
        try:
            cleanup(
                boundary,
                use_sudo=use_sudo,
                cwd=cwd,
                env=env,
                docker_command=docker_command,
            )
        except Refusal as exc:
            errors.append(str(exc))
    if errors:
        raise Refusal("partial Docker boundary cleanup failed: " + "; ".join(errors))


def create_docker_boundary(
    planned: DockerBoundary,
    *,
    use_sudo: bool,
    cwd: pathlib.Path,
    env: Mapping[str, str],
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
    lease: DockerBoundaryLease | None = None,
    after_toolcache: Callable[[], None] | None = None,
) -> DockerBoundary:
    if planned.network_id is not None or planned.toolcache_owned:
        raise Refusal("refusing to recreate an initialized Docker boundary")
    active_lease = lease or DockerBoundaryLease(planned)
    if (
        active_lease.boundary != planned
        or active_lease.complete
        or active_lease.released
    ):
        raise Refusal("Docker boundary lease was not initialized from the plan")
    boundary = planned
    try:
        boundary = create_act_toolcache_volume(
            planned,
            use_sudo=use_sudo,
            cwd=cwd,
            env=env,
            docker_command=docker_command,
        )
        active_lease.boundary = boundary
        if after_toolcache is not None:
            after_toolcache()
        result = docker_command(
            [
                "network",
                "create",
                "--driver",
                "bridge",
                "--label",
                f"{DOCKER_OWNER_LABEL}={planned.token}",
                planned.name,
            ],
            use_sudo=use_sudo,
            cwd=cwd,
            env=env,
            description="isolated Docker network creation",
        )
        network_id = result.stdout.strip()
        if not DOCKER_ID_RE.fullmatch(network_id):
            raise Refusal("Docker returned an invalid boundary network ID")
        boundary = replace(boundary, network_id=network_id)
        active_lease.boundary = boundary
        gateway = inspect_docker_boundary(
            boundary,
            use_sudo=use_sudo,
            cwd=cwd,
            env=env,
            docker_command=docker_command,
        )
        boundary = replace(boundary, gateway=gateway)
        active_lease.boundary = boundary
        active_lease.complete = True
    except BaseException as primary:
        try:
            with blocked_cleanup_signals():
                cleanup_partial_docker_boundary(
                    active_lease.boundary,
                    use_sudo=use_sudo,
                    cwd=cwd,
                    env=env,
                    docker_command=docker_command,
                )
                active_lease.released = True
        except Refusal as cleanup_error:
            raise Refusal(
                f"Docker boundary setup rollback failed: {cleanup_error}"
            ) from primary
        raise
    return boundary


def docker_container_inventory(
    *,
    use_sudo: bool,
    cwd: pathlib.Path,
    env: Mapping[str, str],
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
    cancel: threading.Event | None = None,
) -> list[dict[str, object]]:
    if cancel is not None and cancel.is_set():
        return []
    listed = docker_command(
        ["container", "ls", "--all", "--quiet", "--no-trunc"],
        use_sudo=use_sudo,
        cwd=cwd,
        env=env,
        description="Docker container inventory",
    )
    if cancel is not None and cancel.is_set():
        return []
    ids = [line for line in listed.stdout.splitlines() if line]
    if len(ids) != len(set(ids)) or any(
        not DOCKER_ID_RE.fullmatch(item) for item in ids
    ):
        raise Refusal("Docker returned an invalid container inventory")
    inventory: list[dict[str, object]] = []
    for requested_id in ids:
        if cancel is not None and cancel.is_set():
            return []
        inspected = docker_command(
            ["container", "inspect", requested_id],
            use_sudo=use_sudo,
            cwd=cwd,
            env=env,
            description="Docker container metadata inspection",
            check=False,
        )
        if cancel is not None and cancel.is_set():
            return []
        if inspected.returncode != 0:
            # An act cleanup or an unrelated host task may remove a container
            # between the inventory and inspection. Its absence is already the
            # cleanup result we need; every other daemon error fails closed.
            if "No such container:" in inspected.stderr:
                continue
            detail = inspected.stderr.strip().splitlines()
            suffix = f": {detail[-1]}" if detail else ""
            raise Refusal(f"Docker container metadata inspection failed{suffix}")
        try:
            raw = json.loads(inspected.stdout)
            item = raw[0]
        except (json.JSONDecodeError, IndexError, TypeError) as exc:
            raise Refusal("Docker returned malformed container metadata") from exc
        if not isinstance(item, dict):
            raise Refusal("Docker returned a malformed container entry")
        container_id = item.get("Id")
        if not isinstance(container_id, str) or not DOCKER_ID_RE.fullmatch(
            container_id
        ):
            raise Refusal("Docker returned a malformed container ID")
        if container_id != requested_id:
            raise Refusal("Docker returned metadata for the wrong container")
        inventory.append(item)
        if cancel is not None and cancel.is_set():
            return []
    return inventory


def owned_container_ids(
    inventory: Sequence[Mapping[str, object]], boundary: DockerBoundary
) -> set[str]:
    """Select only containers proven to belong to this unpredictable boundary."""
    records: dict[str, Mapping[str, object]] = {}
    names: dict[str, str] = {}
    owned: set[str] = set()
    for item in inventory:
        container_id = item.get("Id")
        if not isinstance(container_id, str) or not DOCKER_ID_RE.fullmatch(
            container_id
        ):
            raise Refusal("cannot establish ownership of a malformed container ID")
        records[container_id] = item
        raw_name = item.get("Name")
        if isinstance(raw_name, str) and raw_name.startswith("/") and len(raw_name) > 1:
            names[raw_name[1:]] = container_id

        config = item.get("Config")
        labels = config.get("Labels") if isinstance(config, dict) else None
        host_config = item.get("HostConfig")
        network_mode = (
            host_config.get("NetworkMode") if isinstance(host_config, dict) else None
        )
        network_settings = item.get("NetworkSettings")
        networks = (
            network_settings.get("Networks")
            if isinstance(network_settings, dict)
            else None
        )
        label_owned = (
            isinstance(labels, dict)
            and labels.get(DOCKER_OWNER_LABEL) == boundary.token
        )
        mode_owned = network_mode == boundary.name or (
            boundary.network_id is not None and network_mode == boundary.network_id
        )
        network_owned = isinstance(networks, dict) and boundary.name in networks
        if label_owned or mode_owned or network_owned:
            owned.add(container_id)

    changed = True
    while changed:
        changed = False
        for container_id, item in records.items():
            if container_id in owned:
                continue
            host_config = item.get("HostConfig")
            network_mode = (
                host_config.get("NetworkMode")
                if isinstance(host_config, dict)
                else None
            )
            if not isinstance(network_mode, str) or not network_mode.startswith(
                "container:"
            ):
                continue
            target = network_mode.removeprefix("container:")
            if not target:
                raise Refusal("Docker returned an empty container-network target")
            matches = {known_id for known_id in records if known_id.startswith(target)}
            if target in names:
                matches.add(names[target])
            if len(matches) > 1:
                raise Refusal("Docker returned an ambiguous container-network target")
            if matches.intersection(owned):
                owned.add(container_id)
                changed = True
    return owned


def running_container_ids(
    inventory: Sequence[Mapping[str, object]], selected: set[str]
) -> list[str]:
    running: list[str] = []
    for item in inventory:
        container_id = item.get("Id")
        if container_id not in selected:
            continue
        state = item.get("State")
        if isinstance(state, dict) and state.get("Running") is True:
            if not isinstance(container_id, str):
                raise Refusal("Docker returned a malformed running container ID")
            running.append(container_id)
    return sorted(running)


def verify_runner_toolcache_mounts(
    inventory: Sequence[Mapping[str, object]],
    boundary: DockerBoundary,
    *,
    require_any: bool,
) -> int:
    """Prove every directly labeled act job uses the owned global cache slot."""
    verified = 0
    for item in inventory:
        config = item.get("Config")
        labels = config.get("Labels") if isinstance(config, dict) else None
        if not (
            isinstance(labels, dict)
            and labels.get(DOCKER_OWNER_LABEL) == boundary.token
        ):
            continue
        mounts = item.get("Mounts")
        if not isinstance(mounts, list):
            raise Refusal("owned act container has malformed mount metadata")
        candidates = [
            mount
            for mount in mounts
            if isinstance(mount, dict)
            and (
                mount.get("Name") == ACT_TOOLCACHE_VOLUME
                or mount.get("Destination") == ACT_TOOLCACHE_TARGET
            )
        ]
        if (
            len(candidates) != 1
            or candidates[0].get("Type") != "volume"
            or candidates[0].get("Name") != ACT_TOOLCACHE_VOLUME
            or candidates[0].get("Destination") != ACT_TOOLCACHE_TARGET
            or candidates[0].get("RW") is not True
        ):
            raise Refusal(
                "owned act container does not use exactly the verified ephemeral "
                "tool-cache volume"
            )
        verified += 1
    if require_any and verified == 0:
        raise Refusal("no owned act container exposed a verifiable tool-cache mount")
    return verified


def cleanup_owned_containers(
    boundary: DockerBoundary,
    *,
    use_sudo: bool,
    cwd: pathlib.Path,
    env: Mapping[str, str],
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
) -> int:
    inventory = docker_container_inventory(
        use_sudo=use_sudo, cwd=cwd, env=env, docker_command=docker_command
    )
    owned = owned_container_ids(inventory, boundary)
    initial_count = len(owned)
    attempt_errors: list[str] = []
    running = running_container_ids(inventory, owned)
    if running:
        try:
            result = docker_command(
                ["container", "stop", "--time", "3", *running],
                use_sudo=use_sudo,
                cwd=cwd,
                env=env,
                description="owned Docker container stop",
                check=False,
            )
            if result.returncode != 0:
                attempt_errors.append("graceful stop failed")
        except Refusal as exc:
            attempt_errors.append(str(exc))

    try:
        inventory = docker_container_inventory(
            use_sudo=use_sudo,
            cwd=cwd,
            env=env,
            docker_command=docker_command,
        )
        remaining = sorted(owned_container_ids(inventory, boundary))
    except Refusal as exc:
        attempt_errors.append(str(exc))
        remaining = sorted(owned)
    if remaining:
        try:
            result = docker_command(
                ["container", "rm", "--force", "--volumes", *remaining],
                use_sudo=use_sudo,
                cwd=cwd,
                env=env,
                description="owned Docker container removal",
                check=False,
            )
            if result.returncode != 0:
                attempt_errors.append("forced removal failed")
        except Refusal as exc:
            attempt_errors.append(str(exc))

    verification_errors: list[str] = []
    try:
        final_inventory = docker_container_inventory(
            use_sudo=use_sudo,
            cwd=cwd,
            env=env,
            docker_command=docker_command,
        )
        survivors = owned_container_ids(final_inventory, boundary)
        if survivors:
            verification_errors.append(
                f"{len(survivors)} owned container(s) survived cleanup"
            )
    except Refusal as exc:
        verification_errors.append(str(exc))
    if verification_errors:
        details = [*attempt_errors, *verification_errors]
        raise Refusal("Docker container cleanup failed: " + "; ".join(details))
    return initial_count


def cleanup_docker_boundary(
    boundary: DockerBoundary,
    *,
    use_sudo: bool,
    cwd: pathlib.Path,
    env: Mapping[str, str],
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
) -> None:
    errors: list[str] = []
    try:
        cleanup_owned_containers(
            boundary,
            use_sudo=use_sudo,
            cwd=cwd,
            env=env,
            docker_command=docker_command,
        )
    except Refusal as exc:
        errors.append(str(exc))
    try:
        inspect_docker_network(
            boundary,
            use_sudo=use_sudo,
            cwd=cwd,
            env=env,
            docker_command=docker_command,
        )
    except Refusal as exc:
        errors.append(str(exc))
    else:
        network_id = boundary.network_id
        if network_id is None:
            errors.append("Docker boundary has no network ID during cleanup")
            network_id = boundary.name
        try:
            result = docker_command(
                ["network", "rm", network_id],
                use_sudo=use_sudo,
                cwd=cwd,
                env=env,
                description="Docker boundary network removal",
                check=False,
            )
            if result.returncode != 0:
                errors.append("Docker boundary network removal failed")
        except Refusal as exc:
            errors.append(str(exc))

    if docker_command is run_docker:
        try:
            discard_docker_network_if_owned(
                boundary,
                use_sudo=use_sudo,
                cwd=cwd,
                env=env,
                docker_command=docker_command,
            )
            name_check = docker_command(
                ["network", "inspect", boundary.name],
                use_sudo=use_sudo,
                cwd=cwd,
                env=env,
                description="Docker boundary name absence check",
                check=False,
            )
            if name_check.returncode == 0:
                errors.append("Docker boundary network name survived cleanup")
            elif not docker_reports_missing_network(name_check, boundary.name):
                detail = name_check.stderr.strip().splitlines()
                suffix = f": {detail[-1]}" if detail else ""
                errors.append(f"cannot verify Docker boundary name absence{suffix}")
        except Refusal as exc:
            errors.append(str(exc))

    try:
        cleanup_act_toolcache_volume(
            boundary,
            use_sudo=use_sudo,
            cwd=cwd,
            env=env,
            docker_command=docker_command,
        )
    except Refusal as exc:
        errors.append(str(exc))

    if boundary.network_id is not None:
        try:
            result = docker_command(
                ["network", "inspect", boundary.network_id],
                use_sudo=use_sudo,
                cwd=cwd,
                env=env,
                description="Docker boundary absence check",
                check=False,
            )
            if result.returncode == 0:
                errors.append("Docker boundary network survived cleanup")
            elif not any(
                marker in result.stderr
                for marker in (
                    f"network {boundary.network_id} not found",
                    f"No such network: {boundary.network_id}",
                )
            ):
                detail = result.stderr.strip().splitlines()
                suffix = f": {detail[-1]}" if detail else ""
                errors.append(f"cannot verify Docker boundary absence{suffix}")
        except Refusal as exc:
            errors.append(str(exc))
    try:
        final_inventory = docker_container_inventory(
            use_sudo=use_sudo,
            cwd=cwd,
            env=env,
            docker_command=docker_command,
        )
        survivors = owned_container_ids(final_inventory, boundary)
        if survivors:
            errors.append(f"{len(survivors)} owned container(s) remain")
    except Refusal as exc:
        errors.append(str(exc))
    if errors:
        raise Refusal("Docker boundary cleanup failed: " + "; ".join(errors))


@contextlib.contextmanager
def temporary_docker_boundary(
    planned: DockerBoundary,
    *,
    use_sudo: bool,
    cwd: pathlib.Path,
    env: Mapping[str, str],
) -> Iterator[DockerBoundary]:
    lease = DockerBoundaryLease(planned)
    try:
        create_docker_boundary(
            planned,
            use_sudo=use_sudo,
            cwd=cwd,
            env=env,
            lease=lease,
        )
        yield lease.boundary
    finally:
        if not lease.released:
            with blocked_cleanup_signals():
                if lease.complete:
                    cleanup_docker_boundary(
                        lease.boundary,
                        use_sudo=use_sudo,
                        cwd=cwd,
                        env=env,
                    )
                else:
                    cleanup_partial_docker_boundary(
                        lease.boundary,
                        use_sudo=use_sudo,
                        cwd=cwd,
                        env=env,
                    )
                lease.released = True


def act_prefix(act_binary: str, use_sudo: bool, env: Mapping[str, str]) -> list[str]:
    return isolated_command_prefix(act_binary, use_sudo, env)


def build_act_command(
    prefix: Sequence[str],
    workflow: str,
    layout: RunLayout,
    artifact_port: int,
    boundary: DockerBoundary,
) -> list[str]:
    if not 1 <= artifact_port <= 65535:
        raise Refusal(f"invalid artifact-server port: {artifact_port}")
    if not boundary.toolcache_owned:
        raise Refusal("Docker boundary has no exclusive act tool-cache volume")
    try:
        gateway = ipaddress.ip_address(boundary.gateway or "")
    except ValueError as exc:
        raise Refusal("Docker boundary has no valid server-bind gateway") from exc
    if gateway.version != 4:
        raise Refusal("Docker boundary server-bind gateway must be IPv4")
    server_address = str(gateway)
    artifact_path = layout.artifacts / workflow
    artifact_path.mkdir(parents=True, exist_ok=True)
    return [
        *prefix,
        "pull_request",
        "--strict",
        "--no-recurse",
        "--rm",
        "--directory",
        str(layout.checkout),
        "--workflows",
        str(layout.checkout / WORKFLOWS[workflow]),
        "--eventpath",
        str(layout.event_path),
        "--platform",
        f"ubuntu-latest={RUNNER_IMAGE}",
        "--artifact-server-path",
        str(artifact_path),
        "--artifact-server-addr",
        server_address,
        "--artifact-server-port",
        str(artifact_port),
        "--action-cache-path",
        str(layout.action_cache),
        "--cache-server-path",
        str(layout.cache_server),
        "--cache-server-addr",
        server_address,
        "--cache-server-port",
        "0",
        "--env-file",
        str(layout.env_file),
        "--secret-file",
        str(layout.secret_file),
        "--var-file",
        str(layout.var_file),
        "--input-file",
        str(layout.input_file),
        "--secret",
        "GITHUB_TOKEN=",
        "--container-daemon-socket",
        "-",
        "--container-options",
        f"--label={DOCKER_OWNER_LABEL}={boundary.token}",
        "--network",
        boundary.name,
    ]


def allocate_tcp_port() -> int:
    """Select a currently free host port; a later bind race fails closed in act."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.bind(("", 0))
            port = listener.getsockname()[1]
    except OSError as exc:
        raise Refusal(f"cannot allocate an artifact-server port: {exc}") from exc
    if not isinstance(port, int) or not 1 <= port <= 65535:
        raise Refusal(f"host returned an invalid artifact-server port: {port!r}")
    return port


def terminate_act_process_group(
    process: subprocess.Popen[object],
    *,
    use_sudo: bool,
    primary: BaseException,
    group_exists: Callable[..., bool] | None = None,
    signal_group: Callable[..., None] | None = None,
    escalation: Sequence[tuple[int, float]] = (
        (signal.SIGINT, 10),
        (signal.SIGTERM, 10),
        (signal.SIGKILL, 5),
    ),
    sleep: Callable[[float], None] = time.sleep,
    recovery_notice: Callable[[str], None] | None = None,
) -> None:
    check_group = group_exists or process_group_exists
    send_group_signal = signal_group or signal_process_group
    notify_recovery = recovery_notice or (
        lambda message: print(message, file=sys.stderr, flush=True)
    )
    group_absent = False
    for sent_signal, timeout in escalation:
        try:
            if not check_group(process.pid, use_sudo=use_sudo):
                group_absent = True
                break
        except Exception:
            # Inspection failure must not suppress the privileged signal.
            pass
        try:
            send_group_signal(process.pid, sent_signal, use_sudo=use_sudo)
        except ProcessLookupError:
            # A missing result is encouraging but is not the final proof; the
            # absence check below remains authoritative.
            pass
        except Exception:
            # Escalate through the remaining signals, then require proof.
            continue
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                process.poll()
            except Exception:
                pass
            try:
                if not check_group(process.pid, use_sudo=use_sudo):
                    group_absent = True
                    break
            except Exception:
                pass
            try:
                sleep(0.1)
            except Exception:
                pass
        if group_absent:
            break

    # Detection is not containment. If the escalation could not establish
    # absence, stay on this side of the Docker boundary and keep using bounded
    # kill/check commands until the group is provably gone. An operator can
    # restore sudo/daemon health or terminate the printed PGID externally.
    recovery_round = 0
    while not group_absent:
        recovery_round += 1
        detail = "still live"
        try:
            group_absent = not check_group(process.pid, use_sudo=use_sudo)
        except Exception as exc:
            detail = f"absence is unprovable ({exc})"
        if group_absent:
            break
        try:
            send_group_signal(process.pid, signal.SIGKILL, use_sudo=use_sudo)
        except ProcessLookupError:
            detail = "kill reports missing; awaiting independent absence proof"
        except Exception as exc:
            detail = f"kill failed ({exc})"
        if recovery_round == 1 or recovery_round % 20 == 0:
            try:
                notify_recovery(
                    "act-ci: containment hold for host process group "
                    f"{process.pid}: {detail}; Docker teardown is paused. "
                    "Restore sudo/kill access or terminate that process group "
                    "externally; retrying until absence is proven."
                )
            except Exception:
                # Diagnostics have no authority to release containment.
                pass
        try:
            process.poll()
        except Exception:
            pass
        try:
            sleep(0.25)
        except Exception:
            pass

    try:
        process.wait(timeout=1)
    except subprocess.TimeoutExpired:
        raise Refusal("cannot reap interrupted host process leader") from primary


def run_act_process(
    command: Sequence[str],
    *,
    cwd: pathlib.Path,
    env: Mapping[str, str],
    check: bool = False,
    started: Callable[[int], None] | None = None,
    use_sudo: bool = False,
    popen: Callable[..., subprocess.Popen[object]] = subprocess.Popen,
    terminate_group: Callable[..., None] = terminate_act_process_group,
    before_terminate_group: Callable[[], None] | None = None,
) -> subprocess.CompletedProcess[object]:
    """Run act in its own process group and reap that group on interruption."""
    del check  # This boundary always returns the workflow status to its caller.
    process: subprocess.Popen[object] | None = None
    try:
        # Latch parent cleanup signals across fork/exec, Popen return, and
        # assignment. Caught dispositions reset on exec, so unlike a blocked
        # mask this does not prevent the act child receiving INT/TERM/HUP.
        with deferred_cleanup_signal_delivery():
            process = popen(
                command,
                cwd=cwd,
                env=dict(env),
                start_new_session=True,
            )
        if started is not None:
            started(process.pid)
        returncode = process.wait()
        if process_group_exists(process.pid, use_sudo=use_sudo):
            raise Refusal("act process group survived its leader")
        return subprocess.CompletedProcess(command, returncode)
    except BaseException as primary:
        if process is not None:
            if before_terminate_group is not None:
                before_terminate_group()
            with blocked_cleanup_signals():
                terminate_group(process, use_sudo=use_sudo, primary=primary)
        raise


def sudo_process_group_signal(
    process_group: int,
    sent_signal: int,
    *,
    run_command: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> subprocess.CompletedProcess[str]:
    signal_name = (
        "0"
        if sent_signal == 0
        else signal.Signals(sent_signal).name.removeprefix("SIG")
    )
    try:
        return run_command(
            [
                require_tool("sudo"),
                "-n",
                "--",
                require_tool("kill"),
                f"-{signal_name}",
                "--",
                f"-{process_group}",
            ],
            env={
                "PATH": SAFE_PATH,
                "LANG": "C.UTF-8",
                "LC_ALL": "C.UTF-8",
            },
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=DOCKER_COMMAND_TIMEOUT,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise Refusal("privileged process-group signal timed out") from exc
    except OSError as exc:
        raise Refusal(f"cannot run privileged process-group signal: {exc}") from exc


def process_group_signal_reports_missing(
    result: subprocess.CompletedProcess[str],
) -> bool:
    return result.returncode != 0 and "no such process" in result.stderr.lower()


def process_group_exists(
    process_group: int,
    *,
    use_sudo: bool,
    run_command: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    kill_group: Callable[[int, int], None] = os.killpg,
) -> bool:
    if process_group <= 0:
        raise Refusal("invalid host process-group ID")
    if use_sudo:
        result = sudo_process_group_signal(
            process_group, 0, run_command=run_command
        )
        if result.returncode == 0:
            return True
        if process_group_signal_reports_missing(result):
            return False
        detail = result.stderr.strip().splitlines()
        suffix = f": {detail[-1]}" if detail else ""
        raise Refusal(f"cannot inspect host process group{suffix}")
    try:
        kill_group(process_group, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError as exc:
        raise Refusal("cannot inspect unprivileged host process group") from exc


def signal_process_group(
    process_group: int,
    sent_signal: int,
    *,
    use_sudo: bool,
    run_command: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    kill_group: Callable[[int, int], None] = os.killpg,
) -> None:
    if not use_sudo:
        try:
            kill_group(process_group, sent_signal)
            return
        except PermissionError as exc:
            raise Refusal("cannot signal unprivileged host process group") from exc
    result = sudo_process_group_signal(
        process_group, sent_signal, run_command=run_command
    )
    if result.returncode != 0:
        if process_group_signal_reports_missing(result):
            raise ProcessLookupError(process_group)
        detail = result.stderr.strip().splitlines()
        suffix = f": {detail[-1]}" if detail else ""
        raise Refusal(f"cannot signal host process group{suffix}")


def run_tracked_process_group_command(
    command: Sequence[str],
    *,
    cwd: pathlib.Path,
    env: Mapping[str, str],
    timeout: float,
    use_sudo: bool,
    popen: Callable[..., subprocess.Popen[str]] = subprocess.Popen,
    terminate_group: Callable[..., None] = terminate_act_process_group,
) -> subprocess.CompletedProcess[str]:
    """Run a host command without letting a sudo child outlive its CLI."""
    process: subprocess.Popen[str] | None = None
    group_absent = False
    current_mask = signal.pthread_sigmask(signal.SIG_BLOCK, set())
    cleanup_mask_inherited = all(item in current_mask for item in CLEANUP_SIGNALS)
    try:
        if (
            threading.current_thread() is threading.main_thread()
            and not cleanup_mask_inherited
        ):
            with deferred_cleanup_signal_delivery():
                process = popen(
                    command,
                    cwd=cwd,
                    env=dict(env),
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    start_new_session=True,
                )
        else:
            # Protected cleanup scopes and runner workers already have these
            # signals blocked, closing the Popen handoff; workers also cannot
            # call signal.signal(). A failed child is killed as a complete
            # PGID below, with SIGKILL first because the mask survives exec.
            process = popen(
                command,
                cwd=cwd,
                env=dict(env),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True,
            )
        stdout, stderr = process.communicate(timeout=timeout)
        if process_group_exists(process.pid, use_sudo=use_sudo):
            raise Refusal("host command process group survived its leader")
        group_absent = True
        return subprocess.CompletedProcess(
            command,
            process.returncode,
            stdout,
            stderr,
        )
    except BaseException as primary:
        if process is not None and not group_absent:
            with blocked_cleanup_signals():
                if (
                    terminate_group is terminate_act_process_group
                    and (
                        threading.current_thread() is not threading.main_thread()
                        or cleanup_mask_inherited
                    )
                ):
                    terminate_group(
                        process,
                        use_sudo=use_sudo,
                        primary=primary,
                        escalation=((signal.SIGKILL, 5),),
                    )
                else:
                    terminate_group(process, use_sudo=use_sudo, primary=primary)
                # The leader is reaped above; drain its captured pipes without
                # allowing pipe cleanup to precede process-group containment.
                try:
                    process.communicate(timeout=1)
                except subprocess.TimeoutExpired as exc:
                    raise Refusal(
                        "cannot drain terminated host command pipes"
                    ) from exc
        raise


def process_group_inventory(process_group: int) -> list[tuple[int, str, int]]:
    """Return (pid, state, effective uid) for one host process group."""
    try:
        result = subprocess.run(
            [require_tool("ps"), "-eo", "pid=,pgid=,stat=,euid="],
            env={"PATH": SAFE_PATH, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=DOCKER_COMMAND_TIMEOUT,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise Refusal("act process-group inventory timed out") from exc
    if result.returncode != 0:
        detail = result.stderr.strip().splitlines()
        suffix = f": {detail[-1]}" if detail else ""
        raise Refusal(f"cannot inventory act process group{suffix}")
    members: list[tuple[int, str, int]] = []
    for line in result.stdout.splitlines():
        fields = line.split()
        if len(fields) != 4:
            raise Refusal("host returned malformed process-group metadata")
        try:
            pid, pgid, effective_uid = int(fields[0]), int(fields[1]), int(fields[3])
        except ValueError as exc:
            raise Refusal("host returned malformed process-group identity") from exc
        if pgid == process_group:
            members.append((pid, fields[2], effective_uid))
    return sorted(members)


def wait_for_frozen_process_group(
    process_group: int,
    expected_pids: set[int],
    *,
    timeout: float = 5,
) -> list[tuple[int, str, int]]:
    deadline = time.monotonic() + timeout
    while True:
        members = process_group_inventory(process_group)
        current_pids = {pid for pid, _state, _uid in members}
        if (
            members
            and expected_pids.issubset(current_pids)
            and all(state.startswith("T") for _pid, state, _uid in members)
        ):
            return members
        if time.monotonic() >= deadline:
            raise Refusal("act process group did not freeze completely")
        time.sleep(0.1)


def require_runtime(
    act_binary: str,
    use_sudo: bool,
    layout: RunLayout,
    env: Mapping[str, str],
) -> list[str]:
    version_text = capture(
        [act_binary, "--version"],
        cwd=layout.invocation,
        env=env,
        description="act version check",
    )
    version = parse_act_version(version_text)
    require_supported_act_version(version)

    run_docker(
        ["info", "--format", "{{.ServerVersion}}"],
        use_sudo=use_sudo,
        cwd=layout.invocation,
        env=env,
        description="Docker daemon check",
    )
    return act_prefix(act_binary, use_sudo, env)


def execute_act_boundary(
    command: Sequence[str],
    *,
    pr: PullRequest,
    repository: str,
    cwd: pathlib.Path,
    env: Mapping[str, str],
    integrity_check: Callable[[], None],
    use_sudo: bool = False,
    query: Callable[[int, str], PullRequest] = query_pull_request,
    run_process: Callable[..., subprocess.CompletedProcess[object]] = run_act_process,
) -> int:
    """Bind one act process between fresh remote-state and byte checks."""
    require_live_pull_request(pr, repository, query)
    integrity_check()
    try:
        result = run_process(
            command,
            cwd=cwd,
            env=dict(env),
            check=False,
            use_sudo=use_sudo,
        )
    except OSError as exc:
        raise Refusal(f"cannot start act: {exc}") from exc
    require_live_pull_request(pr, repository, query)
    integrity_check()
    return result.returncode


def run_validation(
    pr: PullRequest,
    repository: str,
    workflows: Sequence[str],
    candidate_worktree: pathlib.Path,
    *,
    act_binary: str,
    use_sudo: bool,
    dry_run: bool,
) -> int:
    with temporary_run_directory(use_sudo and not dry_run) as run_root:
        layout = make_layout(run_root, pr)
        materialize_remote_head(pr, repository, layout)
        validate_checkout(
            pr, candidate_worktree, workflows, label="candidate worktree"
        )
        validate_checkout(pr, layout.checkout, workflows, label="materialized checkout")
        validate_workflow_sandbox(layout.checkout, workflows)
        initialize_required_submodules(layout.checkout, layout.home)
        validate_checkout(pr, layout.checkout, workflows, label="materialized checkout")
        require_live_pull_request(pr, repository)

        event = build_event(pr, repository)
        layout.event_path.write_text(
            json.dumps(event, indent=2) + "\n", encoding="utf-8"
        )
        env = controlled_act_environment(layout)
        validate_isolation_layout(layout)
        prefix = (
            act_prefix(act_binary, use_sudo, env)
            if dry_run
            else require_runtime(act_binary, use_sudo, layout, env)
        )
        planned_boundary = new_docker_boundary()
        print(f"act-ci: PR #{pr.number} {event['action']} exact head {pr.head_sha}")
        print(
            f"act-ci: base {pr.base_sha} ({pr.base_ref}), "
            f"draft={str(pr.draft).lower()}"
        )
        print("act-ci: credentials=none docker-socket=none caches=ephemeral")

        def integrity_check() -> None:
            validate_isolation_layout(layout)
            validate_checkout(
                pr, candidate_worktree, workflows, label="candidate worktree"
            )
            validate_checkout(
                pr, layout.checkout, workflows, label="materialized checkout"
            )

        def execute_workflows(boundary: DockerBoundary) -> int:
            for workflow in workflows:
                inspect_docker_boundary(
                    boundary,
                    use_sudo=use_sudo,
                    cwd=layout.invocation,
                    env=env,
                )
                artifact_port = allocate_tcp_port()
                command = build_act_command(
                    prefix, workflow, layout, artifact_port, boundary
                )
                if dry_run:
                    print(f"act-ci: {workflow}: {shlex.join(command)}")
                    continue
                print(
                    f"act-ci: running {workflow} ({WORKFLOWS[workflow]})",
                    flush=True,
                )
                result = execute_act_boundary(
                    command,
                    pr=pr,
                    repository=repository,
                    cwd=layout.invocation,
                    env=env,
                    integrity_check=integrity_check,
                    use_sudo=use_sudo,
                )
                leftovers = cleanup_owned_containers(
                    boundary,
                    use_sudo=use_sudo,
                    cwd=layout.invocation,
                    env=env,
                )
                if leftovers:
                    raise Refusal(
                        f"act left {leftovers} owned container(s) after {workflow}; "
                        "the runner removed them and refuses the run"
                    )
                if result != 0:
                    print(f"act-ci: {workflow}: FAILED ({result})", file=sys.stderr)
                    return RC_FAILED
                print(f"act-ci: {workflow}: PASS at {pr.head_sha}")
            require_live_pull_request(pr, repository)
            integrity_check()
            return RC_OK

        with temporary_docker_boundary(
            planned_boundary,
            use_sudo=use_sudo,
            cwd=layout.invocation,
            env=env,
        ) as boundary:
            return execute_workflows(boundary)


def expect_refusal(label: str, action: Callable[[], object]) -> bool:
    try:
        action()
    except Refusal:
        print(f"  ok   {label}")
        return True
    print(f"  FAIL {label}")
    return False


def selftest(shipping_root: pathlib.Path = ROOT) -> int:
    failures = 0

    def check(label: str, condition: bool) -> None:
        nonlocal failures
        print(f"  {'ok  ' if condition else 'FAIL'} {label}")
        failures += 0 if condition else 1

    def refused(label: str, action: Callable[[], object]) -> None:
        nonlocal failures
        failures += 0 if expect_refusal(label, action) else 1

    base = "1" * 40
    head = "2" * 40
    repository = "kebag-logic/milan-fpga"
    raw = {
        "number": 268,
        "state": "OPEN",
        "isDraft": False,
        "baseRefName": "dev",
        "baseRefOid": base,
        "headRefName": "268-act-first-validation",
        "headRefOid": head,
        "headRepository": {"nameWithOwner": repository},
        "headRepositoryOwner": {"login": "kebag-logic"},
        "isCrossRepository": False,
        "url": f"https://github.com/{repository}/pull/268",
    }
    pr = PullRequest.from_json(raw)
    validate_pull_request(pr, repository)
    event = build_event(pr, repository)
    event_pr = event["pull_request"]
    assert isinstance(event_pr, dict)
    check(
        "ready event is selected for a non-draft PR",
        event["action"] == "ready_for_review" and event_pr["draft"] is False,
    )
    check(
        "event pins the exact head and base",
        event_pr["head"]["sha"] == head and event_pr["base"]["sha"] == base,
    )
    check(
        "event names the repository default branch without private markers",
        event["repository"]["default_branch"] == DEFAULT_BASE
        and "milan_act_ci" not in event,
    )

    draft_raw = dict(raw)
    draft_raw["isDraft"] = True
    draft_event = build_event(PullRequest.from_json(draft_raw), repository)
    check(
        "draft event uses synchronize and preserves draft=true",
        draft_event["action"] == "synchronize"
        and draft_event["pull_request"]["draft"] is True,
    )
    check(
        "all selects each workflow once in stable order",
        select_workflows(["all"]) == tuple(WORKFLOWS),
    )
    check(
        "explicit workflow selection de-duplicates",
        select_workflows(["docs", "rtl-full", "docs"])
        == ("docs", "rtl-full"),
    )
    refused(
        "all plus another workflow is refused",
        lambda: select_workflows(["all", "docs"]),
    )

    cross_raw = dict(raw)
    cross_raw["isCrossRepository"] = True
    cross_raw["headRepository"] = {"nameWithOwner": "attacker/fork"}
    refused(
        "cross-repository candidate is refused",
        lambda: validate_pull_request(PullRequest.from_json(cross_raw), repository),
    )
    closed_raw = dict(raw)
    closed_raw["state"] = "MERGED"
    refused(
        "non-open pull request is refused",
        lambda: validate_pull_request(PullRequest.from_json(closed_raw), repository),
    )
    wrong_base = dict(raw)
    wrong_base["baseRefName"] = "main"
    refused(
        "non-dev pull request is refused",
        lambda: validate_pull_request(PullRequest.from_json(wrong_base), repository),
    )
    malformed = dict(raw)
    malformed["headRefOid"] = "short"
    refused(
        "malformed GitHub metadata is refused",
        lambda: PullRequest.from_json(malformed),
    )

    with temporary_run_directory(False) as first_root:
        first = make_layout(first_root, pr)
        other_pr = replace(pr, head_sha="3" * 40)
        with temporary_run_directory(False) as second_root:
            second = make_layout(second_root, other_pr)
            allocated_port = allocate_tcp_port()
            selftest_boundary = DockerBoundary(
                token="a" * 32,
                name=f"milan-act-ci-{'a' * 32}",
                network_id="b" * 64,
                gateway="172.30.0.1",
                toolcache_owned=True,
            )
            command = build_act_command(
                ["act"], "rtl-full", first, allocated_port, selftest_boundary
            )
            check(
                "act command selects the real strict exhaustive workflow",
                "--strict" in command
                and str(first.checkout / WORKFLOWS["rtl-full"]) in command,
            )
            check(
                "candidate checkout is copied from immutable materialization",
                "--no-skip-checkout" not in command
                and "--bind" not in command
                and str(first.checkout) in command,
            )
            check(
                "job containers receive no Docker socket or host network",
                command[command.index("--container-daemon-socket") + 1] == "-"
                and command[command.index("--network") + 1]
                == selftest_boundary.name
                and "--privileged" not in command,
            )
            check(
                "artifact and cache servers bind only to the bridge gateway",
                command[command.index("--artifact-server-addr") + 1]
                == selftest_boundary.gateway
                and command[command.index("--cache-server-addr") + 1]
                == selftest_boundary.gateway,
            )
            check(
                "job containers carry the unpredictable runner ownership label",
                command[command.index("--container-options") + 1]
                == f"--label={DOCKER_OWNER_LABEL}={selftest_boundary.token}",
            )
            check(
                "only an explicitly empty GitHub token reaches candidate jobs",
                command[command.index("--secret") + 1] == "GITHUB_TOKEN="
                and not any("ghp_" in value for value in command),
            )
            check(
                "every ambient act input is replaced by an explicit empty file",
                all(
                    flag in command
                    for flag in (
                        "--env-file",
                        "--secret-file",
                        "--var-file",
                        "--input-file",
                    )
                ),
            )
            check(
                "artifact uploads receive a real isolated listener port",
                command[command.index("--artifact-server-port") + 1]
                == str(allocated_port),
            )
            refused(
                "artifact-server port zero is refused rather than advertised",
                lambda: build_act_command(
                    ["act"], "docs", first, 0, selftest_boundary
                ),
            )
            refused(
                "a missing bridge gateway cannot produce an act command",
                lambda: build_act_command(
                    ["act"],
                    "docs",
                    first,
                    allocated_port,
                    replace(selftest_boundary, gateway=None),
                ),
            )
            refused(
                "a boundary without an exclusive tool cache cannot run act",
                lambda: build_act_command(
                    ["act"],
                    "docs",
                    first,
                    allocated_port,
                    replace(selftest_boundary, toolcache_owned=False),
                ),
            )
            volume_metadata = json.dumps(
                [
                    {
                        "Name": ACT_TOOLCACHE_VOLUME,
                        "Driver": "local",
                        "Scope": "local",
                        "Labels": {
                            DOCKER_OWNER_LABEL: selftest_boundary.token,
                        },
                    }
                ]
            )
            parse_act_toolcache_volume(volume_metadata, selftest_boundary)
            check("the labeled ephemeral act tool cache is accepted", True)
            refused(
                "a tool-cache volume owned by another run is refused",
                lambda: parse_act_toolcache_volume(
                    volume_metadata,
                    replace(selftest_boundary, token="f" * 32),
                ),
            )

            def docker_completed(
                arguments: Sequence[str],
                returncode: int = 0,
                stdout: str = "",
                stderr: str = "",
            ) -> subprocess.CompletedProcess[str]:
                return subprocess.CompletedProcess(
                    list(arguments), returncode, stdout, stderr
                )

            missing_volume = (
                f"Error response from daemon: No such volume: "
                f"{ACT_TOOLCACHE_VOLUME}"
            )
            foreign_volume_metadata = volume_metadata.replace(
                selftest_boundary.token, "f" * 32
            )
            unowned_calls: list[tuple[str, ...]] = []

            def unowned_volume(
                arguments: Sequence[str], **_kwargs: object
            ) -> subprocess.CompletedProcess[str]:
                call = tuple(arguments)
                unowned_calls.append(call)
                if call == ("volume", "inspect", ACT_TOOLCACHE_VOLUME):
                    return docker_completed(arguments, stdout=foreign_volume_metadata)
                raise AssertionError(f"unexpected Docker self-test call: {call}")

            existing_message = ""
            try:
                require_act_toolcache_absent(
                    use_sudo=False,
                    cwd=first.invocation,
                    env={},
                    docker_command=unowned_volume,
                )
            except Refusal as exc:
                existing_message = str(exc)
            check(
                "a pre-existing unowned tool cache is refused with label guidance",
                DOCKER_OWNER_LABEL in existing_message,
            )
            discard_act_toolcache_if_owned(
                selftest_boundary,
                use_sudo=False,
                cwd=first.invocation,
                env={},
                docker_command=unowned_volume,
            )
            check(
                "rollback never removes an unowned tool-cache volume",
                not any(call[:2] == ("volume", "rm") for call in unowned_calls),
            )

            race_calls: list[tuple[str, ...]] = []
            race_inspects = 0

            def rival_volume(
                arguments: Sequence[str], **_kwargs: object
            ) -> subprocess.CompletedProcess[str]:
                nonlocal race_inspects
                call = tuple(arguments)
                race_calls.append(call)
                if call == ("volume", "inspect", ACT_TOOLCACHE_VOLUME):
                    race_inspects += 1
                    if race_inspects == 1:
                        return docker_completed(arguments, 1, stderr=missing_volume)
                    return docker_completed(arguments, stdout=foreign_volume_metadata)
                if call[0:2] == ("volume", "create"):
                    return docker_completed(
                        arguments, stdout=f"{ACT_TOOLCACHE_VOLUME}\n"
                    )
                if call[:2] == ("volume", "rm"):
                    return docker_completed(arguments)
                raise AssertionError(f"unexpected Docker self-test call: {call}")

            refused(
                "a rival winning the tool-cache create race is refused",
                lambda: create_act_toolcache_volume(
                    replace(
                        selftest_boundary,
                        network_id=None,
                        gateway=None,
                        toolcache_owned=False,
                    ),
                    use_sudo=False,
                    cwd=first.invocation,
                    env={},
                    docker_command=rival_volume,
                ),
            )
            check(
                "create-race rollback never removes the rival's volume",
                not any(call[:2] == ("volume", "rm") for call in race_calls),
            )

            surviving_calls: list[tuple[str, ...]] = []

            def surviving_volume(
                arguments: Sequence[str], **_kwargs: object
            ) -> subprocess.CompletedProcess[str]:
                call = tuple(arguments)
                surviving_calls.append(call)
                if call == ("volume", "inspect", ACT_TOOLCACHE_VOLUME):
                    return docker_completed(arguments, stdout=volume_metadata)
                if call == ("volume", "rm", ACT_TOOLCACHE_VOLUME):
                    return docker_completed(arguments)
                raise AssertionError(f"unexpected Docker self-test call: {call}")

            refused(
                "tool-cache cleanup refuses when the volume survives removal",
                lambda: cleanup_act_toolcache_volume(
                    selftest_boundary,
                    use_sudo=False,
                    cwd=first.invocation,
                    env={},
                    docker_command=surviving_volume,
                ),
            )
            check(
                "surviving-volume control exercised the removal request",
                ("volume", "rm", ACT_TOOLCACHE_VOLUME) in surviving_calls,
            )

            accepted_volume = {"exists": False}
            accepted_volume_calls: list[tuple[str, ...]] = []

            def post_accept_volume_failure(
                arguments: Sequence[str], **_kwargs: object
            ) -> subprocess.CompletedProcess[str]:
                call = tuple(arguments)
                accepted_volume_calls.append(call)
                if call == ("volume", "inspect", ACT_TOOLCACHE_VOLUME):
                    if accepted_volume["exists"]:
                        return docker_completed(arguments, stdout=volume_metadata)
                    return docker_completed(arguments, 1, stderr=missing_volume)
                if call[0:2] == ("volume", "create"):
                    accepted_volume["exists"] = True
                    raise Refusal("injected post-accept volume timeout")
                if call == ("volume", "rm", ACT_TOOLCACHE_VOLUME):
                    accepted_volume["exists"] = False
                    return docker_completed(arguments)
                raise AssertionError(f"unexpected Docker self-test call: {call}")

            refused(
                "a post-accept volume-create timeout is reconciled",
                lambda: create_act_toolcache_volume(
                    replace(
                        selftest_boundary,
                        network_id=None,
                        gateway=None,
                        toolcache_owned=False,
                    ),
                    use_sudo=False,
                    cwd=first.invocation,
                    env={},
                    docker_command=post_accept_volume_failure,
                ),
            )
            check(
                "post-accept volume rollback removes and verifies its resource",
                not accepted_volume["exists"]
                and ("volume", "rm", ACT_TOOLCACHE_VOLUME)
                in accepted_volume_calls,
            )

            failed_volume_rollback = {"exists": False}

            def volume_rollback_failure(
                arguments: Sequence[str], **_kwargs: object
            ) -> subprocess.CompletedProcess[str]:
                call = tuple(arguments)
                if call == ("volume", "inspect", ACT_TOOLCACHE_VOLUME):
                    if failed_volume_rollback["exists"]:
                        return docker_completed(arguments, stdout=volume_metadata)
                    return docker_completed(arguments, 1, stderr=missing_volume)
                if call[0:2] == ("volume", "create"):
                    failed_volume_rollback["exists"] = True
                    raise Refusal("injected post-accept volume timeout")
                if call == ("volume", "rm", ACT_TOOLCACHE_VOLUME):
                    return docker_completed(
                        arguments, 1, stderr="injected volume rollback failure"
                    )
                raise AssertionError(f"unexpected Docker self-test call: {call}")

            rollback_message = ""
            try:
                create_act_toolcache_volume(
                    replace(
                        selftest_boundary,
                        network_id=None,
                        gateway=None,
                        toolcache_owned=False,
                    ),
                    use_sudo=False,
                    cwd=first.invocation,
                    env={},
                    docker_command=volume_rollback_failure,
                )
            except Refusal as exc:
                rollback_message = str(exc)
            check(
                "a failed setup rollback is surfaced rather than reported clean",
                "setup rollback failed" in rollback_message
                and failed_volume_rollback["exists"],
            )

            network_metadata = json.dumps(
                [
                    {
                        "Id": selftest_boundary.network_id,
                        "Name": selftest_boundary.name,
                        "Labels": {
                            DOCKER_OWNER_LABEL: selftest_boundary.token,
                        },
                        "IPAM": {"Config": [{"Gateway": selftest_boundary.gateway}]},
                    }
                ]
            )
            missing_network = (
                f"Error response from daemon: No such network: "
                f"{selftest_boundary.network_id}"
            )
            missing_network_name = (
                f"Error response from daemon: No such network: "
                f"{selftest_boundary.name}"
            )
            teardown_state = {"network": True}
            teardown_calls: list[tuple[str, ...]] = []

            def cache_failure_during_teardown(
                arguments: Sequence[str], **_kwargs: object
            ) -> subprocess.CompletedProcess[str]:
                call = tuple(arguments)
                teardown_calls.append(call)
                if call[0:2] == ("container", "ls"):
                    return docker_completed(arguments)
                if call == (
                    "network",
                    "inspect",
                    str(selftest_boundary.network_id),
                ):
                    if teardown_state["network"]:
                        return docker_completed(arguments, stdout=network_metadata)
                    return docker_completed(arguments, 1, stderr=missing_network)
                if call == (
                    "network",
                    "rm",
                    str(selftest_boundary.network_id),
                ):
                    teardown_state["network"] = False
                    return docker_completed(arguments)
                if call == ("volume", "inspect", ACT_TOOLCACHE_VOLUME):
                    return docker_completed(arguments, 1, stderr=missing_volume)
                raise AssertionError(f"unexpected Docker self-test call: {call}")

            teardown_message = ""
            try:
                cleanup_docker_boundary(
                    selftest_boundary,
                    use_sudo=False,
                    cwd=first.invocation,
                    env={},
                    docker_command=cache_failure_during_teardown,
                )
            except Refusal as exc:
                teardown_message = str(exc)
            check(
                "tool-cache failure cannot suppress independent network teardown",
                not teardown_state["network"]
                and "owned act tool-cache volume disappeared" in teardown_message
                and "network survived cleanup" not in teardown_message,
            )

            def run_network_setup_control(
                *,
                network_rm_fails: bool,
                interrupt_create: bool = False,
                interrupt_after_toolcache: bool = False,
            ) -> tuple[
                dict[str, bool], list[tuple[str, ...]], str
            ]:
                state = {"volume": False, "network": False}
                calls: list[tuple[str, ...]] = []

                def post_accept_network_failure(
                    arguments: Sequence[str], **_kwargs: object
                ) -> subprocess.CompletedProcess[str]:
                    call = tuple(arguments)
                    calls.append(call)
                    if call == ("volume", "inspect", ACT_TOOLCACHE_VOLUME):
                        if state["volume"]:
                            return docker_completed(arguments, stdout=volume_metadata)
                        return docker_completed(arguments, 1, stderr=missing_volume)
                    if call[0:2] == ("volume", "create"):
                        state["volume"] = True
                        return docker_completed(
                            arguments, stdout=f"{ACT_TOOLCACHE_VOLUME}\n"
                        )
                    if call == ("volume", "rm", ACT_TOOLCACHE_VOLUME):
                        state["volume"] = False
                        return docker_completed(arguments)
                    if call[0:2] == ("network", "create"):
                        state["network"] = True
                        if interrupt_create:
                            raise KeyboardInterrupt
                        raise Refusal("injected post-accept network timeout")
                    if call == ("network", "inspect", selftest_boundary.name):
                        if state["network"]:
                            return docker_completed(
                                arguments, stdout=network_metadata
                            )
                        return docker_completed(
                            arguments, 1, stderr=missing_network_name
                        )
                    if call == (
                        "network",
                        "rm",
                        str(selftest_boundary.network_id),
                    ):
                        if network_rm_fails:
                            return docker_completed(
                                arguments,
                                1,
                                stderr="injected network rollback failure",
                            )
                        state["network"] = False
                        return docker_completed(arguments)
                    if call == (
                        "network",
                        "inspect",
                        str(selftest_boundary.network_id),
                    ):
                        if state["network"]:
                            return docker_completed(arguments, stdout=network_metadata)
                        return docker_completed(arguments, 1, stderr=missing_network)
                    raise AssertionError(f"unexpected Docker self-test call: {call}")

                message = ""

                def toolcache_handoff() -> None:
                    if interrupt_after_toolcache:
                        raise TerminationRequest(signal.SIGTERM)

                try:
                    create_docker_boundary(
                        replace(
                            selftest_boundary,
                            network_id=None,
                            gateway=None,
                            toolcache_owned=False,
                        ),
                        use_sudo=False,
                        cwd=first.invocation,
                        env={},
                        docker_command=post_accept_network_failure,
                        after_toolcache=toolcache_handoff,
                    )
                except Refusal as exc:
                    message = str(exc)
                except KeyboardInterrupt:
                    message = "KeyboardInterrupt"
                except TerminationRequest as exc:
                    message = signal.Signals(exc.signum).name
                return state, calls, message

            setup_state, setup_calls, setup_message = run_network_setup_control(
                network_rm_fails=False
            )
            check(
                "a post-accept network-create timeout reconciles both resources",
                bool(setup_message)
                and not setup_state["network"]
                and not setup_state["volume"]
                and ("network", "rm", str(selftest_boundary.network_id))
                in setup_calls,
            )
            failed_state, _failed_calls, failed_message = run_network_setup_control(
                network_rm_fails=True
            )
            check(
                "network rollback failure is surfaced while cache cleanup continues",
                "setup rollback failed" in failed_message
                and failed_state["network"]
                and not failed_state["volume"],
            )
            interrupt_state, _interrupt_calls, interrupt_message = (
                run_network_setup_control(
                    network_rm_fails=False, interrupt_create=True
                )
            )
            check(
                "a post-accept KeyboardInterrupt reconciles both resources",
                interrupt_message == "KeyboardInterrupt"
                and not interrupt_state["network"]
                and not interrupt_state["volume"],
            )
            handoff_state, handoff_calls, handoff_message = (
                run_network_setup_control(
                    network_rm_fails=False,
                    interrupt_after_toolcache=True,
                )
            )
            check(
                "a signal after cache return but before network create is reconciled",
                handoff_message == "SIGTERM"
                and not handoff_state["network"]
                and not handoff_state["volume"]
                and not any(call[:2] == ("network", "create") for call in handoff_calls),
            )
            delayed_clock = [0.0]
            delayed_state = {"volume": False, "network": False, "released": False}
            delayed_calls: list[tuple[str, ...]] = []

            def delayed_daemon_completion(
                arguments: Sequence[str], **_kwargs: object
            ) -> subprocess.CompletedProcess[str]:
                call = tuple(arguments)
                delayed_calls.append(call)
                if call == ("volume", "inspect", ACT_TOOLCACHE_VOLUME):
                    if delayed_state["volume"]:
                        return docker_completed(arguments, stdout=volume_metadata)
                    return docker_completed(arguments, 1, stderr=missing_volume)
                if call == ("volume", "rm", ACT_TOOLCACHE_VOLUME):
                    delayed_state["volume"] = False
                    return docker_completed(arguments)
                if call == ("network", "inspect", selftest_boundary.name):
                    if delayed_state["network"]:
                        return docker_completed(arguments, stdout=network_metadata)
                    return docker_completed(arguments, 1, stderr=missing_network_name)
                if call == (
                    "network",
                    "rm",
                    str(selftest_boundary.network_id),
                ):
                    delayed_state["network"] = False
                    return docker_completed(arguments)
                raise AssertionError(f"unexpected delayed mutation call: {call}")

            def advance_delayed_daemon(duration: float) -> None:
                delayed_clock[0] += duration
                if not delayed_state["released"]:
                    delayed_state["released"] = True
                    delayed_state["volume"] = True
                    delayed_state["network"] = True

            discard_act_toolcache_if_owned(
                selftest_boundary,
                use_sudo=False,
                cwd=first.invocation,
                env={},
                docker_command=delayed_daemon_completion,
                stability_window=0.1,
                monotonic=lambda: delayed_clock[0],
                sleep=advance_delayed_daemon,
            )
            discard_docker_network_if_owned(
                selftest_boundary,
                use_sudo=False,
                cwd=first.invocation,
                env={},
                docker_command=delayed_daemon_completion,
                stability_window=0.1,
                monotonic=lambda: delayed_clock[0],
                sleep=advance_delayed_daemon,
            )
            check(
                "stable rollback catches delayed Docker daemon mutations",
                not delayed_state["volume"]
                and not delayed_state["network"]
                and ("volume", "rm", ACT_TOOLCACHE_VOLUME) in delayed_calls
                and (
                    "network",
                    "rm",
                    str(selftest_boundary.network_id),
                )
                in delayed_calls,
            )
            check(
                "two heads receive different writable action/workflow caches",
                first.action_cache != second.action_cache
                and first.cache_server != second.cache_server
                and first.checkout != second.checkout,
            )
            (first.cache_server / "poison").write_text("head A\n", encoding="utf-8")
            check(
                "a cache entry written by head A is absent from head B",
                not (second.cache_server / "poison").exists(),
            )
            controlled = controlled_act_environment(first)
            check(
                "controlled act environment drops tokens, agents, and runtime secrets",
                not {
                    "GH_TOKEN",
                    "GITHUB_TOKEN",
                    "SSH_AUTH_SOCK",
                    "ACTIONS_RUNTIME_TOKEN",
                }.intersection(controlled),
            )
            previous_context = os.environ.get("DOCKER_CONTEXT")
            os.environ["DOCKER_CONTEXT"] = "attacker-current-context"
            try:
                hostile_context = controlled_act_environment(first)
            finally:
                if previous_context is None:
                    os.environ.pop("DOCKER_CONTEXT", None)
                else:
                    os.environ["DOCKER_CONTEXT"] = previous_context
            check(
                "a fake ambient Docker current context is excluded",
                not {"DOCKER_CONTEXT", "DOCKER_CONFIG", "DOCKER_HOST"}.intersection(
                    hostile_context
                ),
            )
            sudo_docker = docker_prefix(True, hostile_context)
            sudo_act = act_prefix("/audited/act", True, hostile_context)
            check(
                "sudo Docker and act share the same explicit isolated environment",
                sudo_docker[:-1] == sudo_act[:-1]
                and sudo_docker[-1] == require_tool("docker")
                and sudo_act[-1] == "/audited/act"
                and "-i" in sudo_docker
                and f"HOME={first.home}" in sudo_docker,
            )
            privileged_signal_calls: list[tuple[str, ...]] = []

            def fake_privileged_signal(
                command: Sequence[str], **_kwargs: object
            ) -> subprocess.CompletedProcess[str]:
                privileged_signal_calls.append(tuple(command))
                return docker_completed(command)

            def forbidden_unprivileged_signal(_group: int, _signal: int) -> None:
                raise AssertionError("unprivileged killpg used for a sudo act group")

            signal_process_group(
                987654321,
                signal.SIGSTOP,
                use_sudo=True,
                run_command=fake_privileged_signal,
                kill_group=forbidden_unprivileged_signal,
            )
            check(
                "sudo act groups are privileged-signalled from the first signal",
                len(privileged_signal_calls) == 1
                and "-STOP" in privileged_signal_calls[0]
                and "-987654321" in privileged_signal_calls[0],
            )

            def fake_missing_group(
                command: Sequence[str], **_kwargs: object
            ) -> subprocess.CompletedProcess[str]:
                privileged_signal_calls.append(tuple(command))
                return docker_completed(
                    command, 1, stderr="kill: (-987654321): No such process"
                )

            check(
                "sudo process-group absence uses privileged kill zero",
                not process_group_exists(
                    987654321,
                    use_sudo=True,
                    run_command=fake_missing_group,
                    kill_group=forbidden_unprivileged_signal,
                )
                and "-0" in privileged_signal_calls[-1],
            )
            containment_trace: list[str] = []
            containment_states: Iterator[bool | Refusal] = iter(
                (
                    Refusal("injected initial inspection failure"),
                    Refusal("injected recovery inspection failure"),
                    True,
                    False,
                )
            )
            containment_signal_count = 0

            class ContainmentProcess:
                pid = 987654319

                def poll(self) -> None:
                    containment_trace.append("poll")

                def wait(self, timeout: float) -> int:
                    containment_trace.append(f"reaped-{timeout}")
                    return 0

            def uncertain_group_exists(
                _group: int, *, use_sudo: bool
            ) -> bool:
                del use_sudo
                state = next(containment_states)
                if isinstance(state, Refusal):
                    containment_trace.append("absence-unknown")
                    raise state
                containment_trace.append("group-live" if state else "group-absent")
                return state

            def recovering_group_signal(
                _group: int, _signal: int, *, use_sudo: bool
            ) -> None:
                nonlocal containment_signal_count
                del use_sudo
                containment_signal_count += 1
                containment_trace.append(f"kill-{containment_signal_count}")
                if containment_signal_count < 3:
                    raise Refusal("injected privileged kill failure")

            containment_notices: list[str] = []

            def broken_containment_notifier(message: str) -> None:
                containment_notices.append(message)
                raise BrokenPipeError("injected closed stderr")

            terminate_act_process_group(
                ContainmentProcess(),  # type: ignore[arg-type]
                use_sudo=True,
                primary=TerminationRequest(signal.SIGTERM),
                group_exists=uncertain_group_exists,
                signal_group=recovering_group_signal,
                escalation=((signal.SIGKILL, 0),),
                sleep=lambda _duration: containment_trace.append("held"),
                recovery_notice=broken_containment_notifier,
            )
            containment_trace.append("docker-teardown")
            check(
                "Docker teardown waits through kill/inspection failure for PGID absence",
                containment_trace[-2:] == ["reaped-1", "docker-teardown"]
                and containment_trace.index("group-absent")
                < containment_trace.index("docker-teardown")
                and containment_trace.count("absence-unknown") == 2
                and containment_signal_count == 3
                and len(containment_notices) == 1
                and "Docker teardown is paused" in containment_notices[0],
            )
            latched_interrupt = False
            with cleanup_termination_signals():
                interrupt_handler = signal.getsignal(signal.SIGINT)
                if callable(interrupt_handler):
                    try:
                        interrupt_handler(signal.SIGINT, None)
                    except TerminationRequest as exc:
                        latched_interrupt = (
                            exc.signum == signal.SIGINT
                            and all(
                                signal.getsignal(item) == signal.SIG_IGN
                                for item in (
                                    signal.SIGINT,
                                    signal.SIGTERM,
                                    signal.SIGHUP,
                                )
                            )
                        )
            check(
                "the first handled signal defers repeats until cleanup completes",
                latched_interrupt,
            )
            deferred_interrupt = False
            with cleanup_termination_signals():
                try:
                    with blocked_cleanup_signals():
                        signal.raise_signal(signal.SIGINT)
                        deferred_interrupt = signal.SIGINT in signal.sigpending()
                except TerminationRequest as exc:
                    deferred_interrupt = (
                        deferred_interrupt and exc.signum == signal.SIGINT
                    )
            check(
                "a first signal during cleanup is delivered only afterward",
                deferred_interrupt,
            )
            worker_trace: list[str] = []
            worker_ready = threading.Event()
            worker_stop = threading.Event()
            worker_threads: list[threading.Thread] = []

            def signal_safe_worker() -> None:
                worker_ready.set()
                worker_stop.wait(2)

            def cleanup_with_live_worker() -> int:
                worker = threading.Thread(
                    target=signal_safe_worker,
                    name="act-ci-signal-mask-selftest",
                    daemon=True,
                )
                worker_threads.append(worker)
                start_cleanup_safe_thread(worker)
                if not worker_ready.wait(1):
                    raise Refusal("signal-mask self-test worker did not start")
                try:
                    with blocked_cleanup_signals():
                        worker_trace.append("cleanup-start")
                        os.kill(os.getpid(), signal.SIGTERM)
                        time.sleep(0.02)
                        worker_trace.append("cleanup-finished")
                finally:
                    worker_stop.set()
                    worker.join(timeout=1)
                return RC_OK

            worker_signal_rc = run_with_cleanup_signals(cleanup_with_live_worker)
            check(
                "worker threads cannot intercept a signal before cleanup finishes",
                worker_signal_rc == 128 + signal.SIGTERM
                and worker_trace == ["cleanup-start", "cleanup-finished"]
                and len(worker_threads) == 1
                and not worker_threads[0].is_alive(),
            )
            join_cancel = threading.Event()
            join_complete = threading.Event()
            join_lock = threading.Lock()
            join_trace: list[str] = []
            join_workers: list[threading.Thread] = []
            join_problems: list[str] = []

            def signal_during_monitor_join() -> None:
                try:
                    join_cancel.wait(1)
                    join_trace.append("signal-sent")
                    os.kill(os.getpid(), signal.SIGHUP)
                    time.sleep(0.02)
                    join_trace.append("worker-finished")
                finally:
                    join_complete.set()

            def join_signal_action() -> int:
                worker = threading.Thread(
                    target=signal_during_monitor_join,
                    name="act-ci-monitor-join-selftest",
                    daemon=True,
                )
                join_workers.append(worker)
                start_cleanup_safe_thread(worker)
                cancel_and_join_cleanup_threads(
                    join_cancel,
                    join_lock,
                    [(worker, join_complete)],
                    join_problems,
                    timeout=1,
                )
                return RC_OK

            join_signal_rc = run_with_cleanup_signals(join_signal_action)
            check(
                "a first signal during monitor join waits for proven termination",
                join_signal_rc == 128 + signal.SIGHUP
                and join_trace == ["signal-sent", "worker-finished"]
                and join_complete.is_set()
                and len(join_workers) == 1
                and not join_workers[0].is_alive()
                and not join_problems,
            )
            never_started = threading.Thread(
                target=lambda: None,
                name="act-ci-never-started-selftest",
                daemon=True,
            )

            def injected_thread_start_failure() -> None:
                raise RuntimeError("injected thread start failure")

            never_started.start = injected_thread_start_failure  # type: ignore[method-assign]
            refused(
                "monitor start failure becomes a cleanup refusal",
                lambda: start_cleanup_thread_or_refuse(
                    never_started, "interrupt monitor"
                ),
            )
            never_started_problems: list[str] = []
            refused(
                "registered monitor start failure is a cleanup refusal",
                lambda: cancel_and_join_cleanup_threads(
                    threading.Event(),
                    threading.Lock(),
                    [(never_started, threading.Event())],
                    never_started_problems,
                    timeout=0.01,
                ),
            )
            check(
                "registered monitor start failure is reported without an invalid join",
                never_started.ident is None
                and never_started_problems
                == ["interrupt monitor was registered but never started"],
            )
            worker_cli_results: list[tuple[str, float]] = []

            def timed_worker_cli() -> None:
                started_at = time.monotonic()
                try:
                    run_tracked_process_group_command(
                        [
                            sys.executable,
                            "-I",
                            "-c",
                            "import time; time.sleep(30)",
                        ],
                        cwd=pathlib.Path.cwd(),
                        env={
                            "PATH": SAFE_PATH,
                            "LANG": "C.UTF-8",
                            "LC_ALL": "C.UTF-8",
                        },
                        timeout=0.05,
                        use_sudo=False,
                    )
                except subprocess.TimeoutExpired:
                    worker_cli_results.append(
                        ("contained", time.monotonic() - started_at)
                    )

            worker_cli_thread = threading.Thread(
                target=timed_worker_cli,
                name="act-ci-worker-cli-selftest",
                daemon=True,
            )
            start_cleanup_safe_thread(worker_cli_thread)
            worker_cli_thread.join(timeout=3)
            check(
                "a worker-thread CLI timeout kills its blocked-mask process group",
                not worker_cli_thread.is_alive()
                and len(worker_cli_results) == 1
                and worker_cli_results[0][0] == "contained"
                and worker_cli_results[0][1] < 2,
            )
            check(
                "act configuration roots and invocation directory are per-run",
                controlled["HOME"] == str(first.home)
                and controlled["XDG_CONFIG_HOME"] == str(first.xdg_config)
                and first.invocation.parent == first.root,
            )
            for hostile_path in (
                first.xdg_config / "act" / "actrc",
                first.home / ".actrc",
                first.invocation / ".actrc",
                first.invocation / ".env",
                first.invocation / ".secrets",
                first.invocation / ".vars",
                first.invocation / ".input",
            ):
                hostile_path.parent.mkdir(parents=True, exist_ok=True)
                hostile_path.write_text("--privileged\n", encoding="utf-8")
                refused(
                    f"hostile private input {hostile_path.name} is refused",
                    lambda: validate_isolation_layout(first),
                )
                hostile_path.unlink()
            first.secret_file.write_text("GITHUB_TOKEN=operator\n", encoding="utf-8")
            refused(
                "a nonempty explicit secret file is refused",
                lambda: validate_isolation_layout(first),
            )
            first.secret_file.write_text("", encoding="utf-8")
            validate_isolation_layout(first)

    owned_id = "c" * 64
    child_id = "d" * 64
    unrelated_id = "e" * 64
    inventory = [
        {
            "Id": owned_id,
            "Name": "/owned",
            "Config": {"Labels": {DOCKER_OWNER_LABEL: selftest_boundary.token}},
            "HostConfig": {"NetworkMode": selftest_boundary.name},
            "NetworkSettings": {"Networks": {}},
            "State": {"Running": False},
            "Mounts": [
                {
                    "Type": "volume",
                    "Name": ACT_TOOLCACHE_VOLUME,
                    "Destination": ACT_TOOLCACHE_TARGET,
                    "RW": True,
                }
            ],
        },
        {
            "Id": child_id,
            "Name": "/child",
            "Config": {"Labels": {}},
            "HostConfig": {"NetworkMode": f"container:{owned_id[:12]}"},
            "NetworkSettings": {"Networks": {}},
            "State": {"Running": True},
        },
        {
            "Id": unrelated_id,
            "Name": "/unrelated",
            "Config": {"Labels": {DOCKER_OWNER_LABEL: "f" * 32}},
            "HostConfig": {"NetworkMode": "bridge"},
            "NetworkSettings": {"Networks": {"bridge": {}}},
            "State": {"Running": True},
        },
    ]
    selected = owned_container_ids(inventory, selftest_boundary)
    check(
        "stopped boundary and container-network children are owned exactly",
        selected == {owned_id, child_id},
    )
    check(
        "unrelated containers are excluded from cleanup",
        unrelated_id not in selected
        and running_container_ids(inventory, selected) == [child_id],
    )
    check(
        "the live-container inspector verifies the effective tool-cache mount",
        verify_runner_toolcache_mounts(
            inventory, selftest_boundary, require_any=True
        )
        == 1,
    )
    delayed_inventory_cancel = threading.Event()
    delayed_inspect_entered = threading.Event()
    delayed_inspect_release = threading.Event()
    delayed_inventory_result: list[list[dict[str, object]]] = []
    delayed_inventory_errors: list[BaseException] = []

    def delayed_last_inspect(
        arguments: Sequence[str], **_kwargs: object
    ) -> subprocess.CompletedProcess[str]:
        call = tuple(arguments)
        if call[0:2] == ("container", "ls"):
            return docker_completed(arguments, stdout=f"{owned_id}\n")
        if call == ("container", "inspect", owned_id):
            delayed_inspect_entered.set()
            if not delayed_inspect_release.wait(1):
                raise AssertionError("delayed inventory self-test was not released")
            return docker_completed(arguments, stdout=json.dumps([inventory[0]]))
        raise AssertionError(f"unexpected delayed inventory call: {call}")

    def collect_delayed_inventory() -> None:
        try:
            delayed_inventory_result.append(
                docker_container_inventory(
                    use_sudo=False,
                    cwd=pathlib.Path.cwd(),
                    env={},
                    docker_command=delayed_last_inspect,
                    cancel=delayed_inventory_cancel,
                )
            )
        except BaseException as exc:
            delayed_inventory_errors.append(exc)

    delayed_inventory_thread = threading.Thread(
        target=collect_delayed_inventory,
        name="act-ci-delayed-inventory-selftest",
        daemon=True,
    )
    start_cleanup_safe_thread(delayed_inventory_thread)
    delayed_inspect_started = delayed_inspect_entered.wait(1)
    delayed_inventory_cancel.set()
    delayed_inspect_release.set()
    delayed_inventory_thread.join(timeout=1)
    check(
        "cancellation during the final container inspect stops the monitor inventory",
        delayed_inspect_started
        and not delayed_inventory_thread.is_alive()
        and not delayed_inventory_errors
        and delayed_inventory_result == [[]],
    )
    invalid_mount_inventory = [
        {
            **inventory[0],
            "Mounts": [
                {
                    "Type": "volume",
                    "Name": "shared-elsewhere",
                    "Destination": ACT_TOOLCACHE_TARGET,
                    "RW": True,
                }
            ],
        }
    ]
    refused(
        "an owned container on a different tool-cache volume is refused",
        lambda: verify_runner_toolcache_mounts(
            invalid_mount_inventory, selftest_boundary, require_any=True
        ),
    )

    check(
        "act version parser accepts the tested version",
        parse_act_version("act version 0.2.89") == SUPPORTED_ACT_VERSION,
    )
    require_supported_act_version(SUPPORTED_ACT_VERSION)
    check("the audited act version is accepted", True)
    refused(
        "an unaudited newer act version is refused",
        lambda: require_supported_act_version((0, 2, 90)),
    )
    refused(
        "unparseable act version is refused",
        lambda: parse_act_version("act unknown"),
    )

    def successful_process(*_args, **_kwargs):  # type: ignore[no-untyped-def]
        return subprocess.CompletedProcess([], 0)

    spawn_handoff_trace: list[str] = []

    class SpawnHandoffProcess:
        pid = 987654320

    def signal_before_popen_return(
        *_args: object, **_kwargs: object
    ) -> subprocess.Popen[object]:
        spawn_handoff_trace.append("spawned")
        os.kill(os.getpid(), signal.SIGTERM)
        spawn_handoff_trace.append("constructor-returned")
        return SpawnHandoffProcess()  # type: ignore[return-value]

    def record_spawn_termination(
        process: subprocess.Popen[object],
        *,
        use_sudo: bool,
        primary: BaseException,
    ) -> None:
        del use_sudo, primary
        spawn_handoff_trace.append(f"terminated-{process.pid}")

    def repeat_signal_at_spawn_cleanup_entry() -> None:
        spawn_handoff_trace.append("cleanup-entered")
        os.kill(os.getpid(), signal.SIGHUP)
        spawn_handoff_trace.append("repeat-ignored")

    spawn_handoff_rc = run_with_cleanup_signals(
        lambda: run_act_process(
            ["act"],
            cwd=pathlib.Path.cwd(),
            env={},
            popen=signal_before_popen_return,
            terminate_group=record_spawn_termination,
            before_terminate_group=repeat_signal_at_spawn_cleanup_entry,
        ).returncode
    )
    check(
        "a signal after spawn but before Popen return terminates the stored group",
        spawn_handoff_rc == 128 + signal.SIGTERM
        and spawn_handoff_trace
        == [
            "spawned",
            "constructor-returned",
            "cleanup-entered",
            "repeat-ignored",
            "terminated-987654320",
        ],
    )
    nested_cleanup_trace: list[str] = []

    class NestedCleanupProcess:
        pid = 987654317
        returncode = 0

        def communicate(self, timeout: float) -> tuple[str, str]:
            del timeout
            nested_cleanup_trace.append("cleanup-command-finished")
            return "", ""

    def repeat_during_cleanup_popen(
        *_args: object, **_kwargs: object
    ) -> subprocess.Popen[str]:
        nested_cleanup_trace.append("cleanup-command-spawned")
        os.kill(os.getpid(), signal.SIGHUP)
        nested_cleanup_trace.append("repeat-ignored")
        return NestedCleanupProcess()  # type: ignore[return-value]

    def tracked_cleanup_after_first_signal() -> int:
        try:
            os.kill(os.getpid(), signal.SIGTERM)
        finally:
            nested_cleanup_trace.append("cleanup-entered")
            run_tracked_process_group_command(
                ["docker", "network", "rm"],
                cwd=pathlib.Path.cwd(),
                env={},
                timeout=1,
                use_sudo=False,
                popen=repeat_during_cleanup_popen,
            )
            nested_cleanup_trace.append("cleanup-tail-finished")
        return RC_OK

    nested_cleanup_rc = run_with_cleanup_signals(
        tracked_cleanup_after_first_signal
    )
    check(
        "a repeat signal inside a tracked cleanup command cannot abort the tail",
        nested_cleanup_rc == 128 + signal.SIGTERM
        and nested_cleanup_trace
        == [
            "cleanup-entered",
            "cleanup-command-spawned",
            "repeat-ignored",
            "cleanup-command-finished",
            "cleanup-tail-finished",
        ],
    )
    docker_timeout_trace: list[str] = []

    class DockerTimeoutProcess:
        pid = 987654318
        returncode = -signal.SIGKILL
        communicate_calls = 0

        def communicate(self, timeout: float) -> tuple[str, str]:
            self.communicate_calls += 1
            docker_timeout_trace.append(f"communicate-{self.communicate_calls}")
            if self.communicate_calls == 1:
                raise subprocess.TimeoutExpired(["docker"], timeout)
            return "", ""

    def spawn_timeout_command(
        *_args: object, **_kwargs: object
    ) -> subprocess.Popen[str]:
        docker_timeout_trace.append("spawned")
        return DockerTimeoutProcess()  # type: ignore[return-value]

    def contain_timeout_command(
        process: subprocess.Popen[object],
        *,
        use_sudo: bool,
        primary: BaseException,
    ) -> None:
        del use_sudo, primary
        docker_timeout_trace.append(f"group-absent-{process.pid}")

    docker_timeout_caught = False
    try:
        run_tracked_process_group_command(
            ["docker", "volume", "create"],
            cwd=pathlib.Path.cwd(),
            env={},
            timeout=0.01,
            use_sudo=True,
            popen=spawn_timeout_command,
            terminate_group=contain_timeout_command,
        )
    except subprocess.TimeoutExpired:
        docker_timeout_caught = True
        docker_timeout_trace.append("rollback-entry")
    check(
        "a timed-out sudo Docker CLI is contained before rollback begins",
        docker_timeout_caught
        and docker_timeout_trace
        == [
            "spawned",
            "communicate-1",
            "group-absent-987654318",
            "communicate-2",
            "rollback-entry",
        ],
    )
    child_environment = {
        "PATH": SAFE_PATH,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
    }
    with deferred_cleanup_signal_delivery():
        child_mask_probe = subprocess.run(
            [
                sys.executable,
                "-I",
                "-c",
                (
                    "import signal; "
                    "print(sorted(int(item) for item in "
                    "signal.pthread_sigmask(signal.SIG_BLOCK, set())))"
                ),
            ],
            env=child_environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,
            check=False,
        )
    with deferred_cleanup_signal_delivery():
        term_probe = subprocess.Popen(
            [sys.executable, "-I", "-c", "import time; time.sleep(30)"],
            env=child_environment,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
    os.kill(term_probe.pid, signal.SIGTERM)
    try:
        term_probe_status = term_probe.wait(timeout=5)
    except subprocess.TimeoutExpired:
        term_probe.kill()
        term_probe.wait(timeout=5)
        term_probe_status = 0
    try:
        inherited_mask = {
            int(item) for item in json.loads(child_mask_probe.stdout or "[]")
        }
    except (json.JSONDecodeError, TypeError, ValueError):
        inherited_mask = set(CLEANUP_SIGNALS)
    check(
        "spawned children inherit no cleanup-signal mask and honor SIGTERM",
        child_mask_probe.returncode == 0
        and inherited_mask.isdisjoint(CLEANUP_SIGNALS)
        and term_probe_status == -signal.SIGTERM,
    )

    @contextlib.contextmanager
    def selftest_child_subreaper() -> Iterator[None]:
        """Give orphaned probe zombies a reaper even under act's bare PID 1."""
        if not sys.platform.startswith("linux"):
            yield
            return
        libc = ctypes.CDLL(None, use_errno=True)
        try:
            prctl = libc.prctl
        except AttributeError as exc:
            raise Refusal("self-test cannot configure a child subreaper") from exc
        current = ctypes.c_int()
        if prctl(37, ctypes.byref(current), 0, 0, 0) != 0:
            error = ctypes.get_errno()
            raise Refusal(
                f"self-test cannot inspect child subreaper state: errno {error}"
            )
        if prctl(36, 1, 0, 0, 0) != 0:
            error = ctypes.get_errno()
            raise Refusal(
                f"self-test cannot enable child subreaper: errno {error}"
            )
        try:
            yield
        finally:
            if prctl(36, current.value, 0, 0, 0) != 0:
                error = ctypes.get_errno()
                raise Refusal(
                    f"self-test cannot restore child subreaper: errno {error}"
                )

    def reap_adopted_process_group(process_group: int) -> None:
        """Reap only orphaned probe descendants adopted from one command PGID."""
        if process_group <= 1:
            return
        while True:
            try:
                waited, _raw_status = os.waitpid(-process_group, os.WNOHANG)
            except ChildProcessError:
                return
            if waited == 0:
                return

    def process_directed_signal_probe_under_reaper(
        action: Callable[[], int],
        *,
        ready_path: pathlib.Path,
        sent_signal: int,
    ) -> bool:
        """Signal a runner and prove its recorded command PGID is gone."""
        try:
            ready_path.unlink()
        except FileNotFoundError:
            pass
        runner_pid = os.fork()
        if runner_pid == 0:
            try:
                exit_status = action()
            except BaseException:
                exit_status = 99
            os._exit(exit_status)

        recorded: tuple[int, int, int] | None = None
        ready_deadline = time.monotonic() + 10
        while time.monotonic() < ready_deadline:
            try:
                fields = tuple(
                    int(item) for item in ready_path.read_text().split()
                )
            except (FileNotFoundError, OSError, UnicodeError, ValueError):
                fields = ()
            if len(fields) == 3 and all(item > 1 for item in fields):
                recorded = (fields[0], fields[1], fields[2])
                break
            time.sleep(0.05)

        if recorded is not None:
            os.kill(runner_pid, sent_signal)
        else:
            os.kill(runner_pid, signal.SIGKILL)

        process_group = recorded[2] if recorded is not None else -1
        runner_status: int | None = None
        # The production boundary may consume its complete 10 s INT, 10 s TERM,
        # and 5 s KILL escalation before it can report containment.
        exit_deadline = time.monotonic() + 35
        while time.monotonic() < exit_deadline:
            reap_adopted_process_group(process_group)
            waited, raw_status = os.waitpid(runner_pid, os.WNOHANG)
            if waited == runner_pid:
                runner_status = os.waitstatus_to_exitcode(raw_status)
                break
            time.sleep(0.05)
        if runner_status is None:
            try:
                os.kill(runner_pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            _waited, raw_status = os.waitpid(runner_pid, 0)
            runner_status = os.waitstatus_to_exitcode(raw_status)

        group_absent = False
        if process_group > 1 and process_group != os.getpgrp():
            absence_deadline = time.monotonic() + 3
            while time.monotonic() < absence_deadline:
                reap_adopted_process_group(process_group)
                try:
                    if not process_group_exists(process_group, use_sudo=False):
                        group_absent = True
                        break
                except Refusal:
                    pass
                time.sleep(0.05)
            if not group_absent:
                try:
                    # Test cleanup first gives a cooperative leader a chance to
                    # reap its child. This keeps a deliberately failed mutation
                    # from stranding an unkillable zombie under a non-reaping
                    # container PID 1.
                    os.killpg(process_group, signal.SIGTERM)
                except ProcessLookupError:
                    pass
                cleanup_deadline = time.monotonic() + 3
                while time.monotonic() < cleanup_deadline:
                    reap_adopted_process_group(process_group)
                    try:
                        if not process_group_exists(
                            process_group, use_sudo=False
                        ):
                            break
                    except Refusal:
                        pass
                    time.sleep(0.05)
                try:
                    if process_group_exists(process_group, use_sudo=False):
                        os.killpg(process_group, signal.SIGKILL)
                except (ProcessLookupError, Refusal):
                    pass
                cleanup_deadline = time.monotonic() + 3
                while time.monotonic() < cleanup_deadline:
                    reap_adopted_process_group(process_group)
                    try:
                        if not process_group_exists(
                            process_group, use_sudo=False
                        ):
                            break
                    except Refusal:
                        pass
                    time.sleep(0.05)

        passed = (
            recorded is not None
            and recorded[0] != recorded[1]
            and runner_status == 128 + sent_signal
            and group_absent
        )
        if not passed:
            print(
                "process-directed signal probe detail: "
                f"signal={signal.Signals(sent_signal).name} "
                f"runner={runner_pid} recorded={recorded!r} "
                f"runner_status={runner_status!r} group_absent={group_absent} "
                f"parent_pgrp={os.getpgrp()}",
                file=sys.stderr,
            )
        return passed

    def process_directed_signal_probe(
        action: Callable[[], int],
        *,
        ready_path: pathlib.Path,
        sent_signal: int,
    ) -> bool:
        with selftest_child_subreaper():
            return process_directed_signal_probe_under_reaper(
                action,
                ready_path=ready_path,
                sent_signal=sent_signal,
            )

    def process_directed_capture_probe(
        command: Sequence[str],
        *,
        cwd: pathlib.Path,
        env: Mapping[str, str],
        ready_path: pathlib.Path,
        sent_signal: int,
    ) -> bool:
        def run_probe_command() -> int:
            capture(
                command,
                cwd=cwd,
                env=env,
                description="process-directed capture self-test",
            )
            return RC_FAILED

        return process_directed_signal_probe(
            lambda: run_with_cleanup_signals(run_probe_command),
            ready_path=ready_path,
            sent_signal=sent_signal,
        )

    with tempfile.TemporaryDirectory(
        prefix="act-ci-capture-signal-selftest-"
    ) as raw_capture_probe:
        capture_probe_root = pathlib.Path(raw_capture_probe)
        cooperative_tree_program = (
            f"#!{sys.executable}\n"
            "import os, pathlib, signal, subprocess, sys\n"
            "child = subprocess.Popen([sys.executable, '-I', '-c', "
            "'import signal,time; signal.signal(signal.SIGINT, "
            "signal.SIG_DFL); time.sleep(300)'])\n"
            "def terminate(signum, _frame):\n"
            "    try:\n"
            "        child.terminate()\n"
            "    except ProcessLookupError:\n"
            "        pass\n"
            "    try:\n"
            "        child.wait(timeout=5)\n"
            "    except subprocess.TimeoutExpired:\n"
            "        child.kill()\n"
            "        child.wait(timeout=5)\n"
            "    raise SystemExit(128 + signum)\n"
            "for item in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):\n"
            "    signal.signal(item, terminate)\n"
            "pathlib.Path(os.environ['ACT_CI_PIDFILE']).write_text("
            "f'{os.getpid()} {child.pid} {os.getpgrp()}')\n"
            "while True:\n"
            "    signal.pause()\n"
        )
        tree_helper = capture_probe_root / "cooperative-tree.py"
        tree_helper.write_text(cooperative_tree_program, encoding="utf-8")
        tree_helper.chmod(0o755)
        for sent_signal in (signal.SIGTERM, signal.SIGHUP):
            tree_ready = capture_probe_root / f"tree-{sent_signal}.ready"
            check(
                f"process-directed {signal.Signals(sent_signal).name} "
                "contains a captured child tree",
                process_directed_capture_probe(
                    [sys.executable, "-I", str(tree_helper)],
                    cwd=capture_probe_root,
                    env={
                        **child_environment,
                        "ACT_CI_PIDFILE": str(tree_ready),
                    },
                    ready_path=tree_ready,
                    sent_signal=sent_signal,
                ),
            )

        entry_helper_root = capture_probe_root / "entry-bin"
        entry_helper_root.mkdir()
        fake_gh = entry_helper_root / "gh"
        fake_gh.write_text(cooperative_tree_program, encoding="utf-8")
        fake_gh.chmod(0o755)
        entry_ready = capture_probe_root / "entry.ready"
        original_safe_path = SAFE_PATH

        def run_main_entry_probe() -> int:
            global SAFE_PATH
            SAFE_PATH = f"{entry_helper_root}:{original_safe_path}"
            os.environ["ACT_CI_PIDFILE"] = str(entry_ready)
            return main([str(pathlib.Path(__file__)), "--pr", "1"])

        check(
            "production main contains an interrupted early repository lookup",
            process_directed_signal_probe(
                run_main_entry_probe,
                ready_path=entry_ready,
                sent_signal=signal.SIGTERM,
            ),
        )

        git_repo = capture_probe_root / "repo"
        git_repo.mkdir()
        git_env = git_environment(capture_probe_root)
        capture(
            [*git_prefix(), "init", "--quiet", str(git_repo)],
            cwd=capture_probe_root,
            env=git_env,
            description="Git interruption self-test repository creation",
        )
        capture(
            [
                *git_prefix(),
                "-C",
                str(git_repo),
                "remote",
                "add",
                "origin",
                "https://example.invalid/milan-act-ci-probe.git",
            ],
            cwd=capture_probe_root,
            env=git_env,
            description="Git interruption self-test remote creation",
        )
        helper_root = capture_probe_root / "git-exec"
        helper_root.mkdir()
        remote_helper = helper_root / "git-remote-https"
        remote_helper.write_text(cooperative_tree_program, encoding="utf-8")
        remote_helper.chmod(0o755)
        fetch_command = [
            *git_prefix(),
            "-C",
            str(git_repo),
            "fetch",
            "--force",
            "--no-tags",
            "origin",
        ]
        for sent_signal in (signal.SIGTERM,):
            git_ready = capture_probe_root / f"git-{sent_signal}.ready"
            probe_env = {
                **git_env,
                "GIT_EXEC_PATH": str(helper_root),
                "ACT_CI_PIDFILE": str(git_ready),
            }
            check(
                f"process-directed {signal.Signals(sent_signal).name} "
                "contains a Git remote-helper tree",
                process_directed_capture_probe(
                    fetch_command,
                    cwd=git_repo,
                    env=probe_env,
                    ready_path=git_ready,
                    sent_signal=sent_signal,
                ),
            )

    def execute_with_remote_change(changed: PullRequest) -> int:
        answers = iter((pr, changed))

        def moving_query(_number: int, _repository: str) -> PullRequest:
            return next(answers)

        return execute_act_boundary(
            ["act"],
            pr=pr,
            repository=repository,
            cwd=ROOT,
            env={},
            integrity_check=lambda: None,
            query=moving_query,
            run_process=successful_process,
        )

    for label, changed in (
        ("head SHA", replace(pr, head_sha="4" * 40)),
        ("state", replace(pr, state="CLOSED")),
        ("draft state", replace(pr, draft=True)),
        ("base ref", replace(pr, base_ref="main")),
    ):
        refused(
            f"remote {label} movement across an act process is refused",
            lambda changed=changed: execute_with_remote_change(changed),
        )

    check(
        "base-tip movement is noted without discarding exact-head evidence",
        execute_with_remote_change(replace(pr, base_sha="5" * 40)) == RC_OK,
    )

    acquisition_parent = pathlib.Path(tempfile.gettempdir()).resolve()
    interrupted_run_lease = RunDirectoryLease(acquisition_parent)

    def interrupt_after_run_create() -> None:
        raise TerminationRequest(signal.SIGTERM)

    interrupted_run_signal = 0
    try:
        make_run_directory(
            interrupted_run_lease,
            after_create=interrupt_after_run_create,
        )
    except TerminationRequest as exc:
        interrupted_run_signal = exc.signum
    check(
        "a signal after run-directory creation reconciles the accepted path",
        interrupted_run_signal == signal.SIGTERM
        and interrupted_run_lease.accepted
        and interrupted_run_lease.released
        and interrupted_run_lease.path is not None
        and not interrupted_run_lease.path.exists(),
    )

    failed_stat_lease = RunDirectoryLease(acquisition_parent)

    def failed_run_stat(_path: pathlib.Path) -> os.stat_result:
        raise OSError("injected post-create stat failure")

    refused(
        "a post-create run-directory stat failure is reconciled",
        lambda: make_run_directory(
            failed_stat_lease,
            inspect_path=failed_run_stat,
        ),
    )
    check(
        "the stat-failure path is absent after acquisition rollback",
        failed_stat_lease.accepted
        and failed_stat_lease.released
        and failed_stat_lease.path is not None
        and not failed_stat_lease.path.exists(),
    )

    cleanup = make_run_directory()

    def failed_chown(*_args, **_kwargs):  # type: ignore[no-untyped-def]
        return subprocess.CompletedProcess([], 1, "", "injected chown failure")

    refused(
        "sudo chown failure cannot report cleanup success",
        lambda: cleanup_run_directory(
            cleanup,
            True,
            run_command=failed_chown,
            sudo_binary="sudo",
        ),
    )
    shutil.rmtree(cleanup.path)

    cleanup = make_run_directory()

    def failed_chown_launch(*_args, **_kwargs):  # type: ignore[no-untyped-def]
        raise OSError("injected chown launch failure")

    refused(
        "sudo chown launch failure is a cleanup refusal",
        lambda: cleanup_run_directory(
            cleanup,
            True,
            run_command=failed_chown_launch,
            sudo_binary="sudo",
        ),
    )
    shutil.rmtree(cleanup.path)

    with tempfile.TemporaryDirectory(prefix="act-ci-install-selftest-") as raw_temp:
        install_root = pathlib.Path(raw_temp)
        installed = install_root / "trusted" / "act_ci.py"
        installed.parent.mkdir()
        installed.write_text("audited runner\n", encoding="utf-8")
        installed.chmod(0o555)
        digest = hashlib.sha256(installed.read_bytes()).hexdigest()
        validate_installed_runner_file(installed, digest, install_root / "candidate")
        check("content-pinned immutable runner installation is accepted", True)
        refused(
            "installed runner with the wrong content pin is refused",
            lambda: validate_installed_runner_file(
                installed, "0" * 64, install_root / "candidate"
            ),
        )
        refused(
            "runner installed inside the candidate worktree is refused",
            lambda: validate_installed_runner_file(installed, digest, install_root),
        )
        refused(
            "bootstrap install requires explicit repository and worktree",
            lambda: validate_bootstrap_options(digest, None, None),
        )
        validate_bootstrap_options(digest, repository, install_root / "candidate")
        check("bootstrap accepts both explicit identity arguments", True)

    cleanup = make_run_directory()

    def failed_remove(_path: pathlib.Path) -> None:
        raise OSError("injected removal failure")

    refused(
        "directory removal failure cannot report cleanup success",
        lambda: cleanup_run_directory(cleanup, False, remove_tree=failed_remove),
    )
    shutil.rmtree(cleanup.path)

    cleanup = make_run_directory()
    shutil.rmtree(cleanup.path)
    cleanup.path.symlink_to(cleanup.path / "missing-target")
    refused(
        "broken replacement symlink cannot masquerade as completed cleanup",
        lambda: cleanup_run_directory(cleanup, False),
    )
    cleanup.path.unlink()

    with tempfile.TemporaryDirectory(prefix="act-ci-git-selftest-") as raw_temp:
        repo = pathlib.Path(raw_temp) / "repo"
        repo.mkdir()
        git = require_tool("git")
        test_env = git_environment(pathlib.Path(raw_temp))

        def test_git(*arguments: str) -> str:
            return capture(
                [git, "-c", "core.hooksPath=/dev/null", "-C", str(repo), *arguments],
                cwd=repo,
                env=test_env,
                description="self-test git command",
            )

        test_git("init", "--quiet")
        test_git("config", "user.name", "act-ci selftest")
        test_git("config", "user.email", "act-ci@example.invalid")
        workflow_path = repo / WORKFLOWS["docs"]
        workflow_path.parent.mkdir(parents=True)
        workflow_text = (
            "name: docs\non: push\njobs:\n  docs:\n    runs-on: ubuntu-latest\n"
            "    steps:\n      - run: true\n"
        )
        workflow_path.write_text(workflow_text, encoding="utf-8")
        test_git("add", WORKFLOWS["docs"])
        test_git("commit", "--quiet", "-m", "base")
        first_commit = test_git("rev-parse", "HEAD")
        (repo / "README").write_text("second\n", encoding="utf-8")
        test_git("add", "README")
        test_git("commit", "--quiet", "-m", "head")
        test_head = test_git("rev-parse", "HEAD")
        test_pr = replace(pr, head_sha=test_head)

        for flag in ("assume-unchanged", "skip-worktree"):
            test_git("update-index", f"--{flag}", WORKFLOWS["docs"])
            workflow_path.write_text("candidate-hidden-edit\n", encoding="utf-8")
            refused(
                f"{flag} cannot hide selected workflow bytes",
                lambda: validate_checkout(
                    test_pr, repo, ("docs",), label="self-test checkout"
                ),
            )
            workflow_path.write_text(workflow_text, encoding="utf-8")
            test_git("update-index", f"--no-{flag}", WORKFLOWS["docs"])

        test_git("update-index", "--assume-unchanged", WORKFLOWS["docs"])
        workflow_path.unlink()
        workflow_path.symlink_to("/dev/zero")
        refused(
            "an index flag cannot hide a selected workflow symlink",
            lambda: validate_checkout(
                test_pr, repo, ("docs",), label="self-test checkout"
            ),
        )
        workflow_path.unlink()
        workflow_path.write_text(workflow_text, encoding="utf-8")
        test_git("update-index", "--no-assume-unchanged", WORKFLOWS["docs"])

        test_git("replace", test_head, first_commit)
        refused(
            "replacement object is refused even when HEAD text is unchanged",
            lambda: validate_checkout(
                test_pr, repo, ("docs",), label="self-test checkout"
            ),
        )
        test_git("replace", "-d", test_head)

        gitmodules_text = "".join(
            f'[submodule "{name}"]\n\tpath = {path}\n\turl = {url}\n'
            for name, path, url in TRUSTED_SUBMODULES
        )
        (repo / ".gitmodules").write_text(gitmodules_text, encoding="utf-8")
        test_git("add", ".gitmodules")
        gitlink_oid = "9" * 40
        trusted_gitlinks = tuple(path for _name, path, _url in TRUSTED_SUBMODULES)
        for gitlink in trusted_gitlinks:
            test_git(
                "update-index",
                "--add",
                "--cacheinfo",
                f"160000,{gitlink_oid},{gitlink}",
            )
        test_git("commit", "--quiet", "-m", "trusted submodule manifest")
        manifest_commit = test_git("rev-parse", "HEAD")
        validate_submodule_manifest(repo, manifest_commit, trusted_gitlinks)
        check("the exact trusted submodule manifest is accepted", True)

        hostile_manifest = gitmodules_text.replace(
            "https://github.com/alexforencich/verilog-axis",
            "https://127.0.0.1:9/attacker/verilog-axis",
        )
        (repo / ".gitmodules").write_text(hostile_manifest, encoding="utf-8")
        test_git("add", ".gitmodules")
        test_git("commit", "--quiet", "-m", "hostile submodule URL")
        hostile_commit = test_git("rev-parse", "HEAD")
        refused(
            "candidate submodule URL changes are refused before fetch",
            lambda: validate_submodule_manifest(
                repo, hostile_commit, trusted_gitlinks
            ),
        )

        hostile_update = gitmodules_text.replace(
            "\turl = https://github.com/alexforencich/verilog-axis\n",
            "\turl = https://github.com/alexforencich/verilog-axis\n"
            "\tupdate = !touch /tmp/act-ci-host-command\n",
        )
        (repo / ".gitmodules").write_text(hostile_update, encoding="utf-8")
        test_git("add", ".gitmodules")
        test_git("commit", "--quiet", "-m", "hostile submodule update")
        hostile_update_commit = test_git("rev-parse", "HEAD")
        refused(
            "candidate submodule update commands are refused before fetch",
            lambda: validate_submodule_manifest(
                repo, hostile_update_commit, trusted_gitlinks
            ),
        )
        refused(
            "candidate gitlink path changes are refused before fetch",
            lambda: validate_submodule_manifest(
                repo, manifest_commit, (*trusted_gitlinks[:-1], "unexpected")
            ),
        )
        prefix = git_prefix()
        check(
            "Git disables every protocol except credential-free HTTPS",
            "protocol.allow=never" in prefix
            and "protocol.https.allow=always" in prefix
            and not any("protocol.ssh.allow=always" == part for part in prefix),
        )

        unsafe_path = repo / "unsafe.yml"
        unsafe_path.write_text(
            "name: unsafe\non: push\njobs:\n  pwn:\n    runs-on: self-hosted\n"
            "    container:\n      image: alpine\n      options: --privileged\n",
            encoding="utf-8",
        )
        original_docs = WORKFLOWS["docs"]
        try:
            WORKFLOWS["docs"] = "unsafe.yml"
            refused(
                "self-hosted and candidate container authority is refused",
                lambda: validate_workflow_sandbox(repo, ("docs",)),
            )
        finally:
            WORKFLOWS["docs"] = original_docs

        docker_action_workflows = {
            "docker-url.yml": "docker://alpine:3.20",
            "remote-docker-action.yml": "example/docker-action@v1",
            "local-docker-action.yml": "./local-docker-action",
        }
        local_action = repo / "local-docker-action"
        local_action.mkdir()
        (local_action / "action.yml").write_text(
            "name: local docker action\nruns:\n  using: docker\n"
            "  image: Dockerfile\n",
            encoding="utf-8",
        )
        (local_action / "Dockerfile").write_text(
            "FROM alpine:3.20\n", encoding="utf-8"
        )
        try:
            for filename, action in docker_action_workflows.items():
                (repo / filename).write_text(
                    "name: docker-action-negative\non: push\njobs:\n"
                    "  unsafe:\n    runs-on: ubuntu-latest\n    steps:\n"
                    f"      - uses: {action}\n",
                    encoding="utf-8",
                )
                WORKFLOWS["docs"] = filename
                refused(
                    f"step-level action {action} is refused before act",
                    lambda: validate_workflow_sandbox(repo, ("docs",)),
                )
        finally:
            WORKFLOWS["docs"] = original_docs

        reader_root = repo / "workflow-reader"
        reader_root.mkdir()
        safe_workflow = reader_root / "safe.yml"
        safe_workflow.write_text(
            "name: safe\non: push\njobs:\n  safe:\n    runs-on: ubuntu-latest\n"
            "    steps:\n      - run: true\n",
            encoding="utf-8",
        )
        symlink_workflow = reader_root / "symlink.yml"
        symlink_workflow.symlink_to(safe_workflow)
        refused(
            "workflow reads do not follow a candidate symlink",
            lambda: load_workflow(reader_root, "symlink.yml"),
        )
        fifo_workflow = reader_root / "fifo.yml"
        os.mkfifo(fifo_workflow)
        refused(
            "workflow reads reject a FIFO without blocking",
            lambda: load_workflow(reader_root, "fifo.yml"),
        )
        refused(
            "workflow reads reject a host device before reading it",
            lambda: load_workflow(pathlib.Path("/"), "dev/null"),
        )
        oversized_workflow = reader_root / "oversized.yml"
        oversized_workflow.write_bytes(b"x" * (MAX_WORKFLOW_BYTES + 1))
        refused(
            "workflow reads reject an oversized regular file before parsing",
            lambda: load_workflow(reader_root, "oversized.yml"),
        )

    try:
        validate_workflow_sandbox(shipping_root, tuple(WORKFLOWS))
    except Refusal as exc:
        check(f"shipping workflows satisfy the sandbox policy ({exc})", False)
    else:
        check("shipping workflows satisfy the sandbox policy", True)

    print("selftest:", "PASS" if failures == 0 else f"{failures} FAILURE(S)")
    return RC_OK if failures == 0 else RC_FAILED


def interrupt_selftest(act_binary: str, use_sudo: bool) -> int:
    """Prove tool-cache separation, then interrupt act and verify cleanup."""
    probe_pr = PullRequest(
        number=1,
        state="OPEN",
        draft=False,
        base_ref=DEFAULT_BASE,
        base_sha="1" * 40,
        head_ref="interrupt-selftest",
        head_sha="2" * 40,
        head_repo="kebag-logic/milan-fpga",
        cross_repo=False,
        url="https://github.com/kebag-logic/milan-fpga/pull/1",
    )
    workflow = "interrupt-selftest"
    relative_workflow = ".github/workflows/interrupt-selftest.yml"
    seed_workflow = "toolcache-seed-selftest"
    seed_path = ".github/workflows/toolcache-seed-selftest.yml"
    probe_workflow = "toolcache-probe-selftest"
    probe_path = ".github/workflows/toolcache-probe-selftest.yml"
    marker = "milan-act-ci-cross-run-marker"
    with temporary_run_directory(use_sudo) as run_root:
        layout = make_layout(run_root, probe_pr)
        layout.checkout.mkdir(parents=True)
        workflow_sources = {
            relative_workflow: (
                "name: interrupt-selftest\n"
                "on: pull_request\n"
                "jobs:\n"
                "  sleep:\n"
                "    runs-on: ubuntu-latest\n"
                "    steps:\n"
                "      - run: sleep 300\n"
            ),
            seed_path: (
                "name: toolcache-seed-selftest\n"
                "on: pull_request\n"
                "jobs:\n"
                "  seed:\n"
                "    runs-on: ubuntu-latest\n"
                "    steps:\n"
                "      - shell: bash\n"
                "        run: |\n"
                "          set -euo pipefail\n"
                f'          test "$RUNNER_TOOL_CACHE" = "{ACT_TOOLCACHE_TARGET}"\n'
                f'          printf "head-a\\n" > "$RUNNER_TOOL_CACHE/{marker}"\n'
            ),
            probe_path: (
                "name: toolcache-probe-selftest\n"
                "on: pull_request\n"
                "jobs:\n"
                "  probe:\n"
                "    runs-on: ubuntu-latest\n"
                "    steps:\n"
                "      - shell: bash\n"
                "        run: |\n"
                "          set -euo pipefail\n"
                f'          test "$RUNNER_TOOL_CACHE" = "{ACT_TOOLCACHE_TARGET}"\n'
                f'          test ! -e "$RUNNER_TOOL_CACHE/{marker}"\n'
            ),
        }
        for path, contents in workflow_sources.items():
            workflow_path = layout.checkout / path
            workflow_path.parent.mkdir(parents=True, exist_ok=True)
            workflow_path.write_text(contents, encoding="utf-8")
        git = git_prefix()
        git_env = git_environment(layout.home)
        capture(
            [*git, "init", "--quiet", str(layout.checkout)],
            cwd=layout.root,
            env=git_env,
            description="interrupt self-test repository creation",
        )
        capture(
            [
                *git,
                "-C",
                str(layout.checkout),
                "add",
                *workflow_sources,
            ],
            cwd=layout.root,
            env=git_env,
            description="interrupt self-test workflow staging",
        )
        capture(
            [
                *git,
                "-C",
                str(layout.checkout),
                "-c",
                "user.name=act-ci selftest",
                "-c",
                "user.email=act-ci@example.invalid",
                "commit",
                "--quiet",
                "-m",
                "interrupt self-test",
            ],
            cwd=layout.root,
            env=git_env,
            description="interrupt self-test workflow commit",
        )
        layout.event_path.write_text(
            json.dumps({"action": "ready_for_review", "pull_request": {}}) + "\n",
            encoding="utf-8",
        )
        env = controlled_act_environment(layout)
        validate_isolation_layout(layout)
        prefix = require_runtime(act_binary, use_sudo, layout, env)

        cli_probe_token = secrets.token_hex(16)
        cli_probe_volume = f"milan-act-ci-cli-timeout-{cli_probe_token}"
        cli_probe_script = layout.temporary / "delayed-docker-cli.py"
        cli_probe_script.write_text(
            "import subprocess, sys, time\n"
            "time.sleep(2)\n"
            "raise SystemExit(subprocess.run(sys.argv[1:], check=False).returncode)\n",
            encoding="utf-8",
        )
        cli_probe_script.chmod(0o555)
        cli_probe_command = [
            *isolated_command_prefix(sys.executable, use_sudo, env),
            "-I",
            str(cli_probe_script),
            require_tool("docker"),
            "volume",
            "create",
            "--driver",
            "local",
            "--label",
            f"{DOCKER_OWNER_LABEL}={cli_probe_token}",
            cli_probe_volume,
        ]
        cli_probe_timed_out = False
        try:
            run_tracked_process_group_command(
                cli_probe_command,
                cwd=layout.invocation,
                env=env,
                timeout=0.2,
                use_sudo=use_sudo,
            )
        except subprocess.TimeoutExpired:
            cli_probe_timed_out = True
        time.sleep(2.2)
        cli_probe_inspect = run_docker(
            ["volume", "inspect", cli_probe_volume],
            use_sudo=use_sudo,
            cwd=layout.invocation,
            env=env,
            description="delayed Docker CLI containment probe",
            check=False,
        )
        if cli_probe_inspect.returncode == 0:
            try:
                cli_probe_metadata = json.loads(cli_probe_inspect.stdout)[0]
                cli_probe_labels = cli_probe_metadata["Labels"]
            except (json.JSONDecodeError, IndexError, KeyError, TypeError) as exc:
                raise Refusal(
                    "delayed Docker CLI probe left malformed volume metadata"
                ) from exc
            if (
                not isinstance(cli_probe_labels, dict)
                or cli_probe_labels.get(DOCKER_OWNER_LABEL) != cli_probe_token
            ):
                raise Refusal("delayed Docker CLI probe volume ownership changed")
            run_docker(
                ["volume", "rm", cli_probe_volume],
                use_sudo=use_sudo,
                cwd=layout.invocation,
                env=env,
                description="delayed Docker CLI probe cleanup",
            )
            cli_probe_absent = run_docker(
                ["volume", "inspect", cli_probe_volume],
                use_sudo=use_sudo,
                cwd=layout.invocation,
                env=env,
                description="delayed Docker CLI probe cleanup verification",
                check=False,
            )
            if (
                cli_probe_absent.returncode == 0
                or cli_probe_volume.lower()
                not in (cli_probe_absent.stderr or "").lower()
                or "no such volume"
                not in (cli_probe_absent.stderr or "").lower()
            ):
                raise Refusal("delayed Docker CLI probe volume survived cleanup")
            raise Refusal(
                "timed-out Docker CLI child survived and performed a delayed mutation"
            )
        missing_cli_probe = (cli_probe_inspect.stderr or "").lower()
        if (
            not cli_probe_timed_out
            or cli_probe_volume.lower() not in missing_cli_probe
            or "no such volume" not in missing_cli_probe
        ):
            raise Refusal("cannot verify delayed Docker CLI containment")

        try:
            WORKFLOWS[workflow] = relative_workflow
            WORKFLOWS[seed_workflow] = seed_path
            WORKFLOWS[probe_workflow] = probe_path

            def run_completed_live_probe(selected_workflow: str) -> None:
                with temporary_docker_boundary(
                    new_docker_boundary(),
                    use_sudo=use_sudo,
                    cwd=layout.invocation,
                    env=env,
                ) as probe_boundary:
                    probe_command = build_act_command(
                        prefix,
                        selected_workflow,
                        layout,
                        allocate_tcp_port(),
                        probe_boundary,
                    )
                    probe_command.append("--pull=false")
                    probe_result = run_act_process(
                        probe_command,
                        cwd=layout.invocation,
                        env=env,
                        use_sudo=use_sudo,
                    )
                    if probe_result.returncode != 0:
                        raise Refusal(
                            f"{selected_workflow} exited "
                            f"{probe_result.returncode}"
                        )

            run_completed_live_probe(seed_workflow)
            require_act_toolcache_absent(
                use_sudo=use_sudo, cwd=layout.invocation, env=env
            )
            run_completed_live_probe(probe_workflow)
            require_act_toolcache_absent(
                use_sudo=use_sudo, cwd=layout.invocation, env=env
            )

            planned = new_docker_boundary()
            monitor_cancel = threading.Event()
            frozen = threading.Event()
            privileged_child_seen = threading.Event()
            process_group_reaped = threading.Event()
            monitor_problems: list[str] = []
            monitor_threads: list[threading.Thread] = []
            monitor_completions: list[threading.Event] = []
            monitor_signal_lock = threading.Lock()
            launched_process_group: int | None = None
            with temporary_docker_boundary(
                planned,
                use_sudo=use_sudo,
                cwd=layout.invocation,
                env=env,
            ) as boundary:
                command = build_act_command(
                    prefix,
                    workflow,
                    layout,
                    allocate_tcp_port(),
                    boundary,
                )
                command.append("--pull=false")

                def process_started(process_group: int) -> None:
                    nonlocal launched_process_group
                    launched_process_group = process_group

                    def interrupt_main(message: str, sent_signal: int) -> None:
                        with monitor_signal_lock:
                            if monitor_cancel.is_set():
                                return
                            if message:
                                monitor_problems.append(message)
                            os.kill(os.getpid(), sent_signal)

                    def freeze_live_act() -> None:
                        deadline = time.monotonic() + 120
                        while not monitor_cancel.is_set():
                            try:
                                inventory = docker_container_inventory(
                                    use_sudo=use_sudo,
                                    cwd=layout.invocation,
                                    env=env,
                                    cancel=monitor_cancel,
                                )
                                if monitor_cancel.is_set():
                                    return
                                selected = owned_container_ids(inventory, boundary)
                                if running_container_ids(inventory, selected):
                                    if monitor_cancel.is_set():
                                        return
                                    try:
                                        inspect_act_toolcache_volume(
                                            boundary,
                                            use_sudo=use_sudo,
                                            cwd=layout.invocation,
                                            env=env,
                                        )
                                        if monitor_cancel.is_set():
                                            return
                                        verify_runner_toolcache_mounts(
                                            inventory,
                                            boundary,
                                            require_any=True,
                                        )
                                    except Refusal as exc:
                                        interrupt_main(str(exc), signal.SIGINT)
                                        return
                                    if monitor_cancel.is_set():
                                        return
                                    try:
                                        members = process_group_inventory(
                                            process_group
                                        )
                                        if not members:
                                            raise Refusal(
                                                "live act process group disappeared"
                                            )
                                        if use_sudo:
                                            if not any(
                                                pid != process_group and uid == 0
                                                for pid, _state, uid in members
                                            ):
                                                raise Refusal(
                                                    "no privileged act child appeared"
                                                )
                                            privileged_child_seen.set()
                                        if monitor_cancel.is_set():
                                            return
                                    except (OSError, Refusal) as exc:
                                        interrupt_main(
                                            f"cannot freeze live act process: {exc}",
                                            signal.SIGINT,
                                        )
                                        return
                                    # Cancellation and the privileged STOP are
                                    # one serialized transition. Main cannot
                                    # begin Docker teardown until this worker
                                    # either completes the injection or exits.
                                    with monitor_signal_lock:
                                        if monitor_cancel.is_set():
                                            return
                                        try:
                                            signal_process_group(
                                                process_group,
                                                signal.SIGSTOP,
                                                use_sudo=use_sudo,
                                            )
                                            frozen_members = (
                                                wait_for_frozen_process_group(
                                                    process_group,
                                                    {
                                                        pid
                                                        for pid, _state, _uid in members
                                                    },
                                                )
                                            )
                                            if use_sudo and not any(
                                                pid != process_group
                                                and uid == 0
                                                and state.startswith("T")
                                                for pid, state, uid in frozen_members
                                            ):
                                                raise Refusal(
                                                    "privileged act child was not frozen"
                                                )
                                            frozen.set()
                                            os.kill(os.getpid(), signal.SIGTERM)
                                        except (OSError, Refusal) as exc:
                                            monitor_problems.append(
                                                "cannot freeze live act process: "
                                                f"{exc}"
                                            )
                                            os.kill(os.getpid(), signal.SIGINT)
                                    return
                            except Refusal:
                                # Container creation/removal can race one inventory;
                                # retry until the bounded deadline.
                                pass
                            if time.monotonic() >= deadline:
                                interrupt_main(
                                    "no owned running act container appeared "
                                    "within 120s",
                                    signal.SIGINT,
                                )
                                return
                            monitor_cancel.wait(0.25)

                    monitor_complete = threading.Event()

                    def monitored_freeze_live_act() -> None:
                        try:
                            freeze_live_act()
                        finally:
                            monitor_complete.set()

                    monitor = threading.Thread(
                        target=monitored_freeze_live_act,
                        name="act-ci-interrupt-monitor",
                        daemon=True,
                    )
                    monitor_threads.append(monitor)
                    monitor_completions.append(monitor_complete)
                    start_cleanup_thread_or_refuse(
                        monitor, "interrupt monitor"
                    )

                interrupted = False
                try:
                    result = run_act_process(
                        command,
                        cwd=layout.invocation,
                        env=env,
                        started=process_started,
                        use_sudo=use_sudo,
                    )
                except (KeyboardInterrupt, TerminationRequest) as exc:
                    if (
                        isinstance(exc, TerminationRequest)
                        and exc.signum not in (signal.SIGINT, signal.SIGTERM)
                    ):
                        raise
                    interrupted = True
                finally:
                    cancel_and_join_cleanup_threads(
                        monitor_cancel,
                        monitor_signal_lock,
                        list(
                            zip(
                                monitor_threads,
                                monitor_completions,
                                strict=True,
                            )
                        ),
                        monitor_problems,
                    )
                if not interrupted:
                    raise Refusal(
                        f"interrupt self-test act process exited {result.returncode} "
                        "before fault injection"
                    )
                if monitor_problems:
                    raise Refusal(monitor_problems[0])
                if not frozen.is_set():
                    raise Refusal("interrupt self-test did not freeze act")
                if use_sudo and not privileged_child_seen.is_set():
                    raise Refusal("interrupt self-test did not inspect root act")
                if launched_process_group is None:
                    raise Refusal("interrupt self-test did not record the act group")
                if process_group_exists(
                    launched_process_group, use_sudo=use_sudo
                ):
                    raise Refusal("interrupt self-test left an act process-group member")
                process_group_reaped.set()
        finally:
            for selected_workflow in (
                workflow,
                seed_workflow,
                probe_workflow,
            ):
                WORKFLOWS.pop(selected_workflow, None)

        final_inventory = docker_container_inventory(
            use_sudo=use_sudo, cwd=layout.invocation, env=env
        )
        survivors = owned_container_ids(final_inventory, planned)
        if survivors:
            raise Refusal(
                f"interrupt self-test left {len(survivors)} owned container(s)"
            )
        require_act_toolcache_absent(
            use_sudo=use_sudo, cwd=layout.invocation, env=env
        )
        if not process_group_reaped.is_set():
            raise Refusal("interrupt self-test did not prove process-group absence")
    print(
        "interrupt-selftest: PASS (tool cache did not cross runs; the frozen "
        "act process group left no process, container, network, or volume)"
    )
    return RC_OK


def main(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pr", type=int, help="open pull-request number")
    parser.add_argument("--repo", help="OWNER/REPO (default: trusted gh repository)")
    parser.add_argument(
        "--worktree",
        type=pathlib.Path,
        help="candidate worktree to cross-check (default: current directory)",
    )
    parser.add_argument(
        "--workflow",
        action="append",
        choices=("all", *WORKFLOWS),
        help="workflow alias; repeatable (default: all)",
    )
    parser.add_argument("--act-bin", default="act", help="trusted act executable")
    parser.add_argument(
        "--trusted-install-sha256",
        help=(
            "SHA-256 of an independently audited immutable runner install; "
            "bootstrap only, never point this at the candidate worktree"
        ),
    )
    parser.add_argument(
        "--sudo",
        action="store_true",
        help="run Docker and act through non-interactive sudo",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="materialize and print exact act commands without running them",
    )
    parser.add_argument(
        "--selftest",
        action="store_true",
        help="run offline negative and construction tests",
    )
    parser.add_argument(
        "--interrupt-selftest",
        action="store_true",
        help="freeze a live act job and verify Docker cleanup (requires Docker)",
    )
    args = parser.parse_args(argv[1:])

    if args.selftest:
        if (
            args.pr is not None
            or args.workflow
            or args.dry_run
            or args.trusted_install_sha256
            or args.interrupt_selftest
        ):
            parser.error("--selftest cannot be combined with PR-run arguments")
        shipping_root = (args.worktree or ROOT).expanduser().resolve()
        return selftest(shipping_root)
    if args.interrupt_selftest:
        if (
            args.pr is not None
            or args.workflow
            or args.dry_run
            or args.trusted_install_sha256
            or args.repo is not None
            or args.worktree is not None
        ):
            parser.error(
                "--interrupt-selftest cannot be combined with PR-run arguments"
            )
        try:
            act_binary = resolve_act_binary(args.act_bin)
            validate_act_binary(act_binary, pathlib.Path.cwd().resolve())
            return run_with_cleanup_signals(
                lambda: interrupt_selftest(act_binary, args.sudo)
            )
        except Refusal as exc:
            print(f"act-ci: REFUSED: {exc}", file=sys.stderr)
            return RC_REFUSED
    if args.pr is None or args.pr <= 0:
        parser.error("--pr requires a positive pull-request number")

    def execute_pr_run() -> int:
        validate_bootstrap_options(
            args.trusted_install_sha256, args.repo, args.worktree
        )
        workflows = select_workflows(args.workflow)
        repository = args.repo or repository_name()
        pr = query_pull_request(args.pr, repository)
        validate_pull_request(pr, repository)
        candidate_worktree = (args.worktree or pathlib.Path.cwd()).expanduser().resolve()
        validate_runner(pr, candidate_worktree, args.trusted_install_sha256)
        act_binary = resolve_act_binary(args.act_bin)
        validate_act_binary(act_binary, candidate_worktree)
        return run_validation(
            pr,
            repository,
            workflows,
            candidate_worktree,
            act_binary=act_binary,
            use_sudo=args.sudo,
            dry_run=args.dry_run,
        )

    try:
        return run_with_cleanup_signals(execute_pr_run)
    except Refusal as exc:
        print(f"act-ci: REFUSED: {exc}", file=sys.stderr)
        return RC_REFUSED


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
