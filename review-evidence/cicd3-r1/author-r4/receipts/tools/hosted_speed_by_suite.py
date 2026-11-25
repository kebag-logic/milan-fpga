#!/usr/bin/env python3
"""Runner speed per hosted job of a NEW run, from the same suites' Verilator builds in a REFERENCE run.

usage: hosted_speed_by_suite.py REF_LOGDIR NEW_LOGDIR NEW_JOBS.json NEW_JOBLOGDIR
For each suite log in both runs (wherever each dealer put it), pairs its Verilator build reports in
order; a job's speed index is the median build-wall ratio new/ref over the suites it ran (builds of at
least 1 s). Prints per new job: minutes (jobs API), its suites' windows (tree's measure_log over the job
log), the index and its pair count.
"""
import json
import re
import statistics
import sys
from datetime import datetime
from pathlib import Path

REPORT = re.compile(r"Verilator: Walltime ([0-9.]+) s \(elab=[0-9.]+, cvt=[0-9.]+, bld=([0-9.]+)\)")
sys.path.insert(0, "/data-2/milan/lanes/cicd-1/scripts")
import suite_shards as s  # noqa: E402


def logs(root: Path) -> dict[str, tuple[str, Path]]:
    return {log.stem: (log.parent.name, log) for log in root.glob("suite-logs-*/*.log")}


def builds(path: Path) -> list[float]:
    return [float(m.group(1)) for m in REPORT.finditer(path.read_text(errors="replace"))]


ref, new = logs(Path(sys.argv[1])), logs(Path(sys.argv[2]))
jobs = json.loads(Path(sys.argv[3]).read_text())["jobs"]
ratio = {}
for suite in set(ref) & set(new):
    pairs = [(b, n) for b, n in zip(builds(ref[suite][1]), builds(new[suite][1])) if b >= 1.0]
    if pairs:
        ratio[suite] = [n / b for b, n in pairs]
print(f"{'job':>4} {'min':>5} {'index':>6} {'pairs':>5}  suites (window s)")
for job in sorted(jobs, key=lambda j: j["name"]):
    m = re.fullmatch(r"Verilator shard (\d+)/19", job["name"])
    if not m:
        continue
    n = int(m.group(1))
    minutes = (datetime.fromisoformat(job["completed_at"].replace("Z", "+00:00"))
               - datetime.fromisoformat(job["started_at"].replace("Z", "+00:00"))).total_seconds() / 60
    t = s.measure_log((Path(sys.argv[4]) / f"{n}.log").read_text(encoding="utf-8"))
    mine = [r for suite in t.seconds for r in ratio.get(suite, [])]
    index = statistics.median(mine) if mine else float("nan")
    big = ", ".join(f"{k} {v}" for k, v in sorted(t.seconds.items(), key=lambda kv: -kv[1]) if v >= 60)
    print(f"{n:>4} {minutes:5.1f} {index:6.2f} {len(mine):>5}  {big}")
