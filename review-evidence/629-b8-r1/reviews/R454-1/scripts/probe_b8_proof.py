#!/usr/bin/env python3
"""Disposable probe of lane B8's b8_proof.py: planted captures, expected verdicts.

usage: probe_b8_proof.py <dir holding b8_proof.py and b6_thdn.py>
Writes synthetic 8-channel S32_LE captures (24-bit sample in bits 31:8), 10 s at 48 kHz.
"""
import json, os, subprocess, sys
import numpy as np

d = sys.argv[1]
FS, N = 48000, 480000
t = np.arange(N) / FS
rng = np.random.default_rng(629)

def write(name, chans):
    x = np.zeros((N, 8), dtype=np.int64)
    for c, v in chans.items():
        x[:, c] = v
    raw = (np.clip(x, -2**23, 2**23 - 1).astype(np.int64) << 8).astype("<i4")
    p = os.path.join(d, name + ".raw")
    raw.tofile(p)
    return p

amp = 2**23 * 10 ** (-20 / 20) * np.sqrt(2)  # -20 dBFS RMS
floor = lambda: rng.integers(-2, 1, N)          # the observed -2..0 LSB floor
tone = lambda f: np.round(amp * np.sin(2 * np.pi * f * t)).astype(np.int64)
cases = {
    "idle_floor": ({0: floor(), 1: floor(), 2: floor(), 3: floor()}, "TONE ABSENT"),
    "tones_ch0_ch1": ({0: tone(997), 1: tone(9973), 2: floor(), 3: floor()}, "TONE PRESENT"),
    "tones_ch2_ch3": ({0: floor(), 1: floor(), 2: tone(997), 3: tone(9973)}, "TONE PRESENT"),
    "tones_at_minus50": ({0: tone(997) // 31, 1: tone(9973) // 31}, "TONE ABSENT"),
    "one_tone_only": ({0: tone(997), 1: floor()}, "TONE ABSENT"),
}
bad = 0
for name, (chans, want) in cases.items():
    p = write(name, chans)
    r = subprocess.run([sys.executable, os.path.join(d, "b8_proof.py"), p, p + ".json"],
                       capture_output=True, text=True)
    got = json.load(open(p + ".json"))["verdict"]
    lv = [c["rms_dbfs"] for c in json.load(open(p + ".json"))["channels"][:4]]
    ok = got == want
    bad += not ok
    print(f"{'OK ' if ok else 'BAD'} {name}: verdict={got} rc={r.returncode} want={want} levels_ch0-3={lv}")
    os.remove(p)
print("problems=%d" % bad)
sys.exit(1 if bad else 0)
