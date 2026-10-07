#!/usr/bin/env python3
"""Run one foreground command and retain its output and return code."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument("--repo", type=Path, required=True)
parser.add_argument("--name", required=True)
parser.add_argument("--cc")
parser.add_argument("command", nargs=argparse.REMAINDER)
args = parser.parse_args()
packet = Path(__file__).resolve().parent
scratch = packet / "scratch"
scratch.mkdir(exist_ok=True)
command = args.command
if command and command[0] == "--":
    command = command[1:]
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE="1")
if args.cc:
    env["MILAN_RV32_CC"] = args.cc
started = time.monotonic()
with (packet / (args.name + ".log")).open("wb") as output:
    result = subprocess.run(command, cwd=args.repo, env=env, stdout=output,
                            stderr=subprocess.STDOUT, timeout=1800)
(packet / (args.name + ".rc")).write_text(str(result.returncode) + "\n")
(packet / (args.name + ".command.json")).write_text(json.dumps({
    "argv": command, "MILAN_RV32_CC": args.cc,
    "temporary_directory": "scratch/", "elapsed_seconds": round(time.monotonic()-started, 3),
    "returncode": result.returncode}, indent=2) + "\n")
print(args.name + ": rc=" + str(result.returncode), flush=True)
raise SystemExit(result.returncode)
