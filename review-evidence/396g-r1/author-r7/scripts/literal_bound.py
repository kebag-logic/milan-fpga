"""The round-7 ruling's literal lower edge, measured with the planner's own fuzz gate.

The ruling (#396 issuecomment-6435672624, item 1) states: each listing falls at or after the event's first word and
no later than 63 samples after its last word. This runs the planner's _fuzz_check unchanged except _fuzz_reach,
which here also refuses a listing whose samples all lie before the event's first word. Any composition the planner's
own gate passes and this refuses is one the literal lower edge would fail.

usage: python3 -I -B literal_bound.py <torture_campaign.py> <frames> <lo> <hi> <jobs> <units|nested> <out.json>
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


def literal(event, first, last):
    low, high = event.get("located_within", (event["capture_index"],) * 2)
    if event["class"] not in ("dropped", "repeated"):
        high = max(high, event["capture_index"] + event["n"] - 1)
    return MOD.AUDIO_GUARD_FRAMES + 1 if high < first else max(low - last, 0)


def one(seed):
    units = T._fuzz_units(FRAMES, seed) if FAMILY == "units" else T._fuzz_nested(FRAMES, seed)
    original = type(T)._fuzz_reach
    try:
        T._fuzz_check(FRAMES, units)
        gate = None
    except AssertionError as error:
        gate = str(error)[:200]
    T._fuzz_reach = staticmethod(literal).__get__(T)
    try:
        T._fuzz_check(FRAMES, units)
        refused = None
    except AssertionError as error:
        refused = str(error)[:400]
    finally:
        T._fuzz_reach = original
    return seed, gate, refused


def main():
    path, frames, lo, hi, jobs, family, out = (sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]),
                                               int(sys.argv[5]), sys.argv[6], sys.argv[7])
    with multiprocessing.Pool(jobs, initializer=init, initargs=(path, frames, family)) as pool:
        rows = pool.map(one, range(lo, hi), chunksize=16)
    result = {"frames": frames, "family": family, "seeds": [lo, hi],
              "gate_violations": sum(1 for _, g, _ in rows if g),
              "literal_refused": sum(1 for _, g, r in rows if r and not g),
              "refused_seeds": [s for s, g, r in rows if r and not g][:40],
              "first_refusals": [{"seed": s, "refusal": r} for s, g, r in rows if r and not g][:8]}
    with open(out, "w") as fh:
        json.dump(result, fh, indent=1)
    print(json.dumps({k: result[k] for k in ("frames", "family", "seeds", "gate_violations", "literal_refused",
                                             "refused_seeds")}))


if __name__ == "__main__":
    main()
