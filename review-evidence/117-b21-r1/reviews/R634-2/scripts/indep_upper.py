"""Independent recomputation of the restart upper bound (no author code imported).
For each logged cycle: start = the cycle driver's binding-rule stamp; end = the realtime stamp of the
capture read whose cumulative frame count first covers the first valid pattern frame after the silence
that contains the start. Also checks the reader's record covers the sample file exactly.
usage: indep_upper.py <cycles.jsonl> <cap-lr.raw> <cap-ts.bin>"""
import json, sys
import numpy as np
cyc, lr, tsf = sys.argv[1:4]
ev = [json.loads(l) for l in open(cyc) if l.startswith("{")]
starts = [(e["tag"], e["t"]) for e in ev if e["kind"] == "binding-rule"]
binds = [e["t"] for e in ev if e["kind"] == "bind"]
raw = np.fromfile(lr, dtype=np.uint8)
assert len(raw) % 6 == 0
n = len(raw) // 6
s = raw.reshape(n, 2, 3).astype(np.int64)
s = s[..., 0] | s[..., 1] << 8 | s[..., 2] << 16
L, R = s[:, 0], s[:, 1]
valid = (L >> 16 == 1) & (R >> 16 == 2) & ((L & 0xFFFF) == (R & 0xFFFF))
ts = np.fromfile(tsf, dtype=[("f", "<i8"), ("rt", "<f8"), ("mono", "<i8")])
print("frames", n, "reader total", int(ts["f"][-1]), "monotone", bool(np.all(np.diff(ts["f"]) > 0)))
d = ts["rt"] - ts["mono"] / 1e9
print("realtime-monotonic span us", round((d.max() - d.min()) * 1e6, 2))
# first frame index delivered by each read
first_of_read = np.concatenate([[0], ts["f"][:-1]])
ups = []
for (tag, t0), tb in zip(starts, binds):
    r = int(np.searchsorted(ts["rt"], t0))          # first read stamped after the start
    f0 = int(first_of_read[r])                        # frames from this read on arrived after t0
    # the start must lie in a silence: the frames delivered up to read r must end in invalid frames
    # first valid frame at or after f0 that begins 480 valid in-order frames
    v = np.flatnonzero(valid[f0:]) + f0
    k = int(v[0])
    run = valid[k:k + 480].all() and np.all(np.diff(L[k:k + 480] & 0xFFFF) % 65536 == 1)
    rr = int(np.searchsorted(ts["f"], k + 1))
    prev_valid = int(np.flatnonzero(valid[:f0])[-1])
    gap = k - prev_valid - 1
    up = ts["rt"][rr] - t0
    ups.append(up)
    print(tag, "upper_ms", f"{up*1e3:.3f}", "silence_frames", gap, "480ok", bool(run),
          "start_before_bind_event_ms", f"{(tb - t0)*1e3:.1f}")
ups = np.array(ups)
print("n", len(ups), "min", f"{ups.min()*1e3:.3f}", "median", f"{np.median(ups)*1e3:.3f}", "max", f"{ups.max()*1e3:.3f}", "under_1s", int((ups < 1).sum()))
