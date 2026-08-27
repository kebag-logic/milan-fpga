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
MIN_ACT_VERSION = (0, 2, 89)
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
REPOSITORY_RE = re.compile(
    r"^[A-Za-z0-9](?:[A-Za-z0-9_.-]{0,98}[A-Za-z0-9])?/"
    r"[A-Za-z0-9](?:[A-Za-z0-9_.-]{0,98}[A-Za-z0-9])?$"
)
ACT_VERSION_RE = re.compile(r"\b(\d+)\.(\d+)\.(\d+)\b")
SAFE_PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
MAX_WORKFLOW_BYTES = 1024 * 1024
MAX_GITMODULES_BYTES = 64 * 1024
DOCKER_ID_RE = re.compile(r"^[0-9a-f]{64}$")
DOCKER_OWNER_LABEL = "org.kebag-logic.milan-act-ci.owner"
DOCKER_COMMAND_TIMEOUT = 30

WORKFLOWS: dict[str, str] = {
    "docs": ".github/workflows/docs.yml",
    "elaborate": ".github/workflows/elaborate.yml",
    "rtl-fast": ".github/workflows/rtl-fast.yml",
    "rtl-full": ".github/workflows/rtl.yml",
}
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
    """One unpredictable, runner-owned Docker network and ownership label."""

    token: str
    name: str
    network_id: str | None = None
    gateway: str | None = None


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
        result = subprocess.run(
            command,
            cwd=cwd,
            env=dict(env) if env is not None else None,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
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
    path = root / relative
    try:
        info = path.lstat()
        data = path.read_bytes()
    except (OSError, ValueError) as exc:
        raise Refusal(f"cannot read checked-out {relative}: {exc}") from exc
    if not stat.S_ISREG(info.st_mode):
        raise Refusal(f"checked-out {relative} is not a regular file")
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


def make_run_directory() -> RunDirectory:
    parent = pathlib.Path(tempfile.gettempdir()).resolve()
    path = pathlib.Path(tempfile.mkdtemp(prefix="milan-act-ci-", dir=parent))
    info = path.stat()
    return RunDirectory(path, parent, info.st_dev, info.st_ino)


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
        result = run_command(
            [
                sudo,
                "-n",
                "--",
                require_tool("chown"),
                "-R",
                f"{os.getuid()}:{os.getgid()}",
                str(path),
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
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
    run = make_run_directory()
    try:
        yield run.path
    finally:
        cleanup_run_directory(run, use_sudo)


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


def load_workflow(path: pathlib.Path) -> dict[str, object]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise Refusal(f"cannot read workflow {path}: {exc}") from exc
    if len(raw) > MAX_WORKFLOW_BYTES:
        raise Refusal(f"workflow exceeds the {MAX_WORKFLOW_BYTES}-byte safety limit: {path}")
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
        document = load_workflow(root / relative)
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


def docker_prefix(use_sudo: bool) -> list[str]:
    command = [require_tool("docker")]
    if use_sudo:
        command = [require_tool("sudo"), "-n", "--", *command]
    return command


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
    command = [*docker_prefix(use_sudo), *arguments]
    try:
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


def new_docker_boundary() -> DockerBoundary:
    token = secrets.token_hex(16)
    if not re.fullmatch(r"[0-9a-f]{32}", token):
        raise Refusal("cannot generate a safe Docker ownership token")
    return DockerBoundary(token=token, name=f"milan-act-ci-{token}")


def inspect_docker_boundary(
    boundary: DockerBoundary,
    *,
    use_sudo: bool,
    cwd: pathlib.Path,
    env: Mapping[str, str],
) -> str:
    if boundary.network_id is None or not DOCKER_ID_RE.fullmatch(boundary.network_id):
        raise Refusal("Docker boundary has no valid network ID")
    result = run_docker(
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


def create_docker_boundary(
    planned: DockerBoundary,
    *,
    use_sudo: bool,
    cwd: pathlib.Path,
    env: Mapping[str, str],
) -> DockerBoundary:
    if planned.network_id is not None:
        raise Refusal("refusing to recreate an initialized Docker boundary")
    result = run_docker(
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
        run_docker(
            ["network", "rm", planned.name],
            use_sudo=use_sudo,
            cwd=cwd,
            env=env,
            description="malformed Docker boundary removal",
            check=False,
        )
        raise Refusal("Docker returned an invalid boundary network ID")
    boundary = replace(planned, network_id=network_id)
    try:
        gateway = inspect_docker_boundary(
            boundary, use_sudo=use_sudo, cwd=cwd, env=env
        )
    except BaseException:
        run_docker(
            ["network", "rm", network_id],
            use_sudo=use_sudo,
            cwd=cwd,
            env=env,
            description="invalid Docker boundary removal",
            check=False,
        )
        raise
    return replace(boundary, gateway=gateway)


def docker_container_inventory(
    *, use_sudo: bool, cwd: pathlib.Path, env: Mapping[str, str]
) -> list[dict[str, object]]:
    listed = run_docker(
        ["container", "ls", "--all", "--quiet", "--no-trunc"],
        use_sudo=use_sudo,
        cwd=cwd,
        env=env,
        description="Docker container inventory",
    )
    ids = [line for line in listed.stdout.splitlines() if line]
    if len(ids) != len(set(ids)) or any(
        not DOCKER_ID_RE.fullmatch(item) for item in ids
    ):
        raise Refusal("Docker returned an invalid container inventory")
    inventory: list[dict[str, object]] = []
    for requested_id in ids:
        inspected = run_docker(
            ["container", "inspect", requested_id],
            use_sudo=use_sudo,
            cwd=cwd,
            env=env,
            description="Docker container metadata inspection",
            check=False,
        )
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


def cleanup_owned_containers(
    boundary: DockerBoundary,
    *,
    use_sudo: bool,
    cwd: pathlib.Path,
    env: Mapping[str, str],
) -> int:
    inventory = docker_container_inventory(use_sudo=use_sudo, cwd=cwd, env=env)
    owned = owned_container_ids(inventory, boundary)
    initial_count = len(owned)
    attempt_errors: list[str] = []
    running = running_container_ids(inventory, owned)
    if running:
        try:
            result = run_docker(
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
        inventory = docker_container_inventory(use_sudo=use_sudo, cwd=cwd, env=env)
        remaining = sorted(owned_container_ids(inventory, boundary))
    except Refusal as exc:
        attempt_errors.append(str(exc))
        remaining = sorted(owned)
    if remaining:
        try:
            result = run_docker(
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
            use_sudo=use_sudo, cwd=cwd, env=env
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
) -> None:
    errors: list[str] = []
    try:
        cleanup_owned_containers(
            boundary, use_sudo=use_sudo, cwd=cwd, env=env
        )
    except Refusal as exc:
        errors.append(str(exc))
    try:
        inspect_docker_boundary(
            boundary, use_sudo=use_sudo, cwd=cwd, env=env
        )
    except Refusal as exc:
        errors.append(str(exc))
    else:
        network_id = boundary.network_id
        if network_id is None:
            errors.append("Docker boundary has no network ID during cleanup")
            network_id = boundary.name
        try:
            result = run_docker(
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

    if boundary.network_id is not None:
        try:
            result = run_docker(
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
            use_sudo=use_sudo, cwd=cwd, env=env
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
    boundary = create_docker_boundary(
        planned, use_sudo=use_sudo, cwd=cwd, env=env
    )
    try:
        yield boundary
    finally:
        cleanup_docker_boundary(
            boundary, use_sudo=use_sudo, cwd=cwd, env=env
        )


def act_prefix(act_binary: str, use_sudo: bool, env: Mapping[str, str]) -> list[str]:
    if not use_sudo:
        return [act_binary]
    assignments = [f"{key}={value}" for key, value in sorted(env.items())]
    return [
        require_tool("sudo"),
        "-n",
        "--",
        require_tool("env"),
        "-i",
        *assignments,
        act_binary,
    ]


def build_act_command(
    prefix: Sequence[str],
    workflow: str,
    layout: RunLayout,
    artifact_port: int,
    boundary: DockerBoundary,
) -> list[str]:
    if not 1 <= artifact_port <= 65535:
        raise Refusal(f"invalid artifact-server port: {artifact_port}")
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


def run_act_process(
    command: Sequence[str],
    *,
    cwd: pathlib.Path,
    env: Mapping[str, str],
    check: bool = False,
    started: Callable[[int], None] | None = None,
) -> subprocess.CompletedProcess[object]:
    """Run act in its own process group and reap that group on interruption."""
    del check  # This boundary always returns the workflow status to its caller.
    process = subprocess.Popen(
        command,
        cwd=cwd,
        env=dict(env),
        start_new_session=True,
    )
    try:
        if started is not None:
            started(process.pid)
        return subprocess.CompletedProcess(command, process.wait())
    except BaseException:
        for sent_signal, timeout in (
            (signal.SIGINT, 10),
            (signal.SIGTERM, 10),
            (signal.SIGKILL, 5),
        ):
            if process.poll() is not None:
                break
            try:
                signal_process_group(process.pid, sent_signal)
            except ProcessLookupError:
                break
            try:
                process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                continue
        if process.poll() is None:
            raise Refusal("cannot terminate interrupted act process group")
        raise


def signal_process_group(process_group: int, sent_signal: int) -> None:
    try:
        os.killpg(process_group, sent_signal)
        return
    except PermissionError:
        pass
    signal_name = signal.Signals(sent_signal).name.removeprefix("SIG")
    result = subprocess.run(
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
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.strip().splitlines()
        suffix = f": {detail[-1]}" if detail else ""
        raise Refusal(f"cannot signal act process group{suffix}")


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
    if version < MIN_ACT_VERSION:
        want = ".".join(str(part) for part in MIN_ACT_VERSION)
        got = ".".join(str(part) for part in version)
        raise Refusal(f"act {got} is older than the tested minimum {want}")

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
    query: Callable[[int, str], PullRequest] = query_pull_request,
    run_process: Callable[..., subprocess.CompletedProcess[object]] = run_act_process,
) -> int:
    """Bind one act process between fresh remote-state and byte checks."""
    require_live_pull_request(pr, repository, query)
    integrity_check()
    try:
        result = run_process(command, cwd=cwd, env=dict(env), check=False)
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
            "Config": {"Labels": {}},
            "HostConfig": {"NetworkMode": selftest_boundary.name},
            "NetworkSettings": {"Networks": {}},
            "State": {"Running": False},
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
        "act version parser accepts the tested version",
        parse_act_version("act version 0.2.89") == MIN_ACT_VERSION,
    )
    refused(
        "unparseable act version is refused",
        lambda: parse_act_version("act unknown"),
    )

    def successful_process(*_args, **_kwargs):  # type: ignore[no-untyped-def]
        return subprocess.CompletedProcess([], 0)

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

    try:
        validate_workflow_sandbox(shipping_root, tuple(WORKFLOWS))
    except Refusal as exc:
        check(f"shipping workflows satisfy the sandbox policy ({exc})", False)
    else:
        check("shipping workflows satisfy the sandbox policy", True)

    print("selftest:", "PASS" if failures == 0 else f"{failures} FAILURE(S)")
    return RC_OK if failures == 0 else RC_FAILED


def interrupt_selftest(act_binary: str, use_sudo: bool) -> int:
    """Freeze act with a live job and prove daemon-owned cleanup completes."""
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
    with temporary_run_directory(use_sudo) as run_root:
        layout = make_layout(run_root, probe_pr)
        layout.checkout.mkdir(parents=True)
        workflow_path = layout.checkout / relative_workflow
        workflow_path.parent.mkdir(parents=True)
        workflow_path.write_text(
            "name: interrupt-selftest\n"
            "on: pull_request\n"
            "jobs:\n"
            "  sleep:\n"
            "    runs-on: ubuntu-latest\n"
            "    steps:\n"
            "      - run: sleep 300\n",
            encoding="utf-8",
        )
        git = git_prefix()
        git_env = git_environment(layout.home)
        capture(
            [*git, "init", "--quiet", str(layout.checkout)],
            cwd=layout.root,
            env=git_env,
            description="interrupt self-test repository creation",
        )
        capture(
            [*git, "-C", str(layout.checkout), "add", relative_workflow],
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
        planned = new_docker_boundary()
        monitor_cancel = threading.Event()
        frozen = threading.Event()
        monitor_problems: list[str] = []
        monitor_threads: list[threading.Thread] = []

        try:
            WORKFLOWS[workflow] = relative_workflow
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
                    def freeze_live_act() -> None:
                        deadline = time.monotonic() + 120
                        while not monitor_cancel.is_set():
                            try:
                                inventory = docker_container_inventory(
                                    use_sudo=use_sudo,
                                    cwd=layout.invocation,
                                    env=env,
                                )
                                selected = owned_container_ids(inventory, boundary)
                                if running_container_ids(inventory, selected):
                                    try:
                                        signal_process_group(
                                            process_group, signal.SIGSTOP
                                        )
                                    except (OSError, Refusal) as exc:
                                        monitor_problems.append(
                                            f"cannot freeze live act process: {exc}"
                                        )
                                        os.kill(os.getpid(), signal.SIGINT)
                                        return
                                    frozen.set()
                                    os.kill(os.getpid(), signal.SIGINT)
                                    return
                            except Refusal:
                                # Container creation/removal can race one inventory;
                                # retry until the bounded deadline.
                                pass
                            if time.monotonic() >= deadline:
                                monitor_problems.append(
                                    "no owned running act container appeared "
                                    "within 120s"
                                )
                                os.kill(os.getpid(), signal.SIGINT)
                                return
                            monitor_cancel.wait(0.25)

                    monitor = threading.Thread(
                        target=freeze_live_act,
                        name="act-ci-interrupt-monitor",
                        daemon=True,
                    )
                    monitor_threads.append(monitor)
                    monitor.start()

                interrupted = False
                try:
                    result = run_act_process(
                        command,
                        cwd=layout.invocation,
                        env=env,
                        started=process_started,
                    )
                except KeyboardInterrupt:
                    interrupted = True
                finally:
                    monitor_cancel.set()
                    for monitor in monitor_threads:
                        monitor.join(timeout=5)
                if not interrupted:
                    raise Refusal(
                        f"interrupt self-test act process exited {result.returncode} "
                        "before fault injection"
                    )
                if monitor_problems:
                    raise Refusal(monitor_problems[0])
                if not frozen.is_set():
                    raise Refusal("interrupt self-test did not freeze act")
        finally:
            WORKFLOWS.pop(workflow, None)

        final_inventory = docker_container_inventory(
            use_sudo=use_sudo, cwd=layout.invocation, env=env
        )
        survivors = owned_container_ids(final_inventory, planned)
        if survivors:
            raise Refusal(
                f"interrupt self-test left {len(survivors)} owned container(s)"
            )
    print("interrupt-selftest: PASS (frozen act left no container or network)")
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
            return interrupt_selftest(act_binary, args.sudo)
        except Refusal as exc:
            print(f"act-ci: REFUSED: {exc}", file=sys.stderr)
            return RC_REFUSED
    if args.pr is None or args.pr <= 0:
        parser.error("--pr requires a positive pull-request number")

    try:
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
    except Refusal as exc:
        print(f"act-ci: REFUSED: {exc}", file=sys.stderr)
        return RC_REFUSED


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
