"""The round-8 inside-scope sentence on every swept event, from a dump_sweeps.py output.

Composition sweep: each corruption (one word at arm index + d, on each channel of its pair), in captures that do not
void. Slip-before sweep: the slip (every channel) and the excursion (each channel). For each event and channel it
counts whether a DUT listing on that channel begins (its capture_index) within 63 samples of the event's first word,
and whether one covers it (its span, located_within or the listed sample widened to its words for every class but
dropped and repeated, overlaps [first - 63, last + 63]); and the largest |capture_index - first| of the nearest.

usage: python3 -I -B sweep_scope_check.py <dump.txt>
"""
import json
import re
import sys

ARMS = lambda frames: [300, 500, 700, frames - 700, frames - 450, frames - 200]  # noqa: E731


def span(e):
    low, high = e.get("located_within") or (e["capture_index"],) * 2
    if e["class"] not in ("dropped", "repeated"):
        high = max(high, e["capture_index"] + e["n"] - 1)
    return low, high


stats = {"events": 0, "begins_within_63": 0, "covered": 0, "max_begin_distance": 0, "misses": []}
for line in open(sys.argv[1]):
    name, record = line.split(" | ", 1)
    verdict, missed, why, events = json.loads(record)
    dut = [json.loads(e) for e in events]
    dut = [e for e in dut if e["attribution"] == "dut"]
    units = []
    m = re.match(r"composition frames=(\d+) d=(-?\d+) mask=(\S+) pair=\((\d), (\d)\)", name)
    if m and verdict != "NOT RUN":
        frames, d = int(m.group(1)), int(m.group(2))
        units = [(index + d, index + d, channel) for index in ARMS(frames)
                 for channel in (int(m.group(4)), int(m.group(5)))]
    m = re.match(r"before length=(\d+) begin=(\d+) gap=(\d+) n=(-?\d+)", name)
    if m:
        length, begin, gap = int(m.group(1)), int(m.group(2)), int(m.group(3))
        units = [(begin - gap, begin - gap, c) for c in range(5)] + [(begin, begin + length - 1, c) for c in range(5)]
    for first, last, channel in units:
        stats["events"] += 1
        mine = [e for e in dut if e["channel"] == channel]
        near = min((abs(e["capture_index"] - first) for e in mine), default=None)
        if near is not None and near <= 63:
            stats["begins_within_63"] += 1
            stats["max_begin_distance"] = max(stats["max_begin_distance"], near)
        elif len(stats["misses"]) < 8:
            stats["misses"].append([name, first, channel, near])
        if any(span(e)[0] <= last + 63 and span(e)[1] >= first - 63 for e in mine):
            stats["covered"] += 1
print(json.dumps(stats, indent=1))
