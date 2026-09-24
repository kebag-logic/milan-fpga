#!/usr/bin/env python3
"""Run one foreground gate, recording its command, output and true return code."""
import json
from pathlib import Path
import subprocess
import sys
import time

out = Path(__file__).resolve().parent
name, cwd, *cmd = sys.argv[1:]
log = out / f"{name}.log"
start = time.time()
print(f"START {name}: {cmd} (cwd={cwd}, timeout=7200s)", flush=True)
with log.open("w") as stream:
    try:
        result = subprocess.run(cmd, cwd=cwd, stdout=stream, stderr=subprocess.STDOUT, timeout=7200)
        rc = result.returncode
    except subprocess.TimeoutExpired:
        rc = 124
        stream.write("\nGATE TIMEOUT after 7200 seconds\n")
record = {"name": name, "cwd": cwd, "cmd": cmd, "rc": rc,
          "seconds": round(time.time() - start, 3), "log": str(log)}
with (out / "gates.jsonl").open("a") as stream:
    stream.write(json.dumps(record) + "\n")
print(json.dumps(record), flush=True)
print("\n".join(log.read_text(errors="replace").splitlines()[-25:]), flush=True)
raise SystemExit(rc)
