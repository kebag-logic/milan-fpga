#!/usr/bin/env python3
"""Cost of the round-5 names() walk on a deep and wide note, against the round-4 gate on the same file.

Usage: probe_r5_size.py <repo checkout> <scratch dir>

names() pushes every child of an object or list with its full path tuple, so a list of W items at depth d holds W
tuples of length d on the stack until they are popped. A note shaped as W items per level, the deeper list first,
keeps about W * d tuples alive at depth d. This probe writes such a note into a copy of the committed baseline
(the description note, which the gate never reads as data), runs check-baseline as a separate process under the
head's gate and under the round-4 gate (79e53831, the same file layout), and records exit status, wall time,
peak resident memory and the last line. Each child runs under an address-space cap (CAP_GB) so a blow-up shows
as a refusal or a kill rather than taking the host's memory.
"""
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import sys
import time

CAP_GB = 6
repo, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
shutil.rmtree(scratch, ignore_errors=True)
(scratch / "r4").mkdir(parents=True)
for module in ("pp_resource_gate.py", "pp_baseline_rank.py", "pp_resource_gate_selftest.py"):
    data = subprocess.run(["git", "-C", str(repo), "show", f"79e53831a4f623a594f22765be1d05dffeb696a7:syn/ooc/{module}"],
                          capture_output=True, check=True).stdout
    (scratch / "r4" / module).write_bytes(data)
GATES = {"head ec7eb2d8": repo / "syn/ooc/pp_resource_gate.py", "round-4 79e53831": scratch / "r4/pp_resource_gate.py"}
BASE = (repo / "syn/ooc/pp_resource_baseline.json").read_text()
BUDGET = repo / "docs/design/AREA_BUDGET.md"


def note(depth: int, width: int) -> str:
    text = "0"
    for _ in range(depth):
        text = "[" + text + ", 0" * (width - 1) + "]"
    return text


def limit():
    cap = CAP_GB * 1024 ** 3
    resource.setrlimit(resource.RLIMIT_AS, (cap, cap))


#: A fresh wrapper per run, so the peak it reports is that one gate process's own.
WRAP = ("import resource, subprocess, sys; p = subprocess.run(sys.argv[1:]); "
        "print('PEAK', resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss, file=sys.stderr); sys.exit(p.returncode)")


def run(gate: Path, path: Path) -> tuple:
    start = time.monotonic()
    proc = subprocess.run([sys.executable, "-c", WRAP, sys.executable, "-B", str(gate), "check-baseline", "--baseline",
                           str(path), "--budget", str(BUDGET)], capture_output=True, text=True, timeout=1800,
                          preexec_fn=limit)
    wall = time.monotonic() - start
    peak = int(next(line.split()[1] for line in proc.stderr.splitlines() if line.startswith("PEAK")))
    err = [line for line in proc.stderr.splitlines() if not line.startswith("PEAK")]
    last = (proc.stdout.strip().splitlines() or err or [""])[-1]
    return proc.returncode, wall, peak, "Traceback" in proc.stderr, last[:150]


print(f"address-space cap per run: {CAP_GB} GiB; peak RSS is the gate process's own (ru_maxrss)")
for depth, width in ((1, 1000), (100, 1000), (300, 1000), (500, 1000), (700, 1000), (900, 1000), (900, 2000),
                     (2000, 10)):
    path = scratch / f"note-d{depth}-w{width}.json"
    data = json.loads(BASE)
    data["description"] = "__NOTE__"
    path.write_text(json.dumps(data).replace('"__NOTE__"', note(depth, width)))
    size = path.stat().st_size
    for label, gate in GATES.items():
        rc, wall, peak, tb, last = run(gate, path)
        print(f"depth {depth:5d} width {width:5d} file {size / 1e6:7.2f} MB  {label:17s} rc {rc:3d} "
              f"wall {wall:7.2f} s  peak RSS {peak / 1024:8.0f} MiB  traceback {tb}  :: {last}")
