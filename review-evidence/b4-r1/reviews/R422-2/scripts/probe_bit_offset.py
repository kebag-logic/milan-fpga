#!/usr/bin/env python3
"""Independent one-bit-offset probe for the #451 timing page's framing claims.

usage: probe_bit_offset.py <decode_capture.py> <workdir>

Synthesises the page's pattern (tag t = c + 1 in slot c, bits 31:8 =
(t << 16) | (n & 0xffff), bits 7:0 zero) as one continuous MSB-first TDM8
serial line, 8 x 32 bits per frame. A receiver with the correct data delay
reads it aligned. "One bit early" is the DUT's data starting one bit clock
earlier than the receiver expects (receiver word = line bits shifted left by
one, the next word's MSB entering at bit 0). "One bit late" is the data
starting one bit clock later (the previous word's LSB entering at bit 31).
Each case is written as S32_LE and decoded with the lane packet's decoder,
and also judged by this script's own per-check counts.
"""
import json, subprocess, sys, os, struct, hashlib

dec, work = sys.argv[1], sys.argv[2]
os.makedirs(work, exist_ok=True)
# ordinals: cross bit 15 and wrap 0xffff -> 0
ords = list(range(0x7ff0, 0x8010)) + list(range(0xfff0, 0x10000)) + list(range(0, 0x10))
N = len(ords)

def word(t, n):
    return (((t << 16) | (n & 0xFFFF)) << 8) & 0xFFFFFFFF

line = []  # list of bits, MSB first
for n in ords:
    for c in range(8):
        w = word(c + 1, n)
        line.extend((w >> (31 - b)) & 1 for b in range(32))

def frames_from(bits):
    out = []
    for f in range(N):
        fr = []
        for c in range(8):
            base = (f * 8 + c) * 32
            v = 0
            for b in range(32):
                v = (v << 1) | bits[base + b]
            fr.append(v)
        out.append(fr)
    return out

cases = {
    "aligned": line,
    # data one bit early: the receiver's window starts one bit into the line
    "early": line[1:] + [0],
    # data one bit late: the receiver's window starts one bit before the line
    # (the previous frame's slot 7 LSB, which the pattern makes 0)
    "late": [0] + line[:-1],
}

def own_checks(frs):
    r = dict(torn=0, low_byte_words=0, zero_words=0, tag_out_of_range_words=0,
             wrong_channel_tag_words=0, steps={})
    prev = None
    for fr in frs:
        ordset = set()
        for c, v in enumerate(fr):
            if v == 0:
                r["zero_words"] += 1; continue
            t, lo = v >> 24, v & 0xFF
            if lo: r["low_byte_words"] += 1
            if not 1 <= t <= 8: r["tag_out_of_range_words"] += 1
            elif t != c + 1: r["wrong_channel_tag_words"] += 1
            if not lo and 1 <= t <= 8:
                ordset.add((v >> 8) & 0xFFFF)
        if len(ordset) != 1:
            r["torn"] += 1; prev = None; continue
        o = ordset.pop()
        if prev is not None:
            d = (o - prev) & 0xFFFF
            r["steps"][d] = r["steps"].get(d, 0) + 1
        prev = o
    r["steps"] = {str(k): v for k, v in sorted(r["steps"].items())}
    return r

result = dict(frames=N, decoder=dec, decoder_sha256=hashlib.sha256(open(dec, "rb").read()).hexdigest(), cases={})
for name, bits in cases.items():
    frs = frames_from(bits)
    raw = os.path.join(work, f"{name}.raw")
    with open(raw, "wb") as fh:
        for fr in frs:
            fh.write(struct.pack("<8I", *fr))
    d = json.loads(subprocess.run([sys.executable, dec, raw], capture_output=True, text=True, check=True).stdout)
    per = {}
    for ch in d["per_channel"]:
        per[ch["soc_channel"]] = dict(tags=ch["tags"], zero=ch["zero_words"], non_pattern=ch["non_pattern_words"])
    result["cases"][name] = dict(
        decoder=dict(torn_frames=d["torn_frames"], silent=d["silent_frames"],
                     ordinal_steps=d["ordinal_steps"], per_channel=per),
        own=own_checks(frs),
        ch0_first_two_frames_hex=[f"{frs[0][0]:08x}", f"{frs[1][0]:08x}"])
print(json.dumps(result, indent=1))
