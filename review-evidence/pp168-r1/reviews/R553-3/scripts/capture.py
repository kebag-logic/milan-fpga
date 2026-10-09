#!/usr/bin/env python3
"""Run one foreground command and preserve its unfiltered output and exit status.
Usage: capture.py PACKET LABEL CWD COMMAND [ARG ...]
"""
import json, os, subprocess, sys, time
from pathlib import Path
packet, label, cwd, *command = sys.argv[1:]
r = Path(packet) / "receipts"
r.mkdir(parents=True, exist_ok=True)
started = time.time()
with (r / (label + ".log")).open("wb") as log:
    result = subprocess.run(command, cwd=cwd, stdout=log, stderr=subprocess.STDOUT)
(r / (label + ".rc")).write_text(str(result.returncode) + "\n")
(r / (label + ".json")).write_text(json.dumps({"command": command, "cwd": cwd,
    "start_epoch": started, "end_epoch": time.time(), "returncode": result.returncode}, indent=2) + "\n")
print((r / (label + ".log")).read_text(errors="replace"))
print(label + " rc=" + str(result.returncode))
sys.exit(result.returncode)
