#!/usr/bin/env python3
"""bitdiff.py A.bit B.bit: where two Xilinx 7-series .bit files differ, byte by byte.

The .bit header (its TLV fields: design name with UserID/Version/SW_CRC/SW_HDR_SHA256, part, ...) is read, then the
configuration packet stream after the sync word 0xAA995566: each type-1/type-2 packet's register and payload. The
FDRI payload is the frame data, 101 32-bit words a frame (UG470, 7-series frame length). Every differing byte is
classified as:
  header        the .bit TLV header before the sync word
  packet        a packet header or a non-FDRI register write; the register is named (CRC, FAR, CMD, ...)
  frame         FDRI frame data: the frame index from the first FDRI word, the word within the frame (word 50 holds
                the frame's ECC bits) and the bits that differ
Exit 0 when the files are equal, 1 when they differ, 2 when the two streams do not have the same packet structure
(lengths or registers), which is printed."""
import struct
import sys
from pathlib import Path

REGS = {0: "CRC", 1: "FAR", 2: "FDRI", 3: "FDRO", 4: "CMD", 5: "CTL0", 6: "MASK", 7: "STAT", 8: "LOUT", 9: "COR0",
        10: "MFWR", 11: "CBC", 12: "IDCODE", 13: "AXSS", 14: "COR1", 16: "WBSTAR", 17: "TIMER", 22: "BOOTSTS",
        24: "CTL1", 31: "BSPI"}
FRAME_WORDS = 101


def parse(path):
    b = Path(path).read_bytes()
    sync = b.find(b"\xaa\x99\x55\x66")
    assert sync > 0, f"{path}: no sync word"
    header_end = sync
    i = sync + 4
    regions = []  # (start, end, kind, reg)
    last_reg = None
    while i + 4 <= len(b):
        w, = struct.unpack_from(">I", b, i)
        typ = w >> 29
        if typ == 1:
            op, reg, cnt = (w >> 27) & 3, (w >> 13) & 0x3FFF, w & 0x7FF
            regions.append((i, i + 4, "packet", f"type1 hdr {REGS.get(reg, reg)} op{op} n{cnt}"))
            last_reg = reg
            if cnt:
                kind = "fdri" if reg == 2 else "packet"
                regions.append((i + 4, i + 4 + 4 * cnt, kind, REGS.get(reg, str(reg))))
            i += 4 + 4 * cnt
        elif typ == 2:
            cnt = w & 0x7FFFFFF
            regions.append((i, i + 4, "packet", f"type2 hdr {REGS.get(last_reg, last_reg)} n{cnt}"))
            kind = "fdri" if last_reg == 2 else "packet"
            regions.append((i + 4, i + 4 + 4 * cnt, kind, REGS.get(last_reg, str(last_reg))))
            i += 4 + 4 * cnt
        else:
            regions.append((i, i + 4, "packet", f"word 0x{w:08x}"))
            i += 4
    return b, header_end, regions


def main():
    a, ha, ra = parse(sys.argv[1])
    b, hb, rb = parse(sys.argv[2])
    print(f"A {len(a)} B, header {ha} B, {len(ra)} regions; B {len(b)} B, header {hb} B, {len(rb)} regions")
    shape_a = [(s - ha, e - ha, k, r) for s, e, k, r in ra]
    shape_b = [(s - hb, e - hb, k, r) for s, e, k, r in rb]
    if len(a) != len(b) or ha != hb or shape_a != shape_b:
        print("STRUCTURE DIFFERS")
        return 2
    diff = [i for i in range(len(a)) if a[i] != b[i]]
    print(f"differing bytes: {len(diff)}")
    if not diff:
        return 0
    fdri = [(s, e) for s, e, k, _r in ra if k == "fdri"]
    frames = {}
    other = []
    for i in diff:
        if i < ha:
            other.append(("header", i, None))
            continue
        hit = None
        for s, e, k, r in ra:
            if s <= i < e:
                hit = (s, k, r)
                break
        if hit and hit[1] == "fdri":
            base = hit[0]
            word = (i - base) // 4
            frame, fword = divmod(word, FRAME_WORDS)
            frames.setdefault(frame, set()).add(fword)
        else:
            other.append(("packet", i, hit[2] if hit else "beyond the stream"))
    for kind, i, what in other:
        print(f"  {kind:<7} offset {i:>8}  A {a[i]:02x} B {b[i]:02x}  {what or ''}")
    total_frames = sum((e - s) // 4 for s, e in fdri) // FRAME_WORDS
    print(f"  frame data: {len(frames)} of {total_frames} frames differ (FDRI payload starts at byte {fdri[0][0]})")
    for fr in sorted(frames):
        words = sorted(frames[fr])
        base = fdri[0][0] + 4 * FRAME_WORDS * fr
        bits = 0
        for wd in words:
            wa, = struct.unpack_from(">I", a, base + 4 * wd)
            wb, = struct.unpack_from(">I", b, base + 4 * wd)
            bits += bin(wa ^ wb).count("1")
        ecc = " (word 50: the frame's ECC)" if 50 in words else ""
        print(f"    frame {fr:>6}: words {words}{ecc}, {bits} bit(s)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
