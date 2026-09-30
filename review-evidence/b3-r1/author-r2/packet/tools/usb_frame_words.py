#!/usr/bin/env python3
"""Print the eight 32-bit words of one frame of an 8-channel S32_LE capture
taken on the host's USB Audio card (offline, no bench access).

usage: usb_frame_words.py <raw> <sha256> <frame> [<json_out>]

The raw file is read whole and its SHA-256 must equal <sha256>, so the words
are tied to the capture the findings page identifies. Each word is split as
the first-light pattern defines it: tag bits 31:24, 16-bit frame ordinal bits
23:8, low byte bits 7:0. The fractional ordinal is bits 23:0 / 256, as
grade_usb.py reads it.
"""
import array
import hashlib
import json
import sys


def main():
    path, want, frame = sys.argv[1], sys.argv[2], int(sys.argv[3])
    data = open(path, "rb").read()
    got = hashlib.sha256(data).hexdigest()
    if got != want:
        sys.exit(f"sha256 mismatch: {got} != {want}")
    w = array.array("I")
    w.frombytes(data)
    if sys.byteorder != "little":
        w.byteswap()
    frames = len(w) // 8
    if not 0 <= frame < frames:
        sys.exit(f"frame {frame} outside 0..{frames - 1}")
    prev = w[(frame - 1) * 8:frame * 8] if frame else None
    fr = w[frame * 8:(frame + 1) * 8]
    words = []
    for c, v in enumerate(fr):
        words.append(dict(channel=c, word=f"{v:08x}", tag=v >> 24, ordinal=f"{(v >> 8) & 0xffff:04x}",
                          low_byte=f"{v & 0xff:02x}", fractional_ordinal=round((v & 0xffffff) / 256.0, 6)))
    res = dict(file=path.split("/")[-1], bytes=len(data), sha256=got, frames=frames, frame=frame,
               byte_offset=frame * 32,
               previous_frame_silent=(prev is not None and not any(prev)),
               in_order=all(x["tag"] == x["channel"] + 1 for x in words),
               words=words)
    text = json.dumps(res, indent=1)
    print(text)
    if len(sys.argv) > 4:
        with open(sys.argv[4], "w") as f:
            f.write(text + "\n")


if __name__ == "__main__":
    main()
