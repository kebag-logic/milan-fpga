"""How one torture_campaign.py reads R699-6's interrupted-excursion grid (probe_gap.py's cases) on the excursion's
channel: the tally of the first DUT listing's shape relative to the excursion and its slip.

usage: python3 -I -B interrupted_reading.py <torture_campaign.py> <frames> <jobs>
"""
import itertools
import json
import multiprocessing
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "r699-6-packet", "scripts"))
import probe_gap  # noqa: E402


def one(case):
    start, length, back, kind, n, mask = case
    slip = start + length - back
    events = [{"kind": "flip", "index": start + k, "channel": 0, "mask": mask} for k in range(length)]
    events.append({"kind": kind, "index": slip, "n": n})
    verdict, detail, _ = probe_gap.T._sweep_grade(probe_gap.FRAMES, events)
    dut = sorted((e for e in detail["events"] if e["attribution"] == "dut" and e["channel"] == 0
                  and e["capture_index"] >= start - 63), key=lambda e: e["capture_index"])
    if slip == start:
        return "slip at the first word"
    head = dut[0]
    if (head["capture_index"], head["class"], head["n"], head.get("mask")) == (start, "bit-flip", slip - start,
                                                                                f"0x{mask:08X}"):
        return "one bit-flip from the first word to the slip, then the slip's words"
    if (head["capture_index"], head["class"]) == (start, "bit-flip") and head.get("mask") == f"0x{mask:08X}":
        return "a bit-flip of the excursion's mask from the first word, of another length"
    return "first listing at %+d from the first word, %s" % (head["capture_index"] - start, head["class"])


def main():
    path, frames, jobs = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    cases = [c for c in itertools.product(range(1000, 9000, 397), (300, 900, 1726, 2500, 4000), (53, 300),
                                          ("repeat", "drop"), (3, 17), probe_gap.MASKS)
             if c[0] + c[1] + 80 < frames - 700]
    with multiprocessing.Pool(jobs, initializer=probe_gap.init, initargs=(path, frames)) as pool:
        rows = pool.map(one, cases, chunksize=8)
    tally = {}
    for row in rows:
        tally[row] = tally.get(row, 0) + 1
    print(json.dumps({"frames": frames, "cases": len(rows), "tally": tally}, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
