#!/usr/bin/env python3
"""Offline grade of one Direction A run (lane B5).

usage: grade_a.py <packet_run_dir> <raw_run_dir> <out.json>

Reads the run's events.jsonl and ctl.jsonl (packet) and the raw capture files:
cap-lr.raw (the graded pair, S24_3LE, channel 0 then 1), cap-ts.bin (one record per
pipe read: frames after the read, this host's realtime, monotonic ns) and
cap-all-<n>ch.raw (ten seconds of all capture channels).

Pattern (first light): channel c carries the 24-bit word (tag << 16) | (n & 0xffff),
tag = c + 1, n the TDM frame ordinal. A frame is valid when channel 0 carries tag 1,
channel 1 tag 2, and both carry the same ordinal: every bit of both 24-bit words is
then the expected one (bit-exact at the captured word length). A frame with both tags
right and different ordinals is torn.

Continuity steps between consecutive valid frames, d = (n[k+1] - n[k]) mod 65536:
1 in order; 0 whole-frame repeat; 2..32767 forward skip of d - 1 frames (a skip of
6 m frames is m whole AAF packets at six frames per packet); 32768.. a backward jump.
A silent stretch is a run of frames with both words zero.

Restart (per cycle): from the CONNECT_RX response, taken on the controller host's
clock and moved to this host's clock with the best clock-offset ping that brackets it,
to the first frame of the first run of at least RUN valid frames after it. Capture
frames are placed on this host's clock by the lower envelope of the pipe-read times
(read time minus frames / fs), fitted per 10 s block; that places a frame no earlier
than it reached this host, so a restart is an upper bound by the capture path latency.
"""
import json
import struct
import sys
from pathlib import Path

import numpy as np

FS = 48000
RUN = 480  # 10 ms

run_dir, raw_dir, out_path = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
events = [json.loads(l) for l in open(run_dir / "events.jsonl")]
ctl = [json.loads(l) for l in open(run_dir / "ctl.jsonl")]


def ev(kind):
    return [e for e in events if e["kind"] == kind]


def words(path, nch, chans):
    b = np.fromfile(path, dtype=np.uint8)
    n = len(b) // (3 * nch)
    b = b[:n * 3 * nch].reshape(n, nch, 3).astype(np.int64)
    w = b[:, :, 0] | (b[:, :, 1] << 8) | (b[:, :, 2] << 16)
    return w[:, chans] if chans is not None else w


lr = words(raw_dir / "cap-lr.raw", 2, None)
L, R = lr[:, 0], lr[:, 1]
NFR = len(L)
valid = ((L >> 16) == 1) & ((R >> 16) == 2) & ((L & 0xFFFF) == (R & 0xFFFF))
torn = ((L >> 16) == 1) & ((R >> 16) == 2) & ((L & 0xFFFF) != (R & 0xFFFF))
zero = (L == 0) & (R == 0)
ordn = L & 0xFFFF
res = dict(frames_captured=int(NFR))

# --- channel identification (10 s of all <capture-channel-count> channels) ------------------------------
full = raw_dir / "cap-all-<n>ch.raw"
if full.exists():
    w = words(full, <capture-channel-count>, None)
    ident = []
    for c in range(<capture-channel-count>):
        col = w[:, c]
        tags = np.unique(col >> 16)
        pat = [int(t) for t in tags if 1 <= t <= 8]
        pw = int(np.isin(col >> 16, pat).sum()) if pat else 0
        ident.append(dict(channel=c, frames=int(len(col)), zero_words=int((col == 0).sum()),
                          pattern_tags=pat, pattern_words=pw))
    res["channel_identification"] = ident

# --- host-time model of capture frames ----------------------------------------------
# The capture path loses frames in stalls (a read gap above STALL_MS), so a frame is placed
# from the reads around it only, never across a stall: t(k) = min over nearby reads j of
# (read time - (frames delivered by j - k) / fs), which is the frame's arrival on this
# host plus the smallest read latency in the neighbourhood.
STALL_MS = 15.0
ts = np.fromfile(raw_dir / "cap-ts.bin", dtype=np.dtype([("f", "<i8"), ("rt", "<f8"), ("mono", "<i8")]))
TF, TRT = ts["f"], ts["rt"]
gaps_ms = np.diff(ts["mono"]) / 1e6
stall_after = np.concatenate((gaps_ms > STALL_MS, [False]))  # read j is followed by a stall
res["capture_reads"] = dict(records=int(len(ts)), read_gap_ms_max=round(float(gaps_ms.max()), 3),
                            read_gap_ms_p99=round(float(np.percentile(gaps_ms, 99)), 3),
                            stalls=int((gaps_ms > STALL_MS).sum()))


def frame_time(k, half=20):
    j0 = int(np.searchsorted(TF, k, side="right"))
    j0 = min(j0, len(TF) - 1)
    lo, hi = j0, j0
    while lo > 0 and lo > j0 - half and not stall_after[lo - 1]:
        lo -= 1
    while hi < len(TF) - 1 and hi < j0 + half and not stall_after[hi]:
        hi += 1
    js = np.arange(lo, hi + 1)
    return float(np.min(TRT[js] - (TF[js] - k) / FS))


def stall_near(k0, k1):
    """Stalls whose read interval covers frames between k0 and k1."""
    j0 = int(np.searchsorted(TF, k0, side="right")) - 1
    j1 = int(np.searchsorted(TF, k1, side="right"))
    return [round(float(g), 3) for g in gaps_ms[max(0, j0):max(0, j1)] if g > STALL_MS]


# --- offsets (controller minus this host) -------------------------------------------
syncs = [s for s in ev("sync")]


def offset_near(t_local):
    """Best (lowest round trip) ping among the three before and three after t_local."""
    before = [s for s in syncs if s["t1"] <= t_local][-1:]
    after = [s for s in syncs if s["t0"] >= t_local][:1]
    cand = before + after
    best = min(cand, key=lambda s: s["rtt_ms"])
    return best["offset_ms"] / 1e3, best["rtt_ms"] / 2e3, cand


# --- segments --------------------------------------------------------------------------
c0 = ev("continuity-start")[0]["frame"]
c1 = ev("continuity-end")[0]["frame"]


def steps_in(a, b):
    """Classify consecutive-frame transitions inside [a, b)."""
    v = valid[a:b]
    o = ordn[a:b]
    z = zero[a:b]
    out = dict(frames=int(b - a), seconds=round((b - a) / FS, 3), valid=int(v.sum()),
               invalid_nonzero=int((~v & ~z).sum()), torn=int(torn[a:b].sum()), zero_frames=int(z.sum()))
    # silent stretches
    zz = np.diff(np.concatenate(([0], z.astype(np.int8), [0])))
    zs, ze = np.flatnonzero(zz == 1), np.flatnonzero(zz == -1)
    out["silent_stretches"] = [dict(start=int(a + s), frames=int(t - s)) for s, t in zip(zs, ze)]
    # steps between consecutive frames both valid
    both = v[:-1] & v[1:]
    d = (o[1:] - o[:-1]) % 65536
    idx = np.flatnonzero(both & (d != 1))
    ev_list = []
    for i in idx:
        dd = int(d[i])
        kind = "repeat" if dd == 0 else ("backward" if dd >= 32768 else "skip")
        ev_list.append(dict(frame=int(a + i + 1), step=dd, kind=kind,
                            frames=(0 if dd == 0 else (dd - 1 if kind == "skip" else 65536 - dd))))
    out["in_order_steps"] = int((both & (d == 1)).sum())
    out["repeats"] = sum(1 for x in ev_list if x["kind"] == "repeat")
    sk = [x for x in ev_list if x["kind"] == "skip"]
    out["skip_events"] = len(sk)
    out["skipped_frames"] = sum(x["frames"] for x in sk)
    out["skip_single_frame"] = sum(1 for x in sk if x["frames"] == 1)
    out["skip_whole_packets"] = sum(1 for x in sk if x["frames"] % 6 == 0)
    out["skip_whole_packet_frames"] = sum(x["frames"] for x in sk if x["frames"] % 6 == 0)
    out["skip_other"] = sum(1 for x in sk if x["frames"] != 1 and x["frames"] % 6)
    out["backward"] = sum(1 for x in ev_list if x["kind"] == "backward")
    hist = {}
    for x in sk:
        hist[x["frames"]] = hist.get(x["frames"], 0) + 1
    out["skip_size_histogram"] = dict(sorted(hist.items()))
    out["events"] = ev_list
    # clusters: events closer than 50 ms
    cl = []
    for x in ev_list:
        if cl and x["frame"] - cl[-1]["last"] < FS // 20:
            cl[-1]["last"] = x["frame"]
            cl[-1]["events"].append(x)
        else:
            cl.append(dict(first=x["frame"], last=x["frame"], events=[x]))
    out["clusters"] = len(cl)
    rp = [x["frame"] for x in ev_list if x["kind"] == "repeat"]
    out["repeat_spacing_frames"] = [int(s) for s in np.diff(rp)] if len(rp) > 1 else []
    return out


res["continuity"] = steps_in(c0, c1)
res["continuity"]["window"] = [int(c0), int(c1)]
res["continuity"]["window_time"] = [round(frame_time(c0), 6), round(frame_time(min(c1, NFR - 1)), 6)]
res["continuity"]["capture_stalls_in_window"] = len(stall_near(c0, c1))

# --- binds and cycles --------------------------------------------------------------------
binds = ev("bind")
unbinds = ev("unbind")
cycles = ev("cycle")
init = ev("initial-valid")[0]


def first_run_after(k0, cap_frames):
    """First frame >= k0 that starts RUN consecutive valid frames; None if none in cap."""
    end = min(NFR, k0 + cap_frames)
    v = valid[k0:end]
    if len(v) < RUN:
        return None
    c = np.convolve(v.astype(np.int32), np.ones(RUN, dtype=np.int32), mode="valid")
    hit = np.flatnonzero(c == RUN)
    return int(k0 + hit[0]) if len(hit) else None


def local_index(t_local):
    """Capture frame index placed at t_local (inverse of frame_time)."""
    j = int(np.searchsorted(TRT, t_local))
    j = min(max(j, 0), len(TRT) - 1)
    k = int(TF[j] - (TRT[j] - t_local) * FS)
    for _ in range(4):
        k = int(round(k + (t_local - frame_time(max(0, min(NFR - 1, k)))) * FS))
    return max(0, min(NFR - 1, k))


def bind_record(bev, label):
    off, unc, cand = offset_near(bev["t"])
    t_rx_local = bev["t_rx"] - off
    t_tx_local = bev["t_tx"] - off
    k_bind = local_index(t_rx_local)
    k_first = first_run_after(k_bind, 30 * FS)
    r = dict(label=label, status=bev["status"], offset_ms=round(off * 1e3, 3), offset_unc_ms=round(unc * 1e3, 3),
             cmd_to_response_ms=round((bev["t_rx"] - bev["t_tx"]) * 1e3, 3), bind_frame=k_bind, first_valid_frame=k_first)
    if k_first is not None:
        r["restart_s"] = round(frame_time(k_first) - t_rx_local, 6)
        r["restart_from_command_s"] = round(frame_time(k_first) - t_tx_local, 6)
        r["capture_stalls_bind_to_first_valid"] = stall_near(k_bind, k_first + RUN)
        pre = slice(k_bind, k_first)
        r["frames_before_first_valid"] = dict(zero=int(zero[pre].sum()), valid=int(valid[pre].sum()),
                                              other=int((~zero[pre] & ~valid[pre]).sum()))
    return r


res["initial_bind"] = bind_record(binds[0], "initial")
cyc_rows = []
for i, cy in enumerate(cycles):
    c = cy["cycle"]
    ub = unbinds[i]
    bd = binds[i + 1]
    off_u, _, _ = offset_near(ub["t"])
    t_unbind_local = ub["t_rx"] - off_u
    k_unbind = local_index(t_unbind_local)
    rec = bind_record(bd, f"cycle-{c}")
    k_bind = rec["bind_frame"]
    # last valid frame before the bind, at or after the unbind - 1 s
    seg = valid[max(0, k_unbind - FS):k_bind]
    lastv = np.flatnonzero(seg)
    k_last = int(max(0, k_unbind - FS) + lastv[-1]) if len(lastv) else None
    # stopped: no valid frame from unbind response + 0.5 s to the bind response
    held = int(valid[k_unbind + FS // 2:k_bind].sum()) if k_bind > k_unbind + FS // 2 else 0
    rec.update(cycle=c, unbind_status=ub["status"], unbind_frame=k_unbind,
               last_valid_after_unbind_s=(round(frame_time(k_last) - t_unbind_local, 6) if k_last is not None else None),
               hold_s=round(bd["t_rx"] - ub["t_rx"], 6), valid_frames_in_hold=held,
               stopped=held == 0, flowing_before=cy["flowing_before"])
    if rec.get("first_valid_frame") is not None:
        k_first = rec["first_valid_frame"]
        after = steps_in(k_first, min(NFR, k_first + 3 * FS))
        rec["after_3s"] = {k: after[k] for k in ("repeats", "skip_events", "skipped_frames", "invalid_nonzero", "torn",
                                                  "zero_frames")}
    rec["demonstrated_restart"] = bool(rec["stopped"] and rec.get("first_valid_frame") is not None)
    rec["pass_1s"] = bool(rec["demonstrated_restart"] and rec["restart_s"] < 1.0)
    cyc_rows.append(rec)
res["cycles"] = cyc_rows

rs = np.array([r["restart_s"] for r in cyc_rows if r["demonstrated_restart"]])
if len(rs):
    srt = np.sort(rs)
    p95 = srt[int(np.ceil(0.95 * len(srt))) - 1]
    res["restart_distribution"] = dict(count=int(len(rs)), below_1s=int((rs < 1.0).sum()), min=round(float(srt[0]), 6),
                                       median=round(float(np.median(rs)), 6), p95=round(float(p95), 6),
                                       max=round(float(srt[-1]), 6), mean=round(float(rs.mean()), 6))
    xs = np.array([r["cycle"] for r in cyc_rows if r["demonstrated_restart"]], dtype=float)
    if len(xs) >= 3:
        A = np.vstack([xs, np.ones_like(xs)]).T
        coef, ssr, _, _ = np.linalg.lstsq(A, rs, rcond=None)
        dof = len(xs) - 2
        s2 = float(ssr[0]) / dof if len(ssr) else 0.0
        se = np.sqrt(s2 / np.sum((xs - xs.mean()) ** 2))
        from math import isfinite
        try:
            from scipy.stats import t as tdist
            tq = float(tdist.ppf(0.975, dof))
        except Exception:
            tq = {28: 2.048, 27: 2.052, 26: 2.056, 25: 2.060, 24: 2.064, 23: 2.069, 22: 2.074, 21: 2.080,
                  20: 2.086, 19: 2.093, 18: 2.101}.get(dof, 2.0)
        res["restart_growth"] = dict(first_ten_median=round(float(np.median(rs[:10])), 6),
                                     last_ten_median=round(float(np.median(rs[-10:])), 6),
                                     slope_s_per_cycle=float(coef[0]),
                                     slope_ci95=[float(coef[0] - tq * se), float(coef[0] + tq * se)], dof=dof, t=tq)

# --- peer listener counters at each read -------------------------------------------
cnt = []
for l in ctl:
    x = l.get("line", {})
    if x.get("cmd") == "GET_COUNTERS":
        pl = bytes.fromhex(x["payload"])
        vals = [int.from_bytes(pl[8 + 4 * i:12 + 4 * i], "big") for i in range(32)]
        cnt.append(dict(role=x["role"], what=x["what"], t=l["local_rx"], valid=f"{int.from_bytes(pl[4:8], 'big'):#x}",
                        nonzero={i: v for i, v in enumerate(vals) if v}))
res["counters"] = cnt
res["format_checks"] = ev("format-check")
json.dump(res, open(out_path, "w"), indent=1)
summ = {k: v for k, v in res.items() if k not in ("cycles", "counters", "format_checks", "channel_identification")}
summ["continuity"] = {k: v for k, v in res["continuity"].items() if k not in ("events", "silent_stretches")}
print(json.dumps(summ, indent=1)[:6000])
