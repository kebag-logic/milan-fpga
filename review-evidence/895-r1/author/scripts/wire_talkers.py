#!/usr/bin/env python3
"""Decode a CPU budget harness log's WIRE lines: MAAP ANNOUNCEs (IEEE 1722-2016 B.2) and MSRP Talker attributes
(IEEE 802.1Q-2018 35.2.2.8, 10.8.2.10 ThreeVector events), and grade the #895 evidence:
  - no Talker declared before the first ACMP probe;
  - each source's Talker Advertise carries MAAP's announced start + n;
  - each source's Talker is withdrawn (Lv) after the probe window, and no Advertise follows its Leave.
usage: wire_talkers.py LOG [--sources N] [--clock-hz 100000000]
"""
from __future__ import annotations

import argparse
import sys

EVENTS = ("New", "JoinIn", "In", "JoinMt", "Mt", "Lv")
TYPES = {1: "TalkerAdvertise", 2: "TalkerFailed", 3: "Listener", 4: "Domain"}
LENGTHS = {1: 25, 2: 34, 3: 8, 4: 4}


def be(b: bytes) -> int:
    return int.from_bytes(b, "big")


def msrp(pdu: bytes):
    """Yield (type, value bytes, event, leaveall) per attribute of an MSRP MRPDU (after the ethertype)."""
    p = 1  # ProtocolVersion
    while p + 2 <= len(pdu):
        atype, alen = pdu[p], pdu[p + 1]
        if atype == 0:
            return
        listlen = be(pdu[p + 2:p + 4])
        end = p + 4 + listlen
        q = p + 4
        while q + 2 <= end:
            hdr = be(pdu[q:q + 2])
            if hdr == 0:
                q += 2
                break
            leaveall, nvals = hdr >> 13, hdr & 0x1fff
            first = pdu[q + 2:q + 2 + alen]
            q += 2 + alen
            nthree = (nvals + 2) // 3
            three = pdu[q:q + nthree]
            q += nthree
            if atype == 3:
                q += (nvals + 3) // 4
            for k in range(nvals):
                packed = three[k // 3]
                e = (packed // 36, packed // 6 % 6, packed % 6)[k % 3]
                value = bytearray(first)
                if k:  # FirstValue + k: the StreamID's last bytes for a Talker (35.2.2.8.1)
                    if atype in (1, 2):
                        sid = be(value[0:8]) + k
                        da = be(value[8:14]) + k
                        value[0:8] = sid.to_bytes(8, "big")
                        value[8:14] = da.to_bytes(6, "big")
                    else:
                        v = be(value) + k
                        value = bytearray(v.to_bytes(len(value), "big"))
                yield atype, bytes(value), EVENTS[e] if e < 6 else str(e), leaveall
        p = end


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("log")
    ap.add_argument("--sources", type=int, required=True)
    ap.add_argument("--clock-hz", type=int, default=100_000_000)
    a = ap.parse_args()
    announces: dict[int, tuple[int, int]] = {}
    talkers = []  # (ms, if, type, sid, da, event)
    probes = []
    for line in open(a.log, errors="replace"):
        parts = line.split()
        if not parts:
            continue
        if parts[0] == "MARK" and len(parts) >= 3:
            ms = int(parts[1]) * 1000.0 / a.clock_hz
            print(f"{ms:10.3f} ms MARK {parts[2]}")
            if parts[2].startswith("srp.talker_declare"):
                probes.append(ms)
            continue
        if parts[0] != "WIRE" or len(parts) < 5:
            continue
        cyc, iface, frame = int(parts[1]), int(parts[2]), bytes.fromhex(parts[4])
        ms = cyc * 1000.0 / a.clock_hz
        etype = be(frame[12:14])
        body = frame[14:]
        if etype == 0x22f0 and body[0] == 0xfe:
            mtype = body[1] & 0x0f
            if mtype == 3:  # ANNOUNCE
                start, count = be(body[12:18]), be(body[18:20])
                if announces.get(iface) != (start, count):
                    print(f"{ms:10.3f} ms if{iface} MAAP ANNOUNCE start {start:012x} count {count}")
                announces[iface] = (start, count)
        elif etype == 0x22ea:
            for atype, value, ev, la in msrp(body):
                if atype in (1, 2):
                    sid, da = be(value[0:8]), be(value[8:14])
                    talkers.append((ms, iface, atype, sid, da, ev, la, announces.get(iface, (None, 0))[0]))
    # print every Talker attribute's first appearance per (if, type, sid, da, event) run
    last = {}
    for ms, iface, atype, sid, da, ev, la, _ in talkers:
        key = (iface, atype, sid)
        if last.get(key) != (da, ev):
            print(f"{ms:10.3f} ms if{iface} {TYPES[atype]} stream {sid:016x} DA {da:012x} {ev}"
                  f"{' (LeaveAll)' if la else ''}")
        last[key] = (da, ev)
    failures = 0
    for n in range(a.sources):
        sid_low = n
        adv = [t for t in talkers if t[2] == 1 and (t[3] & 0xffff) == sid_low]
        if not adv:
            print(f"FAIL s{n}: no Talker Advertise on the wire")
            failures += 1
            continue
        first = adv[0]
        start = first[7]
        ok_da = start is not None and first[4] == start + n
        print(f"{'PASS' if ok_da else 'FAIL'} s{n}: first Advertise at {first[0]:.3f} ms on if{first[1]}, "
              f"DA {first[4]:012x}, MAAP start {start:012x} + {n}" if start is not None else
              f"FAIL s{n}: no MAAP ANNOUNCE on if{first[1]}")
        failures += not ok_da
        leaves = [t for t in adv if t[5] == "Lv"]
        if not leaves:
            print(f"FAIL s{n}: no Leave of its Advertise")
            failures += 1
            continue
        lv = leaves[0]
        after = [t for t in adv if t[0] > lv[0] and t[5] != "Lv"]
        held = lv[0] - first[0]
        print(f"{'PASS' if not after else 'FAIL'} s{n}: Leave at {lv[0]:.3f} ms, {held:.3f} ms after its first "
              f"Advertise; {len(after)} Advertise declarations after it")
        failures += bool(after)
    early = [t for t in talkers if not probes or t[0] < probes[0]]
    print(f"{'PASS' if probes and not early else 'FAIL'} no Talker attribute before the first probe "
          f"({len(early)} seen; first probe at {probes[0] if probes else float('nan'):.3f} ms)")
    failures += bool(early) or not probes
    failed_types = [t for t in talkers if t[2] == 2]
    print(f"{'PASS' if not failed_types else 'FAIL'} no Talker Failed on the wire ({len(failed_types)} seen)")
    failures += bool(failed_types)
    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
