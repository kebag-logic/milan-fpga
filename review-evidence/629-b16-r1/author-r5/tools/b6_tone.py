#!/usr/bin/env python3
"""The lane B6 tone loop and its decoder tables.

One loop of 48,000 frames (1 s at 48 kHz), 8 channels, S32_LE, the 24-bit sample in
bits 31:8 (the first-light word layout):
  channel 0: 997 Hz, channel 1: 9,973 Hz, both at -1 dBFS (peak 0.891 x (2^23 - 1)),
  start phases 0.7 rad and 2.1 rad; channels 2-7 zero.
997 and 9,973 are primes and coprime with 48,000, so each tone runs a whole number of
cycles per loop (the loop repeats seamlessly) and its 48,000 phases are all distinct,
which spreads the 24-bit quantization error over the band like noise.

The pair (channel 0, channel 1) of every frame is unique within the loop (checked at
generation), so each captured frame decodes to its loop ordinal; consecutive ordinals
give every discontinuity with its exact size. No frame of the loop is silent.

usage: b6_tone.py <out.raw>      writes the loop and prints its size and SHA-256
"""
import hashlib
import sys

import numpy as np

FS = 48000
N = 48000
F0, F1 = 997, 9973
PH0, PH1 = 0.7, 2.1
AMP = 10 ** (-1 / 20) * (2 ** 23 - 1)


def tone(f, ph, n=None, rate=1.0):
    """24-bit integer samples of one tone; rate != 1 resamples (source clock / capture clock)."""
    k = np.arange(N if n is None else n, dtype=np.float64)
    # exact phase: (f * k mod FS) keeps the argument small for the nominal loop
    if rate == 1.0:
        ph_k = 2 * np.pi * ((f * k.astype(np.int64)) % FS) / FS + ph
    else:
        ph_k = 2 * np.pi * f * rate * k / FS + ph
    return np.round(AMP * np.sin(ph_k)).astype(np.int64)


def loop():
    """(N, 2) int64 array of the two graded channels."""
    return np.stack([tone(F0, PH0), tone(F1, PH1)], axis=1)


def key(c0, c1):
    """48-bit key of a frame from two 24-bit two's-complement words (int64 arrays)."""
    return ((c0 & 0xFFFFFF) << 24) | (c1 & 0xFFFFFF)


def table():
    """Sorted keys and their ordinals, for np.searchsorted decoding."""
    lp = loop()
    k = key(lp[:, 0], lp[:, 1])
    order = np.argsort(k)
    ks = k[order]
    if np.any(np.diff(ks) == 0):
        raise SystemExit("frame pairs are not unique")
    return ks, order


def decode(c0, c1, tab=None):
    """Ordinal per frame, -1 where the pair is not a loop frame."""
    ks, order = table() if tab is None else tab
    k = key(c0, c1)
    i = np.searchsorted(ks, k)
    i = np.clip(i, 0, len(ks) - 1)
    hit = ks[i] == k
    return np.where(hit, order[i], -1)


def raw_bytes():
    lp = loop()
    w = np.zeros((N, 8), dtype=np.int64)
    w[:, 0], w[:, 1] = lp[:, 0], lp[:, 1]
    return ((w << 8) & 0xFFFFFFFF).astype("<u4").tobytes()


if __name__ == "__main__":
    lp = loop()
    ks, order = table()
    silent = int(((lp[:, 0] == 0) & (lp[:, 1] == 0)).sum())
    b = raw_bytes()
    open(sys.argv[1], "wb").write(b)
    print(dict(frames=N, bytes=len(b), sha256=hashlib.sha256(b).hexdigest(), unique_pairs=len(ks),
               silent_frames=silent, peak=[int(np.abs(lp[:, c]).max()) for c in (0, 1)]))
