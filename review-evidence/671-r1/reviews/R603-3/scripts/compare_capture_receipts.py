#!/usr/bin/env python3
# R603-3: compare the capture receipt at two revisions, capture by capture.
# usage: compare_capture_receipts.py ROOT OLD_REV NEW_REV
import json
import subprocess
import sys

root, old, new = sys.argv[1:4]


def load(rev):
    return json.loads(subprocess.check_output(
        ["git", "-C", root, "show", f"{rev}:tb/verilator/nvm_capture_cpu/measurements.json"]))


a, b = load(old), load(new)
print("changed top-level keys:", [k for k in b if a.get(k) != b.get(k)])
print("maxima equal:", a["maxima"] == b["maxima"])
n = d = 0
for ma, mb in zip(a["measurements"], b["measurements"]):
    for ra, rb in zip(ma["rows"], mb["rows"]):
        n += 1
        d += ra != rb
    print(f"{mb['shape']} cpu_hz={mb['cpu_hz']} traffic={mb['traffic']} min={mb['minimum_ms']:.5f} "
          f"max={mb['maximum_ms']:.5f} ratio={49 / mb['maximum_ms']:.4f}x")
print(f"captures compared: {n}; rows differing in any field: {d}")
print("firmware sha256 in receipt:", b["product_firmware_sha256"])
