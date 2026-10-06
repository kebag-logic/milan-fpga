#!/usr/bin/env python3
"""Run a focused review command synchronously with a log and exit receipt."""
import argparse
import os
from pathlib import Path
import subprocess
import sys
import time

p = argparse.ArgumentParser()
p.add_argument("name")
p.add_argument("--repo", type=Path, required=True)
p.add_argument("command", nargs=argparse.REMAINDER)
a = p.parse_args()
packet = Path(__file__).resolve().parent
scratch = packet / "scratch"
scratch.mkdir(exist_ok=True)
argv = a.command[1:] if a.command[:1] == ["--"] else a.command
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE="1")
start = time.monotonic()
with (packet / f"{a.name}.log").open("w") as out:
    result = subprocess.run(argv, cwd=a.repo, env=env, stdout=out, stderr=subprocess.STDOUT, check=False)
(packet / f"{a.name}.rc").write_text(str(result.returncode) + "\n")
print(f"{a.name}: rc={result.returncode}, seconds={time.monotonic()-start:.1f}", flush=True)
sys.exit(result.returncode)
