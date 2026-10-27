#!/usr/bin/env python3
"""Seeded falsification probes for the #396 audio counter grader at one head.

Usage: python3 -I r5_fuzz.py <repo> <family> <first-seed> <count> <jobs>

Families:
  isolated  1 to 4 DUT events, each 200+ samples from every other and 80+ from every planted arm.
            Claim checked: FAIL with every arm found; no unbalanced guard; per-channel DUT slip
            net equals the planted net; each event found at its sample with its class and size.
  before    a short slip (1 to 8 either way) 1 to 64 samples before a constant-mask excursion
            (64 to 2100 words, random block position, mask from the sweep classes and random
            multi-bit ones). Claim: the slip exact on every channel and one bit-flip of the
            excursion's length and mask on its channel (REQ-VER-06, TESTING 6d).
  cluster   2 to 5 DUT events of any kind inside 80 samples, away from arms. Claim checked:
            never PASS; arms all found; either the reading balances (DUT slip net equals the
            planted net) or an unresolved guard event is recorded.
Prints one line per violation and a closing tally.
"""
import json
import random
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

REPO = None
FRAMES = 16384
ARMS = [("drop", 300, 3, None), ("repeat", 500, 2, None), ("flip", 700, 0x100, 1),
        ("drop", FRAMES - 700, 3, None), ("repeat", FRAMES - 450, 2, None), ("flip", FRAMES - 200, 0x100, 1)]
MASKS = (0x100, 0x200, 0x1E00, 0x40000, 0x80000, 0x80100, 0x100000, 0x01000000, 0x00F00F00, 0x7FE00)


def tc():
    sys.path.insert(0, str(Path(REPO) / "tb" / "tools"))
    import torture_campaign
    return torture_campaign


def grade(m, extra, channels=4):
    source = [{"kind": "flip", "index": i, "channel": c, "mask": s} if k == "flip"
              else {"kind": k, "index": i, "n": s} for k, i, s, c in ARMS]
    log = [{"class": "bit-flip", "index": i, "mask": s, "channel": c} if k == "flip"
           else {"class": "dropped" if k == "drop" else "repeated", "index": i, "n": s} for k, i, s, c in ARMS]
    cap = m.synthesize_counter_capture(FRAMES, channels, byteorder=sys.byteorder, events=source + extra)
    return m.grade_audio_counter_capture(cap, m.CounterCapture(channels, sys.byteorder, 48000, 0.0, 0.0),
                                         m.CounterRunLog(log, [], 2), required_s=(FRAMES - 126) / 48000)


def net(m, events, channel):
    return m._audio_net(e for e in events if e["channel"] == channel and e["attribution"] == "dut")


def far(at, taken, gap):
    return all(abs(at - t) >= gap for t in taken)


def isolated(m, seed):
    rnd, bad = random.Random(seed), []
    taken, extra, want = [a[1] for a in ARMS], [], []
    for _ in range(rnd.randint(1, 4)):
        for _ in range(200):
            at = rnd.randint(500, FRAMES - 500)
            if far(at, taken[:6], 80) and far(at, taken[6:], 200):
                break
        else:
            continue
        taken.append(at)
        kind = rnd.choice(("flip", "drop", "repeat", "run", "silence", "inserted"))
        if kind == "flip":
            c, mask = rnd.randrange(4), rnd.choice(MASKS)
            extra.append({"kind": "flip", "index": at, "channel": c, "mask": mask})
            want.append((c, at, "bit-flip", 1))
        elif kind in ("drop", "repeat"):
            n = rnd.choice((1, 2, 3, 5, 17, 100, 1023, 1025))
            extra.append({"kind": kind, "index": at, "n": n})
            want += [(c, at, "dropped" if kind == "drop" else "repeated", n) for c in range(4)]
        elif kind == "run":
            c, mask, length = rnd.randrange(4), rnd.choice(MASKS), rnd.randint(2, 150)
            extra += [{"kind": "flip", "index": at + k, "channel": c, "mask": mask} for k in range(length)]
            want.append((c, at, "bit-flip", length))
        else:
            n = rnd.randint(1, 40)
            extra.append({"kind": "silence", "index": at, "n": n, "inserted": kind == "inserted"})
            want += [(c, at, "silence", n) for c in range(4)]
    verdict, detail = grade(m, extra)
    dut = [e for e in detail.get("events", []) if e["attribution"] == "dut"]
    got = sorted((e["channel"], e["capture_index"], e["class"], e["n"]) for e in dut)
    if (verdict, detail.get("planted_missed")) != ("FAIL", []):
        bad.append(("verdict", verdict, detail.get("why")))
    if any(e.get("unresolved") == m.AUDIO_UNBALANCED_REASON for e in detail.get("events", [])):
        bad.append(("guard fired",))
    for c in range(4):
        planted = sum((e["n"] if e["kind"] == "drop" else -e["n"]) if e["kind"] in ("drop", "repeat")
                      else -e["n"] if e["kind"] == "silence" and e.get("inserted") else 0 for e in extra)
        if net(m, detail.get("events", []), c) != planted:
            bad.append(("net", c, net(m, detail.get("events", []), c), planted))
    if got != sorted(want):
        bad.append(("events", got, sorted(want)))
    return seed, extra, bad


def before(m, seed):
    rnd, bad = random.Random(seed), []
    length, gap = rnd.choice((64, 65, rnd.randint(66, 400), rnd.randint(400, 2100))), rnd.randint(1, 64)
    begin = rnd.choice((rnd.randint(2000, 9000), 4096 - rnd.randint(0, 70), 6144 - rnd.randint(0, 70)))
    n = rnd.choice((1, 2, 3, 4, 5, 6, 7, 8)) * rnd.choice((1, -1))
    c, mask = rnd.randrange(4), rnd.choice(MASKS)
    extra = [{"kind": "drop" if n > 0 else "repeat", "index": begin - gap, "n": abs(n)}]
    extra += [{"kind": "flip", "index": begin + k, "channel": c, "mask": mask} for k in range(length)]
    verdict, detail = grade(m, extra)
    dut = sorted((e["channel"], e["capture_index"], e["class"], e["n"], e.get("mask", ""))
                 for e in detail.get("events", []) if e["attribution"] == "dut")
    slip = "dropped" if n > 0 else "repeated"
    want = sorted([(k, begin - gap, slip, abs(n), "") for k in range(4)] + [(c, begin, "bit-flip", length, f"0x{mask:08X}")])
    if (verdict, detail.get("planted_missed")) != ("FAIL", []) or dut != want:
        bad.append(("before", verdict, dut, want))
    if any(e.get("unresolved") == m.AUDIO_UNBALANCED_REASON for e in detail.get("events", [])):
        bad.append(("guard fired",))
    return seed, extra, bad


def cluster(m, seed):
    rnd, bad = random.Random(seed), []
    base, extra, planted = rnd.randint(1200, FRAMES - 1500), [], 0
    for _ in range(rnd.randint(2, 5)):
        at, kind = base + rnd.randint(0, 80), rnd.choice(("flip", "drop", "repeat", "run"))
        if kind == "flip":
            extra.append({"kind": "flip", "index": at, "channel": rnd.randrange(4), "mask": rnd.choice(MASKS)})
        elif kind == "run":
            c, mask = rnd.randrange(4), rnd.choice(MASKS)
            extra += [{"kind": "flip", "index": at + k, "channel": c, "mask": mask} for k in range(rnd.randint(2, 90))]
        else:
            n = rnd.choice((1, 2, 3, 7, 1024, 2048, 4096))
            extra.append({"kind": kind, "index": at, "n": n})
            planted += n if kind == "drop" else -n
    verdict, detail = grade(m, extra)
    events = detail.get("events", [])
    if verdict != "FAIL" or detail.get("planted_missed"):
        bad.append(("verdict", verdict, detail.get("why")))
    guard = {e["channel"] for e in events if e.get("unresolved") == m.AUDIO_UNBALANCED_REASON}
    for c in range(4):
        if c not in guard and net(m, events, c) != planted:
            bad.append(("net", c, net(m, events, c), planted))
    return seed, extra, bad


def work(args):
    global REPO
    REPO, family, seed = args
    m = tc()
    seed, extra, bad = {"isolated": isolated, "before": before, "cluster": cluster}[family](m, seed)
    return seed, extra, bad


def main():
    repo, family, first, count, jobs = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    fails = 0
    with ProcessPoolExecutor(jobs) as pool:
        for seed, extra, bad in pool.map(work, [(repo, family, s) for s in range(first, first + count)], chunksize=4):
            if bad:
                fails += 1
                print(json.dumps({"seed": seed, "extra": extra, "bad": bad}, default=str), flush=True)
    print(f"{family}: {fails} violating of {count} seeds from {first}", flush=True)
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
