"""Repeat `--control owner_report` from several trees side by side, under the same load, and keep every result.

usage: python3 -I stress_report.py OUT N JOBS BURNERS NAME=TREE [NAME=TREE ...]

Each tree runs N times, JOBS at once, all trees at the same time, so each sees the same host load.
BURNERS busy loops run beside them for the whole campaign, on this process's own CPUs (they inherit
its affinity); each is ended through its own handle, never by name. Results append to OUT/<name>.jsonl;
the host load is sampled every 5 s to OUT/load.txt.
"""
import concurrent.futures
import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

out, n, jobs, burners = Path(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
trees = dict(arg.split("=", 1) for arg in sys.argv[5:])
out.mkdir(parents=True, exist_ok=True)
env = {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}
env["TMPDIR"] = "$VALIDATION_STORAGE/833-a726j/tmp"
lock = threading.Lock()
done = threading.Event()


def sample() -> None:
    with (out / "load.txt").open("a") as log:
        while not done.wait(5):
            log.write(f"{time.time():.0f} {open('/proc/loadavg').read()}")
            log.flush()


def one(name: str, index: int) -> dict:
    load = open("/proc/loadavg").read().split()[0]
    began = time.monotonic()
    try:
        p = subprocess.run([sys.executable, "-B", "scripts/test_suite_cancellation.py", "--control", "owner_report"],
                           cwd=trees[name], env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                           timeout=120, start_new_session=True)
        rc, text = p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        rc, text = None, "cut at 120 s"
    lines = [line for line in text.splitlines() if line.strip()]
    row = dict(tree=name, i=index, rc=rc, s=round(time.monotonic() - began, 3), load=float(load),
               last=(lines[-1][:400] if lines else ""))
    with lock, (out / f"{name}.jsonl").open("a") as log:
        log.write(json.dumps(row) + "\n")
    return row


busy = [subprocess.Popen([sys.executable, "-c", "while True: pass"]) for _ in range(burners)]
sampler = threading.Thread(target=sample, daemon=True)
sampler.start()
try:
    pools = {name: concurrent.futures.ThreadPoolExecutor(jobs) for name in trees}
    futures = [pools[name].submit(one, name, i) for i in range(n) for name in trees]
    rows = [f.result() for f in futures]
finally:
    done.set()
    for process in busy:
        process.kill()
        process.wait()
for name in trees:
    mine = [r for r in rows if r["tree"] == name]
    red = [r for r in mine if r["rc"] != 0]
    loads = [r["load"] for r in mine]
    print(f"{name}: {len(mine)} runs, {len(red)} red, load at start min {min(loads):.1f} "
          f"mean {sum(loads) / len(loads):.1f} max {max(loads):.1f}", flush=True)
    for r in red:
        print(f"  red {name} #{r['i']} rc {r['rc']}: {r['last'][:300]}", flush=True)
