#!/usr/bin/env python3
"""Lane B15 (new): does the DUT's TDM output carry exactly the samples the DUT received? (offline)

usage: align_b15.py <tap.pcap> <stream_id> <port> <mcasp-all.raw> <out.json> [nch]
       align_b15.py control <tap.pcap> <stream_id> <port> <out.json>
         planted controls built from the decoded stream itself: (1) 480,000 frames copied exactly ->
         SAMPLE-EXACT; (2) one frame dropped at recording frame 200,000 -> one slip of +1 there;
         (3) one frame repeated at 250,000 -> one slip of -1; (4) one sample changed by 1 LSB at
         300,000 -> one differing frame; (5) a recording from another stretch with channel 0 negated
         -> not SAMPLE-EXACT.

The stream the DUT received (decoded from the DUT's link tap by tone_points_b15.aaf_decode, the 24-bit
sample in bits 31:8) and McASP0's recording of the DUT's TDM output (8 x S32_LE) are compared on the
first <nch> channels (default 4, the four identity mappings stream channel c -> TDM slot c). A 256-frame
window of the recording is located in the stream by exact match of all <nch> channels; the recording is
then walked frame by frame against the stream from that offset, and every frame where the two differ is
counted, with each re-synchronisation (a slip of the DUT's render path) located by searching the next
match within +-64 frames. The idle floor (-2 to +1 LSB per channel, four channels) makes a 256-frame
window unique in a 24 s capture; the tool reports how many offsets matched the first window.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tone_points_b15 as TP  # noqa: E402

W = 256


def key(a):
    """One integer per frame, the channels packed (each value offset into 0..255)."""
    k = np.zeros(len(a), dtype=np.int64)
    for c in range(a.shape[1]):
        k = (k << 8) | ((a[:, c] + 128) & 0xFF)
    return k


def find(ks, win, lo=0, hi=None):
    hi = len(ks) - len(win) if hi is None else min(hi, len(ks) - len(win))
    if hi < lo:
        return []
    cand = np.nonzero(ks[lo:hi + 1] == win[0])[0] + lo
    return [int(p) for p in cand if np.array_equal(ks[p:p + len(win)], win)]


def compare(s, m, nch, seq_gaps):
    ks, km = key(s), key(m)
    n = len(m)
    res = dict(stream_frames=int(len(s)), mcasp_frames=int(n), channels=nch, window=W, seq_gaps=seq_gaps)
    start = None
    for t in range(0, n - W, 4800):
        hits = find(ks, km[t:t + W])
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
        if ks[j] == km[i]:
            compared += 1
            i += 1
            continue
        win = km[i:i + W]
        if len(win) < W:
            diffs += n - i
            break
        h = find(ks, win, max(0, j - 64), j + 64)
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


def load(pcap, sid, port, nch):
    x, info = TP.aaf_decode(pcap, sid, port)
    return (x[:, :nch] >> 8).astype(np.int64), info


def controls(pcap, sid, port, out):
    s, info = load(pcap, sid, port, 4)
    base = s[100000:580000].copy()
    cases = []

    def run(label, m, want):
        r = compare(s, m, 4, info["seq_gaps"])
        ok = bool(want(r))
        cases.append(dict(control=label, verdict=r.get("verdict"), slips=r.get("slips"),
                          frames_differing=r.get("frames_differing"), result="PASS" if ok else "FAIL"))

    run("exact copy", base, lambda r: r["verdict"] == "SAMPLE-EXACT")
    # A slip shows where the recording first departs from the old alignment: at the planted frame,
    # or later by the run of consecutive source frames equal to their neighbour (the floor's values
    # are few, so equal neighbours occur). The expected frame is computed from the content.
    ks = key(s)
    i = 200000
    while ks[100000 + i] == ks[100000 + i + 1]:
        i += 1
    drop_at = i
    m = np.delete(s[100000:580001], 200000, axis=0)
    run(f"one frame dropped at 200,000 (expected at {drop_at})", m,
        lambda r: r["verdict"] == "DIFFERENT" and r["slips"] == [dict(recording_frame=drop_at, step=1)] and r["frames_differing"] == 0)
    i = 250000
    while ks[100000 + i] == ks[100000 + i - 1]:
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
    res = dict(controls=cases, all_pass=all(c["result"] == "PASS" for c in cases), stream_frames=int(len(s)))
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res))
    return 0 if res["all_pass"] else 1


if __name__ == "__main__":
    if sys.argv[1] == "control":
        sys.exit(controls(sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5]))
    pcap, sid, port, mraw, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5]
    nch = int(sys.argv[6]) if len(sys.argv) > 6 else 4
    s, info = load(pcap, sid, port, nch)
    w = np.fromfile(mraw, dtype="<i4")
    n = len(w) // 8
    m = (w[:n * 8].reshape(n, 8)[:, :nch].astype(np.int64) >> 8)
    res = compare(s, m, nch, info["seq_gaps"])
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res))
