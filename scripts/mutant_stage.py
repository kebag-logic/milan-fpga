#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Stable staging directories for the mutation drivers, so a warm compiler cache answers
their model compiles (Issue #998; REQ-VER-01 and REQ-VER-04).

A driver plants each mutant in a copy of the RTL and builds a model from it. Verilator
writes the path it was given for every source into the model's C++ (the file name of each
VL_FATAL_MT and $stop site), so a model staged under tempfile's random directory differs
from the same model staged in any other run, and ccache misses every one of them in every
run: crf_rx missed 36 of its 115 compiles on a warm cache, all of them mutant models and
staged harness copies. `directory()` and `mkdtemp()` stand in for tempfile's two calls and
return the same path in every run, `<TMPDIR>/milan-mutant-stage-<uid>/<prefix><slot>`
with TMPDIR resolved, from any checkout, so the model's C++ is the same and the warm cache
answers it. The mutant, its build and its verdict are untouched: only the directory's
name changes.

The stage root is used only once it is proved: a real directory, not a symbolic link,
owned by this user, open to no other user's writes and private once taken, directly
inside the resolved temporary directory, which is itself owned by this user or root and
sticky if others may write it. It is created atomically by one mkdir with mode 0700. A
root that fails any of these is refused with its reason on stderr, and the driver stages
at a random private directory, as tempfile did: correct, and merely cold.

Each slot is its own directory, and its lock is that directory: a holder keeps an
exclusive flock on the slot's inode for as long as it uses it. Every caller that names one
physical directory, through any TMPDIR, any spelling of the parent or any user, therefore
meets the same lock, so a held slot is never emptied or handed out twice. A slot is
emptied when it is taken, so a run never sees another run's files, and a slot owned by
another user is never touched. A second concurrent run of the same driver takes the next
slot; when every slot is held it falls back to a random directory. While a slot is held
the driver's builds see CCACHE_BASEDIR at the stage root, so a planted harness compiled in
one slot hits the same harness compiled in another, and CCACHE_NOHASHDIR keeps the build
directory out of the key (FPGA-gPTP #104); a CCACHE_* setting of the caller's own wins.
With no compiler cache (OBJCACHE empty) none of this changes a compile.

    python3 scripts/mutant_stage.py --selftest
"""

from __future__ import annotations

import argparse
from collections.abc import Callable, Iterator
from contextlib import contextmanager
import fcntl
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile

#: Concurrent runs of one driver that each get a stable directory; a further one is cold.
SLOTS = 8
#: Locks a mkdtemp() caller holds until it exits: it removes the directory itself.
_HELD: list[int] = []
#: Attempts at one slot while its previous holder removes it as this caller opens it.
_RETRIES = 4


def _uid() -> int:
    """The owner every stage directory must have (the self-test's foreign-owner control replaces it)."""
    return os.getuid()


def _base() -> Path:
    """The resolved temporary directory, so every spelling of TMPDIR names one stage root."""
    return Path(tempfile.gettempdir()).resolve()


def stage_root() -> Path:
    """The per-user root every stable directory lives under."""
    return _base() / f"milan-mutant-stage-{_uid()}"


def _same(fd: int, path: Path) -> bool:
    """True when `path`, not followed, is still the directory open as `fd`."""
    try:
        here = os.lstat(path)
    except FileNotFoundError:
        return False
    held = os.fstat(fd)
    return (here.st_dev, here.st_ino) == (held.st_dev, held.st_ino)


def proved_root() -> tuple[Path | None, str]:
    """The stage root once proved, else None and the reason it is refused."""
    base = _base()
    try:
        info = os.lstat(base)
    except OSError as exc:
        return None, f"{base}: {exc.strerror}"
    if not stat.S_ISDIR(info.st_mode):
        return None, f"{base} is not a directory"
    if info.st_uid not in (_uid(), 0):
        return None, f"{base} is owned by uid {info.st_uid}"
    if info.st_mode & 0o022 and not info.st_mode & stat.S_ISVTX:
        return None, f"{base} may be written by others and is not sticky"
    root = base / f"milan-mutant-stage-{_uid()}"
    try:
        os.mkdir(root, 0o700)
    except FileExistsError:
        pass
    except OSError as exc:
        return None, f"{root}: {exc.strerror}"
    info = os.lstat(root)
    if stat.S_ISLNK(info.st_mode):
        return None, f"{root} is a symbolic link"
    if not stat.S_ISDIR(info.st_mode):
        return None, f"{root} is not a directory"
    if info.st_uid != _uid():
        return None, f"{root} is owned by uid {info.st_uid}"
    if info.st_mode & 0o022:
        return None, f"{root} may be written by others (mode {stat.S_IMODE(info.st_mode):04o})"
    fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        if not _same(fd, root) or root.resolve() != root:
            return None, f"{root} changed while it was checked"
        if stat.S_IMODE(info.st_mode) != 0o700:
            os.fchmod(fd, 0o700)  # an earlier, readable root: no other user could write it
    finally:
        os.close(fd)
    return root, ""


def _empty(path: Path) -> None:
    """Remove everything inside the held slot `path`, following no link."""
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_dir(follow_symlinks=False):
                shutil.rmtree(entry.path)
            else:
                os.unlink(entry.path)


def _hold(path: Path) -> int | None:
    """Lock and empty the slot directory `path`: its locked descriptor, or None when another
    holder has it or another user owns it."""
    for _ in range(_RETRIES):
        try:
            os.mkdir(path, 0o700)
        except FileExistsError:
            pass
        try:
            info = os.lstat(path)
        except FileNotFoundError:
            continue  # its holder removed it between our mkdir and lstat
        if info.st_uid != _uid():
            return None  # another user's slot, or its leftover: never touched
        if not stat.S_ISDIR(info.st_mode):
            os.unlink(path)  # this user's file or link in the slot's name, left by a killed run
            continue
        try:
            fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        except FileNotFoundError:
            continue
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            os.close(fd)
            return None
        if not _same(fd, path):
            os.close(fd)  # its holder removed it after we opened it: take the new one
            continue
        if stat.S_IMODE(info.st_mode) != 0o700:
            os.fchmod(fd, 0o700)
        _empty(path)
        return fd
    return None


def _take(prefix: str, parent: str | os.PathLike | None) -> tuple[Path, int | None, Path | None]:
    """The first free slot's emptied directory, its held lock and the cache base, or a random
    private directory, no lock and no cache base."""
    if "/" in prefix or prefix in ("", ".", ".."):
        raise ValueError(f"a staging prefix names one directory: {prefix!r}")
    if parent is not None:
        base: Path | None = Path(parent).resolve()
    else:
        base, reason = proved_root()
        if base is None:
            print(f"mutant_stage: {reason}; staging at a random private directory instead "
                  "(correct, but the compiler cache cannot answer it)", file=sys.stderr, flush=True)
    if base is not None:
        for slot in range(SLOTS):
            path = base / f"{prefix}{slot}"
            fd = _hold(path)
            if fd is not None:
                return path, fd, base
    return Path(tempfile.mkdtemp(prefix=prefix, dir=parent)), None, None


def _cache_env(root: Path | None) -> dict[str, str | None]:
    """Point ccache at the stage root, keeping a caller's own settings; the previous values."""
    previous = {name: os.environ.get(name) for name in ("CCACHE_BASEDIR", "CCACHE_NOHASHDIR")}
    if root is not None:
        os.environ.setdefault("CCACHE_BASEDIR", str(root))
        os.environ.setdefault("CCACHE_NOHASHDIR", "1")
    return previous


@contextmanager
def directory(prefix: str, parent: str | os.PathLike | None = None) -> Iterator[str]:
    """tempfile.TemporaryDirectory's stand-in: a stable, empty, exclusively held directory,
    removed with its lock released at exit. `parent` places it under that directory instead."""
    path, fd, root = _take(prefix, parent)
    previous = _cache_env(root)
    try:
        yield str(path)
    finally:
        for name, value in previous.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value
        shutil.rmtree(path, ignore_errors=True)  # while still held, so no later holder's files
        if fd is not None:
            os.close(fd)


def mkdtemp(prefix: str, parent: str | os.PathLike | None = None) -> str:
    """tempfile.mkdtemp's stand-in: a stable, empty directory whose slot stays held until
    this process exits. The caller removes the directory, as it removed mkdtemp's."""
    path, fd, root = _take(prefix, parent)
    _cache_env(root)
    if fd is not None:
        _HELD.append(fd)
    return str(path)


# Each concurrent holder in the controls below is its own process: it takes a slot, writes
# its token there, waits until every holder holds one, then reports whether its slot still
# holds exactly its own token. `uid` set makes this module see every directory as foreign.
_HOLDER = r"""
import json, os, sys, time
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import mutant_stage
token, prefix, parent, sync, count, uid = sys.argv[2:8]
if uid:
    mutant_stage._uid = lambda: int(uid)
with mutant_stage.directory(prefix, parent or None) as held:
    Path(held, "owner").write_text(token)
    Path(sync, token).touch()
    deadline = time.monotonic() + 60
    while len(os.listdir(sync)) < int(count) and time.monotonic() < deadline:
        time.sleep(0.01)
    print(json.dumps({"path": held, "token": token, "all_held": len(os.listdir(sync)) >= int(count),
                      "kept": sorted(os.listdir(held)) == ["owner"] and Path(held, "owner").read_text() == token}))
"""


def _holders(specs: list[dict], sync: Path) -> list[dict]:
    """Run one independent holder process per spec at once; their reports."""
    sync.mkdir()
    procs = []
    for number, spec in enumerate(specs):
        env = {**os.environ, "TMPDIR": spec.get("tmpdir", os.environ["TMPDIR"])}
        procs.append(subprocess.Popen(
            [sys.executable, "-c", _HOLDER, str(Path(__file__).resolve().parent), f"holder-{number}",
             spec["prefix"], str(spec.get("parent", "")), str(sync), str(len(specs)), str(spec.get("uid", ""))],
            env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True))
    reports = []
    for proc in procs:
        out, err = proc.communicate(timeout=120)
        assert proc.returncode == 0, err
        reports.append({**json.loads(out), "stderr": err})
    shutil.rmtree(sync)
    return reports


def _exclusive(reports: list[dict]) -> None:
    """Every holder held at once, in its own physical directory, and nobody emptied another's."""
    real = [Path(report["path"]).resolve() for report in reports]
    assert all(report["all_held"] for report in reports), reports
    assert len(set(real)) == len(real), real
    assert all(report["kept"] for report in reports), reports


def _slot_controls(scratch: Path, tree: Path) -> None:
    """One process: stable, exclusive, emptied when taken, fallback, a caller's cache wins."""
    with directory("ctl-") as first:
        Path(first, "planted.sv").write_text("module m; endmodule\n")
        assert os.environ["CCACHE_BASEDIR"] == str(stage_root())
        assert os.environ["CCACHE_NOHASHDIR"] == "1"
        assert stat.S_IMODE(os.lstat(stage_root()).st_mode) == 0o700
        with directory("ctl-") as second:
            assert second != first and second.endswith("ctl-1"), (first, second)
    assert "CCACHE_BASEDIR" not in os.environ and not Path(first).exists()
    print("mutant stage control: a held slot is never handed out twice, and the root is created 0700")
    with directory("ctl-") as again:
        assert again == first and list(Path(again).iterdir()) == [], again
    print("mutant stage control: the same path in every run, and empty")
    stale = Path(first)
    stale.mkdir()
    (stale / "left-by-a-killed-run.o").write_text("stale\n")
    (stale / "sub").mkdir()
    outside = scratch / "outside"
    outside.mkdir()
    (outside / "keep").write_text("keep\n")
    (stale / "sub" / "link").symlink_to(outside)
    (stale / "link").symlink_to(outside)
    with directory("ctl-") as taken:
        assert taken == first and list(Path(taken).iterdir()) == [], taken
    assert (outside / "keep").exists()
    print("mutant stage control: a killed run's leftovers are cleared when the slot is taken, following no link")
    held = [_take("full-", None) for _ in range(SLOTS)]
    with directory("full-") as cold:
        assert Path(cold).name.startswith("full-") and Path(cold).name not in {
            f"full-{slot}" for slot in range(SLOTS)}, cold
    for _, fd, _ in held:
        os.close(fd)
    print("mutant stage control: with every slot held, a random directory, still correct")
    os.environ["CCACHE_BASEDIR"] = "/caller"
    with directory("ctl-"):
        assert os.environ["CCACHE_BASEDIR"] == "/caller"
    assert os.environ.pop("CCACHE_BASEDIR") == "/caller"
    print("mutant stage control: a caller's CCACHE_BASEDIR wins")
    kept = mkdtemp("in-tree-", parent=tree)
    assert kept == str(tree / "in-tree-0") and sorted(os.listdir(tree)) == ["in-tree-0"]
    shutil.rmtree(kept)
    print("mutant stage control: an in-tree directory leaves nothing else in the tree")
    for bad in ("a/b", "", ".."):
        try:
            _take(bad, None)
        except ValueError:
            continue
        raise AssertionError(f"accepted prefix {bad!r}")
    print("mutant stage control: a prefix naming more than one directory is refused")


def _domain_controls(scratch: Path, tmp: Path, tree: Path) -> None:
    """Independent processes, all holding at once: one lock domain per physical directory."""
    sync = scratch / "sync"
    _exclusive(_holders([{"prefix": "race-"} for _ in range(6)], sync))
    print("mutant stage control: six drivers racing for one slot each hold their own, none emptied")
    other_tmp = scratch / "other-tmp"
    other_tmp.mkdir(mode=0o700)
    _exclusive(_holders([{"prefix": "split-", "parent": tree, "tmpdir": str(tmp)},
                         {"prefix": "split-", "parent": tree, "tmpdir": str(other_tmp)}], sync))
    print("mutant stage control: two in-tree drivers under different TMPDIRs share one lock domain")
    alias_tmp = scratch / "alias-tmp"
    alias_tmp.symlink_to(tmp)
    alias_tree = scratch / "alias-tree"
    alias_tree.symlink_to(tree)
    reports = _holders([{"prefix": "alias-", "tmpdir": str(tmp)}, {"prefix": "alias-", "tmpdir": str(alias_tmp)},
                        {"prefix": "alias-", "parent": tree}, {"prefix": "alias-", "parent": alias_tree}], sync)
    _exclusive(reports[:2])
    _exclusive(reports[2:])
    assert all(not report["path"].startswith(str(alias_tmp)) for report in reports), reports
    print("mutant stage control: a resolved and an unresolved spelling of one directory share one lock")
    planted = tree / "theirs-0"
    planted.mkdir()
    (planted / "their-live-model.o").write_text("theirs\n")
    reports = _holders([{"prefix": "theirs-", "parent": tree, "uid": os.getuid() + 1}], sync)
    assert (planted / "their-live-model.o").exists() and reports[0]["path"] != str(planted), reports
    for leftover in tree.glob("theirs-*"):  # slots the foreign-seeing holder made and refused
        shutil.rmtree(leftover)
    print("mutant stage control: another user's slot is never emptied or taken")


def _link_root(case: Path, root: Path) -> Path:
    """A root that is a symbolic link to a directory its planter chose."""
    victim = case / "elsewhere"
    victim.mkdir()
    root.symlink_to(victim)
    return victim


def _writable_root(case: Path, root: Path) -> Path:
    """A root every user may write."""
    root.mkdir()
    os.chmod(root, 0o777)
    return root


def _regular_root(case: Path, root: Path) -> None:
    """A file where the root should be."""
    root.write_text("not a directory\n")


def _owned_root(case: Path, root: Path) -> Path:
    """A root this user made, seen by a holder that is another uid."""
    root.mkdir(mode=0o700, exist_ok=True)
    return root


def _refused(scratch: Path, plant: Callable[[Path, Path], Path | None], expect: str,
             uid: int | None = None, case: Path | None = None) -> None:
    """`plant` makes a bad root in a TMPDIR (a fresh private one unless `case`): the driver must
    name the reason, stage elsewhere and leave the planted directory as it was."""
    if case is None:
        case = scratch / f"case{plant.__name__}"
        case.mkdir(mode=0o700)
    root = case / f"milan-mutant-stage-{os.getuid() if uid is None else uid}"
    target = plant(case, root)
    try:
        before = sorted(os.listdir(target)) if target else None
        report, = _holders([{"prefix": "root-", "tmpdir": str(case), **({"uid": uid} if uid else {})}],
                           scratch / "sync")
        assert expect in report["stderr"] and "random private directory" in report["stderr"], report
        assert not Path(report["path"]).resolve().is_relative_to(root.resolve()), report
        if target:
            assert sorted(os.listdir(target)) == before, (target, os.listdir(target))
    finally:
        if uid is not None:
            shutil.rmtree(root, ignore_errors=True)
    print(f"mutant stage control: a root that {expect} is refused, and the driver stages elsewhere")


def _root_controls(scratch: Path) -> None:
    """The stage root is used only once proved."""
    _refused(scratch, _link_root, "is a symbolic link")
    _refused(scratch, _writable_root, "may be written by others")
    _refused(scratch, _regular_root, "is not a directory")
    # Another user's root: the system's sticky, root-owned temporary directory holds a root
    # this user made, which a holder seeing itself as an unused uid must refuse.
    system_tmp = Path("/tmp")
    info = os.lstat(system_tmp)
    assert info.st_uid == 0 and info.st_mode & stat.S_ISVTX, "this control needs a sticky, root-owned /tmp"
    _refused(scratch, _owned_root, "is owned by uid", uid=2**31 - 3, case=system_tmp)
    shared = scratch / "shared"
    shared.mkdir()
    os.chmod(shared, 0o777)
    report, = _holders([{"prefix": "root-", "tmpdir": str(shared)}], scratch / "sync")
    assert "may be written by others and is not sticky" in report["stderr"], report
    assert not (shared / f"milan-mutant-stage-{os.getuid()}").exists()
    print("mutant stage control: a TMPDIR others may write without the sticky bit is refused")
    readable = scratch / "readable"
    readable.mkdir(mode=0o700)
    earlier = readable / f"milan-mutant-stage-{os.getuid()}"
    earlier.mkdir()
    os.chmod(earlier, 0o755)
    (earlier / "locks").write_text("an earlier layout\n")
    report, = _holders([{"prefix": "root-", "tmpdir": str(readable)}], scratch / "sync")
    assert report["stderr"] == "" and report["path"] == str(earlier / "root-0"), report
    assert stat.S_IMODE(os.lstat(earlier).st_mode) == 0o700
    print("mutant stage control: an earlier readable root is made private and used, its old entries ignored")


def selftest() -> int:
    """Stable across uses, exclusive while held across processes, TMPDIRs, aliases and users,
    emptied when taken, a root used only once proved, a caller's cache wins."""
    saved = {name: os.environ.pop(name, None) for name in ("TMPDIR", "CCACHE_BASEDIR", "CCACHE_NOHASHDIR")}
    with tempfile.TemporaryDirectory(prefix="mutant-stage-selftest-") as scratch_name:
        scratch = Path(scratch_name).resolve()
        tmp = scratch / "tmp"
        tmp.mkdir(mode=0o700)
        tree = scratch / "tree"
        tree.mkdir()
        os.environ["TMPDIR"] = str(tmp)
        tempfile.tempdir = None
        try:
            _slot_controls(scratch, tree)
            _domain_controls(scratch, tmp, tree)
            _root_controls(scratch)
        finally:
            for fd in _HELD:
                os.close(fd)
            _HELD.clear()
            for name, value in saved.items():
                os.environ.pop(name, None)
                if value is not None:
                    os.environ[name] = value
            tempfile.tempdir = None
    print("mutant stage: all controls PASS")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--selftest", action="store_true", required=True)
    parser.parse_args()
    raise SystemExit(selftest())
