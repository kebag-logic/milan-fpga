#!/usr/bin/env python3
"""Attribution figures of the lane B5 continuity window (round 2).

usage:
  b5_attrib.py derive   <raw_a-long_dir> <a472_packet_dir> <out_dir>
  b5_attrib.py wholerun <raw_a-long_dir> <a472_packet_dir> <out.json>
  b5_attrib.py figures  <a472_packet_dir> <derived_dir>

derive (needs the raw read-time record, which stays local) writes the derived read
record of the continuity window, a-long-reads.u16 and a-long-reads.json. wholerun
(needs the raw graded pair) writes the whole-run integrity counts. figures needs only
published inputs: the round-1 packet's summary/a-long/summary.json,
summary/a-long/continuity-events.csv and runs/a-long/events.jsonl, and the derived
read record.

The read-time record (cap-ts.bin) holds one entry per read of the capture pipe: the
frames delivered so far, this host's realtime and its monotonic clock in ns. In the
window every read delivers 480 frames, one capture period, nominally 10 ms apart.
The derived record keeps, for read r = 1 .. R of the window, the monotonic time since
the window's first read in whole microseconds, stored as uint16 little-endian
differences of the rounded cumulative time, so the sum of the first r entries is the
cumulative time rounded to 1 us with no accumulated rounding error. Read r ends at
capture frame c0 + 480 r, where c0 is the window's first frame.

Delivery deficit. D(r) = t(r) * 48000 - 480 r frames, with t(r) the host time since
the window's first read. A frame lost inside the capture path after the capture
samples it delays every later read by its duration, so D steps up by the frames lost.
A frame already missing from the signal the capture samples leaves D unchanged.
Read-to-read scheduling jitter only raises single reads, so the floor of D is taken:
the step across reads a .. b is min D[b + GA .. b + GA + W] - min D[a - GB - W .. a - GB].
A capture frame k is delivered by read r(k) = (k - c0) // 480 + 1.

Stall: a read interval over 15 ms (grade_a.py's STALL_MS). Its excess is the interval
less the 10 ms period.
"""
import csv
import hashlib
import json
import os
import struct
import sys
from pathlib import Path

import numpy as np

FS = 48000
PER = 480                      # frames per read in the window (asserted)
STALL_MS = 15.0                # grade_a.py's stall definition
# floor width and guards, in reads, and the match tolerance in frames; B5_W, B5_GB, B5_GA
# and B5_TOL override them for the sensitivity runs
W, GB, GA = (int(os.environ.get(k, d)) for k, d in (("B5_W", 10), ("B5_GB", 3), ("B5_GA", 2)))
JOIN = GB + GA + W + 1         # multi-frame skips closer than this many reads form one cluster
TOL = float(os.environ.get("B5_TOL", 4.0))   # a step "matches" a hypothesis within this
MS1 = FS // 1000               # 48 frames, one millisecond
CAP_TS_SHA = "717141923d15fc32f09e998d3af779b9e95d8a263091c039e7165bc3c7728262"
CAP_LR_SHA = "2ac666fb5ff6284cc665887758ad6f2754918e5b7932258a06ea7efeeec99bdf"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 22), b""):
            h.update(blk)
    return h.hexdigest()


def window(packet):
    ev = [json.loads(l) for l in open(Path(packet) / "runs/a-long/events.jsonl")]
    c0 = [e for e in ev if e["kind"] == "continuity-start"][0]["frame"]
    c1 = [e for e in ev if e["kind"] == "continuity-end"][0]["frame"]
    return c0, c1


def derive(raw, packet, out):
    raw, out = Path(raw), Path(out)
    src = raw / "cap-ts.bin"
    assert sha256(src) == CAP_TS_SHA, "cap-ts.bin is not the a-long read-time record"
    ts = np.fromfile(src, dtype=np.dtype([("f", "<i8"), ("rt", "<f8"), ("mono", "<i8")]))
    F, mono = ts["f"].astype(np.int64), ts["mono"].astype(np.int64)
    c0, c1 = window(packet)
    j0, j1 = int(np.flatnonzero(F == c0)[0]), int(np.flatnonzero(F == c1)[0])
    assert np.all(np.diff(F[j0:j1 + 1]) == PER), "a read in the window did not deliver one period"
    cum_us = np.rint((mono[j0:j1 + 1] - mono[j0]) / 1000.0).astype(np.int64)
    d = np.diff(cum_us)
    assert d.min() >= 0 and d.max() < 65536
    out.mkdir(parents=True, exist_ok=True)
    rec = out / "a-long-reads.u16"
    d.astype("<u2").tofile(rec)
    meta = dict(source=dict(file="a-long/cap-ts.bin", bytes=src.stat().st_size, sha256=CAP_TS_SHA),
                window_frames=[int(c0), int(c1)], window_read_indices=[j0, j1], reads=int(len(d)),
                frames_per_read=PER, clock="monotonic", unit="us",
                encoding="uint16 LE: differences of the cumulative time rounded to 1 us",
                elapsed_ns_exact=int(mono[j1] - mono[j0]), elapsed_us_record=int(cum_us[-1]),
                record=dict(file=rec.name, bytes=rec.stat().st_size, sha256=sha256(rec)))
    json.dump(meta, open(out / "a-long-reads.json", "w"), indent=1)
    print(json.dumps(meta, indent=1))


def wholerun(raw, packet, out):
    raw = Path(raw)
    src = raw / "cap-lr.raw"
    assert sha256(src) == CAP_LR_SHA, "cap-lr.raw is not the a-long graded pair"
    b = np.fromfile(src, dtype=np.uint8)
    n = len(b) // 6
    b = b[:n * 6].reshape(n, 2, 3).astype(np.int64)
    w = b[:, :, 0] | (b[:, :, 1] << 8) | (b[:, :, 2] << 16)
    L, R = w[:, 0], w[:, 1]
    zero = (L == 0) & (R == 0)
    tagL, tagR = (L != 0) & ((L >> 16) == 1), (R != 0) & ((R >> 16) == 2)
    valid = tagL & tagR & ((L & 0xFFFF) == (R & 0xFFFF))
    torn = tagL & tagR & ((L & 0xFFFF) != (R & 0xFFFF))
    c0, c1 = window(packet)
    ev = [json.loads(l) for l in open(Path(packet) / "runs/a-long/events.jsonl")]
    v = np.flatnonzero(valid)
    first_valid, last_valid = int(v[0]), int(v[-1])
    # zero frames by place: before the first valid frame, after the last, in the window,
    # and in each gap between valid frames that holds an unbind (a cycle's hold)
    zz = np.diff(np.concatenate(([0], zero.astype(np.int8), [0])))
    zs, ze = np.flatnonzero(zz == 1), np.flatnonzero(zz == -1)
    unb = [e["unbind_frames"][1] for e in ev if e["kind"] == "cycle"]
    place = dict(before_first_valid=0, after_last_valid=0, in_window=0, in_a_cycle_hold=0, elsewhere=0)
    elsewhere = []
    for s, e in zip(zs, ze):
        k = int(e - s)
        if e <= first_valid:
            place["before_first_valid"] += k
        elif s > last_valid:
            place["after_last_valid"] += k
        elif c0 <= s and e <= c1:
            place["in_window"] += k
        else:
            # the valid frames bracketing this zero run, and an unbind between them
            lo = v[np.searchsorted(v, s) - 1]
            hi = v[np.searchsorted(v, e)]
            if any(lo - FS <= u <= hi for u in unb):
                place["in_a_cycle_hold"] += k
            else:
                place["elsewhere"] += k
                elsewhere.append([int(s), k])
    res = dict(source=dict(file="a-long/cap-lr.raw", bytes=src.stat().st_size, sha256=CAP_LR_SHA),
               frames=int(n), zero_frames=int(zero.sum()), valid=int(valid.sum()), torn=int(torn.sum()),
               nonzero_words_ch0=int((L != 0).sum()), nonzero_words_ch0_wrong_tag=int(((L != 0) & ~tagL).sum()),
               nonzero_words_ch1=int((R != 0).sum()), nonzero_words_ch1_wrong_tag=int(((R != 0) & ~tagR).sum()),
               first_valid_frame=first_valid, last_valid_frame=last_valid, zero_frames_by_place=place,
               zero_runs_elsewhere=elsewhere)
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


# ------------------------------------------------------------------------- figures --
def pct(x, q=(0, 5, 25, 50, 75, 95, 100)):
    return "[" + ", ".join(f"{v:+.1f}" for v in np.percentile(np.asarray(x, float), q)) + "]"


def figures(packet, derived):
    packet, derived = Path(packet), Path(derived)
    meta = json.load(open(derived / "a-long-reads.json"))
    rec = derived / meta["record"]["file"]
    assert sha256(rec) == meta["record"]["sha256"]
    gap_us = np.fromfile(rec, dtype="<u2").astype(np.int64)
    R = len(gap_us)
    t = np.concatenate(([0], np.cumsum(gap_us))) / 1e6          # t[r], r = 0 .. R
    D = t * FS - PER * np.arange(R + 1)                          # delivery deficit, frames
    g = np.concatenate(([np.nan], gap_us / 1e3))                 # g[r]: interval ending at read r, ms
    s = json.load(open(packet / "summary/a-long/summary.json"))["continuity"]
    c0, c1 = s["window"]
    assert [c0, c1] == meta["window_frames"] and (c1 - c0) == PER * R
    ev = [dict(frame=int(e["frame"]), kind=e["kind"], step=int(e["step"]), frames=int(e["frames"]))
          for e in csv.DictReader(open(packet / "summary/a-long/continuity-events.csv"))]
    for e in ev:
        e["r"] = (e["frame"] - c0) // PER + 1
    zeros = [z["start"] for z in s["silent_stretches"]]
    out = []
    p = out.append

    p("== inputs")
    p(f"derived read record {meta['record']['file']} {meta['record']['bytes']} B sha256 {meta['record']['sha256']}")
    p(f"  from {meta['source']['file']} {meta['source']['bytes']} B sha256 {meta['source']['sha256']}")
    p(f"window frames {c0} .. {c1}: {c1 - c0} frames, {R} reads of {PER} frames")
    p(f"events {len(ev)}: repeats {sum(e['kind'] == 'repeat' for e in ev)}, skips {sum(e['kind'] == 'skip' for e in ev)}")

    p("== window and count drift (bench host clock, uncalibrated)")
    wt = s["window_time"][1] - s["window_time"][0]
    p(f"summary.json window_time {wt:.6f} s: 48 kHz gives {wt * FS:.1f} frames; captured {c1 - c0}; "
      f"deficit {wt * FS - (c1 - c0):.1f} frames ({(wt * FS - (c1 - c0)) / FS:.3f} s)")
    p(f"read record, first to last read of the window: {t[-1]:.6f} s; deficit D(R) - D(0) = {D[-1]:.1f} frames")
    skips = [e for e in ev if e["kind"] == "skip"]
    multi = [e for e in skips if e["frames"] >= 2]
    p(f"skipped frames: all {sum(e['frames'] for e in skips)}; skips of 2 or more {sum(e['frames'] for e in multi)} "
      f"({len(multi)} skips); one-frame {sum(1 for e in skips if e['frames'] == 1)}")
    p(f"deficit less the frames in skips of 2 or more: {wt * FS - (c1 - c0) - sum(e['frames'] for e in multi):.1f} frames")
    content_frames = (c1 - c0) + sum(e["frames"] for e in multi)
    for name, lo, hi in (("2 or more", 2, None), ("60 or more", 60, None), ("2 to 59", 2, 60)):
        f = sum(e["frames"] for e in skips if e["frames"] >= lo and (hi is None or e["frames"] < hi))
        p(f"share of captured plus skipped frames ({content_frames}) in skips of {name}: {f} frames, {100 * f / content_frames:.3f}%")
    p("the round-1 figure 115,614 is not reproduced by either clock reading")

    p("== stalls (read interval over 15 ms)")
    st = np.flatnonzero(g[1:] > STALL_MS) + 1
    ex = (g[st] - 10.0) * FS / 1000
    p(f"stalls {len(st)}; excess over the 10 ms period {ex.sum():.1f} frames; interval {g[st].min():.2f} .. {g[st].max():.2f} ms")
    sp = np.diff(t[st])
    p(f"recurrence: spacing median {np.median(sp):.4f} s, min {sp.min():.3f} s, max {sp.max():.3f} s")
    big = [e for e in skips if e["frames"] >= 240]
    mid = [e for e in skips if 60 <= e["frames"] < 240]
    small = [e for e in skips if 2 <= e["frames"] < 60]
    # alignment: the skip's read lies 0 .. 2 reads after the stall's read
    sset = set(int(x) for x in st)
    def stall_before(e):
        hits = [e["r"] - o for o in (0, 1, 2) if (e["r"] - o) in sset]
        return hits[0] if hits else None
    for name, grp in (("240 frames or more", big), ("60 to 239 frames", mid), ("2 to 59 frames", small)):
        al = [stall_before(e) for e in grp]
        off = [int(e["r"] - a) for e, a in zip(grp, al) if a is not None]
        offc = {o: off.count(o) for o in sorted(set(off))}
        p(f"skips of {name}: {len(grp)}, {sum(e['frames'] for e in grp)} frames; with a stall 0 to 2 reads before: "
          f"{sum(a is not None for a in al)}, reads before {offc}")
    used = {}
    for e in big:
        a = stall_before(e)
        if a is not None:
            used.setdefault(a, []).append(e)
    p(f"stalls followed by a skip of 240 frames or more within 2 reads: {len(used)} of {len(st)}; "
      f"skips per such stall: {sorted(set(len(v) for v in used.values()))}")
    m = np.array([(g[a] - 10.0) * FS / 1000 - sum(e["frames"] for e in multi if 0 <= e["r"] - a <= 2) for a in used])
    p(f"per stall, excess less the frames of every skip of 2 or more 0 to 2 reads after it, "
      f"percentiles 0/5/25/50/75/95/100: {pct(m)}")
    for e in big + mid:
        if stall_before(e) is None:
            iv = g[max(1, e["r"] - 2):e["r"] + 1]
            p(f"  skip of {e['frames']} frames with no stall 0 to 2 reads before: longest read interval there {iv.max():.2f} ms "
              f"({iv.max() - 10.0:.2f} ms over the period, {e['frames'] / 48:.2f} ms lost)")
    p(f"stall excess {ex.sum():.1f} frames against {sum(e['frames'] for e in big)} in the skips of 240 or more "
      f"and {sum(e['frames'] for e in big + mid)} in the skips of 60 or more")

    p("== delivery deficit steps (floor test)")
    p(f"floor width W={W + 1} reads, guards {GB} before and {GA} after; clusters join skips of 2 or more "
      f"within {JOIN} reads; a step matches within {TOL:.0f} frames")

    def step(a, b):
        lo, hi = a - GB - W, b + GA + W
        if lo < 0 or hi > R:
            return None
        return float(D[b + GA:hi + 1].min() - D[lo:a - GB + 1].min())

    mr = np.array(sorted(e["r"] for e in multi))
    def free(a, b, margin):
        i, j = np.searchsorted(mr, a - margin), np.searchsorted(mr, b + margin, side="right")
        return j == i

    # controls
    for name, sel in (("repeats (DUT beat)", lambda e: e["kind"] == "repeat"),
                      ("one-frame skips", lambda e: e["kind"] == "skip" and e["frames"] == 1)):
        es = [e for e in ev if sel(e) and free(e["r"], e["r"], JOIN)]
        x = [step(e["r"], e["r"]) for e in es]
        x = [v for v in x if v is not None]
        p(f"control, {name} clear of skips of 2 or more: {len(x)}; step percentiles {pct(x)}; "
          f"|step| > {TOL:.0f}: {sum(abs(v) > TOL for v in x)}")
    pos = [r for r in range(GB + W, R - GA - W) if free(r, r, JOIN + 4)]
    x = np.array([step(r, r) for r in pos])
    big_free = np.flatnonzero(np.abs(x) > TOL)
    grp = []
    for i in big_free:
        if grp and pos[i] - grp[-1][-1] <= 2 * JOIN:
            grp[-1].append(pos[i])
        else:
            grp.append([pos[i]])
    # a group's step is its largest |step| (the floor windows slide across one shift)
    gmax = [max((x[pos.index(r)] for r in gg), key=abs) for gg in grp]
    near48 = sum(1 for v in gmax if abs(v - MS1) <= TOL)
    p(f"control, every read position clear of skips of 2 or more: {len(pos)}; step percentiles "
      f"0.01/1/50/99/99.99: {pct(x, (0.01, 1, 50, 99, 99.99))}; positions with |step| > {TOL:.0f}: {len(big_free)}, "
      f"in {len(grp)} groups, {near48} of them a step of 48 +- {TOL:.0f} frames (1 ms)")
    for gg, v in zip(grp, gmax):
        p(f"  group at reads {gg[0]} .. {gg[-1]}: largest |step| {v:+.1f} frames")
    # planted steps: add m frames to D after a clear position, recover it
    rng = np.random.default_rng(117)
    pick = rng.choice(np.array(pos), size=300, replace=False)
    for mplant in (6, 12, 24):
        rec_err = []
        for r in pick:
            Dsave = D.copy()
            D[r - 1:] += mplant           # the loss shows at the read before the skip's read, as observed
            rec_err.append(step(r, r) - mplant)
            D[:] = Dsave
        p(f"planted step of {mplant} frames at 300 clear positions: recovered less planted {pct(rec_err)}")

    # clusters of skips of 2 or more
    cl = []
    for e in sorted(multi, key=lambda e: e["r"]):
        if cl and e["r"] - cl[-1][-1]["r"] < JOIN:
            cl[-1].append(e)
        else:
            cl.append([e])
    rows = []
    for c in cl:
        a, b = c[0]["r"], c[-1]["r"]
        stv = step(a, b)
        has_stall = bool(np.any(g[max(1, a - 2):b + 1] > STALL_MS))
        rows.append(dict(a=a, b=b, sizes=[e["frames"] for e in c], step=stv, stall=has_stall,
                         n_small=sum(2 <= e["frames"] < 60 for e in c), f_small=sum(e["frames"] for e in c if e["frames"] < 60),
                         n_large=sum(e["frames"] >= 60 for e in c), f_large=sum(e["frames"] for e in c if e["frames"] >= 60)))
    edge = [r for r in rows if r["step"] is None]
    rows = [r for r in rows if r["step"] is not None]
    p(f"clusters {len(rows) + len(edge)}; at the window's edge (no step) {len(edge)}: sizes {[r['sizes'] for r in edge]}")
    A = [r for r in rows if r["n_large"]]
    B = [r for r in rows if not r["n_large"]]
    tot = lambda rs, k: sum(r[k] for r in rs)
    p(f"clusters with a skip of 60 or more: {len(A)} (with a stall {sum(r['stall'] for r in A)}); skips of 60 or more "
      f"{tot(A, 'n_large')}, {tot(A, 'f_large')} frames; skips of 2 to 59 in them {tot(A, 'n_small')}, {tot(A, 'f_small')} frames")
    p(f"  step less all their skip frames, percentiles {pct([r['step'] - r['f_large'] - r['f_small'] for r in A])}; "
      f"sum of steps {sum(r['step'] for r in A):.1f} against {tot(A, 'f_large') + tot(A, 'f_small')} frames")
    p(f"  step less the frames of 60 or more only, percentiles {pct([r['step'] - r['f_large'] for r in A])}")
    p(f"clusters of skips of 2 to 59 only: {len(B)} (with a stall {sum(r['stall'] for r in B)}); "
      f"skips {tot(B, 'n_small')}, {tot(B, 'f_small')} frames")

    hyp = (("no step", lambda f: 0), ("1 ms step only", lambda f: MS1),
           ("step = skip frames", lambda f: f), ("step = skip frames + 1 ms", lambda f: f + MS1))

    def kind(r):
        f, v = r["f_small"], r["step"]
        fit = [k for k, h in hyp if abs(v - h(f)) <= TOL]
        if len(fit) > 1:
            return "ambiguous"
        return fit[0] if fit else "other"
    for k in [h[0] for h in hyp] + ["ambiguous", "other"]:
        rs = [r for r in B if kind(r) == k]
        fr = sorted(r["f_small"] for r in rs)
        p(f"  {k}: {len(rs)} clusters, {tot(rs, 'n_small')} skips, {tot(rs, 'f_small')} frames"
          + (f"; cluster frames {fr[0]} .. {fr[-1]}; steps {pct([r['step'] for r in rs])}" if rs else "")
          + (f"; {[(r['sizes'], round(r['step'], 1)) for r in rs]}" if k in ("other", "ambiguous", "step = skip frames",
                                                                          "step = skip frames + 1 ms") and rs else ""))
    p(f"skips of 2 to 59: {len(small)} = {tot(A, 'n_small')} in clusters with a skip of 60 or more + {tot(B, 'n_small')} "
      f"in clusters of 2 to 59 only + {len(small) - tot(A, 'n_small') - tot(B, 'n_small')} at the window's edge")

    p("== one-frame skips and repeats (content positions)")
    def content(k, done):
        return (k - c0) + sum(e["step"] - 1 for e in done) - sum(1 for z in zeros if z < k)
    pos_c, done = [], []
    for e in ev:
        pos_c.append(content(e["frame"], done))
        done.append(e)
    one = [(pc, e) for pc, e in zip(pos_c, ev) if e["kind"] == "skip" and e["frames"] == 1]
    slips = []
    for pc, e in one:
        if slips and e["frame"] - slips[-1][1]["frame"] <= 12:
            slips[-1][2].append(e)
            continue
        slips.append([pc, e, [e]])
    pairs = [x for x in slips if len(x[2]) == 2]
    pz = sum(1 for x in pairs if any(x[2][0]["frame"] <= z < x[2][1]["frame"] for z in zeros))
    p(f"one-frame skips {len(one)} form {len(slips)} slip events: {len(slips) - len(pairs)} single, {len(pairs)} of the form "
      f"skip, zero frame, skip ({pz} with the zero between; gaps {sorted(set(x[2][1]['frame'] - x[2][0]['frame'] for x in pairs))} frames); "
      f"zero frames in the window {len(zeros)}")
    spc = [b[0] - a[0] for a, b in zip(slips, slips[1:])]
    single = sorted(v for v in spc if v < 100000)
    med = float(np.median(single))
    p(f"slip spacing, content frames: min {single[0]}, median {med:.0f}, max {single[-1]}; doubles {[v for v in spc if v >= 100000]}")
    p(f"  median {med / FS:.4f} s; one frame in {med:.0f} is {1e6 / med:.2f} ppm (range {1e6 / single[-1]:.2f} .. {1e6 / single[0]:.2f})")
    reps = [pc for pc, e in zip(pos_c, ev) if e["kind"] == "repeat"]
    rsp = [b - a for a, b in zip(reps, reps[1:])]
    rs1 = sorted(v for v in rsp if v < 140000)
    p(f"repeat spacing, content frames: min {rs1[0]}, max {rs1[-1]}, median {np.median(rs1):.0f}; doubles {[v for v in rsp if v >= 140000]}")
    p("  (content positions take each zero frame as inserted between consecutive ordinals)")

    p("== round-1 absolute rates (dropped from the page)")
    content_adv = s["in_order_steps"] + sum(e["step"] for e in skips) + 6
    stream = content_adv + s["repeats"]
    out_ = stream - len(slips)
    for name, n in (("stream", stream), ("recorded output, every skip of 2 or more counted as a capture loss", out_)):
        p(f"{name}: {n} frames in {wt:.6f} s, {1e6 * (n - wt * FS) / (wt * FS):+.2f} ppm against 48 kHz on the bench host's clock")
    p(f"  identity: the second figure is captured frames plus the frames in skips of 2 or more ({out_ - (c1 - c0)})")
    print("\n".join(out))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "derive":
        derive(*sys.argv[2:5])
    elif cmd == "wholerun":
        wholerun(*sys.argv[2:5])
    elif cmd == "figures":
        figures(*sys.argv[2:4])
    else:
        raise SystemExit(__doc__)
