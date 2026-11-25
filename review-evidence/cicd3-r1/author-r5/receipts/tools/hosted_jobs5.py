#!/usr/bin/env python3
"""hosted_jobs5.py JOBS.json [MEASURE.txt LANE_ROOT]: every job's minutes from the Actions jobs API
(completed_at - started_at), and for each Verilator worker the minutes of its cold "Build Verilator from source on
cache miss" step and the minutes without it. With a `suite_shards.py --measure` output of the run's worker logs and
the lane at the run's head, also each worker's projection against its measured windows and each new piece's window
against its figure.
"""
import json
import math
import re
import sys
from datetime import datetime
from pathlib import Path


def span(a, b):
    if not a or not b:
        return float("nan")
    t0 = datetime.fromisoformat(a.replace("Z", "+00:00"))
    t1 = datetime.fromisoformat(b.replace("Z", "+00:00"))
    return (t1 - t0).total_seconds() / 60


jobs = json.loads(Path(sys.argv[1]).read_text())["jobs"]
rows, total, billed = [], 0.0, 0
for job in jobs:
    # A job cancelled while queued has no runner and no steps: its started_at is its queue time, so it never ran.
    ran = bool(job.get("runner_name")) or any(s.get("started_at") for s in job.get("steps", []))
    minutes = span(job.get("started_at"), job.get("completed_at")) if ran else 0.0
    if not ran:
        job = {**job, "conclusion": f"{job.get('conclusion')}, never ran"}
    cold = sum(span(s.get("started_at"), s.get("completed_at")) for s in job.get("steps", [])
               if s["name"].startswith("Build Verilator from source") and s.get("conclusion") == "success")
    rows.append((job["name"], job.get("conclusion"), minutes, cold))
    if job.get("conclusion") not in ("skipped", None) and minutes == minutes and minutes > 0:
        total += minutes
        billed += math.ceil(minutes)


def key(row):
    m = re.match(r"(.*?)(\d+)/(\d+)$", row[0])
    return (m[1], int(m[2])) if m else (row[0], 0)


print(f"{'job':40} {'result':9} {'minutes':>7} {'cold build':>10} {'without':>7}")
for name, result, minutes, cold in sorted(rows, key=key):
    print(f"{name:40} {str(result):9} {minutes:7.1f} {cold:10.1f} {minutes - cold:7.1f}")
watch = [m for n, _, m, _ in rows if n.startswith("Fail fast")]
print(f"\nall jobs: {total:.1f} job-minutes ({billed} rounded up per job), of which the fail-fast watcher "
      f"{sum(watch):.1f}")
ver = [(n, m, c) for n, r, m, c in rows if n.startswith("Verilator shard")]
print(f"Verilator workers: {len(ver)}, {sum(m for _, m, _ in ver):.1f} job-minutes, of which cold Verilator builds "
      f"{sum(c for _, _, c in ver):.1f}; slowest {max(m for _, m, _ in ver):.1f} min, slowest without the cold "
      f"build {max(m - c for _, m, c in ver):.1f} min")
over = [(n, m, c) for n, m, c in ver if m > 30]
print("over 30 minutes:", over or "none")

if len(sys.argv) > 3:
    windows = {m[1]: int(m[2]) for line in open(sys.argv[2]) if (m := re.match(r'\s+"(\S+)": (\d+),', line))}
    overhead = None
    for line in open(sys.argv[2]):
        if line.startswith("WORKER_OVERHEAD_SECONDS = ("):
            overhead = [int(x) for x in line.split("(")[1].rstrip(")\n").split(",")]
    sys.path.insert(0, str(Path(sys.argv[3]) / "scripts"))
    import suite_shards as s
    suites = s.expand_suites(s.sweep_suites(Path(sys.argv[3]) / "tb" / "verilator"))
    owners, load = s.balance(suites, len(s.WORKER_OVERHEAD_SECONDS))
    print(f"\n{'w':>2} {'proj':>5} {'meas':>5} {'m/p':>5}  suites (figure -> window)")
    for w, value in enumerate(load):
        mine = [x for x in suites if owners[x] == w]
        measured = (overhead[w] if overhead else 0) + sum(windows.get(x, 0) for x in mine)
        detail = "; ".join(f"{x} {s.SUITE_SECONDS[x]}->{windows.get(x, '?')}" for x in mine
                           if s.SUITE_SECONDS[x] >= 100)
        print(f"{w:2} {value:5} {measured:5} {measured / value:5.2f}  ovh 122->{overhead[w] if overhead else '?'}; "
              f"{detail}")
    new = [x for x in suites if x.split("__")[0] in ("milan_dp", "capture_coherence", "follow_ring", "media_phase")
           and "__" in x]
    print("\nnew pieces: figure -> first hosted window")
    for x in new:
        flag = "OVER" if windows.get(x, 0) > s.SUITE_SECONDS[x] else ""
        print(f"  {x:22} {s.SUITE_SECONDS[x]:5} -> {windows.get(x, '?'):>5} {flag}")
