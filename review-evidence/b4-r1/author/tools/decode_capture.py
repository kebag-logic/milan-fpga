#!/usr/bin/env python3
"""Decode an 8-channel S32_LE capture carrying the ordinal pattern.

usage: decode_capture.py <raw> [<json_out>]

Pattern word for tag t (1..8) and ordinal n: ((t << 16) | (n & 0xffff)) << 8.
Per SoC channel it reports the tag histogram, zero words and words that are
not a pattern word (low byte nonzero or tag outside 1..8). Per frame it checks
that all eight slots carry the same ordinal (a torn or rotated frame does not),
then classifies ordinal steps between consecutive non-silent frames: +1 normal,
0 repeat, +2 one skipped frame, other forward jumps, backward jumps, and
silent (all-zero) frames. Nothing is inferred from silence.
"""
import array
import collections
import hashlib
import json
import sys


def main():
    path = sys.argv[1]
    data = open(path, "rb").read()
    assert len(data) % 32 == 0, len(data)
    w = array.array("I")
    w.frombytes(data)
    if sys.byteorder != "little":
        w.byteswap()
    frames = len(w) // 8
    tags = [collections.Counter() for _ in range(8)]
    zero = [0] * 8
    bad = [0] * 8
    torn = 0
    silent = 0
    steps = collections.Counter()
    jumps = collections.Counter()
    prev = None
    first_ord = None
    seg_len = 0
    runs = []
    events = []
    for f in range(frames):
        fr = w[f * 8:(f + 1) * 8]
        if not any(fr):
            silent += 1
            for c in range(8):
                zero[c] += 1
            continue
        ords = set()
        for c in range(8):
            v = fr[c]
            if v == 0:
                zero[c] += 1
                continue
            t, lo = v >> 24, v & 0xFF
            if lo or not 1 <= t <= 8:
                bad[c] += 1
                continue
            tags[c][t] += 1
            ords.add((v >> 8) & 0xFFFF)
        if len(ords) != 1:
            torn += 1
            continue
        o = ords.pop()
        if first_ord is None:
            first_ord = o
        if prev is not None:
            d = (o - prev) & 0xFFFF
            if d == 1:
                steps["+1"] += 1
                seg_len += 1
            else:
                key = "0 (repeat)" if d == 0 else "+2 (one skipped)" if d == 2 else (
                    "backward" if d > 0x8000 else "forward>2")
                steps[key] += 1
                jumps[d if d < 0x8000 else d - 0x10000] += 1
                events.append((f, d if d < 0x8000 else d - 0x10000))
                runs.append(seg_len)
                seg_len = 0
        prev = o
    runs.append(seg_len)
    # group discontinuities closer than 50 ms (2400 frames) into clusters
    clusters = []
    for f, d in events:
        if clusters and f - clusters[-1]["last_frame"] <= 2400:
            c = clusters[-1]
        else:
            c = dict(first_frame=f, last_frame=f, repeats=0, skips=0, other=[])
            clusters.append(c)
        c["last_frame"] = f
        if d == 0:
            c["repeats"] += 1
        elif d == 2:
            c["skips"] += 1
        else:
            c["other"].append(d)
    starts = [c["first_frame"] for c in clusters]
    gaps = [b - a for a, b in zip(starts, starts[1:])]
    out = dict(
        file=path.split("/")[-1], bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
        frames=frames, nominal_seconds=frames / 48000, silent_frames=silent, torn_frames=torn,
        per_channel=[dict(soc_channel=c, tags=dict(sorted(tags[c].items())), zero_words=zero[c],
                          non_pattern_words=bad[c]) for c in range(8)],
        ordinal_steps=dict(steps), jump_sizes=dict(sorted(jumps.items())),
        longest_clean_run_frames=max(runs) if runs else 0, first_ordinal=first_ord,
        first_nonsilent_frame=next((i for i in range(frames) if any(w[i * 8:(i + 1) * 8])), None),
        clusters=len(clusters), cluster_start_gaps_frames=gaps, cluster_detail=clusters)
    s = json.dumps(out, indent=1)
    print(s)
    if len(sys.argv) > 2:
        open(sys.argv[2], "w").write(s + "\n")


if __name__ == "__main__":
    main()
