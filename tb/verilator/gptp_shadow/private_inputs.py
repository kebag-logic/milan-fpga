#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Verify and copy the shadow campaign's source population without Git writes."""

import hashlib
import os
import stat
from pathlib import Path

FIRST_PARTY = ("hdl", "tb/common", "tb/verilator/gptp_shadow")
# Match the Makefile: engine/generator sources and axis RTL only. Vendor
# documentation links are not build inputs and never enter the private tree.
DEPENDENCIES = {"gptp-processor": ("hdl",), "third_party/verilog-axis": ("rtl",)}


class InputRefused(Exception):
    """The campaign cannot attribute these input bytes to a clean tree."""


def _git(root, owner, *args):
    status, output = owner.run(
        ["git", "--no-replace-objects", "--literal-pathspecs", "-C", str(root), *args])
    if status:
        raise InputRefused(f"git {' '.join(args)}: {output.strip()}")
    return output


def _records(text, tree=False):
    records = {}
    for row in text.split("\0"):
        if not row:
            continue
        metadata, name = row.split("\t", 1)
        mode, second, third = metadata.split()
        if not tree and third != "0":
            raise InputRefused(f"unmerged input: {name}")
        if name in records:
            raise InputRefused(f"duplicate input: {name}")
        records[name] = (mode, third if tree else second)
    return records


def _directory(root, relative):
    current = root
    for part in Path(relative).parts:
        current = current / part
        if not stat.S_ISDIR(current.lstat().st_mode):
            raise InputRefused(f"input directory is missing or linked: {current}")


def _copy_tree(root, target, owner, revision, scopes):
    expected = _records(_git(root, owner, "ls-tree", "-rz", revision, "--", *scopes), tree=True)
    indexed = _records(_git(root, owner, "ls-files", "--stage", "-z", "--", *scopes))
    if not expected or expected != indexed:
        raise InputRefused(f"index differs from {revision}: {root}")
    unknown = _git(root, owner, "ls-files", "--others", "--exclude-standard", "-z", "--", *scopes)
    if unknown:
        raise InputRefused(f"untracked input: {unknown.replace(chr(0), ', ')}")
    for name, (mode, blob) in expected.items():
        owner.checkpoint()
        if mode not in ("100644", "100755"):
            raise InputRefused(f"input is not a regular tracked file: {name}")
        _directory(root, str(Path(name).parent))
        source = root / name
        info = source.lstat()
        if not stat.S_ISREG(info.st_mode):
            raise InputRefused(f"input is not a regular file: {source}")
        content = source.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()
        executable = bool(info.st_mode & stat.S_IXUSR)
        if actual != blob or executable != (mode == "100755"):
            raise InputRefused(f"modified input bytes/mode: {source}")
        destination = target / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        # New files only: neither hardlinks nor source symlinks enter scratch.
        destination.write_bytes(content)
        destination.chmod(stat.S_IMODE(info.st_mode) | stat.S_IWUSR)


def copy_inputs(repo: Path, target: Path, owner: object) -> None:
    """Snapshot verified input files, including both required pinned dependencies."""
    # Caller Git environment must not redirect identity checks to another tree.
    if any(name.startswith("GIT_") for name in os.environ
           if name not in ("GIT_NO_REPLACE_OBJECTS", "GIT_CONFIG_NOSYSTEM", "GIT_TERMINAL_PROMPT")):
        raise InputRefused("Git environment overrides are not accepted")
    _copy_tree(repo, target, owner, "HEAD", FIRST_PARTY)
    pins = _records(_git(repo, owner, "ls-tree", "-z", "HEAD", "--", *DEPENDENCIES), tree=True)
    indexed = _records(_git(repo, owner, "ls-files", "--stage", "-z", "--", *DEPENDENCIES))
    if pins != indexed or set(pins) != set(DEPENDENCIES):
        raise InputRefused("required dependency gitlinks differ from HEAD")
    for name, (mode, revision) in pins.items():
        _directory(repo, name)
        root = repo / name
        if mode != "160000" or _git(root, owner, "rev-parse", "HEAD").strip() != revision:
            raise InputRefused(f"required dependency is not at its pin: {name}")
        if Path(_git(root, owner, "rev-parse", "--show-toplevel").strip()) != root:
            raise InputRefused(f"required dependency has no checkout: {name}")
        _copy_tree(root, target / name, owner, revision, DEPENDENCIES[name])
