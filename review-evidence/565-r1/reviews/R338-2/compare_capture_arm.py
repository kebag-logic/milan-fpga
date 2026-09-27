#!/usr/bin/env python3
"""Compare a reproduced capture arm with the committed receipt's matching arm.

Usage: compare_capture_arm.py <repo> <measurement.json>
Prints the reproduced summary, whether every row equals the receipt's row, and
regrades the reproduction with the harness's own grader.
"""
import json
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / "tb/verilator/nvm_capture_cpu"))
import run as capture  # noqa: E402

got = json.loads(Path(sys.argv[2]).read_text())
receipt = json.loads((repo / "tb/verilator/nvm_capture_cpu/measurements.json").read_text())
arm = [a for a in receipt["measurements"]
       if (a["shape"], a["cpu_hz"], a["traffic"]) == (got["shape"], got["cpu_hz"], got["traffic"])]
assert len(arm) == 1, "no unique matching receipt arm"
arm = arm[0]
summary = {k: v for k, v in got.items() if k != "rows"}
print("reproduced:", json.dumps(summary))
fields = ["shape", "captures", "sys_hz", "cpu_hz", "configured_cpu_hz", "phase", "traffic",
          "minimum_ms", "maximum_ms", "hold_ms", "hold_floor_ms", "margin"]
for f in fields:
    print(f"  {f}: reproduced={got[f]!r} receipt={arm[f]!r} {'EQUAL' if got[f] == arm[f] else 'DIFFERENT'}")
same = [r == s for r, s in zip(got["rows"], arm["rows"])]
print(f"rows: {len(got['rows'])} reproduced, {len(arm['rows'])} in receipt, {sum(same)} identical")
for i, (r, s) in enumerate(zip(got["rows"], arm["rows"])):
    if r != s:
        print(f"  row {i}: reproduced={r} receipt={s}")
regraded = capture.grade_rows(got["rows"], {k: got[k] for k in fields if k in got} | {"tdm_hz": 0})
print("regraded maximum_ms:", regraded["maximum_ms"], "under 24.5 ms:", regraded["maximum_ms"] <= 24.5)
ok = all(got[f] == arm[f] for f in fields) and all(same) and len(got["rows"]) == len(arm["rows"])
print("RESULT:", "IDENTICAL TO RECEIPT" if ok else "DIFFERS FROM RECEIPT")
sys.exit(0 if ok else 1)
