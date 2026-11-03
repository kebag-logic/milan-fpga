#!/usr/bin/env python3
"""Preflight cost: each owner control alone, then the whole test, at two trees.

usage: python3 -I -B cost.py <old tree> <new tree> <rounds> <whole runs> <jobs>
Controls run one at a time, alternating trees, `rounds` times; the whole test runs
`whole runs` times per tree, `jobs` at once. Each run is a fresh interpreter.
"""
import concurrent.futures
import subprocess
import sys
import time
from pathlib import Path

old, new = Path(sys.argv[1]), Path(sys.argv[2])
rounds, whole, jobs = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
CONTROLS = ("owner_report", "owner_reparented", "owner_late_exit", "owner_stall", "owner_shell_window",
            "owner_survivor", "owner_vanishing", "owner_late_cancel", "owner_stated_seconds", "owner_reused_identity")


def run(tree: Path, control: str | None) -> tuple[int, float]:
    """One run from a tree; its status and wall seconds."""
    argv = [sys.executable, "-B", "scripts/test_suite_cancellation.py", *(["--control", control] if control else [])]
    began = time.monotonic()
    status = subprocess.run(argv, cwd=tree, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                            stdin=subprocess.DEVNULL, timeout=600).returncode
    return status, time.monotonic() - began


print("load", Path("/proc/loadavg").read_text().strip(), flush=True)
times = {}
for _round in range(rounds):
    for control in CONTROLS:
        for label, tree in (("old", old), ("new", new)):
            status, seconds = run(tree, control)
            times.setdefault((label, control), []).append((status, seconds))
for control in CONTROLS:
    cells = [f"{label} " + " ".join(f"{s:.2f}" + ("" if st == 0 else f"(rc {st})") for st, s in times[(label, control)])
             for label in ("old", "new")]
    print(f"{control}: " + "; ".join(cells), flush=True)
print("load", Path("/proc/loadavg").read_text().strip(), flush=True)
runs = [(label, tree) for _i in range(whole) for label, tree in (("old", old), ("new", new))]
with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
    results = list(pool.map(lambda r: (r[0], run(r[1], None)), runs))
for label in ("old", "new"):
    mine = [(st, s) for name, (st, s) in results if name == label]
    print(f"whole {label}: " + " ".join(f"{s:.1f}" for _st, s in mine)
          + f"; mean {sum(s for _st, s in mine) / len(mine):.1f} s; all rc 0: {all(st == 0 for st, _s in mine)}",
          flush=True)
print("load", Path("/proc/loadavg").read_text().strip(), flush=True)
