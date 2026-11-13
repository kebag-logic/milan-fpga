#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Independent decoder of a CPU budget harness log's WIRE lines (reviewer-owned; not derived from the lane's decoder).

WIRE <cycle> <interface> <channel> <frame hex>. The bus clock is read off the log's own MS lines (MS <cycle> <ms> ...).
MSRP frames (EtherType 0x22EA) are decoded per IEEE 802.1Q-2018 10.8 (MRPDU) and 35.2.2 (attribute types and
lengths); MAAP frames (EtherType 0x22F0) per IEEE 1722-2016 Annex B (B.2: message_type, requested_start_address,
requested_count). Prints one line per Talker/Listener/Domain vector value and per MAAP frame, then a summary:
every Talker Failed seen, the first Talker declaration time per StreamID, and every declaring event after a Leave of
the same StreamID. Usage: decode_wire.py LOG [LOG...]
"""
import sys

EVENTS = {0: "New", 1: "JoinIn", 2: "In", 3: "JoinMt", 4: "Mt", 5: "Lv"}
TYPES = {1: "TalkerAdvertise", 2: "TalkerFailed", 3: "Listener", 4: "Domain"}
MAAP = {1: "PROBE", 2: "DEFEND", 3: "ANNOUNCE"}


def cycles_per_ms(lines):
    pts = []
    for ln in lines:
        p = ln.split()
        if len(p) >= 3 and p[0] == "MS":
            pts.append((int(p[1]), int(p[2])))
        if len(pts) >= 3:
            break
    (c1, m1), (c2, m2) = pts[0], pts[-1]
    return (c2 - c1) / (m2 - m1)


def add(atype, v, n):
    """The n-th value of a vector from its FirstValue (IEEE 802.1Q-2018 35.2.2.8, the vector's successive values, and 10.8.2.8): a Talker's StreamID
    and destination_address each incremented by n, a Listener's StreamID by n; a Domain value is returned unchanged
    (its successive values are not used by these frames)."""
    def inc(b, k):
        return (int.from_bytes(b, "big") + k).to_bytes(len(b), "big")
    if n == 0:
        return v
    if atype in (1, 2):
        return inc(v[0:8], n) + inc(v[8:14], n) + v[14:]
    if atype == 3:
        return inc(v, n)
    return v


def mrpdu(b):
    """Yield (type, event, value bytes, leaveall, NumberOfValues) for every value in an MSRP MRPDU (b starts at ProtocolVersion)."""
    lengths = {1: 25, 2: 34, 3: 8, 4: 4}
    k = 1
    while k + 1 < len(b):
        if b[k] == 0 and b[k + 1] == 0:
            return
        atype, alen = b[k], b[k + 1]
        llen = int.from_bytes(b[k + 2:k + 4], "big")
        if lengths.get(atype) != alen:
            raise ValueError(f"attribute type {atype} length {alen}")
        end = k + 4 + llen
        j = k + 4
        while j + 1 < end:
            if b[j] == 0 and b[j + 1] == 0:
                break
            hdr = int.from_bytes(b[j:j + 2], "big")
            la, n = hdr >> 13, hdr & 0x1FFF
            first = bytes(b[j + 2:j + 2 + alen])
            j += 2 + alen
            three = b[j:j + (n + 2) // 3]
            j += (n + 2) // 3
            if atype == 3:
                j += (n + 3) // 4
            evs = []
            for t in three:
                evs += [t // 36, (t // 6) % 6, t % 6]
            for i in range(n):
                yield atype, evs[i], add(atype, first, i), la, n
        k = end


def main(paths):
    for path in paths:
        lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
        cpm = cycles_per_ms(lines)
        first_decl, leaves, after_leave, failed, n_wire = {}, {}, [], [], 0
        print(f"# {path}: {cpm:.0f} cycles a ms")
        for ln in lines:
            p = ln.split()
            if len(p) != 5 or p[0] != "WIRE":
                continue
            n_wire += 1
            t = int(p[1]) / cpm
            ifc = int(p[2])
            fr = bytes.fromhex(p[4])
            et = int.from_bytes(fr[12:14], "big")
            if et == 0x22F0 and fr[14] == 0xFE:
                mt = fr[15] & 0x0F
                start = fr[26:32].hex()
                cnt = int.from_bytes(fr[32:34], "big")
                print(f"{t:11.3f} ms if{ifc} MAAP {MAAP.get(mt, mt)} start {start} count {cnt} src {fr[6:12].hex()}")
            elif et == 0x22F0 and fr[14] == 0xFC:
                # IEEE 1722.1-2021 8.2.1: message_type, status, talker_unique_id at 36..38 of the AVTPDU (12-octet header, three 8-octet IDs)
                mt, status = fr[15] & 0x0F, fr[16] >> 3
                print(f"{t:11.3f} ms if{ifc} ACMP message_type {mt} status {status} "
                      f"talker_uid {int.from_bytes(fr[14 + 36:14 + 38], 'big')}")
            elif et == 0x22F0:
                print(f"{t:11.3f} ms if{ifc} AVTP control subtype {fr[14]:#04x}")
            elif et == 0x22EA:
                for atype, ev, val, la, nv in mrpdu(fr[14:]):
                    name = TYPES[atype]
                    if atype in (1, 2):
                        sid, da, vid = val[0:8].hex(), val[8:14].hex(), int.from_bytes(val[14:16], "big")
                        extra = f" code {val[33]}" if atype == 2 else ""
                        print(f"{t:11.3f} ms if{ifc} {name} stream {sid} DA {da} vid {vid} {EVENTS[ev]}{extra}"
                              f"{' LeaveAll' if la else ''} (vector of {nv})")
                        key = (ifc, sid)
                        if atype == 2:
                            failed.append((t, ifc, sid, val[33]))
                        if ev == 5:
                            leaves.setdefault(key, t)
                        elif ev in (0, 1, 3):
                            first_decl.setdefault(key, (t, da))
                            if key in leaves:
                                after_leave.append((t, ifc, sid, EVENTS[ev], da))
                    elif atype == 3:
                        print(f"{t:11.3f} ms if{ifc} Listener stream {val.hex()} {EVENTS[ev]}")
                    else:
                        print(f"{t:11.3f} ms if{ifc} Domain {val.hex()} {EVENTS[ev]}{' LeaveAll' if la else ''}")
        print(f"SUMMARY {path}: WIRE lines {n_wire}; Talker Failed values {len(failed)}; Talker StreamIDs "
              f"{len(first_decl)}; declaring events after a Leave of the same StreamID {len(after_leave)}")
        for key, (t, da) in sorted(first_decl.items(), key=lambda kv: kv[1][0]):
            lv = leaves.get(key)
            print(f"  if{key[0]} {key[1]}: first declared {t:.3f} ms DA {da}; first Leave "
                  f"{'%.3f ms' % lv if lv is not None else 'none'}")
        for item in after_leave:
            print(f"  AFTER-LEAVE {item}")
        for item in failed:
            print(f"  FAILED {item}")


if __name__ == "__main__":
    main(sys.argv[1:])
