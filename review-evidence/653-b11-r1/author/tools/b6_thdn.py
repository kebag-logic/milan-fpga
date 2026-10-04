#!/usr/bin/env python3
"""Lane B6 analysis tool: per-second sine fit, THD+N, SNR, frequency offset and every
sample discontinuity of a captured tone pair, and the synthetic controls that prove it.

Per one-second block (48,000 consecutive captured frames) and per channel:
  * a four-parameter least-squares sine fit (amplitude and phase as cos/sin terms, DC and
    the frequency, the frequency refined by Gauss-Newton from nominal);
  * the residual band-limited to 20 Hz - 20 kHz (the AES17 measurement band, applied as a
    brick-wall on the residual's spectrum);
  * THD+N = band-limited residual power over the fitted fundamental's power, in dB;
  * SNR = fundamental power over the band-limited residual left after also fitting the
    harmonics 2f, 3f, ... below 20 kHz, in dB;
  * the fitted frequency against nominal, in ppm (of the capture's own sample clock).
Every captured frame is decoded to its loop ordinal (b6_tone.py); between consecutive
decoded frames the ordinal step e = (d - 1) mod 48,000, centred, is 0 in order, > 0 a skip
of e frames, < 0 a repeat of -e frames. Frames that do not decode are counted as invalid;
an invalid frame whose two words decode separately to ordinals within 3 of its neighbours
is counted as torn (the two channels from different frames).

A clean block (no discontinuity, every frame decoded) holds 48,000 consecutive loop
frames, a rotation of the loop, so its THD+N and SNR equal the loop's own 24-bit floor
exactly; the floor is computed from the loop.

usage:
  b6_thdn.py controls <out.json>     synthetic controls (clean, one drop, one repeat,
                                     16 ppm and 1 ppm as a resampled rate and as slips)
"""
import json
import sys

import numpy as np

sys.path.insert(0, __import__("os").path.dirname(__file__))
import b6_tone as T  # noqa: E402

FS = 48000
BLK = 48000
F_NOM = (T.F0, T.F1)
BAND = (20.0, 20000.0)


def sine_fit(x, f0, iters=6):
    """Four-parameter fit; returns (f, a, b, c, fitted) with x ~ a cos + b sin + c."""
    n = np.arange(len(x), dtype=np.float64)
    w = 2 * np.pi * f0 / FS
    xm = x.astype(np.float64)
    # three-parameter start at the nominal frequency
    for it in range(iters + 1):
        cw, sw = np.cos(w * n), np.sin(w * n)
        if it == 0:
            M = np.stack([cw, sw, np.ones_like(n)], axis=1)
            a, b, c = np.linalg.lstsq(M, xm, rcond=None)[0]
            continue
        # Gauss-Newton on (a, b, c, w)
        dw = -a * n * sw + b * n * cw
        M = np.stack([cw, sw, np.ones_like(n), dw], axis=1)
        r = xm - (a * cw + b * sw + c)
        sc = np.sqrt((M * M).sum(axis=0))  # column scaling: the w column is ~n*A larger
        da, db, dc, ddw = np.linalg.lstsq(M / sc, r, rcond=None)[0] / sc
        a, b, c, w = a + da, b + db, c + dc, w + ddw
        if abs(ddw) < 1e-16:
            break
    cw, sw = np.cos(w * n), np.sin(w * n)
    fit = a * cw + b * sw + c
    return w * FS / (2 * np.pi), a, b, c, fit


def band_power(r):
    """Mean power of r inside BAND (brick-wall on the spectrum; Parseval)."""
    R = np.fft.rfft(r)
    f = np.fft.rfftfreq(len(r), 1 / FS)
    m = (f >= BAND[0]) & (f <= BAND[1])
    p = np.abs(R[m]) ** 2
    # rfft bins other than DC and Nyquist stand for two conjugate bins
    w = np.where((f[m] == 0) | (f[m] == FS / 2), 1.0, 2.0)
    return float((p * w).sum() / len(r) ** 2)


def block_metrics(x, f_nom):
    f, a, b, c, fit = sine_fit(x, f_nom)
    p_sig = (a * a + b * b) / 2
    r = x - fit
    p_thdn = band_power(r)
    # harmonics of the fitted frequency inside the band, removed for the SNR
    n = np.arange(len(x), dtype=np.float64)
    w = 2 * np.pi * f / FS
    cols = []
    k = 2
    while k * f <= BAND[1]:
        cols += [np.cos(k * w * n), np.sin(k * w * n)]
        k += 1
    if cols:
        H = np.stack(cols, axis=1)
        r2 = r - H @ np.linalg.lstsq(H, r, rcond=None)[0]
    else:
        r2 = r
    p_n = band_power(r2)
    return dict(f_hz=f, ppm=(f / f_nom - 1) * 1e6,
                thdn_db=10 * np.log10(p_thdn / p_sig) if p_thdn > 0 else -400.0,
                snr_db=10 * np.log10(p_sig / p_n) if p_n > 0 else 400.0,
                level_dbfs=10 * np.log10(p_sig / ((2 ** 23) ** 2 / 2)))


def floor():
    lp = T.loop()
    return [block_metrics(lp[:, c], F_NOM[c]) for c in (0, 1)]


def steps(ordn, c0=None, c1=None, tab=None):
    """Discontinuities between consecutive decoded frames, and invalid/torn counts."""
    ok = ordn >= 0
    idx = np.flatnonzero(ok)
    out = dict(frames=int(len(ordn)), decoded=int(ok.sum()), invalid=int((~ok).sum()))
    if len(idx) < 2:
        out["events"] = []
        return out
    d = (ordn[idx[1:]] - ordn[idx[:-1]]) % T.N
    gap = idx[1:] - idx[:-1]  # captured frames between the two decoded frames
    e = (d - gap) % T.N
    e = np.where(e >= T.N // 2, e - T.N, e)
    ev = []
    for j in np.flatnonzero(e != 0):
        ev.append(dict(frame=int(idx[j + 1]), step=int(e[j]),
                       kind="skip" if e[j] > 0 else "repeat", frames=int(abs(e[j])),
                       invalid_between=int(gap[j] - 1)))
    out["events"] = ev
    out["events_across_invalid"] = sum(1 for x in ev if x["invalid_between"] > 0)
    if c0 is not None and out["invalid"]:
        # torn: each word alone is a loop value of an ordinal within 3 of the neighbours
        lp = T.loop()
        torn = 0
        bad = np.flatnonzero(~ok)
        for k in bad[:100000]:
            lo = ordn[k - 1] if k > 0 and ok[k - 1] else None
            if lo is None:
                continue
            near = (lo + np.arange(-2, 5)) % T.N
            a0 = np.flatnonzero(lp[near, 0] == c0[k])
            a1 = np.flatnonzero(lp[near, 1] == c1[k])
            if len(a0) and len(a1) and not set(a0) & set(a1):
                torn += 1
        out["torn"] = torn
    return out


def grade(c0, c1, block=BLK):
    """Per-block metrics for both channels plus the discontinuity list."""
    tab = T.table()
    ordn = T.decode(c0, c1, tab)
    st = steps(ordn, c0, c1, tab)
    ev_frames = np.array([e["frame"] for e in st["events"]], dtype=np.int64)
    blocks = []
    nb = len(c0) // block
    bad = ordn < 0
    for i in range(nb):
        a, b = i * block, (i + 1) * block
        ne = int(((ev_frames >= a + 1) & (ev_frames < b)).sum()) if len(ev_frames) else 0
        m = [block_metrics(x[a:b], F_NOM[c]) for c, x in enumerate((c0, c1))]
        blocks.append(dict(block=i, start=a, events=ne, invalid=int(bad[a:b].sum()),
                           ch0=m[0], ch1=m[1]))
    return st, blocks, ordn


def summarize(st, blocks, fl):
    clean = [b for b in blocks if b["events"] == 0 and b["invalid"] == 0]
    dirty = [b for b in blocks if not (b["events"] == 0 and b["invalid"] == 0)]
    s = dict(blocks=len(blocks), clean_blocks=len(clean), blocks_with_discontinuity=len(dirty),
             events=len(st["events"]), invalid=st["invalid"], torn=st.get("torn", 0),
             skips=sum(1 for e in st["events"] if e["kind"] == "skip"),
             repeats=sum(1 for e in st["events"] if e["kind"] == "repeat"),
             skipped_frames=sum(e["frames"] for e in st["events"] if e["kind"] == "skip"),
             repeated_frames=sum(e["frames"] for e in st["events"] if e["kind"] == "repeat"))
    for c in (0, 1):
        k = f"ch{c}"
        for name, grp in (("clean", clean), ("all", blocks), ("discontinuity", dirty)):
            if not grp:
                continue
            th = np.array([b[k]["thdn_db"] for b in grp])
            sn = np.array([b[k]["snr_db"] for b in grp])
            pp = np.array([b[k]["ppm"] for b in grp])
            s[f"{k}_{name}"] = dict(n=len(grp), thdn_db_median=round(float(np.median(th)), 2),
                                   thdn_db_worst=round(float(th.max()), 2),
                                   snr_db_median=round(float(np.median(sn)), 2),
                                   snr_db_worst=round(float(sn.min()), 2),
                                   ppm_median=float(np.median(pp)), ppm_maxabs=float(np.abs(pp).max()))
        s[f"{k}_floor"] = dict(thdn_db=round(fl[c]["thdn_db"], 3), snr_db=round(fl[c]["snr_db"], 3))
        if clean:
            th = np.array([b[k]["thdn_db"] for b in clean])
            s[f"{k}_clean_max_dev_from_floor_db"] = float(np.abs(th - fl[c]["thdn_db"]).max())
    return s


def controls(out_path):
    rng = np.random.default_rng(477)
    lp = T.loop()
    fl = floor()
    res = dict(floor=[{k: float(v) for k, v in m.items()} for m in fl], cases={})

    def tiled(nframes, start=12345):
        k = (start + np.arange(nframes)) % T.N
        return lp[k, 0].copy(), lp[k, 1].copy()

    def run(name, c0, c1, expect):
        st, blocks, _ = grade(c0, c1)
        s = summarize(st, blocks, fl)
        s["events_list"] = st["events"][:50]
        s["expect"] = expect
        res["cases"][name] = s
        print(name, json.dumps({k: s[k] for k in ("blocks", "clean_blocks", "events", "skips", "repeats",
                                                   "skipped_frames", "repeated_frames", "invalid")}),
              "ch0 clean", s.get("ch0_clean"), "ch1 clean", s.get("ch1_clean"),
              "ch0 dirty", s.get("ch0_discontinuity"), flush=True)
        return s

    # 1. clean: 10 s of the loop from an arbitrary ordinal
    c0, c1 = tiled(10 * FS)
    s = run("clean", c0, c1, "0 events; every block at the floor; 0 ppm")
    s["pass"] = (s["events"] == 0 and s["clean_blocks"] == 10 and s["ch0_clean_max_dev_from_floor_db"] < 0.01
                 and s["ch1_clean_max_dev_from_floor_db"] < 0.01
                 and s["ch0_clean"]["ppm_maxabs"] < 1e-6 and s["ch1_clean"]["ppm_maxabs"] < 1e-6)
    # 2. one dropped frame at capture frame 4.5 s + 777
    c0, c1 = tiled(10 * FS + 1)
    k = 4 * FS + 24777
    c0, c1 = np.delete(c0, k), np.delete(c1, k)
    s = run("drop1", c0, c1, f"one skip of 1 frame at capture frame {k}")
    ev = s["events_list"]
    s["pass"] = (len(ev) == 1 and ev[0]["kind"] == "skip" and ev[0]["frames"] == 1 and ev[0]["frame"] == k
                 and s["blocks_with_discontinuity"] == 1 and s["ch1_discontinuity"]["thdn_db_worst"] > -100)
    # 3. one repeated frame
    c0, c1 = tiled(10 * FS - 1)
    k = 6 * FS + 1234
    c0, c1 = np.insert(c0, k, c0[k - 1]), np.insert(c1, k, c1[k - 1])
    s = run("repeat1", c0, c1, f"one repeat of 1 frame at capture frame {k}")
    ev = s["events_list"]
    s["pass"] = (len(ev) == 1 and ev[0]["kind"] == "repeat" and ev[0]["frames"] == 1 and ev[0]["frame"] == k
                 and s["blocks_with_discontinuity"] == 1 and s["ch1_discontinuity"]["thdn_db_worst"] > -100)
    # 4/5. rate errors as a resampled tone (source clock / capture clock = 1 + ppm)
    for ppm in (16.0, 1.0):
        n = 10 * FS
        c0 = T.tone(T.F0, T.PH0, n, rate=1 + ppm * 1e-6)
        c1 = T.tone(T.F1, T.PH1, n, rate=1 + ppm * 1e-6)
        s = run(f"rate{ppm:g}ppm-resampled", c0, c1, f"fitted offset +{ppm:g} ppm on both tones")
        a0, a1 = s["ch0_all"]["ppm_median"], s["ch1_all"]["ppm_median"]
        s["pass"] = abs(a0 - ppm) < 0.01 * max(ppm, 1) and abs(a1 - ppm) < 0.01 * max(ppm, 1)
    # 6/7. rate errors as slips: one dropped frame every 1/ppm frames
    for ppm, secs in ((16.0, 30), (1.0, 90)):
        period = int(round(1e6 / ppm))
        n = secs * FS
        k = np.arange(n, dtype=np.int64)
        src = k + (k // period)  # one source frame skipped every `period` captured frames
        idx = (777 + src) % T.N
        c0, c1 = lp[idx, 0].copy(), lp[idx, 1].copy()
        s = run(f"rate{ppm:g}ppm-slips", c0, c1, f"one 1-frame skip every {period} frames")
        nexp = (n - 1) // period
        s["expected_events"] = int(nexp)
        sp = np.diff([e["frame"] for e in res["cases"][f"rate{ppm:g}ppm-slips"]["events_list"]])
        s["event_spacing"] = sorted(set(int(x) for x in sp))
        s["effective_ppm"] = s["skipped_frames"] / n * 1e6
        s["pass"] = (s["events"] == nexp and s["skips"] == nexp and s["skipped_frames"] == nexp
                     and s["event_spacing"] in ([period], []))
    res["all_pass"] = all(c["pass"] for c in res["cases"].values())
    json.dump(res, open(out_path, "w"), indent=1, default=float)
    print("ALL_PASS", res["all_pass"])
    return 0 if res["all_pass"] else 1


if __name__ == "__main__":
    if sys.argv[1] == "controls":
        sys.exit(controls(sys.argv[2]))
    raise SystemExit("unknown mode")
