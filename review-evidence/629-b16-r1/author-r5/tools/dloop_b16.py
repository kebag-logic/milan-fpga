#!/usr/bin/env python3
"""Lane B16b (new, offline): lane B6's loop decoded at the external capture, to classify the positive
control's discontinuities at (d).

The external capture records the reference peer's digital output, which carries lane B6's loop (b6_tone.py)
when McASP0 plays it into the DUT (run_b16.py modes dira and b0). Every captured frame of the pair is
decoded to its loop ordinal with lane B6's b6_tone.decode, and lane B6's b6_thdn.steps lists every
discontinuity between consecutive decoded frames (skip or repeat, with its size) and the undecodable and
torn frames. Nothing is changed in either; this file only reads the capture (packed 3-byte little-endian,
<nch> channels) and keeps the two channels named on the command line, whose indices come from the private
record, so neither this file nor its output states the capture's layout.

usage: dloop_b16.py <extcap.raw> <nch> <ch_a> <ch_b> <out.json>
       dloop_b16.py control <out.json>     a synthetic capture: the loop on two of six channels, two
                                          silent seconds first, one frame dropped and one repeated
"""
import hashlib
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import b6_thdn as A  # noqa: E402
import b6_tone as T  # noqa: E402

FS = 48000


def read(path, nch, a, b):
    raw = np.fromfile(path, dtype=np.uint8)
    n = len(raw) // (3 * nch)
    r = raw[:n * 3 * nch].reshape(n, nch, 3)
    out = []
    for c in (a, b):
        x = r[:, c, :].astype(np.int64)
        v = x[:, 0] | (x[:, 1] << 8) | (x[:, 2] << 16)
        out.append(np.where(v >= 1 << 23, v - (1 << 24), v))
    return out[0], out[1], n


def analyse(c0, c1, n):
    ordn = T.decode(c0, c1)
    st = A.steps(ordn, c0, c1)
    ok = np.flatnonzero(ordn >= 0)
    ev = [dict(e, second=round(e["frame"] / FS, 3)) for e in st["events"]]
    net = sum(e["step"] for e in st["events"])
    return dict(frames=int(n), decoded=st["decoded"], invalid=st["invalid"], torn=st.get("torn", 0),
                first_decoded_frame=int(ok[0]) if len(ok) else None, last_decoded_frame=int(ok[-1]) if len(ok) else None,
                events=ev, skips=sum(1 for e in ev if e["kind"] == "skip"), repeats=sum(1 for e in ev if e["kind"] == "repeat"),
                net_step_frames=int(net), events_across_invalid=st.get("events_across_invalid", 0))


def control(out):
    lp = T.loop()
    seq = np.concatenate([np.arange(48000 * 3) % T.N])
    seq = np.delete(seq, 60000)                    # one frame dropped at 60,000
    seq = np.insert(seq, 100000, seq[99999])       # one frame repeated at 100,000
    nch, a, b = 6, 2, 5
    body = np.zeros((len(seq), nch), dtype=np.int64)
    body[:, a], body[:, b] = lp[seq, 0], lp[seq, 1]
    sig = np.vstack([np.zeros((2 * FS, nch), dtype=np.int64), body])
    u = sig & 0xFFFFFF
    raw = np.stack([u & 0xFF, (u >> 8) & 0xFF, (u >> 16) & 0xFF], axis=-1).astype(np.uint8).tobytes()
    path = out + ".tmp.raw"
    open(path, "wb").write(raw)
    c0, c1, n = read(path, nch, a, b)
    os.remove(path)
    r = analyse(c0, c1, n)
    kinds = [(e["kind"], e["frames"], e["frame"]) for e in r["events"]]
    ok = kinds == [("skip", 1, 2 * FS + 60000), ("repeat", 1, 2 * FS + 100000)] and r["invalid"] == 2 * FS
    res = dict(control="drop at 60,000 and repeat at 100,000 after 2 s of silence", result=r,
               expected=[["skip", 1, 2 * FS + 60000], ["repeat", 1, 2 * FS + 100000]], verdict="PASS" if ok else "FAIL")
    json.dump(res, open(out, "w"), indent=1)
    print(res["verdict"], kinds, r["invalid"])
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1] == "control":
        sys.exit(control(sys.argv[2]))
    path, nch, a, b, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    c0, c1, n = read(path, nch, a, b)
    r = analyse(c0, c1, n)
    r["sha256"] = hashlib.sha256(open(path, "rb").read()).hexdigest()
    json.dump(r, open(out, "w"), indent=1)
    print(json.dumps({k: v for k, v in r.items() if k != "events"}), json.dumps(r["events"][:20]))
