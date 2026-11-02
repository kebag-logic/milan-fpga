#!/usr/bin/env python3
"""usage: watch.py <cgroup name> <out> <seconds>  Scratch only. Samples every owner (python running owned_process.py or focus.py)
in that unit each 50 ms: state, wchan, schedstat. Logs any sample in D, any 50 ms window with over 40 ms of run-queue wait,
and any gap in this watcher itself over 200 ms. Also records CPU steal for this unit's CPUs at the end."""
import json, os, sys, time
from pathlib import Path
unit, out, seconds = sys.argv[1], sys.argv[2], float(sys.argv[3])
cg = Path(f"/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/{unit}.service/cgroup.procs")
def steal():
    rows = {}
    for line in Path("/proc/stat").read_text().splitlines():
        f = line.split()
        if f[0].startswith("cpu") and f[0] != "cpu" and 16 <= int(f[0][3:]) <= 31:
            rows[f[0]] = (int(f[8]), sum(map(int, f[1:9])))
    return rows
s0 = steal(); start = time.monotonic(); last = {}; prev = start; n = 0
with open(out, "a") as f:
    while time.monotonic() - start < seconds:
        now = time.monotonic()
        if now - prev > 0.2:
            f.write(json.dumps(dict(t=round(now - start, 2), watcher_gap=round(now - prev, 3))) + "\n")
        prev = now
        try:
            pids = cg.read_text().split()
        except OSError:
            pids = []
        for p in pids:
            try:
                cmd = Path(f"/proc/{p}/cmdline").read_bytes()
                if b"owned_process.py" not in cmd and b"focus.py" not in cmd:
                    continue
                st = Path(f"/proc/{p}/stat").read_text().rsplit(")", 1)[1].split()[0]
                wchan = Path(f"/proc/{p}/wchan").read_text().strip()
                cpu, rq, _slices = map(int, Path(f"/proc/{p}/schedstat").read_text().split())
            except OSError:
                continue
            old = last.get(p)
            last[p] = (now, cpu, rq)
            if st == "D" or (old and rq - old[2] > 40_000_000):
                f.write(json.dumps(dict(t=round(now - start, 2), pid=p, state=st, wchan=wchan, cmd=cmd[:60].decode(errors="replace").replace("\0", " "),
                                        rq_ms=None if not old else round((rq - old[2]) / 1e6, 1), cpu_ms=None if not old else round((cpu - old[1]) / 1e6, 1),
                                        dt_ms=None if not old else round((now - old[0]) * 1e3, 1))) + "\n")
                f.flush()
        n += 1
        time.sleep(0.05)
    s1 = steal()
    f.write(json.dumps(dict(samples=n, steal_pct={k: round(100 * (s1[k][0] - s0[k][0]) / max(1, s1[k][1] - s0[k][1]), 2) for k in s0})) + "\n")
