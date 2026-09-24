"""Run a foreground gate with a three-hour deadline and direct log files."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

out = Path(__file__).resolve().parent
label, cwd, *command = sys.argv[1:]
env = dict(os.environ)
env["PATH"] = "$VALIDATION_TOOLS/verilator-v5.050/bin:" + env["PATH"]
env["TSAGEN_DIR"] = "$WORKSPACE_HOME/prjs/tsn-gen"
env["PYTHONUNBUFFERED"] = "1"
env["VERILATOR_JOBS"] = "8"
if label in ("before-mutants", "after-mutants"):
    env["PYTHONPATH"] = str(out / "observer")
    env["A281_MUTANT_RECEIPTS"] = str(out / label)
start = time.monotonic()
print("RUN", label, command, flush=True)
with (out / (label + ".stdout.log")).open("w") as stdout, (out / (label + ".stderr.log")).open("w") as stderr:
    result = subprocess.run(command, cwd=cwd, env=env, stdout=stdout, stderr=stderr, timeout=10800)
receipt = {"command": command, "cwd": cwd, "returncode": result.returncode, "elapsed_seconds": round(time.monotonic() - start, 3)}
(out / (label + ".receipt.json")).write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt), flush=True)
for suffix in ("stdout", "stderr"):
    lines = (out / (label + "." + suffix + ".log")).read_text().splitlines()
    print("\n".join(lines[-12:]), flush=True)
sys.exit(result.returncode)
