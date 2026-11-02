#!/usr/bin/env python3
"""usage: killlat.py <out jsonl> <seconds> <workers>  Scratch only. Measures SIGKILL until death directly, through a pidfd, for two kinds of target:
one asleep and one forking, as a make or a shell is. While waiting it samples the target's state and wait channel. No /proc census is involved."""
import json, os, select, signal, subprocess, sys, time
from pathlib import Path
out, seconds, workers = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
IDLE = "import time; print('r', flush=True); time.sleep(600)"
FORKER = """
import os, time
print('r', flush=True)
while True:
    p = os.fork()
    if p == 0:
        os._exit(0)
    os.waitpid(p, 0)
"""
def state(pid):
    try:
        st = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[0]
        w = Path(f"/proc/{pid}/wchan").read_text().strip()
        return st, w
    except OSError:
        return None
def worker(n):
    end = time.monotonic() + seconds
    rows = []
    kinds = ("idle", "forker")
    i = 0
    while time.monotonic() < end:
        kind = kinds[i % 2]; i += 1
        spawn0 = time.monotonic()
        p = subprocess.Popen([sys.executable, "-c", IDLE if kind == "idle" else FORKER], stdout=subprocess.PIPE)
        p.stdout.readline()
        spawn = time.monotonic() - spawn0
        if kind == "forker":
            time.sleep(0.01)
        fd = os.pidfd_open(p.pid)
        poll = select.poll(); poll.register(fd, select.POLLIN)
        t0 = time.monotonic()
        signal.pidfd_send_signal(fd, signal.SIGKILL)
        seen = {}
        while not poll.poll(10):
            s = state(p.pid)
            if s:
                key = f"{s[0]} {s[1]}"
                seen[key] = seen.get(key, 0) + 1
        t1 = time.monotonic()
        os.close(fd); p.wait(); p.stdout.close()
        rows.append(dict(kind=kind, latency=round(t1 - t0, 4), spawn=round(spawn, 3), seen=seen, t=round(t0, 1),
                         load=float(Path("/proc/loadavg").read_text().split()[0])))
        if len(rows) >= 50:
            with open(out, "a") as f:
                for r in rows: f.write(json.dumps(r) + "\n")
            rows = []
    with open(out, "a") as f:
        for r in rows: f.write(json.dumps(r) + "\n")
pids = []
for n in range(workers):
    c = os.fork()
    if c == 0:
        worker(n); os._exit(0)
    pids.append(c)
for c in pids:
    os.waitpid(c, 0)
