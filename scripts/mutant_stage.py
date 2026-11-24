#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Stable staging directories for the mutation drivers, so a warm compiler cache answers
their model compiles.

A driver plants each mutant in a copy of the RTL and builds a model from it. Verilator
writes the path it was given for every source into the model's C++ (the file name of each
VL_FATAL_MT and $stop site), so a model staged under tempfile's random directory differs
from the same model staged in any other run, and ccache misses every one of them in every
run: crf_rx missed 36 of its 115 compiles on a warm cache, all of them mutant models and
staged harness copies. `directory()` and `mkdtemp()` stand in for tempfile's two calls and
return the same path in every run, `<TMPDIR>/milan-mutant-stage-<uid>/<prefix><slot>`,
from any checkout, so the model's C++ is the same and the warm cache answers it. The
mutant, its build and its verdict are untouched: only the directory's name changes.

Each slot is held under an exclusive lock for as long as its caller uses it, and is
emptied when it is taken, so a run never sees another run's files. A second concurrent
run of the same driver takes the next slot; when every slot is held it falls back to a
random directory, which is correct and merely cold. While a slot is held the driver's
builds see CCACHE_BASEDIR at the stage root, so a planted harness compiled in one slot
hits the same harness compiled in another, and CCACHE_NOHASHDIR keeps the build
directory out of the key (FPGA-gPTP #104); a CCACHE_* setting of the caller's own wins.
With no compiler cache (OBJCACHE empty) none of this changes a compile.

    python3 scripts/mutant_stage.py --selftest
"""

from __future__ import annotations

import argparse
from collections.abc import Iterator
from contextlib import contextmanager
import fcntl
import hashlib
import os
from pathlib import Path
import shutil
import tempfile

#: Concurrent runs of one driver that each get a stable directory; a further one is cold.
SLOTS = 8
#: Locks a mkdtemp() caller holds until it exits: it removes the directory itself.
_HELD: list[int] = []


def stage_root() -> Path:
    """The per-user root every stable directory and every slot lock lives under."""
    return Path(tempfile.gettempdir()) / f"milan-mutant-stage-{os.getuid()}"


def _take(prefix: str, parent: str | os.PathLike | None) -> tuple[Path, int | None]:
    """The first free slot's emptied directory and its held lock, or a random directory."""
    locks = stage_root() / "locks"
    locks.mkdir(parents=True, exist_ok=True, mode=0o700)
    base = Path(parent).resolve() if parent is not None else stage_root()
    if "/" in prefix or prefix in ("", ".", ".."):
        raise ValueError(f"a staging prefix names one directory: {prefix!r}")
    for slot in range(SLOTS):
        path = base / f"{prefix}{slot}"
        lock = locks / (hashlib.sha256(str(path).encode()).hexdigest()[:24] + ".lock")
        fd = os.open(lock, os.O_RDWR | os.O_CREAT, 0o600)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            os.close(fd)
            continue
        if path.is_symlink() or path.is_file():
            path.unlink()
        elif path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True, mode=0o700)
        return path, fd
    return Path(tempfile.mkdtemp(prefix=prefix, dir=parent)), None


def _cache_env(root: Path) -> dict[str, str | None]:
    """Point ccache at the stage root, keeping a caller's own settings; the previous values."""
    previous = {name: os.environ.get(name) for name in ("CCACHE_BASEDIR", "CCACHE_NOHASHDIR")}
    os.environ.setdefault("CCACHE_BASEDIR", str(root))
    os.environ.setdefault("CCACHE_NOHASHDIR", "1")
    return previous


@contextmanager
def directory(prefix: str, parent: str | os.PathLike | None = None) -> Iterator[str]:
    """tempfile.TemporaryDirectory's stand-in: a stable, empty, exclusively held directory,
    removed with its lock released at exit. `parent` places it under that directory instead."""
    path, fd = _take(prefix, parent)
    previous = _cache_env(stage_root() if parent is None else Path(parent).resolve())
    try:
        yield str(path)
    finally:
        for name, value in previous.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value
        shutil.rmtree(path, ignore_errors=True)
        if fd is not None:
            os.close(fd)


def mkdtemp(prefix: str, parent: str | os.PathLike | None = None) -> str:
    """tempfile.mkdtemp's stand-in: a stable, empty directory whose slot stays held until
    this process exits. The caller removes the directory, as it removed mkdtemp's."""
    path, fd = _take(prefix, parent)
    _cache_env(stage_root() if parent is None else Path(parent).resolve())
    if fd is not None:
        _HELD.append(fd)
    return str(path)


def selftest() -> int:
    """Stable across uses, exclusive while held, emptied when taken, caller's cache wins."""
    saved = {name: os.environ.pop(name, None) for name in ("TMPDIR", "CCACHE_BASEDIR", "CCACHE_NOHASHDIR")}
    with tempfile.TemporaryDirectory(prefix="mutant-stage-selftest-") as scratch:
        os.environ["TMPDIR"] = scratch
        tempfile.tempdir = None
        try:
            with directory("ctl-") as first:
                Path(first, "planted.sv").write_text("module m; endmodule\n")
                assert os.environ["CCACHE_BASEDIR"] == str(stage_root())
                assert os.environ["CCACHE_NOHASHDIR"] == "1"
                with directory("ctl-") as second:
                    assert second != first and second.endswith("ctl-1"), (first, second)
            assert "CCACHE_BASEDIR" not in os.environ and not Path(first).exists()
            print("mutant stage control: a held slot is never handed out twice")
            with directory("ctl-") as again:
                assert again == first and list(Path(again).iterdir()) == [], again
            print("mutant stage control: the same path in every run, and empty")
            stale = Path(first)
            stale.mkdir()
            (stale / "left-by-a-killed-run.o").write_text("stale\n")
            with directory("ctl-") as taken:
                assert taken == first and list(Path(taken).iterdir()) == [], taken
            print("mutant stage control: a killed run's leftovers are cleared when the slot is taken")
            held = [_take("full-", None) for _ in range(SLOTS)]
            with directory("full-") as cold:
                assert Path(cold).name.startswith("full-") and Path(cold).name not in {
                    f"full-{slot}" for slot in range(SLOTS)}, cold
            for _, fd in held:
                os.close(fd)
            print("mutant stage control: with every slot held, a random directory, still correct")
            os.environ["CCACHE_BASEDIR"] = "/caller"
            with directory("ctl-"):
                assert os.environ["CCACHE_BASEDIR"] == "/caller"
            assert os.environ.pop("CCACHE_BASEDIR") == "/caller"
            print("mutant stage control: a caller's CCACHE_BASEDIR wins")
            tree = Path(scratch, "tree")
            tree.mkdir()
            kept = mkdtemp("in-tree-", parent=tree)
            assert kept == str(tree.resolve() / "in-tree-0") and sorted(os.listdir(tree)) == ["in-tree-0"]
            shutil.rmtree(kept)
            print("mutant stage control: an in-tree directory leaves nothing else in the tree")
            for bad in ("a/b", "", ".."):
                try:
                    _take(bad, None)
                except ValueError:
                    continue
                raise AssertionError(f"accepted prefix {bad!r}")
            print("mutant stage control: a prefix naming more than one directory is refused")
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
