#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run this repository's GitHub workflows locally at one exact PR head.

The runner is host-side security code. Invoke the copy from a clean trusted
``dev`` worktree, never the copy in the pull request being tested. It refuses
unless that trusted worktree is the validation base: the live remote ``dev``
tip resolved once at invocation. GitHub's recorded PR base oid is frozen when
the PR is opened, so it never refuses a run: it is printed, it selects which
note is printed, and it is the base SHA in the generated event, because that
payload feeds scope classification and hosted receives the recorded value.
Candidate files
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
A handled terminal signal returns ``128 + signum`` only after cleanup; SIGINT
therefore returns 130 and names itself in the final diagnostic.
"""

from __future__ import annotations

import argparse
import ast
import contextlib
import ctypes
import hashlib
import io
import inspect
import io
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
import socketserver
import stat
import subprocess
import sys
import tempfile
import threading
import time
from dataclasses import dataclass, field, fields, replace
from typing import Callable, Iterable, Iterator, Mapping, Sequence
from unittest import mock


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
#: The most host CPUs one job container may schedule onto. Hosted
#: ``ubuntu-latest`` runners have 4 vCPUs, so a workflow step written as
#: ``make -j"$(nproc)"`` (the Verilator and Yosys builds in rtl-fast) is a
#: hosted-shaped assumption: ``nproc`` reads the scheduler affinity, which
#: follows the container's cpuset, so an unbounded container starts one
#: compiler per host core - 128 on a 128-vCPU host, which exhausted the host's
#: memory and had the harness kill the replica. Four is the hosted runner's
#: own count, so a job's ``-j$(nproc)`` builds exactly what it builds hosted;
#: sixteen was tried first and four matrix legs at sixteen compilers each
#: still exhausted a 72 GB host. This is a replica-shape decision, not a
#: trust-boundary one; the cost is replica time, never fidelity.
CONTAINER_CPU_LIMIT = 4
#: The memory one job container may take, applied as both ``--memory`` and
#: ``--memory-swap`` so the bound includes swap. Hosted ``ubuntu-latest``
#: runners have 16 GB, so a job that needs more fails hosted too; a bounded
#: container fails the replica instead of the host, which eight unbounded
#: ``-j$(nproc)`` toolchain builds had nearly exhausted. Docker size syntax.
CONTAINER_MEMORY = "16g"
#: The jobs of one workflow stage act starts at once. Hosted jobs each get
#: their own runner; on one host the replica's jobs share it, and with the
#: CPU set alone an rtl-full replica launched all eight shard jobs together,
#: each building its toolchain. The flag bounds jobs, not matrix legs: act
#: runs a matrix job's legs ``strategy.max-parallel`` wide (default 4)
#: inside that job's slot, so one job at a time still lets each of
#: rtl-full's four-shard jobs fan out to four containers, each held to
#: CONTAINER_MEMORY: at most 64 GB at once. Below one, act falls back to
#: one job per host CPU. A replica-shape decision, as above; the hosted
#: runner gives every job its own machine.
CONCURRENT_JOB_LIMIT = 1
ACT_TOOLCACHE_VOLUME = "act-toolcache"
ACT_TOOLCACHE_TARGET = "/opt/hostedtoolcache"
ACT_TOOLCACHE_SEED_SUFFIX = "-toolcache-seed"
# act 0.2.89 names each job's workspace and environment volumes
# ``act-<workflow>-<job>-<sha256>`` and ``...-env`` from the workflow and
# job names, never from a run token, and removes them only inside its own
# graceful teardown; forced process-group containment bypasses that path.
ACT_JOB_VOLUME_RE = re.compile(
    r"^act-[A-Za-z0-9-]{0,58}[A-Za-z0-9]-[0-9a-f]{64}(?:-env)?$"
)
ACT_JOB_VOLUME_PREFIX_RE = re.compile(r"^act-(?:[A-Za-z0-9]+-)+$")
DOCKER_VOLUME_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
# One attached seed run bounds the daemon-side image copy-up (minutes for a
# multi-gigabyte runner tool cache) plus a possible first-time image pull.
ACT_TOOLCACHE_SEED_TIMEOUT = 30 * 60
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
#: act 0.2.89's own grammar for a remote `uses:` (newRemoteAction): owner,
#: repository, an optional subpath, and a mandatory ref.
ACTION_REFERENCE_RE = re.compile(r"^([^/@]+)/([^/@]+)(?:/([^@]*))?@(.+)$")
#: act names an action's cache directory after the WHOLE `uses:` string with
#: these characters turned into `-` (safeFilename), so `actions/cache@v4` is
#: read from `actions-cache@v4` and a subpath action keeps its subpath.
ACTION_CACHE_KEY_TRANSLATION = str.maketrans({char: "-" for char in '<>:"/\\|?*'})
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


@dataclass
class _CleanupSignalLatch:
    """Record one cleanup signal without changing masks or dispositions."""

    signum: int | None = None

    def __call__(self, signum: int, _frame: object) -> None:
        if self.signum is not None:
            return
        self.signum = signum
        raise TerminationRequest(signum)


@contextlib.contextmanager
def cleanup_termination_signals() -> Iterator[None]:
    """Make INT/TERM/HUP run cleanup and defer repeats until it completes."""
    watched = CLEANUP_SIGNALS
    previous = {item: signal.getsignal(item) for item in watched}
    request_cleanup = _CleanupSignalLatch()

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
    """Start a cleanup-safe worker; a start failure is a Refusal naming `description`."""
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
    installed_handlers = tuple(previous.values())
    first_handler = installed_handlers[0]
    cleanup_already_latched = (
        isinstance(first_handler, _CleanupSignalLatch)
        and first_handler.signum is not None
        and all(handler is first_handler for handler in installed_handlers)
    )

    if cleanup_already_latched or all(
        handler == signal.SIG_IGN for handler in installed_handlers
    ):
        # A first cleanup signal has already latched and repeats must remain
        # harmless. Use caught no-op handlers so exec resets the child to its
        # default dispositions instead of inheriting SIG_IGN.
        def ignore_repeat(_signum: int, _frame: object) -> None:
            """A caught no-op handler for a repeat signal."""
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
        """Record the first signal and defer it."""
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
    """Run `action` under the cleanup-signal handlers; an interrupt returns 128 + signum after cleanup."""
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
        """A PullRequest from `gh pr view` JSON; any malformed field is a Refusal."""
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
class ValidatedRun:
    """The pull request, its repository, and the ONE base every check reads.

    #292 was a base DISAGREEMENT: the trusted-worktree check read GitHub's
    frozen recorded oid while the fetch check read the live branch, so no
    worktree satisfied both. Threading one resolved SHA through six
    signatures repairs that symptom but keeps the shape that caused it - an
    argument position any call site can fill with a different string - and a
    source-shape check is not a durable guard for it: [R3] on PR #336 drove
    an ordinary pass-through helper through exactly such a check with every
    arm green, reinstating #292 in one line.

    So there is no base argument left to fill. The resolve returns this
    object, every consumer takes it, and the base is reachable only as
    ``run.validation_base``. Substituting the recorded oid now takes a second
    ValidatedRun - a visible new construction site, not a one-word edit - and
    the self-test pins that production has exactly one.
    """

    pr: PullRequest
    repository: str
    validation_base: str

    def __post_init__(self) -> None:
        if not SHA_RE.fullmatch(self.validation_base):
            raise Refusal(
                f"validation base is not a full commit SHA: "
                f"{self.validation_base!r}"
            )


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
class RemoteAction:
    """One remote `uses:` reference as act parses it: owner, repository, optional subpath, and ref."""

    spec: str
    owner: str
    repo: str
    path: str
    ref: str

    @property
    def clone_url(self) -> str:
        """The exact URL act clones and later compares with `remote.origin.url`; a `.git` suffix would differ."""
        return f"https://github.com/{self.owner}/{self.repo}"

    @property
    def cache_key(self) -> str:
        """The directory name act 0.2.89 derives from the `uses:` string."""
        return self.spec.translate(ACTION_CACHE_KEY_TRANSLATION)


@dataclass(frozen=True)
class DockerBoundary:
    """One unpredictable runner-owned Docker network and ephemeral cache slot."""

    token: str
    name: str
    network_id: str | None = None
    gateway: str | None = None
    toolcache_owned: bool = False
    toolcache_seeded: bool = False
    job_volume_prefixes: tuple[str, ...] = ()


@dataclass
class DockerBoundaryLease:
    """Mutable acquisition state registered before any Docker mutation."""

    boundary: DockerBoundary
    complete: bool = False
    released: bool = False


@dataclass(frozen=True)
class AbsenceWindow:
    """How long a removed resource must stay absent, with injectable clocks."""

    seconds: float | None = None
    monotonic: Callable[[], float] = time.monotonic
    sleep: Callable[[float], None] = time.sleep


@dataclass(frozen=True)
class CommandContext:
    """Where a host or Docker command runs: under sudo or not, in which directory, with which environment.

    The three cross every Docker and process boundary together, so they travel as one value.
    """

    use_sudo: bool
    cwd: pathlib.Path
    env: Mapping[str, str]


def require_tool(name: str) -> str:
    """The resolved path of host executable `name` found on SAFE_PATH; an absent tool is a Refusal."""
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
    """Stripped stdout of one host command; a failure, timeout, or launch error is a Refusal."""
    try:
        result = run_tracked_process_group_command(
            command,
            context=CommandContext(
                use_sudo=False,
                cwd=cwd,
                env=dict(os.environ if env is None else env),
            ),
            timeout=HOST_COMMAND_TIMEOUT,
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
    """The trusted OWNER/REPO name from `gh repo view`; malformed metadata is a Refusal."""
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
    """Read pull request `number` in `repository` through `gh`; malformed metadata is a Refusal."""
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
    """Refuse a PR that is not open, does not target dev, is cross-repository, or misreports its URL."""
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
    """The PullRequest field names that differ, ignoring the informational recorded base oid."""
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
    """Re-read the PR and refuse any change but a moved recorded base oid, which is only noted."""
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
            f"act-ci: NOTE: recorded base oid moved from {expected.base_sha} "
            f"to {current.base_sha} during validation; the validation base is "
            f"the live {expected.base_ref} tip resolved at invocation and the "
            f"unchanged exact-head evidence for {expected.head_sha} remains "
            "valid",
            flush=True,
        )


def parse_ls_remote_tip(raw: str, base_ref: str) -> str:
    """The ``refs/heads/<base_ref>`` SHA in ``git ls-remote`` output.

    ``git ls-remote <url> <pattern>`` matches the pattern against the TAIL of
    each ref name, not the whole of it, so the reply legitimately carries refs
    the caller did not ask for: a branch or TAG merely ENDING in
    ``refs/heads/<base_ref>`` matches too. Selecting the EXACT ref is
    therefore the correctness requirement, and counting the reply's lines is
    not a substitute for it - [R3] on PR #336 measured the cost of the line
    count on git 2.55.0: `git tag refs/heads/dev` is enough to make every
    lookup return two lines, so one pushed ref refused every run of a
    mandatory gate, repository-wide, until someone found and deleted it.

    Split out of the lookup so the refusals that read REMOTE-CONTROLLED bytes
    - a reply carrying no matching ref, the exact ref twice, or a line with no
    ref at all - are exercised by the self-test rather than trusted ([R1] on
    PR #336).
    """
    wanted = f"refs/heads/{base_ref}"
    tips: list[str] = []
    for line in raw.splitlines():
        sha, tab, name = line.partition("\t")
        if not tab:
            raise Refusal(
                f"live {base_ref} tip lookup returned a line carrying no ref: "
                f"{line!r}"
            )
        if name == wanted:
            tips.append(sha)
    if len(tips) != 1:
        raise Refusal(
            f"live {base_ref} tip lookup returned {len(tips)} {wanted} refs, "
            "not one"
        )
    return tips[0]


def query_remote_base_tip(repository: str, base_ref: str) -> str:
    """Read the live remote base tip once, credential-free, over HTTPS.

    Run from a scratch directory with a scratch HOME, the way every other
    remote operation in this runner already is. ``git_environment`` clears
    the system and per-user configuration but CANNOT clear a repository's own
    ``.git/config``, and that file is untracked, so the trusted worktree's
    cleanliness check never sees it: reading from ROOT let a local
    ``insteadOf`` retarget this lookup, and made the ordinary
    ``url."ssh://git@github.com/".insteadOf https://github.com/`` mirror
    rewrite refuse every run under ``protocol.allow=never``. A scratch HOME
    likewise keeps a ``.netrc`` beside the checkout out of the request that
    the docs call credential-free ([R3] on PR #336).
    """
    remote_url = f"https://github.com/{repository}.git"
    with tempfile.TemporaryDirectory(prefix="act-ci-ls-remote-") as scratch:
        scratch_root = pathlib.Path(scratch)
        raw = capture(
            [*git_prefix(), "ls-remote", "--", remote_url, f"refs/heads/{base_ref}"],
            cwd=scratch_root,
            env=git_environment(scratch_root),
            description=f"live {base_ref} tip lookup",
        )
    return parse_ls_remote_tip(raw, base_ref)


def base_construction_report(source: str) -> list[str]:
    """The top-level functions that construct a ValidatedRun, self-test aside.

    The value object removes the base ARGUMENT, so no call site can hand a
    consumer the wrong string any more - which is what the 172-line
    source-shape reader this replaces existed to catch, and what [R3] on
    PR #336 walked past with a pass-through helper whose parameter merely
    shared the audited name. What a value object cannot remove is a second
    CONSTRUCTION: ``ValidatedRun(pr, repository, pr.base_sha)`` elsewhere
    would reinstate #292 whole.

    So that is what this reads, and the whole of what it claims: production
    builds the object in exactly one place, the audited resolve. One
    property, checkable, with no oversized claim attached - a correct check
    carrying one is how three defects in this lane's own evidence were
    written ([R2] named the pattern).
    """
    tree = ast.parse(source)
    span = next(
        (
            (node.lineno, node.end_lineno or node.lineno)
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef) and node.name == "selftest"
        ),
        None,
    )

    def owner(line: int) -> str:
        """The top-level function containing `line`, or `<module>`."""
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and (
                node.lineno <= line <= (node.end_lineno or node.lineno)
            ):
                return node.name
        return "<module>"

    sites: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
            continue
        if node.func.id != "ValidatedRun":
            continue
        if span is not None and span[0] <= node.lineno <= span[1]:
            continue
        sites.append((node.lineno, owner(node.lineno)))
    return [name for _line, name in sorted(sites)]


def emit_flushed(message: str) -> None:
    """Print one runner note, flushed - a transcript line, not buffered text."""
    print(message, flush=True)


def resolve_validation_base(
    pr: PullRequest,
    repository: str,
    *,
    query_tip: Callable[[str, str], str] = query_remote_base_tip,
    emit: Callable[[str], None] = emit_flushed,
) -> ValidatedRun:
    """Resolve the one base every later check reads, and bind it to the run.

    GitHub freezes a pull request's recorded base oid (``baseRefOid``) when
    the PR is opened; it does not track the base branch afterward. The runner
    therefore validates against the live remote base tip resolved once here.
    The recorded oid stays informational: it is read only to choose which
    note to print, and never refuses a run.

    The repository name and the base ref are re-asserted here rather than
    inherited from an earlier call, because both are interpolated into the
    remote lookup below. The ordering arm this replaces pinned where
    ``validate_pull_request`` APPEARS in ``main``, which is not the same as
    it having run: moving that call into a never-invoked closure kept the
    arm green and left these two values unchecked ([R3] on PR #336).

    The two collaborators are keyword-only so a call site cannot fill them
    positionally, and the self-test pins their defaults.
    """
    if not REPOSITORY_RE.fullmatch(repository):
        raise Refusal(f"invalid repository name: {repository!r}")
    if pr.base_ref != DEFAULT_BASE:
        raise Refusal(
            f"pull request #{pr.number} targets {pr.base_ref}, not {DEFAULT_BASE}"
        )
    live = query_tip(repository, pr.base_ref)
    if not SHA_RE.fullmatch(live):
        raise Refusal(
            f"live {pr.base_ref} tip is not a full commit SHA: {live!r}"
        )
    if live == pr.base_sha:
        emit(
            f"act-ci: validation base {live} (live {pr.base_ref} tip; "
            "matches the recorded base oid)"
        )
    else:
        emit(
            f"act-ci: NOTE: recorded base oid {pr.base_sha} is stale; "
            f"validating against the live {pr.base_ref} tip {live}"
        )
    return ValidatedRun(pr, repository, live)


def select_workflows(requested: Iterable[str] | None) -> tuple[str, ...]:
    """The workflow aliases to run, de-duplicated in request order; `all` alone selects every one."""
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
    """The (major, minor, patch) triple in act's version text; unparseable text is a Refusal."""
    found = ACT_VERSION_RE.search(text)
    if not found:
        raise Refusal(f"cannot parse act version from {text!r}")
    return tuple(int(value) for value in found.groups())  # type: ignore[return-value]


def require_supported_act_version(version: tuple[int, int, int]) -> None:
    """Refuse any act version but the audited SUPPORTED_ACT_VERSION."""
    if version != SUPPORTED_ACT_VERSION:
        want = ".".join(str(part) for part in SUPPORTED_ACT_VERSION)
        got = ".".join(str(part) for part in version)
        raise Refusal(
            f"act {got} is not the audited version {want}; review its Docker "
            "tool-cache behavior before changing the pin"
        )


def resolve_act_binary(value: str) -> str:
    """The absolute act executable for a path or a SAFE_PATH name; an unavailable one is a Refusal."""
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
    """Refuse an act executable that resolves inside the candidate worktree."""
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
    """The git command prefix that disables hooks, credentials, and every protocol but HTTPS."""
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
    """Stripped stdout of one git command in `root` under the no-ambient-configuration environment."""
    safe_home = home or root
    return capture(
        [*git_prefix(), "-C", str(root), *arguments],
        cwd=root,
        env=git_environment(safe_home),
        description=description,
    )


def checkout_state(root: pathlib.Path) -> tuple[str, str, str]:
    """(HEAD SHA, porcelain status, replacement refs) for the worktree at `root`."""
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
    """The Git blob object ID of `data`."""
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()  # noqa: S324 - Git object ID


def expected_file(root: pathlib.Path, commit: str, relative: str) -> tuple[str, str]:
    """(mode, blob OID) of `relative` at `commit`; anything but one regular tracked blob is a Refusal."""
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
    """Refuse a checked-out file whose bytes or mode differ from `relative` at `commit`."""
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
    """Refuse a worktree that is dirty, carries replacement refs, or is not at the exact PR head."""
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


def validate_trusted_runner(
    run: ValidatedRun,
    *,
    state: Callable[[pathlib.Path], tuple[str, str, str]] = checkout_state,
    verify_bytes: Callable[[pathlib.Path, str, str], None] = validate_file_bytes,
) -> None:
    """Refuse a runner loaded from the candidate or a modified/stale base.

    The worktree is required at the VALIDATION BASE - the live remote tip -
    not at the frozen recorded oid, which is the half of #292 that made no
    trusted worktree satisfy both checks. The two collaborators are injected
    so the self-test exercises that comparison ([R1] on PR #336 found it
    asserted by nothing, and the audited-install proof routes around it).
    """
    head, dirty, replacements = state(ROOT)
    if replacements:
        raise Refusal(
            "trusted runner worktree has replacement refs; use a clean dev worktree"
        )
    if dirty:
        raise Refusal(
            "trusted runner worktree is dirty; invoke the exact clean remote dev copy"
        )
    if head != run.validation_base:
        raise Refusal(
            f"runner was loaded from {head}, not the live {run.pr.base_ref} tip "
            f"{run.validation_base}; fast-forward the trusted worktree to the "
            f"current remote {run.pr.base_ref} tip and invoke it again"
        )
    try:
        relative = pathlib.Path(__file__).resolve().relative_to(ROOT).as_posix()
    except ValueError as exc:
        raise Refusal("runner is not installed beneath its trusted repository") from exc
    verify_bytes(ROOT, run.validation_base, relative)


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
    run: ValidatedRun,
    candidate_worktree: pathlib.Path,
    trusted_install_sha256: str | None,
) -> None:
    """Validate the trusted-worktree runner, or the content-pinned install when a pin is given."""
    if trusted_install_sha256 is None:
        validate_trusted_runner(run)
        return
    validate_installed_runner_file(
        pathlib.Path(__file__), trusted_install_sha256, candidate_worktree
    )


def validate_bootstrap_options(
    trusted_install_sha256: str | None,
    repository_argument: str | None,
    worktree_argument: pathlib.Path | None,
) -> None:
    """Refuse a content-pinned bootstrap that does not name both --repo and --worktree."""
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
    """Remove the exact generated run directory, reclaiming sudo-owned data first; any doubt is a Refusal."""
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
                    context=CommandContext(
                        use_sudo=True,
                        cwd=run.parent,
                        env={"PATH": SAFE_PATH, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"},
                    ),
                    timeout=RUN_DIRECTORY_RECLAIM_TIMEOUT,
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
    """Yield a private run directory and reclaim it, even from a partial acquisition, on exit."""
    lease = RunDirectoryLease(pathlib.Path(tempfile.gettempdir()).resolve())
    try:
        run = make_run_directory(lease)
        yield run.path
    finally:
        if lease.accepted and not lease.released:
            with blocked_cleanup_signals():
                cleanup_partial_run_directory(lease, use_sudo)


def make_layout(run_root: pathlib.Path, pr: PullRequest) -> RunLayout:
    """Create the per-run directories and empty input files beneath `run_root` for `pr`."""
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
    """The `git config` keys and values the trusted .gitmodules manifest must equal."""
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


def require_exact_fetched_refs(
    run: ValidatedRun, fetched_base: str, fetched_head: str
) -> None:
    """Refuse any ref movement since metadata lookup and the base resolve."""
    if fetched_head != run.pr.head_sha:
        raise Refusal(
            f"remote head {run.pr.head_ref} moved from {run.pr.head_sha} to "
            f"{fetched_head} between metadata lookup and fetch; discard this run"
        )
    if fetched_base != run.validation_base:
        raise Refusal(
            f"remote {run.pr.base_ref} moved from {run.validation_base} to "
            f"{fetched_base} between the invocation-time base resolve and "
            "fetch; re-run to resolve the new tip"
        )


def materialize_remote_head(
    run: ValidatedRun, layout: RunLayout
) -> pathlib.Path:
    """Fetch the public same-repository refs into a new credential-free repo."""
    pr = run.pr
    repository = run.repository
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
    require_exact_fetched_refs(run, fetched_base, fetched_head)
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
    """The workflow mapping at `relative`, parsed without anchors, aliases, or duplicate keys."""
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
        def construct_mapping(
            self, node: yaml.MappingNode, deep: bool = False
        ) -> dict[str, object]:
            """Construct a mapping, refusing non-string or duplicate keys."""
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


def parse_action_reference(spec: str) -> RemoteAction | None:
    """The remote action `spec` names; None for a `./` local or `docker://` step; any other shape is a Refusal."""
    if spec.startswith("./") or spec.startswith("docker://"):
        return None
    match = ACTION_REFERENCE_RE.fullmatch(spec)
    if match is None:
        raise Refusal(f"step uses {spec!r}, which is not of the form owner/repo[/path]@ref")
    owner, repo, path, ref = match.groups()
    return RemoteAction(spec=spec, owner=owner, repo=repo, path=path or "", ref=ref)


def workflow_step_uses(root: pathlib.Path, relative: str) -> list[str]:
    """Every step-level `uses:` string in the workflow at `relative` beneath `root`, in document order."""
    document = load_workflow(root, relative)
    jobs = document.get("jobs")
    if not isinstance(jobs, dict):
        raise Refusal(f"workflow has no jobs mapping: {relative}")
    uses: list[str] = []
    for job in jobs.values():
        steps = job.get("steps") if isinstance(job, dict) else None
        for step in steps if isinstance(steps, list) else ():
            if isinstance(step, dict) and isinstance(step.get("uses"), str):
                uses.append(step["uses"])
    return uses


def collect_workflow_actions(
    root: pathlib.Path, relatives: Sequence[str]
) -> tuple[RemoteAction, ...]:
    """The distinct remote actions the workflows at `relatives` use, sorted by `uses:` string.

    Local and `docker://` steps are not remote actions and are skipped here;
    the sandbox scan, which runs first, is what refuses them. Two distinct
    references that act would read from one cache directory are refused,
    because act re-clones a directory whose origin URL is not the one it
    expects, and in offline mode that is the race this step exists to end.
    """
    actions: dict[str, RemoteAction] = {}
    for relative in relatives:
        for spec in workflow_step_uses(root, relative):
            action = parse_action_reference(spec)
            if action is not None:
                actions.setdefault(spec, action)
    keyed: dict[str, str] = {}
    for spec, action in sorted(actions.items()):
        other = keyed.setdefault(action.cache_key, spec)
        if other != spec:
            raise Refusal(
                f"actions {other} and {spec} share act's cache directory {action.cache_key}"
            )
    return tuple(action for _spec, action in sorted(actions.items()))


def action_cache_directory(layout: RunLayout, action: RemoteAction) -> pathlib.Path:
    """Where act reads `action` from beneath this run's `--action-cache-path`."""
    return layout.action_cache / action.cache_key


def resolve_action_commit(
    directory: pathlib.Path,
    action: RemoteAction,
    *,
    home: pathlib.Path,
    run_git: Callable[..., str],
) -> str:
    """The commit `action.ref` names in the clone at `directory`, tried as act does: tag, origin branch, SHA.

    `git checkout --detach <name>` cannot take a branch that exists only as
    `origin/<name>` after a fresh clone, so the ref is resolved first, in
    the order act's own duck-typing uses, and the checkout takes the SHA.
    """
    failures: list[str] = []
    for candidate in (
        f"refs/tags/{action.ref}",
        f"refs/remotes/origin/{action.ref}",
        action.ref,
    ):
        try:
            resolved = run_git(
                [
                    *git_prefix(),
                    "-C",
                    str(directory),
                    "rev-parse",
                    "--verify",
                    "--quiet",
                    "--end-of-options",
                    f"{candidate}^{{commit}}",
                ],
                cwd=directory,
                env=git_environment(home),
                description=f"action {action.spec} resolve of {candidate}",
            )
        except Refusal as exc:
            failures.append(str(exc))
            continue
        if SHA_RE.fullmatch(resolved):
            return resolved
        failures.append(f"{candidate} resolved to {resolved!r}")
    raise Refusal(
        f"action {action.spec}: ref {action.ref!r} is neither a tag, an origin branch, "
        f"nor a commit of the clone ({'; '.join(failures)})"
    )


def materialize_action(
    layout: RunLayout, action: RemoteAction, run_git: Callable[..., str]
) -> str:
    """Clone `action` credential-free into its cache directory and check its ref out detached; the SHA."""
    directory = action_cache_directory(layout, action)
    env = git_environment(layout.home)
    run_git(
        [*git_prefix(), "clone", "--quiet", action.clone_url, str(directory)],
        cwd=layout.root,
        env=env,
        description=f"action {action.spec} clone",
    )
    commit = resolve_action_commit(directory, action, home=layout.home, run_git=run_git)
    run_git(
        [*git_prefix(), "-C", str(directory), "checkout", "--quiet", "--detach", commit],
        cwd=layout.root,
        env=env,
        description=f"action {action.spec} checkout",
    )
    return commit


def materialize_workflow_actions(
    layout: RunLayout,
    workflows: Sequence[str],
    *,
    dry_run: bool,
    run_git: Callable[..., str] = capture,
) -> tuple[RemoteAction, ...]:
    """Populate the run's action cache serially before act can start; under dry-run only print the plan.

    act materialises an action lazily from whichever sibling job reaches it
    first - a full clone into `<action-cache-path>/<key>` and a checkout of
    the ref - while the other siblings copy that same directory into their
    containers. A copy taken mid-checkout sees the default branch's files
    or a torn bundle (#337: `jest.config.ts` missing under
    `actions-cache@v4`; `__dirname` undefined in a truncated
    `dist/restore/index.js`). So the runner performs every clone itself,
    one at a time, and launches act with `--action-offline-mode` so no job
    fetches or checks out again. The audited set is re-checked here rather
    than inherited from the sandbox scan's position in the sequence: this
    is the step that puts candidate-named repositories on the network.
    """
    actions = collect_workflow_actions(
        layout.checkout, [WORKFLOWS[workflow] for workflow in workflows]
    )
    for action in actions:
        if action.spec not in TRUSTED_ACTION_USES:
            raise Refusal(
                f"action {action.spec} is outside the audited set and is not cloned"
            )
    for action in actions:
        if dry_run:
            directory = action_cache_directory(layout, action)
            emit_flushed(
                f"act-ci: action {action.spec} planned at {directory} (dry-run, not cloned)"
            )
            continue
        commit = materialize_action(layout, action, run_git)
        emit_flushed(f"act-ci: action {action.spec} materialised at {commit}")
    return actions


def act_container_name(*parts: str) -> str:
    """Mirror act 0.2.89 ``createContainerName``; the self-test pins it to a live name."""
    sanitized = re.sub(r"[^a-zA-Z0-9]", "-", "-".join(parts)).replace("--", "-")
    digest = hashlib.sha256(sanitized.encode("ascii")).hexdigest()
    return f"{sanitized[:63].strip('-')}-{digest}"


def act_job_volume_prefix(workflow_name: object) -> str:
    """The name prefix act gives every job volume of one workflow name."""
    if not isinstance(workflow_name, str) or not workflow_name.strip():
        raise Refusal(
            "workflow must declare a non-empty name; act derives job volume "
            "names from it"
        )
    if workflow_name.strip() in ("null", "Null", "NULL", "~"):
        # The sandbox loader keeps YAML scalars as strings; act's decoder reads
        # these as no name and falls back to the file name.
        raise Refusal(
            f"workflow name {workflow_name!r} is a YAML null literal, which act "
            "reads as no name"
        )
    prefix = re.sub(r"[^a-zA-Z0-9]", "-", f"act-{workflow_name}/").replace(
        "--", "-"
    )
    if len(prefix) > 63 or not ACT_JOB_VOLUME_PREFIX_RE.fullmatch(prefix):
        raise Refusal(
            f"workflow name {workflow_name!r} yields an unleasable act "
            "job-volume prefix"
        )
    return prefix


def workflow_job_volume_scope(
    root: pathlib.Path, workflows: Sequence[str]
) -> dict[str, str]:
    """Map each selected workflow alias to the act job-volume prefix it leases."""
    scope: dict[str, str] = {}
    for workflow in workflows:
        relative = WORKFLOWS[workflow]
        document = load_workflow(root, relative)
        try:
            scope[workflow] = act_job_volume_prefix(document.get("name"))
        except Refusal as exc:
            raise Refusal(f"workflow {relative}: {exc}") from exc
    # act separates the workflow and job segments with the same "-" it uses
    # inside them, so one prefix extending another could not be told apart.
    prefixes = set(scope.values())
    for prefix in sorted(prefixes):
        for other in sorted(prefixes):
            if other != prefix and other.startswith(prefix):
                raise Refusal(
                    f"workflow name prefixes {prefix!r} and {other!r} overlap; "
                    "their act job volumes could not be told apart"
                )
    return scope


def is_leased_act_job_volume(boundary: DockerBoundary, name: str) -> bool:
    """True when act's name shape matches and a leased prefix owns the name."""
    return bool(ACT_JOB_VOLUME_RE.fullmatch(name)) and any(
        name.startswith(prefix) for prefix in boundary.job_volume_prefixes
    )


def build_event(run: ValidatedRun) -> dict[str, object]:
    """The smallest pull_request payload every repository workflow consumes.

    The base SHA is the RECORDED base oid, because this payload's only
    consumer is scope classification and hosted receives the recorded value.
    All three scope steps (`rtl.yml`, `rtl-fast.yml`, `elaborate.yml`) run a
    two-argument `git diff <base> <head>` - a tree comparison, not a
    merge-base one - so handing them a different base makes the local replica
    classify a different file set than the hosted run it exists to predict,
    in BOTH directions: a file the head and the live tip now agree on drops
    out of the diff, and `ci_scope.is_rtl_relevant` fails safe only on a
    wholly EMPTY list, not on a docs-only remainder. A stacked PR whose own
    changes are documentation would then report PASS locally having run no
    RTL job while hosted ran the sweep ([R3] on PR #336; the equality this
    lane replaced made the divergence impossible, so it is this lane's to
    avoid). The fetch is full-history, so the recorded oid is present in the
    materialized checkout and the two diffs are identical.

    The trust properties stay on the validation base, where they belong:
    which commit the trusted worktree must be at, and which commit the fetch
    must return. Neither reads this payload.
    """
    pr = run.pr
    repository = run.repository
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
    """`executable` alone, or under sudo a `sudo -n -- env -i` prefix carrying exactly `env`."""
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
    """The isolated command prefix for the host docker executable."""
    return isolated_command_prefix(require_tool("docker"), use_sudo, env)


def run_docker(
    arguments: Sequence[str],
    *,
    context: CommandContext,
    description: str,
    check: bool = True,
    timeout: float = DOCKER_COMMAND_TIMEOUT,
    run_command: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> subprocess.CompletedProcess[str]:
    """One Docker CLI command's completed result; a timeout, launch error, or checked failure is a Refusal."""
    command = [*docker_prefix(context.use_sudo, context.env), *arguments]
    try:
        if run_command is subprocess.run:
            result = run_tracked_process_group_command(
                command,
                context=context,
                timeout=timeout,
            )
        else:
            result = run_command(
                command,
                cwd=context.cwd,
                env=dict(context.env),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout,
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
    """Whether a failed `docker volume` result says the act tool-cache volume does not exist."""
    detail = (result.stderr or "").lower()
    return (
        result.returncode != 0
        and ACT_TOOLCACHE_VOLUME in detail
        and "no such volume" in detail
    )


def docker_reports_missing_volume(
    result: subprocess.CompletedProcess[str], name: str
) -> bool:
    """True only when Docker itself says this exact volume does not exist."""
    detail = (result.stderr or "").lower()
    return (
        result.returncode != 0
        and name.lower() in detail
        and "no such volume" in detail
    )


def list_docker_volume_names(
    *,
    context: CommandContext,
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
) -> list[str]:
    """Every volume name the daemon lists; a failed inventory is a refusal."""
    result = docker_command(
        ["volume", "ls", "--quiet"],
        context=context,
        description="Docker volume inventory",
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or "").strip().splitlines()
        suffix = f": {detail[-1]}" if detail else ""
        raise Refusal(f"Docker volume inventory failed{suffix}")
    names: list[str] = []
    for line in (result.stdout or "").splitlines():
        name = line.strip()
        if not name:
            continue
        if not DOCKER_VOLUME_NAME_RE.fullmatch(name):
            raise Refusal("Docker returned a malformed volume name")
        names.append(name)
    return names


def docker_volume_record(
    name: str,
    *,
    context: CommandContext,
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
) -> Mapping[str, object] | None:
    """The inspected volume, or None only when Docker reports it absent."""
    result = docker_command(
        ["volume", "inspect", name],
        context=context,
        description=f"volume {name} inspection",
        check=False,
    )
    if result.returncode != 0:
        if docker_reports_missing_volume(result, name):
            return None
        detail = (result.stderr or "").strip().splitlines()
        suffix = f": {detail[-1]}" if detail else ""
        raise Refusal(f"cannot inspect volume {name}{suffix}")
    try:
        volumes = json.loads(result.stdout)
        volume = volumes[0]
    except (json.JSONDecodeError, IndexError, KeyError, TypeError) as exc:
        raise Refusal(f"Docker returned malformed metadata for volume {name}") from exc
    if (
        not isinstance(volumes, list)
        or len(volumes) != 1
        or not isinstance(volume, dict)
        or volume.get("Name") != name
    ):
        raise Refusal(f"Docker returned malformed metadata for volume {name}")
    return volume


def require_act_job_volumes_absent(
    boundary: DockerBoundary,
    *,
    context: CommandContext,
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
) -> None:
    """Refuse before any mutation when act would reuse a job volume nobody owns."""
    if not boundary.job_volume_prefixes:
        raise Refusal("Docker boundary leases no act job-volume scope")
    present = [
        name
        for name in list_docker_volume_names(
            context=context, docker_command=docker_command
        )
        if is_leased_act_job_volume(boundary, name)
    ]
    if present:
        raise Refusal(
            "act job volume(s) already exist inside this run's lease scope: "
            + ", ".join(present)
            + "; act derives these names from workflow and job names rather "
            "than the run token, so a pre-existing one would become the "
            "candidate's workspace or environment; serialize every act runner, "
            "prove no container uses them, then remove them before retrying"
        )


def owned_volume_mounts(
    inventory: Sequence[Mapping[str, object]], owned: set[str]
) -> list[str]:
    """Named volumes mounted by owned containers.

    The leased tool cache is excluded, and so is every anonymous volume,
    whose 64-hex name is removed with its container.
    """
    names: set[str] = set()
    for item in inventory:
        if item.get("Id") not in owned:
            continue
        mounts = item.get("Mounts")
        if not isinstance(mounts, list):
            raise Refusal("owned act container has malformed mount metadata")
        for mount in mounts:
            if not isinstance(mount, dict) or mount.get("Type") != "volume":
                continue
            name = mount.get("Name")
            if not isinstance(name, str) or not DOCKER_VOLUME_NAME_RE.fullmatch(name):
                raise Refusal("owned act container mounts a malformed volume name")
            if name != ACT_TOOLCACHE_VOLUME and not DOCKER_ID_RE.fullmatch(name):
                names.add(name)
    return sorted(names)


def absence_window_seconds(
    absence: AbsenceWindow | None,
    docker_command: Callable[..., subprocess.CompletedProcess[str]],
) -> float:
    """The window a real daemon must keep a removed volume absent; fakes get none."""
    clock = absence or AbsenceWindow()
    if clock.seconds is None:
        return DOCKER_MUTATION_STABLE_SECONDS if docker_command is run_docker else 0.0
    return clock.seconds


def remove_act_job_volume(
    name: str,
    *,
    context: CommandContext,
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
    absence: AbsenceWindow | None = None,
) -> bool:
    """Remove one leased job volume without force and require stable absence.

    Returns whether the daemon still held the volume when removal began.
    """
    result = docker_command(
        ["volume", "rm", name],
        context=context,
        description=f"act job volume {name} removal",
        check=False,
    )
    removed = result.returncode == 0
    if result.returncode != 0 and not docker_reports_missing_volume(result, name):
        detail = (result.stderr or "").strip().splitlines()
        suffix = f": {detail[-1]}" if detail else ""
        raise Refusal(f"cannot remove act job volume {name}{suffix}")
    clock = absence or AbsenceWindow()
    window = absence_window_seconds(absence, docker_command)
    stable_since: float | None = None
    probes = 0
    while True:
        probes += 1
        if probes > 1000:
            raise Refusal(f"act job volume {name} absence window never elapsed")
        probe = docker_command(
            ["volume", "inspect", name],
            context=context,
            description=f"act job volume {name} absence check",
            check=False,
        )
        if probe.returncode == 0:
            raise Refusal(f"act job volume {name} survived removal")
        if not docker_reports_missing_volume(probe, name):
            detail = (probe.stderr or "").strip().splitlines()
            suffix = f": {detail[-1]}" if detail else ""
            raise Refusal(f"cannot verify act job volume {name} absence{suffix}")
        now = clock.monotonic()
        if stable_since is None:
            stable_since = now
        remaining = window - (now - stable_since)
        if remaining <= 1e-6:
            return removed
        clock.sleep(min(0.05, remaining))


def cleanup_act_job_volumes(
    boundary: DockerBoundary,
    observed: Sequence[str],
    *,
    context: CommandContext,
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
) -> list[str]:
    """Remove every job volume act created for this boundary and prove absence.

    Only a name inside the workflow-scoped lease is removed, because only that
    scope was proved absent at acquisition. A volume an owned container mounted
    outside the scope cannot be proved to be this run's creation: it is
    preserved and reported as lease drift. Nothing is forced, so a volume
    another container still holds is preserved and reported too.
    """
    errors: list[str] = []
    if not boundary.job_volume_prefixes:
        errors.append("Docker boundary leases no act job-volume scope")
    listed: list[str] = []
    try:
        listed = list_docker_volume_names(
            context=context, docker_command=docker_command
        )
    except Refusal as exc:
        errors.append(str(exc))
    in_scope = {name for name in listed if is_leased_act_job_volume(boundary, name)}
    strays = sorted(
        name for name in observed if not is_leased_act_job_volume(boundary, name)
    )
    if strays:
        errors.append(
            "owned container(s) mounted volume(s) outside the leased act "
            "job-volume scope, preserved for the operator: " + ", ".join(strays)
        )
    leased_observed = {
        name for name in observed if is_leased_act_job_volume(boundary, name)
    }
    removed: list[str] = []
    for name in sorted(in_scope.union(leased_observed)):
        try:
            if remove_act_job_volume(
                name,
                context=context,
                docker_command=docker_command,
            ):
                removed.append(name)
        except Refusal as exc:
            errors.append(str(exc))
    try:
        survivors = [
            name
            for name in list_docker_volume_names(
                context=context, docker_command=docker_command
            )
            if is_leased_act_job_volume(boundary, name)
        ]
    except Refusal as exc:
        errors.append(str(exc))
    else:
        if survivors:
            errors.append(
                "act job volume(s) survived cleanup: " + ", ".join(survivors)
            )
    if errors:
        raise Refusal("act job volume cleanup failed: " + "; ".join(errors))
    return removed


def docker_reports_missing_network(
    result: subprocess.CompletedProcess[str], target: str
) -> bool:
    """Whether a failed `docker network` result says `target` does not exist."""
    detail = (result.stderr or "").lower()
    return (
        result.returncode != 0
        and target.lower() in detail
        and ("no such network" in detail or "not found" in detail)
    )


def docker_reports_missing_container(
    result: subprocess.CompletedProcess[str], target: str
) -> bool:
    """Whether a failed `docker container` result says `target` does not exist."""
    detail = (result.stderr or "").lower()
    return (
        result.returncode != 0
        and target.lower() in detail
        and ("no such container" in detail or "no such object" in detail)
    )


def decode_act_toolcache_volume(text: str) -> Mapping[str, object]:
    """The single volume object in `docker volume inspect` JSON; anything else is a Refusal."""
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
    """The act tool-cache volume, refused unless local and labelled with `boundary`'s token."""
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
    context: CommandContext,
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
) -> None:
    """Refuse when the shared act tool-cache volume exists or its absence cannot be verified."""
    result = docker_command(
        ["volume", "inspect", ACT_TOOLCACHE_VOLUME],
        context=context,
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
    context: CommandContext,
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
) -> Mapping[str, object]:
    """The owned act tool-cache volume's metadata; a missing or foreign volume is a Refusal."""
    if not boundary.toolcache_owned:
        raise Refusal("Docker boundary has no owned act tool-cache volume")
    result = docker_command(
        ["volume", "inspect", ACT_TOOLCACHE_VOLUME],
        context=context,
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
    context: CommandContext,
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
            context=context,
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
            context=context,
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
    context: CommandContext,
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
) -> DockerBoundary:
    """Create the labelled act tool-cache volume for `planned`, rolling it back on any failure."""
    if planned.toolcache_owned:
        raise Refusal("refusing to recreate an initialized act tool-cache volume")
    require_act_toolcache_absent(
        context=context, docker_command=docker_command
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
            context=context,
            description="ephemeral act tool-cache creation",
        )
        if result.stdout.strip() != ACT_TOOLCACHE_VOLUME:
            raise Refusal("Docker returned the wrong act tool-cache volume name")
        inspect_act_toolcache_volume(
            boundary,
            context=context,
            docker_command=docker_command,
        )
    except BaseException as primary:
        try:
            with blocked_cleanup_signals():
                discard_act_toolcache_if_owned(
                    boundary,
                    context=context,
                    docker_command=docker_command,
                )
        except Refusal as cleanup_error:
            raise Refusal(
                f"act tool-cache setup rollback failed: {cleanup_error}"
            ) from primary
        raise
    return boundary


def toolcache_seed_container_name(boundary: DockerBoundary) -> str:
    """The name of the seed container that populates `boundary`'s tool cache."""
    return f"{boundary.name}{ACT_TOOLCACHE_SEED_SUFFIX}"


def discard_toolcache_seed_container(
    boundary: DockerBoundary,
    *,
    context: CommandContext,
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
    stability_window: float | None = None,
    monotonic: Callable[[], float] = time.monotonic,
    sleep: Callable[[float], None] = time.sleep,
) -> None:
    """Remove an owned seed container and require a stable absence window."""
    name = toolcache_seed_container_name(boundary)
    window = (
        DOCKER_MUTATION_STABLE_SECONDS
        if stability_window is None and docker_command is run_docker
        else (stability_window or 0)
    )
    stable_since: float | None = None
    removals = 0
    while True:
        result = docker_command(
            ["container", "inspect", name],
            context=context,
            description="act tool-cache seed container inspection",
            check=False,
        )
        if result.returncode != 0:
            if not docker_reports_missing_container(result, name):
                detail = (result.stderr or "").strip().splitlines()
                suffix = f": {detail[-1]}" if detail else ""
                raise Refusal(
                    f"cannot reconcile act tool-cache seed container{suffix}"
                )
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
            containers = json.loads(result.stdout)
            item = containers[0]
            config = item.get("Config")
            labels = config.get("Labels") if isinstance(config, dict) else None
        except (json.JSONDecodeError, IndexError, TypeError, AttributeError) as exc:
            raise Refusal(
                "Docker returned malformed seed container metadata"
            ) from exc
        if not isinstance(labels, dict):
            raise Refusal("act tool-cache seed container has malformed labels")
        if labels.get(DOCKER_OWNER_LABEL) != boundary.token:
            # Never delete a container this run does not own, even under the
            # unpredictable seed name; the volume rollback will fail loudly.
            return
        if removals >= 3:
            raise Refusal(
                "owned act tool-cache seed container survived repeated rollback"
            )
        removed = docker_command(
            ["container", "rm", "--force", "--volumes", name],
            context=context,
            description="act tool-cache seed container removal",
            check=False,
        )
        if removed.returncode != 0:
            detail = (removed.stderr or "").strip().splitlines()
            suffix = f": {detail[-1]}" if detail else ""
            raise Refusal(
                f"act tool-cache seed container removal failed{suffix}"
            )
        removals += 1


def seed_act_toolcache_volume(
    boundary: DockerBoundary,
    *,
    context: CommandContext,
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
) -> DockerBoundary:
    """Populate the fresh tool cache exactly once before any sibling job.

    Concurrent sibling-job container creates against one freshly created empty
    ``act-toolcache`` volume race inside the Docker daemon's image copy-up
    (an ``os.ReadDir`` emptiness gate followed by an unsynchronized directory
    copy): a losing create dies with ``failed to mkdir .../_data/Python: file
    exists`` while a trailing create can skip the copy entirely and run its
    job against a partially populated cache (#315). One owned, networkless
    seed container therefore performs the only empty-volume mount; its exit
    status proves the cache is populated before act may launch sibling jobs,
    which then all skip the daemon copy-up deterministically.
    """
    if not boundary.toolcache_owned:
        raise Refusal("cannot seed an unowned act tool-cache volume")
    if boundary.toolcache_seeded:
        raise Refusal("refusing to reseed an initialized act tool cache")
    name = toolcache_seed_container_name(boundary)
    try:
        result = docker_command(
            [
                "run",
                "--name",
                name,
                "--label",
                f"{DOCKER_OWNER_LABEL}={boundary.token}",
                "--network",
                "none",
                "--volume",
                f"{ACT_TOOLCACHE_VOLUME}:{ACT_TOOLCACHE_TARGET}",
                "--entrypoint",
                "/bin/bash",
                RUNNER_IMAGE,
                "-c",
                f'test -n "$(ls -A {ACT_TOOLCACHE_TARGET})"',
            ],
            context=context,
            description="act tool-cache deterministic seed",
            check=False,
            timeout=ACT_TOOLCACHE_SEED_TIMEOUT,
        )
        if result.returncode != 0:
            detail = (result.stderr or "").strip().splitlines()
            suffix = f": {detail[-1]}" if detail else ""
            raise Refusal(
                f"act tool-cache seed did not prove a populated cache{suffix}"
            )
        discard_toolcache_seed_container(
            boundary,
            context=context,
            docker_command=docker_command,
        )
        inspect_act_toolcache_volume(
            boundary,
            context=context,
            docker_command=docker_command,
        )
    except BaseException as primary:
        try:
            with blocked_cleanup_signals():
                discard_toolcache_seed_container(
                    boundary,
                    context=context,
                    docker_command=docker_command,
                )
        except Refusal as cleanup_error:
            raise Refusal(
                f"act tool-cache seed rollback failed: {cleanup_error}"
            ) from primary
        raise
    return replace(boundary, toolcache_seeded=True)


def cleanup_act_toolcache_volume(
    boundary: DockerBoundary,
    *,
    context: CommandContext,
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
) -> None:
    """Remove the owned act tool-cache volume and prove it absent; any failure is a Refusal."""
    inspect_act_toolcache_volume(
        boundary,
        context=context,
        docker_command=docker_command,
    )
    result = docker_command(
        ["volume", "rm", ACT_TOOLCACHE_VOLUME],
        context=context,
        description="ephemeral act tool-cache removal",
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or "").strip().splitlines()
        suffix = f": {detail[-1]}" if detail else ""
        raise Refusal(f"act tool-cache removal failed{suffix}")
    discard_act_toolcache_if_owned(
        boundary,
        context=context,
        docker_command=docker_command,
    )
    require_act_toolcache_absent(
        context=context,
        docker_command=docker_command,
    )


def new_docker_boundary(
    job_volume_prefixes: Iterable[str] = (),
) -> DockerBoundary:
    """A planned boundary with a fresh unpredictable ownership token and network name."""
    token = secrets.token_hex(16)
    if not re.fullmatch(r"[0-9a-f]{32}", token):
        raise Refusal("cannot generate a safe Docker ownership token")
    prefixes = tuple(sorted(set(job_volume_prefixes)))
    for prefix in prefixes:
        if len(prefix) > 63 or not ACT_JOB_VOLUME_PREFIX_RE.fullmatch(prefix):
            raise Refusal(f"invalid act job-volume lease prefix: {prefix!r}")
    return DockerBoundary(
        token=token, name=f"milan-act-ci-{token}", job_volume_prefixes=prefixes
    )


def inspect_docker_network(
    boundary: DockerBoundary,
    *,
    context: CommandContext,
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
) -> str:
    """The IPv4 gateway of `boundary`'s network; changed identity, ownership, or gateway is a Refusal."""
    if boundary.network_id is None or not DOCKER_ID_RE.fullmatch(boundary.network_id):
        raise Refusal("Docker boundary has no valid network ID")
    result = docker_command(
        ["network", "inspect", boundary.network_id],
        context=context,
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
    context: CommandContext,
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
) -> str:
    """The boundary's gateway once both its network and its tool-cache volume verify."""
    gateway = inspect_docker_network(
        boundary,
        context=context,
        docker_command=docker_command,
    )
    inspect_act_toolcache_volume(
        boundary,
        context=context,
        docker_command=docker_command,
    )
    return gateway


def discard_docker_network_if_owned(
    boundary: DockerBoundary,
    *,
    context: CommandContext,
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
            context=context,
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
            context=context,
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
    context: CommandContext,
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
) -> None:
    """Roll back whichever of the network and the tool cache this run owns; a failure is a Refusal."""
    errors: list[str] = []
    for cleanup in (discard_docker_network_if_owned, discard_act_toolcache_if_owned):
        try:
            cleanup(
                boundary,
                context=context,
                docker_command=docker_command,
            )
        except Refusal as exc:
            errors.append(str(exc))
    if errors:
        raise Refusal("partial Docker boundary cleanup failed: " + "; ".join(errors))


def create_docker_boundary(
    planned: DockerBoundary,
    *,
    context: CommandContext,
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
    lease: DockerBoundaryLease | None = None,
    after_toolcache: Callable[[], None] | None = None,
) -> DockerBoundary:
    """Create the tool cache, seed it, then the network, as one lease-tracked unit rolled back on failure."""
    if (
        planned.network_id is not None
        or planned.toolcache_owned
        or planned.toolcache_seeded
    ):
        raise Refusal("refusing to recreate an initialized Docker boundary")
    active_lease = lease or DockerBoundaryLease(planned)
    if (
        active_lease.boundary != planned
        or active_lease.complete
        or active_lease.released
    ):
        raise Refusal("Docker boundary lease was not initialized from the plan")
    require_act_job_volumes_absent(
        planned,
        context=context,
        docker_command=docker_command,
    )
    boundary = planned
    try:
        boundary = create_act_toolcache_volume(
            planned,
            context=context,
            docker_command=docker_command,
        )
        active_lease.boundary = boundary
        boundary = seed_act_toolcache_volume(
            boundary,
            context=context,
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
            context=context,
            description="isolated Docker network creation",
        )
        network_id = result.stdout.strip()
        if not DOCKER_ID_RE.fullmatch(network_id):
            raise Refusal("Docker returned an invalid boundary network ID")
        boundary = replace(boundary, network_id=network_id)
        active_lease.boundary = boundary
        gateway = inspect_docker_boundary(
            boundary,
            context=context,
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
                    context=context,
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
    context: CommandContext,
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
    cancel: threading.Event | None = None,
) -> list[dict[str, object]]:
    """Every container's inspect metadata, or an empty list once `cancel` is set."""
    if cancel is not None and cancel.is_set():
        return []
    listed = docker_command(
        ["container", "ls", "--all", "--quiet", "--no-trunc"],
        context=context,
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
            context=context,
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
    """The sorted IDs in `selected` whose state is Running."""
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
    context: CommandContext,
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
    observed_volumes: list[str] | None = None,
) -> int:
    """Stop and remove every container `boundary` owns and return how many there were; a survivor is a Refusal."""
    inventory = docker_container_inventory(
        context=context, docker_command=docker_command
    )
    owned = owned_container_ids(inventory, boundary)
    initial_count = len(owned)
    attempt_errors: list[str] = []
    mount_errors: list[str] = []
    if observed_volumes is not None:
        # Record act's job volumes while the containers that prove their
        # ownership still exist; removal below would orphan the names.
        try:
            observed_volumes.extend(owned_volume_mounts(inventory, owned))
        except Refusal as exc:
            mount_errors.append(str(exc))
    running = running_container_ids(inventory, owned)
    if running:
        try:
            result = docker_command(
                ["container", "stop", "--time", "3", *running],
                context=context,
                description="owned Docker container stop",
                check=False,
            )
            if result.returncode != 0:
                attempt_errors.append("graceful stop failed")
        except Refusal as exc:
            attempt_errors.append(str(exc))

    try:
        inventory = docker_container_inventory(
            context=context,
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
                context=context,
                description="owned Docker container removal",
                check=False,
            )
            if result.returncode != 0:
                attempt_errors.append("forced removal failed")
        except Refusal as exc:
            attempt_errors.append(str(exc))

    verification_errors: list[str] = list(mount_errors)
    try:
        final_inventory = docker_container_inventory(
            context=context,
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


def remove_boundary_network(
    boundary: DockerBoundary,
    observed_volumes: list[str],
    *,
    context: CommandContext,
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
) -> list[str]:
    """Stop this boundary's containers and remove its network; the problems found, in order.

    Teardown reports every failure rather than stopping at the first, so each
    step returns its complaints instead of raising them. `observed_volumes`
    collects the job-volume names the stopped containers were seen mounting,
    so the reconciliation that follows judges what was observed rather than
    what the daemon still lists.
    """
    errors: list[str] = []
    try:
        cleanup_owned_containers(
            boundary,
            context=context,
            docker_command=docker_command,
            observed_volumes=observed_volumes,
        )
    except Refusal as exc:
        errors.append(str(exc))
    try:
        inspect_docker_network(
            boundary,
            context=context,
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
                context=context,
                description="Docker boundary network removal",
                check=False,
            )
            if result.returncode != 0:
                errors.append("Docker boundary network removal failed")
        except Refusal as exc:
            errors.append(str(exc))
    return errors


def verify_boundary_name_released(
    boundary: DockerBoundary,
    *,
    context: CommandContext,
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
) -> list[str]:
    """Roll back a still-owned network and prove its NAME is free again; the problems found."""
    errors: list[str] = []
    try:
        discard_docker_network_if_owned(
            boundary,
            context=context,
            docker_command=docker_command,
        )
        name_check = docker_command(
            ["network", "inspect", boundary.name],
            context=context,
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
    return errors


def verify_boundary_network_absent(
    boundary: DockerBoundary,
    *,
    context: CommandContext,
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
) -> list[str]:
    """Prove the daemon no longer knows this boundary's network ID; the problems found."""
    errors: list[str] = []
    if boundary.network_id is None:
        return errors
    try:
        result = docker_command(
            ["network", "inspect", boundary.network_id],
            context=context,
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
    return errors


def verify_no_owned_containers(
    boundary: DockerBoundary,
    *,
    context: CommandContext,
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
) -> list[str]:
    """Prove no surviving container still carries this boundary's token; the problems found."""
    errors: list[str] = []
    try:
        final_inventory = docker_container_inventory(
            context=context,
            docker_command=docker_command,
        )
        survivors = owned_container_ids(final_inventory, boundary)
        if survivors:
            errors.append(f"{len(survivors)} owned container(s) remain")
    except Refusal as exc:
        errors.append(str(exc))
    return errors


def cleanup_docker_boundary(
    boundary: DockerBoundary,
    *,
    context: CommandContext,
    docker_command: Callable[..., subprocess.CompletedProcess[str]] = run_docker,
) -> None:
    """Remove containers, network, and tool cache, then prove each absent; every problem is one Refusal."""
    observed_volumes: list[str] = []
    errors = remove_boundary_network(
        boundary, observed_volumes, context=context, docker_command=docker_command
    )

    if docker_command is run_docker:
        errors += verify_boundary_name_released(
            boundary, context=context, docker_command=docker_command
        )

    try:
        cleanup_act_toolcache_volume(
            boundary,
            context=context,
            docker_command=docker_command,
        )
    except Refusal as exc:
        errors.append(str(exc))
    try:
        cleanup_act_job_volumes(
            boundary,
            observed_volumes,
            context=context,
            docker_command=docker_command,
        )
    except Refusal as exc:
        errors.append(str(exc))

    errors += verify_boundary_network_absent(
        boundary, context=context, docker_command=docker_command
    )
    errors += verify_no_owned_containers(
        boundary, context=context, docker_command=docker_command
    )
    if errors:
        raise Refusal("Docker boundary cleanup failed: " + "; ".join(errors))


@contextlib.contextmanager
def temporary_docker_boundary(
    planned: DockerBoundary,
    *,
    context: CommandContext,
) -> Iterator[DockerBoundary]:
    """Yield a created boundary and tear it down, partially or fully, on exit."""
    lease = DockerBoundaryLease(planned)
    try:
        create_docker_boundary(
            planned,
            context=context,
            lease=lease,
        )
        yield lease.boundary
    finally:
        if not lease.released:
            with blocked_cleanup_signals():
                if lease.complete:
                    cleanup_docker_boundary(
                        lease.boundary,
                        context=context,
                    )
                else:
                    cleanup_partial_docker_boundary(
                        lease.boundary,
                        context=context,
                    )
                lease.released = True


def act_prefix(act_binary: str, use_sudo: bool, env: Mapping[str, str]) -> list[str]:
    """The isolated command prefix for the act executable."""
    return isolated_command_prefix(act_binary, use_sudo, env)


def container_cpuset() -> str:
    """The `--cpuset-cpus` range one job container gets: `0-<n-1>` for n = min(host CPUs, CONTAINER_CPU_LIMIT)."""
    bound = min(os.cpu_count() or 1, CONTAINER_CPU_LIMIT)
    return f"0-{bound - 1}"


def build_act_command(
    prefix: Sequence[str],
    workflow: str,
    layout: RunLayout,
    artifact_port: int,
    boundary: DockerBoundary,
) -> list[str]:
    """The exact act command line for `workflow` inside `boundary`; an unfit boundary or port is a Refusal."""
    if not 1 <= artifact_port <= 65535:
        raise Refusal(f"invalid artifact-server port: {artifact_port}")
    if not boundary.toolcache_owned:
        raise Refusal("Docker boundary has no exclusive act tool-cache volume")
    if not boundary.toolcache_seeded:
        raise Refusal(
            "Docker boundary tool cache was never deterministically seeded; "
            "concurrent sibling jobs must not race the daemon copy-up"
        )
    if not boundary.job_volume_prefixes:
        raise Refusal("Docker boundary leases no act job-volume scope")
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
        "--action-offline-mode",
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
        "--concurrent-jobs",
        str(CONCURRENT_JOB_LIMIT),
        "--container-options",
        f"--label={DOCKER_OWNER_LABEL}={boundary.token} "
        f"--cpuset-cpus={container_cpuset()} "
        f"--memory={CONTAINER_MEMORY} --memory-swap={CONTAINER_MEMORY}",
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


@dataclass(frozen=True)
class ContainmentPolicy:
    """The signal ladder a stranded process group is walked down, and the seams around it.

    The default is the production ladder. One production site substitutes the
    escalation per call - the timeout path of run_tracked_process_group_command
    walks straight to SIGKILL - and the self-test substitutes fields to shorten
    the wait or to observe the walk.
    """

    escalation: Sequence[tuple[int, float]] = (
        (signal.SIGINT, 10),
        (signal.SIGTERM, 10),
        (signal.SIGKILL, 5),
    )
    group_exists: Callable[..., bool] | None = None
    signal_group: Callable[..., None] | None = None
    sleep: Callable[[float], None] = time.sleep
    recovery_notice: Callable[[str], None] | None = None


def terminate_act_process_group(
    process: subprocess.Popen[object],
    *,
    use_sudo: bool,
    primary: BaseException,
    policy: ContainmentPolicy = ContainmentPolicy(),
) -> None:
    """Escalate signals until the process group is provably gone, then reap its leader."""
    check_group = policy.group_exists or process_group_exists
    send_group_signal = policy.signal_group or signal_process_group
    sleep = policy.sleep
    notify_recovery = policy.recovery_notice or (
        lambda message: print(message, file=sys.stderr, flush=True)
    )
    group_absent = False
    for sent_signal, timeout in policy.escalation:
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


@dataclass(frozen=True)
class ProcessSeams:
    """The spawn and containment collaborators a process-group boundary calls through.

    The defaults are production; only the self-test replaces a field, and it
    replaces several at once, so they are one value rather than four keywords.
    """

    popen: Callable[..., subprocess.Popen[object]] = subprocess.Popen
    terminate_group: Callable[..., None] = terminate_act_process_group
    group_exists: Callable[..., bool] | None = None
    before_terminate_group: Callable[[], None] | None = None


def run_act_process(
    command: Sequence[str],
    *,
    context: CommandContext,
    check: bool = False,
    started: Callable[[int], None] | None = None,
    seams: ProcessSeams = ProcessSeams(),
) -> subprocess.CompletedProcess[object]:
    """Run act in its own process group and reap that group on interruption."""
    del check  # This boundary always returns the workflow status to its caller.
    popen = seams.popen
    terminate_group = seams.terminate_group
    group_exists = seams.group_exists
    before_terminate_group = seams.before_terminate_group
    process: subprocess.Popen[object] | None = None
    try:
        # Latch parent cleanup signals across fork/exec, Popen return, and
        # assignment. Caught dispositions reset on exec, so unlike a blocked
        # mask this does not prevent the act child receiving INT/TERM/HUP.
        with deferred_cleanup_signal_delivery():
            process = popen(
                command,
                cwd=context.cwd,
                env=dict(context.env),
                start_new_session=True,
            )
        if started is not None:
            started(process.pid)
        returncode = process.wait()
        check_group = group_exists or process_group_exists
        if check_group(process.pid, use_sudo=context.use_sudo):
            raise Refusal("act process group survived its leader")
        return subprocess.CompletedProcess(command, returncode)
    except BaseException as primary:
        if process is not None:
            if before_terminate_group is not None:
                before_terminate_group()
            with blocked_cleanup_signals():
                terminate_group(process, use_sudo=context.use_sudo, primary=primary)
        raise


def sudo_process_group_signal(
    process_group: int,
    sent_signal: int,
    *,
    run_command: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> subprocess.CompletedProcess[str]:
    """The result of `sudo kill -SIGNAL -- -PGID`; a timeout or launch error is a Refusal."""
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
    """Whether a failed privileged kill says the process group does not exist."""
    return result.returncode != 0 and "no such process" in result.stderr.lower()


def process_group_exists(
    process_group: int,
    *,
    use_sudo: bool,
    run_command: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    kill_group: Callable[[int, int], None] = os.killpg,
) -> bool:
    """Whether `process_group` still has a member; an unanswerable check is a Refusal."""
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
    """Send `sent_signal` to the whole group; a missing group is a ProcessLookupError."""
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
    context: CommandContext,
    timeout: float,
    seams: ProcessSeams = ProcessSeams(),
) -> subprocess.CompletedProcess[str]:
    """Run a host command without letting a sudo child outlive its CLI."""
    popen = seams.popen
    terminate_group = seams.terminate_group
    group_exists = seams.group_exists
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
                    cwd=context.cwd,
                    env=dict(context.env),
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
                cwd=context.cwd,
                env=dict(context.env),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True,
            )
        stdout, stderr = process.communicate(timeout=timeout)
        check_group = group_exists or process_group_exists
        if check_group(process.pid, use_sudo=context.use_sudo):
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
                        use_sudo=context.use_sudo,
                        primary=primary,
                        policy=ContainmentPolicy(escalation=((signal.SIGKILL, 5),)),
                    )
                else:
                    terminate_group(process, use_sudo=context.use_sudo, primary=primary)
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
    """The group's members once every one is stopped; a missed deadline is a Refusal."""
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
    """The act prefix once the audited act version and a reachable Docker daemon are proven."""
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
        context=CommandContext(use_sudo=use_sudo, cwd=layout.invocation, env=env),
        description="Docker daemon check",
    )
    return act_prefix(act_binary, use_sudo, env)


@dataclass(frozen=True)
class SpawnSeams:
    """The collaborators one act spawn calls through: the live-state query, the spawn, and the last gate.

    The defaults are production; the self-test and the workflow loop each
    replace one or two of them, so they travel as one value rather than three
    keywords threaded through every caller.
    """

    query: Callable[[int, str], PullRequest] = query_pull_request
    run_process: Callable[..., subprocess.CompletedProcess[object]] = run_act_process
    pre_spawn: Callable[[], None] | None = None


def execute_act_boundary(
    command: Sequence[str],
    *,
    run: ValidatedRun,
    context: CommandContext,
    integrity_check: Callable[[], None],
    seams: SpawnSeams = SpawnSeams(),
) -> int:
    """Bind one act process between fresh remote-state and byte checks.

    ``seams.pre_spawn`` runs after every other pre-spawn check and immediately
    before the process starts; the lease gate lives there so no round trip
    separates its inventory from act's first mount.
    """
    require_live_pull_request(run.pr, run.repository, seams.query)
    integrity_check()
    if seams.pre_spawn is not None:
        seams.pre_spawn()
    try:
        result = seams.run_process(
            command,
            context=replace(context, env=dict(context.env)),
            check=False,
        )
    except OSError as exc:
        raise Refusal(f"cannot start act: {exc}") from exc
    require_live_pull_request(run.pr, run.repository, seams.query)
    integrity_check()
    return result.returncode


@dataclass(frozen=True)
class WorkflowPlan:
    """What one validation run executes: the selection it came from, and how each workflow is launched.

    The five travel together from `run_validation` into the helpers it hoists,
    so a reader checks one value rather than five more keywords.
    """

    workflows: Sequence[str]
    candidate_worktree: pathlib.Path
    job_volume_scope: Mapping[str, str]
    prefix: Sequence[str]
    dry_run: bool


def check_run_integrity(
    run: ValidatedRun, layout: RunLayout, plan: WorkflowPlan
) -> None:
    """Re-verify the isolation layout and both checkouts."""
    validate_isolation_layout(layout)
    validate_checkout(
        run.pr, plan.candidate_worktree, plan.workflows, label="candidate worktree"
    )
    validate_checkout(
        run.pr, layout.checkout, plan.workflows, label="materialized checkout"
    )


def execute_workflows(
    run: ValidatedRun,
    layout: RunLayout,
    plan: WorkflowPlan,
    boundary: DockerBoundary,
    *,
    context: CommandContext,
) -> int:
    """Run each selected workflow inside `boundary`; RC_FAILED at the first failure."""
    pr = run.pr
    repository = run.repository

    def integrity_check() -> None:
        """Re-verify the isolation layout and both checkouts."""
        check_run_integrity(run, layout, plan)

    for workflow in plan.workflows:
        if plan.job_volume_scope[workflow] not in boundary.job_volume_prefixes:
            raise Refusal(
                f"Docker boundary does not lease the act job volumes "
                f"of {workflow}"
            )
        inspect_docker_boundary(
            boundary,
            context=context,
        )
        artifact_port = allocate_tcp_port()
        command = build_act_command(
            plan.prefix, workflow, layout, artifact_port, boundary
        )
        if plan.dry_run:
            print(f"act-ci: {workflow}: {shlex.join(command)}")
            continue
        print(
            f"act-ci: running {workflow} ({WORKFLOWS[workflow]})",
            flush=True,
        )

        def lease_gate() -> None:
            """The acquisition gate ran before a seed that can take
            minutes; prove the lease is still empty at the spawn."""
            require_act_job_volumes_absent(boundary, context=context)

        result = execute_act_boundary(
            command,
            run=run,
            context=context,
            integrity_check=integrity_check,
            seams=SpawnSeams(pre_spawn=lease_gate),
        )
        observed_volumes: list[str] = []
        leftovers = cleanup_owned_containers(
            boundary,
            context=context,
            observed_volumes=observed_volumes,
        )
        # Reconcile before refusing: drift observed on a leftover
        # container is reported here or never.
        leftover_volumes = cleanup_act_job_volumes(
            boundary,
            observed_volumes,
            context=context,
        )
        if leftovers or leftover_volumes:
            raise Refusal(
                f"act left {leftovers} owned container(s) and "
                f"{len(leftover_volumes)} job volume(s) after {workflow}; "
                "the runner removed them and refuses the run"
            )
        if result != 0:
            print(f"act-ci: {workflow}: FAILED ({result})", file=sys.stderr)
            return RC_FAILED
        print(f"act-ci: {workflow}: PASS at {pr.head_sha}")
    require_live_pull_request(pr, repository)
    integrity_check()
    return RC_OK


def run_validation(
    run: ValidatedRun,
    workflows: Sequence[str],
    candidate_worktree: pathlib.Path,
    *,
    act_binary: str,
    use_sudo: bool,
    dry_run: bool,
) -> int:
    """Materialize, verify, and run every selected workflow for `run`; RC_OK, RC_FAILED, or a Refusal."""
    pr = run.pr
    repository = run.repository
    with temporary_run_directory(use_sudo and not dry_run) as run_root:
        layout = make_layout(run_root, pr)
        materialize_remote_head(run, layout)
        validate_checkout(
            pr, candidate_worktree, workflows, label="candidate worktree"
        )
        validate_checkout(pr, layout.checkout, workflows, label="materialized checkout")
        validate_workflow_sandbox(layout.checkout, workflows)
        job_volume_scope = workflow_job_volume_scope(layout.checkout, workflows)
        initialize_required_submodules(layout.checkout, layout.home)
        validate_checkout(pr, layout.checkout, workflows, label="materialized checkout")
        require_live_pull_request(pr, repository)

        event = build_event(run)
        layout.event_path.write_text(
            json.dumps(event, indent=2) + "\n", encoding="utf-8"
        )
        env = controlled_act_environment(layout)
        context = CommandContext(use_sudo=use_sudo, cwd=layout.invocation, env=env)
        validate_isolation_layout(layout)
        prefix = (
            act_prefix(act_binary, use_sudo, env)
            if dry_run
            else require_runtime(act_binary, use_sudo, layout, env)
        )
        planned_boundary = new_docker_boundary(job_volume_scope.values())
        print(f"act-ci: PR #{pr.number} {event['action']} exact head {pr.head_sha}")
        print(
            f"act-ci: base {run.validation_base} (live {pr.base_ref} tip; "
            f"recorded base oid {pr.base_sha}), draft={str(pr.draft).lower()}"
        )
        print("act-ci: credentials=none docker-socket=none caches=ephemeral")
        materialize_workflow_actions(layout, workflows, dry_run=dry_run)
        plan = WorkflowPlan(
            workflows=workflows,
            candidate_worktree=candidate_worktree,
            job_volume_scope=job_volume_scope,
            prefix=prefix,
            dry_run=dry_run,
        )
        with temporary_docker_boundary(
            planned_boundary,
            context=context,
        ) as boundary:
            return execute_workflows(run, layout, plan, boundary, context=context)


def expect_refusal(label: str, action: Callable[[], object]) -> bool:
    """Print one arm line and return whether `action` raised Refusal."""
    try:
        action()
    except Refusal:
        print(f"  ok   {label}")
        return True
    print(f"  FAIL {label}")
    return False


class SelftestTally:
    """The running failure count behind the self-test's `check` and `refused` arms."""

    def __init__(self) -> None:
        self.failures = 0

    def check(self, label: str, condition: bool) -> None:
        """Print ok/FAIL for `label` and count a failure when `condition` is false."""
        print(f"  {'ok  ' if condition else 'FAIL'} {label}")
        self.failures += 0 if condition else 1

    def refused(self, label: str, action: Callable[[], object]) -> None:
        """Count a failure unless `action` raises Refusal."""
        self.failures += 0 if expect_refusal(label, action) else 1


@dataclass(frozen=True)
class SelftestFixture:
    """The synthetic pull request the offline arms share, and the SHAs it is built from."""

    base: str
    head: str
    repository: str
    raw: dict[str, object]
    pr: PullRequest
    live_tip: str


@dataclass(frozen=True)
class DockerFixture:
    """One self-test boundary with the fake daemon's fixed replies: metadata and not-found errors."""

    boundary: DockerBoundary
    layout: RunLayout
    context: CommandContext
    port: int
    volume_metadata: str
    missing_volume: str
    foreign_volume_metadata: str
    network_metadata: str
    missing_network: str
    missing_network_name: str
    seed_container_name: str
    seed_container_metadata: str
    missing_seed_container: str


@dataclass(frozen=True)
class GitFixture:
    """A scratch repository with one committed workflow at two commits, and how to drive it."""

    repo: pathlib.Path
    test_git: Callable[..., str]
    workflow_path: pathlib.Path
    workflow_text: str
    first_commit: str
    test_head: str
    test_pr: PullRequest


def selftest_fixture() -> SelftestFixture:
    """The validated fixture PR #268 and its SHAs."""
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
    return SelftestFixture(
        base=base,
        head=head,
        repository=repository,
        raw=raw,
        pr=pr,
        live_tip="3" * 40,
    )


def selftest_event_payload(
    tally: SelftestTally,
    fixture: SelftestFixture,
    fixture_run: ValidatedRun,
    draft_run: ValidatedRun,
) -> None:
    """Arms: the event payload for a ready and a draft PR."""
    check = tally.check
    base = fixture.base
    head = fixture.head
    event = build_event(fixture_run)
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

    draft_event = build_event(draft_run)
    check(
        "draft event uses synchronize and preserves draft=true",
        draft_event["action"] == "synchronize"
        and draft_event["pull_request"]["draft"] is True,
    )


def selftest_base_resolution(tally: SelftestTally, fixture: SelftestFixture) -> ValidatedRun:
    """Arms: resolving the live base tip against a stale and a matching recorded oid; the resolved run."""
    check = tally.check
    refused = tally.refused
    repository = fixture.repository
    pr = fixture.pr
    live_tip = fixture.live_tip
    noted: list[str] = []
    resolved = resolve_validation_base(
        pr, repository, query_tip=lambda _repo, _ref: live_tip, emit=noted.append
    )
    check(
        "a stale recorded base oid resolves to the live dev tip and proceeds",
        resolved.validation_base == live_tip
        and resolved.validation_base != pr.base_sha,
    )
    check(
        "the stale-base note prints the recorded and live base SHAs",
        len(noted) == 1
        and pr.base_sha in noted[0]
        and live_tip in noted[0]
        and "recorded base oid" in noted[0]
        and "stale" in noted[0],
    )
    matched: list[str] = []
    check(
        "a recorded base oid matching the live tip resolves unchanged",
        resolve_validation_base(
            pr,
            repository,
            query_tip=lambda _repo, _ref: pr.base_sha,
            emit=matched.append,
        ).validation_base
        == pr.base_sha
        and len(matched) == 1
        and "matches the recorded base oid" in matched[0],
    )
    refused(
        "an invalid live-tip lookup result is refused",
        lambda: resolve_validation_base(
            pr, repository, query_tip=lambda _repo, _ref: "not-a-sha"
        ),
    )
    return resolved


def selftest_fetch_window(
    tally: SelftestTally,
    fixture: SelftestFixture,
    resolved: ValidatedRun,
) -> None:
    """Arms: the fetch-time ref equality and the recorded oid in the event payload."""
    check = tally.check
    head = fixture.head
    pr = fixture.pr
    live_tip = fixture.live_tip
    def fetch_window_message(fetched_base: str, fetched_head: str) -> str | None:
        """The refusal text for the fetched pair, or None when it is accepted."""
        try:
            require_exact_fetched_refs(resolved, fetched_base, fetched_head)
        except Refusal as exc:
            return str(exc)
        return None

    check(
        "a stale recorded base with a moved dev passes the fetch equality "
        "check against the resolved live tip",
        fetch_window_message(live_tip, head) is None,
    )
    moved_head = "4" * 40
    head_message = fetch_window_message(live_tip, moved_head)
    check(
        "a head moved between metadata lookup and fetch is refused naming "
        "the head",
        head_message is not None
        and "head" in head_message
        and head in head_message
        and moved_head in head_message,
    )
    window_tip = "5" * 40
    base_message = fetch_window_message(window_tip, head)
    check(
        "dev moving between the invocation-time resolve and the fetch is "
        "refused naming both base SHAs",
        base_message is not None
        and resolved.validation_base in base_message
        and window_tip in base_message
        and "resolve" in base_message,
    )
    stale_event = build_event(resolved)
    stale_event_pr = stale_event["pull_request"]
    assert isinstance(stale_event_pr, dict)
    #: [R3] on PR #336: the payload feeds scope classification and nothing
    #: else, and hosted receives the RECORDED oid, so the replica must too or
    #: its verdict stops predicting the run it stands in for. The trust
    #: checks read resolved.validation_base and never this payload, so the
    #: two arms below pin the split in both directions.
    check(
        "the event carries the recorded base oid, so the local replica "
        "classifies the same file set hosted does",
        stale_event_pr["base"]["sha"] == pr.base_sha,
    )
    check(
        "and that is not the validation base, so the payload cannot be "
        "mistaken for the commit the trust checks read",
        stale_event_pr["base"]["sha"] != resolved.validation_base,
    )


def materialize_for_transcript(
    _run: ValidatedRun, layout: RunLayout
) -> pathlib.Path:
    """A materialization stand-in that writes only the workflow headers the lease reads."""
    # The real job-volume lease reads the declared workflow name from
    # this checkout, so materialize the selected workflow's header.
    for alias in ("docs", "elaborate"):
        transcript_workflow = layout.checkout / WORKFLOWS[alias]
        transcript_workflow.parent.mkdir(parents=True, exist_ok=True)
        transcript_workflow.write_text(
            f"name: {alias}\non: pull_request\njobs:\n  check:\n"
            "    runs-on: ubuntu-latest\n    steps:\n      - run: true\n",
            encoding="utf-8",
        )
    return layout.checkout


def selftest_validation_transcript(
    tally: SelftestTally,
    fixture: SelftestFixture,
    resolved: ValidatedRun,
    shipping_root: pathlib.Path,
) -> None:
    """Arm: the ordinary validation path prints the resolved base and enters its Docker boundary."""
    check = tally.check
    pr = fixture.pr
    #: The ordinary PR path used to reach its status transcript with an
    #: unbound ``validation_base`` name while all construction-only arms
    #: stayed green (#340). Drive run_validation through that transcript and
    #: into the Docker-boundary context without touching Git, Docker, or act.
    dry_boundaries: list[DockerBoundary] = []


    @contextlib.contextmanager
    def dry_boundary(
        planned: DockerBoundary, **_kwargs: object
    ) -> Iterator[DockerBoundary]:
        """A boundary stand-in that records the fully populated boundary it yields."""
        active = replace(
            planned,
            network_id="a" * 64,
            gateway="172.18.0.1",
            toolcache_owned=True,
            toolcache_seeded=True,
        )
        dry_boundaries.append(active)
        yield active

    transcript = io.StringIO()
    transcript_error: Exception | None = None
    transcript_rc: int | None = None
    with mock.patch.multiple(
        sys.modules[__name__],
        materialize_remote_head=materialize_for_transcript,
        validate_checkout=lambda *_args, **_kwargs: None,
        validate_workflow_sandbox=lambda *_args, **_kwargs: None,
        initialize_required_submodules=lambda *_args, **_kwargs: None,
        require_live_pull_request=lambda *_args, **_kwargs: None,
        inspect_docker_boundary=lambda *_args, **_kwargs: None,
        temporary_docker_boundary=dry_boundary,
        allocate_tcp_port=lambda: 43210,
    ):
        try:
            with contextlib.redirect_stdout(transcript):
                transcript_rc = run_validation(
                    resolved,
                    ("docs",),
                    shipping_root,
                    act_binary="/trusted/act",
                    use_sudo=False,
                    dry_run=True,
                )
        except Exception as exc:  # the result is graded below
            transcript_error = exc
    expected_base_line = (
        f"act-ci: base {resolved.validation_base} (live {pr.base_ref} tip; "
        f"recorded base oid {pr.base_sha}), draft=false"
    )
    check(
        "the normal validation path prints the resolved base and enters its "
        "Docker boundary",
        transcript_error is None
        and transcript_rc == RC_OK
        and expected_base_line in transcript.getvalue().splitlines()
        and len(dry_boundaries) == 1
        and "act-ci: docs:" in transcript.getvalue(),
    )
    check(
        "the normal validation path leases the selected workflow's act job volumes",
        len(dry_boundaries) == 1
        and dry_boundaries[0].job_volume_prefixes == ("act-docs-",),
    )
    check(
        "dry-run prints the job bound and the bounded container options as "
        "one quoted argv word",
        f" --concurrent-jobs {CONCURRENT_JOB_LIMIT} --container-options "
        f"'--label={DOCKER_OWNER_LABEL}="
        in transcript.getvalue()
        and f" --cpuset-cpus={container_cpuset()} --memory={CONTAINER_MEMORY}"
        f" --memory-swap={CONTAINER_MEMORY}'" in transcript.getvalue(),
    )



def workflow_control_fakes(
    resolved: ValidatedRun,
    log: list[tuple[str, ...]],
    boundaries: list[DockerBoundary],
    *,
    leased_prefixes: tuple[str, ...] | None,
    leftover_containers: int,
    leftover_volumes: Sequence[str],
) -> dict[str, object]:
    """The fakes one run_validation control patches in: act, Docker, GitHub, gate."""
    real_execute = execute_act_boundary

    @contextlib.contextmanager
    def leased_boundary(
        planned: DockerBoundary, **_kwargs: object
    ) -> Iterator[DockerBoundary]:
        """Yield the planned boundary as acquired, optionally under another lease."""
        active = replace(
            planned,
            network_id="a" * 64,
            gateway="172.18.0.1",
            toolcache_owned=True,
            toolcache_seeded=True,
            job_volume_prefixes=(
                planned.job_volume_prefixes
                if leased_prefixes is None
                else leased_prefixes
            ),
        )
        boundaries.append(active)
        yield active

    def spawn(
        command: Sequence[str], **_kwargs: object
    ) -> subprocess.CompletedProcess[object]:
        """Record the act spawn in place of a real process."""
        workflow_file = command[command.index("--workflows") + 1]
        log.append(("spawn", workflow_file.rsplit("/", 1)[-1]))
        return subprocess.CompletedProcess(list(command), 0)

    def execute(command: Sequence[str], **kwargs: object) -> int:
        """The real spawn boundary with the spawn and the GitHub query faked."""
        seams = kwargs.pop("seams", SpawnSeams())
        assert isinstance(seams, SpawnSeams)
        return real_execute(
            command,
            seams=replace(
                seams, run_process=spawn, query=lambda *_args: resolved.pr
            ),
            **kwargs,
        )

    def containers(
        boundary: DockerBoundary,
        *,
        observed_volumes: list[str] | None = None,
        **_kwargs: object,
    ) -> int:
        """Record container cleanup and hand one observed volume onward."""
        log.append(("containers",))
        if observed_volumes is not None:
            observed_volumes.append(
                f"{boundary.job_volume_prefixes[0]}observed-" + "0" * 64
            )
        return leftover_containers

    def volumes(
        _boundary: DockerBoundary, observed: Sequence[str], **_kwargs: object
    ) -> list[str]:
        """Record volume reconciliation with what it was handed."""
        log.append(("volumes", *observed))
        return list(leftover_volumes)

    return {
        "materialize_remote_head": materialize_for_transcript,
        "validate_checkout": lambda *_args, **_kwargs: None,
        "validate_workflow_sandbox": lambda *_args, **_kwargs: None,
        "initialize_required_submodules": lambda *_args, **_kwargs: None,
        "require_live_pull_request": lambda *_args, **_kwargs: None,
        "require_runtime": lambda *_args, **_kwargs: ["act"],
        "inspect_docker_boundary": lambda *_args, **_kwargs: None,
        "temporary_docker_boundary": leased_boundary,
        "allocate_tcp_port": lambda: 43210,
        "require_act_job_volumes_absent": lambda *_args, **_kwargs: log.append(
            ("gate",)
        ),
        "execute_act_boundary": execute,
        "cleanup_owned_containers": containers,
        "cleanup_act_job_volumes": volumes,
    }



def run_workflow_control(
    resolved: ValidatedRun,
    shipping_root: pathlib.Path,
    *,
    leftover_volumes: Sequence[str],
    leftover_containers: int = 0,
    leased_prefixes: tuple[str, ...] | None = None,
) -> tuple[int | None, str, str, list[tuple[str, ...]], tuple[str, ...]]:
    """Drive execute_workflows through the real spawn boundary.

    Every faked call lands in one ordered log so the gate-before-spawn and
    containers-before-volumes orders are measured, not assumed.
    """
    log: list[tuple[str, ...]] = []
    boundaries: list[DockerBoundary] = []
    output = io.StringIO()
    message = ""
    rc: int | None = None
    with mock.patch.multiple(
        sys.modules[__name__],
        **workflow_control_fakes(
            resolved,
            log,
            boundaries,
            leased_prefixes=leased_prefixes,
            leftover_containers=leftover_containers,
            leftover_volumes=leftover_volumes,
        ),
    ):
        try:
            with contextlib.redirect_stdout(output):
                rc = run_validation(
                    resolved,
                    ("docs", "elaborate"),
                    shipping_root,
                    act_binary="/trusted/act",
                    use_sudo=False,
                    dry_run=False,
                )
        except Refusal as exc:
            message = str(exc)
    leased = tuple(boundaries[0].job_volume_prefixes) if boundaries else ()
    return rc, message, output.getvalue(), log, leased



def selftest_workflow_order(
    tally: SelftestTally,
    resolved: ValidatedRun,
    shipping_root: pathlib.Path,
) -> None:
    """Arms: each workflow gates, spawns, cleans containers, then reconciles its own job volumes."""
    check = tally.check
    clean_rc, clean_message, clean_output, clean_log, clean_leased = (
        run_workflow_control(
            resolved, shipping_root, leftover_volumes=()
        )
    )
    ordered = ["gate", "spawn", "containers", "volumes"]
    check(
        "a two-workflow run leases both, and gates, spawns, cleans containers, "
        "then reconciles volumes, once per workflow in that order",
        clean_rc == RC_OK
        and clean_message == ""
        and "act-ci: docs: PASS" in clean_output
        and "act-ci: elaborate: PASS" in clean_output
        and [entry[0] for entry in clean_log] == ordered + ordered
        and clean_log[1] == ("spawn", "docs.yml")
        and clean_log[5] == ("spawn", "elaborate.yml")
        and clean_leased == ("act-docs-", "act-elaborate-"),
    )
    check(
        "volumes observed on a workflow's containers reach that workflow's "
        "reconciliation",
        len(clean_log) == 8
        and clean_log[3] == ("volumes", "act-docs-observed-" + "0" * 64)
        and clean_log[7] == ("volumes", "act-docs-observed-" + "0" * 64),
    )
    leftover_rc, leftover_message, _leftover_output, _leftover_log, _l = (
        run_workflow_control(
            resolved,
            shipping_root,
            leftover_volumes=("act-docs-check-" + "0" * 64,),
        )
    )
    check(
        "a job volume act left after a workflow refuses the run after removal",
        leftover_rc is None
        and "job volume(s) after docs" in leftover_message
        and "refuses the run" in leftover_message,
    )
    stranded_rc, stranded_message, _stranded_output, stranded_log, _s = (
        run_workflow_control(
            resolved, shipping_root, leftover_volumes=(), leftover_containers=1
        )
    )
    check(
        "a leftover container refuses the run only after that workflow's "
        "volumes were reconciled",
        stranded_rc is None
        and "owned container(s)" in stranded_message
        and [entry[0] for entry in stranded_log] == ordered,
    )
    unleased_rc, unleased_message, _unleased_output, unleased_log, _u = (
        run_workflow_control(
            resolved,
            shipping_root,
            leftover_volumes=(),
            leased_prefixes=("act-other-",),
        )
    )
    check(
        "a boundary that does not lease the selected workflow refuses before act",
        unleased_rc is None
        and "does not lease the act job volumes of docs" in unleased_message
        and not any(entry[0] == "spawn" for entry in unleased_log),
    )


def trusted_runner_message(
    resolved: ValidatedRun,
    worktree_head: str,
    dirty: str = "",
    replacements: str = "",
) -> tuple[str | None, list[tuple[pathlib.Path, str, str]]]:
    """(refusal text or None, recorded collaborator calls) for one trusted-worktree state."""
    #: every collaborator argument is recorded, not just some: [R2] on
    #: PR #336 found that capturing only the commit let a mutation swap
    #: the ROOT and stay green, and [R3] found the same defect one
    #: argument to the right - the file whose bytes are verified was
    #: discarded, so verifying README.md instead of the runner itself
    #: kept this arm green.
    seen: list[tuple[pathlib.Path, str, str]] = []
    roots: list[pathlib.Path] = []
    try:
        validate_trusted_runner(
            resolved,
            state=lambda root: (
                roots.append(root),
                (worktree_head, dirty, replacements),
            )[1],
            verify_bytes=lambda root, commit, rel: seen.append(
                (root, commit, rel)
            ),
        )
    except Refusal as exc:
        return str(exc), seen
    return None, seen + [(root, "state", "state") for root in roots]


def selftest_trusted_runner(
    tally: SelftestTally,
    fixture: SelftestFixture,
    resolved: ValidatedRun,
) -> None:
    """Arms: the trusted worktree is compared to the live tip, with dirty and replaced states refused first."""
    check = tally.check
    pr = fixture.pr
    #: [R1] on PR #336: the trusted-worktree comparison is the lane's
    #: load-bearing change and was asserted by nothing - the live proof runs
    #: the audited-install path, which skips it entirely. These arms drive it
    #: with both collaborators injected, so a revert to the recorded oid is
    #: red in both directions.
    accepted, verified = trusted_runner_message(resolved, resolved.validation_base)
    installed_runner_relative = (
        pathlib.Path(__file__).resolve().relative_to(ROOT).as_posix()
    )
    check(
        "a trusted worktree at the live tip is accepted while the recorded "
        "base oid is stale",
        accepted is None,
    )
    check(
        "the runner's own bytes - that file, in the trusted root, at the "
        "validation base and not the recorded oid - are what is verified",
        verified
        == [
            (ROOT, resolved.validation_base, installed_runner_relative),
            (ROOT, "state", "state"),
        ],
    )
    stale_worktree, _ = trusted_runner_message(resolved, pr.base_sha)
    check(
        "a trusted worktree at the stale recorded base is refused naming the "
        "loaded head and the live tip",
        stale_worktree is not None
        and pr.base_sha in stale_worktree
        and resolved.validation_base in stale_worktree
        and "live" in stale_worktree,
    )
    #: [R3] on PR #336: the precedence arms below used a fixture head that
    #: already EQUALLED the validation base, so the base branch could not
    #: fire whatever the order was, and `refused` passes on any Refusal.
    #: Both now drive a head that differs and name the check that must win.
    dirty_message, dirty_verified = trusted_runner_message(
        resolved, pr.base_sha, dirty="M scripts/act_ci.py"
    )
    check(
        "a dirty trusted worktree is refused for being dirty, before the "
        "base comparison and before any bytes are read",
        dirty_message is not None
        and "dirty" in dirty_message
        and resolved.validation_base not in dirty_message
        and dirty_verified == [],
    )
    replaced_message, replaced_verified = trusted_runner_message(
        resolved, pr.base_sha, replacements="refs/replace/deadbeef"
    )
    check(
        "a trusted worktree carrying replacement refs is refused for those, "
        "before the base comparison and before any bytes are read",
        replaced_message is not None
        and "replacement refs" in replaced_message
        and resolved.validation_base not in replaced_message
        and replaced_verified == [],
    )
    #: the resolve targets refs/heads/<pr.base_ref> while the fetch targets
    #: the refs/heads/<DEFAULT_BASE> constant ([R1] on PR #336). They are one
    #: ref only because validate_pull_request pins the base ref, so the
    #: coupling is pinned rather than left as prose. Scope, stated exactly
    #: ([R2] measured it): this arm fires when DEFAULT_BASE itself moves; the
    #: other half - a WIDENED accept-set in validate_pull_request - is caught
    #: by the "non-dev pull request is refused" arm below. Between them the
    #: two targets cannot diverge silently.
    check(
        "the fixture's validated base ref is the constant the fetch targets, "
        "so the resolve and the fetch name one ref",
        pr.base_ref == DEFAULT_BASE == "dev",
    )


def selftest_wiring_pins(tally: SelftestTally) -> None:
    """Arms: one production ValidatedRun construction, and the real collaborators as defaults."""
    check = tally.check
    #: [R2] F8/F10 on PR #336 asked who HANDS each consumer the base, because
    #: reverting one call site reinstated #292 with the suite green. That was
    #: answered by reading the call sites, and [R3] then drove an ordinary
    #: pass-through helper through the reader: its parameter merely shared the
    #: audited name, so every site still "looked" wired while the frozen oid
    #: flowed. The question is now unaskable instead of re-answered - there is
    #: no base argument - and what remains checkable is the construction.
    constructors = base_construction_report(inspect.getsource(sys.modules[__name__]))
    check(
        "production constructs the validated run exactly once, in the "
        "audited resolve, so no second construction can bind the recorded "
        "oid as the validation base",
        constructors == ["resolve_validation_base"],
    )
    #: [R3] on PR #336: the injected collaborators are the runner's own trust
    #: checks, and nothing pinned their production defaults - a one-line
    #: default swap made validate_trusted_runner verify nothing, and made the
    #: "live remote tip" a local rev-parse, with every arm green. They are
    #: keyword-only so a call site cannot fill them positionally either.
    check(
        "the trusted-runner check defaults to reading the real checkout "
        "state and verifying real bytes",
        validate_trusted_runner.__kwdefaults__
        == {"state": checkout_state, "verify_bytes": validate_file_bytes},
    )
    check(
        "the resolve defaults to the real remote lookup and a flushed note",
        resolve_validation_base.__kwdefaults__
        == {"query_tip": query_remote_base_tip, "emit": emit_flushed},
    )


def selftest_remote_tip_lookup(tally: SelftestTally, fixture: SelftestFixture) -> None:
    """Arms: the resolve re-checks its inputs, and ls-remote replies are parsed by exact ref."""
    check = tally.check
    refused = tally.refused
    head = fixture.head
    repository = fixture.repository
    raw = fixture.raw
    pr = fixture.pr
    live_tip = fixture.live_tip
    refused(
        "the resolve re-checks the repository name it interpolates, rather "
        "than inheriting the check from main's ordering",
        lambda: resolve_validation_base(
            pr, "not a repo", query_tip=lambda _repo, _ref: live_tip
        ),
    )
    off_base = PullRequest.from_json({**raw, "baseRefName": "main"})
    refused(
        "and re-checks the base ref it interpolates, for the same reason",
        lambda: resolve_validation_base(
            off_base, repository, query_tip=lambda _repo, _ref: live_tip
        ),
    )

    #: [R1] F2: the lookup parses REMOTE-CONTROLLED bytes; its two refusals
    #: were unarmed because every arm above injects query_tip.
    check(
        "a well-formed ls-remote reply yields the tip",
        parse_ls_remote_tip(f"{live_tip}\trefs/heads/dev\n", "dev") == live_tip,
    )
    refused(
        "an ls-remote reply naming no ref is refused",
        lambda: parse_ls_remote_tip("", "dev"),
    )
    refused(
        "an ls-remote reply naming another ref is refused",
        lambda: parse_ls_remote_tip(f"{live_tip}\trefs/heads/main\n", "dev"),
    )
    #: [R3] on PR #336: `git ls-remote <url> refs/heads/dev` matches the
    #: pattern against each ref's TAIL, so the reply carries refs nobody
    #: asked for and a line count refuses them all. Verified on git 2.55.0:
    #: `git tag refs/heads/dev` is enough. The first arm is the regression -
    #: an unrelated tail match must be IGNORED, not fatal - and the second
    #: keeps the ambiguity that actually matters fatal.
    check(
        "a ref merely ending in the wanted name is ignored, so one pushed "
        "branch or tag cannot refuse every run of the gate",
        parse_ls_remote_tip(
            f"{live_tip}\trefs/heads/dev\n{head}\trefs/tags/refs/heads/dev\n",
            "dev",
        )
        == live_tip,
    )
    refused(
        "an ls-remote reply carrying the wanted ref twice is refused",
        lambda: parse_ls_remote_tip(
            f"{live_tip}\trefs/heads/dev\n{head}\trefs/heads/dev\n", "dev"
        ),
    )
    refused(
        "an ls-remote reply line carrying no ref at all is refused",
        lambda: parse_ls_remote_tip(f"{live_tip} refs/heads/dev\n", "dev"),
    )


def selftest_selection_and_metadata(tally: SelftestTally, fixture: SelftestFixture) -> None:
    """Arms: workflow selection, and the pull-request states and metadata that are refused."""
    check = tally.check
    refused = tally.refused
    repository = fixture.repository
    raw = fixture.raw
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


def docker_completed(
    arguments: Sequence[str],
    returncode: int = 0,
    stdout: str = "",
    stderr: str = "",
) -> subprocess.CompletedProcess[str]:
    """A completed Docker result for `arguments`."""
    return subprocess.CompletedProcess(
        list(arguments), returncode, stdout, stderr
    )


def selftest_docker_fixture(layout: RunLayout) -> DockerFixture:
    """A fully populated boundary for `layout`, a free port, and the fake daemon's replies about it."""
    allocated_port = allocate_tcp_port()
    selftest_boundary = DockerBoundary(
        token="a" * 32,
        name=f"milan-act-ci-{'a' * 32}",
        network_id="b" * 64,
        gateway="172.30.0.1",
        toolcache_owned=True,
        toolcache_seeded=True,
        job_volume_prefixes=("act-docs-", "act-rtl-full-"),
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

    missing_volume = (
        f"Error response from daemon: No such volume: "
        f"{ACT_TOOLCACHE_VOLUME}"
    )
    foreign_volume_metadata = volume_metadata.replace(
        selftest_boundary.token, "f" * 32
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
    seed_container_name = toolcache_seed_container_name(selftest_boundary)
    seed_container_metadata = json.dumps(
        [
            {
                "Id": "ab" * 32,
                "Name": f"/{seed_container_name}",
                "Config": {
                    "Labels": {
                        DOCKER_OWNER_LABEL: selftest_boundary.token,
                    },
                },
            }
        ]
    )
    missing_seed_container = (
        f"Error response from daemon: No such container: "
        f"{seed_container_name}"
    )
    return DockerFixture(
        boundary=selftest_boundary,
        layout=layout,
        context=CommandContext(use_sudo=False, cwd=layout.invocation, env={}),
        port=allocated_port,
        volume_metadata=volume_metadata,
        missing_volume=missing_volume,
        foreign_volume_metadata=foreign_volume_metadata,
        network_metadata=network_metadata,
        missing_network=missing_network,
        missing_network_name=missing_network_name,
        seed_container_name=seed_container_name,
        seed_container_metadata=seed_container_metadata,
        missing_seed_container=missing_seed_container,
    )


def selftest_act_command(tally: SelftestTally, docker: DockerFixture) -> None:
    """Arms: the act command line isolates the job and binds its servers to the bridge gateway."""
    check = tally.check
    selftest_boundary = docker.boundary
    first = docker.layout
    allocated_port = docker.port
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
        "job container options are one argv word: the ownership label, the "
        "CPU set, then the memory and swap limits",
        command.count("--container-options") == 1
        and command[command.index("--container-options") + 1]
        == f"--label={DOCKER_OWNER_LABEL}={selftest_boundary.token} "
        f"--cpuset-cpus={container_cpuset()} "
        f"--memory={CONTAINER_MEMORY} --memory-swap={CONTAINER_MEMORY}",
    )
    #: Hosted jobs each get their own runner; a replica's jobs share one
    #: host, so act starts at most CONCURRENT_JOB_LIMIT of a stage's jobs.
    #: Below one, act falls back to one job per host CPU.
    check(
        f"act starts at most {CONCURRENT_JOB_LIMIT} jobs of a stage at once, "
        "stated exactly once",
        command.count("--concurrent-jobs") == 1
        and command[command.index("--concurrent-jobs") + 1]
        == str(CONCURRENT_JOB_LIMIT)
        and CONCURRENT_JOB_LIMIT >= 1,
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
    #: #337: every job reads the cache the runner populated before act
    #: started; without this flag act fetches and checks out each action
    #: from whichever sibling reaches it first while the others copy it.
    check(
        "act reads the pre-populated per-head action cache offline, exactly once",
        command.count("--action-offline-mode") == 1
        and command[command.index("--action-cache-path") + 1]
        == str(first.action_cache),
    )


def selftest_container_cpu_bound(tally: SelftestTally, docker: DockerFixture) -> None:
    """Arms: the job container's cpuset is bounded by CONTAINER_CPU_LIMIT and keeps the ownership label."""
    check = tally.check
    selftest_boundary = docker.boundary
    cpuset_re = re.compile(r"^--cpuset-cpus=0-(\d+)$")

    def cpuset_words(host_cpus: int | None) -> list[str]:
        """The cpuset words of a command built on a host reporting `host_cpus`."""
        with mock.patch.object(os, "cpu_count", return_value=host_cpus):
            command = build_act_command(
                ["act"], "rtl-fast", docker.layout, docker.port, selftest_boundary
            )
        words = shlex.split(command[command.index("--container-options") + 1])
        return [word for word in words if word.startswith("--cpuset-cpus=")]

    def bound_of(host_cpus: int | None) -> int | None:
        """The CPU count a `0-<n-1>` cpuset word encodes, or None when the word is malformed."""
        words = cpuset_words(host_cpus)
        match = cpuset_re.match(words[0]) if len(words) == 1 else None
        return int(match.group(1)) + 1 if match else None

    #: rtl-fast's ``make -j"$(nproc)"`` Verilator build ran 128 compilers
    #: inside an unbounded container on a 128-vCPU host and exhausted its
    #: memory; hosted runners have 4 vCPUs. ``nproc`` follows the cpuset.
    check(
        "job containers get a cpuset of 0-<n-1> for n = min(host CPUs, "
        f"{CONTAINER_CPU_LIMIT})",
        bound_of(128) == CONTAINER_CPU_LIMIT
        and bound_of(CONTAINER_CPU_LIMIT + 1) == CONTAINER_CPU_LIMIT
        and bound_of(4) == 4
        and bound_of(1) == 1
        and bound_of(None) == 1
        and bound_of(os.cpu_count())
        == min(os.cpu_count() or 1, CONTAINER_CPU_LIMIT),
    )
    label_command = build_act_command(
        ["act"], "rtl-fast", docker.layout, docker.port, selftest_boundary
    )
    option_words = shlex.split(
        label_command[label_command.index("--container-options") + 1]
    )
    check(
        "the CPU bound leaves the unpredictable ownership label in the same "
        "container options word",
        option_words[0] == f"--label={DOCKER_OWNER_LABEL}={selftest_boundary.token}"
        and option_words[1] == f"--cpuset-cpus={container_cpuset()}"
        and "--privileged" not in label_command,
    )


def selftest_container_memory_bound(tally: SelftestTally, docker: DockerFixture) -> None:
    """Arms: job containers are held to CONTAINER_MEMORY, swap included, in a word of exactly four bounded tokens."""
    check = tally.check
    selftest_boundary = docker.boundary
    command = build_act_command(
        ["act"], "rtl-full", docker.layout, docker.port, selftest_boundary
    )
    option_words = shlex.split(command[command.index("--container-options") + 1])
    memory_words = [word for word in option_words if word.startswith("--memory=")]
    swap_words = [word for word in option_words if word.startswith("--memory-swap=")]
    #: Hosted ``ubuntu-latest`` runners have 16 GB: a job that needs more
    #: fails hosted too, and a bounded container fails the replica instead
    #: of the host. Swap equal to memory is Docker for "no swap beyond it".
    check(
        f"job containers are held to {CONTAINER_MEMORY} of memory and the "
        "same swap ceiling, one limit each, in Docker size syntax",
        memory_words == [f"--memory={CONTAINER_MEMORY}"]
        and swap_words == [f"--memory-swap={CONTAINER_MEMORY}"]
        and re.fullmatch(r"[1-9][0-9]*[kmg]", CONTAINER_MEMORY) is not None,
    )
    check(
        "the container options word splits into exactly four tokens: label, "
        "cpuset, memory, memory-swap, in that order",
        option_words
        == [
            f"--label={DOCKER_OWNER_LABEL}={selftest_boundary.token}",
            f"--cpuset-cpus={container_cpuset()}",
            f"--memory={CONTAINER_MEMORY}",
            f"--memory-swap={CONTAINER_MEMORY}",
        ],
    )


def selftest_act_command_refusals(tally: SelftestTally, docker: DockerFixture) -> None:
    """Arms: an unfit port or boundary cannot produce an act command."""
    refused = tally.refused
    selftest_boundary = docker.boundary
    first = docker.layout
    allocated_port = docker.port
    refused(
        "a boundary without a job-volume lease cannot build an act command",
        lambda: build_act_command(
            ["act"],
            "rtl-full",
            first,
            allocated_port,
            replace(selftest_boundary, job_volume_prefixes=()),
        ),
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
    refused(
        "a boundary with an unseeded tool cache cannot run act",
        lambda: build_act_command(
            ["act"],
            "docs",
            first,
            allocated_port,
            replace(selftest_boundary, toolcache_seeded=False),
        ),
    )


ACTION_FIXTURE_WORKFLOW = (
    "name: actions\non: push\njobs:\n  use:\n    runs-on: ubuntu-latest\n"
    "    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/cache@v4\n"
    "      - uses: actions/checkout@v4\n"
)


def recording_git(calls: list[tuple[list[str], object]]) -> Callable[..., str]:
    """A git stand-in that appends (argv, env) to `calls` and answers every rev-parse with one SHA."""

    def run(command: Sequence[str], **kwargs: object) -> str:
        """Record the call; a rev-parse resolves, everything else succeeds silently."""
        calls.append((list(command), kwargs.get("env")))
        return "c" * 40 if "rev-parse" in command else ""

    return run


def selftest_action_materialisation(tally: SelftestTally, docker: DockerFixture) -> None:
    """Arms: the collector, act's directory naming, the resolve order, and the credential-free clone argv."""
    check = tally.check
    refused = tally.refused
    first = docker.layout
    fixture_root = first.temporary / "action-fixture"
    fixture_root.mkdir()
    (fixture_root / "mixed.yml").write_text(
        "name: mixed\non: push\njobs:\n"
        "  one:\n    runs-on: ubuntu-latest\n    steps:\n"
        "      - uses: owner/repo@v1\n      - uses: owner/repo/sub@v1\n"
        "      - uses: ./local\n      - uses: docker://alpine:3.20\n      - run: true\n"
        "  two:\n    runs-on: ubuntu-latest\n    steps:\n"
        "      - uses: owner/repo@v1\n      - uses: actions/cache@v4\n",
        encoding="utf-8",
    )
    collected = collect_workflow_actions(fixture_root, ("mixed.yml",))
    check(
        "the collector yields each remote action once, sorted, skipping local and "
        "docker:// steps",
        tuple(action.spec for action in collected)
        == ("actions/cache@v4", "owner/repo/sub@v1", "owner/repo@v1"),
    )
    cache = collected[0]
    check(
        "an action is cloned into the directory act 0.2.89 derives from its uses: "
        "string, from act's exact clone URL",
        action_cache_directory(first, cache) == first.action_cache / "actions-cache@v4"
        and action_cache_directory(first, collected[1])
        == first.action_cache / "owner-repo-sub@v1"
        and cache.clone_url == "https://github.com/actions/cache",
    )
    refused(
        "a uses: string that is neither local, docker://, nor owner/repo@ref is refused",
        lambda: parse_action_reference("actions/cache"),
    )
    calls: list[tuple[list[str], object]] = []
    commit = materialize_action(first, cache, recording_git(calls))
    argv = [command for command, _env in calls]
    directory = str(first.action_cache / "actions-cache@v4")
    check(
        "the clone is a full credential-free HTTPS clone, a tag-first resolve, then "
        "a detached checkout of the resolved SHA",
        len(argv) == 3
        and argv[0][-4:] == ["clone", "--quiet", "https://github.com/actions/cache", directory]
        and argv[1][-1] == "refs/tags/v4^{commit}"
        and argv[2][-4:] == ["checkout", "--quiet", "--detach", "c" * 40]
        and commit == "c" * 40,
    )
    expected_env = git_environment(first.home)
    check(
        "every action git call runs with the runner's no-prompt, no-helper, "
        "HTTPS-only environment and no token",
        all(env == expected_env for _command, env in calls)
        and expected_env["GIT_TERMINAL_PROMPT"] == "0"
        and expected_env["GIT_ASKPASS"] == os.devnull
        and not any("TOKEN" in key for key in expected_env)
        and all(
            "credential.helper=" in command and "protocol.allow=never" in command
            for command in argv
        ),
    )
    attempts: list[str] = []

    def branch_only_git(command: Sequence[str], **_kwargs: object) -> str:
        """Resolve only the origin-branch candidate, recording each attempt."""
        attempts.append(command[-1])
        if command[-1].startswith("refs/remotes/origin/"):
            return "d" * 40
        raise Refusal("resolve failed")

    check(
        "a ref is resolved the way act duck-types it: tag, then origin branch, then SHA",
        resolve_action_commit(
            first.action_cache / "x", cache, home=first.home, run_git=branch_only_git
        )
        == "d" * 40
        and attempts == ["refs/tags/v4^{commit}", "refs/remotes/origin/v4^{commit}"],
    )

    def failing_git(command: Sequence[str], **kwargs: object) -> str:
        """Fail every call the way capture reports a nonzero git exit."""
        raise Refusal(f"{kwargs.get('description')} failed: fatal: repository not found")

    try:
        materialize_action(first, cache, failing_git)
    except Refusal as exc:
        clone_refusal: str | None = str(exc)
    else:
        clone_refusal = None
    check(
        "a failing clone is a Refusal naming the action",
        clone_refusal is not None and "actions/cache@v4" in clone_refusal,
    )


def selftest_action_plan(tally: SelftestTally, docker: DockerFixture) -> None:
    """Arms: dry-run prints the plan and clones nothing; the audited set is re-checked; the real git default."""
    check = tally.check
    first = docker.layout
    workflow_path = first.checkout / WORKFLOWS["docs"]
    workflow_path.parent.mkdir(parents=True, exist_ok=True)
    workflow_path.write_text(ACTION_FIXTURE_WORKFLOW, encoding="utf-8")
    calls: list[tuple[list[str], object]] = []
    plan = io.StringIO()
    with contextlib.redirect_stdout(plan):
        planned = materialize_workflow_actions(
            first, ("docs",), dry_run=True, run_git=recording_git(calls)
        )
    check(
        "dry-run prints the planned action set and clones nothing",
        tuple(action.spec for action in planned) == ("actions/cache@v4", "actions/checkout@v4")
        and not calls
        and "act-ci: action actions/cache@v4 planned at" in plan.getvalue()
        and "act-ci: action actions/checkout@v4 planned at" in plan.getvalue(),
    )
    workflow_path.write_text(
        ACTION_FIXTURE_WORKFLOW + "      - uses: example/setup@v1\n", encoding="utf-8"
    )
    tally.refused(
        "the materialiser re-checks each action against the audited set rather than "
        "inheriting the sandbox scan's position in the sequence",
        lambda: materialize_workflow_actions(
            first, ("docs",), dry_run=False, run_git=recording_git(calls)
        ),
    )
    check(
        "and that refusal reaches git for nothing",
        not calls,
    )
    check(
        "the materialiser defaults to the real tracked capture boundary",
        materialize_workflow_actions.__kwdefaults__ == {"run_git": capture},
    )
    workflow_path.unlink()


@dataclass(frozen=True)
class ActionDrive:
    """What one faked full validation run recorded: the call order, its result, and the layout it used."""

    events: list[str]
    rc: int | None
    error: Exception | None
    layout: RunLayout | None


def drive_validation_with_actions(
    resolved: ValidatedRun,
    shipping_root: pathlib.Path,
    run_git: Callable[..., str],
) -> ActionDrive:
    """Run the full, non-dry validation path with Git, Docker, and act faked; the recorded call order."""
    events: list[str] = []
    layouts: list[RunLayout] = []
    real_materialize = materialize_workflow_actions

    def materialize_for_actions(_run: ValidatedRun, layout: RunLayout) -> pathlib.Path:
        """A checkout stand-in carrying the two selected workflows, each using both actions."""
        layouts.append(layout)
        for workflow in ("docs", "elaborate"):
            path = layout.checkout / WORKFLOWS[workflow]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(ACTION_FIXTURE_WORKFLOW, encoding="utf-8")
        return layout.checkout

    @contextlib.contextmanager
    def recording_boundary(
        planned: DockerBoundary, **_kwargs: object
    ) -> Iterator[DockerBoundary]:
        """A boundary stand-in that records its entry and yields a populated boundary."""
        events.append("boundary")
        yield replace(
            planned,
            network_id="a" * 64,
            gateway="172.18.0.1",
            toolcache_owned=True,
            toolcache_seeded=True,
        )

    def act_for_actions(_command: Sequence[str], **_kwargs: object) -> int:
        """An act stand-in that records the launch and passes."""
        events.append("act")
        return 0

    def materialize_with_fake_git(
        layout: RunLayout, workflows: Sequence[str], **kwargs: object
    ) -> tuple[RemoteAction, ...]:
        """The real materialiser, recorded, with the fake git in place of capture."""
        events.append("materialise")
        return real_materialize(layout, workflows, run_git=run_git, **kwargs)  # type: ignore[arg-type]

    rc: int | None = None
    error: Exception | None = None
    with mock.patch.multiple(
        sys.modules[__name__],
        materialize_remote_head=materialize_for_actions,
        validate_checkout=lambda *_args, **_kwargs: None,
        validate_workflow_sandbox=lambda *_args, **_kwargs: None,
        initialize_required_submodules=lambda *_args, **_kwargs: None,
        require_live_pull_request=lambda *_args, **_kwargs: None,
        require_runtime=lambda *_args, **_kwargs: ["/trusted/act"],
        inspect_docker_boundary=lambda *_args, **_kwargs: None,
        temporary_docker_boundary=recording_boundary,
        allocate_tcp_port=lambda: 43211,
        execute_act_boundary=act_for_actions,
        cleanup_owned_containers=lambda *_args, **_kwargs: 0,
        cleanup_act_job_volumes=lambda *_args, **_kwargs: [],
        materialize_workflow_actions=materialize_with_fake_git,
    ):
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                rc = run_validation(
                    resolved,
                    ("docs", "elaborate"),
                    shipping_root,
                    act_binary="/trusted/act",
                    use_sudo=False,
                    dry_run=False,
                )
        except Exception as exc:  # the result is graded by the caller
            error = exc
    return ActionDrive(events, rc, error, layouts[0] if layouts else None)


def selftest_action_launch_order(
    tally: SelftestTally, resolved: ValidatedRun, shipping_root: pathlib.Path
) -> None:
    """Arms: one population before the boundary and the first act launch; a failed clone launches nothing."""
    check = tally.check
    calls: list[tuple[list[str], object]] = []
    drive = drive_validation_with_actions(resolved, shipping_root, recording_git(calls))
    clones = [command[-2] for command, _env in calls if "clone" in command]
    check(
        "the action cache is populated exactly once per run, before the Docker "
        "boundary exists and before the first act launch",
        drive.error is None
        and drive.rc == RC_OK
        and drive.events == ["materialise", "boundary", "act", "act"],
    )
    check(
        "two workflows sharing two actions produce one clone each, in sorted order",
        clones == ["https://github.com/actions/cache", "https://github.com/actions/checkout"],
    )
    check(
        "the clones in the real sequence carry the run's own credential-free git "
        "environment",
        drive.layout is not None
        and bool(calls)
        and all(env == git_environment(drive.layout.home) for _command, env in calls),
    )

    def failing_clone(command: Sequence[str], **kwargs: object) -> str:
        """Fail the clone the way capture reports it; resolve nothing else."""
        raise Refusal(f"{kwargs.get('description')} failed: fatal: could not read from remote")

    failed = drive_validation_with_actions(resolved, shipping_root, failing_clone)
    check(
        "a failing clone refuses the run naming the action, before any boundary or act "
        "launch",
        isinstance(failed.error, Refusal)
        and "actions/cache@v4" in str(failed.error)
        and failed.events == ["materialise"],
    )


def selftest_boundary_plants(tally: SelftestTally, docker: DockerFixture) -> None:
    """Arms: plants and silent recorders, plant-free runner environments, and an admissible probe workflow."""
    check = tally.check
    first = docker.layout
    root = first.temporary / "boundary-plants"
    root.mkdir()
    plants = plant_boundary_secrets(root, (3128, 8080))
    environment = plants.environment()
    direct = plants.environment(proxied=False)
    files = (".netrc", ".git-credentials", ".config/gh/hosts.yml", ".docker/config.json")
    check(
        "the plants occupy every operator-environment name the boundary must withhold, each "
        "credential file carries the planted token, and both recorders are executable and silent",
        all(name in environment for name in PLANTED_ENVIRONMENT_NAMES)
        and not any(name.lower().endswith("_proxy") for name in direct)
        and environment["HTTPS_PROXY"] == plants.proxy_url == environment["all_proxy"]
        and all(plants.token in (plants.home / name).read_text(encoding="utf-8") for name in files)
        and str(plants.home / "planted-credential-helper")
        in (plants.home / ".gitconfig").read_text(encoding="utf-8")
        and all(
            os.access(plants.home / name, os.X_OK) for name in ("planted-credential-helper", "planted-ssh")
        )
        and not recorder_activity(plants, "fixture"),
    )
    runner_environments = (git_environment(first.home), controlled_act_environment(first))
    prefix = " ".join(isolated_command_prefix("/trusted/act", True, controlled_act_environment(first)))
    check(
        "no plant reaches the runner's git environment, act's environment, or the sudo prefix "
        "by construction",
        all(
            name not in built and built["HOME"] != str(plants.home)
            for built in runner_environments
            for name in PLANTED_ENVIRONMENT_NAMES
        )
        and plants.token not in prefix
        and str(plants.home) not in prefix,
    )
    fixture_root = first.temporary / "boundary-probe-fixture"
    for path, contents in boundary_probe_sources(plants).items():
        (fixture_root / path).parent.mkdir(parents=True, exist_ok=True)
        (fixture_root / path).write_text(contents, encoding="utf-8")
    WORKFLOWS[BOUNDARY_PROBE_WORKFLOW] = BOUNDARY_PROBE_PATH
    try:
        validate_workflow_sandbox(fixture_root, (BOUNDARY_PROBE_WORKFLOW,))
        scope = workflow_job_volume_scope(fixture_root, (BOUNDARY_PROBE_WORKFLOW,))
    finally:
        WORKFLOWS.pop(BOUNDARY_PROBE_WORKFLOW, None)
    text = boundary_probe_sources(plants)[BOUNDARY_PROBE_PATH]
    check(
        "the probe workflow passes the trusted sandbox, leases its own job-volume prefix, maps the "
        "token secret, reports every check in both states, and carries no plant but the token marker",
        scope == {BOUNDARY_PROBE_WORKFLOW: "act-boundary-probe-selftest-"}
        and "PROBE_TOKEN: ${{ secrets.GITHUB_TOKEN }}" in text
        and all(f"report {name} visible" in text and f"report {name} absent" in text for name in BOUNDARY_PROBE_NAMES)
        and f"/dev/tcp/127.0.0.1/{plants.loopback_port}" in text
        and "/var/run/docker.sock" in text
        and plants.proxy_url not in text
        and str(plants.home) not in text,
    )


def selftest_boundary_probe_commands(tally: SelftestTally, docker: DockerFixture) -> None:
    """Arms: transcript grading on planted transcripts, and the boundary and leaky command shapes."""
    check = tally.check
    first = docker.layout
    plants = plant_boundary_secrets(first.temporary / "boundary-command-plants", (3128, 8080))
    prefix = f"[{BOUNDARY_PROBE_WORKFLOW}/probe]   | boundary-probe "
    absent = "".join(f"{prefix}{name}=absent\n" for name in BOUNDARY_PROBE_NAMES)
    visible = "".join(f"{prefix}{name}=visible\n" for name in BOUNDARY_PROBE_NAMES)
    partial = absent.replace(f"{prefix}docker-socket=absent\n", "")
    check(
        "grading: an all-absent transcript passes the boundary arm and fails the leaky arm on the "
        "three discriminators; all-visible the reverse; an unreported check fails both; `other` fails "
        "the boundary arm",
        grade_probe_transcript(absent, "boundary") == []
        and len(grade_probe_transcript(absent, "leaky")) == len(BOUNDARY_DISCRIMINATORS)
        and len(grade_probe_transcript(visible, "boundary")) == len(BOUNDARY_PROBE_NAMES)
        and grade_probe_transcript(visible, "leaky") == []
        and all("docker-socket was not reported" in p for p in grade_probe_transcript(partial, "boundary")[:1])
        and any("not reported" in p for p in grade_probe_transcript(partial, "leaky"))
        and grade_probe_transcript(absent.replace("token=absent", "token=other"), "boundary")
        == ["boundary arm: token is other"],
    )
    command = build_act_command(["act"], "docs", first, docker.port, docker.boundary)
    leaky = leaky_act_command(command, plants, False)
    check(
        "the boundary command carries the empty token, the disabled socket and the owned network; "
        "the leaky command drops exactly those, sources the token from the environment, and keeps "
        "the ownership label and the event",
        expect_refusal("the boundary command is refused as a leaky arm", lambda: require_boundary_removed(command))
        and expect_refusal(
            "the leaky command is refused as a boundary arm",
            lambda: require_boundary_present(leaky, docker.boundary),
        )
        and "--container-daemon-socket" not in leaky
        and "--network" not in leaky
        and leaky[leaky.index("--secret") + 1] == "GITHUB_TOKEN"
        and leaky[leaky.index("--container-options") + 1] == command[command.index("--container-options") + 1]
        and leaky[leaky.index("--eventpath") + 1] == str(first.event_path)
        and leaky[0] == "act",
    )
    require_boundary_present(command, docker.boundary)
    require_boundary_removed(leaky)
    sudo_command = build_act_command(
        isolated_command_prefix("/trusted/act", True, controlled_act_environment(first)),
        "docs",
        first,
        docker.port,
        docker.boundary,
    )
    leaky_sudo = leaky_act_command(sudo_command, plants, True)
    head = leaky_sudo[: leaky_sudo.index("pull_request")]
    check(
        "under sudo the leaky command starts act from the planted environment, not an emptied one, "
        "and the boundary command without its `-i` is refused",
        "-i" not in head
        and f"HOME={plants.home}" in head
        and f"GITHUB_TOKEN={plants.token}" in head
        and head[-1] == "/trusted/act"
        and pathlib.Path(head[0]).name == "sudo"
        and expect_refusal(
            "a sudo boundary command that keeps the operator environment is refused",
            lambda: require_boundary_present(
                [word for word in sudo_command if word != "-i"], docker.boundary
            ),
        ),
    )
    transcript = first.temporary / "boundary-transcript.log"
    child = transcript_popen(transcript)(
        [sys.executable, "-c", "print('boundary-probe token=absent')"], cwd=first.temporary
    )
    child.wait()
    check(
        "the transcript Popen appends the child's output where the grader reads it",
        child.returncode == 0 and parse_probe_transcript(transcript.read_text(encoding="utf-8")) == {"token": "absent"},
    )



def selftest_probe_clone_runner(tally: SelftestTally, docker: DockerFixture) -> None:
    """Arms: the probe-clone runner drains a lingering group, refuses a success, kills one outliving the grace.

    The lingering grandchildren release the pipes, as git's remote helper does,
    so `communicate` returns while the group still has a member.
    """
    check = tally.check
    cwd = docker.layout.temporary
    env = {"PATH": SAFE_PATH}
    shell = require_tool("sh")
    text = run_probe_clone(
        [shell, "-c", "sleep 0.2 >/dev/null 2>&1 & printf 'first\\nlast line\\n' >&2; exit 1"],
        env=env,
        cwd=cwd,
        label="draining",
    )
    check(
        "a failing child whose group drains within the grace yields its last stderr line",
        text == "last line",
    )
    tally.refused(
        "a probe clone that succeeds is refused",
        lambda: run_probe_clone([shell, "-c", "exit 0"], env=env, cwd=cwd, label="success"),
    )
    try:
        run_probe_clone(
            [shell, "-c", "sleep 30 >/dev/null 2>&1 & exit 1"],
            env=env,
            cwd=cwd,
            label="lingering",
            grace=0.1,
        )
    except Refusal as exc:
        message = str(exc)
    else:
        message = ""
    check(
        "a group that outlives the grace is killed and reported",
        "survived 0.1 s" in message and "was killed" in message,
    )


def selftest_toolcache_ownership(tally: SelftestTally, docker: DockerFixture) -> None:
    """Arms: the labelled tool cache is accepted, and a foreign or rival cache is never removed."""
    check = tally.check
    refused = tally.refused
    selftest_boundary = docker.boundary
    first_context = docker.context
    volume_metadata = docker.volume_metadata
    missing_volume = docker.missing_volume
    foreign_volume_metadata = docker.foreign_volume_metadata
    parse_act_toolcache_volume(volume_metadata, selftest_boundary)
    check("the labeled ephemeral act tool cache is accepted", True)
    refused(
        "a tool-cache volume owned by another run is refused",
        lambda: parse_act_toolcache_volume(
            volume_metadata,
            replace(selftest_boundary, token="f" * 32),
        ),
    )

    unowned_calls: list[tuple[str, ...]] = []

    def unowned_volume(
        arguments: Sequence[str], **_kwargs: object
    ) -> subprocess.CompletedProcess[str]:
        """A daemon holding a tool cache another run owns."""
        call = tuple(arguments)
        unowned_calls.append(call)
        if call == ("volume", "inspect", ACT_TOOLCACHE_VOLUME):
            return docker_completed(arguments, stdout=foreign_volume_metadata)
        raise AssertionError(f"unexpected Docker self-test call: {call}")

    existing_message = ""
    try:
        require_act_toolcache_absent(
            context=first_context,
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
        context=first_context,
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
        """A daemon where a rival's volume appears after the absence check."""
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
            context=first_context,
            docker_command=rival_volume,
        ),
    )
    check(
        "create-race rollback never removes the rival's volume",
        not any(call[:2] == ("volume", "rm") for call in race_calls),
    )


def selftest_toolcache_survivor(tally: SelftestTally, docker: DockerFixture) -> None:
    """Arm: tool-cache cleanup refuses when the volume survives removal."""
    check = tally.check
    refused = tally.refused
    selftest_boundary = docker.boundary
    first_context = docker.context
    volume_metadata = docker.volume_metadata
    surviving_calls: list[tuple[str, ...]] = []

    def surviving_volume(
        arguments: Sequence[str], **_kwargs: object
    ) -> subprocess.CompletedProcess[str]:
        """A daemon whose owned volume survives `volume rm`."""
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
            context=first_context,
            docker_command=surviving_volume,
        ),
    )
    check(
        "surviving-volume control exercised the removal request",
        ("volume", "rm", ACT_TOOLCACHE_VOLUME) in surviving_calls,
    )


def selftest_toolcache_post_accept(tally: SelftestTally, docker: DockerFixture) -> None:
    """Arms: a volume create accepted and then timed out is reconciled, and a failed rollback is surfaced."""
    check = tally.check
    refused = tally.refused
    selftest_boundary = docker.boundary
    first_context = docker.context
    volume_metadata = docker.volume_metadata
    missing_volume = docker.missing_volume
    accepted_volume = {"exists": False}
    accepted_volume_calls: list[tuple[str, ...]] = []

    def post_accept_volume_failure(
        arguments: Sequence[str], **_kwargs: object
    ) -> subprocess.CompletedProcess[str]:
        """A daemon whose volume create is accepted and then times out."""
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
            context=first_context,
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
        """A daemon whose volume create times out and whose rollback fails."""
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
            context=first_context,
            docker_command=volume_rollback_failure,
        )
    except Refusal as exc:
        rollback_message = str(exc)
    check(
        "a failed setup rollback is surfaced rather than reported clean",
        "setup rollback failed" in rollback_message
        and failed_volume_rollback["exists"],
    )


def selftest_teardown_independence(tally: SelftestTally, docker: DockerFixture) -> None:
    """Arm: a tool-cache failure cannot suppress the independent network teardown."""
    check = tally.check
    selftest_boundary = docker.boundary
    first_context = docker.context
    missing_volume = docker.missing_volume
    network_metadata = docker.network_metadata
    missing_network = docker.missing_network
    teardown_state = {"network": True}
    teardown_calls: list[tuple[str, ...]] = []

    def cache_failure_during_teardown(
        arguments: Sequence[str], **_kwargs: object
    ) -> subprocess.CompletedProcess[str]:
        """A daemon whose owned tool cache has vanished before teardown."""
        call = tuple(arguments)
        teardown_calls.append(call)
        if call == ("volume", "ls", "--quiet"):
            return docker_completed(arguments)
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
            context=first_context,
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


def make_post_accept_network_daemon(
    docker: DockerFixture,
    state: dict[str, bool],
    calls: list[tuple[str, ...]],
    *,
    network_rm_fails: bool,
    interrupt_create: bool,
) -> Callable[..., subprocess.CompletedProcess[str]]:
    """A fake daemon whose network create is accepted, then fails or is interrupted; it records to `state`/`calls`."""
    selftest_boundary = docker.boundary
    volume_metadata = docker.volume_metadata
    missing_volume = docker.missing_volume
    network_metadata = docker.network_metadata
    missing_network = docker.missing_network
    missing_network_name = docker.missing_network_name
    seed_container_name = docker.seed_container_name
    seed_container_metadata = docker.seed_container_metadata
    missing_seed_container = docker.missing_seed_container

    def post_accept_network_failure(
        arguments: Sequence[str], **_kwargs: object
    ) -> subprocess.CompletedProcess[str]:
        """A daemon whose network create is accepted and then fails or is interrupted."""
        call = tuple(arguments)
        calls.append(call)
        if call == ("volume", "ls", "--quiet"):
            return docker_completed(arguments)
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
        if call[0] == "run" and seed_container_name in call:
            state["seed"] = True
            return docker_completed(arguments)
        if call == ("container", "inspect", seed_container_name):
            if state["seed"]:
                return docker_completed(
                    arguments, stdout=seed_container_metadata
                )
            return docker_completed(
                arguments, 1, stderr=missing_seed_container
            )
        if call == (
            "container",
            "rm",
            "--force",
            "--volumes",
            seed_container_name,
        ):
            state["seed"] = False
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

    return post_accept_network_failure


def run_network_setup_control(
    docker: DockerFixture,
    *,
    network_rm_fails: bool,
    interrupt_create: bool = False,
    interrupt_after_toolcache: bool = False,
) -> tuple[dict[str, bool], list[tuple[str, ...]], str]:
    """Drive a boundary create whose network step fails; (state, calls, message)."""
    selftest_boundary = docker.boundary
    first_context = docker.context
    state = {"volume": False, "network": False, "seed": False}
    calls: list[tuple[str, ...]] = []
    post_accept_network_failure = make_post_accept_network_daemon(
        docker,
        state,
        calls,
        network_rm_fails=network_rm_fails,
        interrupt_create=interrupt_create,
    )
    message = ""

    def toolcache_handoff() -> None:
        """Raise SIGTERM's TerminationRequest after the tool cache when asked to."""
        if interrupt_after_toolcache:
            raise TerminationRequest(signal.SIGTERM)

    try:
        create_docker_boundary(
            replace(
                selftest_boundary,
                network_id=None,
                gateway=None,
                toolcache_owned=False,
                toolcache_seeded=False,
            ),
            context=first_context,
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


def selftest_network_setup_rollback(tally: SelftestTally, docker: DockerFixture) -> None:
    """Arms: a network create that fails, is interrupted, or is pre-empted by a signal reconciles both resources."""
    check = tally.check
    selftest_boundary = docker.boundary
    setup_state, setup_calls, setup_message = run_network_setup_control(
        docker,
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
        docker,
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
            docker,
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
            docker,
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


def make_deterministic_seed_daemon(
    docker: DockerFixture,
    state: dict[str, bool],
    calls: list[tuple[str, ...]],
    *,
    seed_exit: int,
) -> Callable[..., subprocess.CompletedProcess[str]]:
    """A fake daemon that creates, seeds, and networks in order, with the seed exiting `seed_exit`."""
    selftest_boundary = docker.boundary
    volume_metadata = docker.volume_metadata
    missing_volume = docker.missing_volume
    network_metadata = docker.network_metadata
    missing_network = docker.missing_network
    missing_network_name = docker.missing_network_name
    seed_container_name = docker.seed_container_name
    seed_container_metadata = docker.seed_container_metadata
    missing_seed_container = docker.missing_seed_container

    def deterministic_seed_daemon(
        arguments: Sequence[str], **_kwargs: object
    ) -> subprocess.CompletedProcess[str]:
        """A daemon that creates, seeds, and networks in order, with the seed exiting `seed_exit`."""
        call = tuple(arguments)
        calls.append(call)
        if call == ("volume", "ls", "--quiet"):
            return docker_completed(arguments)
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
        if call[0] == "run" and seed_container_name in call:
            state["seed"] = True
            return docker_completed(
                arguments,
                seed_exit,
                stderr=(
                    "" if seed_exit == 0 else "injected empty tool cache"
                ),
            )
        if call == ("container", "inspect", seed_container_name):
            if state["seed"]:
                return docker_completed(
                    arguments, stdout=seed_container_metadata
                )
            return docker_completed(
                arguments, 1, stderr=missing_seed_container
            )
        if call == (
            "container",
            "rm",
            "--force",
            "--volumes",
            seed_container_name,
        ):
            state["seed"] = False
            return docker_completed(arguments)
        if call[0:2] == ("network", "create"):
            state["network"] = True
            return docker_completed(
                arguments, stdout=f"{selftest_boundary.network_id}\n"
            )
        if call == ("network", "inspect", selftest_boundary.name):
            if state["network"]:
                return docker_completed(arguments, stdout=network_metadata)
            return docker_completed(
                arguments, 1, stderr=missing_network_name
            )
        if call == (
            "network",
            "inspect",
            str(selftest_boundary.network_id),
        ):
            if state["network"]:
                return docker_completed(arguments, stdout=network_metadata)
            return docker_completed(arguments, 1, stderr=missing_network)
        raise AssertionError(f"unexpected seed self-test call: {call}")

    return deterministic_seed_daemon


def run_seed_boundary_control(
    docker: DockerFixture,
    *,
    seed_exit: int,
) -> tuple[dict[str, bool], list[tuple[str, ...]], str, DockerBoundary | None]:
    """Drive a full boundary create whose seed exits `seed_exit`; (state, calls, message, boundary)."""
    selftest_boundary = docker.boundary
    first_context = docker.context
    state = {"volume": False, "network": False, "seed": False}
    calls: list[tuple[str, ...]] = []
    deterministic_seed_daemon = make_deterministic_seed_daemon(
        docker, state, calls, seed_exit=seed_exit
    )
    message = ""
    built: DockerBoundary | None = None
    try:
        built = create_docker_boundary(
            replace(
                selftest_boundary,
                network_id=None,
                gateway=None,
                toolcache_owned=False,
                toolcache_seeded=False,
            ),
            context=first_context,
            docker_command=deterministic_seed_daemon,
        )
    except Refusal as exc:
        message = str(exc)
    return state, calls, message, built


def selftest_seed_ordering(tally: SelftestTally, docker: DockerFixture) -> None:
    """Arms: the cold tool cache is seeded exactly once before sibling jobs, and an empty seed refuses."""
    check = tally.check
    selftest_boundary = docker.boundary
    # Regression control for the #315 cold-cache concurrent-create
    # race: the boundary must interpose exactly one owned seed mount
    # between creating the empty volume and any act sibling job.
    seeded_state, seeded_calls, seeded_message, seeded_boundary = (
        run_seed_boundary_control(docker, seed_exit=0)
    )
    seed_run_calls = [
        index
        for index, call in enumerate(seeded_calls)
        if call and call[0] == "run"
    ]
    volume_create_index = next(
        index
        for index, call in enumerate(seeded_calls)
        if call[0:2] == ("volume", "create")
    )
    network_create_index = next(
        index
        for index, call in enumerate(seeded_calls)
        if call[0:2] == ("network", "create")
    )
    seed_run_call = (
        seeded_calls[seed_run_calls[0]] if seed_run_calls else ()
    )
    check(
        "the cold tool cache is seeded exactly once before sibling jobs",
        not seeded_message
        and seeded_boundary is not None
        and seeded_boundary.toolcache_seeded
        and len(seed_run_calls) == 1
        and volume_create_index < seed_run_calls[0] < network_create_index
        and RUNNER_IMAGE in seed_run_call
        and f"{ACT_TOOLCACHE_VOLUME}:{ACT_TOOLCACHE_TARGET}"
        in seed_run_call
        and f"{DOCKER_OWNER_LABEL}={selftest_boundary.token}"
        in seed_run_call
        and seed_run_call[seed_run_call.index("--network") + 1] == "none"
        and not seeded_state["seed"],
    )
    empty_state, empty_calls, empty_message, empty_boundary = (
        run_seed_boundary_control(docker, seed_exit=1)
    )
    check(
        "an unpopulated seed refuses the boundary and reconciles it",
        empty_boundary is None
        and "seed did not prove a populated cache" in empty_message
        and not empty_state["seed"]
        and not empty_state["volume"]
        and not any(
            call[0:2] == ("network", "create") for call in empty_calls
        ),
    )


def selftest_delayed_daemon(tally: SelftestTally, docker: DockerFixture) -> None:
    """Arm: stable rollback catches a Docker daemon whose removals land late."""
    check = tally.check
    selftest_boundary = docker.boundary
    first_context = docker.context
    volume_metadata = docker.volume_metadata
    missing_volume = docker.missing_volume
    network_metadata = docker.network_metadata
    missing_network_name = docker.missing_network_name
    delayed_clock = [0.0]
    delayed_state = {"volume": False, "network": False, "released": False}
    delayed_calls: list[tuple[str, ...]] = []

    def delayed_daemon_completion(
        arguments: Sequence[str], **_kwargs: object
    ) -> subprocess.CompletedProcess[str]:
        """A daemon whose removals only take effect after the clock advances."""
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
        """Advance the fake clock and let the delayed removals land."""
        delayed_clock[0] += duration
        if not delayed_state["released"]:
            delayed_state["released"] = True
            delayed_state["volume"] = True
            delayed_state["network"] = True

    discard_act_toolcache_if_owned(
        selftest_boundary,
        context=first_context,
        docker_command=delayed_daemon_completion,
        stability_window=0.1,
        monotonic=lambda: delayed_clock[0],
        sleep=advance_delayed_daemon,
    )
    discard_docker_network_if_owned(
        selftest_boundary,
        context=first_context,
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


def selftest_layout_isolation(
    tally: SelftestTally,
    first: RunLayout,
    second: RunLayout,
) -> dict[str, str]:
    """Arms: two heads share nothing and the act environment carries nothing ambient; the controlled env."""
    check = tally.check
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
    return controlled


def selftest_privileged_signals(tally: SelftestTally) -> None:
    """Arms: a sudo act group is signalled and inspected only through privileged kill."""
    check = tally.check
    privileged_signal_calls: list[tuple[str, ...]] = []

    def fake_privileged_signal(
        command: Sequence[str], **_kwargs: object
    ) -> subprocess.CompletedProcess[str]:
        """Record one privileged kill command and report success."""
        privileged_signal_calls.append(tuple(command))
        return docker_completed(command)

    def forbidden_unprivileged_signal(_group: int, _signal: int) -> None:
        """Fail the arm: a sudo group must never see an unprivileged killpg."""
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
        """Record one privileged kill and report the group missing."""
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


def selftest_containment_hold(tally: SelftestTally) -> None:
    """Arm: Docker teardown waits through kill and inspection failures until the group is provably absent."""
    check = tally.check
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
            """Record one poll."""
            containment_trace.append("poll")

        def wait(self, timeout: float) -> int:
            """Record the reap and its timeout."""
            containment_trace.append(f"reaped-{timeout}")
            return 0

    def uncertain_group_exists(
        _group: int, *, use_sudo: bool
    ) -> bool:
        """Answer the next scripted inspection, raising when it is a Refusal."""
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
        """Fail the first two kills and accept the third."""
        nonlocal containment_signal_count
        del use_sudo
        containment_signal_count += 1
        containment_trace.append(f"kill-{containment_signal_count}")
        if containment_signal_count < 3:
            raise Refusal("injected privileged kill failure")

    containment_notices: list[str] = []

    def broken_containment_notifier(message: str) -> None:
        """Record the notice, then fail as a closed stderr would."""
        containment_notices.append(message)
        raise BrokenPipeError("injected closed stderr")

    terminate_act_process_group(
        ContainmentProcess(),  # type: ignore[arg-type]
        use_sudo=True,
        primary=TerminationRequest(signal.SIGTERM),
        policy=ContainmentPolicy(
            escalation=((signal.SIGKILL, 0),),
            group_exists=uncertain_group_exists,
            signal_group=recovering_group_signal,
            sleep=lambda _duration: containment_trace.append("held"),
            recovery_notice=broken_containment_notifier,
        ),
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


def run_adversarial_sigint() -> tuple[int | None, str, list[str], str]:
    """One SIGINT delivered while the mask and disposition APIs fail; (rc, escaped error, forced calls, stderr)."""
    handler_api_calls: list[str] = []
    handler_race_rc: int | None = None
    handler_race_error = ""
    handler_race_stderr = io.StringIO()
    original_pthread_sigmask = signal.pthread_sigmask
    original_signal = signal.signal

    def fail_handler_mask(
        *_args: object, **_kwargs: object
    ) -> None:
        """Injected pthread_sigmask failure: any mask call inside the handler raises."""
        handler_api_calls.append("pthread_sigmask")
        raise OSError("Signal 2 ignored due to race condition")

    def fail_handler_disposition(
        *_args: object, **_kwargs: object
    ) -> None:
        """Injected signal.signal failure: any disposition call inside the handler raises."""
        handler_api_calls.append("signal")
        raise OSError("signal disposition changed during delivery")

    def adversarial_sigint() -> int:
        """Deliver one real SIGINT while the mask and disposition APIs are made to fail."""
        setattr(signal, "pthread_sigmask", fail_handler_mask)
        setattr(signal, "signal", fail_handler_disposition)
        try:
            signal.raise_signal(signal.SIGINT)
        finally:
            setattr(signal, "signal", original_signal)
            setattr(signal, "pthread_sigmask", original_pthread_sigmask)
        return RC_OK

    try:
        with contextlib.redirect_stderr(handler_race_stderr):
            handler_race_rc = run_with_cleanup_signals(
                adversarial_sigint
            )
    except OSError as exc:
        handler_race_error = str(exc)
    finally:
        setattr(signal, "signal", original_signal)
        setattr(signal, "pthread_sigmask", original_pthread_sigmask)
    return (
        handler_race_rc,
        handler_race_error,
        handler_api_calls,
        handler_race_stderr.getvalue(),
    )


def selftest_signal_latching(tally: SelftestTally) -> None:
    """Arms: the first handled signal latches, the handler survives the mask race, and cleanup defers one."""
    check = tally.check
    latched_interrupt = False
    with cleanup_termination_signals():
        interrupt_handler = signal.getsignal(signal.SIGINT)
        if callable(interrupt_handler):
            try:
                interrupt_handler(signal.SIGINT, None)
            except TerminationRequest as exc:
                repeat_was_harmless = False
                try:
                    interrupt_handler(signal.SIGTERM, None)
                except TerminationRequest:
                    pass
                else:
                    repeat_was_harmless = True
                latched_interrupt = (
                    exc.signum == signal.SIGINT
                    and repeat_was_harmless
                    and isinstance(
                        interrupt_handler, _CleanupSignalLatch
                    )
                    and interrupt_handler.signum == signal.SIGINT
                    and all(
                        signal.getsignal(item) is interrupt_handler
                        for item in CLEANUP_SIGNALS
                    )
                )
    check(
        "the first handled signal latches and repeats stay harmless",
        latched_interrupt,
    )
    (
        handler_race_rc,
        handler_race_error,
        handler_api_calls,
        handler_race_stderr,
    ) = run_adversarial_sigint()
    check(
        "SIGINT handler avoids the Python signal-mask race",
        handler_race_rc == 128 + signal.SIGINT
        and not handler_race_error
        and not handler_api_calls
        and handler_race_stderr
        == "act-ci: interrupted by SIGINT after cleanup\n",
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


def selftest_worker_signal_mask(tally: SelftestTally) -> None:
    """Arm: a worker thread cannot intercept a signal before cleanup finishes."""
    check = tally.check
    worker_trace: list[str] = []
    worker_ready = threading.Event()
    worker_stop = threading.Event()
    worker_threads: list[threading.Thread] = []

    def signal_safe_worker() -> None:
        """Signal readiness and wait to be released."""
        worker_ready.set()
        worker_stop.wait(2)

    def cleanup_with_live_worker() -> int:
        """Signal this process inside a cleanup scope while a worker thread is live."""
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


def selftest_monitor_join(tally: SelftestTally) -> None:
    """Arms: a signal during the monitor join waits for proven termination, and a monitor that never started refuses."""
    check = tally.check
    refused = tally.refused
    join_cancel = threading.Event()
    join_complete = threading.Event()
    join_lock = threading.Lock()
    join_trace: list[str] = []
    join_workers: list[threading.Thread] = []
    join_problems: list[str] = []

    def signal_during_monitor_join() -> None:
        """Signal this process from the worker while main joins it."""
        try:
            join_cancel.wait(1)
            join_trace.append("signal-sent")
            os.kill(os.getpid(), signal.SIGHUP)
            time.sleep(0.02)
            join_trace.append("worker-finished")
        finally:
            join_complete.set()

    def join_signal_action() -> int:
        """Start a worker and join it through the cleanup-thread protocol."""
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
        """Fail the way an exhausted host would."""
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


def selftest_worker_cli_timeout(tally: SelftestTally) -> None:
    """Arm: a worker-thread CLI timeout kills its blocked-mask process group."""
    check = tally.check
    worker_cli_results: list[tuple[str, float]] = []

    def timed_worker_cli() -> None:
        """Run a tracked CLI with a tiny timeout from a worker thread and record containment."""
        started_at = time.monotonic()
        try:
            run_tracked_process_group_command(
                [
                    sys.executable,
                    "-I",
                    "-c",
                    "import time; time.sleep(30)",
                ],
                context=CommandContext(
                    use_sudo=False,
                    cwd=pathlib.Path.cwd(),
                    env={
                        "PATH": SAFE_PATH,
                        "LANG": "C.UTF-8",
                        "LC_ALL": "C.UTF-8",
                    },
                ),
                timeout=0.05,
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


def selftest_private_inputs(
    tally: SelftestTally,
    first: RunLayout,
    controlled: Mapping[str, str],
) -> None:
    """Arms: per-run configuration roots, and every planted act input is refused."""
    check = tally.check
    refused = tally.refused
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


def selftest_container_ownership(
    tally: SelftestTally,
    docker: DockerFixture,
) -> list[dict[str, object]]:
    """Arms: ownership follows labels and container networks exactly; the three-container inventory."""
    check = tally.check
    selftest_boundary = docker.boundary
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
    return inventory


def selftest_cancelled_inventory(
    tally: SelftestTally,
    docker: DockerFixture,
    inventory: list[dict[str, object]],
) -> None:
    """Arms: cancellation stops the monitor inventory, and a foreign tool-cache mount is refused."""
    check = tally.check
    refused = tally.refused
    selftest_boundary = docker.boundary
    owned_id = str(inventory[0]["Id"])
    delayed_inventory_cancel = threading.Event()
    delayed_inspect_entered = threading.Event()
    delayed_inspect_release = threading.Event()
    delayed_inventory_result: list[list[dict[str, object]]] = []
    delayed_inventory_errors: list[BaseException] = []

    def delayed_last_inspect(
        arguments: Sequence[str], **_kwargs: object
    ) -> subprocess.CompletedProcess[str]:
        """A daemon whose final container inspect blocks until released."""
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
        """Collect the inventory under cancellation, recording the result or the error."""
        try:
            delayed_inventory_result.append(
                docker_container_inventory(
                    context=CommandContext(use_sudo=False, cwd=pathlib.Path.cwd(), env={}),
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


@dataclass(frozen=True)
class JobVolumeFaults:
    """Failures the fake daemon injects into one job-volume cleanup."""

    in_use: frozenset[str] = frozenset()
    immortal: frozenset[str] = frozenset()
    probe_errors: frozenset[str] = frozenset()
    ghosts: frozenset[str] = frozenset()
    inventory_failures: frozenset[int] = frozenset()


@dataclass(frozen=True)
class JobVolumeFixture:
    """The live act job-volume names this suite reasons about, and what leases or neighbours them."""

    live: str
    scope: DockerBoundary
    boundary: DockerBoundary
    rival: str
    orphan: str
    embedded_rival: str
    cased_rival: str
    residents: set[str]
    bystander_id: str
    bystander: Mapping[str, object]


def job_volume_fixture(docker: DockerFixture) -> JobVolumeFixture:
    """The live act job-volume names, the boundaries that lease them, and one unrelated tenant container."""
    selftest_boundary = docker.boundary
    live_job_volume = (
        "act-interrupt-selftest-sleep-"
        "e6269f0c21890b2977d8be082bc36ff62700a3ce80ad05652f9e186d237d234b"
    )
    interrupt_scope = new_docker_boundary(
        (act_job_volume_prefix("interrupt-selftest"),)
    )
    rival_job_volume = act_container_name("act", "interrupt-rival/sleep")
    orphan_job_volume = act_container_name("act", "interrupt-selftest/orphan")
    embedded_rival_volume = f"act-rival-{live_job_volume}"
    cased_rival_volume = "act-Interrupt-Selftest-sleep-" + live_job_volume[-64:]
    bystander_id = "9" * 63 + "1"
    bystander_volume = "tenant-data"
    residents = {
        rival_job_volume,
        embedded_rival_volume,
        cased_rival_volume,
        bystander_volume,
    }
    bystander = {
        "Id": bystander_id,
        "Name": "/tenant",
        "Config": {"Labels": {}},
        "HostConfig": {"NetworkMode": "bridge"},
        "NetworkSettings": {"Networks": {"bridge": {}}},
        "State": {"Running": False},
        "Mounts": [
            {
                "Type": "volume",
                "Name": bystander_volume,
                "Destination": "/data",
                "RW": True,
            }
        ],
    }
    scoped_boundary = replace(
        selftest_boundary, job_volume_prefixes=("act-interrupt-selftest-",)
    )
    return JobVolumeFixture(
        live=live_job_volume,
        scope=interrupt_scope,
        boundary=scoped_boundary,
        rival=rival_job_volume,
        orphan=orphan_job_volume,
        embedded_rival=embedded_rival_volume,
        cased_rival=cased_rival_volume,
        residents=residents,
        bystander_id=bystander_id,
        bystander=bystander,
    )


def selftest_job_volume_lease(tally: SelftestTally, jobs: JobVolumeFixture) -> None:
    """Arms: the job-volume name mirror is act's, and only in-scope names fall inside a workflow lease."""
    check = tally.check
    refused = tally.refused
    check(
        "the act job-volume name mirror reproduces a live act 0.2.89 volume name",
        act_container_name("act", "interrupt-selftest/sleep") == jobs.live,
    )
    check(
        "job workspace and environment volumes fall inside their workflow lease",
        jobs.scope.job_volume_prefixes == ("act-interrupt-selftest-",)
        and is_leased_act_job_volume(jobs.scope, jobs.live)
        and is_leased_act_job_volume(jobs.scope, f"{jobs.live}-env"),
    )
    check(
        "the tool cache, foreign act jobs, and near-miss names stay unleased",
        not is_leased_act_job_volume(jobs.scope, ACT_TOOLCACHE_VOLUME)
        and not is_leased_act_job_volume(
            jobs.scope, act_container_name("act", "interrupt-rival/sleep")
        )
        and not is_leased_act_job_volume(
            jobs.scope, act_container_name("act", "interrupt-selftests/sleep")
        )
        and not is_leased_act_job_volume(jobs.scope, jobs.live[:-1])
        and not is_leased_act_job_volume(jobs.scope, f"{jobs.live}-envx"),
    )
    check(
        "workflow names sanitize the way act builds container names",
        act_job_volume_prefix("rtl full/2") == "act-rtl-full-2-"
        and act_job_volume_prefix("-x") == "act-x-",
    )
    for bad_prefix in ("act-docs", "docs-", "act--docs-", "act-docs--", ""):
        refused(
            f"malformed job-volume lease prefix {bad_prefix!r} is refused",
            lambda bad=bad_prefix: new_docker_boundary((bad,)),
        )
    refused(
        "a workflow without a name cannot lease act job volumes",
        lambda: act_job_volume_prefix(None),
    )
    refused(
        "a blank workflow name cannot lease act job volumes",
        lambda: act_job_volume_prefix("  "),
    )


def selftest_job_volume_gate(tally: SelftestTally, jobs: JobVolumeFixture) -> None:
    """Arms: a pre-existing in-scope job volume refuses acquisition before any mutation."""
    check = tally.check
    refused = tally.refused
    gate_calls: list[tuple[str, ...]] = []

    def planted_job_volume_daemon(
        arguments: Sequence[str], **_kwargs: object
    ) -> subprocess.CompletedProcess[str]:
        """Fake daemon whose inventory already holds in-scope act job volumes."""
        call = tuple(arguments)
        gate_calls.append(call)
        if call == ("volume", "ls", "--quiet"):
            return docker_completed(
                arguments,
                stdout=f"{jobs.live}\n{jobs.live}-env\nunrelated\n",
            )
        # Any other call means acquisition mutated before the gate; answer
        # with a failure so the arm grades red instead of crashing.
        return docker_completed(
            arguments, 1, stderr=f"unexpected job-volume gate call: {call}"
        )

    gate_message = ""
    try:
        create_docker_boundary(
            jobs.scope,
            context=CommandContext(use_sudo=False, cwd=pathlib.Path.cwd(), env={}),
            docker_command=planted_job_volume_daemon,
        )
    except Refusal as exc:
        gate_message = str(exc)
    check(
        "a pre-existing in-scope act job volume refuses acquisition before any mutation",
        jobs.live in gate_message
        and f"{jobs.live}-env" in gate_message
        and "already exist" in gate_message
        and gate_calls == [("volume", "ls", "--quiet")],
    )

    def foreign_job_volume_daemon(
        arguments: Sequence[str], **_kwargs: object
    ) -> subprocess.CompletedProcess[str]:
        """Fake daemon holding only volumes outside the lease."""
        call = tuple(arguments)
        if call == ("volume", "ls", "--quiet"):
            return docker_completed(
                arguments,
                stdout=(
                    f"{act_container_name('act', 'interrupt-rival/sleep')}\n"
                    f"{ACT_TOOLCACHE_VOLUME}\n"
                ),
            )
        raise AssertionError(f"unexpected foreign job-volume call: {call}")

    require_act_job_volumes_absent(
        jobs.scope,
        context=CommandContext(use_sudo=False, cwd=pathlib.Path.cwd(), env={}),
        docker_command=foreign_job_volume_daemon,
    )
    check("act job volumes outside the lease do not block acquisition", True)
    refused(
        "a boundary without a job-volume lease cannot pass the acquisition gate",
        lambda: require_act_job_volumes_absent(
            replace(jobs.scope, job_volume_prefixes=()),
            context=CommandContext(use_sudo=False, cwd=pathlib.Path.cwd(), env={}),
            docker_command=foreign_job_volume_daemon,
        ),
    )
    for lone_name in (jobs.live, f"{jobs.live}-env"):
        refused(
            f"a lone in-scope twin {lone_name[-8:]} refuses acquisition",
            lambda lone=lone_name: require_act_job_volumes_absent(
                jobs.scope,
                context=CommandContext(use_sudo=False, cwd=pathlib.Path.cwd(), env={}),
                docker_command=lambda arguments, **_kwargs: docker_completed(
                    arguments, stdout=f"{lone}\n"
                ),
            ),
        )


def selftest_job_volume_name_corpus(tally: SelftestTally) -> None:
    """Arms: the lease prefix is what act's own name builder produces, and unleasable names are refused."""
    check = tally.check
    refused = tally.refused
    corpus = ("a--b", "-x", "x-", "rtl full/2", "interrupt-selftest", "a.b_c", "A/B")
    check(
        "the lease prefix is what act's own name builder produces for every "
        "leasable name",
        all(
            act_container_name("act", f"{name}/job").startswith(
                act_job_volume_prefix(name)
            )
            for name in corpus
        ),
    )
    refused(
        "a name whose separators act keeps doubled is unleasable",
        lambda: act_job_volume_prefix("a   b"),
    )
    for null_literal in ("null", "NULL", "~"):
        refused(
            f"the YAML null literal {null_literal!r} cannot lease act job volumes",
            lambda literal=null_literal: act_job_volume_prefix(literal),
        )


def selftest_job_volume_records(tally: SelftestTally, jobs: JobVolumeFixture) -> None:
    """Arms: a volume record is None only for a named-missing volume, and a malformed inventory refuses."""
    check = tally.check
    refused = tally.refused
    def volume_record_with(
        returncode: int, stdout: str = "", stderr: str = ""
    ) -> Mapping[str, object] | None:
        """docker_volume_record against one canned inspect reply."""
        return docker_volume_record(
            jobs.live,
            context=CommandContext(use_sudo=False, cwd=pathlib.Path.cwd(), env={}),
            docker_command=lambda arguments, **_kwargs: docker_completed(
                arguments, returncode, stdout=stdout, stderr=stderr
            ),
        )

    check(
        "a volume record is None only when Docker names the volume as missing",
        volume_record_with(
            1, stderr=f"Error response from daemon: get {jobs.live}: no such volume"
        )
        is None
        and volume_record_with(0, stdout=json.dumps([{"Name": jobs.live}]))
        == {"Name": jobs.live},
    )
    refused(
        "a volume record for another name is refused",
        lambda: volume_record_with(0, stdout=json.dumps([{"Name": "other"}])),
    )
    refused(
        "a malformed volume record is refused",
        lambda: volume_record_with(0, stdout="not json"),
    )
    refused(
        "a volume inspection failing for another reason is refused",
        lambda: volume_record_with(1, stderr="permission denied"),
    )
    refused(
        "a malformed volume inventory refuses acquisition",
        lambda: require_act_job_volumes_absent(
            jobs.scope,
            context=CommandContext(use_sudo=False, cwd=pathlib.Path.cwd(), env={}),
            docker_command=lambda arguments, **_kwargs: docker_completed(
                arguments, stdout="bad name\n"
            ),
        ),
    )
    check(
        "a lease never matches a name that merely contains or re-cases its prefix",
        not is_leased_act_job_volume(jobs.scope, jobs.embedded_rival)
        and not is_leased_act_job_volume(jobs.scope, jobs.cased_rival),
    )


def make_job_volume_reply(
    docker: DockerFixture,
    state: dict[str, object],
    volumes: set[str],
    inventories: list[int],
    *,
    faults: JobVolumeFaults,
) -> Callable[..., subprocess.CompletedProcess[str] | None]:
    """The volume half of the fake daemon: one callable answering the `docker volume` subcommands."""
    volume_metadata = docker.volume_metadata
    missing_volume = docker.missing_volume
    missing = "Error response from daemon: get {name}: no such volume"
    def volume_reply(
        arguments: Sequence[str], call: tuple[str, ...]
    ) -> subprocess.CompletedProcess[str] | None:
        """Answer the volume subcommands; None means the call is not one."""
        if call == ("volume", "inspect", ACT_TOOLCACHE_VOLUME):
            if state["toolcache"]:
                return docker_completed(arguments, stdout=volume_metadata)
            return docker_completed(arguments, 1, stderr=missing_volume)
        if call == ("volume", "rm", ACT_TOOLCACHE_VOLUME):
            state["toolcache"] = False
            return docker_completed(arguments)
        if call == ("volume", "ls", "--quiet"):
            inventories[0] += 1
            if inventories[0] in faults.inventory_failures:
                return docker_completed(
                    arguments, 1, stderr="injected volume inventory failure"
                )
            listed = sorted(volumes | faults.ghosts)
            return docker_completed(
                arguments, stdout="".join(f"{v}\n" for v in listed)
            )
        if call[0:2] == ("volume", "rm"):
            name = call[2]
            if name in faults.in_use:
                holder = "f" * 64
                detail = f"Error response from daemon: remove {name}: volume is in use - [{holder}]"
                return docker_completed(arguments, 1, stderr=detail)
            if name not in volumes:
                return docker_completed(
                    arguments, 1, stderr=missing.format(name=name)
                )
            if name not in faults.immortal:
                volumes.discard(name)
            return docker_completed(arguments)
        if call[0:2] == ("volume", "inspect"):
            name = call[2]
            if name in faults.probe_errors:
                return docker_completed(
                    arguments, 1, stderr="permission denied while inspecting"
                )
            if name in volumes:
                record = {"Name": name, "Driver": "local", "Scope": "local", "Labels": {}}
                return docker_completed(arguments, stdout=json.dumps([record]))
            return docker_completed(
                arguments, 1, stderr=missing.format(name=name)
            )
        return None

    return volume_reply


def job_volume_daemon(
    docker: DockerFixture,
    state: dict[str, object],
    calls: list[tuple[str, ...]],
    *,
    container: Mapping[str, object],
    faults: JobVolumeFaults,
) -> Callable[..., subprocess.CompletedProcess[str]]:
    """A fake daemon holding containers, a network, the tool cache, and volumes."""
    selftest_boundary = docker.boundary
    network_metadata = docker.network_metadata
    missing_network = docker.missing_network
    volumes = state["volumes"]
    containers = state["containers"]
    assert isinstance(volumes, set) and isinstance(containers, set)
    inventories = [0]
    volume_reply = make_job_volume_reply(
        docker, state, volumes, inventories, faults=faults
    )
    def daemon(
        arguments: Sequence[str], **_kwargs: object
    ) -> subprocess.CompletedProcess[str]:
        """Dispatch one Docker CLI call against the fake state."""
        call = tuple(arguments)
        calls.append(call)
        if call[0:2] == ("container", "ls"):
            return docker_completed(
                arguments, stdout="".join(f"{c}\n" for c in sorted(containers))
            )
        if call[0:2] == ("container", "inspect"):
            if call[2] in containers:
                records = state.get("records")
                record = records.get(call[2], container) if isinstance(records, dict) else container
                return docker_completed(arguments, stdout=json.dumps([record]))
            return docker_completed(
                arguments, 1, stderr=f"Error: No such container: {call[2]}"
            )
        if call[0:2] in (("container", "stop"), ("container", "rm")):
            for target in call[2:]:
                containers.discard(target)
            return docker_completed(arguments)
        if call == ("network", "inspect", str(selftest_boundary.network_id)):
            if state["network"]:
                return docker_completed(arguments, stdout=network_metadata)
            return docker_completed(arguments, 1, stderr=missing_network)
        if call == ("network", "rm", str(selftest_boundary.network_id)):
            state["network"] = False
            return docker_completed(arguments)
        reply = volume_reply(arguments, call)
        if reply is not None:
            return reply
        raise AssertionError(f"unexpected job-volume cleanup call: {call}")

    return daemon


def run_job_volume_cleanup_control(
    docker: DockerFixture,
    jobs: JobVolumeFixture,
    inventory: list[dict[str, object]],
    *,
    mounted: tuple[str, ...] | None = None,
    faults: JobVolumeFaults | None = None,
) -> tuple[set[str], list[tuple[str, ...]], str]:
    """Run the boundary cleanup against the fake daemon; return its residue.

    `mounted` defaults to the workflow's own workspace and environment volume
    pair, which is derived from `jobs` and so cannot be spelled as a default.
    """
    owned_id = str(inventory[0]["Id"])
    if mounted is None:
        mounted = (jobs.live, f"{jobs.live}-env")
    state: dict[str, object] = {
        "volumes": {*mounted, jobs.orphan, *jobs.residents},
        "containers": {owned_id, jobs.bystander_id},
        "records": {jobs.bystander_id: jobs.bystander},
        "network": True,
        "toolcache": True,
    }
    calls: list[tuple[str, ...]] = []
    container = {
        **inventory[0],
        "Mounts": [
            *inventory[0]["Mounts"],
            {"Type": "bind", "Source": "/tmp/bound", "Destination": "/bound"},
            *(
                {
                    "Type": "volume",
                    "Name": name,
                    "Destination": f"/mnt/{index}",
                    "RW": True,
                }
                for index, name in enumerate(mounted)
            ),
        ],
    }
    message = ""
    try:
        cleanup_docker_boundary(
            jobs.boundary,
            context=CommandContext(use_sudo=False, cwd=pathlib.Path.cwd(), env={}),
            docker_command=job_volume_daemon(
                docker,
                state,
                calls,
                container=container,
                faults=faults or JobVolumeFaults(),
            ),
        )
    except Refusal as exc:
        message = str(exc)
    volumes = state["volumes"]
    assert isinstance(volumes, set)
    return volumes, calls, message


def selftest_job_volume_cleanup(
    tally: SelftestTally,
    docker: DockerFixture,
    jobs: JobVolumeFixture,
    inventory: list[dict[str, object]],
) -> None:
    """Arms: cleanup removes the observed volumes and an in-scope orphan, and leaves every neighbour."""
    check = tally.check
    owned_id = str(inventory[0]["Id"])
    clean_volumes, clean_calls, clean_message = run_job_volume_cleanup_control(
        docker, jobs, inventory
    )
    check(
        "interrupt cleanup removes the observed job volumes and an in-scope orphan "
        "while rival, re-cased, embedding, and bystander volumes survive",
        clean_message == ""
        and clean_volumes == jobs.residents
        and not any(
            call[0:2] == ("volume", "rm") and call[2] in jobs.residents
            for call in clean_calls
        ),
    )
    def observed_mounts(*records: Mapping[str, object]) -> object:
        """owned_volume_mounts over records, graded rather than raised."""
        try:
            return owned_volume_mounts(list(records), {owned_id})
        except Refusal as exc:
            return f"refused: {exc}"

    bound_owned = {
        **inventory[0],
        "Mounts": [
            {"Type": "bind", "Source": "/tmp/b", "Destination": "/b"},
            {"Type": "volume", "Name": jobs.live, "Destination": "/w", "RW": True},
        ],
    }
    check(
        "a bystander container and its volume are neither observed nor removed, "
        "and a bind mount is not a volume",
        not any(
            call[0:2] == ("container", "rm") and jobs.bystander_id in call
            for call in clean_calls
        )
        and observed_mounts(inventory[0], jobs.bystander) == []
        and observed_mounts(bound_owned) == [jobs.live],
    )
    with mock.patch.object(
        sys.modules[__name__],
        "remove_act_job_volume",
        wraps=remove_act_job_volume,
    ) as removal_spy:
        run_job_volume_cleanup_control(
        docker, jobs, inventory
    )
    check(
        "reconciliation never overrides the removal's absence window",
        removal_spy.call_count >= 1
        and all(
            call.kwargs.get("absence") is None for call in removal_spy.call_args_list
        ),
    )
    check(
        "the absence window is the daemon constant for the real CLI and zero for fakes",
        absence_window_seconds(None, run_docker) == DOCKER_MUTATION_STABLE_SECONDS
        and absence_window_seconds(None, docker_completed) == 0.0
        and absence_window_seconds(AbsenceWindow(0.25), run_docker) == 0.25
        and absence_window_seconds(AbsenceWindow(0), run_docker) == 0,
    )
    container_removals = [
        index
        for index, call in enumerate(clean_calls)
        if call[0:2] == ("container", "rm")
    ]
    job_volume_removals = [
        index
        for index, call in enumerate(clean_calls)
        if call[0:2] == ("volume", "rm") and call[2] != ACT_TOOLCACHE_VOLUME
    ]
    check(
        "job-volume removal never forces and follows every container removal",
        bool(container_removals)
        and bool(job_volume_removals)
        and max(container_removals) < min(job_volume_removals)
        and not any(
            any("force" in item for item in clean_calls[index])
            for index in job_volume_removals
        ),
    )


def selftest_job_volume_held(
    tally: SelftestTally,
    docker: DockerFixture,
    jobs: JobVolumeFixture,
    inventory: list[dict[str, object]],
) -> None:
    """Arms: a job volume another container holds, one that survives removal, and one outside the lease."""
    check = tally.check
    held_volumes, _held_calls, held_message = run_job_volume_cleanup_control(
        docker,
        jobs,
        inventory,
        faults=JobVolumeFaults(in_use=frozenset({f"{jobs.live}-env"}))
    )
    check(
        "a job volume another container still holds is preserved and reported",
        f"{jobs.live}-env" in held_message
        and "in use" in held_message
        and f"{jobs.live}-env" in held_volumes
        and jobs.live not in held_volumes,
    )
    immortal_volumes, _immortal_calls, immortal_message = (
        run_job_volume_cleanup_control(
            docker,
            jobs,
            inventory,
            faults=JobVolumeFaults(immortal=frozenset({jobs.live}))
        )
    )
    check(
        "a job volume surviving its removal is reported rather than certified absent",
        "survived" in immortal_message and jobs.live in immortal_volumes,
    )
    stray_job_volume = act_container_name("act", "interrupt-rival/stray")
    foreign_stray_volume = "foreign-data"
    stray_volumes, stray_calls, stray_message = run_job_volume_cleanup_control(
        docker,
        jobs,
        inventory,
        mounted=(jobs.live, stray_job_volume, foreign_stray_volume)
    )
    check(
        "a volume an owned container mounted outside the lease is preserved and "
        "reported as lease drift, act-shaped or not",
        "outside the leased" in stray_message
        and stray_job_volume in stray_message
        and foreign_stray_volume in stray_message
        and {stray_job_volume, foreign_stray_volume} <= stray_volumes
        and not any(
            call[0:2] == ("volume", "rm")
            and call[2] in (stray_job_volume, foreign_stray_volume)
            for call in stray_calls
        )
        and jobs.live not in stray_volumes
        and jobs.rival in stray_volumes,
    )


def selftest_job_volume_survivors(
    tally: SelftestTally,
    docker: DockerFixture,
    jobs: JobVolumeFixture,
    inventory: list[dict[str, object]],
) -> None:
    """Arms: an anonymous, unprobeable, ghost, or uncounted job volume is reported, never certified absent."""
    check = tally.check
    anonymous_volume = "9" * 64
    anonymous_volumes, anonymous_calls, anonymous_message = (
        run_job_volume_cleanup_control(
            docker,
            jobs,
            inventory,
            mounted=(jobs.live, f"{jobs.live}-env", anonymous_volume)
        )
    )
    check(
        "an anonymous volume on an owned container is neither drift nor a target",
        anonymous_message == ""
        and anonymous_volumes == jobs.residents | {anonymous_volume}
        and not any(
            call[0:2] == ("volume", "rm") and call[2] == anonymous_volume
            for call in anonymous_calls
        ),
    )
    _probe_volumes, _probe_calls, probe_message = run_job_volume_cleanup_control(
        docker,
        jobs,
        inventory,
        faults=JobVolumeFaults(probe_errors=frozenset({jobs.live}))
    )
    check(
        "an absence probe that fails is reported as unverifiable, never as absent",
        "cannot verify act job volume" in probe_message
        and jobs.live in probe_message,
    )
    ghost_job_volume = act_container_name("act", "interrupt-selftest/ghost")
    _ghost_volumes, _ghost_calls, ghost_message = run_job_volume_cleanup_control(
        docker,
        jobs,
        inventory,
        faults=JobVolumeFaults(ghosts=frozenset({ghost_job_volume}))
    )
    check(
        "an in-scope volume the final inventory still lists is a reported survivor",
        "survived cleanup" in ghost_message and ghost_job_volume in ghost_message,
    )
    _first_volumes, _first_calls, first_inventory_message = (
        run_job_volume_cleanup_control(
            docker,
            jobs,
            inventory,
            faults=JobVolumeFaults(inventory_failures=frozenset({1}))
        )
    )
    check(
        "a failed volume inventory before reconciliation is reported, not skipped",
        "Docker volume inventory failed" in first_inventory_message,
    )
    _last_volumes, _last_calls, last_inventory_message = (
        run_job_volume_cleanup_control(
            docker,
            jobs,
            inventory,
            faults=JobVolumeFaults(inventory_failures=frozenset({2}))
        )
    )
    check(
        "a failed volume inventory after reconciliation is reported, not certified",
        "Docker volume inventory failed" in last_inventory_message,
    )


def selftest_job_volume_absence(tally: SelftestTally, jobs: JobVolumeFixture) -> None:
    """Arms: a volume reappearing inside the absence window is a survivor, and a durably absent one is not."""
    check = tally.check
    refused = tally.refused
    reappearing_clock = [0.0]
    reappearing_state = {"present": False, "probes": 0}

    def reappearing_daemon(
        arguments: Sequence[str], **_kwargs: object
    ) -> subprocess.CompletedProcess[str]:
        """Fake daemon whose removed volume reappears once the clock advances."""
        call = tuple(arguments)
        if call == ("volume", "rm", jobs.live):
            return docker_completed(arguments)
        if call == ("volume", "inspect", jobs.live):
            reappearing_state["probes"] += 1
            if reappearing_state["present"]:
                return docker_completed(
                    arguments, stdout=json.dumps([{"Name": jobs.live}])
                )
            return docker_completed(
                arguments,
                1,
                stderr=f"Error response from daemon: get {jobs.live}: "
                "no such volume",
            )
        return docker_completed(
            arguments, 1, stderr=f"unexpected reappearing daemon call: {call}"
        )

    def reappear(duration: float) -> None:
        """Advance the fake clock and bring the volume back."""
        reappearing_clock[0] += duration
        reappearing_state["present"] = True

    refused(
        "a job volume reappearing inside the absence window is a reported survivor",
        lambda: remove_act_job_volume(
            jobs.live,
            context=CommandContext(use_sudo=False, cwd=pathlib.Path.cwd(), env={}),
            docker_command=reappearing_daemon,
            absence=AbsenceWindow(0.1, lambda: reappearing_clock[0], reappear),
        ),
    )
    check(
        "the absence window probed more than once before the volume reappeared",
        reappearing_state["probes"] >= 2,
    )
    reappearing_state.update(present=False, probes=0)
    reappearing_clock[0] = 0.0

    def stay_absent(duration: float) -> None:
        """Advance the fake clock with the volume still absent."""
        reappearing_clock[0] += duration

    certified: object = None
    try:
        certified = remove_act_job_volume(
            jobs.live,
            context=CommandContext(use_sudo=False, cwd=pathlib.Path.cwd(), env={}),
            docker_command=reappearing_daemon,
            absence=AbsenceWindow(0.1, lambda: reappearing_clock[0], stay_absent),
        )
    except Refusal as exc:
        certified = f"refused: {exc}"
    check(
        "a job volume absent for the whole window is certified removed",
        certified is True and reappearing_state["probes"] >= 2,
    )


def selftest_job_volume_mounts(
    tally: SelftestTally,
    docker: DockerFixture,
    jobs: JobVolumeFixture,
    inventory: list[dict[str, object]],
) -> None:
    """Arms: malformed mount metadata fails cleanup, and the leased name pattern is act's own."""
    check = tally.check
    refused = tally.refused
    owned_id = str(inventory[0]["Id"])
    def malformed_mount_control(mounts: object) -> str:
        """Cleanup message for an owned container whose Mounts metadata is ``mounts``."""
        state: dict[str, object] = {
            "volumes": set(),
            "containers": {owned_id},
            "network": True,
            "toolcache": True,
        }
        calls: list[tuple[str, ...]] = []
        observed: list[str] = []
        try:
            cleanup_owned_containers(
                jobs.boundary,
                context=CommandContext(use_sudo=False, cwd=pathlib.Path.cwd(), env={}),
                docker_command=job_volume_daemon(
                    docker,
                    state,
                    calls,
                    container={**inventory[0], "Mounts": mounts},
                    faults=JobVolumeFaults(),
                ),
                observed_volumes=observed,
            )
        except Refusal as exc:
            return str(exc)
        return ""

    check(
        "malformed owned-container mount metadata fails container cleanup",
        "malformed mount metadata" in malformed_mount_control(None)
        and "malformed volume name"
        in malformed_mount_control(
            [{"Type": "volume", "Name": "bad name", "Destination": "/x", "RW": True}]
        ),
    )
    check(
        "the job-volume name pattern is act's: no underscore, at most 63 stem bytes",
        not is_leased_act_job_volume(
            jobs.scope,
            "act-interrupt-selftest-a_b-" + "0" * 64,
        )
        and is_leased_act_job_volume(
            jobs.scope,
            "act-interrupt-selftest-" + "s" * 40 + "-" + "0" * 64,
        )
        and not is_leased_act_job_volume(
            jobs.scope,
            "act-interrupt-selftest-" + "s" * 41 + "-" + "0" * 64,
        ),
    )
    refused(
        "a workflow name whose prefix act would trim is refused",
        lambda: act_job_volume_prefix("x" * 60),
    )
    check(
        "a missing-volume report must name the volume it is about",
        not docker_reports_missing_volume(
            subprocess.CompletedProcess(
                [], 1, "", "Error response from daemon: get other: no such volume"
            ),
            jobs.live,
        )
        and docker_reports_missing_volume(
            subprocess.CompletedProcess(
                [],
                1,
                "",
                f"Error response from daemon: get {jobs.live}: no such volume",
            ),
            jobs.live,
        ),
    )


def selftest_job_volume_leftovers(
    tally: SelftestTally,
    docker: DockerFixture,
    jobs: JobVolumeFixture,
    inventory: list[dict[str, object]],
) -> None:
    """Arms: a job volume act left behind is removed and reported, and reconciliation needs a lease."""
    check = tally.check
    refused = tally.refused
    leftover_state: dict[str, object] = {
        "volumes": {jobs.orphan, jobs.rival},
        "containers": set(),
        "network": True,
        "toolcache": True,
    }
    leftover_calls: list[tuple[str, ...]] = []
    leftover_removed: list[str] = []
    try:
        leftover_removed = cleanup_act_job_volumes(
            jobs.boundary,
            [act_container_name("act", "interrupt-selftest/gone")],
            context=CommandContext(use_sudo=False, cwd=pathlib.Path.cwd(), env={}),
            docker_command=job_volume_daemon(
                docker,
                leftover_state,
                leftover_calls,
                container=inventory[0],
                faults=JobVolumeFaults(),
            ),
        )
    except Refusal as exc:
        leftover_removed = [f"refused: {exc}"]
    check(
        "a job volume act left after a workflow is removed and reported as leftover; "
        "an observed name the daemon no longer holds is not",
        leftover_removed == [jobs.orphan]
        and leftover_state["volumes"] == {jobs.rival},
    )
    refused(
        "reconciliation without a lease scope is refused",
        lambda: cleanup_act_job_volumes(
            replace(jobs.boundary, job_volume_prefixes=()),
            [],
            context=CommandContext(use_sudo=False, cwd=pathlib.Path.cwd(), env={}),
            docker_command=job_volume_daemon(
                docker,
                {"volumes": set(), "containers": set(), "network": True, "toolcache": True},
                [],
                container=inventory[0],
                faults=JobVolumeFaults(),
            ),
        ),
    )


def selftest_act_version(tally: SelftestTally) -> None:
    """Arms: only the audited act version is accepted."""
    check = tally.check
    refused = tally.refused
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


def successful_process(
    *_args: object, **_kwargs: object
) -> subprocess.CompletedProcess[object]:
    """A stand-in act process that always exits 0."""
    return subprocess.CompletedProcess([], 0)


def selftest_spawn_handoff(tally: SelftestTally) -> None:
    """Arm: a signal between spawn and Popen return still terminates the stored group."""
    check = tally.check
    spawn_handoff_trace: list[str] = []

    class SpawnHandoffProcess:
        pid = 987654320

    def signal_before_popen_return(
        *_args: object, **_kwargs: object
    ) -> subprocess.Popen[object]:
        """Spawn, then signal this process before the constructor returns."""
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
        """Record which process group was terminated."""
        del use_sudo, primary
        spawn_handoff_trace.append(f"terminated-{process.pid}")

    def repeat_signal_at_spawn_cleanup_entry() -> None:
        """Send a repeat signal on cleanup entry and record that it was ignored."""
        spawn_handoff_trace.append("cleanup-entered")
        os.kill(os.getpid(), signal.SIGHUP)
        spawn_handoff_trace.append("repeat-ignored")

    spawn_handoff_rc = run_with_cleanup_signals(
        lambda: run_act_process(
            ["act"],
            context=CommandContext(use_sudo=False, cwd=pathlib.Path.cwd(), env={}),
            seams=ProcessSeams(
                popen=signal_before_popen_return,
                terminate_group=record_spawn_termination,
                before_terminate_group=repeat_signal_at_spawn_cleanup_entry,
            ),
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


def check_surviving_group_refusal(
    tally: SelftestTally,
    trace: list[str],
    label: str,
    expected_error: str,
    expected_trace: Sequence[str],
    action: Callable[[], object],
) -> None:
    """Run `action` and check its refusal text and `trace` against the expectation."""
    trace.clear()
    error = ""
    try:
        action()
    except Refusal as exc:
        error = str(exc)
    tally.check(
        label,
        error == expected_error and trace == expected_trace,
    )


def selftest_surviving_group(tally: SelftestTally) -> None:
    """Arms: a successful act or host-command leader cannot leave a live process group."""
    surviving_group_trace: list[str] = []

    class SuccessfulLeader:
        def __init__(self, pid: int) -> None:
            self.pid = pid
            self.returncode = RC_OK

        def wait(self) -> int:
            """Record the wait and exit successfully."""
            surviving_group_trace.append(f"waited-{self.pid}")
            return RC_OK

        def communicate(self, timeout: float) -> tuple[str, str]:
            """Record the drain and return empty pipes."""
            del timeout
            surviving_group_trace.append(f"communicated-{self.pid}")
            return "", ""

    def spawn_successful_leader(
        process: SuccessfulLeader,
    ) -> Callable[..., subprocess.Popen[object]]:
        """A popen stand-in that returns `process` and records the spawn."""
        def spawn(*_args: object, **_kwargs: object) -> subprocess.Popen[object]:
            """Record the spawn and return the leader."""
            surviving_group_trace.append(f"spawned-{process.pid}")
            return process  # type: ignore[return-value]

        return spawn

    def report_surviving_group(process_group: int, *, use_sudo: bool) -> bool:
        """Report the group as still present."""
        del use_sudo
        surviving_group_trace.append(f"group-present-{process_group}")
        return True

    def contain_surviving_group(
        process: subprocess.Popen[object],
        *,
        use_sudo: bool,
        primary: BaseException,
    ) -> None:
        """Record the containment and the exception that caused it."""
        del use_sudo
        surviving_group_trace.append(
            f"contained-{process.pid}-{type(primary).__name__}"
        )

    act_leader = SuccessfulLeader(987654315)
    check_surviving_group_refusal(
        tally,
        surviving_group_trace,
        "a successful act leader cannot leave a live process group",
        "act process group survived its leader",
        [
            "spawned-987654315",
            "waited-987654315",
            "group-present-987654315",
            "contained-987654315-Refusal",
        ],
        lambda: run_act_process(
            ["act"],
            context=CommandContext(use_sudo=False, cwd=pathlib.Path.cwd(), env={}),
            seams=ProcessSeams(
                popen=spawn_successful_leader(act_leader),
                terminate_group=contain_surviving_group,
                group_exists=report_surviving_group,
            ),
        ),
    )

    host_leader = SuccessfulLeader(987654316)
    check_surviving_group_refusal(
        tally,
        surviving_group_trace,
        "a successful host-command leader cannot leave a live process group",
        "host command process group survived its leader",
        [
            "spawned-987654316",
            "communicated-987654316",
            "group-present-987654316",
            "contained-987654316-Refusal",
            "communicated-987654316",
        ],
        lambda: run_tracked_process_group_command(
            ["git", "status"],
            context=CommandContext(use_sudo=False, cwd=pathlib.Path.cwd(), env={}),
            timeout=1,
            seams=ProcessSeams(
                popen=spawn_successful_leader(host_leader),
                terminate_group=contain_surviving_group,
                group_exists=report_surviving_group,
            ),
        ),
    )


def selftest_nested_cleanup(tally: SelftestTally) -> None:
    """Arm: a repeat signal inside a tracked cleanup command cannot abort the tail."""
    check = tally.check
    nested_cleanup_trace: list[str] = []

    class NestedCleanupProcess:
        pid = 987654317
        returncode = 0

        def communicate(self, timeout: float) -> tuple[str, str]:
            """Record the cleanup command finishing."""
            del timeout
            nested_cleanup_trace.append("cleanup-command-finished")
            return "", ""

    def repeat_during_cleanup_popen(
        *_args: object, **_kwargs: object
    ) -> subprocess.Popen[str]:
        """Spawn the cleanup command and send a repeat signal before returning."""
        nested_cleanup_trace.append("cleanup-command-spawned")
        os.kill(os.getpid(), signal.SIGHUP)
        nested_cleanup_trace.append("repeat-ignored")
        return NestedCleanupProcess()  # type: ignore[return-value]

    def tracked_cleanup_after_first_signal() -> int:
        """Take a first signal, then run a tracked command in the cleanup tail."""
        try:
            os.kill(os.getpid(), signal.SIGTERM)
        finally:
            nested_cleanup_trace.append("cleanup-entered")
            run_tracked_process_group_command(
                ["docker", "network", "rm"],
                context=CommandContext(use_sudo=False, cwd=pathlib.Path.cwd(), env={}),
                timeout=1,
                seams=ProcessSeams(popen=repeat_during_cleanup_popen),
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


def selftest_docker_timeout(tally: SelftestTally) -> None:
    """Arm: a timed-out sudo Docker CLI is contained before rollback begins."""
    check = tally.check
    docker_timeout_trace: list[str] = []

    class DockerTimeoutProcess:
        pid = 987654318
        returncode = -signal.SIGKILL
        communicate_calls = 0

        def communicate(self, timeout: float) -> tuple[str, str]:
            """Time out on the first drain and succeed on the second."""
            self.communicate_calls += 1
            docker_timeout_trace.append(f"communicate-{self.communicate_calls}")
            if self.communicate_calls == 1:
                raise subprocess.TimeoutExpired(["docker"], timeout)
            return "", ""

    def spawn_timeout_command(
        *_args: object, **_kwargs: object
    ) -> subprocess.Popen[str]:
        """Spawn the timing-out Docker command stand-in."""
        docker_timeout_trace.append("spawned")
        return DockerTimeoutProcess()  # type: ignore[return-value]

    def contain_timeout_command(
        process: subprocess.Popen[object],
        *,
        use_sudo: bool,
        primary: BaseException,
    ) -> None:
        """Record that the group was contained."""
        del use_sudo, primary
        docker_timeout_trace.append(f"group-absent-{process.pid}")

    docker_timeout_caught = False
    try:
        run_tracked_process_group_command(
            ["docker", "volume", "create"],
            context=CommandContext(use_sudo=True, cwd=pathlib.Path.cwd(), env={}),
            timeout=0.01,
            seams=ProcessSeams(
                popen=spawn_timeout_command,
                terminate_group=contain_timeout_command,
            ),
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


def selftest_child_signal_mask(tally: SelftestTally) -> dict[str, str]:
    """Arm: spawned children inherit no cleanup-signal mask and honor SIGTERM; the child environment."""
    check = tally.check
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
    return child_environment


@contextlib.contextmanager
def selftest_child_subreaper() -> Iterator[None]:
    """Give orphaned probe zombies a reaper even under act's bare PID 1."""
    libc = ctypes.CDLL(None, use_errno=True)
    try:
        prctl = libc.prctl
    except AttributeError:
        yield
        return
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


def await_recorded_probe_pids(
    ready_path: pathlib.Path,
) -> tuple[int, int, int] | None:
    """The (leader, child, PGID) the probe wrote, or None if it never did."""
    ready_deadline = time.monotonic() + 10
    while time.monotonic() < ready_deadline:
        try:
            fields = tuple(
                int(item) for item in ready_path.read_text().split()
            )
        except (FileNotFoundError, OSError, UnicodeError, ValueError):
            fields = ()
        if len(fields) == 3 and all(item > 1 for item in fields):
            return (fields[0], fields[1], fields[2])
        time.sleep(0.05)
    return None


def await_probe_runner_exit(runner_pid: int, process_group: int) -> int:
    """Reap the forked runner, killing it if it will not finish in time; its exit code."""
    # The production boundary may consume its complete 10 s INT, 10 s TERM,
    # and 5 s KILL escalation before it can report containment.
    exit_deadline = time.monotonic() + 35
    while time.monotonic() < exit_deadline:
        reap_adopted_process_group(process_group)
        waited, raw_status = os.waitpid(runner_pid, os.WNOHANG)
        if waited == runner_pid:
            return os.waitstatus_to_exitcode(raw_status)
        time.sleep(0.05)
    try:
        os.kill(runner_pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    _waited, raw_status = os.waitpid(runner_pid, 0)
    return os.waitstatus_to_exitcode(raw_status)


def prove_probe_group_absent(process_group: int) -> bool:
    """Whether the recorded PGID went away on its own.

    A group that did not is a failed check, so this also tears it down rather
    than leaving the rest of the self-test to inherit it.
    """
    if not (process_group > 1 and process_group != os.getpgrp()):
        return False
    absence_deadline = time.monotonic() + 3
    while time.monotonic() < absence_deadline:
        reap_adopted_process_group(process_group)
        try:
            if not process_group_exists(process_group, use_sudo=False):
                return True
        except Refusal:
            pass
        time.sleep(0.05)
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
            if not process_group_exists(process_group, use_sudo=False):
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
            if not process_group_exists(process_group, use_sudo=False):
                break
        except Refusal:
            pass
        time.sleep(0.05)
    return False


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

    recorded = await_recorded_probe_pids(ready_path)
    if recorded is not None:
        os.kill(runner_pid, sent_signal)
    else:
        os.kill(runner_pid, signal.SIGKILL)

    process_group = recorded[2] if recorded is not None else -1
    runner_status = await_probe_runner_exit(runner_pid, process_group)
    group_absent = prove_probe_group_absent(process_group)

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
    """Run the probe with this process as child subreaper."""
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
    """Whether a signal during `capture` of `command` contains the whole command tree."""
    def run_probe_command() -> int:
        """Capture the command; reaching the return means it was not interrupted."""
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


def noncooperative_tree_program() -> str:
    """A leader that spawns a sleeping child, reports both PIDs and its PGID, then ignores signals."""
    return (
        f"#!{sys.executable}\n"
        "import os, pathlib, subprocess, sys, time\n"
        "child = subprocess.Popen([sys.executable, '-I', '-c', "
        "'import time; time.sleep(300)'], stdout=subprocess.DEVNULL, "
        "stderr=subprocess.DEVNULL)\n"
        "pathlib.Path(os.environ['ACT_CI_PIDFILE']).write_text("
        "f'{os.getpid()} {child.pid} {os.getpgrp()}')\n"
        "time.sleep(300)\n"
    )


def cooperative_tree_program() -> str:
    """A leader that spawns a child, reports both PIDs and its PGID, and exits 128+signum on a signal."""
    return (
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


def selftest_captured_tree_probes(
    tally: SelftestTally,
    capture_probe_root: pathlib.Path,
    child_environment: Mapping[str, str],
) -> None:
    """Arms: a process-directed TERM or HUP during `capture` contains a non-cooperative child tree."""
    check = tally.check
    tree_helper = capture_probe_root / "noncooperative-tree.py"
    tree_helper.write_text(noncooperative_tree_program(), encoding="utf-8")
    tree_helper.chmod(0o755)
    for sent_signal in CLEANUP_SIGNALS:
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


def selftest_main_entry_probe(tally: SelftestTally, capture_probe_root: pathlib.Path) -> None:
    """Arm: production main, interrupted during its first repository lookup, contains the lookup's tree."""
    check = tally.check
    entry_helper_root = capture_probe_root / "entry-bin"
    entry_helper_root.mkdir()
    fake_gh = entry_helper_root / "gh"
    fake_gh.write_text(cooperative_tree_program(), encoding="utf-8")
    fake_gh.chmod(0o755)
    entry_ready = capture_probe_root / "entry.ready"
    original_safe_path = SAFE_PATH

    def run_main_entry_probe() -> int:
        """Run production main against a stub gh that reports its PIDs."""
        # This runs in the forked probe child, which os._exit discards, so
        # the module attribute is patched in place rather than rebound.
        with mock.patch.object(
            sys.modules[__name__],
            "SAFE_PATH",
            f"{entry_helper_root}:{original_safe_path}",
        ):
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


def selftest_git_remote_helper_probes(
    tally: SelftestTally,
    capture_probe_root: pathlib.Path,
) -> None:
    """Arms: a process-directed TERM or HUP during a fetch contains the Git remote-helper tree."""
    check = tally.check
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
    remote_helper.write_text(noncooperative_tree_program(), encoding="utf-8")
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
    for sent_signal in CLEANUP_SIGNALS:
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


def selftest_remote_change(
    tally: SelftestTally,
    fixture: SelftestFixture,
    fixture_run: ValidatedRun,
) -> None:
    """Arms: remote movement across an act process is refused, except a moved recorded base oid, which is noted."""
    check = tally.check
    refused = tally.refused
    pr = fixture.pr
    def execute_with_remote_change(changed: PullRequest) -> int:
        """Run the act boundary with the PR re-read as `changed` after the process."""
        answers = iter((pr, changed))

        def moving_query(_number: int, _repository: str) -> PullRequest:
            """Answer the pinned PR first, then the changed one."""
            return next(answers)

        return execute_act_boundary(
            ["act"],
            run=fixture_run,
            context=CommandContext(use_sudo=False, cwd=ROOT, env={}),
            integrity_check=lambda: None,
            seams=SpawnSeams(query=moving_query, run_process=successful_process),
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
        "recorded base oid movement is noted without discarding exact-head "
        "evidence",
        execute_with_remote_change(replace(pr, base_sha="5" * 40)) == RC_OK,
    )


def selftest_run_directory_rollback(tally: SelftestTally) -> None:
    """Arms: a signal or a stat failure right after run-directory creation reconciles the accepted path."""
    check = tally.check
    refused = tally.refused
    acquisition_parent = pathlib.Path(tempfile.gettempdir()).resolve()
    interrupted_run_lease = RunDirectoryLease(acquisition_parent)

    def interrupt_after_run_create() -> None:
        """Raise SIGTERM's TerminationRequest once the directory exists."""
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
        """Fail the post-create inspection."""
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


def selftest_sudo_cleanup_failures(tally: SelftestTally) -> None:
    """Arms: a failed or unlaunchable sudo chown cannot report cleanup success."""
    refused = tally.refused
    cleanup = make_run_directory()

    def failed_chown(
        *_args: object, **_kwargs: object
    ) -> subprocess.CompletedProcess[str]:
        """A chown stand-in that fails."""
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

    def failed_chown_launch(
        *_args: object, **_kwargs: object
    ) -> subprocess.CompletedProcess[str]:
        """A chown stand-in that cannot launch."""
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


def selftest_installed_runner(tally: SelftestTally, fixture: SelftestFixture) -> None:
    """Arms: a content-pinned immutable runner install is accepted only with the right pin, place, and options."""
    check = tally.check
    refused = tally.refused
    repository = fixture.repository
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


def selftest_cleanup_failures(tally: SelftestTally) -> None:
    """Arms: a failed removal or a replacement symlink cannot masquerade as completed cleanup."""
    refused = tally.refused
    cleanup = make_run_directory()

    def failed_remove(_path: pathlib.Path) -> None:
        """A removal stand-in that fails."""
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


def selftest_git_fixture(root: pathlib.Path, pr: PullRequest) -> GitFixture:
    """A scratch repository beneath `root` with the docs workflow committed at a base and a head."""
    repo = root / "repo"
    repo.mkdir()
    git = require_tool("git")
    test_env = git_environment(root)

    def test_git(*arguments: str) -> str:
        """Stripped stdout of one git command in the self-test repository."""
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
    return GitFixture(
        repo=repo,
        test_git=test_git,
        workflow_path=workflow_path,
        workflow_text=workflow_text,
        first_commit=first_commit,
        test_head=test_head,
        test_pr=test_pr,
    )


def selftest_index_flags(tally: SelftestTally, git_fixture: GitFixture) -> None:
    """Arms: no index flag, symlink, or replacement object can hide selected workflow bytes."""
    refused = tally.refused
    repo = git_fixture.repo
    test_git = git_fixture.test_git
    workflow_path = git_fixture.workflow_path
    workflow_text = git_fixture.workflow_text
    first_commit = git_fixture.first_commit
    test_head = git_fixture.test_head
    test_pr = git_fixture.test_pr
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


def selftest_submodule_manifest(tally: SelftestTally, git_fixture: GitFixture) -> None:
    """Arms: only the exact trusted submodule manifest and gitlinks are accepted, over HTTPS alone."""
    check = tally.check
    refused = tally.refused
    repo = git_fixture.repo
    test_git = git_fixture.test_git
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


def selftest_sandbox_policy(tally: SelftestTally, repo: pathlib.Path) -> None:
    """Arms: every job-level and step-level authority the sandbox forbids is refused before act."""
    refused = tally.refused
    sandbox_job_workflows = {
        "self-hosted-job.yml": (
            "self-hosted runner authority is refused",
            "    runs-on: self-hosted\n"
            "    steps:\n      - run: echo safe\n",
        ),
        "missing-runs-on-job.yml": (
            "a missing runner label is refused",
            "    steps:\n      - run: echo safe\n",
        ),
        "dynamic-runs-on-job.yml": (
            "a nonliteral runner label is refused",
            "    runs-on: ${{ matrix.os }}\n"
            "    steps:\n      - run: echo safe\n",
        ),
        "job-container.yml": (
            "job container authority is refused",
            "    runs-on: ubuntu-latest\n"
            "    container: alpine:3.20\n"
            "    steps:\n      - run: echo safe\n",
        ),
        "service-container.yml": (
            "service container authority is refused",
            "    runs-on: ubuntu-latest\n"
            "    services:\n      database:\n        image: postgres:16\n"
            "    steps:\n      - run: echo safe\n",
        ),
        "reusable-workflow-job.yml": (
            "reusable workflow authority is refused",
            "    uses: example/workflows/.github/workflows/build.yml@v1\n"
            "    runs-on: ubuntu-latest\n"
            "    steps:\n      - run: echo safe\n",
        ),
    }
    original_docs = WORKFLOWS["docs"]
    try:
        for filename, (label, job) in sandbox_job_workflows.items():
            (repo / filename).write_text(
                "name: sandbox-job-negative\non: push\njobs:\n"
                f"  unsafe:\n{job}",
                encoding="utf-8",
            )
            WORKFLOWS["docs"] = filename
            refused(
                label,
                lambda: validate_workflow_sandbox(repo, ("docs",)),
            )
    finally:
        WORKFLOWS["docs"] = original_docs

    forbidden_action_workflows = {
        "docker-url.yml": "docker://alpine:3.20",
        "neutral-remote-action.yml": "example/setup@v1",
        "same-namespace-version-drift.yml": "actions/checkout@v5",
        "neutral-local-action.yml": "./local-action",
    }
    local_action = repo / "local-action"
    local_action.mkdir()
    (local_action / "action.yml").write_text(
        "name: local action\nruns:\n  using: docker\n"
        "  image: Dockerfile\n",
        encoding="utf-8",
    )
    (local_action / "Dockerfile").write_text(
        "FROM alpine:3.20\n", encoding="utf-8"
    )
    try:
        for filename, action in forbidden_action_workflows.items():
            (repo / filename).write_text(
                "name: action-negative\non: push\njobs:\n"
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


def selftest_job_volume_scope(tally: SelftestTally, repo: pathlib.Path) -> None:
    """Arms: a workflow leases act job volumes by its declared name, and overlapping names cannot share."""
    check = tally.check
    refused = tally.refused
    original_docs = WORKFLOWS["docs"]
    (repo / "nameless.yml").write_text(
        "on: push\njobs:\n  safe:\n    runs-on: ubuntu-latest\n"
        "    steps:\n      - run: echo safe\n",
        encoding="utf-8",
    )
    WORKFLOWS["docs"] = "nameless.yml"
    try:
        refused(
            "a workflow without a declared name cannot lease act job volumes",
            lambda: workflow_job_volume_scope(repo, ("docs",)),
        )
    finally:
        WORKFLOWS["docs"] = original_docs
    for filename, name in (("rtl-short.yml", "rtl"), ("rtl-long.yml", "rtl-fast")):
        (repo / filename).write_text(
            f"name: {name}\non: push\njobs:\n  safe:\n    runs-on: ubuntu-latest\n"
            "    steps:\n      - run: echo safe\n",
            encoding="utf-8",
        )
    original_elaborate = WORKFLOWS["elaborate"]
    WORKFLOWS["docs"] = "rtl-short.yml"
    WORKFLOWS["elaborate"] = "rtl-long.yml"
    try:
        refused(
            "a workflow name that is a hyphen-prefix of another cannot share a lease",
            lambda: workflow_job_volume_scope(repo, ("docs", "elaborate")),
        )
        check(
            "either overlapping workflow alone still leases its own volumes",
            workflow_job_volume_scope(repo, ("docs",)) == {"docs": "act-rtl-"}
            and workflow_job_volume_scope(repo, ("elaborate",))
            == {"elaborate": "act-rtl-fast-"},
        )
    finally:
        WORKFLOWS["docs"] = original_docs
        WORKFLOWS["elaborate"] = original_elaborate


def selftest_workflow_reader(tally: SelftestTally, repo: pathlib.Path) -> None:
    """Arms: workflow reads refuse a symlink, a FIFO, a device, and an oversized file."""
    refused = tally.refused
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


def selftest_run_directory_stages(
    tally: SelftestTally, pr: PullRequest
) -> DockerFixture:
    """Every arm that needs a real run directory; the Docker fixture the later arms reuse."""
    with temporary_run_directory(False) as first_root:
        first = make_layout(first_root, pr)
        other_pr = replace(pr, head_sha="3" * 40)
        with temporary_run_directory(False) as second_root:
            second = make_layout(second_root, other_pr)
            docker = selftest_docker_fixture(first)
            selftest_act_command(tally, docker)
            selftest_container_cpu_bound(tally, docker)
            selftest_container_memory_bound(tally, docker)
            selftest_act_command_refusals(tally, docker)
            selftest_action_materialisation(tally, docker)
            selftest_action_plan(tally, docker)
            selftest_boundary_plants(tally, docker)
            selftest_boundary_probe_commands(tally, docker)
            selftest_probe_clone_runner(tally, docker)
            selftest_toolcache_ownership(tally, docker)
            selftest_toolcache_survivor(tally, docker)
            selftest_toolcache_post_accept(tally, docker)
            selftest_teardown_independence(tally, docker)
            selftest_network_setup_rollback(tally, docker)
            selftest_seed_ordering(tally, docker)
            selftest_delayed_daemon(tally, docker)
            controlled = selftest_layout_isolation(tally, first, second)
            selftest_privileged_signals(tally)
            selftest_containment_hold(tally)
            selftest_signal_latching(tally)
            selftest_worker_signal_mask(tally)
            selftest_monitor_join(tally)
            selftest_worker_cli_timeout(tally)
            selftest_private_inputs(tally, first, controlled)
    return docker


def selftest_job_volume_stages(
    tally: SelftestTally,
    docker: DockerFixture,
    inventory: list[dict[str, object]],
) -> None:
    """Every act job-volume arm, in the order the lease, gate, cleanup, and reconciliation run."""
    jobs = job_volume_fixture(docker)
    selftest_job_volume_lease(tally, jobs)
    selftest_job_volume_gate(tally, jobs)
    selftest_job_volume_name_corpus(tally)
    selftest_job_volume_records(tally, jobs)
    selftest_job_volume_cleanup(tally, docker, jobs, inventory)
    selftest_job_volume_held(tally, docker, jobs, inventory)
    selftest_job_volume_survivors(tally, docker, jobs, inventory)
    selftest_job_volume_absence(tally, jobs)
    selftest_job_volume_mounts(tally, docker, jobs, inventory)
    selftest_job_volume_leftovers(tally, docker, jobs, inventory)


def selftest_shipping_workflows(
    tally: SelftestTally, shipping_root: pathlib.Path
) -> None:
    """Arms: the shipping workflows satisfy the sandbox policy and lease disjoint act job volumes."""
    try:
        validate_workflow_sandbox(shipping_root, tuple(WORKFLOWS))
    except Refusal as exc:
        tally.check(f"shipping workflows satisfy the sandbox policy ({exc})", False)
    else:
        tally.check("shipping workflows satisfy the sandbox policy", True)
    try:
        shipping_scope = workflow_job_volume_scope(shipping_root, tuple(WORKFLOWS))
    except Refusal as exc:
        tally.check(
            f"shipping workflows lease act job volumes by declared name ({exc})",
            False,
        )
    else:
        tally.check(
            "shipping workflows lease act job volumes by declared name",
            shipping_scope
            == {
                "docs": "act-docs-",
                "elaborate": "act-elaborate-",
                "rtl-fast": "act-rtl-fast-",
                "rtl-full": "act-rtl-full-",
            },
        )
        shipping_prefixes = sorted(shipping_scope.values())
        tally.check(
            "no shipping workflow name is a hyphen-prefix of another, so a rival "
            "workflow's volumes stay outside every lease",
            not any(
                longer.startswith(shorter)
                for index, shorter in enumerate(shipping_prefixes)
                for longer in shipping_prefixes[index + 1 :]
            ),
        )


def selftest(shipping_root: pathlib.Path = ROOT) -> int:
    """Run every offline arm; RC_OK when all pass, else RC_FAILED."""
    tally = SelftestTally()
    fixture = selftest_fixture()
    pr, repository, base = fixture.pr, fixture.repository, fixture.base
    fixture_run = ValidatedRun(pr, repository, base)
    draft_raw = dict(fixture.raw)
    draft_raw["isDraft"] = True
    draft_run = ValidatedRun(PullRequest.from_json(draft_raw), repository, base)
    selftest_event_payload(tally, fixture, fixture_run, draft_run)
    resolved = selftest_base_resolution(tally, fixture)
    selftest_fetch_window(tally, fixture, resolved)
    selftest_validation_transcript(tally, fixture, resolved, shipping_root)
    selftest_workflow_order(tally, resolved, shipping_root)
    selftest_action_launch_order(tally, resolved, shipping_root)
    selftest_trusted_runner(tally, fixture, resolved)
    selftest_wiring_pins(tally)
    tally.refused(
        "a validated run cannot be built on anything but a full commit SHA",
        lambda: ValidatedRun(pr, repository, "not-a-sha"),
    )
    selftest_remote_tip_lookup(tally, fixture)
    selftest_selection_and_metadata(tally, fixture)

    docker = selftest_run_directory_stages(tally, pr)

    inventory = selftest_container_ownership(tally, docker)
    selftest_cancelled_inventory(tally, docker, inventory)
    selftest_job_volume_stages(tally, docker, inventory)
    selftest_act_version(tally)
    selftest_spawn_handoff(tally)
    selftest_surviving_group(tally)
    selftest_nested_cleanup(tally)
    selftest_docker_timeout(tally)
    child_environment = selftest_child_signal_mask(tally)

    with tempfile.TemporaryDirectory(
        prefix="act-ci-capture-signal-selftest-"
    ) as raw_capture_probe:
        capture_probe_root = pathlib.Path(raw_capture_probe)
        selftest_captured_tree_probes(tally, capture_probe_root, child_environment)
        selftest_main_entry_probe(tally, capture_probe_root)
        selftest_git_remote_helper_probes(tally, capture_probe_root)

    selftest_remote_change(tally, fixture, fixture_run)
    selftest_run_directory_rollback(tally)
    selftest_sudo_cleanup_failures(tally)
    selftest_installed_runner(tally, fixture)
    selftest_cleanup_failures(tally)

    with tempfile.TemporaryDirectory(prefix="act-ci-git-selftest-") as raw_temp:
        git_fixture = selftest_git_fixture(pathlib.Path(raw_temp), pr)
        selftest_index_flags(tally, git_fixture)
        selftest_submodule_manifest(tally, git_fixture)
        selftest_sandbox_policy(tally, git_fixture.repo)
        selftest_job_volume_scope(tally, git_fixture.repo)
        selftest_workflow_reader(tally, git_fixture.repo)

    selftest_shipping_workflows(tally, shipping_root)

    failures = tally.failures
    print("selftest:", "PASS" if failures == 0 else f"{failures} FAILURE(S)")
    return RC_OK if failures == 0 else RC_FAILED


def interrupt_selftest_sources(
    relative_workflow: str, seed_path: str, probe_path: str, marker: str
) -> dict[str, str]:
    """The three probe workflows by path: a sleeper, a cache writer, and a cache reader."""
    return {
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


def commit_interrupt_selftest_checkout(
    layout: RunLayout, workflow_sources: Mapping[str, str]
) -> None:
    """Write the probe workflows into the checkout, commit them, and write the event payload."""
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


def spawn_delayed_docker_cli_probe(
    layout: RunLayout, context: CommandContext
) -> tuple[str, str, bool]:
    """Run a volume create through a CLI that sleeps past its timeout; (token, volume, timed out)."""
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
        *isolated_command_prefix(sys.executable, context.use_sudo, context.env),
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
            context=context,
            timeout=0.2,
        )
    except subprocess.TimeoutExpired:
        cli_probe_timed_out = True
    time.sleep(2.2)
    return cli_probe_token, cli_probe_volume, cli_probe_timed_out


def require_delayed_docker_cli_contained(
    context: CommandContext,
    cli_probe_token: str,
    cli_probe_volume: str,
    cli_probe_timed_out: bool,
) -> None:
    """Refuse unless the timed-out CLI's delayed volume create never landed; a landed one is removed first."""
    cli_probe_inspect = run_docker(
        ["volume", "inspect", cli_probe_volume],
        context=context,
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
            context=context,
            description="delayed Docker CLI probe cleanup",
        )
        cli_probe_absent = run_docker(
            ["volume", "inspect", cli_probe_volume],
            context=context,
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


@dataclass(frozen=True)
class PlantedVolumes:
    """Act-shaped volumes the interrupt self-test creates itself, and the label that proves it did.

    `rival` is outside the sleeping job's lease and must survive untouched;
    `collision` is inside it and must refuse acquisition while surviving.
    `created` records intent before each create, so a create the daemon
    accepts after a CLI timeout is still reconciled by the final cleanup.
    """

    token: str
    rival: str
    collision: str
    created: list[str]


def new_planted_volumes() -> PlantedVolumes:
    """Two act-shaped volume names the runner did not create, under one fresh ownership label."""
    planted_token = secrets.token_hex(16)
    planted_digest = hashlib.sha256(planted_token.encode("ascii")).hexdigest()
    return PlantedVolumes(
        token=planted_token,
        rival=f"act-interrupt-rival-{planted_token}-{planted_digest}",
        collision=(
            f"act-interrupt-selftest-planted-{planted_token}-{planted_digest}"
        ),
        created=[],
    )


def planted_selftest_volume(
    name: str, planted: PlantedVolumes, *, context: CommandContext
) -> Mapping[str, object] | None:
    """The planted volume's record, None when absent; a foreign owner refuses."""
    volume = docker_volume_record(name, context=context)
    if volume is None:
        return None
    labels = volume.get("Labels")
    if (
        not isinstance(labels, dict)
        or labels.get(DOCKER_OWNER_LABEL) != planted.token
    ):
        raise Refusal(f"planted volume {name} ownership changed")
    return volume


def plant_selftest_volume(
    name: str, planted: PlantedVolumes, *, context: CommandContext
) -> None:
    """Create one act-shaped volume the runner did not create, labelled as planted."""
    # Record intent first: a create the daemon accepts after a CLI
    # timeout must still be reconciled by the final cleanup.
    planted.created.append(name)
    run_docker(
        [
            "volume",
            "create",
            "--label",
            f"{DOCKER_OWNER_LABEL}={planted.token}",
            name,
        ],
        context=context,
        description=f"planted volume {name} creation",
    )
    if planted_selftest_volume(name, planted, context=context) is None:
        raise Refusal(f"planted volume {name} did not appear")


def remove_planted_selftest_volume(
    name: str, planted: PlantedVolumes, *, context: CommandContext
) -> None:
    """Remove a planted volume and prove its absence; already absent is fine."""
    if planted_selftest_volume(name, planted, context=context) is None:
        return
    run_docker(
        ["volume", "rm", name],
        context=context,
        description=f"planted volume {name} removal",
    )
    if planted_selftest_volume(name, planted, context=context) is not None:
        raise Refusal(f"planted volume {name} survived removal")


def require_planted_collision_refused(
    planned: DockerBoundary,
    planted: PlantedVolumes,
    job_volume_prefix: str,
    *,
    context: CommandContext,
) -> None:
    """Plant both volumes, prove the in-scope one refuses acquisition, and leave the rival standing."""
    if (
        not ACT_JOB_VOLUME_RE.fullmatch(planted.rival)
        or is_leased_act_job_volume(planned, planted.rival)
        or not is_leased_act_job_volume(planned, planted.collision)
    ):
        raise Refusal("interrupt self-test planted names are misclassified")
    plant_selftest_volume(planted.rival, planted, context=context)
    plant_selftest_volume(planted.collision, planted, context=context)
    collision_message = ""
    try:
        with temporary_docker_boundary(
            new_docker_boundary((job_volume_prefix,)),
            context=context,
        ):
            raise Refusal(
                "collision probe acquired a boundary despite a planted "
                "in-scope act job volume"
            )
    except Refusal as exc:
        collision_message = str(exc)
    if (
        planted.collision not in collision_message
        or "already exist" not in collision_message
    ):
        raise Refusal(
            "collision probe did not refuse the planted in-scope "
            f"volume: {collision_message}"
        )
    for name in (planted.rival, planted.collision):
        if planted_selftest_volume(name, planted, context=context) is None:
            raise Refusal(f"collision refusal did not preserve {name}")
    remove_planted_selftest_volume(planted.collision, planted, context=context)


def require_act_job_volumes_reclaimed(
    observed: Sequence[str],
    job_volume_scope: Mapping[str, str],
    planted: PlantedVolumes,
    *,
    context: CommandContext,
) -> None:
    """Prove both observed job volumes and every in-scope survivor are gone, and the rival is not."""
    if len(observed) != 2:
        raise Refusal("interrupt self-test did not observe the act job volumes")
    for name in observed:
        if docker_volume_record(name, context=context) is not None:
            raise Refusal(f"interrupt self-test left act job volume {name}")
    scope_boundary = new_docker_boundary(job_volume_scope.values())
    job_volume_survivors = [
        name
        for name in list_docker_volume_names(context=context)
        if is_leased_act_job_volume(scope_boundary, name)
    ]
    if job_volume_survivors:
        raise Refusal(
            "interrupt self-test left act job volume(s): "
            + ", ".join(job_volume_survivors)
        )
    if planted_selftest_volume(planted.rival, planted, context=context) is None:
        raise Refusal(
            "interrupt cleanup removed an act-shaped volume outside its lease"
        )


def reclaim_planted_selftest_volumes(
    planted: PlantedVolumes, *, context: CommandContext
) -> list[str]:
    """Remove every planted volume; the problems found, each also printed on stderr as it happens."""
    planted_errors: list[str] = []
    for name in planted.created:
        try:
            remove_planted_selftest_volume(name, planted, context=context)
        except Refusal as exc:
            planted_errors.append(str(exc))
            # A primary failure is propagating past this scope;
            # the residue must still be attributable on stderr.
            print(
                f"act-ci: interrupt self-test: {exc}",
                file=sys.stderr,
                flush=True,
            )
    return planted_errors


def require_expected_job_mounts(
    inventory: Sequence[Mapping[str, object]],
    selected: set[str],
    boundary: DockerBoundary,
) -> list[str]:
    """The two leased volumes an act job must mount: its workspace and that name's `-env` twin."""
    mounted = owned_volume_mounts(inventory, selected)
    if (
        len(mounted) != 2
        or mounted[1] != f"{mounted[0]}-env"
        or not all(
            is_leased_act_job_volume(boundary, name)
            for name in mounted
        )
    ):
        raise Refusal(
            "act job mounted an unexpected "
            "volume set: "
            + ", ".join(mounted)
        )
    return mounted


def run_completed_live_probe(
    selected_workflow: str,
    *,
    prefix: Sequence[str],
    layout: RunLayout,
    context: CommandContext,
    job_volume_scope: Mapping[str, str],
) -> None:
    """Run `selected_workflow` to completion in a fresh boundary; a non-zero exit is a Refusal."""
    with temporary_docker_boundary(
        new_docker_boundary((job_volume_scope[selected_workflow],)),
        context=context,
    ) as probe_boundary:
        probe_command = build_act_command(
            prefix,
            selected_workflow,
            layout,
            allocate_tcp_port(),
            probe_boundary,
        )
        probe_command.append("--pull=false")
        require_act_job_volumes_absent(
            probe_boundary,
            context=context,
        )
        probe_result = run_act_process(
            probe_command,
            context=context,
        )
        if probe_result.returncode != 0:
            raise Refusal(
                f"{selected_workflow} exited "
                f"{probe_result.returncode}"
            )


@dataclass
class InterruptMonitor:
    """The worker that freezes a live act job once it is running, and the state main reads back.

    `started` is handed to run_act_process as its `started` hook and spawns the
    worker thread; main cancels and joins through `cancel`, `signal_lock`,
    `threads`, `completions`, and `problems`.
    """

    context: CommandContext
    boundary: DockerBoundary
    cancel: threading.Event = field(default_factory=threading.Event)
    frozen: threading.Event = field(default_factory=threading.Event)
    privileged_child_seen: threading.Event = field(default_factory=threading.Event)
    signal_lock: threading.Lock = field(default_factory=threading.Lock)
    problems: list[str] = field(default_factory=list)
    threads: list[threading.Thread] = field(default_factory=list)
    completions: list[threading.Event] = field(default_factory=list)
    observed_job_volumes: list[str] = field(default_factory=list)
    launched_process_group: int | None = None

    def started(self, process_group: int) -> None:
        """Record the launched group and start the monitor thread that will freeze it."""
        self.launched_process_group = process_group
        monitor_complete = threading.Event()
        monitor = threading.Thread(
            target=self.freeze_then_complete,
            args=(process_group, monitor_complete),
            name="act-ci-interrupt-monitor",
            daemon=True,
        )
        self.threads.append(monitor)
        self.completions.append(monitor_complete)
        start_cleanup_thread_or_refuse(
            monitor, "interrupt monitor"
        )

    def freeze_then_complete(
        self, process_group: int, monitor_complete: threading.Event
    ) -> None:
        """Run the freeze and mark completion however it ends."""
        try:
            self.freeze_live_act(process_group)
        finally:
            monitor_complete.set()

    def interrupt_main(self, message: str, sent_signal: int) -> None:
        """Record `message` and signal main, unless the monitor is already cancelled."""
        with self.signal_lock:
            if self.cancel.is_set():
                return
            if message:
                self.problems.append(message)
            os.kill(os.getpid(), sent_signal)

    def freeze_live_act(self, process_group: int) -> None:
        """Wait for an owned running job, then freeze its group; a missed deadline signals main."""
        deadline = time.monotonic() + 120
        while not self.cancel.is_set():
            try:
                inventory = docker_container_inventory(
                    context=self.context,
                    cancel=self.cancel,
                )
                if self.cancel.is_set():
                    return
                selected = owned_container_ids(inventory, self.boundary)
                if running_container_ids(inventory, selected):
                    self.freeze_running_job(process_group, inventory, selected)
                    return
            except Refusal:
                # Container creation/removal can race one inventory;
                # retry until the bounded deadline.
                pass
            if time.monotonic() >= deadline:
                self.interrupt_main(
                    "no owned running act container appeared "
                    "within 120s",
                    signal.SIGINT,
                )
                return
            self.cancel.wait(0.25)

    def freeze_running_job(
        self,
        process_group: int,
        inventory: Sequence[Mapping[str, object]],
        selected: set[str],
    ) -> None:
        """Verify the running job's cache and volume mounts and group, STOP it, and signal main."""
        use_sudo = self.context.use_sudo
        if self.cancel.is_set():
            return
        try:
            inspect_act_toolcache_volume(
                self.boundary,
                context=self.context,
            )
            if self.cancel.is_set():
                return
            verify_runner_toolcache_mounts(
                inventory,
                self.boundary,
                require_any=True,
            )
            self.observed_job_volumes[:] = require_expected_job_mounts(
                inventory, selected, self.boundary
            )
        except Refusal as exc:
            self.interrupt_main(str(exc), signal.SIGINT)
            return
        if self.cancel.is_set():
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
                self.privileged_child_seen.set()
            if self.cancel.is_set():
                return
        except (OSError, Refusal) as exc:
            self.interrupt_main(
                f"cannot freeze live act process: {exc}",
                signal.SIGINT,
            )
            return
        # Cancellation and the privileged STOP are
        # one serialized transition. Main cannot
        # begin Docker teardown until this worker
        # either completes the injection or exits.
        with self.signal_lock:
            if self.cancel.is_set():
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
                self.frozen.set()
                os.kill(os.getpid(), signal.SIGINT)
            except (OSError, Refusal) as exc:
                self.problems.append(
                    "cannot freeze live act process: "
                    f"{exc}"
                )
                os.kill(os.getpid(), signal.SIGINT)


def interrupt_live_act(command: Sequence[str], monitor: InterruptMonitor) -> None:
    """Run act until `monitor` freezes it and signals main; refuse unless the frozen group is gone."""
    use_sudo = monitor.context.use_sudo
    interrupted_signal: int | None = None
    try:
        require_act_job_volumes_absent(
            monitor.boundary, context=monitor.context
        )
        result = run_act_process(
            command,
            context=monitor.context,
            started=monitor.started,
        )
    except (KeyboardInterrupt, TerminationRequest) as exc:
        if (
            isinstance(exc, TerminationRequest)
            and exc.signum not in (signal.SIGINT, signal.SIGTERM)
        ):
            raise
        interrupted_signal = (
            signal.SIGINT
            if isinstance(exc, KeyboardInterrupt)
            else exc.signum
        )
    finally:
        cancel_and_join_cleanup_threads(
            monitor.cancel,
            monitor.signal_lock,
            list(
                zip(
                    monitor.threads,
                    monitor.completions,
                    strict=True,
                )
            ),
            monitor.problems,
        )
    if interrupted_signal is None:
        raise Refusal(
            f"interrupt self-test act process exited {result.returncode} "
            "before fault injection"
        )
    if interrupted_signal != signal.SIGINT:
        raise Refusal(
            "interrupt self-test did not deliver the expected SIGINT"
        )
    if monitor.problems:
        raise Refusal(monitor.problems[0])
    if not monitor.frozen.is_set():
        raise Refusal("interrupt self-test did not freeze act")
    if use_sudo and not monitor.privileged_child_seen.is_set():
        raise Refusal("interrupt self-test did not inspect root act")
    if monitor.launched_process_group is None:
        raise Refusal("interrupt self-test did not record the act group")
    if process_group_exists(
        monitor.launched_process_group, use_sudo=use_sudo
    ):
        raise Refusal("interrupt self-test left an act process-group member")


def interrupt_selftest_pull_request() -> PullRequest:
    """The synthetic PR the interrupt self-test materializes its probe workflows under."""
    return PullRequest(
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


def run_interrupt_probe(
    workflows: Sequence[str],
    layout: RunLayout,
    prefix: Sequence[str],
    planted: PlantedVolumes,
    reaped: threading.Event,
    *,
    context: CommandContext,
) -> DockerBoundary:
    """Seed, probe, then freeze and reclaim one interrupted act job; the boundary it was planned in.

    `workflows` is the interrupted workflow followed by the tool-cache seed
    and probe workflows, in that order.
    """
    workflow, seed_workflow, probe_workflow = workflows
    job_volume_scope = workflow_job_volume_scope(
        layout.checkout, (workflow, seed_workflow, probe_workflow)
    )

    run_completed_live_probe(
        seed_workflow,
        prefix=prefix,
        layout=layout,
        context=context,
        job_volume_scope=job_volume_scope,
    )
    require_act_toolcache_absent(context=context)
    run_completed_live_probe(
        probe_workflow,
        prefix=prefix,
        layout=layout,
        context=context,
        job_volume_scope=job_volume_scope,
    )
    require_act_toolcache_absent(context=context)

    planned = new_docker_boundary((job_volume_scope[workflow],))
    require_planted_collision_refused(
        planned, planted, job_volume_scope[workflow], context=context
    )
    with temporary_docker_boundary(
        planned,
        context=context,
    ) as boundary:
        command = build_act_command(
            prefix,
            workflow,
            layout,
            allocate_tcp_port(),
            boundary,
        )
        command.append("--pull=false")
        monitor = InterruptMonitor(context=context, boundary=boundary)
        interrupt_live_act(command, monitor)
        reaped.set()
    require_act_job_volumes_reclaimed(
        monitor.observed_job_volumes,
        job_volume_scope,
        planted,
        context=context,
    )
    return planned


def release_interrupt_selftest_workflows(
    planted: PlantedVolumes, workflows: Sequence[str], *, context: CommandContext
) -> list[str]:
    """Reclaim every planted volume and drop the probe workflows; the problems found."""
    with blocked_cleanup_signals():
        planted_errors = reclaim_planted_selftest_volumes(planted, context=context)
        for selected_workflow in workflows:
            WORKFLOWS.pop(selected_workflow, None)
    return planted_errors


def require_interrupt_selftest_residue_absent(
    planned: DockerBoundary, reaped: threading.Event, *, context: CommandContext
) -> None:
    """Prove no owned container, tool-cache volume, or process group survived the interrupted run."""
    final_inventory = docker_container_inventory(context=context)
    survivors = owned_container_ids(final_inventory, planned)
    if survivors:
        raise Refusal(
            f"interrupt self-test left {len(survivors)} owned container(s)"
        )
    require_act_toolcache_absent(context=context)
    if not reaped.is_set():
        raise Refusal("interrupt self-test did not prove process-group absence")


def interrupt_selftest(act_binary: str, use_sudo: bool) -> int:
    """Prove tool-cache separation, then SIGINT act and verify cleanup."""
    probe_pr = interrupt_selftest_pull_request()
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
        workflow_sources = interrupt_selftest_sources(
            relative_workflow, seed_path, probe_path, marker
        )
        commit_interrupt_selftest_checkout(layout, workflow_sources)
        env = controlled_act_environment(layout)
        context = CommandContext(use_sudo=use_sudo, cwd=layout.invocation, env=env)
        validate_isolation_layout(layout)
        prefix = require_runtime(act_binary, use_sudo, layout, env)

        planted = new_planted_volumes()
        rival_preserved = False
        process_group_reaped = threading.Event()

        cli_probe_token, cli_probe_volume, cli_probe_timed_out = (
            spawn_delayed_docker_cli_probe(layout, context)
        )
        require_delayed_docker_cli_contained(
            context, cli_probe_token, cli_probe_volume, cli_probe_timed_out
        )

        try:
            WORKFLOWS[workflow] = relative_workflow
            WORKFLOWS[seed_workflow] = seed_path
            WORKFLOWS[probe_workflow] = probe_path
            planned = run_interrupt_probe(
                (workflow, seed_workflow, probe_workflow),
                layout,
                prefix,
                planted,
                process_group_reaped,
                context=context,
            )
            rival_preserved = True
        finally:
            planted_errors = release_interrupt_selftest_workflows(
                planted, (workflow, seed_workflow, probe_workflow), context=context
            )
        if planted_errors:
            raise Refusal(
                "interrupt self-test planted volume cleanup failed: "
                + "; ".join(planted_errors)
            )
        if not rival_preserved:
            raise Refusal("interrupt self-test did not prove rival volume preservation")

        require_interrupt_selftest_residue_absent(
            planned, process_group_reaped, context=context
        )
    if run_root.exists() or run_root.is_symlink():
        raise Refusal("interrupt self-test left its exact run directory")
    print(
        "interrupt-selftest: PASS (SIGINT returned after the frozen act process "
        "group, containers, network, tool-cache volume, both act job volumes, "
        "and run directory were absent; a planted in-scope volume refused "
        "acquisition and a planted rival volume survived; the tool cache did "
        "not cross runs)"
    )
    return RC_OK


BOUNDARY_PROBE_WORKFLOW = "boundary-probe-selftest"
BOUNDARY_PROBE_PATH = ".github/workflows/boundary-probe-selftest.yml"
#: The probe job reports by name and state only: `boundary-probe <name>=<state>`.
BOUNDARY_PROBE_LINE_RE = re.compile(r"boundary-probe ([a-z-]+)=(visible|absent|other)\b")
#: Every check the probe job reports. The first three separate a boundaried
#: launch from an unboundaried one; the last three are absent under both,
#: because act forwards no operator environment or home directory on its
#: own, and are reported so the transcript states that rather than assumes it.
BOUNDARY_PROBE_NAMES = (
    "token",
    "docker-socket",
    "host-loopback",
    "ssh-agent",
    "proxy-env",
    "credential-files",
)
BOUNDARY_DISCRIMINATORS = ("token", "docker-socket", "host-loopback")
#: The operator-environment names the plants occupy. None may reach act,
#: the job container, or the runner's own git.
PLANTED_ENVIRONMENT_NAMES = (
    "GITHUB_TOKEN",
    "GH_TOKEN",
    "HTTPS_PROXY",
    "https_proxy",
    "HTTP_PROXY",
    "http_proxy",
    "ALL_PROXY",
    "all_proxy",
    "SSH_AUTH_SOCK",
    "GIT_SSH_COMMAND",
)
#: GitHub answers a clone of a repository that does not exist with a
#: credential challenge, so git consults every credential source its
#: environment offers before it fails; that is the host-side probe.
CREDENTIAL_CHALLENGE_URL = "https://github.com/kebag-logic/act-ci-boundary-selftest-absent"
SSH_PROBE_URL = "ssh://git@github.com/kebag-logic/milan-fpga.git"
#: A probe clone reaches a loopback recorder or GitHub's credential challenge;
#: minutes is generous, and the run is a refusal rather than a hang beyond it.
PROBE_CLONE_TIMEOUT = 5 * 60
PLANTED_PROXY_RESPONSE = (
    b"HTTP/1.1 407 Proxy Authentication Required\r\n"
    b'Proxy-Authenticate: Basic realm="planted"\r\n'
    b"Content-Length: 0\r\nConnection: close\r\n\r\n"
)


@dataclass(frozen=True)
class BoundaryPlants:
    """The fake operator secrets one boundary self-test plants, and where their recorders write.

    Every value is invented for the run: a token, a credential store, a netrc
    line, a `gh` host file, a Docker auth file, a credential helper and an SSH
    command that only record being invoked, an agent socket nothing answers,
    and a proxy on the loopback interface that records who presents
    credentials to it.
    """

    home: pathlib.Path
    token: str
    helper_log: pathlib.Path
    ssh_log: pathlib.Path
    proxy_log: pathlib.Path
    agent_socket: pathlib.Path
    proxy_port: int
    loopback_port: int

    @property
    def proxy_url(self) -> str:
        """The planted proxy with the planted credential in it, as an operator's shell might carry it."""
        return f"http://planted:{self.token}@127.0.0.1:{self.proxy_port}"

    def environment(self, *, proxied: bool = True) -> dict[str, str]:
        """The operator environment with every plant present, as an unboundaried launch inherits it."""
        environment = {
            "PATH": SAFE_PATH,
            "HOME": str(self.home),
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "GITHUB_TOKEN": self.token,
            "GH_TOKEN": self.token,
            "SSH_AUTH_SOCK": str(self.agent_socket),
            "GIT_SSH_COMMAND": str(self.home / "planted-ssh"),
        }
        if proxied:
            for name in PLANTED_ENVIRONMENT_NAMES:
                if name.lower().endswith("_proxy"):
                    environment[name] = self.proxy_url
        return environment


class PlantedProxyServer(socketserver.ThreadingTCPServer):
    """A loopback proxy that answers every request with 407 and records what it was shown."""

    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, log_path: pathlib.Path) -> None:
        """Bind an ephemeral loopback port and record requests to `log_path`."""
        self.log_path = log_path
        super().__init__(("127.0.0.1", 0), PlantedProxyHandler)


class PlantedProxyHandler(socketserver.StreamRequestHandler):
    """Record one request's first line and whether it carried proxy credentials, never the value."""

    def handle(self) -> None:
        """Read the request line and headers, append one record line, answer 407."""
        request = self.rfile.readline(4096).decode("latin-1", "replace").strip()
        credentials = "absent"
        for _ in range(64):
            header = self.rfile.readline(4096)
            if not header or header in (b"\r\n", b"\n"):
                break
            if header.lower().startswith(b"proxy-authorization:"):
                credentials = "present"
        log_path = getattr(self.server, "log_path")
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(f"{request} proxy-authorization={credentials}\n")
        self.wfile.write(PLANTED_PROXY_RESPONSE)


class LoopbackMarkerHandler(socketserver.StreamRequestHandler):
    """Answer a connection on the host loopback listener; reaching it is what the probe reports."""

    def handle(self) -> None:
        """Write one marker line and close."""
        self.wfile.write(b"planted host service\n")


@contextlib.contextmanager
def planted_loopback_services(root: pathlib.Path) -> Iterator[tuple[int, int]]:
    """Serve the planted proxy, the loopback marker and an agent socket under `root`; (proxy, marker) ports."""
    proxy = PlantedProxyServer(root / "proxy.log")
    marker = socketserver.TCPServer(("127.0.0.1", 0), LoopbackMarkerHandler)
    agent = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    agent.bind(str(root / "agent.sock"))
    agent.listen(1)
    threads = [
        threading.Thread(target=server.serve_forever, daemon=True)
        for server in (proxy, marker)
    ]
    for thread in threads:
        thread.start()
    try:
        yield proxy.server_address[1], marker.server_address[1]
    finally:
        for server in (proxy, marker):
            server.shutdown()
            server.server_close()
        agent.close()
        for thread in threads:
            thread.join(timeout=5)


def plant_boundary_secrets(root: pathlib.Path, ports: tuple[int, int]) -> BoundaryPlants:
    """Write the planted operator home, the two recorders and their logs beneath `root`; the plants."""
    token = f"ghp_planted{secrets.token_hex(8)}"
    home = root / "planted-home"
    for directory in (home / ".ssh", home / ".config" / "gh", home / ".docker"):
        directory.mkdir(parents=True, exist_ok=True)
    helper_log = root / "credential-helper.log"
    ssh_log = root / "ssh-command.log"
    for log in (helper_log, ssh_log, root / "proxy.log"):
        log.touch()
    helper = home / "planted-credential-helper"
    helper.write_text(
        "#!/bin/sh\n"
        f"printf 'called %s\\n' \"$1\" >> '{helper_log}'\n"
        "if [ \"$1\" = get ]; then\n"
        f"  printf 'username=planted\\npassword=%s\\n' '{token}'\n"
        "fi\n",
        encoding="utf-8",
    )
    (home / "planted-ssh").write_text(
        "#!/bin/sh\n"
        f"printf 'invoked agent=%s\\n' \"${{SSH_AUTH_SOCK:-unset}}\" >> '{ssh_log}'\n"
        "exit 255\n",
        encoding="utf-8",
    )
    for script in (helper, home / "planted-ssh"):
        script.chmod(0o700)
    (home / ".gitconfig").write_text(
        f"[credential]\n\thelper = {helper}\n"
        "[user]\n\tname = planted\n\temail = planted@example.invalid\n",
        encoding="utf-8",
    )
    (home / ".git-credentials").write_text(f"https://planted:{token}@github.com\n", encoding="utf-8")
    (home / ".netrc").write_text(f"machine github.com login planted password {token}\n", encoding="utf-8")
    (home / ".config" / "gh" / "hosts.yml").write_text(
        f"github.com:\n    oauth_token: {token}\n    user: planted\n", encoding="utf-8"
    )
    (home / ".docker" / "config.json").write_text(
        json.dumps({"auths": {"ghcr.io": {"auth": token}}}) + "\n", encoding="utf-8"
    )
    for private in (home / ".git-credentials", home / ".netrc"):
        private.chmod(0o600)
    return BoundaryPlants(
        home=home,
        token=token,
        helper_log=helper_log,
        ssh_log=ssh_log,
        proxy_log=root / "proxy.log",
        agent_socket=root / "agent.sock",
        proxy_port=ports[0],
        loopback_port=ports[1],
    )


@contextlib.contextmanager
def planted_operator_environment(plants: BoundaryPlants) -> Iterator[None]:
    """Put every plant into this process's own environment while the body runs, then restore it."""
    saved = {name: os.environ.get(name) for name in (*PLANTED_ENVIRONMENT_NAMES, "HOME")}
    os.environ.update(plants.environment())
    try:
        yield
    finally:
        for name, value in saved.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value


def boundary_probe_sources(plants: BoundaryPlants) -> dict[str, str]:
    """The probe workflow by path: one job reporting, by name and state only, which plants it can see."""
    lines = [
        "set -uo pipefail",
        "report() { printf 'boundary-probe %s=%s\\n' \"$1\" \"$2\"; }",
        f'if [ "${{PROBE_TOKEN:-}}" = "{plants.token}" ]; then report token visible',
        'elif [ -n "${PROBE_TOKEN:-}" ]; then report token other',
        "else report token absent; fi",
        "if [ -S /var/run/docker.sock ]; then report docker-socket visible",
        "else report docker-socket absent; fi",
        f"if (exec 3<>/dev/tcp/127.0.0.1/{plants.loopback_port}) 2>/dev/null",
        "then report host-loopback visible; else report host-loopback absent; fi",
        'if [ -n "${SSH_AUTH_SOCK:-}" ] && [ -S "$SSH_AUTH_SOCK" ]; then report ssh-agent visible',
        "else report ssh-agent absent; fi",
        "if env | grep -qiE '^(https?_proxy|all_proxy)='; then report proxy-env visible",
        "else report proxy-env absent; fi",
        'if [ -e "$HOME/.git-credentials" ] || [ -e "$HOME/.netrc" ] \\',
        '   || [ -e "$HOME/.config/gh/hosts.yml" ] \\',
        '   || [ -n "$(git config --global --get-all credential.helper 2>/dev/null)" ]',
        "then report credential-files visible; else report credential-files absent; fi",
        "exit 0",
    ]
    script = "".join(f"          {line}\n" for line in lines)
    return {
        BOUNDARY_PROBE_PATH: (
            f"name: {BOUNDARY_PROBE_WORKFLOW}\n"
            "on: pull_request\n"
            "jobs:\n"
            "  probe:\n"
            "    runs-on: ubuntu-latest\n"
            "    env:\n"
            "      PROBE_TOKEN: ${{ secrets.GITHUB_TOKEN }}\n"
            "    steps:\n"
            "      - shell: bash\n"
            "        run: |\n" + script
        )
    }


def parse_probe_transcript(text: str) -> dict[str, str]:
    """The probe's `name=state` reports found in `text`, the last report per name."""
    return {match.group(1): match.group(2) for match in BOUNDARY_PROBE_LINE_RE.finditer(text)}


def grade_probe_transcript(text: str, arm: str) -> list[str]:
    """The problems with one arm's transcript: a check not reported, or a state that arm forbids.

    The boundary arm must report every check absent. The leaky arm must report
    the three discriminators visible: a probe that cannot see a removed
    boundary proves nothing when it reports the real one intact.
    """
    reports = parse_probe_transcript(text)
    problems: list[str] = []
    for name in BOUNDARY_PROBE_NAMES:
        state = reports.get(name)
        if state is None:
            problems.append(f"{arm} arm: {name} was not reported")
        elif arm == "boundary" and state != "absent":
            problems.append(f"{arm} arm: {name} is {state}")
        elif arm == "leaky" and name in BOUNDARY_DISCRIMINATORS and state != "visible":
            problems.append(f"{arm} arm: {name} is {state}, so the probe cannot see a removed boundary")
    return problems


def require_boundary_present(command: Sequence[str], boundary: DockerBoundary) -> None:
    """Refuse a boundary-arm act command that lacks the empty token, the disabled socket, or the owned network."""
    words = list(command)
    pairs = (
        ("--secret", "GITHUB_TOKEN="),
        ("--container-daemon-socket", "-"),
        ("--network", boundary.name),
    )
    for flag, value in pairs:
        if flag not in words or words[words.index(flag) + 1] != value:
            raise Refusal(f"boundary arm command does not carry {flag} {value}")
    if "sudo" in pathlib.Path(words[0]).name and "-i" not in words[: words.index("pull_request")]:
        raise Refusal("boundary arm command under sudo does not start act from an empty environment")


def require_boundary_removed(command: Sequence[str]) -> None:
    """Refuse a leaky-arm act command that still carries any part of the boundary."""
    words = list(command)
    head = words[: words.index("pull_request")]
    for flag in ("--container-daemon-socket", "--network"):
        if flag in words:
            raise Refusal(f"leaky arm command still carries {flag}")
    if "--secret" not in words or words[words.index("--secret") + 1] != "GITHUB_TOKEN":
        raise Refusal("leaky arm command does not source GITHUB_TOKEN from the environment")
    if "-i" in head:
        raise Refusal("leaky arm command still empties the environment")


def leaky_act_command(
    command: Sequence[str], plants: BoundaryPlants, use_sudo: bool
) -> list[str]:
    """`command` with its boundary removed: operator environment, env-sourced token, socket mount, host network.

    This is the control arm. Everything else, including the ownership label
    that lets the runner reclaim the container, is kept.
    """
    words = list(command)
    act_index = words.index("pull_request") - 1
    arguments = words[act_index + 1 :]
    for flag in ("--container-daemon-socket", "--network"):
        position = arguments.index(flag)
        del arguments[position : position + 2]
    secret = arguments.index("--secret")
    if arguments[secret + 1] != "GITHUB_TOKEN=":
        raise Refusal("boundary command does not carry the explicit empty GITHUB_TOKEN")
    arguments[secret + 1] = "GITHUB_TOKEN"
    if not use_sudo:
        return [words[act_index], *arguments]
    assignments = [f"{key}={value}" for key, value in sorted(plants.environment().items())]
    return [
        require_tool("sudo"),
        "-n",
        "--",
        require_tool("env"),
        *assignments,
        words[act_index],
        *arguments,
    ]


def transcript_popen(path: pathlib.Path) -> Callable[..., subprocess.Popen[object]]:
    """A Popen that appends the child's stdout and stderr to `path`, so a transcript can be graded."""

    def popen(command: Sequence[str], **kwargs: object) -> subprocess.Popen[object]:
        """Start `command` with both streams appended to the transcript file."""
        with path.open("ab") as handle:
            return subprocess.Popen(command, stdout=handle, stderr=subprocess.STDOUT, **kwargs)

    return popen


@dataclass(frozen=True)
class BoundaryProbeRun:
    """What one probe arm launches through: the run layout, the act prefix, the job-volume scope and the plants."""

    layout: RunLayout
    prefix: Sequence[str]
    scope: Mapping[str, str]
    plants: BoundaryPlants


def run_probe_arm(probe: BoundaryProbeRun, context: CommandContext, *, leaky: bool) -> str:
    """Run the probe job once, through the boundary or with it removed; act's transcript."""
    arm = "leaky" if leaky else "boundary"
    transcript = probe.layout.temporary / f"{arm}-probe.log"
    with temporary_docker_boundary(
        new_docker_boundary((probe.scope[BOUNDARY_PROBE_WORKFLOW],)),
        context=context,
    ) as boundary:
        command = build_act_command(
            probe.prefix, BOUNDARY_PROBE_WORKFLOW, probe.layout, allocate_tcp_port(), boundary
        )
        command.append("--pull=false")
        arm_context = context
        if leaky:
            command = leaky_act_command(command, probe.plants, context.use_sudo)
            arm_context = replace(context, env=probe.plants.environment())
            require_boundary_removed(command)
        else:
            require_boundary_present(command, boundary)
        require_act_job_volumes_absent(boundary, context=context)
        result = run_act_process(
            command,
            context=arm_context,
            seams=ProcessSeams(popen=transcript_popen(transcript)),
        )
    text = transcript.read_text(encoding="utf-8", errors="replace")
    if result.returncode != 0:
        tail = " / ".join(text.strip().splitlines()[-3:])
        raise Refusal(f"{arm} probe job exited {result.returncode}: {tail}")
    return text


def run_probe_clone(
    command: Sequence[str],
    *,
    env: Mapping[str, str],
    cwd: pathlib.Path,
    label: str,
    grace: float = 5.0,
) -> str:
    """Run a probe clone that must fail, in its own session; its last stderr line.

    Every probe clone fails by design: at a credential challenge with no
    credential source, at a refused transport, at a proxy that answers 407, or
    through an SSH command that exits 255. When git dies that way its remote
    helper outlives it by some milliseconds, which `capture`'s instantaneous
    process-group check reads as a survivor, so the group is given `grace`
    seconds to drain; one that outlives them is killed and is a Refusal, as is
    a clone that succeeds.
    """
    try:
        with deferred_cleanup_signal_delivery():
            process = subprocess.Popen(
                list(command),
                cwd=cwd,
                env=dict(env),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True,
            )
    except OSError as exc:
        raise Refusal(f"cannot start the {label} clone: {exc}") from exc
    try:
        _stdout, stderr = process.communicate(timeout=PROBE_CLONE_TIMEOUT)
        deadline = time.monotonic() + grace
        while process_group_exists(process.pid, use_sudo=False):
            if time.monotonic() >= deadline:
                raise Refusal(
                    f"the {label} clone's process group survived {grace:g} s after "
                    "its leader exited and was killed"
                )
            time.sleep(0.01)
    except (subprocess.TimeoutExpired, Refusal):
        with blocked_cleanup_signals(), contextlib.suppress(ProcessLookupError):
            os.killpg(process.pid, signal.SIGKILL)
        process.wait()
        raise
    if process.returncode == 0:
        raise Refusal(f"the {label} clone succeeded against a URL that must fail")
    lines = stderr.strip().splitlines()
    return lines[-1] if lines else f"exit {process.returncode} with no stderr"


def host_boundary_arm(plants: BoundaryPlants, layout: RunLayout) -> list[str]:
    """Run the runner's own git at a credential challenge and an SSH URL with every plant present; the problems.

    Both clones must fail for the boundary's reason: the challenge with prompts
    disabled and no credential source, the SSH URL as a refused transport. The
    recorders must have seen nothing.
    """
    problems: list[str] = []
    env = git_environment(layout.home)
    expectations = (
        ("challenge", CREDENTIAL_CHALLENGE_URL, "terminal prompts disabled"),
        ("ssh", SSH_PROBE_URL, "not allowed"),
    )
    for label, url, expected in expectations:
        target = layout.temporary / f"boundary-{label}"
        try:
            text = run_probe_clone(
                [*git_prefix(), "clone", "--quiet", url, str(target)],
                env=env,
                cwd=layout.root,
                label=f"boundary {label}",
            )
        except Refusal as exc:
            problems.append(str(exc))
            continue
        if expected not in text:
            problems.append(f"boundary {label} clone failed for another reason: {text}")
    problems.extend(recorder_activity(plants, "boundary"))
    return problems


def recorder_activity(plants: BoundaryPlants, arm: str) -> list[str]:
    """One problem per planted recorder that holds a record, named for `arm`."""
    recorders = (
        ("credential helper", plants.helper_log),
        ("SSH command", plants.ssh_log),
        ("proxy", plants.proxy_log),
    )
    return [
        f"{arm} arm: the planted {name} recorded activity: {log.read_text(encoding='utf-8').strip()!r}"
        for name, log in recorders
        if log.read_text(encoding="utf-8").strip()
    ]


def host_leaky_arm(plants: BoundaryPlants, layout: RunLayout) -> list[str]:
    """Run plain git under the planted operator environment; every recorder must record its use.

    The proxied clone must present the planted proxy credential, the direct
    clone must consult the planted credential helper, and the SSH clone must
    run the planted SSH command with the planted agent socket. Each clone
    fails, because every plant is fake; the records are the result.
    """
    problems: list[str] = []
    git = require_tool("git")
    proxied = plants.environment()
    direct = plants.environment(proxied=False)
    clones = (
        ("proxied", CREDENTIAL_CHALLENGE_URL, proxied),
        ("direct", CREDENTIAL_CHALLENGE_URL, direct),
        ("ssh", SSH_PROBE_URL, direct),
    )
    for label, url, env in clones:
        target = layout.temporary / f"leaky-{label}"
        try:
            run_probe_clone(
                [git, "clone", "--quiet", url, str(target)],
                env=env,
                cwd=layout.root,
                label=f"leaky {label}",
            )
        except Refusal as exc:
            problems.append(str(exc))
    proxy_text = plants.proxy_log.read_text(encoding="utf-8")
    if "CONNECT github.com:443" not in proxy_text or "proxy-authorization=present" not in proxy_text:
        problems.append("leaky arm: the planted proxy saw no authenticated CONNECT from the unboundaried clone")
    if "called get" not in plants.helper_log.read_text(encoding="utf-8"):
        problems.append("leaky arm: the planted credential helper was not consulted by the unboundaried clone")
    if f"agent={plants.agent_socket}" not in plants.ssh_log.read_text(encoding="utf-8"):
        problems.append("leaky arm: the planted SSH command did not run with the planted agent socket")
    return problems


def run_boundary_arms(probe: BoundaryProbeRun, context: CommandContext) -> list[str]:
    """Boundary arms first, with every plant in place, then the leaky arms; every problem found."""
    problems = grade_probe_transcript(run_probe_arm(probe, context, leaky=False), "boundary")
    problems += host_boundary_arm(probe.plants, probe.layout)
    problems += grade_probe_transcript(run_probe_arm(probe, context, leaky=True), "leaky")
    problems += host_leaky_arm(probe.plants, probe.layout)
    return problems


def boundary_selftest_pull_request() -> PullRequest:
    """The synthetic PR the boundary self-test materializes its probe workflow under."""
    return replace(
        interrupt_selftest_pull_request(),
        head_ref="boundary-selftest",
        head_sha="3" * 40,
    )


def boundary_selftest(act_binary: str, use_sudo: bool) -> int:
    """Live negative control for the credential boundary (#337).

    Plants every operator secret the boundary must withhold, runs a probe job
    and the runner's own git through the boundary and requires them to see
    none of it, then runs the same probe and plain git with the boundary
    removed and requires them to see the plants. The second half is what
    makes the first half evidence rather than silence.
    """
    problems: list[str] = []
    with temporary_run_directory(use_sudo) as run_root:
        layout = make_layout(run_root, boundary_selftest_pull_request())
        layout.checkout.mkdir(parents=True)
        planted_root = run_root / "planted"
        planted_root.mkdir()
        with planted_loopback_services(planted_root) as ports:
            plants = plant_boundary_secrets(planted_root, ports)
            commit_interrupt_selftest_checkout(layout, boundary_probe_sources(plants))
            env = controlled_act_environment(layout)
            context = CommandContext(use_sudo=use_sudo, cwd=layout.invocation, env=env)
            validate_isolation_layout(layout)
            prefix = require_runtime(act_binary, use_sudo, layout, env)
            WORKFLOWS[BOUNDARY_PROBE_WORKFLOW] = BOUNDARY_PROBE_PATH
            try:
                validate_workflow_sandbox(layout.checkout, (BOUNDARY_PROBE_WORKFLOW,))
                scope = workflow_job_volume_scope(layout.checkout, (BOUNDARY_PROBE_WORKFLOW,))
                probe = BoundaryProbeRun(layout, prefix, scope, plants)
                with planted_operator_environment(plants):
                    problems = run_boundary_arms(probe, context)
            finally:
                with blocked_cleanup_signals():
                    WORKFLOWS.pop(BOUNDARY_PROBE_WORKFLOW, None)
    if run_root.exists() or run_root.is_symlink():
        raise Refusal("boundary self-test left its exact run directory")
    if problems:
        raise Refusal("boundary self-test: " + "; ".join(problems))
    print(
        "boundary-selftest: PASS (with a planted token, credential helper, credential "
        "store, netrc, gh and Docker auth files, SSH agent and command, and an "
        "authenticated proxy in the operator environment, the boundaried probe job "
        "and the runner's git saw none of them and every recorder stayed silent; the "
        "same probe and plain git with the boundary removed saw the token, the "
        "Docker socket and the host loopback, presented the proxy credential, "
        "consulted the credential helper and ran the SSH command with the agent)"
    )
    return RC_OK



def build_argument_parser() -> argparse.ArgumentParser:
    """The runner's command-line parser."""
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
        help="SIGINT a frozen live act job and verify cleanup (requires Docker)",
    )
    parser.add_argument(
        "--boundary-selftest",
        action="store_true",
        help=(
            "plant operator secrets, prove the boundaried probe job and git see none, "
            "then prove the same probe sees them once the boundary is removed "
            "(requires Docker)"
        ),
    )
    return parser


def main(argv: Sequence[str]) -> int:
    """Parse `argv` and run the selected mode; a Refusal is printed and returns RC_REFUSED."""
    parser = build_argument_parser()
    args = parser.parse_args(argv[1:])

    if args.selftest:
        if (
            args.pr is not None
            or args.workflow
            or args.dry_run
            or args.trusted_install_sha256
            or args.interrupt_selftest
            or args.boundary_selftest
        ):
            parser.error("--selftest cannot be combined with PR-run arguments")
        shipping_root = (args.worktree or ROOT).expanduser().resolve()
        return selftest(shipping_root)
    if args.interrupt_selftest or args.boundary_selftest:
        flag = "--boundary-selftest" if args.boundary_selftest else "--interrupt-selftest"
        if (
            args.pr is not None
            or args.workflow
            or args.dry_run
            or args.trusted_install_sha256
            or args.repo is not None
            or args.worktree is not None
            or (args.interrupt_selftest and args.boundary_selftest)
        ):
            parser.error(
                f"{flag} cannot be combined with PR-run arguments or the other live self-test"
            )
        live_selftest = boundary_selftest if args.boundary_selftest else interrupt_selftest
        try:
            act_binary = resolve_act_binary(args.act_bin)
            validate_act_binary(act_binary, pathlib.Path.cwd().resolve())
            return run_with_cleanup_signals(
                lambda: live_selftest(act_binary, args.sudo)
            )
        except Refusal as exc:
            print(f"act-ci: REFUSED: {exc}", file=sys.stderr)
            return RC_REFUSED
    if args.pr is None or args.pr <= 0:
        parser.error("--pr requires a positive pull-request number")

    def execute_pr_run() -> int:
        """Validate the PR, the runner, and act, then run the selected workflows."""
        validate_bootstrap_options(
            args.trusted_install_sha256, args.repo, args.worktree
        )
        workflows = select_workflows(args.workflow)
        repository = args.repo or repository_name()
        pr = query_pull_request(args.pr, repository)
        validate_pull_request(pr, repository)
        run = resolve_validation_base(pr, repository)
        candidate_worktree = (args.worktree or pathlib.Path.cwd()).expanduser().resolve()
        validate_runner(run, candidate_worktree, args.trusted_install_sha256)
        act_binary = resolve_act_binary(args.act_bin)
        validate_act_binary(act_binary, candidate_worktree)
        return run_validation(
            run,
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
