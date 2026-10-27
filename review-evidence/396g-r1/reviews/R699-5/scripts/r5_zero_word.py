#!/usr/bin/env python3
"""A constant-mask excursion whose mask clears the channel number, so one masked word is all zero.

Usage: python3 -I r5_zero_word.py <repo>

Channel c carries number c + 1 in word bits 23:20 (sample bits 15:12). The mask (c + 1) << 20
clears it, so the masked word at block position 0 with code bit 0 is the all-zero word.
REQ-VER-06 and TESTING 6d rule 4: "An excursion that returns to its track under one XOR mask
is one bit-flip, at any length", "after a short slip before it"; rule 1: "A flipped channel
number ... is a bit-flip". Prints each reading on the excursion's channel and a tally.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r5_fuzz as f  # noqa: E402


def main():
    f.REPO = sys.argv[1]
    m = f.tc()
    split = cases = 0
    for c in range(4):
        mask = (c + 1) << 20
        for begin, length in ((4096, 1), (4080, 65), (6100, 100), (2100, 9000)):
            for slip in (0, 3, -2):
                extra = [{"kind": "flip", "index": begin + k, "channel": c, "mask": mask} for k in range(length)]
                if slip:
                    extra.append({"kind": "drop" if slip > 0 else "repeat", "index": begin - 5, "n": abs(slip)})
                verdict, detail = f.grade(m, extra)
                mine = sorted((e["capture_index"], e["class"], e["n"]) for e in detail["events"]
                              if e["attribution"] == "dut" and e["channel"] == c
                              and e["class"] not in ("dropped", "repeated"))
                cases += 1
                bad = mine != [(begin, "bit-flip", length)]
                split += bad
                shown = mine if len(mine) <= 7 else mine[:3] + [f"... {len(mine)} events"]
                print(f"{'SPLIT' if bad else 'ok   '} ch{c} mask={mask:#x} begin={begin} len={length} slip={slip:+d}: "
                      f"{verdict} {shown}")
    print(f"{split} of {cases} excursions not read as one bit-flip")


if __name__ == "__main__":
    main()
