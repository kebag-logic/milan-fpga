#!/usr/bin/env python3
"""Fault probe for the #451 framing claim, offline, no bench access.

usage: probe_bit_offset.py <decode_capture.py> <scratch_dir>

Builds the first-light pattern as a TDM8 serial bit stream (eight 32-bit slots,
MSB first, word for tag t and ordinal n = ((t << 16) | (n & 0xffff)) << 8),
then models a receiver that frames its words r bits away from the data:
  r =  0  receiver aligned with the data (the dsp_a, one-bit-delay case);
  r = +1  receiver one bit late, i.e. the data arrives one BCLK early;
  r = -1  receiver one bit early, i.e. the data arrives one BCLK late;
  r = +32 a whole-slot rotation.
Plus two content faults on aligned data: one torn frame, one repeated frame.
Each case is written as 8 x S32_LE and run through the packet's own decoder;
the script prints which checks fire for each case.
"""
import json
import os
import struct
import subprocess
import sys

FRAMES = 4096
N0 = 21403  # the run's first ordinal, to cover a 16-bit wrap region as well


def word(t, n):
    return (((t << 16) | (n & 0xFFFF)) << 8) & 0xFFFFFFFF


def frames_words(ords):
    return [[word(c + 1, n) for c in range(8)] for n in ords]


def to_bits(fw):
    bits = []
    for fr in fw:
        for w in fr:
            bits.extend((w >> (31 - i)) & 1 for i in range(32))
    return bits


def receive(bits, r, nframes):
    out = []
    for f in range(nframes):
        fr = []
        for s in range(8):
            p = f * 256 + s * 32 + r
            v = 0
            for i in range(32):
                q = p + i
                v = (v << 1) | (bits[q] if 0 <= q < len(bits) else 0)
            fr.append(v)
        out.append(fr)
    return out


def write_raw(path, fw):
    with open(path, "wb") as fh:
        for fr in fw:
            fh.write(struct.pack("<8I", *fr))


def run(dec, path):
    p = subprocess.run([sys.executable, dec, path], capture_output=True, text=True, check=True)
    d = json.loads(p.stdout)
    return dict(
        frames=d["frames"], torn=d["torn_frames"], silent=d["silent_frames"],
        tags=[c["tags"] for c in d["per_channel"]],
        invalid=[c["non_pattern_words"] for c in d["per_channel"]],
        zero=[c["zero_words"] for c in d["per_channel"]],
        steps=d["ordinal_steps"])


def verdict(res):
    ident = all(res["tags"][c] == {str(c + 1): res["frames"]} for c in range(8))
    clean = res["torn"] == 0 and sum(res["invalid"]) == 0 and sum(res["zero"]) == 0
    return "PASS" if ident and clean else "FAIL"


def main():
    dec, sd = sys.argv[1], sys.argv[2]
    os.makedirs(sd, exist_ok=True)
    ords = [N0 + i for i in range(FRAMES + 2)]
    bits = to_bits(frames_words(ords))
    cases = {}
    for name, r in (("aligned_r0", 0), ("data_one_bclk_early_r+1", 1),
                    ("data_one_bclk_late_r-1", -1), ("slot_rotation_r+32", 32)):
        # skip frame 0 so r = -1 reads real preceding bits, not padding
        fw = receive(bits, r + 256, FRAMES)
        path = os.path.join(sd, name + ".raw")
        write_raw(path, fw)
        res = run(dec, path)
        res["verdict"] = verdict(res)
        res["tags"] = [dict(sorted(t.items(), key=lambda kv: int(kv[0]))) for t in res["tags"]]
        cases[name] = res
    base = frames_words(ords[1:FRAMES + 1])
    torn = [list(fr) for fr in base]
    torn[100][5] = word(6, ords[1 + 101])
    rep = [list(fr) for fr in base]
    rep[200] = list(rep[199])
    for name, fw in (("one_torn_frame", torn), ("one_repeated_frame", rep)):
        path = os.path.join(sd, name + ".raw")
        write_raw(path, fw)
        res = run(dec, path)
        res["verdict"] = verdict(res)
        cases[name] = res
    for name, res in cases.items():
        print(name, json.dumps(res, sort_keys=True))


if __name__ == "__main__":
    main()
