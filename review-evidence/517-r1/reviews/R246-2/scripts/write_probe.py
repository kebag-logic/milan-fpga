#!/usr/bin/env python3
"""R246-2 per-leg write-set probe (file-operation audit) with a positive control.

  write_probe.py run <suite-dir> <out-dir> <tmpdir> <leg-exe>...
      Run each leg (relative path, from the suite dir, no argument, stdout and
      stderr to <out-dir>/<leg>.out, frame-dump variable absent) under
      `strace -f -y` restricted to path/fd-creating syscalls, <= 8 at once.
  write_probe.py report <out-dir> <suite-dir> <tmpdir> <receipt.json>
      Parse every <leg>.strace: every path a leg (or any descendant: sh,
      python builder, image generator) created, opened for writing, truncated,
      renamed, linked, unlinked, chmodded, utimed, mkdir'd or rmdir'd. Relative
      paths are resolved against the leg's cwd (the suite dir; any chdir is
      reported). Private milan_nxn_XXXXXX components are normalized to report
      the SHAPE of each write set, and the raw per-leg paths are compared
      pairwise for any shared written path.

A leg named plant:<label> runs scripts/planted_writer.sh instead: the positive
control, which writes a tracked file, a new ignored file and a transient mkdtemp
directory through a grandchild process.
"""
import concurrent.futures
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SYSCALLS = ("open,openat,openat2,creat,mkdir,mkdirat,rename,renameat,renameat2,unlink,unlinkat,"
            "rmdir,link,linkat,symlink,symlinkat,truncate,chmod,fchmodat,fchmodat2,utimensat,"
            "utimes,utime,mknod,mknodat,chdir,fchdir")
WRITE_FLAGS = ("O_WRONLY", "O_RDWR", "O_CREAT", "O_TRUNC", "O_APPEND")
HERE = Path(__file__).resolve().parent


def run_one(suite: Path, out: Path, tmpdir: str, leg: str) -> dict:
    name = leg.replace("/", "_").replace(".", "").strip("_")
    env = {k: v for k, v in os.environ.items() if k != "MILAN_COUNTER_FRAME_OUT"}
    env["TMPDIR"] = tmpdir
    argv = [str(HERE / "planted_writer.sh")] if leg.startswith("plant:") else [leg]
    with (out / f"{name}.out").open("wb") as fh:
        rc = subprocess.run(["strace", "-f", "--seccomp-bpf", "-qq", "-y", "-s", "4096", "-e", f"trace={SYSCALLS}",
                             "-e", "signal=none", "-o", str(out / f"{name}.strace"), *argv],
                            cwd=suite, env=env, stdout=fh, stderr=subprocess.STDOUT,
                            stdin=subprocess.DEVNULL).returncode
    return dict(leg=leg, name=name, rc=rc)


LINE = re.compile(r"^(\d+)\s+(\w+)\((.*)\)\s+=\s+(-?\d+)(<[^>]*>)?")


def parse(path: Path, suite: str) -> dict:
    writes, chdirs, failed = set(), [], 0
    for raw in path.read_text(errors="replace").splitlines():
        m = LINE.match(raw)
        if not m:
            continue
        _pid, call, args, ret, fdpath = m.groups()
        if call in ("chdir", "fchdir"):
            chdirs.append(raw)
            continue
        if int(ret) < 0:
            failed += 1
            continue
        strings = re.findall(r'"((?:[^"\\]|\\.)*)"', args)
        if call in ("open", "openat", "openat2", "creat"):
            if call != "creat" and not any(f in args for f in WRITE_FLAGS):
                continue
            target = fdpath[1:-1] if fdpath else strings[0]
            if target.startswith("/dev/") or target.startswith("pipe:"):
                continue
            writes.add(("open-write", target if target.startswith("/") else os.path.join(suite, target)))
            continue
        # *at calls: resolve a relative name against its dirfd (-y prints N</path>).
        bases = re.findall(r"(AT_FDCWD|\d+<[^>]*>),\s*\"", args)
        picks = strings[:2] if call.startswith(("rename", "link", "symlink")) else strings[:1]
        for k, s in enumerate(picks):
            base = suite
            if call.endswith("at") or call.endswith("at2"):
                if k < len(bases) and bases[k] != "AT_FDCWD":
                    base = bases[k].split("<", 1)[1][:-1]
            writes.add((call, s if s.startswith("/") else os.path.normpath(os.path.join(base, s))))
    return dict(writes=sorted(writes), chdirs=chdirs, failed_calls=failed)


def main() -> int:
    mode = sys.argv[1]
    if mode == "run":
        suite, out, tmpdir, legs = Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4], sys.argv[5:]
        out.mkdir(parents=True, exist_ok=True)
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            for row in pool.map(lambda leg: run_one(suite, out, tmpdir, leg), legs):
                print(json.dumps(row), flush=True)
        return 0
    out, suite, tmpdir, receipt = Path(sys.argv[2]), sys.argv[3], sys.argv[4], Path(sys.argv[5])
    legs = {}
    for trace in sorted(out.glob("*.strace")):
        legs[trace.stem] = parse(trace, suite)
    norm = lambda p: re.sub(r"milan_nxn_[A-Za-z0-9]{6}", "milan_nxn_XXXXXX", p) \
        .replace(tmpdir, "$TMPDIR").replace(suite, "$SUITE") \
        .replace(str(Path(suite).parents[2]), "$TREE")
    report = {}
    for name, row in legs.items():
        paths = sorted({p for _c, p in row["writes"]})
        outside = [p for p in paths if not p.startswith(tmpdir + "/milan_nxn_")]
        report[name] = dict(
            write_ops=len(row["writes"]), distinct_paths=len(paths),
            chdirs=row["chdirs"], failed_calls=row["failed_calls"],
            private_dirs=sorted({re.search(r"milan_nxn_[A-Za-z0-9]{6}", p).group(0)
                                 for p in paths if "milan_nxn_" in p}),
            files_in_private_dir=sorted({norm(p) for c, p in row["writes"]
                                         if c == "open-write" and "milan_nxn_" in p}),
            written_outside_private_dir=[norm(p) for p in outside],
            ops=sorted({f"{c} {norm(p)}" for c, p in row["writes"]}))
    names = sorted(legs)
    shared = []
    for i, a in enumerate(names):
        pa = {p for _c, p in legs[a]["writes"]}
        for b in names[i + 1:]:
            common = pa & {p for _c, p in legs[b]["writes"]}
            if common:
                shared.append(dict(a=a, b=b, paths=sorted(norm(p) for p in common)))
    receipt.write_text(json.dumps(dict(legs=report, shared_written_paths=shared), indent=1) + "\n")
    for name in names:
        r = report[name]
        print(f"{name}: ops={r['write_ops']} paths={r['distinct_paths']} private_dirs={r['private_dirs']} "
              f"files_in_private={len(r['files_in_private_dir'])} outside={r['written_outside_private_dir']} "
              f"chdirs={len(r['chdirs'])}")
    print("shared written paths between legs:", json.dumps(shared) if shared else "NONE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
