#!/usr/bin/env python3
"""R246-1: compare the `run` recipe's executed commands at dev (sequential)
and at the PR head (pooled), from `make -n run` of each Makefile.

Usage: python3 inventory.py <probe-tree> <dev-rev> <head-rev> <receipt-file>

The probe tree's Makefile is replaced by each revision's bytes in turn (via
`git show`) and restored to the head bytes afterwards. Every executable leg,
banner, build output and post-pool driver is listed in execution order; the
pooled legs are expanded from sim_pool.py's argv in recipe order.
"""
import shlex
import subprocess
import sys
from pathlib import Path

MK = "tb/verilator/milan_dp/Makefile"


def dry(tree: Path, extra: list[str]) -> list[str]:
    out = subprocess.run(["make", "-n", "-C", str(tree / "tb/verilator/milan_dp"), "run", *extra],
                         capture_output=True, text=True, check=True).stdout
    return out.replace("\\\n", " ").splitlines()


def events(lines: list[str]) -> list[str]:
    seq = []
    for line in lines:
        s = line.strip()
        if s.startswith("exec python3 sim_pool.py"):
            words = shlex.split(s)[3:]
            jobs = words.pop(0)
            seq.append(f"POOL-START {jobs}")
            it = iter(words)
            for w in it:
                if w == "--banner":
                    seq.append("BANNER " + next(it))
                elif w == "--exclusive":
                    seq.append("EXCLUSIVE-NEXT")
                else:
                    seq.append("LEG " + w)
            seq.append("POOL-END")
        elif s.startswith("echo \"----") or s.startswith("echo \"===="):
            seq.append("BANNER " + shlex.split(s)[1])
        elif s.startswith("./"):
            seq.append("LEG " + s)
        elif s.startswith("python3 ") and ("mutants" in s or "controls" in s):
            seq.append("DRIVER " + s)
        elif " -o V" in s:
            seq.append("BUILD " + s.rsplit(" -o ", 1)[1].split()[0])
    return seq


def main() -> int:
    tree, dev, head, receipt = Path(sys.argv[1]), sys.argv[2], sys.argv[3], Path(sys.argv[4])
    original = (tree / MK).read_bytes()
    report = []
    try:
        seqs = {}
        for label, rev, extra in (("dev", dev, []), ("head", head, []),
                                  ("head-SIM_JOBS=1", head, ["SIM_JOBS=1"])):
            blob = subprocess.run(["git", "-C", str(tree), "show", f"{rev}:{MK}"],
                                  capture_output=True, check=True).stdout
            (tree / MK).write_bytes(blob)
            seqs[label] = events(dry(tree, extra))
            report.append(f"## {label} ({rev}) make -n run {' '.join(extra)}")
            report += seqs[label]
            report.append("")
    finally:
        (tree / MK).write_bytes(original)
    legs = {k: [e for e in v if e.startswith("LEG ")] for k, v in seqs.items()}
    banners = {k: [e for e in v if e.startswith("BANNER ")] for k, v in seqs.items()}
    builds = {k: [e for e in v if e.startswith("BUILD ")] for k, v in seqs.items()}
    drivers = {k: [e for e in v if e.startswith("DRIVER ")] for k, v in seqs.items()}
    no_pool = {k: [e for e in v if e not in ("EXCLUSIVE-NEXT", "POOL-END")
                   and not e.startswith("POOL-START")] for k, v in seqs.items()}
    report.append("## comparison")
    report.append(f"legs dev={len(legs['dev'])} head={len(legs['head'])} identical order: {legs['dev'] == legs['head']}")
    report.append(f"duplicate legs head: {len(legs['head']) - len(set(legs['head']))}")
    report.append(f"banners identical: {banners['dev'] == banners['head']}")
    report.append(f"builds identical order: {builds['dev'] == builds['head']} ({len(builds['head'])})")
    report.append(f"post drivers identical: {drivers['dev'] == drivers['head']} {drivers['head']}")
    report.append(f"full interleaved sequence identical (pool markers removed): {no_pool['dev'] == no_pool['head']}")
    report.append(f"SIM_JOBS=1 sequence identical to default except jobs: "
                  f"{[e for e in seqs['head'] if not e.startswith('POOL-START')] == [e for e in seqs['head-SIM_JOBS=1'] if not e.startswith('POOL-START')]}")
    report.append(f"pool jobs default/SIM_JOBS=1: {[e for e in seqs['head'] if e.startswith('POOL-START')]} "
                  f"{[e for e in seqs['head-SIM_JOBS=1'] if e.startswith('POOL-START')]}")
    excl = []
    hs = seqs["head"]
    for i, e in enumerate(hs):
        if e == "EXCLUSIVE-NEXT":
            excl.append(hs[i + 1])
    report.append(f"exclusive legs (recipe order): {excl}")
    receipt.write_text("\n".join(report) + "\n")
    print("\n".join(report[report.index('## comparison'):]))
    assert (tree / MK).read_bytes() == original
    return 0


if __name__ == "__main__":
    sys.exit(main())
