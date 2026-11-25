#!/usr/bin/env python3
"""Attribute a hosted Verilator job's minutes: runner speed against the change.

For each shard of two runs (base, head), pairs every Verilator build report
("Verilator: Walltime W s (elab=E, cvt=C, bld=B); cpu U s on N threads") in the
same suite log, in order, and reports the ratio head/base of:
  - cvt+elab: Verilator's single-threaded front end on identical input (pure CPU speed);
  - bld: the model's C++ compile, make -j4 on the runner (CPU speed, 4 threads);
against the job's minutes from the Actions jobs API (jobs JSON files given).
A suite whose builds are slower by the same factor as its job ran on a slower runner.

usage: hosted_speed.py BASE_LOGDIR HEAD_LOGDIR BASE_JOBS.json HEAD_JOBS.json
LOGDIR holds suite-logs-<n>/ directories (gh run download -n suite-logs-<n>).
"""
from __future__ import annotations

import json
import re
import statistics
import sys
from datetime import datetime
from pathlib import Path

REPORT = re.compile(r"Verilator: Walltime ([0-9.]+) s \(elab=([0-9.]+), cvt=([0-9.]+), bld=([0-9.]+)\); cpu ([0-9.]+) s on (\d+) threads")


def reports(path: Path) -> list[tuple[float, float, float]]:
    out = []
    for m in REPORT.finditer(path.read_text(errors="replace")):
        _, elab, cvt, bld, _, _ = m.groups()
        out.append((float(elab) + float(cvt), float(bld), 0.0))
    return out


def minutes(jobs_file: Path) -> dict[int, float]:
    data = json.loads(jobs_file.read_text())
    jobs = data["jobs"] if isinstance(data, dict) else data
    out = {}
    for job in jobs:
        m = re.fullmatch(r"Verilator shard (\d+)/19", job["name"])
        if m and job.get("started_at") and job.get("completed_at"):
            t0 = datetime.fromisoformat(job["started_at"].replace("Z", "+00:00"))
            t1 = datetime.fromisoformat(job["completed_at"].replace("Z", "+00:00"))
            out[int(m.group(1))] = (t1 - t0).total_seconds() / 60
    return out


def main() -> int:
    base, head, bjobs, hjobs = (Path(a) for a in sys.argv[1:5])
    bm, hm = minutes(bjobs), minutes(hjobs)
    print(f"{'shard':>5} {'job base':>8} {'job head':>8} {'job h/b':>7} | {'pairs':>5} {'fe h/b':>6} {'bld h/b':>7} | {'fe s b':>7} {'fe s h':>7}")
    rows = []
    for n in range(19):
        bdir, hdir = base / f"suite-logs-{n}", head / f"suite-logs-{n}"
        fe_r, bld_r, fe_b, fe_h, pairs = [], [], 0.0, 0.0, 0
        for blog in sorted(bdir.glob("*.log")):
            hlog = hdir / blog.name
            if not hlog.exists():
                continue
            b, h = reports(blog), reports(hlog)
            for (bf, bb, _), (hf, hb, _) in zip(b, h):
                pairs += 1
                fe_b += bf
                fe_h += hf
                if bf >= 0.05:
                    fe_r.append(hf / bf)
                if bb >= 1.0:
                    bld_r.append(hb / bb)
        fe = statistics.median(fe_r) if fe_r else float("nan")
        bl = statistics.median(bld_r) if bld_r else float("nan")
        jb, jh = bm.get(n, float("nan")), hm.get(n, float("nan"))
        rows.append((n, jb, jh, fe, bl))
        print(f"{n:>5} {jb:8.1f} {jh:8.1f} {jh / jb:7.2f} | {pairs:>5} {fe:6.2f} {bl:7.2f} | {fe_b:7.1f} {fe_h:7.1f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
