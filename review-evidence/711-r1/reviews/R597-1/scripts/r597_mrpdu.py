#!/usr/bin/env python3
"""Independent MRPDU decoder and base/head comparison (reviewer R597, issue #711).

Written from IEEE 802.1Q-2018 10.8.1.2 (MRPDU = ProtocolVersion, Message+, EndMark),
10.8.2.4-10.8.2.10 (AttributeType, AttributeLength, VectorAttribute, VectorHeader with
LeaveAllEvent in bits 15..13 and NumberOfValues in bits 12..0, FirstValue, Vector of
ThreePackedEvents, EndMark 0x0000), 35.2.2 (MSRP: AttributeListLength after
AttributeLength; Listener adds FourPackedEvents) and 11.2.3.1 (MVRP VID attribute).
It shares no code with lwSRP or the firmware.

Usage:
  r597_mrpdu.py selftest
  r597_mrpdu.py compare <base dump dir> <head dump dir> <out.json>
A dump dir holds one file per process: 'E <argv0>', then 'R' (model reset) or
'T <if> <ms> <frame hex>' lines.
"""
from __future__ import annotations
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

MSRP, MVRP = 0x22EA, 0x88F5
EVENTS = ("New", "JoinIn", "In", "JoinMt", "Mt", "Lv")


class Malformed(ValueError):
    pass


def be(b: bytes) -> int:
    return int.from_bytes(b, "big")


def add_value(etype: int, atype: int, first: bytes, k: int) -> bytes:
    """FirstValue + k under the per-attribute increment rules."""
    if k == 0:
        return first
    if etype == MVRP:  # 11.2.3.1.? VID: 12-bit increment
        return ((be(first) + k) & 0xFFFF).to_bytes(len(first), "big")
    if atype in (1, 2):  # Talker: StreamID + k and DataFrameParameters DA + k (35.2.2.8.?)
        sid = (be(first[0:8]) + k) % (1 << 64)
        da = (be(first[8:14]) + k) % (1 << 48)
        return sid.to_bytes(8, "big") + da.to_bytes(6, "big") + first[14:]
    if atype == 3:  # Listener: StreamID + k
        return ((be(first) + k) % (1 << 64)).to_bytes(8, "big")
    if atype == 4:  # Domain: SRclassID, SRclassPriority, SRclassVID each + k
        return bytes([(first[0] + k) & 0xFF, (first[1] + k) & 0xFF]) + ((be(first[2:4]) + k) & 0xFFFF).to_bytes(2, "big")
    raise Malformed(f"no increment rule for type {atype}")


def decode(frame: bytes) -> dict:
    """Decode one Ethernet frame carrying an MRPDU; raise Malformed when it does not parse."""
    if len(frame) < 15:
        raise Malformed("short frame")
    etype = be(frame[12:14])
    if etype not in (MSRP, MVRP):
        raise Malformed(f"ethertype {etype:#06x}")
    p = frame[14:]
    version = p[0]
    off = 1
    messages = []  # (type, attrlen, [vectors]) in wire order
    events = []    # (type, value hex, event, four) per value
    leave_all = []  # types flagged LeaveAll, in wire order
    endmark = False
    while True:
        if off + 2 > len(p):
            break  # 10.8.1.2: end of PDU also ends the Message list
        if p[off] == 0 and p[off + 1] == 0:
            endmark = True
            off += 2
            break
        atype, alen = p[off], p[off + 1]
        off += 2
        if alen == 0:
            raise Malformed("AttributeLength 0")
        list_end = len(p)
        if etype == MSRP:
            if off + 2 > len(p):
                raise Malformed("no AttributeListLength")
            list_end = off + 2 + be(p[off:off + 2])
            off += 2
            if list_end > len(p):
                raise Malformed("AttributeListLength beyond PDU")
        vectors = []
        closed = False
        while off + 2 <= list_end:
            hdr = be(p[off:off + 2])
            if hdr == 0:
                off += 2
                closed = True
                break
            la, n = hdr >> 13, hdr & 0x1FFF
            off += 2
            if off + alen > list_end:
                raise Malformed("FirstValue beyond list")
            first = p[off:off + alen]
            off += alen
            three = (n + 2) // 3
            four = (n + 3) // 4 if (etype == MSRP and atype == 3) else 0
            if off + three + four > list_end:
                raise Malformed("Vector beyond list")
            tp, fp = p[off:off + three], p[off + three:off + three + four]
            off += three + four
            if la not in (0, 1):
                raise Malformed(f"LeaveAllEvent {la}")
            if la:
                leave_all.append(atype)
            vals = []
            for k in range(n):
                byte = tp[k // 3]
                e = (byte // 36, (byte // 6) % 6, byte % 6)[k % 3]
                if byte >= 216:
                    raise Malformed("ThreePackedEvent > 215")
                f4 = None
                if four:
                    f4 = (fp[k // 4] >> (6 - 2 * (k % 4))) & 3
                v = add_value(etype, atype, first, k)
                vals.append(v.hex())
                events.append((atype, v.hex(), EVENTS[e], f4))
            vectors.append({"la": la, "n": n, "first": first.hex(), "values": vals})
        if etype == MSRP and off != list_end:
            if not closed:
                raise Malformed("MSRP list without EndMark")
            raise Malformed("AttributeListLength disagrees with EndMark")
        if etype == MVRP and not closed:
            raise Malformed("MVRP Message without EndMark")
        messages.append({"type": atype, "len": alen, "vectors": vectors})
    return {"etype": etype, "version": version, "messages": messages, "events": events,
            "leave_all": leave_all, "endmark": endmark, "trailing": len(p) - off}


def canonical(d: dict) -> tuple:
    """Decoded meaning of one MRPDU: version, LeaveAll types and the multiset of attribute events."""
    return (d["etype"], d["version"], tuple(sorted(d["leave_all"])),
            tuple(sorted((t, v, e, f if f is not None else -1) for t, v, e, f in d["events"])))


def grouped_facts(d: dict) -> list[str]:
    """Departures from the grouped layout of lwSRP#17 / issue #711 (empty list = grouped)."""
    out = []
    types = [m["type"] for m in d["messages"]]
    if len(types) != len(set(types)):
        out.append("type repeated across Messages")
    if types != sorted(types):
        out.append("Messages not in AttributeType order")
    for m in d["messages"]:
        vs = m["vectors"]
        las = [i for i, v in enumerate(vs) if v["la"]]
        if las and las != [0]:
            out.append("LeaveAll vector not first")
        for v in vs:
            if v["la"] and v["n"] != 0:
                out.append("LeaveAll carried on a value vector")
            if not v["la"] and v["n"] != 1:
                out.append(f"value vector with NumberOfValues {v['n']}")
        firsts = [v["first"] for v in vs if not v["la"]]
        if firsts != sorted(firsts):
            out.append("FirstValues not ascending")
        if len(firsts) != len(set(firsts)):
            out.append("FirstValue repeated")
    if not d["endmark"]:
        out.append("no MRPDU EndMark")
    if d["trailing"]:
        out.append(f"{d['trailing']} octets after EndMark")
    return out


def load(dump: Path) -> dict[str, list[list[tuple]]]:
    """argv0 (normalised) -> list of runs, each a list of ('R',) or ('T', if, ms, bytes)."""
    runs = defaultdict(list)
    for f in sorted(dump.glob("*.txt"), key=lambda q: int(q.stem) if q.stem.isdigit() else 0):
        lines = f.read_text().splitlines()
        if not lines or not lines[0].startswith("E "):
            continue
        exe = re.sub(r"^.*?/ctrl-fw-[^/]+/", "", lines[0][2:].split("\0")[0])
        exe = re.sub(r"^.*?/(build|checkout)/", r"\1/", exe) if "ctrl-fw-" not in lines[0] else exe
        rec = []
        for ln in lines[1:]:
            if ln == "R":
                rec.append(("R",))
            else:
                _, i, ms, hx = ln.split()
                rec.append(("T", int(i), int(ms), bytes.fromhex(hx)))
        runs[exe].append(rec)
    return runs


def compare(base_dir: Path, head_dir: Path, out: Path) -> int:
    base, head = load(base_dir), load(head_dir)
    problems = []
    rows = {}
    tot = Counter()
    if sorted(base) != sorted(head):
        problems.append(f"executables differ: base-only {sorted(set(base) - set(head))} head-only {sorted(set(head) - set(base))}")
    for exe in sorted(set(base) & set(head)):
        c = Counter()
        if len(base[exe]) != len(head[exe]):
            problems.append(f"{exe}: {len(base[exe])} base runs, {len(head[exe])} head runs")
            continue
        for rb, rh in zip(base[exe], head[exe]):
            if len(rb) != len(rh):
                problems.append(f"{exe}: {len(rb)} base records, {len(rh)} head records")
                continue
            for a, b in zip(rb, rh):
                if a[0] != b[0]:
                    problems.append(f"{exe}: record kind differs"); break
                if a[0] == "R":
                    c["resets"] += 1
                    continue
                c["frames"] += 1
                if a[1:3] != b[1:3]:
                    c["if_or_time_differs"] += 1
                    problems.append(f"{exe}: interface/time {a[1:3]} vs {b[1:3]}")
                fa, fb = a[3], b[3]
                if fa[:12] != fb[:12]:
                    problems.append(f"{exe}: addresses differ")
                try:
                    da = decode(fa)
                except Malformed as exc:
                    if fa != fb:
                        problems.append(f"{exe}: base non-MRPDU frame changed ({exc})")
                    c["other_frames"] += 1
                    continue
                c["mrpdus"] += 1
                try:
                    db = decode(fb)
                except Malformed as exc:
                    problems.append(f"{exe}: head frame does not decode: {exc}")
                    c["different"] += 1
                    continue
                c["values"] += len(db["events"])
                c["leave_all_types"] += len(db["leave_all"])
                c["octets_base"] += len(fa); c["octets_head"] += len(fb)
                gf = grouped_facts(db)
                if gf:
                    c["head_not_grouped"] += 1
                    problems.append(f"{exe}: head MRPDU not grouped: {gf}")
                if max(Counter(m["type"] for m in da["messages"]).values(), default=0) > 1:
                    c["base_type_split"] += 1
                c["base_multi_value_vectors"] += sum(1 for m in da["messages"] for v in m["vectors"] if v["n"] > 1)
                if fa == fb:
                    c["identical"] += 1
                elif canonical(da) == canonical(db):
                    c["layout_only"] += 1
                else:
                    c["different"] += 1
                    problems.append(f"{exe}: decoded differently: base {canonical(da)} head {canonical(db)}")
        rows[exe] = dict(c)
        tot.update(c)
    result = {"executables": len(rows), "totals": dict(tot), "per_executable": rows, "problems": problems}
    out.write_text(json.dumps(result, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"executables": len(rows), "totals": dict(tot), "problems": len(problems)}, sort_keys=True))
    for p in problems[:20]:
        print("PROBLEM", p)
    return 1 if problems else 0


def frame(etype: int, pdu: bytes) -> bytes:
    return bytes(6) + bytes(6) + etype.to_bytes(2, "big") + pdu


def selftest() -> int:
    """Planted-change controls: every one must be caught or accepted exactly as stated."""
    fails = 0
    def check(name, cond):
        nonlocal fails
        print(("ok   " if cond else "FAIL ") + name)
        fails += not cond
    # MVRP: VID 2 JoinIn + VID 3 JoinMt, grouped, with LeaveAll vector first.
    la = b"\x20\x00" + b"\x00\x00"
    v2 = b"\x00\x01" + b"\x00\x02" + bytes([1 * 36])
    v3 = b"\x00\x01" + b"\x00\x03" + bytes([3 * 36])
    grouped = frame(MVRP, b"\x00" + b"\x01\x02" + la + v2 + v3 + b"\x00\x00" + b"\x00\x00")
    split = frame(MVRP, b"\x00" + b"\x01\x02" + la + b"\x00\x00" + b"\x01\x02" + v2 + b"\x00\x00"
                  + b"\x01\x02" + v3 + b"\x00\x00" + b"\x00\x00")
    packed = frame(MVRP, b"\x00" + b"\x01\x02" + la + b"\x00\x02\x00\x02" + bytes([1 * 36 + 3 * 6]) + b"\x00\x00\x00\x00")
    g, s, k = decode(grouped), decode(split), decode(packed)
    check("grouped == split (layout only)", canonical(g) == canonical(s))
    check("grouped == +k packed (layout only)", canonical(g) == canonical(k))
    check("grouped layout has no departures", grouped_facts(g) == [])
    check("split layout is reported as not grouped", "type repeated across Messages" in grouped_facts(s))
    check("+k packed is reported as not grouped", any("NumberOfValues 2" in x for x in grouped_facts(k)))
    swap = frame(MVRP, b"\x00" + b"\x01\x02" + la + b"\x00\x01\x00\x02" + bytes([3 * 36]) + b"\x00\x01\x00\x03"
                 + bytes([1 * 36]) + b"\x00\x00\x00\x00")
    check("swapped events decode differently", canonical(decode(swap)) != canonical(g))
    drop = frame(MVRP, b"\x00" + b"\x01\x02" + la + v2 + b"\x00\x00\x00\x00")
    check("dropped vector decodes differently", canonical(decode(drop)) != canonical(g))
    nola = frame(MVRP, b"\x00" + b"\x01\x02" + v2 + v3 + b"\x00\x00\x00\x00")
    check("dropped LeaveAll decodes differently", canonical(decode(nola)) != canonical(g))
    vid = frame(MVRP, b"\x00" + b"\x01\x02" + la + v2 + b"\x00\x01\x00\x04" + bytes([3 * 36]) + b"\x00\x00\x00\x00")
    check("changed FirstValue decodes differently", canonical(decode(vid)) != canonical(g))
    order = frame(MVRP, b"\x00" + b"\x01\x02" + la + v3 + v2 + b"\x00\x00\x00\x00")
    check("descending FirstValue is reported as not grouped", "FirstValues not ascending" in grouped_facts(decode(order)))
    noend = frame(MVRP, b"\x00" + b"\x01\x02" + la + v2 + v3 + b"\x00\x00")
    check("missing MRPDU EndMark is reported", "no MRPDU EndMark" in grouped_facts(decode(noend)))
    try:
        decode(frame(MVRP, b"\x00" + b"\x01\x02" + la + v2 + b"\x00\x01\x00"))
        check("truncated vector is refused", False)
    except Malformed:
        check("truncated vector is refused", True)
    # MSRP: two Listener values with FourPackedEvents, AttributeListLength consistent.
    l1 = b"\x00\x01" + bytes(range(8)) + bytes([1 * 36]) + bytes([2 << 6])
    l2 = b"\x00\x01" + bytes(range(1, 9)) + bytes([1 * 36]) + bytes([3 << 6])
    body = l1 + l2 + b"\x00\x00"
    ms = frame(MSRP, b"\x00" + b"\x03\x08" + len(body).to_bytes(2, "big") + body + b"\x00\x00")
    d = decode(ms)
    check("MSRP Listener decodes two values with FourPacked", [e[3] for e in d["events"]] == [2, 3])
    body2 = l1 + l2.replace(bytes([3 << 6]), bytes([1 << 6])) + b"\x00\x00"
    ms2 = frame(MSRP, b"\x00" + b"\x03\x08" + len(body2).to_bytes(2, "big") + body2 + b"\x00\x00")
    check("changed FourPackedEvent decodes differently", canonical(decode(ms2)) != canonical(d))
    bad = frame(MSRP, b"\x00" + b"\x03\x08" + (len(body) + 1).to_bytes(2, "big") + body + b"\x00\x00")
    try:
        decode(bad)
        check("wrong AttributeListLength is refused", False)
    except Malformed:
        check("wrong AttributeListLength is refused", True)
    print(f"r597 decoder selftest: {'FAIL' if fails else 'PASS'} ({fails} failures)")
    return 1 if fails else 0


if __name__ == "__main__":
    if sys.argv[1:2] == ["selftest"]:
        sys.exit(selftest())
    if sys.argv[1:2] == ["compare"] and len(sys.argv) == 5:
        sys.exit(compare(Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])))
    print(__doc__)
    sys.exit(2)
