#!/usr/bin/env python3
"""indep_check.py - reviewer's own MRPDU form, source-address and spacing check of srptx captures.

Written from IEEE 802.1Q-2018 10.8.1.2 / 10.8.2 and 35.2.2 field layouts, sharing no code with
srptx_grade.py. Reads one or more capture JSON files (the "mac" list) and prints a summary per file.
Exit 1 if any frame is malformed or has a wrong source/group address.

  python3 -I indep_check.py CAPTURE.json [...]
"""
import json
import sys

MSRP, MVRP = 0x22EA, 0x88F5
GROUP = {MSRP: bytes.fromhex("0180c200000e"), MVRP: bytes.fromhex("0180c2000021")}
# AttributeType -> AttributeLength (MSRP 35.2.2.x; MVRP 11.2.3.1.x)
ALEN = {MSRP: {1: 25, 2: 34, 3: 8, 4: 4}, MVRP: {1: 2}}
FOURPACKED = {MSRP: {3}, MVRP: set()}


def parse(et, pdu):
    """Return (messages, mrpdu_len) or raise ValueError. message = (type, [(leaveall, n, firstvalue)])"""
    if len(pdu) < 3 or pdu[0] != 0:
        raise ValueError("ProtocolVersion")
    i = 1
    msgs = []
    while True:
        if i + 2 > len(pdu):
            raise ValueError("no PDU EndMark")
        if pdu[i] == 0 and pdu[i + 1] == 0:
            i += 2
            break
        at, al = pdu[i], pdu[i + 1]
        i += 2
        if at not in ALEN[et] or ALEN[et][at] != al:
            raise ValueError(f"AttributeType/Length {at}/{al}")
        list_end = None
        if et == MSRP:
            if i + 2 > len(pdu):
                raise ValueError("no AttributeListLength")
            ll = pdu[i] << 8 | pdu[i + 1]
            i += 2
            list_end = i + ll
            if list_end > len(pdu):
                raise ValueError("AttributeListLength overruns")
        vecs = []
        while True:
            if i + 2 > len(pdu):
                raise ValueError("no AttributeList EndMark")
            hdr = pdu[i] << 8 | pdu[i + 1]
            if hdr == 0:
                i += 2
                break
            la, n = hdr >> 13, hdr & 0x1FFF
            if la not in (0, 1):
                raise ValueError("LeaveAllEvent value")
            i += 2
            fv = pdu[i:i + al]
            i += al
            tp = (n + 2) // 3
            packed = pdu[i:i + tp]
            if len(packed) != tp or any(b > 215 for b in packed):
                raise ValueError("ThreePackedEvents")
            i += tp
            if at in FOURPACKED[et]:
                i += (n + 3) // 4
            if i > len(pdu):
                raise ValueError("vector overruns")
            vecs.append((la, n, bytes(fv)))
        if list_end is not None and i != list_end:
            raise ValueError(f"AttributeList EndMark not at AttributeListLength end ({i} vs {list_end})")
        if not vecs:
            raise ValueError("empty AttributeList")
        msgs.append((at, vecs))
    if any(pdu[i:]):
        raise ValueError("nonzero after PDU EndMark")
    return msgs, i


def main():
    bad = 0
    for path in sys.argv[1:]:
        doc = json.load(open(path))
        port = bytes.fromhex(doc["port_mac"])
        n = {MSRP: 0, MVRP: 0}
        maxlen = {MSRP: 0, MVRP: 0}
        frame_len = {MSRP: set(), MVRP: set()}
        la_times = {MSRP: [], MVRP: []}
        times = {MSRP: [], MVRP: []}
        errs = []
        first = None
        for m in doc["mac"]:
            f = bytes.fromhex(m["hex"])
            et = f[12] << 8 | f[13]
            if et not in (MSRP, MVRP):
                continue
            n[et] += 1
            first = m["ms"] if first is None else first
            frame_len[et].add(len(f))
            if f[:6] != GROUP[et]:
                errs.append(f"{m['ms']}: group {f[:6].hex()}")
            if f[6:12] != port:
                errs.append(f"{m['ms']}: SA {f[6:12].hex()}")
            try:
                msgs, ln = parse(et, f[14:])
            except ValueError as e:
                errs.append(f"{m['ms']}: {e}")
                continue
            maxlen[et] = max(maxlen[et], ln)
            if ln > 1500:
                errs.append(f"{m['ms']}: MRPDU {ln} > 1500")
            types = [t for t, _ in msgs]
            if len(types) != len(set(types)):
                errs.append(f"{m['ms']}: repeated AttributeType {types}")
            fvs = [(t, v[2]) for t, vs in msgs for v in vs if v[1]]
            if len(fvs) != len(set(fvs)):
                errs.append(f"{m['ms']}: repeated FirstValue")
            la_types = {t for t, vs in msgs if any(v[0] for v in vs)}
            if la_types:
                if la_types != set(ALEN[et]):
                    errs.append(f"{m['ms']}: LeaveAll on {sorted(la_types)}")
                la_times[et].append(m["us"] / 1000)
            times[et].append(m["us"] / 1000)
        bad += len(errs)
        print(f"== {path}: scenario {doc['scenario']}, first MRPDU at ms {first}")
        for et, name in ((MSRP, "MSRP"), (MVRP, "MVRP")):
            gaps = [b - a for a, b in zip(la_times[et], la_times[et][1:])]
            four = [d - c for c, d in zip(times[et], times[et][3:])]
            print(f"  {name}: {n[et]} frames, MRPDU max {maxlen[et]} octets, frame lengths "
                  f"{min(frame_len[et]) if frame_len[et] else '-'}..{max(frame_len[et]) if frame_len[et] else '-'}; "
                  f"{len(la_times[et])} LeaveAll frames, consecutive LeaveAll gap ms "
                  f"{(round(min(gaps), 3), round(max(gaps), 3)) if gaps else '-'}, first LeaveAll at ms "
                  f"{round(la_times[et][0], 3) if la_times[et] else '-'}; min span of 4 consecutive frames ms "
                  f"{round(min(four), 3) if four else '-'}")
        for e in errs[:20]:
            print("  ERROR", e)
        print(f"  errors: {len(errs)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
