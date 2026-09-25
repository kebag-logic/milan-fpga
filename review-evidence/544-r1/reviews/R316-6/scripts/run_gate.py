#!/usr/bin/env python3
"""Run one foreground command and preserve its complete output and status."""
import argparse
import os
from pathlib import Path
import subprocess
import time

p = argparse.ArgumentParser()
p.add_argument("--root", type=Path, required=True)
p.add_argument("--packet", type=Path, required=True)
p.add_argument("--name", required=True)
p.add_argument("--timeout", type=int, default=1200)
p.add_argument("command", nargs=argparse.REMAINDER)
a = p.parse_args()
cmd = a.command[1:] if a.command[:1] == ["--"] else a.command
env = dict(os.environ, TMPDIR=str(a.packet / "scratch"),
           PYTHONDONTWRITEBYTECODE="1", GIT_NO_REPLACE_OBJECTS="1")
start = time.monotonic()
log = a.packet / "receipts" / (a.name + ".log")
with log.open("w") as out:
    out.write("command: " + repr(cmd) + "\n")
    out.flush()
    try:
        r = subprocess.run(cmd, cwd=a.root, env=env, stdout=out,
                           stderr=subprocess.STDOUT, timeout=a.timeout)
        code = r.returncode
    except subprocess.TimeoutExpired:
        code = 124
        out.write("TIMEOUT\n")
    out.write(f"\nEXIT_STATUS={code}\nELAPSED_SECONDS={time.monotonic()-start:.3f}\n")
print(f"{a.name}: exit {code}; receipt {log.name}")
print("\n".join(log.read_text().splitlines()[-8:]))
raise SystemExit(code)
