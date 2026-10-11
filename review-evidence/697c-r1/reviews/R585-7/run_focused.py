#!/usr/bin/env python3
"""Concurrent foreground checks; all disposable output stays in scratch."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ap = argparse.ArgumentParser()
ap.add_argument("checkout", type=Path)
ap.add_argument("packet", type=Path)
a = ap.parse_args()
root, packet = a.checkout.resolve(), a.packet.resolve()
scratch = packet / "scratch"
scratch.mkdir(parents=True, exist_ok=True)
env = {**os.environ, "TMPDIR": str(scratch), "PYTHONDONTWRITEBYTECODE": "1"}
jobs = {
    "ctrl-suite": [sys.executable, "-B", "sw/firmware/ctrl/test/test_ctrl_firmware.py",
                   "--require-rv32", "--jobs", "4", "--build-dir", str(scratch / "ctrl")],
    "coverage": [sys.executable, "-B", "sw/firmware/gtest/fw_coverage.py", "--check", "--jobs", "4",
                 "--keep", str(scratch / "coverage")],
    "stack-boundary": [sys.executable, "-B", "third_party/tsn-c-stack/scripts/check_boundary.py",
                       "--selftest", "--jobs", "4", "--work", str(scratch / "stack-boundary")],
    "pin-probe": [sys.executable, "-B", str(packet / "pin_probe.py"), str(root), str(scratch)],
}

def one(item):
    name, cmd = item
    start = time.monotonic()
    with (scratch / (name + ".raw.log")).open("w") as log:
        rc = subprocess.run(cmd, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT,
                            check=False).returncode
    (packet / (name + ".rc")).write_text(str(rc) + "\n")
    raw = (scratch / (name + ".raw.log")).read_text(errors="replace")
    # Public receipt normalizes only local path prefixes. Originals stay in scratch.
    safe = raw.replace(str(root), "<checkout>").replace(str(scratch), "<scratch>")
    safe = safe.replace(str(Path.home()), "<home>")
    (packet / (name + ".log")).write_text(safe)
    row = {"check": name, "rc": rc, "seconds": round(time.monotonic() - start, 2)}
    print(json.dumps(row), flush=True)
    return row

with ThreadPoolExecutor(max_workers=4) as pool:
    rows = list(pool.map(one, jobs.items()))
(packet / "focused-results.json").write_text(json.dumps(rows, indent=2) + "\n")
sys.exit(any(row["rc"] != 0 for row in rows))
