import json
import os
from pathlib import Path
import subprocess
import sys
import time
out = Path(__file__).resolve().parent
label, cwd, *command = sys.argv[1:]
env = os.environ.copy()
env["PATH"] = "$VALIDATION_TOOLS/verilator-v5.050/bin:" + env["PATH"]
env["PYTHONDONTWRITEBYTECODE"] = "1"
if hasattr(os, "sched_getaffinity"):
    os.sched_setaffinity(0, sorted(os.sched_getaffinity(0))[:8])
start = time.monotonic()
print(f"START {label}: {command}", flush=True)
with (out / (label + ".log")).open("w") as stream:
    rc = subprocess.run(command, cwd=cwd, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=14400).returncode
record = dict(label=label, cwd=cwd, command=command, rc=rc, seconds=round(time.monotonic()-start, 2))
(out / (label + ".json")).write_text(json.dumps(record, indent=2)+"\n")
print(json.dumps(record), flush=True)
print("\n".join((out / (label + ".log")).read_text(errors="replace").splitlines()[-12:]), flush=True)
sys.exit(rc)
