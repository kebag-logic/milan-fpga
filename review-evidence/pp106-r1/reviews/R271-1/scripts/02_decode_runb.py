#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Independent reviewer decode of every MSRP MRPDU in the Run B tap capture.

Record layout (read from the file itself): a classic little-endian pcap whose
records each carry a 28-byte tap header -- u32 kind, u32 record length, u32
port, a 64-bit ns timestamp stored as two little-endian u32 words high word
first, u32 frame length, u32 frame length -- followed by the Ethernet frame
(FCS included).

For every MSRP PDU (EtherType 0x22EA) it prints the message list, then checks:
  1. which PDUs carry any LeaveAllEvent, and on which Attribute Types;
  2. for every LeaveAll PDU, whether any type T has a vector WITHOUT
     LeaveAllEvent ahead of the first vector of type T WITH it (the one layout
     the PR processes in DLSDU order rather than LeaveAll-first);
  3. the exact bytes of the switch-port LeaveAll PDU nearest 47.029619 s,
     FCS dropped, compared with the srp_decoder test P transcription.

Usage: 02_decode_runb.py <tap-runB.pcap> <srp_decoder sim_main.cpp>
"""
import re
import struct
import sys

ATTR = {1: "TalkerAdvertise", 2: "TalkerFailed", 3: "Listener", 4: "Domain"}
ALEN = {1: 25, 2: 34, 3: 8, 4: 4}
EV = ["New", "JoinIn", "In", "JoinMt", "Mt", "Lv"]


def records(path):
    data = open(path, "rb").read()
    magic = struct.unpack("<I", data[:4])[0]
    assert magic == 0xA1B2C3D4, hex(magic)
    off = 24
    while off + 16 <= len(data):
        _ts, _tus, incl, _orig = struct.unpack("<IIII", data[off:off + 16])
        off += 16
        rec = data[off:off + incl]
        off += incl
        _kind, _rlen, port = struct.unpack("<III", rec[0:12])
        # 64-bit ns stamp as two little-endian u32 words, HIGH word first
        # (byte 12 steps every 2**32 ns, about 4.3 s, across the file)
        hi, lo = struct.unpack("<II", rec[12:20])
        t_ns = (hi << 32) | lo
        flen = struct.unpack("<I", rec[20:24])[0]
        frame = rec[28:28 + flen]
        yield port, t_ns, frame


def decode_mrpdu(pdu):
    """Return (messages, ok). messages = [(type, [(la, n, fv, events)])]."""
    msgs = []
    i = 1  # ProtocolVersion
    while i + 1 < len(pdu):
        if pdu[i] == 0 and pdu[i + 1] == 0:
            return msgs, True, i + 2
        t, alen = pdu[i], pdu[i + 1]
        if t not in ALEN or ALEN[t] != alen:
            return msgs, False, i
        i += 2
        _ll = struct.unpack(">H", pdu[i:i + 2])[0]
        i += 2
        vecs = []
        while True:
            vh = struct.unpack(">H", pdu[i:i + 2])[0]
            i += 2
            if vh == 0:
                break
            la, n = vh >> 13, vh & 0x1FFF
            fv = pdu[i:i + alen]
            i += alen
            evs = []
            nb3 = (n + 2) // 3
            for b in pdu[i:i + nb3]:
                evs += [b // 36, (b // 6) % 6, b % 6]
            i += nb3
            evs = evs[:n]
            fps = []
            if t == 3:
                nb4 = (n + 3) // 4
                for b in pdu[i:i + nb4]:
                    fps += [(b >> 6) & 3, (b >> 4) & 3, (b >> 2) & 3, b & 3]
                i += nb4
                fps = fps[:n]
            vecs.append((la, n, fv, evs, fps))
        msgs.append((t, vecs))
    return msgs, False, i


def fmt(msgs):
    out = []
    for t, vecs in msgs:
        for la, n, fv, evs, fps in vecs:
            e = ",".join(EV[x] if x < 6 else "?%d" % x for x in evs)
            out.append("%s[LA=%d n=%d fv=%s %s%s]" % (
                ATTR[t], la, n, fv.hex() if n else "(%dB)" % len(fv), e,
                (" fp=" + ",".join(map(str, fps))) if fps else ""))
    return " ".join(out)


def main():
    pcap, sim = sys.argv[1], sys.argv[2]
    t0 = None
    pdus = []
    for port, t_ns, fr in records(pcap):
        if t0 is None:
            t0 = t_ns
        if fr[12:14] != b"\x22\xea":
            continue
        pdus.append(((t_ns - t0) / 1e9, port, fr[6:12].hex(":"), fr))
    print("== every MSRP MRPDU: tap s, port, source MAC, messages ==")
    la_pdus = []
    bad = 0
    for t, port, sa, fr in pdus:
        msgs, ok, end = decode_mrpdu(fr[14:])
        if not ok:
            bad += 1
        print("%10.6f p%d %s %s%s" % (t, port, sa, fmt(msgs), "" if ok else " MALFORMED"))
        if any(v[0] for _, vecs in msgs for v in vecs):
            la_pdus.append((t, port, sa, fr, msgs, end))
    print("\n== totals: %d MSRP PDUs, %d malformed ==" % (len(pdus), bad))
    by_sa = {}
    for _, _, sa, _ in pdus:
        by_sa[sa] = by_sa.get(sa, 0) + 1
    print("   per source:", by_sa)

    print("\n== LeaveAll PDUs: flagged types, and the unflagged-first layout ==")
    unflagged_first = 0
    for t, port, sa, fr, msgs, _ in la_pdus:
        flagged, seen_unflagged, hit = set(), set(), []
        for ty, vecs in msgs:
            for v in vecs:
                if v[0]:
                    if ty not in flagged and ty in seen_unflagged:
                        hit.append(ATTR[ty])
                    flagged.add(ty)
                else:
                    seen_unflagged.add(ty)
        unflagged_first += bool(hit)
        print("%10.6f p%d %s flagged=%s layout=%s unflagged-first=%s" % (
            t, port, sa, sorted(ATTR[x] for x in flagged),
            "".join("[%s LA=%s]" % (ATTR[ty][:6], "".join(str(v[0]) for v in vecs))
                    for ty, vecs in msgs), hit or "none"))
    print("   LeaveAll PDUs with a type-T unflagged vector ahead of its first flagged one:",
          unflagged_first)

    # 3. the switch-port LeaveAll PDU nearest 47.029619 s vs the test transcription
    cand = min(la_pdus, key=lambda r: abs(r[0] - 47.029619))
    t, port, sa, fr, msgs, end = cand
    mrpdu = fr[14:14 + end]
    print("\n== switch LeaveAll PDU at %.6f s p%d %s: %d B MRPDU (frame %d B incl. FCS) =="
          % (t, port, sa, len(mrpdu), len(fr)))
    print("   ", mrpdu.hex())
    src = open(sim).read()
    m = re.search(r"the_run_b_switch_leave_all_strobes_each_type_ahead_of_its_events\(\) \{"
                  r".*?std::vector<uint8_t> p = \{(.*?)\};", src, re.S)
    body = re.sub(r"//[^\n]*", "", m.group(1))
    want = bytes(int(x, 16) for x in re.findall(r"0x([0-9a-fA-F]{2})", body))
    print("   test P transcription %d B, equal to capture MRPDU: %s" % (len(want), want == mrpdu))
    tail = fr[14 + end:]
    print("   bytes after the MRPDU EndMark in the frame (padding + FCS): %d" % len(tail))


if __name__ == "__main__":
    main()
