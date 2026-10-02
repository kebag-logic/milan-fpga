#!/usr/bin/env python3
"""Resolve every path a traced campaign wrote (opened for writing, created,
renamed, linked, unlinked, made a directory) and group it by owner: a unit's
private copy (TMPDIR/<copy>), the campaign's output directory, the review
clone, or anything else (a candidate shared path).

The trace is `strace -ff -y -o DIR/t`: one file per process, so no line is
split; a child's working directory is inherited from its parent's at clone
time and followed through chdir/fchdir.

usage: strace_writes.py TRACE_DIR ROOT_PID_CWD TMPDIR OUTDIR CLONE
"""
import collections
import os
import re
import sys
from pathlib import Path

CALL = re.compile(r'^(\w+)\((.*)\)\s+=\s+(-?\d+)')
ARG_PATH = re.compile(r'(?:(AT_FDCWD|-?\d+<([^>]*)>),\s*)?"([^"]*)"')
WRITE_FLAGS = ("O_WRONLY", "O_RDWR", "O_CREAT")


def resolve(cwd: str, dirpath: str | None, path: str) -> str:
    base = dirpath if dirpath else cwd
    return os.path.normpath(path if path.startswith("/") else os.path.join(base, path))


def main() -> int:
    trace, start_cwd, tmp, out, clone = sys.argv[1:6]
    files = {int(p.name.split(".")[-1]): p for p in Path(trace).glob("t.*")}
    parent_of, cwd_at_clone = {}, {}
    # pass 1: clone results give the child's parent and the order of events
    events = {}
    for pid, path in files.items():
        events[pid] = [line.rstrip("\n") for line in path.open(errors="replace")]
    root = min(files)
    cwd = {}
    written = collections.Counter()

    def walk(pid: int, initial: str) -> None:
        here = initial
        for line in events.get(pid, ()):
            m = CALL.match(line)
            if not m:
                continue
            name, args, ret = m.group(1), m.group(2), int(m.group(3))
            if name in ("clone", "clone3", "fork", "vfork") and ret > 0:
                walk(ret, here)
                continue
            if ret < 0:
                continue
            if name == "chdir":
                here = resolve(here, None, ARG_PATH.search(args).group(3))
                continue
            if name == "fchdir":
                fd = re.match(r'-?\d+<([^>]*)>', args)
                if fd:
                    here = fd.group(1)
                continue
            if name in ("openat", "open", "creat"):
                if name != "creat" and not any(f in args for f in WRITE_FLAGS):
                    continue
                paths = [ARG_PATH.search(args)]
            elif name in ("mkdir", "mkdirat", "rename", "renameat", "renameat2", "unlink",
                          "unlinkat", "link", "linkat", "symlink", "symlinkat"):
                paths = list(ARG_PATH.finditer(args))
                if name.startswith("symlink"):
                    paths = paths[1:]  # the target text is not a written path
            else:
                continue
            for p in paths:
                if p:
                    written[resolve(here, p.group(2), p.group(3))] += 1

    walk(root, start_cwd)
    copies, outputs, in_clone, other = collections.Counter(), set(), set(), collections.Counter()
    kinds = collections.Counter()
    for p, n in written.items():
        if p.startswith(tmp + "/"):
            top = p[len(tmp) + 1:].split("/")[0]
            copies[top] += n
        elif p.startswith(out + "/") or p == out:
            outputs.add(p)
        elif p.startswith(clone + "/") or p == clone:
            in_clone.add(p)
        else:
            other[p] += n
    for top in copies:
        if re.fullmatch(r"cc[A-Za-z0-9]{6}\..*", top):
            kinds["cc??????.* (compiler mkstemp temporaries)"] += 1
        elif re.fullmatch(r"GMfifo\d+", top):
            kinds["GMfifo<pid> (make jobserver fifo, one per make)"] += 1
        elif re.fullmatch(r"[\w-]+-mutants-[\w]{8}|[\w-]+-[\w]{8}", top):
            kinds[re.sub(r"[\w]{8}$", "<random>", top) + " (unit copy)"] += 1
        else:
            kinds[top + " (UNCLASSIFIED)"] += 1
    print(f"processes traced: {len(files)}")
    print(f"unit copies written: {len(copies)} ({sum(copies.values())} write events)")
    for k, n in sorted(kinds.items()):
        print(f"  {n:5d} TMPDIR entries like {k}")
    print(f"output-directory paths written: {len(outputs)}")
    print(f"review-clone paths written: {len(in_clone)}")
    for p in sorted(in_clone):
        print(f"  CLONE {p}")
    print(f"other paths written: {len(other)}")
    for p, n in sorted(other.items()):
        print(f"  {n:6d} {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
