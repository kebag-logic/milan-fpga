#!/usr/bin/env python3
"""Attribute DOUT capture discontinuities (offline, no bench access).

usage: attribute_dout.py <raw> <talker_jsonl> <multiple> [<json_out>]

Unwraps the captured 16-bit ordinals into sender frame numbers (the sender
frame N carries ordinal N & 0xffff) and classifies every discontinuity
cluster (events closer than 50 ms):
  beat    - only repeat/skip pairs, net at most one skipped frame: the
            documented INTERNAL-source TDM frame / media tick beat;
  sender  - a cluster containing underruns (repeats not paired with skips, or
            jumps other than +2) whose first ordinal lies between 60 frames
            before and 2880 frames (60 ms) after a talker PDU sent 150 us or
            more late;
  unexplained - anything else.
"""
import array
import json
import sys


def main():
    raw, tj = sys.argv[1], sys.argv[2]
    w = array.array("I")
    w.frombytes(open(raw, "rb").read())
    frames = len(w) // 8
    late = []
    for line in open(tj):
        if line.startswith("{"):
            o = json.loads(line)
            if o.get("kind") == "late-pdus":
                late = [(n * 6, lat) for n, _, lat in o["entries"]]
    # unwrap: sender frame number of each non-silent captured frame
    seq = []
    prev = None
    base = 0
    for f in range(frames):
        v = w[f * 8]
        if v == 0:
            continue
        o = (v >> 8) & 0xFFFF
        if prev is not None and o < prev and prev - o > 0x8000:
            base += 0x10000
        seq.append((f, base + o))
        prev = o
    # align the unwrapped ordinal to the sender's absolute frame number: choose
    # the 65536 multiple that puts the late PDUs closest before the underruns
    events = []
    for (f0, a), (f1, b) in zip(seq, seq[1:]):
        if b - a != 1:
            events.append((f1, b - a, b))
    clusters = []
    for f, d, n in events:
        if clusters and f - clusters[-1]["last_frame"] <= 2400:
            c = clusters[-1]
        else:
            c = dict(first_frame=f, last_frame=f, first_ordinal_unwrapped=n, repeats=0, skips=0, other=[])
            clusters.append(c)
        c["last_frame"] = f
        if d == 0:
            c["repeats"] += 1
        elif d == 2:
            c["skips"] += 1
        else:
            c["other"].append(d)
    for c in clusters:
        c["kind"] = "beat" if (not c["other"] and 0 <= c["skips"] - c["repeats"] <= 1) else "underrun"
    under = [c for c in clusters if c["kind"] == "underrun"]
    # <multiple>: the 65536-frame multiple taken from the wall-clock start times
    # of the talker and the capture (sender frame = unwrapped ordinal + m * 65536)
    m = int(sys.argv[3])
    off = m * 0x10000
    win = lambda n, lf: -60 <= n - lf <= 2880
    best = (m, sum(1 for c in under if any(win(c["first_ordinal_unwrapped"] + off, lf) for lf, _ in late)))
    for c in clusters:
        if c["kind"] == "underrun":
            n = c["first_ordinal_unwrapped"] + off
            prior = [(lf, lat) for lf, lat in late if win(n, lf)]
            c["kind"] = "sender" if prior else "unexplained"
            c["late_pdus_before"] = len(prior)
            c["max_late_ns_before"] = max((lat for _, lat in prior), default=0)
    summary = dict(
        frames=frames, clusters=len(clusters),
        beat=sum(c["kind"] == "beat" for c in clusters),
        sender=sum(c["kind"] == "sender" for c in clusters),
        unexplained=sum(c["kind"] == "unexplained" for c in clusters),
        beat_repeats=sum(c["repeats"] for c in clusters if c["kind"] == "beat"),
        beat_skips=sum(c["skips"] for c in clusters if c["kind"] == "beat"),
        alignment_multiple=best[0], late_pdus_logged=len(late),
        underrun_clusters_matched=best[1], underrun_clusters=len(under))
    out = dict(summary=summary, clusters=clusters)
    print(json.dumps(summary, indent=1))
    for c in clusters:
        if c["kind"] != "beat":
            print({k: c[k] for k in ("first_frame", "repeats", "skips", "kind", "late_pdus_before", "max_late_ns_before") if k in c})
    if len(sys.argv) > 4:
        open(sys.argv[4], "w").write(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
