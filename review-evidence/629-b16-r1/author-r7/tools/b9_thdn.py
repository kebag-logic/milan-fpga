#!/usr/bin/env python3
"""Lane B9: the Direction B tone grade, and the synthetic controls that prove it.

The Direction B tone is lane B6's tone pair (997 Hz and 9,973 Hz, b9_tone.py at -20 dBFS)
played into the reference peer's talker inputs and received by the DUT's listener, which
renders it on its TDM output; McASP0 records that output in the DUT's TDM clock. Unlike the
Direction A loop, the tone does not arrive as the loop's sample values, so lane B6's frame
decode (b6_tone.decode) cannot number the frames. This tool keeps lane B6's per-block metrics
and replaces the decode with a detector that needs only the tone:

Per one-second block (48,000 consecutive captured frames) and per tone: lane B6's
b6_thdn.block_metrics, unchanged: the four-parameter sine fit, THD+N over 20 Hz - 20 kHz,
SNR with the harmonics also fitted, the fitted frequency against nominal in ppm of the
capture's own clock, and the level.

Discontinuities. A single tone obeys x[n] = 2 cos(w) x[n-1] - x[n-2], so the residual
e[n] = x[n] - 2 cos(w) x[n-1] + x[n-2] holds only the path's noise and distortion, and a
dropped, repeated or inserted frame leaves a spike of up to 2 A sin(w/2) at the frame where it
happens (the 9,973 Hz tone: up to 0.12 of full scale at -20 dBFS). A candidate is a frame where
either tone's residual exceeds K_SIGMA times its block's robust spread (1.4826 x the median
absolute deviation); candidates within GROUP frames of each other are one event. Each event
is sized from both tones: a sine of the nominal frequency is fitted on up to SEG frames before
and after it (bounded by the neighbouring events), and the step e (in frames; e > 0 a skip of
e frames, e < 0 a repeat of -e) is the integer in [-24,000, +24,000) whose phase advance
(w0 e, w1 e) matches the two tones' phase differences best; 997 and 9,973 are coprime with
48,000, so the pair names e uniquely, and the match's error is reported. The event's frame is
the first frame out of sequence (lane B6's convention): the position p near the candidate where
the left fit, continued with the step from p on, matches the data best. An event is a
"repeat" when e < 0 and the frames from p repeat the previous frame exactly on both tones,
an "insert" when they are exactly zero on both, a "skip" when e > 0, and a "glitch" when
the best step is 0 or the two tones do not agree on an integer step (match error above
MATCH_TOL rad). A torn frame (the two tones' channels from different frames) shows as a glitch
or as two events one frame apart; the grade lists both kinds.

The path's floor is not the loop's 24-bit floor: the tone's samples are the path's own. A
block is "at the floor" when it holds no event and its THD+N on each tone lies within
FLOOR_DB of that tone's median over the window's event-free blocks.

Frequency offset over the window, two ways: the net step per frame from the event list (lane
B6's effective offset), and independently the 997 Hz tone's phase at each block's first frame
(three-parameter fit at the nominal frequency, unwrapped): its change from the first block to
the last, in frames, shows any net step the detector missed.

usage:
  b9_thdn.py controls <out.json>                       the synthetic controls
  b9_thdn.py grade <mcasp.raw> <nch> <ch_997> <ch_9973> <f0> <f1> <out.json>
      grade a whole file of McASP0 frames (S32_LE, the 24-bit sample in bits 31:8, <nch>
      channels per frame), frames <f0> to <f1> (f1 = -1: to the end)
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import b6_thdn as A  # noqa: E402

FS = 48000
BLK = 48000
F_NOM = (997, 9973)
K_SIGMA = 8.0
GROUP = 8
SEG = 2400
MIN_SEG = 64
MATCH_TOL = 0.02
FLOOR_DB = 3.0
STEP_RANGE = 24000
W = tuple(2 * np.pi * f / FS for f in F_NOM)


def residual(x, f):
    w = 2 * np.pi * f / FS
    e = np.zeros(len(x))
    e[2:] = x[2:] - 2 * np.cos(w) * x[1:-1] + x[:-2]
    return e


def block_sigma(e, blk=BLK):
    """Robust spread of e per block, as a per-sample array."""
    s = np.empty(len(e))
    for a in range(0, len(e), blk):
        seg = e[a:a + blk]
        d = np.abs(seg - np.median(seg))
        s[a:a + blk] = max(1.4826 * float(np.median(d)), 1e-9)
    return s


def phase_at(x, n, f, n_ref):
    """Three-parameter fit x ~ a cos(w n) + b sin(w n) + c at the nominal frequency; returns the
    phase of the fitted tone at index n_ref (as phi in A cos(w n_ref + phi)) and its amplitude."""
    w = 2 * np.pi * f / FS
    m = (n - n_ref).astype(np.float64)
    M = np.stack([np.cos(w * m), np.sin(w * m), np.ones_like(m)], axis=1)
    a, b, c = np.linalg.lstsq(M, x.astype(np.float64), rcond=None)[0]
    return float(np.arctan2(-b, a)), float(np.hypot(a, b)), (a, b, c)


def wrap(p):
    return (p + np.pi) % (2 * np.pi) - np.pi


_E = np.arange(-STEP_RANGE, STEP_RANGE, dtype=np.float64)


def best_step(d0, d1):
    """The integer step e whose phase advance on both tones best matches (d0, d1)."""
    err = np.abs(wrap(W[0] * _E - d0)) + np.abs(wrap(W[1] * _E - d1))
    i = int(np.argmin(err))
    srt = np.partition(err, 1)[:2]
    return int(_E[i]), float(err[i]), float(srt[1])


def locate(x0, x1, cand, e, lo, hi, fitL):
    """First frame out of sequence near cand: the p where the left fit, continued with step e from p
    on, matches the data best over [p - 24, p + 24] on both tones."""
    best = None
    for p in range(max(lo + 3, cand - GROUP - 2), min(hi - 3, cand + GROUP + 3)):
        n = np.arange(max(lo, p - 24), min(hi, p + 25))
        sse = 0.0
        for c, (x, f) in enumerate(((x0, F_NOM[0]), (x1, F_NOM[1]))):
            a, b, k = fitL[c]
            w = 2 * np.pi * f / FS
            m = np.where(n < p, n, n + e) - cand
            mod = a * np.cos(w * m) + b * np.sin(w * m) + k
            sse += float(((x[n] - mod) ** 2).sum()) / max(a * a + b * b, 1e-9)
        if best is None or sse < best[1]:
            best = (p, sse)
    return best[0]


def detect(x0, x1):
    """Every discontinuity of the tone pair (float arrays of the same length)."""
    n = len(x0)
    z = []
    for x, f in ((x0, F_NOM[0]), (x1, F_NOM[1])):
        e = residual(x, f)
        s = block_sigma(e)
        zz = np.abs(e) / s
        zz[:2] = 0
        z.append(zz)
    hits = np.flatnonzero((z[0] > K_SIGMA) | (z[1] > K_SIGMA))
    groups = []
    for h in hits:
        if groups and h - groups[-1][-1] <= GROUP:
            groups[-1].append(int(h))
        else:
            groups.append([int(h)])
    cands = [g[0] for g in groups]
    events = []
    for gi, g in enumerate(groups):
        c = g[0]
        prev_end = groups[gi - 1][-1] if gi > 0 else -10 ** 9
        next_start = groups[gi + 1][0] if gi + 1 < len(groups) else 10 ** 12
        l0 = max(0, c - SEG, prev_end + GROUP + 2)
        l1 = c - GROUP - 2
        r0 = g[-1] + GROUP + 2
        r1 = min(n, g[-1] + SEG, next_start - GROUP - 2)
        ev = dict(frame=int(c), z0=round(float(z[0][g[0]:g[-1] + 1].max()), 1),
                  z1=round(float(z[1][g[0]:g[-1] + 1].max()), 1), span=int(g[-1] - g[0] + 1))
        if l1 - l0 < MIN_SEG or r1 - r0 < MIN_SEG:
            ev.update(kind="unsized", step=None, frames=None, reason="segments too short",
                      left=int(max(l1 - l0, 0)), right=int(max(r1 - r0, 0)))
            events.append(ev)
            continue
        nl, nr = np.arange(l0, l1), np.arange(r0, r1)
        d, fitL = [], []
        for x, f in ((x0, F_NOM[0]), (x1, F_NOM[1])):
            pl, al, cl = phase_at(x[nl], nl, f, c)
            pr, ar, _ = phase_at(x[nr], nr, f, c)
            d.append(wrap(pr - pl))
            fitL.append(cl)
        e, err, err2 = best_step(d[0], d[1])
        ev.update(step=e, match_err_rad=round(err, 6), next_err_rad=round(err2, 6),
                  left=int(l1 - l0), right=int(r1 - r0))
        if e == 0 or err > MATCH_TOL:
            ev.update(kind="glitch", frames=abs(e))
            events.append(ev)
            continue
        p = locate(x0, x1, c, e, max(l0, 0), min(r1, n), fitL)
        if e > 0:
            kind = "skip"
        else:
            # a repeated or inserted frame is exact: where one lies within GROUP frames of the fit's
            # position, it names the frame (the fit alone cannot place a frame that matches neither side)
            k = -e

            def exact(q0):
                q = np.arange(q0, min(q0 + k, n))
                if q0 < 1 or len(q) < k:
                    return None
                if np.all(x0[q] == x0[q0 - 1]) and np.all(x1[q] == x1[q0 - 1]):
                    return "repeat"
                if np.all(x0[q] == 0) and np.all(x1[q] == 0):
                    return "insert"
                return None
            hit = None
            if k <= 48:
                for q0 in sorted(range(p - GROUP, p + GROUP + 1), key=lambda q: abs(q - p)):
                    hit = exact(q0)
                    if hit:
                        p = q0
                        break
            kind = hit or "repeat"
            ev["exact_repeat"] = hit == "repeat"
            ev["silent"] = hit == "insert"
        ev["frame"] = int(p)
        ev.update(kind=kind, frames=abs(e))
        events.append(ev)
    return events, len(cands)


def block_phases(x, f, blk=BLK):
    """Phase of the tone at each block's first frame (nominal frequency), unwrapped, in rad."""
    nb = len(x) // blk
    ph = []
    for i in range(nb):
        n = np.arange(i * blk, (i + 1) * blk)
        p, _, _ = phase_at(x[n], n, f, n[0])
        ph.append(p + 2 * np.pi * f * (i * blk) / FS)  # phase law referred to frame 0
    return np.unwrap(np.array(ph)) if ph else np.array([])


def grade_arrays(x0, x1, blocks=True):
    x0 = x0.astype(np.float64)
    x1 = x1.astype(np.float64)
    events, ncand = detect(x0, x1)
    out = dict(frames=int(len(x0)), seconds=len(x0) / FS, candidates=ncand, events=events)
    ef = np.array([e["frame"] for e in events], dtype=np.int64)
    bl = []
    nb = len(x0) // BLK
    if blocks:
        for i in range(nb):
            a, b = i * BLK, (i + 1) * BLK
            ne = int(((ef >= a) & (ef < b)).sum()) if len(ef) else 0
            m = [A.block_metrics(x[a:b], F_NOM[c]) for c, x in enumerate((x0, x1))]
            bl.append(dict(block=i, start=a, events=ne, ch0=m[0], ch1=m[1]))
    out["blocks"] = bl
    # window offset: net step per frame, and the 997 Hz phase slope across blocks
    net = sum(e["step"] for e in events if isinstance(e.get("step"), int))
    out["effective_offset_ppm"] = net / len(x0) * 1e6 if len(x0) else None
    ph = block_phases(x0, F_NOM[0])
    if len(ph) >= 3:
        # net frames from the first block's start to the last block's, beyond the nominal phase law
        # (a block holding an event fits a blend of both sides, so an event in the first or the last
        # block shows as a fraction)
        out["phase_net_frames"] = float((ph[-1] - ph[0]) / W[0])
        out["phase_offset_ppm"] = out["phase_net_frames"] / ((len(ph) - 1) * BLK) * 1e6
    else:
        out["phase_offset_ppm"] = None
        out["phase_net_frames"] = None
    out["silent_frames"] = int(((x0 == 0) & (x1 == 0)).sum())
    return out


def summarize(g):
    bl = g["blocks"]
    free = [b for b in bl if b["events"] == 0]
    s = dict(blocks=len(bl), event_free_blocks=len(free))
    med = {}
    for c in (0, 1):
        k = f"ch{c}"
        if free:
            med[k] = float(np.median([b[k]["thdn_db"] for b in free]))
    floor_blocks = [b for b in free if all(b[f"ch{c}"]["thdn_db"] <= med[f"ch{c}"] + FLOOR_DB for c in (0, 1))]
    s["blocks_at_floor"] = len(floor_blocks)
    s["degraded_event_free_blocks"] = [b["block"] for b in free if b not in floor_blocks]
    for c in (0, 1):
        k = f"ch{c}"
        for name, grp in (("floor", floor_blocks), ("all", bl), ("event", [b for b in bl if b["events"] > 0])):
            if not grp:
                continue
            th = np.array([b[k]["thdn_db"] for b in grp])
            sn = np.array([b[k]["snr_db"] for b in grp])
            pp = np.array([b[k]["ppm"] for b in grp])
            lv = np.array([b[k]["level_dbfs"] for b in grp])
            s[f"{k}_{name}"] = dict(n=len(grp), thdn_db_median=round(float(np.median(th)), 2),
                                   thdn_db_worst=round(float(th.max()), 2), thdn_db_best=round(float(th.min()), 2),
                                   snr_db_median=round(float(np.median(sn)), 2), snr_db_worst=round(float(sn.min()), 2),
                                   ppm_median=float(np.median(pp)), ppm_maxabs=float(np.abs(pp).max()),
                                   level_dbfs_median=round(float(np.median(lv)), 2))
    ev = g["events"]
    for kind, key in (("skip", "skips"), ("repeat", "repeats"), ("insert", "inserts"), ("glitch", "glitches"),
                      ("unsized", "unsized")):
        s[key] = sum(1 for e in ev if e["kind"] == kind)
    s["events"] = len(ev)
    s["skipped_frames"] = sum(e["frames"] for e in ev if e["kind"] == "skip")
    s["repeated_frames"] = sum(e["frames"] for e in ev if e["kind"] in ("repeat", "insert"))
    s["sizes"] = {}
    for e in ev:
        key = f"{e['kind']} {e.get('frames')}"
        s["sizes"][key] = s["sizes"].get(key, 0) + 1
    s["effective_offset_ppm"] = g["effective_offset_ppm"]
    s["phase_offset_ppm"] = g["phase_offset_ppm"]
    s["phase_net_frames"] = g["phase_net_frames"]
    s["silent_frames"] = g["silent_frames"]
    return s


# ---------------------------------------------------------------- synthetic controls

LEVEL = 10 ** (-20 / 20) * (2 ** 23 - 1)
PH = (0.7, 2.1)


def synth(n, noise_dbfs, rate=1.0, rng=None, harm_dbc=-90.0, src=None):
    """The tone pair at -20 dBFS, rounded to 24 bits, with 2nd and 3rd harmonics at harm_dbc and
    white noise of noise_dbfs RMS (re full scale); src gives source frame numbers (slips)."""
    k = np.arange(n, dtype=np.float64) if src is None else src.astype(np.float64)
    out = []
    for c, f in enumerate(F_NOM):
        ph = 2 * np.pi * f * rate * k / FS + PH[c]
        x = LEVEL * np.sin(ph)
        h = 10 ** (harm_dbc / 20) * LEVEL
        for m in (2, 3):
            if m * f < FS / 2:
                x = x + h * np.sin(m * ph + 0.3 * m)
        if noise_dbfs is not None:
            x = x + rng.normal(0, 10 ** (noise_dbfs / 20) * 2 ** 23, n)
        out.append(np.round(x))
    return out[0], out[1]


def controls(out_path):
    rng = np.random.default_rng(526)
    res = dict(parameters=dict(K_SIGMA=K_SIGMA, GROUP=GROUP, SEG=SEG, MATCH_TOL=MATCH_TOL, FLOOR_DB=FLOOR_DB,
                               level_dbfs=-20.0, harmonics_dbc=-90.0), cases={})

    def run(name, x0, x1, expect, check):
        g = grade_arrays(x0, x1)
        s = summarize(g)
        s["events_list"] = g["events"][:200]
        s["expect"] = expect
        s["pass"] = bool(check(g, s))
        res["cases"][name] = s
        print(name, "PASS" if s["pass"] else "FAIL",
              json.dumps({k: s[k] for k in ("blocks", "blocks_at_floor", "events", "skips", "repeats", "inserts",
                                            "glitches", "effective_offset_ppm", "phase_offset_ppm")}),
              "ch0 floor", s.get("ch0_floor"), "ch1 floor", s.get("ch1_floor"), flush=True)
        return s

    for nd in (-100.0, -80.0):
        tag = f"noise{int(nd)}"
        # 0. calibration: THD+N of the clean synthetic tone against its analytic value
        n = 10 * FS
        x0, x1 = synth(n, nd, rng=rng)
        # analytic: white noise spreads evenly over the 24,000 Hz; the band holds 19,981 of the
        # one-second block's 1 Hz bins; 24-bit rounding adds 1/12 LSB^2. synth adds a harmonic only
        # below 24 kHz: both of the 997 Hz tone's (1,994 and 2,991 Hz, in band), and only the
        # 9,973 Hz tone's 2nd (19,946 Hz, in band)
        band = 19981 / 24000
        p_sig = LEVEL ** 2 / 2
        p_n = ((10 ** (nd / 20) * 2 ** 23) ** 2 + 1 / 12) * band
        h2 = (10 ** (-90 / 20) * LEVEL) ** 2 / 2
        exp_thdn = [float(10 * np.log10((p_n + 2 * h2) / p_sig)), float(10 * np.log10((p_n + h2) / p_sig))]
        exp_snr = float(10 * np.log10(p_sig / p_n))

        def chk_cal(g, s, exp_thdn=exp_thdn, exp_snr=exp_snr):
            ok = s["events"] == 0 and s["blocks_at_floor"] == 10
            for c in (0, 1):
                ok &= abs(s[f"ch{c}_floor"]["thdn_db_median"] - exp_thdn[c]) < 0.2
                ok &= abs(s[f"ch{c}_floor"]["snr_db_median"] - exp_snr) < 0.2
            return ok
        s = run(f"{tag}-calibration", x0, x1, f"THD+N {exp_thdn[0]:.2f} / {exp_thdn[1]:.2f} dB and SNR {exp_snr:.2f} dB "
                f"within 0.2 dB (analytic: noise in the band plus the in-band harmonics); 0 events", chk_cal)
        s["analytic"] = dict(thdn_db=exp_thdn, snr_db=exp_snr)

        # 1. clean, from another phase
        def chk_clean(g, s):
            return (s["events"] == 0 and s["blocks_at_floor"] == 10 and s["ch0_floor"]["ppm_maxabs"] < 0.01
                    and s["ch1_floor"]["ppm_maxabs"] < 0.01 and abs(s["phase_offset_ppm"]) < 0.01)
        x0, x1 = synth(10 * FS, nd, rng=rng, src=np.arange(10 * FS) + 12345)
        run(f"{tag}-clean", x0, x1, "0 events; every block at the floor; |offset| < 0.01 ppm", chk_clean)

        # 2. one dropped frame
        k = 4 * FS + 24777
        src = np.delete(np.arange(10 * FS + 1), k)
        x0, x1 = synth(10 * FS, nd, rng=rng, src=src)
        run(f"{tag}-drop1", x0, x1, f"one skip of 1 frame at frame {k}",
            lambda g, s, k=k: (s["events"] == 1 and g["events"][0]["kind"] == "skip" and g["events"][0]["frames"] == 1
                               and g["events"][0]["frame"] == k and s["blocks_at_floor"] == 9))

        # 3. one repeated frame (an exact copy of the previous frame, as a render ring repeats it)
        k = 6 * FS + 1234
        x0, x1 = synth(10 * FS - 1, nd, rng=rng)
        x0, x1 = np.insert(x0, k, x0[k - 1]), np.insert(x1, k, x1[k - 1])
        run(f"{tag}-repeat1", x0, x1, f"one repeat of 1 frame at frame {k}",
            lambda g, s, k=k: (s["events"] == 1 and g["events"][0]["kind"] == "repeat" and g["events"][0]["frames"] == 1
                               and g["events"][0]["frame"] == k and g["events"][0]["exact_repeat"]
                               and s["blocks_at_floor"] == 9))

        # 4/5. rate errors as a resampled tone
        for ppm in (16.0, 1.0):
            x0, x1 = synth(10 * FS, nd, rng=rng, rate=1 + ppm * 1e-6)
            run(f"{tag}-rate{ppm:g}ppm-resampled", x0, x1, f"fitted offset +{ppm:g} ppm on both tones; 0 events",
                lambda g, s, ppm=ppm: (s["events"] == 0 and abs(s["ch0_all"]["ppm_median"] - ppm) < 0.01
                                       and abs(s["ch1_all"]["ppm_median"] - ppm) < 0.01
                                       and abs(s["phase_offset_ppm"] - ppm) < 0.01))

        # 6/7. rate errors as slips
        for ppm, secs in ((16.0, 30), (1.0, 90)):
            period = int(round(1e6 / ppm))
            n = secs * FS
            kk = np.arange(n, dtype=np.int64)
            src = kk + kk // period
            x0, x1 = synth(n, nd, rng=rng, src=src + 777)
            nexp = (n - 1) // period

            def chk_slips(g, s, nexp=nexp, period=period, ppm=ppm):
                fr = [e["frame"] for e in g["events"]]
                sp = sorted(set(np.diff(fr).tolist()))
                return (s["events"] == nexp and s["skips"] == nexp and s["skipped_frames"] == nexp
                        and sp in ([period], []) and all(f % period == 0 for f in fr))
            s = run(f"{tag}-rate{ppm:g}ppm-slips", x0, x1, f"one 1-frame skip every {period} frames ({nexp})", chk_slips)
            s["expected_events"] = int(nexp)

        # 8. 60 repeats and 60 drops at random frames (so at random tone phases), 120 s
        n = 120 * FS
        pos = np.sort(rng.choice(np.arange(FS // 2, n - FS // 2, FS // 2), 120, replace=False))
        pos = pos + rng.integers(-1000, 1000, len(pos))
        kinds = rng.permutation(np.array([1] * 60 + [-1] * 60))
        # build the capture: walk the source, skipping or repeating at each planted capture frame
        cap_src = []
        s_i = 0
        planted = []
        j = 0
        for f in range(n):
            if j < len(pos) and f == pos[j]:
                if kinds[j] == 1:
                    s_i += 1
                    planted.append((f, "skip"))
                else:
                    s_i -= 1
                    planted.append((f, "repeat"))
                j += 1
            cap_src.append(s_i)
            s_i += 1
        cap_src = np.array(cap_src)
        x0, x1 = synth(n, nd, rng=rng, src=cap_src + 5000)
        # a repeated frame is an exact copy of the previous one
        for f, kd in planted:
            if kd == "repeat":
                x0[f], x1[f] = x0[f - 1], x1[f - 1]

        def chk_many(g, s, planted=planted):
            got = [(e["frame"], e["kind"]) for e in g["events"] if e.get("frames") == 1]
            return sorted(got) == sorted(planted) and s["events"] == len(planted)
        s = run(f"{tag}-120-at-random-phases", x0, x1,
                "60 one-frame repeats and 60 one-frame skips at random frames: all found at their frames, nothing else",
                chk_many)
        s["planted"] = len(planted)

        # 9. a silent insert, a 60-frame skip and a 24,000-frame step back
        n = 20 * FS
        x0, x1 = synth(n, nd, rng=rng)
        ki, ks, kb = 3 * FS + 101, 9 * FS + 4321, 15 * FS + 999
        src = np.arange(n + 30000, dtype=np.int64)
        cap = np.concatenate([src[:ks], src[ks + 60:kb + 60], src[kb + 60 - 24000:]])[:n]
        x0, x1 = synth(n, nd, rng=rng, src=cap)
        x0 = np.insert(x0, ki, 0)[:n]
        x1 = np.insert(x1, ki, 0)[:n]

        def chk_multi(g, s, ki=ki, ks=ks, kb=kb):
            ev = [(e["frame"], e["kind"], e.get("step")) for e in g["events"]]
            want = [(ki, "insert", -1), (ks + 1, "skip", 60), (kb + 1, "repeat", -24000)]
            return ev == want
        run(f"{tag}-insert-skip60-back24000", x0, x1,
            "a silent insert (step -1), a 60-frame skip and a 24,000-frame step back, each at its frame", chk_multi)

    res["all_pass"] = all(c["pass"] for c in res["cases"].values())
    json.dump(res, open(out_path, "w"), indent=1, default=float)
    print("ALL_PASS", res["all_pass"])
    return 0 if res["all_pass"] else 1


def grade_file(path, nch, c0, c1, f0, f1, out_path):
    raw = np.fromfile(path, dtype="<i4")
    n = len(raw) // nch
    v = raw[:n * nch].reshape(n, nch) >> 8
    f1 = n if f1 < 0 else min(f1, n)
    g = grade_arrays(v[f0:f1, c0], v[f0:f1, c1])
    g["summary"] = summarize(g)
    g["range"] = dict(f0=f0, f1=f1, channels=[c0, c1])
    json.dump(g, open(out_path, "w"), indent=1, default=float)
    print(json.dumps(g["summary"], indent=1, default=float))
    return g


if __name__ == "__main__":
    if sys.argv[1] == "controls":
        sys.exit(controls(sys.argv[2]))
    if sys.argv[1] == "grade":
        a = sys.argv[2:]
        grade_file(a[0], int(a[1]), int(a[2]), int(a[3]), int(a[4]), int(a[5]), a[6])
        sys.exit(0)
    raise SystemExit("unknown mode")
