#!/usr/bin/env python3
"""Run `make <targets>` in a clone, timestamping every output line.

usage: timed_make.py <clone> <outdir> [make targets...]

Writes <outdir>/make.log (stdout+stderr merged, each line prefixed with the
seconds since start), <outdir>/summary.json (start, end, wall, rc). The
environment is the caller's plus PYTHONUNBUFFERED=1, so the drivers' lines
arrive when printed (no effect on any verdict).
"""
import json, os, subprocess, sys, time
from datetime import datetime

clone, outdir, *targets = sys.argv[1:]
os.makedirs(outdir, exist_ok=True)
env = dict(os.environ, PYTHONUNBUFFERED="1")
meta = {"clone": clone, "targets": targets or ["all"],
        "head": subprocess.run(["git", "-C", clone, "rev-parse", "HEAD"],
                               capture_output=True, text=True).stdout.strip(),
        "affinity": sorted(os.sched_getaffinity(0)),
        "PATH": env.get("PATH"), "VERILATOR_ROOT": env.get("VERILATOR_ROOT"),
        "TMPDIR": env.get("TMPDIR"), "start": datetime.now().isoformat()}
t0 = time.monotonic()
with open(os.path.join(outdir, "make.log"), "w") as log:
    p = subprocess.Popen(["make", *(targets or ["all"])], cwd=clone, env=env,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         text=True, bufsize=1)
    for line in p.stdout:
        log.write(f"{time.monotonic() - t0:10.2f} {line}")
        log.flush()
    rc = p.wait()
meta.update(end=datetime.now().isoformat(), wall_s=round(time.monotonic() - t0, 2), rc=rc)
with open(os.path.join(outdir, "summary.json"), "w") as f:
    json.dump(meta, f, indent=1)
print(json.dumps({k: meta[k] for k in ("head", "wall_s", "rc")}))
sys.exit(rc)
