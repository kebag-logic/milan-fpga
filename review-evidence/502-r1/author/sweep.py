import os
from pathlib import Path
import subprocess
import sys

os.environ["PATH"] = "/tmp/502-python/bin:" + os.environ["PATH"]
failed = []
for shard in (5, 0, 1, 2, 3, 4):
    cmd = [sys.executable, "/tmp/502-run-gate.py", f"sweep-{shard}",
           "env", "SUITE_TIMEOUT=10800", "scripts/run_all_suites.sh",
           f"$MANAGEMENT/2026-09-23/502-a338/sweep-{shard}",
           "--shard", f"{shard}/6"]
    rc = subprocess.run(cmd, timeout=21600).returncode
    if rc:
        failed.append((shard, rc))
print("SWEEP FAILURES:", failed, flush=True)
sys.exit(bool(failed))
