#!/usr/bin/env python3
"""Independent decode of a TDM8 SoC capture (8 ch, S32_LE, interleaved).

Pattern: word = ((tag << 16) | (ordinal & 0xffff)) << 8, tag = channel + 1.
Prints JSON: per-channel tag table, valid/invalid/zero counts, torn frames,
frame-to-frame ordinal steps, and clustered discontinuities (gap < 2400 frames).
Usage: decode_dout.py <capture.raw> [cluster_gap_frames]
"""
import json
import sys

import numpy as np

path = sys.argv[1]
gap = int(sys.argv[2]) if len(sys.argv) > 2 else 2400
w = np.fromfile(path, dtype="<u4")
assert w.size % 8 == 0
w = w.reshape(-1, 8)
nframes = w.shape[0]
nz_rows = np.nonzero(np.any(w != 0, axis=1))[0]
first_nz = int(nz_rows[0]) if nz_rows.size else None
zero_rows = int(np.sum(np.all(w == 0, axis=1)))
zero_rows_after_first = int(np.sum(np.all(w[first_nz:] == 0, axis=1))) if first_nz is not None else None
body = w[first_nz:] if first_nz is not None else w[:0]
low = body & 0xFF
tag = (body >> 24).astype(np.int64)
ordv = ((body >> 8) & 0xFFFF).astype(np.int64)
valid = (low == 0) & (tag >= 1) & (tag <= 8)
out = {"file_bytes": int(w.nbytes), "frames": nframes, "first_nonzero_frame": first_nz,
       "all_zero_frames_total": zero_rows, "all_zero_frames_after_first_nonzero": zero_rows_after_first,
       "decoded_frames": int(body.shape[0]), "channels": []}
for c in range(8):
    tags, counts = np.unique(tag[:, c], return_counts=True)
    out["channels"].append({
        "capture_channel": c,
        "tag_histogram": {int(t): int(n) for t, n in zip(tags, counts)},
        "valid_words": int(valid[:, c].sum()),
        "own_tag_valid_words": int((valid[:, c] & (tag[:, c] == c + 1)).sum()),
        "zero_words": int((body[:, c] == 0).sum()),
    })
torn = np.any(ordv != ordv[:, :1], axis=1)
out["torn_frames"] = int(torn.sum())
out["invalid_words"] = int((~valid).sum())
# continuity on channel 0 ordinal (all channels identical if no torn frame)
d = (np.diff(ordv[:, 0]) % 65536)
steps, scount = np.unique(d, return_counts=True)
out["step_histogram"] = {int(s): int(n) for s, n in zip(steps, scount)}
disc = np.nonzero(d != 1)[0]
rep = int(np.sum(d == 0))
# a step of k>1 skips k-1 frames; a step of 0 repeats one; big (wrap) steps flagged separately
drop = int(np.sum(np.where((d > 1) & (d < 32768), d - 1, 0)))
back = int(np.sum(d >= 32768))
out["repeated_frames"] = rep
out["dropped_frames"] = drop
out["backward_steps"] = back
clusters = []
if disc.size:
    start = disc[0]
    prev = disc[0]
    members = [disc[0]]
    for i in disc[1:]:
        if i - prev < gap:
            members.append(i)
        else:
            clusters.append(members)
            members = [i]
        prev = i
    clusters.append(members)
cl = []
for m in clusters:
    m = np.array(m)
    r = int(np.sum(d[m] == 0))
    k = int(np.sum(np.where((d[m] > 1) & (d[m] < 32768), d[m] - 1, 0)))
    cl.append({"start": int(m[0]) + first_nz, "end": int(m[-1]) + first_nz, "repeated": r, "dropped": k, "net": k - r})
out["clusters"] = len(cl)
out["cluster_net_histogram"] = {}
for c in cl:
    out["cluster_net_histogram"][str(c["net"])] = out["cluster_net_histogram"].get(str(c["net"]), 0) + 1
out["cluster_list"] = cl
print(json.dumps(out, indent=1))
