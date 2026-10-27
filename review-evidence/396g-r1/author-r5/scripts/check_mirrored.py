#!/usr/bin/env python3
"""Every slip of located_after_arm.py whose located_within misses its true sample: is it the stated limit?

Usage: python3 -I check_mirrored.py <tb/tools dir> <located_after_arm.log>

The limit: beside a planted flip arm, on its channel, the bytes are that slip
where the reading puts it, with the arm's code bit moved to the word the
reading flips, within the tolerance. For each OUTSIDE case this rebuilds the
channel's words over the span from the reading and compares them with the
capture's. Exit status 0.
"""
import ast
import sys
from pathlib import Path

tools, log = sys.argv[1], sys.argv[2]
sys.path.insert(0, tools)
sys.argv = [sys.argv[0], tools]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import torture_campaign as t  # noqa: E402
from arm_d4 import arms, grade  # noqa: E402
from classify_arm import column, shift_at  # noqa: E402

total = held = 0
for line in open(log, encoding="utf-8"):
    if not line.startswith("OUTSIDE"):
        continue
    F, ai, k, n = ast.literal_eval(line.split(" [")[0][len("OUTSIDE "):])
    arm = arms(F)[ai]
    at = arm[1] + k
    extra = [dict(kind="drop" if n > 0 else "repeat", index=at, n=abs(n))]
    verdict, detail = grade(F, extra)
    words = column(F, extra, arm[3])
    for slip in detail["events"]:
        low, high = slip.get("located_within", [slip["capture_index"]] * 2)
        if (slip["class"] not in ("dropped", "repeated") or slip["n"] != abs(n) or slip["attribution"] != "dut"
                or abs(slip["capture_index"] - at) > 8 or low <= at <= high):
            continue
        total += 1
        flips = [e for e in detail["events"] if e["channel"] == slip["channel"] and e["class"] == "bit-flip"
                 and abs(e["capture_index"] - arm[1]) <= 2 and e["mask"] == "0x00000100"]
        if not flips:
            print("CASE", (F, arm[1], k, n), "channel", slip["channel"], "NO FLIP NEAR THE ARM",
                  [(e["channel"], e["capture_index"], e["class"], e["n"]) for e in detail["events"]
                   if abs(e["capture_index"] - arm[1]) < 10])
            continue
        flip = flips[0]
        start = slip["capture_index"]
        old = shift_at(F, start)
        size = slip["n"] if slip["class"] == "dropped" else -slip["n"]
        same = all(words[i] == t.audio_counter_word(slip["channel"] + 1, i + old + (size if i >= start else 0))
                   ^ (0x100 if i == flip["capture_index"] else 0)
                   for i in range(min(start, arm[1]) - 2, max(start, arm[1], at) + 64))
        held += same
        print("CASE", (F, arm[1], k, n), "slip at", start, "flip at", flip["capture_index"], verdict,
              "bytes identical" if same else "BYTES DIFFER")
print("SUMMARY", total, "slips located away from their sample;", held, "are the stated limit")
