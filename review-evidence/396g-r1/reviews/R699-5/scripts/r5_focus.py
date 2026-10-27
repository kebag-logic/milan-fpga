#!/usr/bin/env python3
"""Focused cases for two fuzz shapes, graded at one checkout.

Usage: python3 -I r5_focus.py <repo>

Z: a constant-mask excursion under 0x100000 on channel 0 (number 1 -> 0) whose
   masked words include an all-zero word (block position 0, code bit 0), with
   and without a short slip before it. Claim: one bit-flip of its length
   (REQ-VER-06: "an excursion that returns to its track under one XOR mask is
   one bit-flip, at any length ... and after a short slip before it").
S: a multi-word constant-mask excursion on one channel that straddles a planted
   slip arm (fuzz seeds 1546, 2160, 2979). Claim checked: whether the run voids,
   a shape outside the two voids TESTING 6d lists.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r5_fuzz as f  # noqa: E402


def show(m, label, extra):
    verdict, detail = f.grade(m, extra)
    dut = sorted((e["channel"], e["capture_index"], e["class"], e["n"], e.get("mask", ""))
                 for e in detail["events"] if e["attribution"] == "dut")
    print(f"{label}: {verdict} | missed={[a['index'] for a in detail.get('planted_missed', [])]} | {dut}")


def run(c, begin, length, mask):
    return [{"kind": "flip", "index": begin + k, "channel": c, "mask": mask} for k in range(length)]


def main():
    f.REPO = sys.argv[1]
    m = f.tc()
    for begin, length in ((4080, 65), (4090, 20), (4095, 2), (4096, 64), (6100, 100), (4000, 488)):
        show(m, f"Z no slip  begin={begin} len={length}", run(0, begin, length, 0x100000))
        for n in (3, -2):
            slip = [{"kind": "drop" if n > 0 else "repeat", "index": begin - 5, "n": abs(n)}]
            show(m, f"Z slip {n:+d} begin={begin} len={length}", slip + run(0, begin + 0, length, 0x100000))
    # The same shape on channel 2 (number 3 -> 2, never zero) as a control.
    show(m, "Z control channel 2 begin=4080 len=65", run(2, 4080, 65, 0x100000))
    show(m, "Z control slip+3 channel 2", [{"kind": "drop", "index": 4075, "n": 3}] + run(2, 4080, 65, 0x100000))
    # Seed shapes: an excursion over a planted slip arm (arms at 15684 drop 3 and 15934 repeat 2).
    show(m, "S seed2979 ch2 0x1000000 15794+143", run(2, 15794, 143, 0x1000000))
    show(m, "S seed1546 ch1 0x40000 15571+126", run(1, 15571, 126, 0x40000))
    for mask in (0x100, 0x1000000, 0x80000, 0x200):
        for lead, tail in ((10, 10), (2, 2), (1, 30), (30, 1), (0, 5), (5, 0)):
            show(m, f"S arm 15934 ch2 mask={mask:#x} lead={lead} tail={tail}", run(2, 15934 - lead, lead + tail, mask))


if __name__ == "__main__":
    main()
