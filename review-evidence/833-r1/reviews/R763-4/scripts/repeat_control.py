#!/usr/bin/env python3
"""Repeat one owner control on several scripts directories, each run in its own
user+PID namespace with a 150 s bound, JOBS at a time.

usage: repeat_control.py RUN_CONTROL CONTROL REPEATS JOBS OUT_DIR SCRIPTS_DIR [SCRIPTS_DIR ...]
Writes OUT_DIR/<dir name>/<n>.log and .rc, then prints one summary line per directory.
"""
import concurrent.futures, subprocess, sys, time
from pathlib import Path
runner, control, repeats, jobs, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5])
dirs = [Path(d) for d in sys.argv[6:]]
NS = ["unshare", "--user", "--map-current-user", "--pid", "--fork", "--kill-child", "--mount-proc"]


def one(job):
    d, n = job
    (out / d.name).mkdir(parents=True, exist_ok=True)
    log = out / d.name / f"{n}.log"
    began = time.monotonic()
    with log.open("w") as s:
        rc = subprocess.run(["timeout", "-k", "5", "150", *NS, sys.executable, "-I", "-B", runner, str(d), control],
                            stdout=s, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL).returncode
    (out / d.name / f"{n}.rc").write_text(f"{rc}\n")
    return d.name, rc, round(time.monotonic() - began, 1)


jobs_list = [(d, n) for n in range(repeats) for d in dirs]
with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
    rows = list(pool.map(one, jobs_list))
for d in dirs:
    mine = [r for r in rows if r[0] == d.name]
    red = sum(r[1] != 0 for r in mine)
    print(f"{d.name} {control}: {len(mine)} runs, {red} red, {len(mine) - red} green, "
          f"seconds {min(r[2] for r in mine)}-{max(r[2] for r in mine)}")
