#!/usr/bin/env python3
"""Repeat one owner control N times per mutant, each in its own user+PID namespace; print red counts and times.

usage: repeat_control.py MUTANTS_DIR RECEIPTS_DIR JOBS RUN_CONTROL CONTROL N MUTANT...
"""
import concurrent.futures, json, subprocess, sys, time
from pathlib import Path
mut, out, jobs, runner, control, n = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5], int(sys.argv[6])
NS = ["unshare", "--user", "--map-current-user", "--pid", "--fork", "--kill-child", "--mount-proc"]


def one(job):
    m, k = job
    (out / m).mkdir(parents=True, exist_ok=True)
    log = out / m / f"{control}.{k}.log"
    began = time.monotonic()
    with log.open("w") as s:
        rc = subprocess.run(["timeout", "-k", "5", "150", *NS, sys.executable, "-I", "-B", runner, str(mut / m), control],
                            stdout=s, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL).returncode
    last = [l for l in log.read_text(errors="replace").splitlines() if l.strip()]
    return dict(mutant=m, run=k, rc=rc, seconds=round(time.monotonic() - began, 1), last=(last[-1] if last else "")[:200])


with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
    rows = list(pool.map(one, [(m, k) for m in sys.argv[7:] for k in range(n)]))
(out / "repeat.json").write_text(json.dumps(rows, indent=1) + "\n")
for m in sys.argv[7:]:
    rs = [r for r in rows if r["mutant"] == m]
    t = sorted(r["seconds"] for r in rs)
    print(f"{m}: red {sum(r['rc'] != 0 for r in rs)}/{len(rs)}, seconds min {t[0]} max {t[-1]}, words {sorted({r['last'] for r in rs if r['rc'] != 0})}")
