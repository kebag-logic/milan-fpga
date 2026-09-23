#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer receipt script: independent read of the Run B tap capture.

Usage: runb_msrp_check.py <original.pcap> [<published.pcap>]

1. Walks every record of a classic libpcap file (either byte order, us or ns
   stamps), keeps MSRP frames (EtherType 0x22EA, optionally behind one 802.1Q
   tag), and prints each MRPDU's messages {type, LeaveAllEvent, NumberOfValues}
   with the tap time relative to the first record.
2. Prints the header-stripped MRPDU bytes of the switch's LeaveAll MRPDUs
   nearest 10.429430 s and 47.029619 s (the two the donor tests transcribe),
   so they can be compared with tb/srp_encoder L2 and tb/srp_decoder P.
3. With a second (published, path-redacted) file: lists the records whose
   bytes differ and says whether any of them is an MSRP frame.
No third-party packages.
"""
import struct
import sys


def records(path):
    data = open(path, "rb").read()
    magic = data[:4]
    if magic in (b"\xd4\xc3\xb2\xa1", b"\x4d\x3c\xb2\xa1"):
        end = "<"
    elif magic in (b"\xa1\xb2\xc3\xd4", b"\xa1\xb2\x3c\x4d"):
        end = ">"
    else:
        raise SystemExit("not a classic pcap file")
    nano = magic in (b"\x4d\x3c\xb2\xa1", b"\xa1\xb2\x3c\x4d")
    off = 24
    idx = 0
    while off + 16 <= len(data):
        sec, frac, incl, _orig = struct.unpack(end + "IIII", data[off:off + 16])
        off += 16
        t = sec + frac / (1e9 if nano else 1e6)
        rec = data[off:off + incl]
        # this tap prefixes each frame with a 28-byte record header of seven
        # little-endian 32-bit words: three words, a 64-bit nanosecond stamp
        # stored high word first, then the frame length twice; when present,
        # strip it and use its stamp
        if len(rec) >= 28:
            w = struct.unpack("<7I", rec[:28])
            if w[5] == incl - 28 and w[6] == w[5]:
                t = ((w[3] << 32) | w[4]) / 1e9
                rec = rec[28:]
        yield idx, t, off, rec
        off += incl
        idx += 1


def mrpdu(frame):
    """Return (src MAC, header-stripped MRPDU) for an MSRP frame, else None."""
    if len(frame) < 14:
        return None
    et = struct.unpack(">H", frame[12:14])[0]
    body = frame[14:]
    if et == 0x8100 and len(frame) >= 18:
        et = struct.unpack(">H", frame[16:18])[0]
        body = frame[18:]
    if et != 0x22EA:
        return None
    return frame[6:12].hex(":"), body


ALEN = {1: 25, 2: 34, 3: 8, 4: 4}


def walk(pdu):
    """MSRP MRPDU walk: list of (type, [(la, nov)...]); stops at the EndMark."""
    i = 1                                    # ProtocolVersion
    msgs = []
    while i + 1 < len(pdu):
        if pdu[i] == 0 and pdu[i + 1] == 0:
            return msgs, i + 2
        t, alen = pdu[i], pdu[i + 1]
        ll = (pdu[i + 2] << 8) | pdu[i + 3]
        i += 4
        vecs = []
        while i + 1 < len(pdu):
            if pdu[i] == 0 and pdu[i + 1] == 0:
                i += 2
                break
            la = pdu[i] >> 5
            nov = ((pdu[i] & 0x1F) << 8) | pdu[i + 1]
            i += 2 + alen + (nov + 2) // 3 + ((nov + 3) // 4 if t == 3 else 0)
            vecs.append((la, nov))
        msgs.append((t, alen, ll, vecs))
    return msgs, None


def main():
    orig = sys.argv[1]
    t0 = None
    la_pdus = []
    n_msrp = 0
    for idx, t, _off, fr in records(orig):
        if t0 is None:
            t0 = t
        m = mrpdu(fr)
        if m is None:
            continue
        n_msrp += 1
        src, pdu = m
        msgs, end = walk(pdu)
        if any(v[0] == 1 for (_t, _a, _l, vs) in msgs for v in vs):
            la_pdus.append((t - t0, src, msgs, pdu[:end] if end else pdu))
    print(f"MSRP frames: {n_msrp}; MRPDUs carrying LeaveAll: {len(la_pdus)}")
    for rel, src, msgs, _pdu in la_pdus:
        desc = " ".join(f"[t{t} " + ",".join(f"LA{la}/n{nov}" for la, nov in vs) + "]"
                        for (t, _a, _l, vs) in msgs)
        print(f"  {rel:11.6f} {src} {desc}")
    # per-type scoping evidence: what the switch sends within 5 s of each
    # DUT LeaveAll MRPDU (message types and each vector's LeaveAll/NoV)
    allm = []
    for _idx, t, _off, fr in records(orig):
        m = mrpdu(fr)
        if m is not None:
            allm.append((t - t0, m[0], walk(m[1])[0]))
    print("\nswitch MSRP frames within 5 s after each DUT LeaveAll MRPDU:")
    for rel, src, _msgs, _pdu in la_pdus:
        if src == "3c:c0:c6:fe:02:11":
            continue
        rep = [(r, msgs) for r, s, msgs in allm
               if s == "3c:c0:c6:fe:02:11" and rel < r <= rel + 5.0]
        txt = "; ".join(f"+{(r - rel) * 1e3:.1f} ms " + " ".join(
            f"t{t}:" + ",".join(f"LA{la}/n{nov}" for la, nov in vs)
            for (t, _a, _l, vs) in msgs) for r, msgs in rep)
        print(f"  DUT LA {rel:10.6f}: {len(rep)} switch frame(s): {txt}")
    for want in (10.429430, 47.029619):
        best = min(la_pdus, key=lambda r: abs(r[0] - want))
        print(f"\nLeaveAll MRPDU nearest {want:.6f} s: {best[0]:.6f} s from {best[1]},"
              f" {len(best[3])} B header-stripped through the MRPDU EndMark:")
        b = best[3]
        for k in range(0, len(b), 16):
            print("  " + " ".join(f"{x:02x}" for x in b[k:k + 16]))
    if len(sys.argv) > 2:
        pub = {idx: (off, fr) for idx, _t, off, fr in records(sys.argv[2])}
        diff = []
        for idx, _t, off, fr in records(orig):
            if pub.get(idx, (None, None))[1] != fr:
                diff.append((idx, mrpdu(fr) is not None))
        print(f"\nrecords differing between the two files: {len(diff)};"
              f" MSRP among them: {sum(1 for _i, m in diff if m)}")


if __name__ == "__main__":
    main()
