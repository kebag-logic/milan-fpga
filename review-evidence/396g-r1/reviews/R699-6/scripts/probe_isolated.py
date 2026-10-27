"""Falsification probe for the exactness scope's first shape: one DUT event with at
least 64 clean samples between it and every other event and planted arm (an
excursion whose mask clears its channel number excepted) is classified at its
sample and sized exactly.

usage: python3 -I probe_isolated.py <torture_campaign.py> <frames> <seed_start> <seed_end> <jobs> <out.json>

Each seed draws one event, placed so its whole span keeps >= 70 clean samples
from every sweep arm, grades it with the sweep's arms at tolerance 2, and
compares the DUT records with the class the event's construction states.
Bytes-indistinguishable outcomes that the rules themselves name (a corrupted
word that equals a neighbouring received word, or that is zero) are counted
apart, not as violations.
"""
import json
import multiprocessing
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import probe_lib  # noqa: E402

MOD = T = FRAMES = None
SIZES = (1, 2, 3, 5, 17, 63, 64, 100, 1023, 1024, 1025, 2047, 2048, 2049, 4096)
MARGIN = 70


def init(path, frames):
    global MOD, T, FRAMES
    MOD = probe_lib.load(path)
    T = probe_lib.case(MOD)
    FRAMES = frames


def draw(rnd):
    arms = [a[1] for a in T._sweep_arms(FRAMES)]
    kind = rnd.choice(("drop", "repeat", "silence", "silence_ins", "flip", "run", "run", "swap", "copy"))
    span = 1
    if kind == "run":
        span = rnd.choice((2, 3, 5, rnd.randint(2, 150), rnd.randint(64, 2100)))
    elif kind in ("silence", "silence_ins"):
        span = rnd.randint(1, 40)
    elif kind in ("swap", "copy"):
        span = rnd.randint(1, 40)
    lo, hi = arms[2] + MARGIN, arms[3] - MARGIN - span
    at = rnd.randint(lo, hi)
    ch = rnd.randrange(4)
    if kind in ("drop", "repeat"):
        n = rnd.choice(SIZES + (rnd.randint(1, 5000),))
        return kind, at, ch, n, None, [{"kind": kind, "index": at, "n": n}]
    if kind in ("silence", "silence_ins"):
        return kind, at, ch, span, None, [{"kind": "silence", "index": at, "n": span,
                                           "inserted": kind == "silence_ins"}]
    if kind in ("flip", "run"):
        pick = rnd.random()
        mask = rnd.choice(T._SWEEP_MASKS) if pick < 0.5 else rnd.randrange(1, 1 << 32)
        return kind, at, ch, span, mask, [{"kind": "flip", "index": at + k, "channel": ch, "mask": mask}
                                          for k in range(span)]
    pair = rnd.sample(range(4), 2)
    return kind, at, pair, span, None, [{"kind": kind, "index": at, "n": span, "channels": pair}]


def one(seed):
    rnd = random.Random(seed)
    kind, at, ch, n, mask, events = draw(rnd)
    try:
        verdict, detail, cols = T._sweep_grade(FRAMES, events)
    except Exception as error:
        return seed, kind, "crash", f"{type(error).__name__}: {error}"[:300]
    dut = sorted((e["channel"], e["capture_index"], e["class"], e.get("n"), e.get("mask"), e.get("inserted"),
                  tuple(e.get("located_within", ())))
                 for e in detail["events"] if e["attribution"] == "dut")
    missed = [a["index"] for a in detail["planted_missed"]]
    note = {"verdict": verdict, "dut": dut, "missed": missed, "why": detail.get("why")}
    if verdict != "FAIL" or missed:
        return seed, kind, "violation", note
    if kind in ("drop", "repeat"):
        cls = "dropped" if kind == "drop" else "repeated"
        ok = len(dut) == 4 and sorted(d[0] for d in dut) == [0, 1, 2, 3] and all(
            d[2] == cls and d[3] == n and (d[1] == at if n % 2048 else ((d[1] == at and not d[6]) or (
                d[6] and d[6][0] <= at <= d[6][1] and abs(d[1] - at) <= 63)))
            for d in dut)
    elif kind in ("silence", "silence_ins"):
        ok = len(dut) == 4 and all(d[2] == "silence" and d[3] == n and d[1] == at
                                   and bool(d[5]) == (kind == "silence_ins") for d in dut)
    elif kind == "swap":
        ok = len(dut) == 2 and sorted(d[0] for d in dut) == sorted(ch) and all(
            d[2] == "swap" and d[3] == n and d[1] == at for d in dut)
    elif kind == "copy":
        src, dst = ch
        want = f"0x{((src + 1) ^ (dst + 1)) << 20:08X}"
        ok = len(dut) == 1 and dut[0][:5] == (dst, at, "bit-flip", n, want)
    else:
        clean_v, clean_d, clean = T._sweep_grade(FRAMES, [])
        words = [cols[ch][at + k] for k in range(n)]
        if kind == "run" and ((mask >> 20) & 0xF) == ch + 1:
            return seed, kind, "out-of-scope", note
        if any(w == 0 for w in words):
            return seed, kind, "named-limit:zero", note
        neigh = {cols[ch][at - 1], cols[ch][at + n]}
        if n == 1 and words[0] in neigh:
            return seed, kind, "named-limit:neighbour", note
        ok = len(dut) == 1 and dut[0][:5] == (ch, at, "bit-flip", n, f"0x{mask:08X}")
    return seed, kind, "ok" if ok else "violation", note


def main():
    path, frames, lo, hi, jobs, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), \
        int(sys.argv[5]), sys.argv[6]
    with multiprocessing.Pool(jobs, initializer=init, initargs=(path, frames)) as pool:
        rows = pool.map(one, range(lo, hi), chunksize=16)
    tally, bad = {}, []
    for seed, kind, outcome, note in rows:
        tally.setdefault(kind, {}).setdefault(outcome, 0)
        tally[kind][outcome] += 1
        if outcome in ("violation", "crash"):
            bad.append({"seed": seed, "kind": kind, "note": note})
    result = {"frames": frames, "seeds": [lo, hi], "tally": tally, "violations": len(bad),
              "first_violations": bad[:40]}
    with open(out, "w") as fh:
        json.dump(result, fh, indent=1, sort_keys=True, default=str)
    print(json.dumps({"frames": frames, "seeds": [lo, hi], "tally": tally, "violations": len(bad)}))


if __name__ == "__main__":
    main()
