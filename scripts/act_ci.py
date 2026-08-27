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
import json
import os
import pathlib
import re
import shlex
import shutil
import stat
import subprocess
import sys
import tempfile
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

WORKFLOWS: dict[str, str] = {
    "docs": ".github/workflows/docs.yml",
    "elaborate": ".github/workflows/elaborate.yml",
    "rtl-fast": ".github/workflows/rtl-fast.yml",
    "rtl-full": ".github/workflows/rtl.yml",
}
REQUIRED_SUBMODULES = (
    "third_party/verilog-axis",
    "protocol-processor",
    "gptp-processor",
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
        if getattr(expected, item.name) != getattr(current, item.name)
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
        "protocol.file.allow=never",
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
    # act's local checkout copier omits empty directories. Populate the three
    # public, pinned dependencies every selected workflow already names so the
    # copied tree has hosted-checkout parity before the workflow repeats this
    # idempotent update. Git runs with no credential, hook, or file transport.
    capture(
        [
            *prefix,
            "-C",
            str(checkout),
            "submodule",
            "update",
            "--init",
            *REQUIRED_SUBMODULES,
        ],
        cwd=layout.root,
        env=env,
        description="public pinned submodule materialization",
    )
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
        "milan_act_ci": {
            "trusted_runner": True,
            "default_branch": DEFAULT_BASE,
            "head_sha": pr.head_sha,
        },
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
    prefix: Sequence[str], workflow: str, layout: RunLayout
) -> list[str]:
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
        "--artifact-server-port",
        "0",
        "--action-cache-path",
        str(layout.action_cache),
        "--cache-server-path",
        str(layout.cache_server),
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
        "--network",
        "bridge",
    ]


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

    docker = require_tool("docker")
    docker_command = [docker, "info", "--format", "{{.ServerVersion}}"]
    if use_sudo:
        docker_command = [require_tool("sudo"), "-n", "--", *docker_command]
    capture(
        docker_command,
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
    run_process: Callable[..., subprocess.CompletedProcess[object]] = subprocess.run,
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

        for workflow in workflows:
            command = build_act_command(prefix, workflow, layout)
            if dry_run:
                print(f"act-ci: {workflow}: {shlex.join(command)}")
                continue
            print(f"act-ci: running {workflow} ({WORKFLOWS[workflow]})", flush=True)
            result = execute_act_boundary(
                command,
                pr=pr,
                repository=repository,
                cwd=layout.invocation,
                env=env,
                integrity_check=integrity_check,
            )
            if result != 0:
                print(f"act-ci: {workflow}: FAILED ({result})", file=sys.stderr)
                return RC_FAILED
            print(f"act-ci: {workflow}: PASS at {pr.head_sha}")
        require_live_pull_request(pr, repository)
        integrity_check()
    return RC_OK


def expect_refusal(label: str, action: Callable[[], object]) -> bool:
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
        "event carries the trusted credential-free default-branch marker",
        event["milan_act_ci"]
        == {
            "trusted_runner": True,
            "default_branch": DEFAULT_BASE,
            "head_sha": head,
        },
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
            command = build_act_command(["act"], "rtl-full", first)
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
                and command[command.index("--network") + 1] == "bridge"
                and "--privileged" not in command,
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

    check(
        "act version parser accepts the tested version",
        parse_act_version("act version 0.2.89") == MIN_ACT_VERSION,
    )
    refused(
        "unparseable act version is refused",
        lambda: parse_act_version("act unknown"),
    )

    changed = replace(pr, head_sha="4" * 40)
    answers = iter((pr, changed))

    def moving_query(_number: int, _repository: str) -> PullRequest:
        return next(answers)

    def successful_process(*_args, **_kwargs):  # type: ignore[no-untyped-def]
        return subprocess.CompletedProcess([], 0)

    refused(
        "remote metadata movement across an act process is refused",
        lambda: execute_act_boundary(
            ["act"],
            pr=pr,
            repository=repository,
            cwd=ROOT,
            env={},
            integrity_check=lambda: None,
            query=moving_query,
            run_process=successful_process,
        ),
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
        validate_workflow_sandbox(ROOT, tuple(WORKFLOWS))
    except Refusal as exc:
        check(f"shipping workflows satisfy the sandbox policy ({exc})", False)
    else:
        check("shipping workflows satisfy the sandbox policy", True)

    print("selftest:", "PASS" if failures == 0 else f"{failures} FAILURE(S)")
    return RC_OK if failures == 0 else RC_FAILED


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
    args = parser.parse_args(argv[1:])

    if args.selftest:
        if (
            args.pr is not None
            or args.workflow
            or args.dry_run
            or args.trusted_install_sha256
        ):
            parser.error("--selftest cannot be combined with PR-run arguments")
        return selftest()
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
