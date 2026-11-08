#!/usr/bin/env python3
"""Run run_job.py once per line of a batch file (its arguments, space-separated), in order; exit 1 if any failed."""
import subprocess
import sys
from pathlib import Path

DRIVER = Path(__file__).with_name("run_job.py")
bad = 0
for line in Path(sys.argv[1]).read_text().splitlines():
    if line.strip():
        print(f"=== run_job.py {line}", flush=True)
        bad += subprocess.run([sys.executable, str(DRIVER), *line.split()]).returncode != 0
print(f"batch done, {bad} job(s) with a failed step", flush=True)
sys.exit(1 if bad else 0)
