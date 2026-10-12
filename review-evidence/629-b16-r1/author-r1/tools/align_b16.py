#!/usr/bin/env python3
"""Lane B16 copy of lane B15's align_b15.py, changed to compare full sample values. (offline)

Lane B15's tool keyed each frame on the low 8 bits of each channel ((value + 128) & 0xFF) and walked the
recording on that key. That is exact for the idle floor it was built for (-2 to +1 LSB), but with a tone
in the stream two frames that differ only above bit 7 compare equal. Lane B16 changes, fixed before any
lane B16 capture:
  * the key is a 64-bit hash of every channel's full 24-bit value, used only to find candidates; every
    candidate window and every frame counted equal is then checked on the full values;
  * a sixth planted control: one sample changed by +256 LSB (its low byte unchanged), which lane B15's
    key misses and this tool must count as one differing frame;
  * `control` runs the six controls on a decoded tap stream, or with `synth` on a synthetic four-channel
    stream (the tone pair at -40 dBFS with a converter-like noise of about +-60 LSB), so the tool is proven
    before any capture;
  * `pair` mode: <nch> may be followed by a list of stream channels (default 0..nch-1) compared against
    McASP0 channels 0..nch-1.
Everything else (the 256-frame first-window search, the +-64-frame re-synchronisation, the verdicts) is
lane B15's.

usage: align_b16.py <tap.pcap> <stream_id> <port> <mcasp-all.raw> <out.json> [nch]
       align_b16.py control <tap.pcap> <stream_id> <port> <out.json>
       align_b16.py control synth - - <out.json>
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tone_points_b16 as TP  # noqa: E402

W = 256
P = np.array([0x9E3779B97F4A7C15, 0xC2B2AE3D27D4EB4F, 0x165667B19E3779F9, 0x27D4EB2F165667C5,
              0x85EBCA77C2B2AE63, 0xFF51AFD7ED558CCD, 0xC4CEB9FE1A85EC53, 0x94D049BB133111EB], dtype=np.uint64)


def key(a):
    """One 64-bit hash per frame of every channel's full value (candidates only; equality is re-checked)."""
    k = np.zeros(len(a), dtype=np.uint64)
    with np.errstate(over="ignore"):
        for c in range(a.shape[1]):
            k = k * np.uint64(31) + (a[:, c] + (1 << 23)).astype(np.uint64) * P[c % len(P)]
    return k


def find(ks, win, s, m_win, lo=0, hi=None):
    hi = len(ks) - len(win) if hi is None else min(hi, len(ks) - len(win))
    if hi < lo:
        return []
    cand = np.nonzero(ks[lo:hi + 1] == win[0])[0] + lo
    return [int(p) for p in cand if np.array_equal(ks[p:p + len(win)], win) and np.array_equal(s[p:p + len(win)], m_win)]


def compare(s, m, nch, seq_gaps):
    ks, km = key(s), key(m)
    n = len(m)
    res = dict(stream_frames=int(len(s)), mcasp_frames=int(n), channels=nch, window=W, seq_gaps=seq_gaps,
               comparison="full 24-bit values")
    start = None
    for t in range(0, n - W, 4800):
        hits = find(ks, km[t:t + W], s, m[t:t + W])
        if hits:
            start = (t, hits)
            break
    if start is None:
        res["verdict"] = "NO MATCH"
        return res
    t0, hits = start
    res.update(first_window_at_recording_frame=t0, matches_of_first_window=len(hits), stream_offset=hits[0])
    off = hits[0] - t0  # stream index = recording index + off
    diffs, slips, i, compared = 0, [], t0, 0
    while i < n:
        j = i + off
        if j >= len(ks):
            break
        if ks[j] == km[i] and np.array_equal(s[j], m[i]):
            compared += 1
            i += 1
            continue
        win = km[i:i + W]
        if len(win) < W:
            diffs += n - i
            break
        h = find(ks, win, s, m[i:i + W], max(0, j - 64), j + 64)
        if h:
            slips.append(dict(recording_frame=int(i), step=int(h[0] - j)))
            off += h[0] - j
        else:
            diffs += 1
            i += 1
    res.update(compared_equal=compared, frames_differing=diffs, slips=slips,
               covered_recording_frames=[int(t0), int(min(n, len(ks) - off))],
               verdict="SAMPLE-EXACT" if diffs == 0 and not slips else "DIFFERENT")
    return res


def load(pcap, sid, port, nch, chans=None):
    x, info = TP.aaf_decode(pcap, sid, port)
    chans = list(range(nch)) if chans is None else chans
    return (x[:, chans] >> 8).astype(np.int64), info


def synth_stream(n=900000):
    rng = np.random.default_rng(1603)
    k = np.arange(n, dtype=np.float64)
    a = 10 ** (-40 / 20) * (2 ** 23 - 1)
    cols = [a * np.sin(2 * np.pi * 997 * k / 48000 + 0.7), a * np.sin(2 * np.pi * 9973 * k / 48000 + 2.1),
            np.zeros(n), np.zeros(n)]
    return np.stack([np.round(c + rng.normal(0, 20, n)) for c in cols], axis=1).astype(np.int64)


def controls(pcap, sid, port, out):
    if pcap == "synth":
        s, info = synth_stream(), dict(seq_gaps=0)
    else:
        s, info = load(pcap, sid, port, 4)
    base = s[100000:580000].copy()
    cases = []

    def run(label, m, want):
        r = compare(s, m, 4, info["seq_gaps"])
        ok = bool(want(r))
        cases.append(dict(control=label, verdict=r.get("verdict"), slips=r.get("slips"),
                          frames_differing=r.get("frames_differing"), result="PASS" if ok else "FAIL"))

    run("exact copy", base, lambda r: r["verdict"] == "SAMPLE-EXACT")
    # As lane B15: the slip shows where the recording first departs from the old alignment, at the planted
    # frame or later by the run of consecutive equal source frames; the expected frame comes from the content.
    i = 200000
    while np.array_equal(s[100000 + i], s[100000 + i + 1]):
        i += 1
    drop_at = i
    m = np.delete(s[100000:580001], 200000, axis=0)
    run(f"one frame dropped at 200,000 (expected at {drop_at})", m,
        lambda r: r["verdict"] == "DIFFERENT" and r["slips"] == [dict(recording_frame=drop_at, step=1)] and r["frames_differing"] == 0)
    i = 250000
    while np.array_equal(s[100000 + i], s[100000 + i - 1]):
        i += 1
    rep_at = i
    m = np.insert(s[100000:579999], 250000, s[100000 + 249999], axis=0)
    run(f"one frame repeated at 250,000 (expected at {rep_at})", m,
        lambda r: r["verdict"] == "DIFFERENT" and r["slips"] == [dict(recording_frame=rep_at, step=-1)] and r["frames_differing"] == 0)
    m = base.copy()
    m[300000, 2] += 1
    run("one sample changed by 1 LSB at 300,000", m,
        lambda r: r["verdict"] == "DIFFERENT" and r["frames_differing"] == 1 and not r["slips"])
    m = s[300007:780007].copy()
    m[:, 0] = -m[:, 0]
    run("another stretch, channel 0 negated", m, lambda r: r["verdict"] != "SAMPLE-EXACT")
    m = base.copy()
    m[310000, 0] += 256
    run("one sample changed by +256 LSB at 310,000, its low byte unchanged (lane B16)", m,
        lambda r: r["verdict"] == "DIFFERENT" and r["frames_differing"] == 1 and not r["slips"])
    res = dict(controls=cases, all_pass=all(c["result"] == "PASS" for c in cases), stream_frames=int(len(s)),
               stream="synthetic" if pcap == "synth" else os.path.basename(pcap))
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res))
    return 0 if res["all_pass"] else 1


if __name__ == "__main__":
    if sys.argv[1] == "control":
        sys.exit(controls(sys.argv[2], sys.argv[3], None if sys.argv[4] == "-" else int(sys.argv[4]), sys.argv[5]))
    pcap, sid, port, mraw, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5]
    nch = int(sys.argv[6]) if len(sys.argv) > 6 else 4
    chans = [int(c) for c in sys.argv[7:]] or None
    s, info = load(pcap, sid, port, nch, chans)
    w = np.fromfile(mraw, dtype="<i4")
    n = len(w) // 8
    m = (w[:n * 8].reshape(n, 8)[:, :nch].astype(np.int64) >> 8)
    res = compare(s, m, nch, info["seq_gaps"])
    res["stream_channels"] = chans or list(range(nch))
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res))
