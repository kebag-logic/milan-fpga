#!/usr/bin/env python3
"""Lane B8: is the known tone present at the DUT's TDM output? (offline, read-only)

usage: b8_proof.py <mcasp-all.raw> <out.json>

The file is McASP0's capture of the DUT's TDM output (8 channels, S32_LE, the 24-bit sample
in bits 31:8) that probe_b8.py recorded while the tone played into the reference peer's
talker inputs and the peer's talker was bound to the DUT's STREAM_INPUT 0 with four identity
mappings. Per channel: RMS level in dBFS, and for each of the two tones (997 Hz, 9,973 Hz)
the share of the channel's power within +-5 Hz of the tone. A channel carries a tone when
that share exceeds 0.9 at a level above -40 dBFS. For a channel that carries a tone, every
whole one-second block is graded with b6_thdn.block_metrics (lane B6's fit, THD+N, SNR and
frequency offset) at that tone. The verdict is TONE PRESENT when the 997 Hz tone is on one
channel and the 9,973 Hz tone on another, each at -40 dBFS or more.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import b6_thdn as A  # noqa: E402

FS = 48000
TONES = (997, 9973)

raw = np.fromfile(sys.argv[1], dtype="<i4")
n = len(raw) // 8
x = (raw[:n * 8].reshape(n, 8) >> 8).astype(np.float64)
out = dict(frames=int(n), seconds=n / FS, channels=[])
found = {}
for c in range(8):
    v = x[:, c]
    p = float(np.mean(v * v))
    lvl = 10 * np.log10(p / (2 ** 23) ** 2) if p > 0 else -400.0
    row = dict(channel=c, rms_dbfs=round(lvl, 2), nonzero=int(np.count_nonzero(v)), min=int(v.min()), max=int(v.max()))
    if p > 0:
        S = np.abs(np.fft.rfft(v - v.mean())) ** 2
        f = np.fft.rfftfreq(len(v), 1 / FS)
        tot = S.sum()
        for t in TONES:
            share = float(S[(f > t - 5) & (f < t + 5)].sum() / tot) if tot > 0 else 0.0
            row[f"share_{t}"] = round(share, 6)
            if share > 0.9 and lvl > -40:
                found.setdefault(t, c)
                blocks = [A.block_metrics(v[i * FS:(i + 1) * FS], t) for i in range(n // FS)]
                row[f"blocks_{t}"] = [{k: round(float(b[k]), 4 if k != "ppm" else 6) for k in
                                      ("level_dbfs", "thdn_db", "snr_db", "ppm")} for b in blocks]
    out["channels"].append(row)
out["tone_channels"] = {str(t): found.get(t) for t in TONES}
ok = all(found.get(t) is not None for t in TONES) and found[TONES[0]] != found[TONES[1]]
out["verdict"] = "TONE PRESENT" if ok else "TONE ABSENT"
json.dump(out, open(sys.argv[2], "w"), indent=1)
for r in out["channels"]:
    print({k: v for k, v in r.items() if not k.startswith("blocks")})
    for t in TONES:
        if f"blocks_{t}" in r:
            print(f"  ch{r['channel']} {t} Hz blocks:", r[f"blocks_{t}"])
print(out["tone_channels"], out["verdict"])
sys.exit(0 if ok else 1)
