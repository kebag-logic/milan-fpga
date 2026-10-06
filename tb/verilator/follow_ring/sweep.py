#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run follow_ring's two campaigns across their phase sweeps, in parallel.

  sweep.py b8     [--jobs N] [--phases K] [--jitter-us J ...] [--hold-s S]
                  [--switch-hold-s S]
  sweep.py pullin [--jobs N] [--phases K] [--hold-us U ...]

b8 (#645, and #647 at each source change): lane B8's INTERNAL-to-AAF set at
K places in one INTERNAL beat (the loopback ring's margin at the set, and the
stream's phase against the grid after the walk, run once round their ranges
across them), at each listed arrival jitter, with an optional rare tail
(--tail-us, --tail-p), then (with --switch-hold-s) AAF to CRF and CRF to AAF.

pullin (#647): one serial-clock hold under a running stream at INTERNAL, with
the stream's arrival latency at K places across one media tick (the feed's
phase against the grid), for each listed hold length.

Every run grades the settle law (sim_main.cpp): one settle recentre per
transient, after 8 LOCKED windows under following; slips before it within the
declared bound; after it no loopback slip, the loopback ring centred and the
render stage on its law. A window #643's ambiguity window cannot grade is
reported, not failed (--allow-ungradable). The executable is
MDIR/Vfollow_ring (make build). Every run's own log lands in OUT/<name>.log
beside the table OUT/<case>.md (its RESULT lines), and the exit status is 0
only when every run completed and passed.
"""

import argparse
import concurrent.futures as cf
import json
import re
import subprocess
import sys
from pathlib import Path

TICK_US = 1e6 / 48000.0


def run(exe: Path, out: Path, name: str, args: list[str]) -> tuple[str, int, list[str]]:
    """One harness run; its exit status and its RESULT lines."""
    log = out / f"{name}.log"
    argv = [str(exe), *args]
    (out / f"{name}.command.json").write_text(json.dumps(argv) + "\n")
    with log.open("w") as fh:
        rc = subprocess.run(argv, stdout=fh, stderr=subprocess.STDOUT, check=False).returncode
    (out / f"{name}.rc").write_text(f"{rc}\n")
    found = re.findall(r"^RESULT-6\d\d(?:-SW)?: .*$", log.read_text(), re.M)
    return name, rc, found


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
    ap.add_argument("--hold-s", type=float, default=50.0)
    ap.add_argument("--switch-hold-s", type=float, default=0.0)
    ap.add_argument("--hold-us", type=float, nargs="+", default=[52.0])
    ap.add_argument("--after-s", type=float, default=2.0)
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
                              "--hold-s", f"{a.hold_s:g}", "--switch-hold-s", f"{a.switch_hold_s:g}",
                              "--latency-us", f"{a.latency_us:g}", "--seed", str(645 + k),
                              "--allow-ungradable", *a.extra]))
    else:
        for hold in a.hold_us:
            for k in range(a.phases):
                lat = a.latency_us + TICK_US * k / a.phases
                runs.append((f"pullin_h{hold:g}_p{k:02d}",
                             ["--case", "pullin", "--peer-ppm", "-5.10", "--hold-us", f"{hold:g}",
                              "--latency-us", f"{lat:.4f}", "--after-s", f"{a.after_s:g}",
                              "--allow-ungradable", *a.extra]))
    rows = []
    with cf.ThreadPoolExecutor(max_workers=a.jobs) as pool:
        futs = [pool.submit(run, a.exe, a.out, n, args) for n, args in runs]
        for f in cf.as_completed(futs):
            name, rc, lines = f.result()
            rows.append((name, rc, lines))
            print(f"{name}: rc {rc}: {lines[0] if lines else '(no RESULT line)'}", flush=True)
    rows.sort()
    table = a.out / f"{a.case}.md"
    with table.open("w") as fh:
        fh.write("| Run | rc | Result |\n|---|---|---|\n")
        for name, rc, lines in rows:
            for line in lines or ["(no RESULT line)"]:
                fh.write(f"| {name} | {rc} | {line} |\n")
    failed = [name for name, rc, lines in rows if rc != 0 or not lines]
    print(f"table: {table}")
    print(f"follow_ring {a.case} campaign: {len(rows) - len(failed)}/{len(rows)} runs passed"
          + (f"; FAILED: {' '.join(failed)}" if failed else ""))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
