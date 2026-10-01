#!/usr/bin/env python3
"""Mutation probe: does the packet's decoder refuse a one-bit data offset?

usage: shift_probe.py <decode_capture.py> <workdir>

Synthesizes the serial TDM8 line the DUT drives: per frame, eight 32-bit
words, MSB first, word = ((tag << 16) | (n & 0xffff)) << 8, tag = slot + 1.
The frame-sync edge opens each frame of P bit clocks. The DUT places slot 0's
MSB D bit clocks after the edge; the receiver (dsp_a) samples from one bit
clock after the edge. Cases: D = 1 (correct), D = 0 (data one bit early),
D = 2 (one bit late), a one-slot rotation, and P = 257 (one idle bit clock
per frame, which a dsp_a receiver cannot see). Each case is written as an
S32_LE raw file and decoded by the packet's decoder; the verdict uses the
page's own criteria (recovered tag == channel + 1, 0 invalid, 0 torn).
"""
import array
import json
import subprocess
import sys

FRAMES = 4096


def words(n):
    return [(((s + 1) << 16) | (n & 0xFFFF)) << 8 for s in range(8)]


def line(D, P, rot=0):
    bits = []
    for n in range(FRAMES + 2):
        fr = [0] * P
        ws = words(n)
        ws = ws[rot:] + ws[:rot]
        for s, w in enumerate(ws):
            for b in range(32):
                pos = D + s * 32 + b
                if pos < P:
                    fr[pos] = (w >> (31 - b)) & 1
                else:  # spills into the next frame's opening bits
                    pass
        bits.append(fr)
    # carry spill of the last bit for D = 2: put it at the start of the next frame
    flat = []
    for fr in bits:
        flat.extend(fr)
    if D + 256 > P:
        # rebuild with spill across the frame boundary
        flat = [0] * (P * (FRAMES + 2) + 8)
        for n in range(FRAMES + 2):
            ws = words(n)
            ws = ws[rot:] + ws[:rot]
            for s, w in enumerate(ws):
                for b in range(32):
                    flat[n * P + D + s * 32 + b] = (w >> (31 - b)) & 1
    return flat


def receive(flat, P):
    out = array.array("I")
    for n in range(FRAMES):
        base = n * P + 1  # dsp_a: first data bit one clock after the edge
        for s in range(8):
            v = 0
            for b in range(32):
                v = (v << 1) | flat[base + s * 32 + b]
            out.append(v)
    return out


def main():
    dec, wd = sys.argv[1], sys.argv[2]
    cases = {"correct_D1": (1, 256, 0), "early_D0": (0, 256, 0), "late_D2": (2, 256, 0),
             "slot_rotation": (1, 256, 1), "idle_bit_P257": (1, 257, 0)}
    res = {}
    for name, (D, P, rot) in cases.items():
        w = receive(line(D, P, rot), P)
        path = f"{wd}/{name}.raw"
        with open(path, "wb") as f:
            w.tofile(f)
        d = json.loads(subprocess.run([sys.executable, dec, path], capture_output=True, text=True, check=True).stdout)
        tags_ok = all(pc["tags"] == {str(pc["soc_channel"] + 1): FRAMES} for pc in d["per_channel"])
        invalid = sum(pc["non_pattern_words"] for pc in d["per_channel"])
        zero = sum(pc["zero_words"] for pc in d["per_channel"])
        verdict = "PASS" if tags_ok and invalid == 0 and zero == 0 and d["torn_frames"] == 0 else "REFUSED"
        res[name] = dict(D=D, P=P, rot=rot, verdict=verdict, torn=d["torn_frames"], invalid=invalid, zero=zero,
                         tags={pc["soc_channel"]: pc["tags"] for pc in d["per_channel"]},
                         steps=d["ordinal_steps"])
    print(json.dumps(res, indent=1))
    exp = {"correct_D1": "PASS", "early_D0": "REFUSED", "late_D2": "REFUSED", "slot_rotation": "REFUSED",
           "idle_bit_P257": "PASS"}
    ok = all(res[k]["verdict"] == v for k, v in exp.items())
    print("PROBE", "AS_EXPECTED" if ok else "UNEXPECTED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
