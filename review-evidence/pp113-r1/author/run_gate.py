import json
import os
from pathlib import Path
import subprocess
import sys
import time

output = Path(__file__).resolve().parent
label, cwd, *command = sys.argv[1:]
env = os.environ.copy()
env["PATH"] = "$VALIDATION_TOOLS/verilator-v5.050/bin:" + env["PATH"]
if hasattr(os, "sched_setaffinity"):
    os.sched_setaffinity(0, sorted(os.sched_getaffinity(0))[:8])
start = time.time()
with (output / (label + ".log")).open("w") as stream:
    result = subprocess.run(command, cwd=cwd, env=env, stdout=stream,
                            stderr=subprocess.STDOUT, timeout=14400, check=False)
record = {"label": label, "cwd": cwd, "command": command, "rc": result.returncode,
          "seconds": round(time.time() - start, 2)}
(output / (label + ".json")).write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record), flush=True)
sys.exit(result.returncode)
