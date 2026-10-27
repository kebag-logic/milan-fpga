#!/usr/bin/env python3
"""A multi-word constant-mask excursion over a planted slip arm, graded at one checkout.

Usage: python3 -I r5_arm_excursion.py <repo>

For each planted slip arm (drop 3 at 300, repeat 2 at 500, drop 3 at FRAMES-700, repeat 2
at FRAMES-450), each channel, each mask class and each excursion of 2 to 12 words starting
8 samples before to 3 after the arm's sample, the planted truth is one reading of the bytes:
the arm at its sample and one bit-flip of the excursion's length under its mask against the
track in force at each word. That reading has exactly one DUT event and finds every arm.

TESTING 6d (this head): "The grader takes another reading only when it has fewer DUT
events, or as many and more arms found"; "It cannot place an arm where the bytes leave no
reading that finds it. The voids below are those shapes"; and the void list names two
one-word shapes only, adding "The code bit alone, a channel-number bit or a pad bit cannot".

Counts the cases graded NOT RUN with the arm missed, and of those, the ones whose mask is the
code bit, a channel-number bit or a pad bit.
"""
import collections
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r5_fuzz as f  # noqa: E402

MASKS = (0x100, 0x200, 0x1E00, 0x40000, 0x80000, 0x80100, 0x100000, 0x01000000)
NOT_POSITION = (0x100, 0x100000, 0x01000000)


def main():
    f.REPO = sys.argv[1]
    m = f.tc()
    tally, examples = collections.Counter(), []
    arms = [a for a in f.ARMS if a[0] != "flip"]
    for kind, index, n, _ in arms:
        for channel in range(4):
            for mask in MASKS:
                if mask == 0x100000 and channel in (0, 2):
                    continue  # channel numbers 1 and 3 lose bit 20: the zero-word and foreign-number shapes, apart
                for start in range(-8, 4):
                    for length in range(2, 13):
                        if start + length <= 0:
                            continue  # the excursion must cover the arm's sample
                        extra = [{"kind": "flip", "index": index + start + k, "channel": channel, "mask": mask}
                                 for k in range(length)]
                        verdict, detail = f.grade(m, extra)
                        missed = [a["index"] for a in detail.get("planted_missed", [])]
                        dut = [e for e in detail["events"] if e["attribution"] == "dut"]
                        tally["cases"] += 1
                        if verdict == "NOT RUN" and missed:
                            tally["void"] += 1
                            tally[f"void mask={mask:#x}"] += 1
                            if mask in NOT_POSITION:
                                tally["void, code/channel/pad mask"] += 1
                            if len(examples) < 12 and mask in NOT_POSITION:
                                examples.append((kind, index, channel, f"{mask:#x}", start, length, len(dut),
                                                 sorted((e["capture_index"], e["class"], e["n"], e.get("mask", ""))
                                                        for e in dut if e["channel"] == channel)))
                        elif verdict != "FAIL":
                            tally[f"other {verdict}"] += 1
    for key in sorted(tally):
        print(f"{key}: {tally[key]}")
    for example in examples:
        print("example", example)


if __name__ == "__main__":
    main()
