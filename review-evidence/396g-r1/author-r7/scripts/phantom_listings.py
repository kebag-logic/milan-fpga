"""Whether every DUT listing lies within reach of an event that changes its channel, over both fuzz families of one
planner: its words (or located_within) reach no earlier than 63 samples before the event's first word and begin no
later than 63 samples after its last, by the planner's own _fuzz_reach. Counts void runs with such listings apart (a
missed arm's own records are DUT-attributed there) and prints the runs that do not void and have one.

usage: python3 -I -B phantom_listings.py <torture_campaign.py> <frames> <lo> <hi> <jobs> <units|nested>
"""
import json
import multiprocessing
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "r699-6-packet", "scripts"))
import probe_lib  # noqa: E402

MOD = T = FRAMES = FAMILY = None


def init(path, frames, family):
    global MOD, T, FRAMES, FAMILY
    MOD = probe_lib.load(path)
    T = probe_lib.case(MOD)
    FRAMES, FAMILY = frames, family


def one(seed):
    units = T._fuzz_units(FRAMES, seed) if FAMILY == "units" else T._fuzz_nested(FRAMES, seed)
    verdict, detail, _ = T._sweep_grade(FRAMES, [event for unit in units for event in unit[4]])
    stray = []
    for e in detail["events"]:
        if e["attribution"] != "dut":
            continue
        if not any(e["channel"] in channels and T._fuzz_reach(e, at, at + span - 1) <= MOD.AUDIO_GUARD_FRAMES
                   for _, at, channels, span, _ in units):
            stray.append((e["channel"], e["capture_index"], e["class"], e["n"], e.get("located_within")))
    return seed, verdict, stray


def main():
    path, frames, lo, hi, jobs, family = (sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]),
                                          int(sys.argv[5]), sys.argv[6])
    with multiprocessing.Pool(jobs, initializer=init, initargs=(path, frames, family)) as pool:
        rows = pool.map(one, range(lo, hi), chunksize=16)
    bad = [(seed, verdict, stray) for seed, verdict, stray in rows if stray and verdict != "NOT RUN"]
    print(json.dumps({"frames": frames, "family": family, "seeds": [lo, hi], "with_stray_outside_void_runs": len(bad), "void_runs_with_stray": sum(1 for _, v, s in rows if s and v == "NOT RUN"),
                      "first": bad[:10]}))


if __name__ == "__main__":
    main()
