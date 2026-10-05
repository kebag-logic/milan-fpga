#!/usr/bin/env python3
"""Run independent focused gates concurrently, retaining their raw receipts."""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys
repo = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
scratch = out / "scratch"
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE="1")
jobs = {
    "store-suite": ["python3", "sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py", "--require-rv32", "--self-test"],
    "shipping-suite": ["python3", "sw/firmware/nvm_hosttest/test_nvm_firmware.py", "--self-test"],
    "capture-receipt": ["python3", "scripts/check_nvm_capture.py"],
}
def run(item):
    name, cmd = item
    with (out / (name + ".log")).open("w") as log:
        log.write("COMMAND " + " ".join(cmd) + "\n")
        log.flush()
        r = subprocess.run(cmd, cwd=repo, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=540, check=False)
    (out / (name + ".rc")).write_text(str(r.returncode) + "\n")
    return name, r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(run, jobs.items()))
for name, rc in results:
    print(name, "rc", rc)
sys.exit(int(any(rc for _, rc in results)))
