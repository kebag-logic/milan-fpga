#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Verify and copy the shadow campaign's build inputs without Git writes.

The population is what the suite's own build reads: the files its Makefile
reports through `make print-inputs`, plus the local headers those C++ files
include. A file the build never reads cannot refuse the campaign. Each
first-party input must be its HEAD blob and mode; each dependency input must
be the blob its pinned gitlink records.
"""

import hashlib
import os
import re
import stat
import tempfile
from collections.abc import Iterable
from pathlib import Path, PurePosixPath

#: The pinned dependencies a build input may come from. Each is verified at
#: its gitlink before any of its files are copied.
DEPENDENCIES = ("gptp-processor", "third_party/verilog-axis")
#: Git variables that point Git at another repository, work tree, index,
#: object store or replacement graph, or inject configuration. The caller's
#: Git would then describe something other than this checkout, so its bytes
#: could not be attributed. Every other Git variable is accepted, and none
#: reaches the identity commands below: they run without any GIT_* setting.
REDIRECTS = frozenset({
    "GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_INDEX_FILE",
    "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_REPLACE_REF_BASE",
    "GIT_CONFIG_PARAMETERS", "GIT_CONFIG_COUNT", "GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM",
})
#: A quoted C/C++ include, resolved relative to the including file. Angle
#: includes and generated headers (absent from the checkout) are not inputs.
INCLUDE = re.compile(r'^[ \t]*#[ \t]*include[ \t]*"([^"\n]+)"', re.M)
CXX_SUFFIXES = (".c", ".cc", ".cpp", ".cxx", ".h", ".hh", ".hpp")


class InputRefused(Exception):
    """The campaign cannot attribute these input bytes to a clean tree."""


def _read(owner, label, argv, cwd=None, env=None):
    """Run a read-only command; parse only its standard output."""
    with tempfile.TemporaryFile() as diagnostics:
        status, output = owner.run(argv, cwd=cwd, env=env, stderr=diagnostics)
        diagnostics.seek(0)
        diagnostic = diagnostics.read().decode("utf-8", errors="replace").strip()
    if status:
        raise InputRefused(f"{label}: exit {status}: {diagnostic}")
    return output


def _git(root, owner, *args):
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    return _read(owner, f"git {' '.join(args)}",
                 ["git", "--no-replace-objects", "--literal-pathspecs", "-C", str(root), *args], env=env)


def _records(text, tree=False):
    records = {}
    for row in text.split("\0"):
        if not row:
            continue
        metadata, tab, name = row.partition("\t")
        fields = metadata.split(" ")
        if not tab or not name or len(fields) != 3 or not all(fields):
            raise InputRefused(f"unreadable Git identity record: {row[:120]!r}")
        mode, second, third = fields
        if not tree and third != "0":
            raise InputRefused(f"unmerged input: {name}")
        if name in records:
            raise InputRefused(f"duplicate input: {name}")
        records[name] = (mode, third if tree else second)
    return records


def _normal(base, relative):
    """Lexical repository-relative name, or None when it leaves the checkout."""
    parts = list(base.parts)
    for part in PurePosixPath(relative).parts:
        if part == "..":
            if not parts:
                return None
            parts.pop()
        elif part != ".":
            parts.append(part)
    return "/".join(parts) or None


def _declared(repo, suite, owner):
    """Ask the suite Makefile for its build inputs, then close over local includes."""
    base = PurePosixPath(suite.relative_to(repo).as_posix())
    names = set()
    argv = ["make", "-s", "--no-print-directory", "print-inputs"]
    for word in _read(owner, "make print-inputs", argv, cwd=suite).split():
        name = None if PurePosixPath(word).is_absolute() else _normal(base, word)
        if name is None:
            raise InputRefused(f"build input is outside the checkout: {word}")
        names.add(name)
    if not names:
        raise InputRefused(f"{suite}: the build declares no inputs")
    pending = sorted(names)
    while pending:
        name = pending.pop()
        if not name.endswith(CXX_SUFFIXES) or not (repo / name).is_file():
            continue
        for included in INCLUDE.findall((repo / name).read_text(encoding="utf-8", errors="replace")):
            header = _normal(PurePosixPath(name).parent, included)
            if header is not None and header not in names and (repo / header).is_file():
                names.add(header)
                pending.append(header)
    return names


def _directory(root, relative):
    current = root
    for part in Path(relative).parts:
        current = current / part
        try:
            linked = not stat.S_ISDIR(current.lstat().st_mode)
        except FileNotFoundError:
            linked = True
        if linked:
            raise InputRefused(f"input directory is missing or linked: {current}")


def _copy_files(root, target, owner, revision, names):
    # Directories first: Git pathspecs must never be resolved through a link.
    for name in sorted(names):
        _directory(root, str(Path(name).parent))
    expected = _records(_git(root, owner, "ls-tree", "-rz", revision, "--", *sorted(names)), tree=True)
    indexed = _records(_git(root, owner, "ls-files", "--stage", "-z", "--", *sorted(names)))
    if set(expected) != set(names):
        missing = sorted(set(names) ^ set(expected))
        raise InputRefused(f"build input is not a tracked file at {revision}: {', '.join(missing)}")
    if expected != indexed:
        raise InputRefused(f"index differs from {revision}: {root}")
    for name, (mode, blob) in expected.items():
        owner.checkpoint()
        if mode not in ("100644", "100755"):
            raise InputRefused(f"input is not a regular tracked file: {name}")
        source = root / name
        try:
            info = source.lstat()
        except FileNotFoundError as exc:
            raise InputRefused(f"input is missing: {source}") from exc
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


def copy_inputs(repo: Path, suite: Path, target: Path, owner: object, required: Iterable[Path]) -> None:
    """Snapshot the verified build inputs, including both required pinned dependencies.

    `required` names the mutation targets and anchors, which must be inputs.
    """
    redirects = sorted(name for name in os.environ if name in REDIRECTS)
    if redirects:
        raise InputRefused(f"Git environment redirects the checkout: {', '.join(redirects)}")
    declared = _declared(repo, suite, owner)
    absent = sorted(str(path.relative_to(repo)) for path in required
                    if str(path.relative_to(repo)) not in declared)
    if absent:
        raise InputRefused(f"mutation target or anchor is not a build input: {', '.join(absent)}")
    groups = {name: set() for name in DEPENDENCIES}
    first_party = set()
    for name in declared:
        root = next((dependency for dependency in DEPENDENCIES if name.startswith(dependency + "/")), None)
        if root is None:
            first_party.add(name)
        else:
            groups[root].add(name[len(root) + 1:])
    _copy_files(repo, target, owner, "HEAD", first_party)
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
        if groups[name]:
            _copy_files(root, target / name, owner, revision, groups[name])
