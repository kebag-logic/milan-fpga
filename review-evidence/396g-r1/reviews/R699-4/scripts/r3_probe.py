#!/usr/bin/env python3
"""Round-3 independent probe of the #396 audio counter grader's boundary rules.

Usage: python3 -I r3_probe.py <path-to-tb/tools> [jobs]

The words are built here from the layout TESTING.md 6d documents, never with
the planner's encoder or synthesizer: sample bits 15:12 = channel number,
11:1 = n mod 2048, bit 0 = bit (n mod 32) of ((n div 2048) * 0x9E3779B1) mod
2^32, the sample in S32 bits 31:8. Every case passes `required_s` explicitly.
One line per case:  <id> <OK|DEVIATION|INFO> <observed>
A summary line per group counts OK and DEVIATION. Exit status is 0.
"""
import importlib.util
import json
import struct
import sys
from multiprocessing import Pool

TOOLS = sys.argv[1]
JOBS = int(sys.argv[2]) if len(sys.argv) > 2 else 8
RATE, C = 48000, 4
_tc = None


def tc():
    global _tc
    if _tc is None:
        spec = importlib.util.spec_from_file_location("tc", TOOLS + "/torture_campaign.py")
        _tc = importlib.util.module_from_spec(spec)
        sys.modules["tc"] = _tc
        spec.loader.exec_module(_tc)
    return _tc


def word(tag, n):
    code = ((n // 2048) * 0x9E3779B1) % 2**32
    return ((tag << 12) | ((n % 2048) << 1) | ((code >> (n % 32)) & 1)) << 8


def build(frames, ops):
    """ops: ('shift', i, k[, ch]) source += k from i on; ('xor', i, ch, mask)."""
    deltas = [{} for _ in range(C)]
    for op in ops:
        if op[0] == "shift":
            for c in (range(C) if len(op) < 4 else (op[3],)):
                deltas[c][op[1]] = deltas[c].get(op[1], 0) + op[2]
    cols = []
    for c in range(C):
        marks = sorted({0, frames} | {i for i in deltas[c] if 0 < i < frames})
        shift, col = deltas[c].get(0, 0), []
        for a, b in zip(marks, marks[1:]):
            if a:
                shift += deltas[c].get(a, 0)
            col += [word(c + 1, i + shift) for i in range(a, b)]
        cols.append(col)
    out = [list(f) for f in zip(*cols)]
    for op in ops:
        if op[0] == "xor":
            out[op[1]][op[2]] ^= op[3]
    return out


def arms(frames):
    ops = [("shift", 300, 3), ("shift", 500, -2), ("xor", 700, 1, 0x100),
           ("shift", frames - 700, 3), ("shift", frames - 450, -2), ("xor", frames - 200, 1, 0x100)]
    log = [{"class": "dropped", "index": 300, "n": 3}, {"class": "repeated", "index": 500, "n": 2},
           {"class": "bit-flip", "index": 700, "mask": 0x100, "channel": 1},
           {"class": "dropped", "index": frames - 700, "n": 3},
           {"class": "repeated", "index": frames - 450, "n": 2},
           {"class": "bit-flip", "index": frames - 200, "mask": 0x100, "channel": 1}]
    return ops, log


def grade(frames, ops, *, planted=True, order="big", chunk=None, required_s=None):
    t = tc()
    aops, alog = arms(frames) if planted else ([], [])
    out = build(frames, aops + list(ops))
    cap = struct.pack(("<" if order == "little" else ">") + "I" * (C * frames), *(w for f in out for w in f))
    if chunk:
        cap = [cap[i:i + chunk] for i in range(0, len(cap), chunk)]
    req = (frames - 126) / RATE if required_s is None else required_s
    v, d = t.grade_audio_counter_capture(cap, t.CounterCapture(C, order, RATE, 0.0, 0.0),
                                         t.CounterRunLog(alog, [], 2), required_s=req)
    dut = [e for e in d.get("events", []) if e["attribution"] == "dut"]
    return v, d, dut


def brief(e):
    return {k: e.get(k) for k in ("channel", "capture_index", "class", "n", "mask", "located_within", "unresolved")
            if e.get(k) is not None}


OPTS = (("big", None), ("little", None), ("big", 113), ("little", 7))
SIZES = (2048, -2048, 4096, -4096, 8192, 6144 * 1024)


# ---- E: a whole-block slip near the capture's end -----------------------------------
def case_end(args):
    back, n, order, chunk = args
    F = 8192
    at = F - back
    v, d, dut = grade(F, [("shift", at, n)], order=order, chunk=chunk)
    q = d.get("qualified") or {}
    start, end = q.get("start"), q.get("end")
    ok = end == F - 63 and start == 63
    if not dut:
        ok = ok and v == "PASS" and at >= end
    else:
        ok = ok and v == "FAIL" and len(dut) == C
        for e in dut:
            lo, hi = e.get("located_within", (e["capture_index"],) * 2)
            if not lo <= at <= hi:
                ok = False
            if e["class"] == "unresolved":
                ok = ok and e["mask"] == "0x00000100" and e["capture_index"] + e["n"] == F and at >= end
            elif e["class"] in ("dropped", "repeated"):
                ok = ok and e["n"] == abs(n) and e["class"] == ("dropped" if n > 0 else "repeated") \
                    and not e.get("unresolved") and at < end
            else:
                ok = False
    return (f"E-{n}-at-F-{back}-{order}-{chunk}", ok,
            [v, [start, end], sorted({(e["class"], e.get("n")) for e in dut})])


# ---- S: a whole-block slip near the capture's start -----------------------------------
def case_start(args):
    at, n, order, chunk = args
    F = 8192
    v, d, dut = grade(F, [("shift", at, n)], order=order, chunk=chunk)
    q = d.get("qualified") or {}
    start = q.get("start")
    ok = q.get("end") == F - 63
    if not dut:
        ok = ok and v == "PASS" and at < start
    else:
        ok = ok and v == "FAIL" and len(dut) == C
        for e in dut:
            lo, hi = e.get("located_within", (e["capture_index"],) * 2)
            if not lo <= at <= hi:
                ok = False
            if e["class"] == "unresolved":
                ok = ok and e["unresolved"].startswith("before acquisition") and e["mask"] == "0x00000100" \
                    and at < start
            elif e["class"] in ("dropped", "repeated"):
                ok = ok and e["n"] == abs(n) and not e.get("unresolved")
            else:
                ok = False
    return (f"S-{n}-at-{at}-{order}-{chunk}", ok,
            [v, start, sorted({(e["class"], e.get("n")) for e in dut})])


# ---- M: one constant mask over an interior excursion, every length ------------------
def case_mask(args):
    mask, at, n, order, chunk = args
    F = 16384
    v, d, dut = grade(F, [("xor", at + k, 2, mask) for k in range(n)], order=order, chunk=chunk)
    got = [(e["channel"], e["capture_index"], e["class"], e["n"], e.get("mask")) for e in dut]
    ok = v == "FAIL" and got == [(2, at, "bit-flip", n, f"0x{mask:08X}")] and d["planted_missed"] == []
    return f"M-0x{mask:X}-at-{at}-n-{n}-{order}-{chunk}", ok, [v, got[:4]]


# ---- A: DUT events beside the planted arms ------------------------------------------
def case_arm(args):
    name, ops, want = args
    F = 16384
    v, d, dut = grade(F, ops)
    got = sorted((e["channel"], e["capture_index"], e["class"], e["n"]) for e in dut)
    ok = v == "FAIL" and d["planted_missed"] == [] and got == sorted(want)
    return f"A-{name}", ok, [v, d["why"], d["planted_missed"], got[:8]]


def jobs():
    yield "E", case_end, [(b, n, o, c) for b in list(range(1, 71)) + [100, 150] for n in SIZES
                          for o, c in (OPTS if n == 4096 else OPTS[:1])]
    yield "S", case_start, [(a, n, o, c) for a in list(range(1, 131)) for n in SIZES
                            for o, c in (OPTS if n == 4096 else OPTS[:1])]
    masks = (0x100, 0x80000, 0x40000, 0x200, 0x00F00F00, 0x80100, 0x1)
    yield "M", case_mask, [(m, at, n, o, c) for m in masks for at in (3000, 4090, 6143)
                           for n in (2, 63, 64, 65, 127, 128, 1000, 2047, 2048, 2049, 4097)
                           for o, c in ((OPTS[0], OPTS[3]) if n in (64, 2049) else OPTS[:1])]
    arm_cases = []
    for gap in (5, 40, 200, 900):
        for arm_at, label in ((300, "drop"), (500, "repeat"), (700, "flip")):
            at = arm_at - gap
            if at > 70:
                arm_cases.append((f"drop1024-{gap}-before-{label}", [("shift", at, 1024)],
                                  [(c, at, "dropped", 1024) for c in range(C)]))
        for arm_at, label in ((300, "drop"), (500, "repeat"), (700, "flip")):
            at = arm_at + gap
            arm_cases.append((f"drop4096-{gap}-after-{label}", [("shift", at, 4096)],
                              [(c, at, "dropped", 4096) for c in range(C)]))
    for ch in (0, 1):
        for start, label in ((595, "ends-5-before-flip"), (705, "starts-5-after-flip"),
                             (450, "spans-repeat"), (16384 - 800, "ends-100-before-end-drop")):
            arm_cases.append((f"ch{ch}-0x80000x100-{label}", [("xor", start + k, ch, 0x80000) for k in range(100)],
                              [(ch, start, "bit-flip", 100)]))
    yield "A", case_arm, arm_cases


def main():
    with Pool(JOBS) as pool:
        for group, fn, cases in jobs():
            ok = dev = 0
            for pid, good, observed in pool.map(fn, cases, chunksize=4):
                tag = good if isinstance(good, str) else ("OK" if good else "DEVIATION")
                ok, dev = ok + (tag == "OK"), dev + (tag == "DEVIATION")
                print(f"{pid} {tag} {json.dumps(observed, default=str)}", flush=True)
            print(f"SUMMARY {group} OK={ok} DEVIATION={dev}", flush=True)


if __name__ == "__main__":
    main()
