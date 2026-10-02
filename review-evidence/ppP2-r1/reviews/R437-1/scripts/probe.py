#!/usr/bin/env python3
"""Reviewer probe driver for tb/nvm_port (PR #145, head 70bf017d).

Each probe = a fresh copy of the exported head tree, a list of exact-once text
edits (file relative to the tree root, old, new), then `make` in the suite dir.
Records the tally line and every FAIL line. Runs probes concurrently.

usage: probe.py HEAD_TREE OUT_DIR JOBS PROBESET.py
PROBESET.py defines PROBES = [(name, suite_dir, [(path, old, new), ...]), ...]
"""
import concurrent.futures as cf
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

TALLY = re.compile(r"(\d+) checks: (\d+) PASS, (\d+) FAIL")


def run_probe(head: Path, out: Path, name: str, suite: str, edits):
    work = out / "work" / name
    if work.exists():
        shutil.rmtree(work)
    shutil.copytree(head, work, symlinks=True)
    for rel, old, new in edits:
        p = work / rel
        t = p.read_text()
        n = t.count(old)
        if n != 1:
            return name, f"ANCHOR {rel} occurs {n} times: {old[:80]!r}", None
        p.write_text(t.replace(old, new, 1))
    # keep each build to 2 compile threads so 16 probes share 16 cores
    mk = work / suite / "Makefile"
    mk.write_text(mk.read_text().replace("--build -j 0", "--build -j 2"))
    p = subprocess.run(["make", "-s"], cwd=work / suite, capture_output=True,
                       text=True, timeout=3000)
    log = p.stdout + p.stderr
    (out / f"{name}.log").write_text(log)
    tallies = TALLY.findall(log)
    fails = [l for l in log.splitlines() if l.startswith("FAIL")]
    shutil.rmtree(work, ignore_errors=True)
    return name, f"rc={p.returncode} tallies={tallies} fails={len(fails)}", fails


def main():
    head, out, jobs, pset = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    out.mkdir(parents=True, exist_ok=True)
    ns = {}
    exec(Path(pset).read_text(), ns)
    probes = ns["PROBES"]
    summary = []
    with cf.ThreadPoolExecutor(max_workers=jobs) as ex:
        futs = {ex.submit(run_probe, head, out, n, s, e): n for n, s, e in probes}
        for f in cf.as_completed(futs):
            name, res, fails = f.result()
            line = f"{name}: {res}"
            if fails:
                line += "\n    first: " + "\n    ".join(fails[:4])
            print(line, flush=True)
            summary.append((name, line))
    summary.sort()
    (out / "SUMMARY.txt").write_text("\n".join(l for _, l in summary) + "\n")


if __name__ == "__main__":
    main()
