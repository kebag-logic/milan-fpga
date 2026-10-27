#!/usr/bin/env python3
"""Summarize fresh_seeds.py receipts: per range, the gate's refusals, verdicts, the independent
coverage count, and how each uncovered unit-channel was excused.

usage: summarize_fresh.py <receipt-dir>
"""
import glob
import json
import os
import sys

total = {"compositions": 0, "refused": 0, "unit_channels": 0, "covered": 0, "uncovered": 0,
         "uncovered_unexcused": 0, "pass_with_dut_unit": 0}
for f in sorted(glob.glob(os.path.join(sys.argv[1], "*_*_*_*.jsonl"))):
    lines = open(f).read().splitlines()
    summary = [line for line in lines if line.startswith("SUMMARY")]
    rows = [json.loads(line) for line in lines if not line.startswith("SUMMARY")]
    if not summary:
        print("NO SUMMARY", os.path.basename(f))
        continue
    s = json.loads(summary[0].split(" ", 5)[5])
    uncovered = [r for r in rows if r["uncovered"]]
    unexcused = [r for r in uncovered if not r["allowed"]]
    passes = [r for r in rows if r["verdict"] == "PASS"]
    for k, v in (("compositions", s["compositions"]), ("refused", s["gate_refused"]),
                 ("unit_channels", s["unit_channels"]), ("covered", s["covered"]),
                 ("uncovered", s["uncovered"]), ("uncovered_unexcused", len(unexcused)),
                 ("pass_with_dut_unit", len(passes))):
        total[k] += v
    print(os.path.basename(f), "compositions", s["compositions"], "refused", s["gate_refused"], "verdicts", s["verdicts"],
          "unit-channels", s["unit_channels"], "covered", s["covered"], "uncovered", s["uncovered"],
          "excused-by", sorted({a for r in uncovered for a in r["allowed"]}), "unexcused", len(unexcused),
          "PASS", len(passes))
print("TOTAL", json.dumps(total))
