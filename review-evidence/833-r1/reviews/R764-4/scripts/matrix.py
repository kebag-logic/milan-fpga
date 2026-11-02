#!/usr/bin/env python3
"""Every mutant directory x every owner control (x REPEATS), each in its own user+PID namespace, 150 s bound.

usage: matrix.py MUTANTS_DIR RECEIPTS_DIR JOBS RUN_CONTROL [REPEATS]
"""
import concurrent.futures, json, subprocess, sys, time
from pathlib import Path
mut, out, jobs, runner = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
repeats = int(sys.argv[5]) if len(sys.argv) > 5 else 1
CONTROLS = ["owner_report", "owner_reparented", "owner_late_exit", "owner_stall",
            "owner_shell_window", "owner_survivor", "owner_vanishing", "owner_late_cancel"]
NS = ["unshare", "--user", "--map-current-user", "--pid", "--fork", "--kill-child", "--mount-proc"]


def one(job):
    m, c, k = job
    (out / m).mkdir(parents=True, exist_ok=True)
    log = out / m / f"{c}.{k}.log"
    began = time.monotonic()
    with log.open("w") as s:
        rc = subprocess.run(["timeout", "-k", "5", "150", *NS, sys.executable, "-I", "-B", runner, str(mut / m), c],
                            stdout=s, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL).returncode
    (out / m / f"{c}.{k}.rc").write_text(f"{rc}\n")
    last = [l for l in log.read_text(errors="replace").splitlines() if l.strip()]
    return dict(mutant=m, control=c, run=k, rc=rc, seconds=round(time.monotonic() - began, 1),
                last=(last[-1] if last else "")[:300])


jobsl = [(m.name, c, k) for m in sorted(mut.iterdir()) for c in CONTROLS for k in range(repeats)]
with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
    rows = list(pool.map(one, jobsl))
(out / "matrix.json").write_text(json.dumps(rows, indent=1) + "\n")
names = sorted({r["mutant"] for r in rows})
print("| mutant | " + " | ".join(c.replace("owner_", "") for c in CONTROLS) + " | red |")
print("|---" * (len(CONTROLS) + 2) + "|")
for n in names:
    cells = []
    for c in CONTROLS:
        rs = [r for r in rows if r["mutant"] == n and r["control"] == c]
        red = sum(r["rc"] != 0 for r in rs)
        cells.append("ok" if red == 0 else (f"RED({red}/{len(rs)})" if len(rs) > 1 else f"RED({rs[0]['rc']})"))
    print(f"| {n} | " + " | ".join(cells) + f" | {sum(c != 'ok' for c in cells)} |")
print()
for r in rows:
    if r["rc"] != 0:
        print(f"- {r['mutant']} / {r['control']} #{r['run']} ({r['seconds']} s): {r['last']}")
