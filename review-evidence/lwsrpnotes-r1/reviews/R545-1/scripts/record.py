#!/usr/bin/env python3
"""Run one foreground command and retain its output, status, and duration."""
import argparse, json, os, subprocess, time
from pathlib import Path
parser = argparse.ArgumentParser()
parser.add_argument("--name", required=True)
parser.add_argument("--cwd", type=Path, required=True)
parser.add_argument("command", nargs=argparse.REMAINDER)
a = parser.parse_args()
packet = Path(__file__).resolve().parents[1]
command = a.command[1:] if a.command[:1] == ["--"] else a.command
start = time.monotonic()
with (packet / "receipts" / (a.name + ".log")).open("w") as log:
    result = subprocess.run(command, cwd=a.cwd, stdout=log, stderr=subprocess.STDOUT)
record = {"command": command, "cwd": str(a.cwd), "rc": result.returncode,
          "seconds": round(time.monotonic()-start, 3)}
(packet / "receipts" / (a.name + ".json")).write_text(json.dumps(record, indent=2)+"\n")
(packet / "receipts" / (a.name + ".rc")).write_text(str(result.returncode)+"\n")
print(json.dumps({"stage": a.name, **record}), flush=True)
raise SystemExit(result.returncode)
