#!/usr/bin/env python3
"""Check fault-window enumeration and firmware-bound capture arithmetic."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
ap = argparse.ArgumentParser()
ap.add_argument("repo", type=Path)
a = ap.parse_args()
repo = a.repo.resolve()
sys.dont_write_bytecode = True
sys.path.insert(0, str(repo / "sw/firmware/nvm_hosttest"))
import read_fault_cases as c
rows = c.fault_cases(1000)
print("cases", len(rows), dict(Counter("restart" if x.restart else "cold" for x in rows)))
assert len(rows) == 2158
for restart in (False, True):
    for valid in "ab":
        seen = {(x.skip,x.count) for x in rows if x.restart == restart and x.valid == valid and x.fault[0] == "--read-fault"}
        assert seen == set(c.windows(c.BOOT_READ_BOUND - int(restart)))
        print("all byte-fault windows represented", "restart" if restart else "cold", valid, len(seen))
m = json.loads((repo / "tb/verilator/nvm_capture_cpu/measurements.json").read_text())
assert hashlib.sha256((repo / "sw/firmware/milan_baremetal/milan_baremetal.c").read_bytes()).hexdigest() == m["product_firmware_sha256"]
print("firmware digest", m["product_firmware_sha256"])
for x in m["measurements"]:
    values = [y["sys_cycles"] / x["sys_hz"] * 1000 for y in x["rows"]]
    assert len(values) == 16
    assert all(y["ok"] == 1 and y["mismatches"] == 0 for y in x["rows"])
    assert abs(max(values) - x["maximum_ms"]) < 1e-9
    assert abs(min(values) - x["minimum_ms"]) < 1e-9
    assert abs(49 / max(values) - x["margin"]) < 1e-9
    print(x["shape"], x["cpu_hz"], x["traffic"], len(values), min(values), max(values))
print("PASS: generated window population and all six capture receipt arms agree")
