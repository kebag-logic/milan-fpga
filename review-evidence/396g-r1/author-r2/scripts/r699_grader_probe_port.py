#!/usr/bin/env python3
"""Independent probe of the #396 audio counter grader and release oracles.

Usage: python3 -I grader_probe.py <path-to-tb/tools>

Builds counter captures with its own generator (it never calls the
planner's synthesize_counter_capture), grades them with the planner's
grade_audio_counter_capture, and prints one line per probe:
    <id> <OK|DEVIATION> <observed>
OK means the grader returned the classification the signal design owes.
Exit status is 0; the report reads the lines.
"""
import importlib.util
import json
import struct
import sys
import time

spec = importlib.util.spec_from_file_location("tc", sys.argv[1] + "/torture_campaign.py")
tc = importlib.util.module_from_spec(spec)
sys.modules["tc"] = tc
spec.loader.exec_module(tc)

RATE = 48000


def word(tag, counter):
    """Port to the round-2 layout (TESTING.md 6d): sample bits 15:12 = tag,
    11:1 = position mod 2048, 0 = bit (n mod 32) of (n div 2048) * 0x9E3779B1
    mod 2^32. The only change to the reviewer's script."""
    code = ((counter // 2048) * 0x9E3779B1) % 2**32
    sample = (tag << 12) | ((counter % 2048) << 1) | ((code >> (counter % 32)) & 1)
    return sample << 8


def build(frames, channels, ops):
    """ops act on a per-frame list of per-channel words.

    ('shift', index, k)    : from index on, source ordinal += k (drop k>0, repeat k<0)
    ('zero', index, n, ins): zero n frames; ins=True also delays content by n
    ('xor', index, ch, m)  : xor mask into one word
    ('swap', index, n, a, b): exchange channels a and b for n frames
    """
    shifts = {}
    zero = set()
    for op in ops:
        if op[0] == 'shift':
            shifts[op[1]] = shifts.get(op[1], 0) + op[2]
        elif op[0] == 'zero':
            zero.update(range(op[1], op[1] + op[2]))
            if op[3]:
                shifts[op[1]] = shifts.get(op[1], 0) - op[2]
    out, s = [], 0
    for i in range(frames):
        s += shifts.get(i, 0)
        if i in zero:
            out.append([0] * channels)
        else:
            out.append([word(c + 1, i + s) for c in range(channels)])
    for op in ops:
        if op[0] == 'xor':
            out[op[1]][op[2]] ^= op[3]
        elif op[0] == 'swap':
            _, i0, n, a, b = op
            for i in range(i0, i0 + n):
                out[i][a], out[i][b] = out[i][b], out[i][a]
    return out


def pack(frames_words, order='big'):
    fmt = ('>' if order == 'big' else '<') + 'I' * len(frames_words[0])
    return b''.join(struct.pack(fmt, *f) for f in frames_words)


def arms_ops(frames):
    """Planted arms at both ends: drop 3, repeat 2, flip 0x100 on channel 1."""
    ops = [('shift', 100, 3), ('shift', 300, -2), ('xor', 500, 1, 0x100),
           ('shift', frames - 900, 3), ('shift', frames - 600, -2), ('xor', frames - 300, 1, 0x100)]
    log = [{"class": "dropped", "index": 100, "n": 3}, {"class": "repeated", "index": 300, "n": 2},
           {"class": "bit-flip", "index": 500, "mask": 0x100, "channel": 1},
           {"class": "dropped", "index": frames - 900, "n": 3},
           {"class": "repeated", "index": frames - 600, "n": 2},
           {"class": "bit-flip", "index": frames - 300, "mask": 0x100, "channel": 1}]
    return ops, log


def grade(frames, channels, extra, *, losses=(), log=None, ops_arms=True, order='big', tags=None):
    ops, alog = arms_ops(frames) if ops_arms else ([], [])
    cap = pack(build(frames, channels, ops + list(extra)), order)
    layout = tc.CounterCapture(channels, order, RATE, 0.0, 0.0, 5, tags)
    rlog = tc.CounterRunLog(alog if log is None else log, list(losses), 2)
    v, d = tc.grade_audio_counter_capture(cap, layout, rlog)
    dut = [(e["channel"], e["capture_index"], e["class"],
            e.get("n"), e.get("mask"), e.get("partner"), e.get("inserted"))
           for e in d.get("events", []) if e["attribution"] == "dut"]
    return v, d, dut


def line(pid, ok, observed):
    print(f"{pid} {'OK' if ok else 'DEVIATION'} {json.dumps(observed, default=str)}")


F, C = 4 * 4096, 4
AT = 2 * 4096 + 13

# Slips on every channel.
for n in (1, 2, 5, 100, 2047):
    v, d, dut = grade(F, C, [('shift', AT, n)])
    line(f"P1-drop-{n}", v == "FAIL" and sorted(dut) == [(c, AT, "dropped", n, None, None, None) for c in range(C)], [v, dut[:2]])
for n in (1, 2, 7, 2048):
    v, d, dut = grade(F, C, [('shift', AT, -n)])
    line(f"P1-repeat-{n}", v == "FAIL" and sorted(dut) == [(c, AT, "repeated", n, None, None, None) for c in range(C)], [v, dut[:2]])
# Hold-one repeat with no lasting shift: c-1, c-1, c, c+1.
v, d, dut = grade(F, C, [('shift', AT, -1), ('shift', AT + 1, 1)])
line("P1-hold-one", v == "FAIL" and {e[2] for e in dut} == {"repeated"} and all(e[3] == 1 for e in dut) and len(dut) == C, [v, dut])

# Silence.
for n, ins in ((1, False), (6, False), (4095, False), (1, True), (6, True)):
    v, d, dut = grade(F, C, [('zero', AT, n, ins)])
    ok = v == "FAIL" and sorted(dut) == [(c, AT, "silence", n, None, None, ins) for c in range(C)]
    line(f"P2-silence-{n}-{'ins' if ins else 'rep'}", ok, [v, dut[:2]])

# Single-word corruption.
for mask in (0x100, 0x80000, 0x100000, 0x1, 0x80000000, 0x00F00F00, 0x0000FF00):
    v, d, dut = grade(F, C, [('xor', AT, 2, mask)])
    ok = v == "FAIL" and dut == [(2, AT, "bit-flip", 1, f"0x{mask:08X}", None, None)]
    line(f"P3-flip-{mask:#010x}", ok, [v, dut])

# Multi-word corruption bursts (a bit-corruption mask over consecutive samples).
for mask, n in ((0x1, 3), (0x80000000, 2), (0x100, 2), (0x100, 3), (0x200, 2)):
    v, d, dut = grade(F, C, [('xor', AT + k, 2, mask) for k in range(n)])
    ok = v == "FAIL" and len(dut) == 1 and dut[0][2] == "bit-flip" and dut[0][3] == n \
        and dut[0][4] == f"0x{mask:08X}"
    line(f"P4-burst-{mask:#010x}x{n}", ok, [v, dut])

# Channel swap: mid-run, from capture start, to capture end.
v, d, dut = grade(F, C, [('swap', AT, 3, 0, 2)])
line("P5-swap-mid", v == "FAIL" and sorted(dut) == [(0, AT, "swap", 3, None, 2, None), (2, AT, "swap", 3, None, 0, None)], [v, dut])
v, d, dut = grade(F, C, [('swap', 0, F, 0, 2)], ops_arms=False, log=[])
line("P5-swap-from-start", v == "FAIL" and {e[2] for e in dut} == {"swap"}, [v, [e[:4] for e in dut]])
v, d, dut = grade(F, C, [('swap', F - 50, 50, 1, 3)])
line("P5-swap-to-end", v == "FAIL" and sorted(e[2] for e in dut) == ["swap", "swap"], [v, dut])

# Planted-arm logic.
v, d, dut = grade(F, C, [])
line("P6-clean-with-arms", v == "PASS" and not dut, [v, d.get("why")])
ops, log = arms_ops(F)
v, d, dut = grade(F, C, [], log=log + [{"class": "dropped", "index": 7000, "n": 4}])
line("P6-missed-arm-voids", v == "NOT RUN" and "void" in d["why"], [v, d.get("why")])
v, d, dut = grade(F, C, [('shift', AT, 5)], log=log + [{"class": "dropped", "index": 7000, "n": 4}])
line("P6-missed-arm-with-dut-event-still-void", v == "NOT RUN", [v, d.get("why")])
mid = F // 2
mid_ops = [('shift', mid - 300, 3), ('shift', mid - 200, -2), ('xor', mid - 100, 1, 0x100),
           ('shift', mid + 100, 3), ('shift', mid + 200, -2), ('xor', mid + 300, 1, 0x100)]
mid_log = [{"class": "dropped", "index": mid - 300, "n": 3}, {"class": "repeated", "index": mid - 200, "n": 2},
           {"class": "bit-flip", "index": mid - 100, "mask": 0x100, "channel": 1},
           {"class": "dropped", "index": mid + 100, "n": 3}, {"class": "repeated", "index": mid + 200, "n": 2},
           {"class": "bit-flip", "index": mid + 300, "mask": 0x100, "channel": 1}]
cap = pack(build(F, C, mid_ops))
v, d = tc.grade_audio_counter_capture(cap, tc.CounterCapture(C, "big", RATE, 0.0, 0.0),
                                      tc.CounterRunLog(mid_log, [], 2))
# Observation, not a pass/fail of the design: arms clustered mid-capture.
print(f"P6-arms-only-mid-capture INFO {json.dumps([v, d.get('why')])}")
# A DUT drop of the arm's size just outside tolerance is DUT-attributed.
v, d, dut = grade(F, C, [('shift', 100 + 40, 3)])
line("P6-dut-drop-near-arm", v == "FAIL" and len(dut) == C, [v, dut[:1]])

# Capture-side losses.
v, d, dut = grade(F, C, [('shift', AT, 9)], losses=[{"index": AT, "frames": 9}])
line("P7-loss-attributed", v == "PASS" and d["counts"].get("capture") == {"dropped": C}, [v, d["counts"]])
v, d, dut = grade(F, C, [('shift', AT, 9), ('shift', AT + 500, 2)], losses=[{"index": AT, "frames": 9}])
line("P7-loss-plus-dut-drop", v == "FAIL" and len(dut) == C and all(e[3] == 2 for e in dut), [v, dut[:1]])
v, d, dut = grade(F, C, [], losses=[{"index": AT, "frames": 9}])
line("P7-logged-loss-absent", v == "NOT RUN", [v, d.get("why")])

# Edges: event at the very first and last frames; little endian; a non-counter channel.
v, d, dut = grade(F, C, [('shift', F - 1, 4)])
line("P8-drop-last-frame", v == "FAIL" and len(dut) == C and all(e[2] in ("dropped", "repeated") for e in dut), [v, dut[:1]])
v, d, dut = grade(F, C, [('shift', AT, 5)], order='little')
line("P8-little-endian-drop", v == "FAIL" and sorted(dut) == [(c, AT, "dropped", 5, None, None, None) for c in range(C)], [v, dut[:1]])
v, d, dut = grade(F, C, [('xor', AT, 0, 0x100)], tags=(1, 2, 3, 4))
line("P8-explicit-tags", v == "FAIL" and dut == [(0, AT, "bit-flip", 1, "0x00000100", None, None)], [v, dut])

# Throughput of the clean fast path, eight channels, to bound a 24 h grade.
frames = 48000 * 20
cap = pack(build(frames, 8, []))
t0 = time.monotonic()
v, d = tc.grade_audio_counter_capture([cap[i:i + 1 << 20] for i in range(0, len(cap), 1 << 20)],
                                      tc.CounterCapture(8, "big", RATE, 0.0, 0.0),
                                      tc.CounterRunLog([], [], 0))
dt = time.monotonic() - t0
print(f"P9-throughput INFO {json.dumps({'verdict': v, 'seconds_audio': 20, 'grade_s': round(dt, 3), 'x_realtime': round(20 / dt, 1)})}")
# After a one-channel persistent offset the fast path is unavailable.
frames = 48000 * 2
ops = [('xor', 10, 0, 0x100)]
w = build(frames, 8, [])
for i in range(100, frames):
    w[i][3] = word(4, i + 7)
cap = pack(w)
t0 = time.monotonic()
v, d = tc.grade_audio_counter_capture(cap, tc.CounterCapture(8, "big", RATE, 0.0, 0.0), tc.CounterRunLog([], [], 0))
dt = time.monotonic() - t0
print(f"P9-slow-path INFO {json.dumps({'verdict': v, 'seconds_audio': 2, 'grade_s': round(dt, 3), 'x_realtime': round(2 / dt, 2)})}")

# Release oracles: soak counters and state restore, independent cases.
def rd(t, ts, **v):
    base = dict(SEQ_NUM_MISMATCH=0, STREAM_INTERRUPTED=0, LATE_TIMESTAMP=0, EARLY_TIMESTAMP=0, MEDIA_UNLOCKED=0)
    base.update(v)
    return {"target": t, "timestamp_s": ts, "values": base}

cases = [
    ("S1-clean", [rd("a", 0), rd("a", 60), rd("crf", 0), rd("crf", 60)], [], ["a", "crf"], "PASS"),
    ("S2-crf-early", [rd("a", 0), rd("a", 60), rd("crf", 0), rd("crf", 60, EARLY_TIMESTAMP=1)], [], ["a", "crf"], "FAIL"),
    ("S3-unlock-other-input-event", [rd("a", 0), rd("a", 60, MEDIA_UNLOCKED=1)],
     [{"target": "b", "kind": "gm", "window_s": (10, 20)}], ["a"], "FAIL"),
    ("S4-unlock-planted", [rd("a", 0), rd("a", 60, MEDIA_UNLOCKED=1)],
     [{"target": "a", "kind": "gm", "window_s": (10, 20)}], ["a"], "PASS"),
    ("S5-seq-in-planted", [rd("a", 0), rd("a", 60, SEQ_NUM_MISMATCH=1)],
     [{"target": "a", "kind": "gm", "window_s": (10, 20)}], ["a"], "FAIL"),
    ("S6-missing-crf-series", [rd("a", 0), rd("a", 60)], [], ["a", "crf"], "NOT RUN"),
    ("S7-wrap-is-reset", [rd("a", 0, MEDIA_UNLOCKED=2**32 - 1), rd("a", 60, MEDIA_UNLOCKED=0)],
     [{"target": "a", "kind": "gm", "window_s": (10, 20)}], ["a"], "FAIL"),
]
for pid, reads, planted, targets, want in cases:
    v, d = tc.check_release_soak_counters(reads, planted, targets=targets, capture_complete=True)
    line(pid, v == want, [v, d.get("why")])

items = list(tc.RELEASE_PERSISTED_ITEMS)
pre = {i: f"set-{i}" for i in items}
dflt = {i: f"dflt-{i}" for i in items}
for k, item in enumerate(items):
    post = dict(pre, **{item: f"other-{item}"})
    v, d = tc.check_release_state_restored(pre, post, dflt, items=items, phase="soft_reset")
    line(f"R1-wrong-{item}", v == "FAIL" and d["differs"] == [item], [v])
new = {i: f"new-{i}" for i in items}
half = {i: (new[i] if k % 2 else pre[i]) for k, i in enumerate(items)}
v, d = tc.check_release_state_restored(pre, half, dflt, items=items, phase="journal_commit", committed=new)
line("R2-commit-mixed", v == "FAIL", [v, d.get("why")])
v, d = tc.check_release_state_restored(pre, new, dflt, items=items, phase="journal_commit", committed=new)
line("R3-commit-new", v == "PASS", [v])
v, d = tc.check_release_state_restored(pre, dflt, dflt, items=items, phase="journal_commit", committed=new)
line("R4-commit-reverted", v == "FAIL", [v, d.get("why")])
