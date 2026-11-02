#!/usr/bin/env python3
"""Reviewer matrix: every mutant directory x every owner control, each in its own
user+PID namespace with a 150 s bound.

usage: matrix.py MUTANTS_DIR RECEIPTS_DIR JOBS RUN_CONTROL
"""
import concurrent.futures, json, subprocess, sys, time
from pathlib import Path
mut, out, jobs, runner = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
CONTROLS = ["owner_report", "owner_reparented", "owner_late_exit", "owner_stall",
            "owner_shell_window", "owner_survivor", "owner_vanishing", "owner_late_cancel"]
NS = ["unshare", "--user", "--map-current-user", "--pid", "--fork", "--kill-child", "--mount-proc"]


def one(job):
    m, c = job
    (out / m).mkdir(parents=True, exist_ok=True)
    log = out / m / f"{c}.log"
    began = time.monotonic()
    with log.open("w") as s:
        rc = subprocess.run(["timeout", "-k", "5", "150", *NS, sys.executable, "-I", "-B", runner, str(mut / m), c],
                            stdout=s, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL).returncode
    (out / m / f"{c}.rc").write_text(f"{rc}\n")
    last = [l for l in log.read_text(errors="replace").splitlines() if l.strip()]
    return dict(mutant=m, control=c, rc=rc, seconds=round(time.monotonic() - began, 1), last=(last[-1] if last else "")[:300])


rows = []
with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
    for row in pool.map(one, [(m.name, c) for m in sorted(mut.iterdir()) for c in CONTROLS]):
        rows.append(row)
(out / "matrix.json").write_text(json.dumps(rows, indent=1) + "\n")
names = sorted({r["mutant"] for r in rows})
print("| mutant | " + " | ".join(c.replace("owner_", "") for c in CONTROLS) + " | red |")
print("|---" * (len(CONTROLS) + 2) + "|")
for n in names:
    cells = [next(r for r in rows if r["mutant"] == n and r["control"] == c) for c in CONTROLS]
    print(f"| {n} | " + " | ".join("ok" if r["rc"] == 0 else f"RED({r['rc']})" for r in cells)
          + f" | {sum(r['rc'] != 0 for r in cells)} |")
print()
for r in rows:
    if r["rc"] != 0:
        print(f"- {r['mutant']} / {r['control']} ({r['seconds']} s): {r['last']}")
