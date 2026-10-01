#!/usr/bin/env python3
"""Offline grade of one lane B6 case (run_b6.py output).

usage: grade_b6.py <packet_run_dir> <raw_run_dir> <out.json>

1. Channel identification: which of the <capture-channel-count> capture channels carry the tone (ten seconds of
   all channels kept once the tone was valid).
2. Tone grade over the window (b6_thdn.grade): per one-second block THD+N, SNR and fitted
   frequency per channel; every discontinuity; invalid and torn frames.
3. Attribution of every discontinuity:
     capture path: skips of two frames or more, grouped into clusters (CLUSTER_READS),
                   whose frames the capture path lost: the read-time record's delivery
                   deficit (read time less frames received / 48 kHz) rises across the
                   cluster by its size within 1 ms + 2 % (a loss over the 1 s loop is
                   matched with whole loops added); where the rise is unmeasurable, or
                   spoiled by a neighbouring stall, a read gap of GAP_MS or more in the
                   LOOKBACK_READS reads before it, with every skip of the cluster
                   48 n + 12 frames, the size of every loss with a matching rise
                   (lane B5's read-time method);
     DUT beat:     a one-frame repeat on the DUT talker's own beat comb: in source frames
                   (captured frame plus every earlier step, capture-path losses at their
                   true size) the densest single phase of one-frame repeats on the beat
                   period (93,990 frames at INTERNAL, TIME_SYNC "talker capture handoff"),
                   refined by a line fit, members within BEAT_RES frames of it;
     listener:     everything else (the reference peer's output dropped, repeated or, as
                   "insert", put one silent frame between two consecutive loop frames).
4. Effective frequency offset of the tone over the window: net frames skipped minus
   repeated per captured frame, in ppm, with and without the capture-path events.
5. Frame-rate ratio of McASP0 (the DUT's TDM clock, sampled on the SoC board) to the
   external capture (the reference peer's output clock), both on this host's
   CLOCK_MONOTONIC_RAW:
     McASP0: the board's hw_ptr samples against each sample line's arrival here, lower
             envelope (the supporting line under all points through the x-centroid, which
             minimises the summed excess); also the two-step estimate (hw_ptr against the
             board's own clock by least squares, times the board-clock rate against this
             host's by the same envelope);
     capture: frames received against read time, the same envelope, after adding back the
             frames the capture path lost (the capture-path events' sizes).
   Each rate is also fitted on the window's two halves as a consistency check.
"""
import json
import struct
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import b6_thdn as A  # noqa: E402
import b6_tone as T  # noqa: E402

FS = 48000
STALL_MS = 15.0
BEAT = 93990

run_dir, raw_dir, out_path = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
events = [json.loads(l) for l in open(run_dir / "events.jsonl")]


def ev(kind):
    return [e for e in events if e["kind"] == kind]


def words24(path, nch):
    b = np.fromfile(path, dtype=np.uint8)
    n = len(b) // (3 * nch)
    b = b[:n * 3 * nch].reshape(n, nch, 3).astype(np.int64)
    w = b[:, :, 0] | (b[:, :, 1] << 8) | (b[:, :, 2] << 16)
    return np.where(w >= 1 << 23, w - (1 << 24), w)


res = dict(case=ev("start")[0]["case"], name=ev("start")[0]["name"])

# 1. channel identification
full = raw_dir / "cap-all-<n>ch.raw"
if full.exists():
    w = words24(full, 20)
    tab = T.table()
    ident = []
    for c in range(20):
        col = w[:, c]
        ident.append(dict(channel=c, frames=int(len(col)), zero=int((col == 0).sum()),
                          peak=int(np.abs(col).max()),
                          loop_ch0_values=int(np.isin(col, T.loop()[:, 0]).sum()),
                          loop_ch1_values=int(np.isin(col, T.loop()[:, 1]).sum())))
    pair = T.decode(w[:, 10], w[:, 11], tab)
    res["channel_identification"] = dict(channels=ident, pair_10_11_decoded=int((pair >= 0).sum()),
                                         frames=int(len(pair)))

# 2. tone grade over the window
lr = words24(raw_dir / "cap-lr.raw", 2)
c0f, c1f = lr[:, 0], lr[:, 1]
w0 = ev("window-start")[0]["frame"]
w1 = min(ev("window-end")[0]["frame"], len(c0f))
c0, c1 = c0f[w0:w1], c1f[w0:w1]
st, blocks, ordn = A.grade(c0, c1)
fl = A.floor()

# 3. read-time record and attribution
ts = np.fromfile(raw_dir / "cap-ts.bin", dtype=np.dtype([("f", "<i8"), ("rt", "<f8"), ("raw", "<i8")]))
TF, TRAW = ts["f"], ts["raw"]
gaps_ms = np.diff(TRAW) / 1e6
sel = (TF[1:] > w0) & (TF[:-1] < w1)
res["capture_reads"] = dict(records=int(sel.sum()), read_gap_ms_max=round(float(gaps_ms[sel].max()), 3),
                            read_gap_ms_p99=round(float(np.percentile(gaps_ms[sel], 99)), 3),
                            read_gap_ms_median=round(float(np.median(gaps_ms[sel])), 3),
                            stalls=int((gaps_ms[sel] > STALL_MS).sum()),
                            stall_gaps_ms=[round(float(g), 3) for g in gaps_ms[sel][gaps_ms[sel] > STALL_MS]][:200])


D = TRAW / 1e9 - TF / FS  # read time less the frames received; a capture-path loss of m frames raises it by m / fs


def floor_rise_ms(k_first, k_last, k_prev, k_next, span=100):
    """Rise of the lower envelope of D from before capture frame k_first to after k_last,
    bounded by the neighbouring events; None when either side has fewer than 3 reads."""
    j0 = int(np.searchsorted(TF, k_first, side="left"))  # first read that delivered k_first
    j1 = int(np.searchsorted(TF, k_last, side="left"))
    jp = max(int(np.searchsorted(TF, k_prev, side="left")) + 1, j0 - span, 1)
    jn = min(int(np.searchsorted(TF, k_next, side="left")), j1 + 1 + span, len(TF))
    if j0 - jp < 3 or jn - (j1 + 1) < 3:
        return None
    return round(float((D[j1 + 1:jn].min() - D[jp:j0].min()) * 1e3), 4)


GAP_MS = 11.0
LOOKBACK_READS = 60  # 600 ms: the capture buffer (500 ms) can hold a stall's audio before the loss shows
CLUSTER_READS = 30   # multi-frame skips within 300 ms are one cluster


def recent_gap(k_first, k_last):
    j0 = int(np.searchsorted(TF, k_first, side="left"))
    j1 = int(np.searchsorted(TF, k_last, side="left"))
    g = gaps_ms[max(0, j0 - 1 - LOOKBACK_READS):min(len(gaps_ms), j1 + 3)]
    return round(float(g.max()), 3) if len(g) else None


evl = st["events"]
for e in evl:
    e["capture_frame"] = int(w0 + e["frame"])
    # a one-frame "repeat" across undecodable frames that are all silent is a silent frame the
    # listener inserted between two consecutive loop frames, not a repeated frame
    if e["invalid_between"] > 0:
        k1 = e["frame"]
        k0 = k1 - e["invalid_between"]
        e["silent_between"] = bool(np.all(c0[k0:k1] == 0) and np.all(c1[k0:k1] == 0))
        if e["silent_between"] and e["step"] == -e["invalid_between"]:
            e["kind"] = "insert"
    e["size_48n_plus_12"] = e["kind"] == "skip" and e["frames"] % 48 == 12
    e["stall_ms"] = None
# clusters of discontinuities of two frames or more (skips, and the multi-frame repeats that
# stale capture-buffer frames produce), within CLUSTER_READS reads of each other
multi = [i for i, e in enumerate(evl) if abs(e["step"]) >= 2]
clusters = []
for i in multi:
    if clusters and evl[i]["capture_frame"] - evl[clusters[-1][-1]]["capture_frame"] <= CLUSTER_READS * 480:
        clusters[-1].append(i)
    else:
        clusters.append([i])
cl_out = []
for ci, cl in enumerate(clusters):
    first, last = evl[cl[0]], evl[cl[-1]]
    i0, i1 = cl[0], cl[-1]
    kp = evl[i0 - 1]["capture_frame"] if i0 > 0 else 0
    kn = evl[i1 + 1]["capture_frame"] if i1 + 1 < len(evl) else int(TF[-1])
    rise = floor_rise_ms(first["capture_frame"], last["capture_frame"], kp, kn)
    net = sum(evl[i]["step"] for i in cl)
    gap = recent_gap(first["capture_frame"], last["capture_frame"])
    k = 0
    sig = all(evl[i]["frames"] % 48 == 12 for i in cl if evl[i]["kind"] == "skip")
    stalled = gap is not None and gap >= GAP_MS
    cap = False
    lost = net
    if rise is not None:
        # a loss longer than the 1 s loop shows its size modulo 48,000 frames in the tone
        k = max(0, int(round((rise * FS / 1e3 - net) / T.N)))
        lost = net + k * T.N
        cap = lost > 0 and abs(rise - lost / FS * 1e3) <= 1.0 + 0.02 * lost / FS * 1e3
        basis = "read-time rise"
        if not cap:
            k, lost = 0, net
    if not cap and net > 0 and stalled and (rise is None or sig):
        # no measurable rise (too few reads between events), or one spoiled by a neighbouring
        # stall: a read gap in the look-back, and every skip of the cluster 48 n + 12 frames,
        # the size signature of every loss this path showed with a matching rise
        cap = True
        basis = "read gap" if rise is None else "read gap and 48 n + 12 size"
    elif not cap:
        basis = "read-time rise" if rise is not None else "read gap"
    for i in cl:
        evl[i]["cluster"] = ci
        evl[i]["read_jump_ms"] = rise
        evl[i]["read_gap_ms"] = gap
        if cap:
            evl[i]["stall_ms"] = gap
    if cap:
        first["cluster_lost_frames"] = int(lost)
    cl_out.append(dict(cluster=ci, events=len(cl), first_frame=first["capture_frame"], net_step=int(net),
                       whole_loops_added=k, lost_frames=int(lost), lost_ms=round(lost / FS * 1e3, 4),
                       read_rise_ms=rise, recent_read_gap_ms=gap, size_signature=bool(sig), basis=basis,
                       capture_path=bool(cap),
                       steps=[int(evl[i]["step"]) for i in cl]))
res["skip_clusters"] = cl_out
# one-frame events: the read-time rise across each, as evidence that no time was lost there
for i, e in enumerate(evl):
    if "cluster" in e:
        continue
    kp = evl[i - 1]["capture_frame"] if i > 0 else 0
    kn = evl[i + 1]["capture_frame"] if i + 1 < len(evl) else int(TF[-1])
    e["read_jump_ms"] = floor_rise_ms(e["capture_frame"], e["capture_frame"], kp, kn)
# DUT beat: the DUT talker repeats one whole frame per beat (93,990 frames at INTERNAL). In
# source frames (the captured frame plus every earlier step, a capture-path cluster counted at
# its true loss) the beat is one comb: a single phase on a single period, every tooth present.
# A listener that slips at the same rate makes a comb of its own at another phase (case A2), so
# the beat comb is the densest phase of one-frame repeats, refined by a line fit; its members
# within BEAT_RES frames of the line are the DUT beat.
cum = 0
for e in evl:
    e["source_frame"] = int(e["capture_frame"] + cum)
    # every step where it occurs; a capture-path cluster's whole loops (a loss over the 1 s loop)
    # at its first event, so an event between a cluster's member skips is placed right
    cum += e["step"]
    if e.get("cluster_lost_frames"):
        cum += e["cluster_lost_frames"] - sum(x["step"] for x in evl if x.get("cluster") == e.get("cluster")
                                              and x["stall_ms"] is not None)
BEAT_RES = 50
rep1 = [e for e in evl if e["kind"] == "repeat" and e["frames"] == 1 and e["stall_ms"] is None]
beat_fit = None
if len(rep1) >= 3:
    pos = np.array([e["source_frame"] for e in rep1], dtype=np.float64)
    P0 = BEAT + 0.5
    ph = pos % P0
    hb = np.bincount((ph // 2000).astype(int), minlength=int(P0 // 2000) + 1)
    ctr = (np.argmax(hb) + 0.5) * 2000
    rel = (ph - ctr + P0 / 2) % P0 - P0 / 2
    mem = np.abs(rel) <= 3000
    for _ in range(3):
        n = np.round((pos[mem] - pos[mem][0]) / P0)
        if len(np.unique(n)) < 2:
            break
        P0, b0 = np.polyfit(n, pos[mem], 1)
        res_all = pos - (b0 + np.round((pos - b0) / P0) * P0)
        mem = np.abs(res_all) <= BEAT_RES
    span = (w1 - w0) + sum(e.get("cluster_lost_frames", 0) for e in evl)
    beat_fit = dict(period_frames=float(P0), members=int(mem.sum()), one_frame_repeats=len(rep1),
                    teeth_in_window=float(span / P0), residual_max=float(np.abs(res_all[mem]).max()))
    for e, m in zip(rep1, mem):
        e["beat_member"] = bool(m)
# cross-check: the DUT's own SLIP_TDM count (0x8D8 [15:0]) between the window's first and last
# console reads, per second, against the comb's rate
dr = {e["tag"]: e for e in ev("dut")}
if beat_fit and "window-0" in dr and "window-2" in dr and dr["window-0"].get("words") and dr["window-2"].get("words"):
    s0 = int(dr["window-0"]["words"]["0x8d8"], 16) & 0xFFFF
    s2 = int(dr["window-2"]["words"]["0x8d8"], 16) & 0xFFFF
    dt = dr["window-2"]["t"] - dr["window-0"]["t"]
    beat_fit["slip_tdm_delta"] = (s2 - s0) % 65536
    beat_fit["slip_tdm_seconds"] = round(dt, 3)
    beat_fit["slip_tdm_per_s"] = ((s2 - s0) % 65536) / dt
    beat_fit["comb_per_s_at_48k"] = FS / beat_fit["period_frames"]
res["beat_comb"] = beat_fit
for e in evl:
    if e["stall_ms"] is not None:
        e["cause"] = "capture path"
    elif e.get("beat_member"):
        e["cause"] = "DUT beat"
    else:
        e["cause"] = "listener"
causes = {}
for e in evl:
    c = causes.setdefault(e["cause"], dict(events=0, skips=0, repeats=0, skipped_frames=0, repeated_frames=0,
                                           sizes={}))
    c["events"] += 1
    if e["kind"] == "insert":
        c["silent_inserts"] = c.get("silent_inserts", 0) + 1
    else:
        c["skips" if e["kind"] == "skip" else "repeats"] += 1
        c["skipped_frames" if e["kind"] == "skip" else "repeated_frames"] += e["frames"]
    key = f"{e['kind']} {e['frames']}"
    c["sizes"][key] = c["sizes"].get(key, 0) + 1
if "capture path" in causes:
    causes["capture path"]["lost_frames"] = int(sum(e.get("cluster_lost_frames", 0) for e in evl))
    causes["capture path"]["clusters"] = int(sum(1 for c in cl_out if c["capture_path"]))
beat = [e["frame"] for e in evl if e["cause"] == "DUT beat"]
res["attribution"] = causes
res["dut_beat_spacing"] = dict(min=int(np.diff(beat).min()) if len(beat) > 1 else None,
                               max=int(np.diff(beat).max()) if len(beat) > 1 else None,
                               median=float(np.median(np.diff(beat))) if len(beat) > 1 else None)
lst = [e for e in evl if e["cause"] == "listener"]
res["listener_spacing"] = dict(median=float(np.median(np.diff([e["frame"] for e in lst]))) if len(lst) > 1 else None)

# per-block metrics split by what the block holds
ev_frames = {c: np.array([e["frame"] for e in evl if e["cause"] == c], dtype=np.int64)
             for c in ("capture path", "DUT beat", "listener")}
for b in blocks:
    a, z = b["start"], b["start"] + A.BLK
    b["by_cause"] = {c: int(((f >= a + 1) & (f < z)).sum()) for c, f in ev_frames.items()}
summ = A.summarize(st, blocks, fl)


def grp_stats(grp, k):
    if not grp:
        return None
    th = np.array([b[k]["thdn_db"] for b in grp])
    sn = np.array([b[k]["snr_db"] for b in grp])
    pp = np.array([b[k]["ppm"] for b in grp])
    return dict(n=len(grp), thdn_db_median=round(float(np.median(th)), 2), thdn_db_worst=round(float(th.max()), 2),
                snr_db_median=round(float(np.median(sn)), 2), snr_db_worst=round(float(sn.min()), 2),
                ppm_median=float(np.median(pp)), ppm_maxabs=float(np.abs(pp).max()))


groups = {
    "clean": [b for b in blocks if b["events"] == 0 and b["invalid"] == 0],
    "listener": [b for b in blocks if b["by_cause"]["listener"] > 0],
    "dut_beat_only": [b for b in blocks if b["by_cause"]["DUT beat"] > 0 and b["by_cause"]["listener"] == 0
                      and b["by_cause"]["capture path"] == 0],
    "capture_path": [b for b in blocks if b["by_cause"]["capture path"] > 0],
    "all": blocks,
}
res["blocks"] = {g: {f"ch{c}": grp_stats(v, f"ch{c}") for c in (0, 1)} for g, v in groups.items()}
res["floor"] = [dict(thdn_db=round(m["thdn_db"], 3), snr_db=round(m["snr_db"], 3)) for m in fl]
res["tone"] = {k: summ[k] for k in ("blocks", "clean_blocks", "blocks_with_discontinuity", "events", "invalid", "torn",
                                    "skips", "repeats", "skipped_frames", "repeated_frames")}
res["tone"]["silent_inserts"] = sum(1 for e in evl if e["kind"] == "insert")
res["tone"]["repeats"] -= res["tone"]["silent_inserts"]
res["tone"]["repeated_frames"] -= res["tone"]["silent_inserts"]
res["tone"]["events_across_invalid"] = st.get("events_across_invalid", 0)
for c in (0, 1):
    res["tone"][f"ch{c}_clean_max_dev_from_floor_db"] = summ.get(f"ch{c}_clean_max_dev_from_floor_db")
nfr = len(c0)
net = sum(e["step"] for e in evl)
net_nocap = sum(e["step"] for e in evl if e["cause"] != "capture path")
net_list = sum(e["step"] for e in evl if e["cause"] == "listener")
res["window"] = dict(frames=int(nfr), seconds=round(nfr / FS, 3), start_frame=int(w0), end_frame=int(w1))
res["effective_offset_ppm"] = dict(all_events=net / nfr * 1e6, without_capture_path=net_nocap / nfr * 1e6,
                                   listener_only=net_list / nfr * 1e6)

# 5. frame-rate ratio
#
# (a) Counted, from the tone: between two consecutive captured frames the McASP0 played (the
#     DUT's TDM input, slaved to the DUT's TDM clock) as many frames as the ordinal advanced,
#     and the reference peer's output produced one. So over the captured frames, McASP0 /
#     peer - 1 = (sum of the non-capture-path steps) / (captured frames); audio the capture
#     path lost, and any event inside it, is left out of both.
# (b) Timed, on this host's CLOCK_MONOTONIC_RAW: for each clock a series D = arrival time -
#     frames / 48,000 (frames: the board's hw_ptr, or the external capture's frames received
#     plus the frames its path lost); its lower envelope rises at (1 - rate / 48,000) s per s
#     plus a latency floor that moves in steps. The slope is the Theil-Sen median of the
#     pairwise slopes of the per-SEG_S-second minima, and its 95 % interval the 2.5 and 97.5
#     percentiles of those pairwise slopes' bootstrap over segments.
SEG_S = 10.0
rng = np.random.default_rng(629)


def seg_minima(t, D, seg=SEG_S):
    k = np.floor((t - t[0]) / seg).astype(np.int64)
    out_t, out_d = [], []
    for s in np.unique(k):
        m = np.flatnonzero(k == s)
        if len(m) >= 5:
            i = m[np.argmin(D[m])]
            out_t.append(t[i]); out_d.append(D[i])
    return np.array(out_t), np.array(out_d)


def theil_sen(x, y):
    i, j = np.triu_indices(len(x), 1)
    dx = x[j] - x[i]
    ok = dx > 0
    return float(np.median((y[j] - y[i])[ok] / dx[ok]))


def rate_of(t, D):
    """Frames per host second from D(t) = t - frames / FS (t and D in seconds)."""
    st_, sd_ = seg_minima(t, D)
    s = theil_sen(st_, sd_)
    boots = []
    for _ in range(300):
        pick = np.sort(rng.integers(0, len(st_), len(st_)))
        u = np.unique(pick)
        if len(u) > 3:
            boots.append(theil_sen(st_[u], sd_[u]))
    lo, hi = np.percentile(boots, [2.5, 97.5])
    h = len(st_) // 2
    return dict(rate=FS * (1 - s), rate_lo=FS * (1 - hi), rate_hi=FS * (1 - lo), segments=int(len(st_)),
                rate_first_half=FS * (1 - theil_sen(st_[:h], sd_[:h])),
                rate_second_half=FS * (1 - theil_sen(st_[h:], sd_[h:])),
                floor_spread_ms=round(float(np.ptp(sd_ - (sd_[0] + s * (st_ - st_[0])))) * 1e3, 4))


steps_nc = sum(e["step"] for e in evl if e["cause"] != "capture path")
lost_cap = sum(e.get("cluster_lost_frames", 0) for e in evl)
# events inside audio the capture path lost cannot be seen, so the count runs over the frames
# observed: McASP0 / peer - 1 = (non-capture-path steps) / (captured frames in the window)
ratio = dict(counted=dict(steps_non_capture=int(steps_nc), observed_frames=int(nfr), capture_lost_frames=int(lost_cap),
                          ppm=steps_nc / nfr * 1e6, resolution_ppm=1 / nfr * 1e6))
samp = []
for line in open(raw_dir / "samples.txt"):
    tt, _, body = line.rstrip("\n").partition("\t")
    p = body.split()
    if len(p) == 11 and p[0] == "S":
        samp.append(dict(arr=int(tt), n=int(p[1]), t0=float(p[2]), t1=float(p[3]), t2=float(p[4]),
                         sp=p[5], hp=int(p[6]), sc=p[7], hc=int(p[8]), gp=p[9], gc=p[10]))
r0 = ev("window-start")[0]["mono_raw_ns"]
r1 = ev("window-end")[0]["mono_raw_ns"]
ratio["samples_total"] = len(samp)
win = [s for s in samp if r0 <= s["arr"] <= r1]
ratio["samples_window"] = len(win)
# external capture
jm = (TRAW >= r0) & (TRAW <= r1)
f = TF[jm].astype(np.float64)
for e in evl:
    if e.get("cluster_lost_frames"):
        f = f + np.where(f >= e["capture_frame"], e["cluster_lost_frames"], 0)
tr = TRAW[jm] / 1e9
ext = rate_of(tr - tr[0], (tr - tr[0]) - (f - f[0]) / FS)
ext["reads"] = int(jm.sum())
ratio["external_capture"] = ext
for nm, hk, sk, gk, (ta, tb_) in (("mcasp_capture", "hc", "sc", "gc", ("t1", "t2")),
                                   ("mcasp_playback", "hp", "sp", "gp", ("t0", "t1"))):
    w_ = [s for s in win if s[sk] == "RUNNING" and s[hk] >= 0]
    if len(w_) < 50:
        ratio[nm] = dict(error="too few running samples", samples=len(w_))
        continue
    trig = sorted(set(s[gk] for s in w_))
    hw = np.array([s[hk] for s in w_], dtype=np.float64)
    if len(trig) != 1 or np.any(np.diff(hw) < 0):
        ratio[nm] = dict(error="the PCM restarted in the window", triggers=trig[:5])
        continue
    a = np.array([s["arr"] for s in w_]) / 1e9
    tb = np.array([(s[ta] + s[tb_]) / 2 for s in w_])
    o = rate_of(a - a[0], (a - a[0]) - (hw - hw[0]) / FS)
    # two-step: frames per board second by least squares; board seconds per host second by the envelope
    pb = np.polyfit(tb - tb[0], hw - hw[0], 1)
    resid = (hw - hw[0]) - np.polyval(pb, tb - tb[0])
    bh = rate_of(a - a[0], (a - a[0]) - (tb - tb[0]) / 1.0 / FS * FS)  # board clock as "frames" at 1 per s
    host_per_board = 1 / (1 - (1 - bh["rate"] / FS))  # board seconds per host second
    o.update(samples=len(w_), trigger=trig[0], rate_board=float(pb[0]),
             board_fit_resid_frames_rms=round(float(np.sqrt((resid ** 2).mean())), 3),
             board_fit_resid_frames_maxabs=round(float(np.abs(resid).max()), 3),
             board_read_us_median=round(float(np.median([(s[tb_] - s[ta]) * 1e6 for s in w_])), 1),
             board_s_per_host_s=bh["rate"] / FS, board_s_per_host_s_lo=bh["rate_lo"] / FS,
             board_s_per_host_s_hi=bh["rate_hi"] / FS)
    o["rate_two_step"] = o["rate_board"] * o["board_s_per_host_s"]
    o["ratio_ppm"] = (o["rate"] / ext["rate"] - 1) * 1e6
    o["ratio_ppm_two_step"] = (o["rate_two_step"] / ext["rate"] - 1) * 1e6
    o["ratio_ppm_first_half"] = (o["rate_first_half"] / ext["rate_first_half"] - 1) * 1e6
    o["ratio_ppm_second_half"] = (o["rate_second_half"] / ext["rate_second_half"] - 1) * 1e6
    # interval: the two rates' bootstrap intervals (independent, half-widths in quadrature), and in
    # quadrature with it half the difference between the halves' ratios: the external capture's
    # read times sit on the host's USB frame grid, so its deficit floor is a 1 ms sawtooth whose
    # phase at the window's ends the bootstrap does not see (set after case A0, before any other
    # case was graded)
    hw1 = (o["rate_hi"] - o["rate_lo"]) / 2 / o["rate"]
    hw2 = (ext["rate_hi"] - ext["rate_lo"]) / 2 / ext["rate"]
    o["ratio_ppm_halfwidth95_bootstrap"] = float(np.hypot(hw1, hw2) * 1e6)
    o["ratio_ppm_halves_halfdiff"] = abs(o["ratio_ppm_first_half"] - o["ratio_ppm_second_half"]) / 2
    o["ratio_ppm_halfwidth95"] = float(np.hypot(o["ratio_ppm_halfwidth95_bootstrap"], o["ratio_ppm_halves_halfdiff"]))
    ratio[nm] = o
res["frame_rate_ratio"] = ratio

# DUT counters at the window marks
res["dut_reads"] = [dict(tag=e["tag"], t=e["t"], words=e.get("words")) for e in ev("dut")]
res["blocks_list"] = blocks
res["events_list"] = evl
json.dump(res, open(out_path, "w"), indent=1, default=float)
short = {k: res[k] for k in ("case", "window", "tone", "attribution", "effective_offset_ppm", "dut_beat_spacing",
                             "listener_spacing", "capture_reads")}
short["blocks"] = res["blocks"]
short["ratio"] = {k: v for k, v in ratio.items()}
print(json.dumps(short, indent=1, default=float))
