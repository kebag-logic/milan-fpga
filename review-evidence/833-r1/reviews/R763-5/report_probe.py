#!/usr/bin/env python3
"""Print the failure description of one live child, as owner_report builds it.

Usage: python3 -I report_probe.py <tree>
TESTING.md:277: the message prints each remaining process's scheduler state,
wait channel, parent and age. Exit 1 if the current parent or a plausible age is missing.
"""
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]) / "scripts"))
import owned_process  # noqa: E402

child = subprocess.Popen(["sleep", "30"])
time.sleep(0.3)
try:
    lines = [owned_process._describe(child.pid, None, None), owned_process._describe(child.pid, 1, None)]
finally:
    child.kill()
    child.wait()
bad = 0
for line in lines:
    print(line)
    if not re.search(rf"\) state \S+ wchan \S+ parent {os.getpid()} ", line):
        print("  current parent missing")
        bad = 1
    age = re.search(r" age (-?[0-9.]+) s ", line)
    if not age or not 0.0 <= float(age.group(1)) < 30.0:
        print("  age missing or implausible for a 0.3 s old child")
        bad = 1
sys.exit(bad)
