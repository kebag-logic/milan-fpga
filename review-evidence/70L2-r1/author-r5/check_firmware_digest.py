#!/usr/bin/env python3
"""Show the product firmware is byte-identical to the reviewed heads.

usage: check_firmware_digest.py <repo>
Exit 0 when sw/firmware has no difference from 597dba85 (round 1, the capture
receipt's head), 943a3dac (round 2), 0a80abcb (round 3) or 5b4a47e9 (round 4),
and the committed
milan_baremetal.c digest equals 597dba85's and the capture receipt's
product_firmware_sha256 (tb/verilator/nvm_capture_cpu/measurements.json).
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
ROUND1 = "597dba8593553ad85b1e94936b016907c4d2003a"
REVIEWED = (ROUND1, "943a3dac973abc7130fe1a19bb6f5943788a01fe",
            "0a80abcb3a09f8f6236379d7b2ed91fc4cc478d4",
            "5b4a47e99f5a453832ccabccfbf4aae116d6fea0")
FW = "sw/firmware/milan_baremetal/milan_baremetal.c"


def git(*args: str) -> bytes:
    """stdout of one git command in `repo`."""
    return subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True).stdout


head = git("rev-parse", "HEAD").decode().strip()
for rev in REVIEWED:
    changed = git("diff", "--name-only", rev, "HEAD", "--", "sw/firmware").decode().split()
    assert not changed, f"firmware files changed since {rev}: {changed}"
now = hashlib.sha256(git("show", f"HEAD:{FW}")).hexdigest()
then = hashlib.sha256(git("show", f"{ROUND1}:{FW}")).hexdigest()
receipt = json.loads(git("show", "HEAD:tb/verilator/nvm_capture_cpu/measurements.json"))
assert now == then == receipt["product_firmware_sha256"], (now, then, receipt["product_firmware_sha256"])
print(f"head {head}: sw/firmware unchanged since {', '.join(rev[:8] for rev in REVIEWED)}; "
      f"{FW} sha256 {now} = round-1 head = capture receipt product_firmware_sha256")
