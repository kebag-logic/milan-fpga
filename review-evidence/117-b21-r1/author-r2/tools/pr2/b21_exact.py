#!/usr/bin/env python3
"""Lane B21 PR round 2: exact comparator for the Direction B McASP capture (offline, read-only).

usage: b21_exact.py <capture_pcm> <wire_samples> <nch> <out_json>

Independent of b21_grade.py: no keys, no hashes and no run logic. It finds every wire position where
the capture's first 64 frames equal the wire frames word for word, takes the single such position as
the offset, then compares all nch 32-bit words of every capture frame with the wire frame at that
offset and counts the unequal frames. It also prints the record's noise statistics the page quotes:
frames equal to the one before, all-zero frames and the slot word values, for capture and wire.
"""
import json
import sys

import numpy as np

pcm, wire, nch, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
M = np.fromfile(pcm, dtype="<u4").reshape(-1, nch)
Wd = np.fromfile(wire, dtype="<u4").reshape(-1, nch)
H = 64
cand = np.flatnonzero(np.all(Wd[:len(Wd) - H + 1] == M[0], axis=1))
for h in range(1, H):
    cand = cand[np.all(Wd[cand + h] == M[h], axis=1)]
res = dict(capture_frames=int(len(M)), wire_frames=int(len(Wd)), head_frames=H, head_positions=cand[:10].tolist(),
           head_position_count=int(len(cand)))
if len(cand) == 1:
    off = int(cand[0])
    n = min(len(M), len(Wd) - off)
    bad = ~np.all(M[:n] == Wd[off:off + n], axis=1)
    res.update(offset=off, compared_frames=int(n), not_compared=int(len(M) - n), unequal_frames=int(bad.sum()),
               first_unequal=int(np.flatnonzero(bad)[0]) if bad.any() else None,
               exact=bool(n == len(M) and not bad.any()))


def stats(A):
    eq = np.all(A[1:] == A[:-1], axis=1)
    z = np.all(A == 0, axis=1)
    v, c = np.unique(A, return_counts=True)
    lsb = {int(np.int32(x)) >> 8: int(k) for x, k in zip(v.astype(np.uint32), c)}
    return dict(frames=int(len(A)), equal_to_previous=int(eq.sum()), fraction_equal_to_previous=round(float(eq.mean()), 4),
                all_zero=int(z.sum()), fraction_all_zero=round(float(z.mean()), 4),
                low_byte_nonzero=int(np.count_nonzero(A & 0xFF)), sample_values_lsb=lsb)


res["capture_stats"] = stats(M)
res["wire_stats"] = stats(Wd)
json.dump(res, open(out, "w"), indent=1)
print(json.dumps(res, indent=1))
