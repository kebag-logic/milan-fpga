"""Over a planner's nested fuzz family: the compositions whose inside events are all slips and whose excursion lies
at least 64 samples from every planted arm. For each, where the excursion's channel is first listed relative to the
excursion's first word (a tally of offsets), and the seeds where that is not 0.

usage: python3 -I -B interrupted_first_word.py <torture_campaign.py> <frames> <lo> <hi> <jobs>
"""
import json
import multiprocessing
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "r699-6-packet", "scripts"))
import probe_lib  # noqa: E402

T = FRAMES = None


def init(path, frames):
    global T, FRAMES
    T = probe_lib.case(probe_lib.load(path))
    FRAMES = frames


def one(seed):
    units = T._fuzz_nested(FRAMES, seed)
    run = units[0]
    start, end = run[1], run[1] + run[3]
    if any(u[0] != "slip" for u in units[1:]) or any(start - 64 <= arm[1] < end + 64 for arm in T._sweep_arms(FRAMES)):
        return None
    if any(u[1] <= start for u in units[1:]):
        return None
    verdict, detail, _ = T._sweep_grade(FRAMES, [e for u in units for e in u[4]])
    first = min((e["capture_index"] for e in detail["events"] if e["attribution"] == "dut"
                 and e["channel"] == run[2][0] and e["capture_index"] >= start - 63), default=None)
    return seed, verdict, None if first is None else first - start


def main():
    path, frames, lo, hi, jobs = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    with multiprocessing.Pool(jobs, initializer=init, initargs=(path, frames)) as pool:
        rows = [r for r in pool.map(one, range(lo, hi), chunksize=16) if r]
    tally = {}
    for _, verdict, offset in rows:
        tally[f"{verdict} {offset}"] = tally.get(f"{verdict} {offset}", 0) + 1
    print(json.dumps({"frames": frames, "seeds": [lo, hi], "compositions": len(rows), "tally": tally,
                      "not_at_first_word": [r for r in rows if r[2] != 0][:20]}))


if __name__ == "__main__":
    main()
