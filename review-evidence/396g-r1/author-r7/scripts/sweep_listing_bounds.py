"""Where each swept DUT event is listed relative to its own words, from a dump_sweeps.py output.

Composition sweep: each corruption (one word at arm index + d, on each channel of its pair), in captures that do not
void. Slip-before sweep: the slip (every channel) and the excursion (each channel). For each, the DUT listings on that
channel within 63 samples either side: the counts with no listing at or after its first word and no later than 63
after its last, the counts listed before their first word, and the largest distance from the first word.

usage: python3 -I -B sweep_listing_bounds.py <dump.txt>
"""
import json
import re
import sys

ARMS = lambda frames: [("dropped", 300, None), ("repeated", 500, None), ("bit-flip", 700, 1),  # noqa: E731
                       ("dropped", frames - 700, None), ("repeated", frames - 450, None), ("bit-flip", frames - 200, 1)]
stats = {"events": 0, "no_listing_in_bound": 0, "listed_before_first": 0, "max_from_first": 0, "examples": []}
for line in open(sys.argv[1]):
    name, record = line.split(" | ", 1)
    verdict, missed, why, events = json.loads(record)
    events = [json.loads(e) for e in events]
    dut = [e for e in events if e["attribution"] == "dut"]
    units = []
    m = re.match(r"composition frames=(\d+) d=(-?\d+) mask=(\S+) pair=\((\d), (\d)\)", name)
    if m and verdict != "NOT RUN":
        frames, d = int(m.group(1)), int(m.group(2))
        units = [(index + d, index + d, channel) for _, index, _ in ARMS(frames)
                 for channel in (int(m.group(4)), int(m.group(5)))]
    m = re.match(r"before length=(\d+) begin=(\d+) gap=(\d+) n=(-?\d+)", name)
    if m:
        length, begin, gap = int(m.group(1)), int(m.group(2)), int(m.group(3))
        units = [(begin - gap, begin - gap, c) for c in range(5)] + [(begin, begin + length - 1, c) for c in range(5)]
    for first, last, channel in units:
        stats["events"] += 1
        near = [e for e in dut if e["channel"] == channel and first - 63 <= e["capture_index"] <= last + 63]
        inside = [e for e in near if first <= e["capture_index"] <= last + 63]
        if not inside:
            stats["no_listing_in_bound"] += 1
            if near and min(e["capture_index"] for e in near) < first:
                stats["listed_before_first"] += 1
                if len(stats["examples"]) < 8:
                    stats["examples"].append([name, first, channel, [(e["capture_index"], e["class"], e["n"])
                                                                     for e in near]])
        else:
            stats["max_from_first"] = max(stats["max_from_first"], min(e["capture_index"] for e in inside) - first)
print(json.dumps(stats, indent=1))
