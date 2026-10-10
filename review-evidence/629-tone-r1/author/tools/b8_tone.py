#!/usr/bin/env python3
"""Lane B8: the Direction B tone loop, for playback into the reference peer's talker inputs.

Lane B6's tone (b6_tone.py: 997 Hz and 9,973 Hz, start phases 0.7 rad and 2.1 rad, one loop
of 48,000 frames that repeats seamlessly) at -20 dBFS instead of -1 dBFS, laid out for the
tone source's playback: <tone-source-layout>. The playback layout (channel count, bytes per
sample) is private and comes from the environment (PLAY_NCH, PLAY_BPS); the samples are
little-endian two's complement, the 24-bit value in the top bytes of each sample.

usage: b8_tone.py <out.raw>      writes one loop and prints its size and SHA-256
       b8_tone.py --check        prints the tone's own figures (no file)
"""
import hashlib
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import b6_tone as T  # noqa: E402

LEVEL_DBFS = -20.0
AMP = 10 ** (LEVEL_DBFS / 20) * (2 ** 23 - 1)


def tone(f, ph, n=None, rate=1.0):
    """24-bit integer samples at LEVEL_DBFS (b6_tone.tone's phase law, this amplitude)."""
    k = np.arange(T.N if n is None else n, dtype=np.float64)
    if rate == 1.0:
        ph_k = 2 * np.pi * ((f * k.astype(np.int64)) % T.FS) / T.FS + ph
    else:
        ph_k = 2 * np.pi * f * rate * k / T.FS + ph
    return np.round(AMP * np.sin(ph_k)).astype(np.int64)


def loop():
    """(N, 2) int64: the two tones, one loop."""
    return np.stack([tone(T.F0, T.PH0), tone(T.F1, T.PH1)], axis=1)


def play_bytes(nch, bps):
    lp = loop()
    w = np.zeros((T.N, nch), dtype=np.int64)
    <tone-source-channels>
    v = (w << (8 * bps - 24)) & ((1 << (8 * bps)) - 1)
    b = np.zeros((T.N, nch, bps), dtype=np.uint8)
    for i in range(bps):
        b[:, :, i] = (v >> (8 * i)) & 0xFF
    return b.tobytes()


if __name__ == "__main__":
    lp = loop()
    fig = dict(frames=T.N, level_dbfs=LEVEL_DBFS, peak=[int(np.abs(lp[:, c]).max()) for c in (0, 1)],
               freqs_hz=[T.F0, T.F1])
    if sys.argv[1] == "--check":
        print(fig)
        sys.exit(0)
    nch, bps = int(os.environ["PLAY_NCH"]), int(os.environ["PLAY_BPS"])
    b = play_bytes(nch, bps)
    open(sys.argv[1], "wb").write(b)
    fig.update(bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
    print(fig)
