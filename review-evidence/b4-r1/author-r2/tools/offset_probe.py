#!/usr/bin/env python3
"""Check the page's per-direction one-bit-offset wording with the packet decoder.

usage: offset_probe.py <decode_capture.py> <scratch_dir>

Synthesizes the first-light pattern as a TDM8 line (256 bit clocks per frame,
eight 32-bit slots, MSB first). The transmitter starts each frame's data D bit
clocks after the frame-sync edge; the receiver expects D = 1 (dsp_a). Ordinals
start at 0x7f00 so bit 15 changes inside the run, and the sequence carries one
repeat and one skip. Each case goes through the packet's own decoder.
"""
import json
import os
import struct
import subprocess
import sys

FRAMES = 4096
BITS = 256


def ordinals():
    seq, n = [], 0x7F00
    for f in range(FRAMES):
        seq.append(n & 0xFFFF)
        if f == 1000:
            continue            # repeat: the next frame carries the same ordinal
        n += 2 if f == 2000 else 1   # skip one ordinal after frame 2000
    return seq


def line(seq, d):
    bits = bytearray(FRAMES * BITS + 2)
    for f, n in enumerate(seq):
        for s in range(8):
            w = (((s + 1) << 16) | n) << 8
            base = f * BITS + s * 32 + d
            for b in range(32):
                bits[base + b] = (w >> (31 - b)) & 1
    return bits


def receive(bits):
    out = bytearray()
    for f in range(FRAMES):
        for s in range(8):
            base = f * BITS + s * 32 + 1
            v = 0
            for b in range(32):
                v = (v << 1) | bits[base + b]
            out += struct.pack("<I", v)
    return bytes(out)


def main():
    dec, scratch = sys.argv[1], sys.argv[2]
    seq = ordinals()
    res = {}
    for name, d in (("aligned", 1), ("one_bit_early", 0), ("one_bit_late", 2)):
        raw = os.path.join(scratch, name + ".raw")
        open(raw, "wb").write(receive(line(seq, d)))
        r = json.loads(subprocess.run([sys.executable, dec, raw], check=True,
                                      capture_output=True, text=True).stdout)
        res[name] = dict(
            frames=r["frames"], torn=r["torn_frames"], silent=r["silent_frames"],
            ordinal_steps=r["ordinal_steps"], jump_sizes=r["jump_sizes"],
            tags=[c["tags"] for c in r["per_channel"]],
            non_pattern=[c["non_pattern_words"] for c in r["per_channel"]],
            zero=[c["zero_words"] for c in r["per_channel"]])
        os.remove(raw)
    # low-byte versus tag-range split of the non-pattern words, per case
    for name, d in (("one_bit_early", 0), ("one_bit_late", 2)):
        w = receive(line(seq, d))
        lo = rng = 0
        for (v,) in struct.iter_unpack("<I", w):
            if v & 0xFF:
                lo += 1
            if v and not 1 <= v >> 24 <= 8:
                rng += 1
        res[name]["words_low_byte_nonzero"] = lo
        res[name]["words_tag_outside_1_8"] = rng
    print(json.dumps(res, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
