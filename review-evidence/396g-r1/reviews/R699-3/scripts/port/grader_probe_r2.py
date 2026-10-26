#!/usr/bin/env python3
"""Round-2 independent probe of the #396 audio counter grader and release oracles.

Usage: python3 -I grader_probe_r2.py <path-to-tb/tools>

The round-1 probe (grader_probe.py) encodes the superseded 4096-sample
counter, so at the new head every one of its captures is a non-counter
signal. This script keeps the round-1 case list and op semantics unchanged
and swaps only the word encoder for the layout TESTING.md 6d now documents
(restated here, never calling the planner's encoder or synthesizer):
sample bits 15:12 = channel number, 11:1 = n mod 2048, bit 0 = bit (n mod 32)
of ((n div 2048) * 0x9E3779B1) mod 2^32; the sample sits in S32 bits 31:8.
New cases cover each round-2 item. One line per probe:
    <id> <OK|DEVIATION|INFO> <observed>
OK means the grader returned what the documented design and its stated
rules owe. Exit status is 0; the report reads the lines.
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

# Round-3 port, the only change: pass required_s, the capture's clean qualified
# length (frames - 2 * 63) / rate, so a short synthetic capture can PASS.
_grade = tc.grade_audio_counter_capture


def _ported(capture, layout, log, **kw):
    if not isinstance(capture, (bytes, bytearray)):
        capture = list(capture)
    size = len(capture) if isinstance(capture, (bytes, bytearray)) else sum(len(c) for c in capture)
    frames = size // (4 * layout.channels)
    kw.setdefault("required_s", max(frames - 126, 1) / layout.rate_hz)
    return _grade(capture, layout, log, **kw)


tc.grade_audio_counter_capture = _ported

RATE = 48000


def word(tag, n):
    code = ((n // 2048) * 0x9E3779B1) % 2**32
    sample = (tag << 12) | ((n % 2048) << 1) | ((code >> (n % 32)) & 1)
    return sample << 8


def build(frames, channels, ops, start=0):
    """ops act on a per-frame list of per-channel words.

    ('shift', index, k)      : from index on, source ordinal += k (drop k>0, repeat k<0)
    ('zero', index, n, ins)  : zero n frames; ins=True also delays content by n
    ('xor', index, ch, m)    : xor mask into one word
    ('swap', index, n, a, b) : exchange channels a and b for n frames
    ('copy', index, n, a, b) : channel a's word also on channel b for n frames
    ('chshift', index, ch, k): from index on, channel ch alone moves by k
    """
    shifts, chs = {}, {}
    zero = set()
    for op in ops:
        if op[0] == 'shift':
            shifts[op[1]] = shifts.get(op[1], 0) + op[2]
        elif op[0] == 'zero':
            zero.update(range(op[1], op[1] + op[2]))
            if op[3]:
                shifts[op[1]] = shifts.get(op[1], 0) - op[2]
        elif op[0] == 'chshift':
            chs.setdefault(op[2], {})[op[1]] = op[3]
    out, s = [], start
    per = {c: 0 for c in range(channels)}
    for i in range(frames):
        s += shifts.get(i, 0)
        for c in chs:
            per[c] += chs[c].get(i, 0)
        if i in zero:
            out.append([0] * channels)
        else:
            out.append([word(c + 1, i + s + per[c]) for c in range(channels)])
    for op in ops:
        if op[0] == 'xor':
            out[op[1]][op[2]] ^= op[3]
        elif op[0] == 'swap':
            _, i0, n, a, b = op
            for i in range(i0, min(frames, i0 + n)):
                out[i][a], out[i][b] = out[i][b], out[i][a]
        elif op[0] == 'copy':
            _, i0, n, a, b = op
            for i in range(i0, min(frames, i0 + n)):
                out[i][b] = out[i][a]
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


def grade(frames, channels, extra, *, losses=(), log=None, ops_arms=True, order='big', tags=None,
          anchors=(), steps=None, start=0, raw=None):
    ops, alog = arms_ops(frames) if ops_arms else ([], [])
    cap = raw if raw is not None else pack(build(frames, channels, ops + list(extra), start), order)
    layout = tc.CounterCapture(channels, order, RATE, 0.0, 0.0, 5, tags, tuple(anchors), steps)
    rlog = tc.CounterRunLog(alog if log is None else log, list(losses), 2)
    v, d = tc.grade_audio_counter_capture(cap, layout, rlog)
    dut = [(e["channel"], e["capture_index"], e["class"],
            e.get("n"), e.get("mask"), e.get("partner"), e.get("inserted"))
           for e in d.get("events", []) if e["attribution"] == "dut"]
    return v, d, dut


def line(pid, ok, observed):
    tag = ok if isinstance(ok, str) else ('OK' if ok else 'DEVIATION')
    print(f"{pid} {tag} {json.dumps(observed, default=str)}", flush=True)


def full(d):
    return [{k: e.get(k) for k in ("channel", "capture_index", "class", "n", "mask", "partner",
                                   "matches_channel", "located_within", "unresolved", "attribution")
             if e.get(k) is not None} for e in d.get("events", []) if e["attribution"] == "dut"]


F, C = 4 * 4096, 4
AT = 2 * 4096 + 13

# ---- Round-1 cases, same ops, new layout ------------------------------------------
for n in (1, 2, 5, 100, 2047):
    v, d, dut = grade(F, C, [('shift', AT, n)])
    line(f"P1-drop-{n}", v == "FAIL" and sorted(dut) == [(c, AT, "dropped", n, None, None, None) for c in range(C)], [v, dut[:2]])
for n in (1, 2, 7, 2048):
    v, d, dut = grade(F, C, [('shift', AT, -n)])
    ok = v == "FAIL" and sorted(e[:4] for e in dut) == [(c, AT, "repeated", n) for c in range(C)] if n != 2048 else \
        v == "FAIL" and sorted(e[2:4] for e in dut) == [("repeated", n)] * C
    line(f"P1-repeat-{n}", ok, [v, full(d)[:2]])
# Hold-one: c-1, c-1, c, c+1. Documented rule 3: 1 repeated then 1 dropped.
v, d, dut = grade(F, C, [('shift', AT, -1), ('shift', AT + 1, 1)])
line("P1-hold-one", v == "FAIL" and sorted(e[:4] for e in dut) == sorted(
    [(c, AT, "repeated", 1) for c in range(C)] + [(c, AT + 1, "dropped", 1) for c in range(C)]), [v, dut[:3]])

for n, ins in ((1, False), (6, False), (4095, False), (1, True), (6, True)):
    v, d, dut = grade(F, C, [('zero', AT, n, ins)])
    ok = v == "FAIL" and sorted(dut) == [(c, AT, "silence", n, None, None, ins) for c in range(C)]
    line(f"P2-silence-{n}-{'ins' if ins else 'rep'}", ok, [v, dut[:2]])

for mask in (0x100, 0x80000, 0x100000, 0x1, 0x80000000, 0x00F00F00, 0x0000FF00):
    v, d, dut = grade(F, C, [('xor', AT, 2, mask)])
    ok = v == "FAIL" and dut == [(2, AT, "bit-flip", 1, f"0x{mask:08X}", None, None)]
    line(f"P3-flip-{mask:#010x}", ok, [v, full(d)])
# Position bit 0 (word bit 9) at an odd position equals the previous sample: documented limit.
v, d, dut = grade(F, C, [('xor', AT, 2, 0x200)])
line("P3-flip-0x00000200-limit", "INFO", [v, full(d)])

for mask, n in ((0x1, 3), (0x80000000, 2), (0x100, 2), (0x100, 3), (0x200, 2)):
    v, d, dut = grade(F, C, [('xor', AT + k, 2, mask) for k in range(n)])
    ok = v == "FAIL" and len(dut) == 1 and dut[0][2] == "bit-flip" and dut[0][3] == n \
        and dut[0][4] == f"0x{mask:08X}"
    line(f"P4-burst-{mask:#010x}x{n}", ok, [v, full(d)])

v, d, dut = grade(F, C, [('swap', AT, 3, 0, 2)])
line("P5-swap-mid", v == "FAIL" and sorted(dut) == [(0, AT, "swap", 3, None, 2, None), (2, AT, "swap", 3, None, 0, None)], [v, dut])
v, d, dut = grade(F, C, [('swap', 0, F, 0, 2)], ops_arms=False, log=[])
line("P5-swap-from-start", v == "FAIL" and {e[2] for e in dut} == {"swap"}, [v, [e[:6] for e in dut]])
v, d, dut = grade(F, C, [('swap', F - 50, 50, 1, 3)])
line("P5-swap-to-end", v == "FAIL" and sorted(e[2] for e in dut) == ["swap", "swap"]
     and all(e[3] == 50 for e in dut), [v, dut])

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
v, d, dut = grade(F, C, mid_ops, ops_arms=False, log=mid_log)
line("P6-arms-only-mid-capture", v == "NOT RUN" and "tenth" in d["why"], [v, d.get("why")])
v, d, dut = grade(F, C, [('shift', 100 + 40, 3)])
line("P6-dut-drop-near-arm", v == "FAIL" and len(dut) == C, [v, dut[:1]])

v, d, dut = grade(F, C, [('shift', AT, 9)], losses=[{"index": AT, "frames": 9}])
line("P7-loss-attributed", v == "PASS" and d["counts"].get("capture") == {"dropped": C}, [v, d["counts"]])
v, d, dut = grade(F, C, [('shift', AT, 9), ('shift', AT + 500, 2)], losses=[{"index": AT, "frames": 9}])
line("P7-loss-plus-dut-drop", v == "FAIL" and len(dut) == C and all(e[3] == 2 for e in dut), [v, dut[:1]])
v, d, dut = grade(F, C, [], losses=[{"index": AT, "frames": 9}])
line("P7-logged-loss-absent", v == "NOT RUN", [v, d.get("why")])

v, d, dut = grade(F, C, [('shift', F - 1, 4)])
line("P8-drop-last-frame", v == "FAIL" and len(dut) == C and all(e[2] in ("dropped", "repeated") for e in dut),
     [v, full(d)[:1]])
v, d, dut = grade(F, C, [('shift', AT, 5)], order='little')
line("P8-little-endian-drop", v == "FAIL" and sorted(dut) == [(c, AT, "dropped", 5, None, None, None) for c in range(C)], [v, dut[:1]])
v, d, dut = grade(F, C, [('xor', AT, 0, 0x100)], tags=(1, 2, 3, 4))
line("P8-explicit-tags", v == "FAIL" and dut == [(0, AT, "bit-flip", 1, "0x00000100", None, None)], [v, dut])

# Round-1 follow-up cases (grader_probe2.py), same ops.
v, d, dut = grade(F, C, [('shift', AT, -1), ('shift', AT + 5, 1)])
line("Q-dup-then-skip-k5", v == "FAIL" and sorted(e[:4] for e in dut) == sorted(
    [(c, AT, "repeated", 1) for c in range(C)] + [(c, AT + 5, "dropped", 1) for c in range(C)]), [v, dut[:2]])
v, d, dut = grade(F, C, [('shift', AT, 1), ('shift', AT + 1, -1)])
line("Q-skip-then-dup-k1", v == "FAIL" and sorted(e[:4] for e in dut) == sorted(
    [(c, AT, "dropped", 1) for c in range(C)] + [(c, AT + 1, "repeated", 1) for c in range(C)]), [v, dut[:3]])
v, d, dut = grade(F, C, [('xor', AT, 2, 0x100000)])
line("Q-tag-flip-nonreciprocal", v == "FAIL" and [e[2] for e in dut] == ["bit-flip"]
     and full(d)[0].get("matches_channel") == 1, [v, full(d)])
for a, b in ((0, 2), (1, 3)):
    v, d, dut = grade(F, C, [('swap', 0, F, a, b)])
    ok = v == "FAIL" and sorted(e[:6] for e in dut) == [(a, 0, "swap", F, None, b), (b, 0, "swap", F, None, a)] \
        and not d["planted_missed"]
    line(f"Q-static-swap-{a}-{b}", ok, [v, d.get("why"), [e[:6] for e in dut], d["counts"].get("planted")])

# ---- New round-2 cases -----------------------------------------------------------
# (1) Non-repeating counter: whole-block slips are seen and sized exactly.
for n in (2048, 4096, 8192, 2048 * 37, 4096 * 1000):
    for sign, cls in ((1, "dropped"), (-1, "repeated")):
        v, d, dut = grade(F, C, [('shift', AT, sign * n)])
        ev = full(d)
        ok = v == "FAIL" and len(ev) == C and all(e["class"] == cls and e["n"] == n for e in ev) and all(
            e.get("located_within", [e["capture_index"]] * 2)[0] <= AT <= e.get("located_within", [0, e["capture_index"]])[1]
            and e["capture_index"] - AT < 64 for e in ev)
        line(f"B1-{cls}-{n}", ok, [v, ev[:1]])
# A run started deep in the period: acquisition decodes the absolute position.
v, d, dut = grade(F, C, [('shift', AT, 4096)], start=2**42 + 12345)
line("B2-late-start-block-slip", v == "FAIL" and all(e[2] == "dropped" and e[3] == 4096 for e in dut) and len(dut) == C,
     [v, full(d)[:1]])
# Period arithmetic stated in the docs.
line("B3-period", tc.AUDIO_PERIOD_FRAMES == 2**43 and tc.AUDIO_PERIOD_FRAMES > 24 * 3600 * 192000 * 500,
     {"period": tc.AUDIO_PERIOD_FRAMES, "days_at_192k": tc.AUDIO_PERIOD_FRAMES / 192000 / 86400,
      "run_24h_192k": 24 * 3600 * 192000, "run_24h_48k": 24 * 3600 * 48000})
# Encoder agreement with the independent restatement.
line("B4-encoder-agrees", all(tc.audio_counter_word(t, n) == word(t, n) for t in (1, 8, 15)
                              for n in list(range(0, 5000, 7)) + [2**43 - 1, 2**42 + 99]), "")

# (2) Tag integrity decides first.
v, d, dut = grade(F, C, [('copy', AT, 1, 0, 2)])
line("T1-copy-one-word", v == "FAIL" and [e["class"] for e in full(d)] == ["bit-flip"]
     and full(d)[0].get("matches_channel") == 0 and full(d)[0]["channel"] == 2, [v, full(d)])
v, d, dut = grade(F, C, [('copy', AT, 100, 0, 2)])
line("T2-copy-100-words", v == "FAIL" and [(e["class"], e["n"], e.get("matches_channel")) for e in full(d)]
     == [("bit-flip", 100, 0)], [v, full(d)])
v, d, dut = grade(F, C, [('xor', AT + k, 2, 0x100000) for k in range(100)])
line("T3-tag-flip-100-words", v == "FAIL" and [(e["class"], e["n"]) for e in full(d)] == [("bit-flip", 100)]
     and full(d)[0]["mask"] == "0x00100000", [v, full(d)])
v, d, dut = grade(F, C, [('swap', AT, 100, 0, 2)])
line("T4-swap-100", v == "FAIL" and sorted((e["channel"], e["class"], e["n"], e.get("partner")) for e in full(d))
     == [(0, "swap", 100, 2), (2, "swap", 100, 0)], [v, full(d)])
v, d, dut = grade(F, C, [('xor', AT, 2, 0x00F00000)])
line("T5-tag-to-unknown-number", v == "FAIL" and [(e["class"], e["n"]) for e in full(d)] == [("bit-flip", 1)], [v, full(d)])
# Swap where one side is also corrupted at one sample: that sample is not reciprocal.
v, d, dut = grade(F, C, [('swap', AT, 3, 0, 2), ('xor', AT + 1, 0, 0x100000)])
line("T6-swap-with-corrupt-side", "INFO", [v, full(d)])
# Tag flip one word on a channel that is statically swapped.
v, d, dut = grade(F, C, [('swap', 0, F, 0, 2), ('xor', AT, 1, 0x100000)])
line("T7-flip-on-static-swap-capture", "INFO", [v, d.get("why"), full(d)])

# (4)(5) capture losses advance the clocks; anchors interpolate.
anchors = [(4096, 4096 / RATE + 0.0, 100.0 + 4096 / RATE), (F, (F + 9) / RATE, 100.0 + (F + 9) / RATE)]
v, d, dut = grade(F, C, [('shift', AT, 9), ('shift', AT + 1000, 2)], losses=[{"index": AT, "frames": 9}],
                  anchors=anchors, steps=())
ev = [e for e in d["events"] if e["attribution"] == "dut"][0]
want_wall = (AT + 1000 + 9) / RATE
line("L1-event-after-loss-clock", v == "FAIL" and ev["acquisition_index"] == AT + 1000 + 9
     and abs(ev["wall_s"] - want_wall) < 1e-9 and ev["gptp_s"] is not None,
     {k: ev.get(k) for k in ("capture_index", "acquisition_index", "wall_s", "gptp_s", "timing")} | {"want_wall": want_wall})
cap_ev = [e for e in d["events"] if e["attribution"] == "capture"]
line("L2-loss-reported-apart", sorted(e["channel"] for e in cap_ev) == list(range(C))
     and d["counts"].get("capture") == {"dropped": C} and d["acquired_frames"] == F + 9,
     [d["counts"], d["acquired_frames"]])
v, d, dut = grade(F, C, [('shift', AT, 9)], losses=[{"index": AT, "frames": 9}],
                  anchors=[(4096, 4096 / RATE, 0.1)], steps=())
ev = [e for e in d["events"] if e["attribution"] == "capture"][0]
line("L3-no-anchor-after-event", ev["wall_s"] is None and "unsupported" in ev["timing"] and v == "PASS",
     [v, ev["timing"], d["timing_unsupported"]])
v, d, dut = grade(F, C, [('shift', AT, 2)], anchors=anchors, steps=(0.15,))
ev = full(d) and [e for e in d["events"] if e["attribution"] == "dut"][0]
line("L4-gptp-step-between-anchors", ev["gptp_s"] is None and ev["wall_s"] is not None, [ev["timing"]])
# Loss shown on only some counter channels (round-1 G07 survivor).
v, d, dut = grade(F, C, [('chshift', AT, 0, 9), ('chshift', AT, 1, 9)], losses=[{"index": AT, "frames": 9}])
line("L5-loss-on-two-of-four-channels", v == "NOT RUN" and "not in the capture" in d["why"], [v, d.get("why")])
# Loss of a whole-block size.
v, d, dut = grade(F, C, [('shift', AT, 4096)], losses=[{"index": AT, "frames": 4096}])
line("L6-loss-4096", v == "PASS" and d["counts"].get("capture") == {"dropped": C}, [v, d.get("why"), d["counts"]])
# Loss logged one frame off (tolerance 0 for losses).
v, d, dut = grade(F, C, [('shift', AT, 9)], losses=[{"index": AT + 1, "frames": 9}])
line("L7-loss-index-off-by-one", v == "NOT RUN", [v, d.get("why")])

# Edges.
v, d, dut = grade(F, C, [('zero', 0, 10, False)])
line("E1-leading-silence", "INFO", [v, full(d)[:1]])
v, d, dut = grade(F, C, [('shift', 10, 7)], ops_arms=True)
line("E2-drop-inside-acquisition", v == "FAIL" and all(e[2] == "dropped" and e[3] == 7 for e in dut) and len(dut) == C,
     [v, full(d)[:1]])
v, d, dut = grade(F, C, [('shift', F - 30, 4096)])
line("E3-block-slip-last-30", "INFO", [v, full(d)[:1]])
v, d, dut = grade(F, C, [('zero', F - 20, 20, False)])
line("E4-trailing-silence", v == "FAIL" and all(e[2] == "silence" and e[3] == 20 for e in dut), [v, full(d)[:1]])
edge = F // 10
for at, want in ((edge - 1, "PASS"), (edge, "NOT RUN")):
    ops = [('shift', at - 200, 3), ('shift', at - 100, -2), ('xor', at, 1, 0x100),
           ('shift', F - 900, 3), ('shift', F - 600, -2), ('xor', F - 300, 1, 0x100)]
    log = [{"class": "dropped", "index": at - 200, "n": 3}, {"class": "repeated", "index": at - 100, "n": 2},
           {"class": "bit-flip", "index": at, "mask": 0x100, "channel": 1}] + arms_ops(F)[1][3:]
    v, d, dut = grade(F, C, ops, ops_arms=False, log=log)
    line(f"E5-flip-arm-at-{at}-of-edge-{edge}", v == want, [v, d.get("why")])

# Per-channel fast path and a channel without the counter.
w = build(F, C, arms_ops(F)[0])
for i in range(F):
    w[i][3] = (i * 2654435761) & 0xFFFFFF00
v, d, dut = grade(F, C, [], raw=pack(w), tags=(1, 2, 3, None))
line("M1-non-counter-channel", v == "PASS", [v, d.get("why")])

# Throughput: clean, one-channel offset, non-counter garbage (8 channels, 1 MiB chunks).
def tp(name, frames, mutate=None):
    w = build(frames, 8, [])
    if mutate:
        mutate(w)
    cap = pack(w)
    t0 = time.monotonic()
    v, d = tc.grade_audio_counter_capture([cap[i:i + (1 << 20)] for i in range(0, len(cap), 1 << 20)],
                                          tc.CounterCapture(8, "big", RATE, 0.0, 0.0),
                                          tc.CounterRunLog([], [], 0))
    dt = time.monotonic() - t0
    print(f"P9-{name} INFO {json.dumps({'verdict': v, 'seconds_audio': frames / RATE, 'grade_s': round(dt, 3), 'x_realtime': round(frames / RATE / dt, 2)})}", flush=True)


tp("clean", RATE * 20)


def offset(w):
    for i in range(100, len(w)):
        w[i][3] = word(4, i + 7)


tp("one-channel-offset", RATE * 20, offset)


def garbage(w):
    for i in range(len(w)):
        w[i][5] = (i * 2654435761) & 0xFFFFFF00


tp("one-channel-non-counter", RATE * 2, garbage)


# ---- Release oracles ------------------------------------------------------------
def rd(t, ts, **v):
    base = dict(SEQ_NUM_MISMATCH=0, STREAM_INTERRUPTED=0, LATE_TIMESTAMP=0, EARLY_TIMESTAMP=0, MEDIA_UNLOCKED=0)
    base.update(v)
    return {"target": t, "timestamp_s": ts, "values": base}


W = [{"target": "a", "kind": "gm", "window_s": (10, 20)}]
cases = [
    ("S1-clean", [rd("a", 0), rd("a", 60), rd("crf", 0), rd("crf", 60)], [], ["a", "crf"], "PASS"),
    ("S2-crf-early", [rd("a", 0), rd("a", 60), rd("crf", 0), rd("crf", 60, EARLY_TIMESTAMP=1)], [], ["a", "crf"], "FAIL"),
    ("S3-unlock-other-input-event", [rd("a", 0), rd("a", 60, MEDIA_UNLOCKED=1)],
     [{"target": "b", "kind": "gm", "window_s": (10, 20)}], ["a"], "FAIL"),
    # Round-1 S4 as written: reads 0 and 60 s around a 10-20 s window. Item (4) now refuses it.
    ("S4-unlock-planted-periodic-interval", [rd("a", 0), rd("a", 60, MEDIA_UNLOCKED=1)], W, ["a"], "FAIL"),
    ("S4b-unlock-planted-edge-reads", [rd("a", 0), rd("a", 10), rd("a", 20, MEDIA_UNLOCKED=1), rd("a", 60, MEDIA_UNLOCKED=1)],
     W, ["a"], "PASS"),
    ("S4c-unlock-after-window", [rd("a", 0), rd("a", 10), rd("a", 20), rd("a", 60, MEDIA_UNLOCKED=1)], W, ["a"], "FAIL"),
    ("S4d-unlock-before-window", [rd("a", 0), rd("a", 10, MEDIA_UNLOCKED=1), rd("a", 20, MEDIA_UNLOCKED=1)], W, ["a"], "FAIL"),
    ("S4e-two-unlocks-one-event", [rd("a", 0), rd("a", 10), rd("a", 15, MEDIA_UNLOCKED=1), rd("a", 20, MEDIA_UNLOCKED=2)],
     W, ["a"], "FAIL"),
    ("S5-seq-in-planted", [rd("a", 0), rd("a", 10), rd("a", 20, SEQ_NUM_MISMATCH=1)], W, ["a"], "FAIL"),
    ("S6-missing-crf-series", [rd("a", 0), rd("a", 60)], [], ["a", "crf"], "NOT RUN"),
    ("S7-wrap-is-reset", [rd("a", 0, MEDIA_UNLOCKED=2**32 - 1), rd("a", 10), rd("a", 20, MEDIA_UNLOCKED=0)],
     W, ["a"], "FAIL"),
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
CUT = tc.ReleaseCommitCut(new, (5.0, 5.4), 5.1)
half = {i: (new[i] if k % 2 else pre[i]) for k, i in enumerate(items)}
v, d = tc.check_release_state_restored(pre, half, dflt, items=items, phase="journal_commit", committed=CUT)
line("R2-commit-mixed", v == "FAIL", [v, d.get("why")])
v, d = tc.check_release_state_restored(pre, new, dflt, items=items, phase="journal_commit", committed=new)
line("R3-commit-new-bare-dict", v == "NOT RUN", [v, d.get("why")])
v, d = tc.check_release_state_restored(pre, new, dflt, items=items, phase="journal_commit", committed=CUT)
line("R3b-commit-new-with-cut", v == "PASS", [v, d.get("restored")])
v, d = tc.check_release_state_restored(pre, dflt, dflt, items=items, phase="journal_commit", committed=CUT)
line("R4-commit-reverted", v == "FAIL", [v, d.get("why")])
# (3) pending at default; cut outside the window; soft reset with a cut (round-1 R03 survivor).
v, d = tc.check_release_state_restored(pre, dflt, dflt, items=items, phase="journal_commit",
                                       committed=tc.ReleaseCommitCut(dflt, (5.0, 5.4), 5.1))
line("R5-pending-all-default", v == "NOT RUN" and d.get("pending_at_default") == items, [v, d.get("why")])
one = dict(new, **{items[3]: dflt[items[3]]})
v, d = tc.check_release_state_restored(pre, one, dflt, items=items, phase="journal_commit",
                                       committed=tc.ReleaseCommitCut(one, (5.0, 5.4), 5.1))
line("R6-pending-one-default", v == "NOT RUN" and d.get("pending_at_default") == [items[3]], [v, d.get("why")])
for cut_s in (4.99, 5.4, 9.0):
    v, d = tc.check_release_state_restored(pre, new, dflt, items=items, phase="journal_commit",
                                           committed=tc.ReleaseCommitCut(new, (5.0, 5.4), cut_s))
    line(f"R7-cut-outside-{cut_s}", v == "NOT RUN" and d.get("why") == "the cut hit no journal commit", [v, d.get("why")])
v, d = tc.check_release_state_restored(pre, pre, dflt, items=items, phase="journal_commit",
                                       committed=tc.ReleaseCommitCut(new, (5.0, 5.4), 9.0))
line("R7b-old-snapshot-cut-outside", v == "NOT RUN" and d.get("why") == "the cut hit no journal commit", [v, d.get("why")])
for phase in ("soft_reset", "idle"):
    v, d = tc.check_release_state_restored(pre, new, dflt, items=items, phase=phase, committed=CUT)
    line(f"R8-{phase}-with-cut-new-readback", v == "FAIL", [v, d.get("why")])
    v, d = tc.check_release_state_restored(pre, new, dflt, items=items, phase=phase, committed=new)
    line(f"R8b-{phase}-with-dict-new-readback", v == "FAIL", [v, d.get("why")])
v, d = tc.check_release_state_restored(pre, new, dflt, items=items, phase="journal_commit",
                                       committed=tc.ReleaseCommitCut(new, (5.0, 5.4), True))
line("R9-cut-instant-bool", v == "NOT RUN", [v, d.get("why")])
