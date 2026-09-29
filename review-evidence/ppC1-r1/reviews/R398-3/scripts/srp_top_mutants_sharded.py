#!/usr/bin/env python3
"""Run the checked-in tb/srp_top mutation driver unchanged, sharded by arm label.

usage:
  srp_top_mutants_sharded.py run   <repo> <outdir> <nshards> <shard> [<shard> ...]
  srp_top_mutants_sharded.py merge <repo> <outdir> <nshards>

`run` starts the given shards in parallel (one process each; call with at most 8),
each as `python3 tb/srp_top/mutants.py --output <outdir>/shard<i> --only <labels>`
with TMPDIR inside <outdir>, and waits for all of them in the foreground.
`merge` reads every shard's stdout and applies the driver's own full-run rules:
every control PASS, every arm KILLED, and the assertion-coverage set equal to the
driver's expected K..R set (the check the driver only makes on an unfiltered run).
"""
import os
import re
import subprocess
import sys
from pathlib import Path


def labels(repo: Path) -> list[str]:
    src = (repo / "tb/srp_top/mutants.py").read_text()
    seen: list[str] = []
    for lab in re.findall(r"^\s+\('([^']+)', '[a-z_]+', '[a-z]*', ", src, re.M):
        if lab not in seen:
            seen.append(lab)
    return seen


def shards(repo: Path, n: int) -> list[list[str]]:
    labs = labels(repo)
    return [labs[i::n] for i in range(n)]


def expected(repo: Path) -> set[str]:
    src = (repo / "tb/srp_top/mutants.py").read_text()
    pairs = re.findall(r'\("([A-Z])", (\d+)\)', src)
    return {f"{g}{i}" for g, c in pairs for i in range(1, int(c) + 1)}


def run(repo: Path, out: Path, n: int, which: list[int]) -> int:
    procs = []
    for i in which:
        d = out / f"shard{i}"
        tmp = out / f"tmp{i}"
        d.mkdir(parents=True, exist_ok=True)
        tmp.mkdir(parents=True, exist_ok=True)
        env = dict(os.environ, TMPDIR=str(tmp))
        log = (out / f"shard{i}.stdout").open("w")
        cmd = ["python3", str(repo / "tb/srp_top/mutants.py"), "--output", str(d),
               "--only", ",".join(shards(repo, n)[i])]
        procs.append((i, subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, env=env)))
    rc = 0
    for i, p in procs:
        r = p.wait()
        print(f"shard{i} rc={r}", flush=True)
        rc |= r != 0
    return rc


def merge(repo: Path, out: Path, n: int) -> int:
    covered: set[str] = set()
    arms = killed = controls = cpass = 0
    bad = []
    for i in range(n):
        text = (out / f"shard{i}.stdout").read_text()
        for line in text.splitlines():
            m = re.match(r"control (\S+) (\S*): rc=(\d+) (PASS|FAIL)", line)
            if m:
                controls += 1
                cpass += m.group(4) == "PASS"
                if m.group(4) != "PASS":
                    bad.append(line)
            m = re.match(r"(\S+): rc=(\d+) failures=(\d+) (KILLED|UNPROVEN) tags=(.*)", line)
            if m:
                arms += 1
                if m.group(4) == "KILLED":
                    killed += 1
                    covered.update(t for t in m.group(5).split(",") if t)
                else:
                    bad.append(line)
    exp = expected(repo)
    missing = sorted(exp - covered)
    print(f"controls {cpass}/{controls} PASS (per shard; groups repeat across shards)")
    print(f"arms {killed}/{arms} KILLED")
    print(f"assertion coverage: {len(exp) - len(missing)}/{len(exp)}; missing={missing}")
    for b in bad:
        print("BAD", b)
    return int(bool(bad) or bool(missing) or arms == 0)


def main() -> int:
    mode, repo, out, n = sys.argv[1], Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve(), int(sys.argv[4])
    if mode == "run":
        return run(repo, out, n, [int(x) for x in sys.argv[5:]])
    return merge(repo, out, n)


if __name__ == "__main__":
    raise SystemExit(main())
