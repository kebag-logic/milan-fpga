#!/usr/bin/env python3
"""Per-leg write-set audit for the pooled milan_dp legs (review receipt tool).

    python3 audit_writes.py <suite-dir> <out-dir> <tmpdir> <jobs> EXE ...

Runs each EXE from <suite-dir> under `strace -f --seccomp-bpf` restricted to
path-creating/modifying syscalls, at most <jobs> at once (never more than 8),
with TMPDIR=<tmpdir>. Writes <out-dir>/<leg>.strace, <leg>.out and a summary
<out-dir>/writes.json: for every leg, its exit status and the sorted set of
paths it successfully opened for writing, created, renamed, linked, removed or
made. Unique mkdtemp names are normalised to milan_nxn_<X> only in the
`shared` computation; the raw sets are kept verbatim. Exit 0 only when every
leg exited 0.
"""

import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SYSCALLS = ("open,openat,openat2,creat,rename,renameat,renameat2,unlink,unlinkat,"
            "mkdir,mkdirat,link,linkat,symlink,symlinkat,truncate,rmdir")
WRITE_FLAGS = ("O_WRONLY", "O_RDWR", "O_CREAT", "O_TRUNC", "O_APPEND")
LINE = re.compile(r'^(?P<pid>\d+)\s+(?P<call>\w+)\((?P<args>.*)\)\s+=\s+(?P<ret>-?\d+)')
QUOTED = re.compile(r'"((?:[^"\\]|\\.)*)"')
#: an *at call's (dirfd, name) pair; strace -y prints a dirfd as N</path>
#: and the current directory as AT_FDCWD</path>
AT_PAIR = re.compile(r'(?:AT_FDCWD(?:<(?P<cwd>[^>]*)>)?|\d+<(?P<dir>[^>]*)>),\s*'
                     r'"(?P<name>(?:[^"\\]|\\.)*)"')


def written_paths(trace: Path, cwd: Path) -> list[str]:
    """Paths a successful call in this trace created, wrote or removed."""
    found = set()
    for raw in trace.read_text(errors="replace").splitlines():
        m = LINE.match(raw)
        if not m or int(m["ret"]) < 0:
            continue
        call, args = m["call"], m["args"]
        if call.endswith("at") or call in ("renameat2", "openat2"):
            pairs = [(pm["dir"] or pm["cwd"], pm["name"]) for pm in AT_PAIR.finditer(args)]
        else:
            pairs = [(None, name) for name in QUOTED.findall(args)]
        if not pairs:
            continue
        if call.startswith("open") or call == "creat":
            if call != "creat" and not any(flag in args for flag in WRITE_FLAGS):
                continue
            pairs = pairs[:1]
        for base, name in pairs:
            path = Path(name)
            if not path.is_absolute():
                path = Path(base) / path if base else cwd / path
            found.add(os.path.normpath(path))
    return sorted(found)


def run_leg(suite: Path, out: Path, tmpdir: Path, exe: str) -> dict:
    """One leg under strace, from the suite directory, TMPDIR pinned."""
    name = Path(exe).name
    trace = out / f"{name}.strace"
    env = dict(os.environ, TMPDIR=str(tmpdir))
    with (out / f"{name}.out").open("wb") as capture:
        proc = subprocess.run(
            ["strace", "-f", "--seccomp-bpf", "-qq", "-y", "-s", "4096", "-e",
             f"trace={SYSCALLS}", "-o", str(trace), exe],
            cwd=suite, env=env, stdin=subprocess.DEVNULL, stdout=capture,
            stderr=subprocess.STDOUT, check=False)
    return {"leg": exe, "exit": proc.returncode,
            "writes": written_paths(trace, suite)}


def main(argv: list[str]) -> int:
    """Audit every leg; print the shared-path verdict."""
    suite, out, tmpdir = (Path(a).resolve() for a in argv[:3])
    jobs = min(int(argv[3]), 8)
    legs = argv[4:]
    out.mkdir(parents=True, exist_ok=True)
    tmpdir.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        results = list(pool.map(lambda exe: run_leg(suite, out, tmpdir, exe), legs))
    owners: dict[str, set[str]] = {}
    private = re.compile(re.escape(str(tmpdir)) + r"/milan_nxn_[A-Za-z0-9]{6}(/|$)")
    for result in results:
        result["outside_private_scratch"] = [
            path for path in result["writes"] if not private.match(path)]
        for path in result["writes"]:
            owners.setdefault(path, set()).add(result["leg"])
    shared = {path: sorted(legs_) for path, legs_ in owners.items() if len(legs_) > 1}
    summary = {"suite": str(suite), "tmpdir": str(tmpdir), "results": results,
               "shared": shared}
    (out / "writes.json").write_text(json.dumps(summary, indent=1) + "\n")
    for result in results:
        print(f"{result['exit']:>3} {len(result['writes']):>4} writes "
              f"{len(result['outside_private_scratch']):>3} outside private "
              f"milan_nxn_* scratch  {result['leg']}")
        for path in result["outside_private_scratch"]:
            print(f"      outside: {path}")
    print(f"exact paths written by more than one leg: {len(shared)}")
    for path, legs_ in sorted(shared.items()):
        print(f"  {path}: {', '.join(legs_)}")
    return 0 if all(r["exit"] == 0 for r in results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
