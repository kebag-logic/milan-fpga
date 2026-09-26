#!/usr/bin/env python3
"""Run one foreground gate, preserving its output and exact return code."""
import json
import subprocess
import sys
import time
from pathlib import Path

out = Path(__file__).resolve().parent
label, *command = sys.argv[1:]
start = time.monotonic()
log = out / (label + ".log")
with log.open("w") as stream:
    stream.write("Command: " + " ".join(command) + "\n")
    stream.flush()
    result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT,
                            timeout=7200)
    elapsed = time.monotonic() - start
    stream.write(f"\nReturn code: {result.returncode}\nElapsed: {elapsed:.2f}s\n")
record = {"command": command, "returncode": result.returncode,
          "seconds": round(elapsed, 2), "log": log.name}
(out / (label + ".json")).write_text(json.dumps(record, indent=2) + "\n")
print("\n".join(log.read_text().splitlines()[-45:]))
sys.exit(result.returncode)
