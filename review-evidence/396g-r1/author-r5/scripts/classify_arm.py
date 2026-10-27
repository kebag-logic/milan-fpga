#!/usr/bin/env python3
"""Classify every arm x one-word corruption case (d = -4..+4) by byte predicates, and check its outcome.

Usage: python3 -I classify_arm.py <tools dir> [jobs]
Classes, decided from the bytes alone:
  X2  flip arm's own channel, on its sample, or one beside it under the arm's own mask   -> void, that arm missed
  X1  slip arm, the sample before it or its own, the corrupted word is another position's word
      (its channel's counter word less than half a block from the old or the new track's) -> void, that arm missed
  L1  the corrupted word equals a received neighbour                                       -> FAIL, a one-sample slip pair at it
  L2  slip arm, its own sample or the next one: the corruption reads first, judged against the offset
      before the slip, the slip after it within the tolerance; bytes identical              -> FAIL, one bit-flip
  E   otherwise                                                                            -> FAIL, the one bit-flip exactly
"""
import json, sys, collections
from multiprocessing import get_context
sys.path.insert(0, sys.argv[1])
JOBS = int(sys.argv[2]) if len(sys.argv) > 2 else 8
import torture_campaign as t
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from arm_d4 import arms, grade, MASKS

def column(F, extra, ch):
    ev = []
    for cls, at, size, armch in arms(F):
        ev.append(dict(kind="flip", index=at, channel=armch, mask=size) if cls == "bit-flip"
                  else dict(kind="drop" if cls == "dropped" else "repeat", index=at, n=size))
    cap = t.synthesize_counter_capture(F, 4, events=ev + extra, byteorder="little")
    import array
    a = array.array("I", cap)
    return a[ch::4]

def shift_at(F, index):
    """The synthesizer's content shift in force at capture index `index` from the slip arms."""
    total = 0
    for cls, at, size, _ in arms(F):
        if cls != "bit-flip" and at <= index:
            total += size if cls == "dropped" else -size
    return total

def predict(F, ai, d, ch, mask):
    cls, at, size, armch = arms(F)[ai]
    s = at + d
    col = column(F, [dict(kind="flip", index=s, channel=ch, mask=mask)], ch)
    w = col[s]
    if cls == "bit-flip" and ch == armch and (d == 0 or (abs(d) == 1 and mask == size)):
        return "X2"
    tag = ch + 1
    true = s + shift_at(F, s)
    if cls != "bit-flip":
        old_pos, new_pos = s + shift_at(F, at - 1), s + shift_at(F, at)
    else:
        old_pos = new_pos = true
    track = any(q != true and t.audio_counter_word(tag, q) == w
                for base in {old_pos, new_pos} for q in range(base - 1024, base + 1025))
    if cls != "bit-flip" and d in (-1, 0) and track:
        return "X1"
    if w in (col[s - 1], col[s + 1]):
        return "L1"
    if cls != "bit-flip" and d in (0, 1):
        return "L2?"
    return "E"

def case(args):
    F, ai, d, ch, mask = args
    cls, at, size, armch = arms(F)[ai]
    s = at + d
    v, det = grade(F, [dict(kind="flip", index=s, channel=ch, mask=mask)])
    dut = [(e["channel"], e["capture_index"], e["class"], e["n"], e.get("mask")) for e in det["events"] if e["attribution"] == "dut"]
    missed = [a["index"] for a in det["planted_missed"]]
    exact = v == "FAIL" and not missed and dut == [(ch, s, "bit-flip", 1, f"0x{mask:08X}")]
    kind = predict(F, ai, d, ch, mask)
    if exact:
        outcome = "E"
    elif v == "NOT RUN" and missed == [at] and det["why"] == "void: a planted arm was missed":
        outcome = "VOID"
    elif v == "FAIL" and not missed and len(dut) == 2 and {x[2] for x in dut} == {"dropped", "repeated"} \
            and all(x[3] == 1 for x in dut) and [x[1] for x in dut] == [s, s + 1]:
        outcome = "PAIR"
    elif v == "FAIL" and not missed and len(dut) == 1 and dut[0][2] == "bit-flip" and dut[0][3] == 1:
        # byte identity: the reported corruption judged against the offset before the slip, the slip after it
        planted = [e for e in det["events"] if e["attribution"] == "planted" and e["channel"] == ch
                   and e["class"] == cls and abs(e["capture_index"] - at) <= 2]
        moved = planted[0]["capture_index"] if planted else None
        r, m2 = dut[0][1], int(dut[0][4], 16)
        actual = column(F, [dict(kind="flip", index=s, channel=ch, mask=mask)], ch)
        def alt_column():
            ev = []
            for c2, a2, size2, ch2 in arms(F):
                a3 = moved if (c2, a2) == (cls, at) else a2
                ev.append(dict(kind="flip", index=a3, channel=ch2, mask=size2) if c2 == "bit-flip"
                          else dict(kind="drop" if c2 == "dropped" else "repeat", index=a3, n=size2))
            cap = t.synthesize_counter_capture(F, 4, events=ev + [dict(kind="flip", index=r, channel=ch, mask=m2)],
                                               byteorder="little")
            import array
            return array.array("I", cap)[ch::4]
        same = moved is not None and r < moved and alt_column() == actual
        outcome = f"FLIP-ELSEWHERE+{moved - at}" if same else "FLIP-ELSEWHERE-NOT-IDENTICAL"
    else:
        outcome = "OTHER"
    return args, kind, outcome, v, missed, dut

if __name__ == "__main__":
    cases = [(F, ai, d, ch, m) for F in (8192, 16384) for ai in range(6) for d in range(-4, 5) for ch in range(4) for m in MASKS]
    with get_context("fork").Pool(JOBS) as pool:
        res = pool.map(case, cases, chunksize=16)
    table = collections.Counter((kind, outcome) for _, kind, outcome, *_ in res)
    for k in sorted(table): print("TABLE", k, table[k])
    for args, kind, outcome, v, missed, dut in res:
        want = {"X2": "VOID", "X1": "VOID", "L1": "PAIR", "L2?": "FLIP-ELSEWHERE", "E": "E"}[kind]
        if not (outcome == want or outcome == "E" or (kind == "L2?" and outcome.startswith("FLIP-ELSEWHERE+"))):
            print("MISMATCH", json.dumps({"case": args, "kind": kind, "outcome": outcome, "v": v, "missed": missed, "dut": dut[:4]}))
