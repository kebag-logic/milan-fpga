"""Finish firmware-unit steps 5 to 7 with the caller's disk scratch and worker cap."""
import subprocess
import sys
import time
from pathlib import Path

root = Path(sys.argv[1])
logs = Path(sys.argv[2])
steps = [
    ["sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py", "--require-rv32", "--jobs", "4"],
    ["sw/firmware/gtest/fw_coverage.py", "--selftest"],
    ["sw/firmware/gtest/fw_coverage.py", "--check", "--jobs", "4"],
]
for number, args in enumerate(steps, 5):
    begin = time.monotonic()
    with (logs / f"{number:02d}.log").open("w") as log:
        result = subprocess.run([sys.executable, *args], cwd=root, stdout=log, stderr=subprocess.STDOUT)
    print(f"step={number} rc={result.returncode} elapsed={time.monotonic() - begin:.2f} python3 " + " ".join(args), flush=True)
    if result.returncode:
        raise SystemExit(result.returncode)
