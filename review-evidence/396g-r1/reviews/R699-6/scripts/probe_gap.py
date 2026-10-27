"""Grid probe: a constant-mask excursion on channel 0 with a DUT slip inside it, away
from every planted arm. Measures the gap from the excursion's first word to the
first DUT event listed on channel 0 (the claim is <= 63), and the verdict.

usage: python3 -I probe_gap.py <torture_campaign.py> <frames> <jobs> <out.json>
"""
import itertools
import json
import multiprocessing
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import probe_lib  # noqa: E402

T = FRAMES = None
MASKS = (0x100, 0x200, 0x1E00, 0x40000, 0x80000, 0x80100, 0x01000000, 0x00C80100)


def init(path, frames):
    global T, FRAMES
    T = probe_lib.case(probe_lib.load(path))
    FRAMES = frames


def one(case):
    start, length, back, kind, n, mask = case
    slip = start + length - back
    events = [{"kind": "flip", "index": start + k, "channel": 0, "mask": mask} for k in range(length)]
    events.append({"kind": kind, "index": slip, "n": n})
    verdict, detail, _ = T._sweep_grade(FRAMES, events)
    first = min((e["capture_index"] for e in detail["events"] if e["attribution"] == "dut" and e["channel"] == 0
                 and e["capture_index"] >= start - 63), default=None)
    gap = None if first is None else first - start
    return dict(start=start, length=length, slip_at=slip, kind=kind, n=n, mask=f"0x{mask:08X}", verdict=verdict,
                missed=len(detail["planted_missed"]), gap=gap)


def main():
    path, frames, jobs, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    cases = [c for c in itertools.product(range(1000, 9000, 397), (300, 900, 1726, 2500, 4000), (53, 300),
                                          ("repeat", "drop"), (3, 17), MASKS)
             if c[0] + c[1] + 80 < frames - 700]
    with multiprocessing.Pool(jobs, initializer=init, initargs=(path, frames)) as pool:
        rows = pool.map(one, cases, chunksize=8)
    bad = [r for r in rows if r["gap"] is None or r["gap"] > 63]
    passes = [r for r in rows if r["verdict"] == "PASS"]
    by_mask = {}
    for r in bad:
        by_mask[r["mask"]] = by_mask.get(r["mask"], 0) + 1
    result = {"frames": frames, "cases": len(rows), "gap_over_63": len(bad), "pass": len(passes),
              "by_mask": by_mask, "max_gap": max((r["gap"] or 0) for r in rows),
              "worst": sorted(bad, key=lambda r: -(r["gap"] or 10 ** 9))[:15]}
    json.dump(result, open(out, "w"), indent=1)
    print(json.dumps({k: result[k] for k in ("frames", "cases", "gap_over_63", "pass", "by_mask", "max_gap")}))


if __name__ == "__main__":
    main()
