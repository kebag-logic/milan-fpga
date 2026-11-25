#!/usr/bin/env python3
"""Runner speed index per hosted Verilator job, whatever suites or legs each job ran.

usage: python3 -I speed_index5.py REF_DIR NEW_DIR NEW_JOBS.json
Each DIR holds suite-logs-<n>/ (gh run download -n suite-logs-<n>).

A model is identified by its Verilator report's "Built from ... C++ files" line (sources, modules, output size and
file count). For every model built in both runs, the C++ build wall (bld=) of the new run over the reference run's
median for that model is one ratio; a job's index is the median of its ratios, so 1.41 means that job's runner
built the same models 1.41 times as slowly as the reference run did. Prints each job's minutes (jobs API,
completed_at - started_at), index and pair count, slowest first.
"""
import json
import re
import statistics
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

BUILT = re.compile(r"Verilator: Built from (.+? C\+\+ files)")
WALL = re.compile(r"Verilator: Walltime [0-9.]+ s \(elab=[0-9.]+, cvt=[0-9.]+, bld=([0-9.]+)\)")


def builds(log: Path):
    key = None
    for line in log.read_text(errors="replace").splitlines():
        if (m := BUILT.search(line)):
            key = m[1]
        elif key and (m := WALL.search(line)):
            yield key, float(m[1])
            key = None


def per_job(root: Path):
    out = defaultdict(list)
    for shard in root.glob("suite-logs-*"):
        n = int(shard.name.rsplit("-", 1)[1])
        for log in shard.glob("*.log"):
            out[n].extend(builds(log))
    return out


def minutes(path: Path):
    data = json.loads(path.read_text())
    out = {}
    for job in data["jobs"] if isinstance(data, dict) else data:
        m = re.fullmatch(r"Verilator shard (\d+)/(\d+)", job["name"])
        if m and job.get("started_at") and job.get("completed_at"):
            t0 = datetime.fromisoformat(job["started_at"].replace("Z", "+00:00"))
            t1 = datetime.fromisoformat(job["completed_at"].replace("Z", "+00:00"))
            out[int(m[1])] = (t1 - t0).total_seconds() / 60
    return out


def main() -> int:
    ref, new, jobs = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    reference = defaultdict(list)
    for rows in per_job(ref).values():
        for key, bld in rows:
            reference[key].append(bld)
    medians = {key: statistics.median(v) for key, v in reference.items()}
    mins = minutes(jobs)
    rows = []
    for n, items in per_job(new).items():
        ratios = [bld / medians[key] for key, bld in items if key in medians and medians[key] > 1.0]
        index = statistics.median(ratios) if ratios else float("nan")
        rows.append((mins.get(n, float("nan")), n, index, len(ratios)))
    print(f"reference {ref}: {len(medians)} models; new {new}")
    print(f"{'job':>4} {'minutes':>7} {'index':>6} {'pairs':>5}")
    for m, n, index, pairs in sorted(rows, reverse=True):
        print(f"{n:4} {m:7.1f} {index:6.2f} {pairs:5}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
