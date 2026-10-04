#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run follow_ring's two reproductions across their phase sweeps, in parallel.

  sweep.py b8     [--jobs N] [--phases K] [--jitter-us J ...] [--hold-s S]
  sweep.py pullin [--jobs N] [--phases K] [--hold-us U ...]

b8: lane B8's INTERNAL-to-AAF set at K places in one INTERNAL beat (the
loopback ring's margin at the set runs once round its range across them), at
each listed arrival jitter, with an optional rare tail (--tail-us, --tail-p).
Each run prints its slips after LOCKED; the table is one row per run.

pullin: one serial-clock hold under a running stream at INTERNAL, with the
stream's arrival latency at K places across one media tick (the feed's phase
against the grid), for each listed hold length. Each run prints the render
stage's first-event delay before and after the pull and whether the stream
left the render law.

The executable is MDIR/Vfollow_ring (make build). Every run's own log lands
in OUT/<name>.log beside the table OUT/<case>.md, and the exit status is 0
once every run completed, whatever the runs measured: the reproductions
record a defect, they do not grade one.
"""

import argparse
import concurrent.futures as cf
import re
import subprocess
import sys
from pathlib import Path

TICK_US = 1e6 / 48000.0


def run(exe: Path, out: Path, name: str, args: list[str]) -> tuple[str, int, str]:
    """One harness run; its log, its exit status and its RESULT line."""
    log = out / f"{name}.log"
    with log.open("w") as fh:
        rc = subprocess.run([str(exe), *args], stdout=fh, stderr=subprocess.STDOUT, check=False).returncode
    text = log.read_text()
    found = re.findall(r"^RESULT-6\d\d: .*$", text, re.M)
    return name, rc, found[-1] if found else "(no RESULT line)"


def main() -> int:
    """Build the run list, run it on a pool, write the table."""
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("case", choices=("b8", "pullin"))
    ap.add_argument("--exe", type=Path, default=Path("obj_dir/Vfollow_ring"))
    ap.add_argument("--out", type=Path, default=Path("obj_dir/sweep"))
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--phases", type=int, default=16)
    ap.add_argument("--jitter-us", type=float, nargs="+", default=[0.0])
    ap.add_argument("--tail-us", type=float, default=0.0)
    ap.add_argument("--tail-p", type=float, default=0.0)
    ap.add_argument("--hold-s", type=float, default=60.0)
    ap.add_argument("--hold-us", type=float, nargs="+", default=[52.0])
    ap.add_argument("--latency-us", type=float, default=200.0)
    ap.add_argument("--extra", nargs=argparse.REMAINDER, default=[],
                    help="arguments passed to every run")
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    runs = []
    if a.case == "b8":
        for jit in a.jitter_us:
            for k in range(a.phases):
                ph = k / a.phases
                tail = f"_t{a.tail_us:g}x{a.tail_p:g}" if a.tail_p > 0.0 else ""
                runs.append((f"b8_j{jit:g}{tail}_p{k:02d}",
                             ["--case", "b8", "--set-phase", f"{ph:.6f}", "--jitter-us", f"{jit:g}",
                              "--tail-us", f"{a.tail_us:g}", "--tail-p", f"{a.tail_p:g}",
                              "--hold-s", f"{a.hold_s:g}", "--latency-us", f"{a.latency_us:g}",
                              "--seed", str(645 + k), *a.extra]))
    else:
        for hold in a.hold_us:
            for k in range(a.phases):
                lat = a.latency_us + TICK_US * k / a.phases
                runs.append((f"pullin_h{hold:g}_p{k:02d}",
                             ["--case", "pullin", "--peer-ppm", "-5.10", "--hold-us", f"{hold:g}",
                              "--latency-us", f"{lat:.4f}", *a.extra]))
    rows = []
    with cf.ThreadPoolExecutor(max_workers=a.jobs) as pool:
        futs = [pool.submit(run, a.exe, a.out, n, args) for n, args in runs]
        for f in cf.as_completed(futs):
            name, rc, line = f.result()
            rows.append((name, rc, line))
            print(f"{name}: rc {rc}: {line}", flush=True)
    rows.sort()
    table = a.out / f"{a.case}.md"
    with table.open("w") as fh:
        fh.write("| Run | rc | Result |\n|---|---|---|\n")
        for name, rc, line in rows:
            fh.write(f"| {name} | {rc} | {line} |\n")
    print(f"table: {table}")
    return 0 if all(line != "(no RESULT line)" for _, _, line in rows) else 1


if __name__ == "__main__":
    sys.exit(main())
