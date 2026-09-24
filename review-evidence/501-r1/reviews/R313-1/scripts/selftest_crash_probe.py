#!/usr/bin/env python3
"""Reviewer probe (R313-1): does --self-test refuse a control that CRASHES?

Usage: python3 selftest_crash_probe.py <head-tree-copy>

SAVED_STATE_FASTCONNECT.md section 4.4 (this head) says of --self-test:
"Each must return a finding, never a crash." Make the existing `collide`
control raise instead of perturbing the allocation, run --self-test on the
COPY, and report whether the gate still exits 0. Restores the original bytes.
"""
import hashlib
import subprocess
import sys
from pathlib import Path

T = Path(sys.argv[1]).resolve()
p = T / "scripts/check_nvm_record_space.py"
orig = p.read_bytes()
old = '    ALLOC["FMT_OUT"] = (ALLOC["FMT_IN"][0], ALLOC["FMT_IN"][1])\n'
t = orig.decode()
assert t.count(old) == 1
p.write_text(t.replace(old, '    raise RuntimeError("R313 probe: this control crashed")\n'))
try:
    single = subprocess.run([sys.executable, str(p), "--mutate=collide", "--quiet"],
                            cwd=T, capture_output=True, text=True)
    print(f"--mutate=collide alone: rc={single.returncode}; traceback={'Traceback' in single.stderr}")
    r = subprocess.run([sys.executable, str(p), "--self-test", "--quiet"],
                       cwd=T, capture_output=True, text=True)
    line = next((ln for ln in r.stdout.splitlines() if "collide" in ln), "")
    print(f"--self-test with a crashing control: rc={r.returncode}")
    print(f"its line: {line}")
    print("RESULT: crash ACCEPTED as a reddened control" if r.returncode == 0
          else "RESULT: crash refused")
finally:
    p.write_bytes(orig)
    assert hashlib.sha256(p.read_bytes()).digest() == hashlib.sha256(orig).digest()
    print("restored original bytes")
