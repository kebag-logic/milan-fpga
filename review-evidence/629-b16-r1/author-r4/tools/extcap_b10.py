#!/usr/bin/env python3
"""Lane B10 (new): one short read-only recording of the external capture while the tone plays, as a
diagnostic beside the tone proof (not graded). Per channel: RMS level in dBFS and the share of
its power within +-5 Hz of 997 Hz and of 9,973 Hz (b8_proof.py's rule: a channel carries a tone
when the share exceeds 0.9 at a level above -40 dBFS). The per-channel rows go to the private
directory (B10_PRIV), because the capture's channel layout is private; the packet gets counts only.
The caller holds the bench lock. No setting of the device is read or written.

usage: extcap_b10.py <raw_dir> <packet_summary.json> <seconds>
Environment (private): CAP_CARD, CAP_NCH, CAP_FMT, B10_PRIV.
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np

raw, out, secs = Path(sys.argv[1]), sys.argv[2], int(sys.argv[3])
raw.mkdir(parents=True, exist_ok=False)
e = os.environ
nch = int(e["CAP_NCH"])
f = raw / "extcap.raw"
r = subprocess.run(["arecord", "-D", f"hw:{e['CAP_CARD']},0", "-f", e["CAP_FMT"], "-r", "48000", "-c", str(nch), "-t", "raw",
                    "-d", str(secs), str(f)], capture_output=True, text=True, timeout=secs + 30)
b = np.frombuffer(f.read_bytes(), dtype=np.uint8)
n = len(b) // (3 * nch)
a = b[:n * 3 * nch].reshape(n, nch, 3).astype(np.int64)
v = a[..., 0] | (a[..., 1] << 8) | (a[..., 2] << 16)
v = np.where(v >= 1 << 23, v - (1 << 24), v).astype(np.float64)
rows = []
for c in range(nch):
    x = v[:, c]
    p = float(np.mean(x * x))
    row = dict(channel=c, rms_dbfs=round(10 * np.log10(p / (2 ** 23) ** 2), 2) if p > 0 else None,
               min=int(x.min()), max=int(x.max()))
    if p > 0:
        S = np.abs(np.fft.rfft(x - x.mean())) ** 2
        fr = np.fft.rfftfreq(len(x), 1 / 48000)
        for t in (997, 9973):
            row[f"share_{t}"] = round(float(S[(fr > t - 5) & (fr < t + 5)].sum() / S.sum()), 6)
    rows.append(row)
carry = {t: sum(1 for r_ in rows if r_.get(f"share_{t}", 0) > 0.9 and (r_["rms_dbfs"] or -400) > -40) for t in (997, 9973)}
nonsilent = sum(1 for r_ in rows if r_["rms_dbfs"] is not None)
(Path(e["B10_PRIV"]) / "extcap-rows.json").write_text(json.dumps(dict(rows=rows, arecord_rc=r.returncode, stderr=r.stderr), indent=1))
s = dict(seconds=n / 48000, frames=int(n), arecord_rc=r.returncode, channels_carrying_997=carry[997],
         channels_carrying_9973=carry[9973], channels_not_all_zero=nonsilent,
         sha256=hashlib.sha256(f.read_bytes()).hexdigest(), bytes=f.stat().st_size)
json.dump(s, open(out, "w"), indent=1)
print(json.dumps(s))
