#!/usr/bin/env python3
"""Item 7 check: one real shipping elaboration graded by the shipping probe.

Usage: run_ship_probe.py <lane> [config] [port]   (default ax7101_1x1_tdm8 e1)
Runs sw/builder/test_shipping_clock_constraints.py in the pins-only
environment (its own HOME, no PYTHONPATH, PYTHONHASHSEED=0), as R382-4's
receipt 07 did, into a fresh output directory that is removed afterwards.
Exits with the probe's own rc and prints the probe's last lines.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

WORK = Path("$VALIDATION_STORAGE/a433")
lane = Path(sys.argv[1])
config = sys.argv[2] if len(sys.argv) > 2 else "ax7101_1x1_tdm8"
port = sys.argv[3] if len(sys.argv) > 3 else "e1"
env = {"PATH": f"{WORK}/pins-venv/bin:{WORK}/tools/bin:/usr/bin:/bin", "HOME": str(WORK / "pins-home"),
       "PYTHONHASHSEED": "0", "PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": str(WORK / "tmp")}
out = Path(tempfile.mkdtemp(prefix="ship-", dir=WORK / "tmp"))
try:
    result = subprocess.run([f"{WORK}/pins-venv/bin/python3", "-B",
                             str(lane / "sw/builder/test_shipping_clock_constraints.py"),
                             "--config", config, "--port", port, "--output-dir", str(out / "build")],
                            cwd=lane / "sw/litex", env=env, text=True, capture_output=True, timeout=900)
finally:
    shutil.rmtree(out, ignore_errors=True)
markers = [line for line in result.stdout.splitlines() if line.startswith("[constraints] shipping ")]
errors = [line for line in (result.stdout + result.stderr).splitlines()
          if "Error" in line or line.startswith("AssertionError")]
print("\n".join(markers + errors[-3:]))
print(f"probe rc={result.returncode}")
sys.exit(result.returncode)
