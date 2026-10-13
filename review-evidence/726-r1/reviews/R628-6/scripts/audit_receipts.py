#!/usr/bin/env python3
"""Re-grade retained runtime logs without rebuilding or executing the source.

Usage: audit_receipts.py PACKET
This checks named detections, omission controls, clean gaps and start shifts.
It is an audit of the saved measurements, not another simulation run.
"""
from collections import Counter
from pathlib import Path
import re
import sys

packet = Path(sys.argv[1])
runs = packet / "receipts/runs"
checked = 0


def read(name):
    global checked
    checked += 1
    return (runs / name).read_text()


def clean(name):
    text = read(name)
    assert "RESULT: PASS" in text and "[FAIL]" not in text, name
    return text


def pair(name, group, omission="escape", count=None, prefix="726"):
    text = read(name + ".run.log")
    fails = [line for line in text.splitlines() if "[FAIL]" in line]
    assert fails and all(f"[{prefix} {group}]" in line for line in fails), name
    if count is not None:
        assert len(fails) == count, (name, len(fails), count)
    clean(name + f".{omission}.log")
    print(f"PAIR {name}: {len(fails)} {group} failures; omission PASS")


groups = {"tx-interval": "TX", "rx-interval": "RX", "tx-reset": "TX_RESET",
          "aaf-reset": "RX_RESET", "crf-reset": "RX_RESET", "rx-saturation": "RX",
          "late": "CADENCE", "egress-stall": "CADENCE", "egress-stall_s8": "CADENCE",
          "rate": "RATE", "tx-nodirty": "OUTPUT_CADENCE", "fixed-grid": "PHASE"}
for variant, group in groups.items():
    pair("m_" + variant, group)
for variant, group in {"late": "CADENCE", "rate": "RATE", "fixed-grid": "PHASE"}.items():
    pair(f"f5_{variant}_s1", group, prefix="F5")
for shape, count in ((1, 8), (8, 36)):
    for probe in ("sched-1600", "sched-2000", "egress-stall"):
        pair(f"r5_{probe}_s{shape}", "CADENCE", omission="omit", count=count)
for probe, group, count in (("aaf-guard", "CADENCE", 2), ("crf-guard", "CADENCE", 2),
                            ("aaf-rx-interval", "RX", 2), ("sched-900", "RATE", 8),
                            ("sched-1030", "CADENCE", 36)):
    pair("my_" + probe, group, omission="omit", count=count)
for shape, rows, gaps, tx in ((1, 8, 28, 799), (8, 36, 126, 800)):
    clean(f"f5_clean_s{shape}.run.log")
    for condition in ("clean", "fo"):
        name = f"w_{condition}_s{shape}"
        text = clean(name + ".run.log")
        data = [line.split(",") for line in text.splitlines() if line.startswith("GAPS,")]
        assert len(data) == rows
        assert sum(int(row[6]) - 1 for row in data) == gaps
        assert all(int(row[6]) >= 2 and float(row[7]) >= 1000
                   and float(row[8]) <= 1025 and float(row[9]) <= 1025 for row in data)
        packets = [line.split(",") for line in text.splitlines() if line.startswith("TX_COUNT,")]
        assert len(packets) == shape + 1
        assert all(int(row[2]) == int(row[3]) == (tx if int(row[1]) < shape else 101)
                   for row in packets)
        shifts = sorted(runs.glob(name + ".shift_*.log"))
        assert len(shifts) == 7
        for log in shifts:
            clean(log.name)
        print(f"CLEAN {name}: {rows} rows, {gaps} gaps, 1000 <= gaps <= 1025 ms; seven shifts PASS")
for shape, count in ((1, 12), (8, 54)):
    text = read(f"b_s{shape}.run.log")
    fails = [line for line in text.splitlines() if "[FAIL]" in line]
    actual = Counter(re.search(r"\[726 ([A-Z_]+)\]", line).group(1) for line in fails)
    assert len(fails) == count and set(actual) == {"TX", "RX", "CADENCE"}
    print(f"BASELINE shape {shape}: {dict(actual)}")
print(f"RECEIPT AUDIT: PASS ({checked} runtime logs checked)")
