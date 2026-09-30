#!/usr/bin/env python3
"""Show the product firmware is byte-identical to the reviewed head.

usage: check_firmware_digest.py <repo>
Exit 0 when sw/firmware has no difference from 597dba85 or 943a3dac, and the committed
milan_baremetal.c digest equals both 597dba85's and the capture receipt's
product_firmware_sha256 (tb/verilator/nvm_capture_cpu/measurements.json).
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
BASE = "597dba8593553ad85b1e94936b016907c4d2003a"
ROUND2 = "943a3dac973abc7130fe1a19bb6f5943788a01fe"
FW = "sw/firmware/milan_baremetal/milan_baremetal.c"


def git(*args):
    return subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True).stdout


head = git("rev-parse", "HEAD").decode().strip()
changed = git("diff", "--name-only", BASE, "HEAD", "--", "sw/firmware").decode().split()
assert not changed, f"firmware files changed since {BASE}: {changed}"
assert not git("diff", "--name-only", ROUND2, "HEAD", "--", "sw/firmware").decode().split()
now = hashlib.sha256(git("show", f"HEAD:{FW}")).hexdigest()
then = hashlib.sha256(git("show", f"{BASE}:{FW}")).hexdigest()
assert then == hashlib.sha256(git("show", f"{ROUND2}:{FW}")).hexdigest()
receipt = json.loads(git("show", "HEAD:tb/verilator/nvm_capture_cpu/measurements.json"))
assert now == then == receipt["product_firmware_sha256"], (now, then, receipt["product_firmware_sha256"])
print(f"head {head}: sw/firmware unchanged since {BASE[:8]} and {ROUND2[:8]}; {FW} sha256 {now} "
      "= reviewed head = capture receipt product_firmware_sha256")
