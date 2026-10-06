#!/usr/bin/env python3
"""Run one foreground check; preserve its exact output and exit status."""
import os
from pathlib import Path
import subprocess
import sys
import time
repo, packet, name, *cmd = sys.argv[1:]
root = Path(packet).resolve()
(root / "scratch/tmp").mkdir(parents=True, exist_ok=True)
env = dict(os.environ, TMPDIR=str(root / "scratch/tmp"),
           PYTHONPYCACHEPREFIX=str(root / "scratch/pycache"))
start = time.monotonic()
with (root / "receipts" / (name + ".log")).open("wb") as log:
    result = subprocess.run(cmd, cwd=repo, env=env, stdout=log,
                            stderr=subprocess.STDOUT, timeout=540)
(root / "receipts" / (name + ".rc")).write_text(str(result.returncode) + "\n")
print(name, "rc=" + str(result.returncode), "seconds=" + str(round(time.monotonic()-start, 3)))
print((root / "receipts" / (name + ".log")).read_text(errors="replace")[-2500:])
sys.exit(result.returncode)
