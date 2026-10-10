#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Reviewer-owned MRPDU decoder and trace comparator (lwSRP PR #18 review).

Written from IEEE 802.1Q-2018 10.8.1.2 and 10.8.2 (with 35.2.2.6 and
35.2.2.7.2 for MSRP). It shares no code with the library parser or with the
test-side decoder in the reviewed tree. It reads only the raw PDU hex, the
EtherType, the send rc and the call records of a transmit trace; the decoded
columns written by the trace shim are ignored.

Usage: r587_decode.py BASE_TRACE CANDIDATE_TRACE  -> comparison report, rc 0/1
       r587_decode.py --grade TRACE                 -> grouped-form grade, rc 0/1
"""
import sys
from collections import OrderedDict, Counter

MSRP, MVRP, MMRP = 0x22EA, 0x88F5, 0x88F6
LAST_TYPE = {MSRP: 4, MVRP: 1, MMRP: 2}


class Bad(Exception):
    pass


def decode(pdu, ethertype):
    """Return (messages, endmarks, trailing). Each message: (type, [vectors]).
    Each vector: dict(la, n, fv, events, four)."""
    msrp = ethertype == MSRP
    if len(pdu) < 1:
        raise Bad("empty")
    pos, msgs, endmarks = 1, [], 0
    while pos < len(pdu):
        if len(pdu) - pos < 2:
            raise Bad("short message header")
        if pdu[pos] == 0 and pdu[pos + 1] == 0:
            endmarks += 1
            return msgs, endmarks, len(pdu) - pos - 2
        atype, alen = pdu[pos], pdu[pos + 1]
        if atype == 0 or alen == 0:
            raise Bad("zero type or length")
        pos += 2
        limit = len(pdu)
        if msrp:
            if len(pdu) - pos < 2:
                raise Bad("short list length")
            llen = (pdu[pos] << 8) | pdu[pos + 1]
            pos += 2
            limit = pos + llen
            if limit > len(pdu):
                raise Bad("list length past end")
        vecs, closed = [], False
        while pos < limit:
            if limit - pos < 2:
                raise Bad("short vector header")
            hdr = (pdu[pos] << 8) | pdu[pos + 1]
            if hdr == 0:
                endmarks += 1
                closed = True
                pos += 2
                break
            la, n = hdr >> 13, hdr & 0x1FFF
            if la > 1:
                raise Bad("reserved LeaveAllEvent")
            n3 = (n + 2) // 3
            n4 = (n + 3) // 4 if (msrp and atype == 3) else 0
            need = 2 + alen + n3 + n4
            if limit - pos < need:
                raise Bad("incomplete vector")
            fv = bytes(pdu[pos + 2:pos + 2 + alen])
            tp = pdu[pos + 2 + alen:pos + 2 + alen + n3]
            fp = pdu[pos + 2 + alen + n3:pos + need]
            events = []
            for i in range(n):
                b = tp[i // 3]
                if b > 215:
                    raise Bad("event octet > 215")
                events.append([b // 36, (b // 6) % 6, b % 6][i % 3])
            four = [(fp[i // 4] >> (6 - 2 * (i % 4))) & 3 for i in range(n)] if n4 else None
            vecs.append(dict(la=la, n=n, fv=fv, events=events, four=four))
            pos += need
        if msrp and pos != limit:
            raise Bad("list length mismatch")
        if not vecs:
            raise Bad("empty attribute list")
        msgs.append((atype, vecs, closed))
    return msgs, endmarks, None  # PDU end acts as EndMark (10.8.1.2 f)


def events_of(msgs):
    """Multiset of decoded events: LeaveAll per type, and per value
    (type, FirstValue+offset as integer, event, four-packed)."""
    out = []
    for atype, vecs, _ in msgs:
        for v in vecs:
            if v["la"]:
                out.append(("LA", atype))
            base = int.from_bytes(v["fv"], "big")
            for i, ev in enumerate(v["events"]):
                out.append((atype, base + i, len(v["fv"]), ev, v["four"][i] if v["four"] else None))
    return Counter(out)


def ordered_events(msgs):
    return [e for atype, vecs, _ in msgs for v in vecs for e in
            ([("LA", atype)] if v["la"] else []) +
            [(atype, v["fv"].hex(), ev) for ev in v["events"]]]


def grade(msgs, endmarks, trailing, ethertype):
    """Issue #17 grouped form. Returns a list of violations."""
    bad = []
    types = [m[0] for m in msgs]
    if types != sorted(set(types)):
        bad.append("types not strictly ascending")
    if endmarks != len(msgs) + 1 or trailing != 0:
        bad.append(f"endmarks {endmarks} for {len(msgs)} messages, trailing {trailing}")
    flagged = 0
    for atype, vecs, closed in msgs:
        if not closed:
            bad.append(f"type {atype} without EndMark")
        prev = None
        for k, v in enumerate(vecs):
            if v["la"]:
                if k != 0 or v["n"] != 0:
                    bad.append(f"type {atype}: LeaveAll not a leading NumberOfValues-0 vector")
                flagged += 1
                continue
            if v["n"] != 1:
                bad.append(f"type {atype}: NumberOfValues {v['n']}")
            if prev is not None and not prev < v["fv"]:
                bad.append(f"type {atype}: FirstValue not ascending")
            prev = v["fv"]
    if flagged not in (0, LAST_TYPE.get(ethertype, -1)):
        bad.append(f"LeaveAll on {flagged} types")
    return bad


def read(path):
    tests = OrderedDict()
    with open(path, "rb") as f:
        for raw in f:
            fields = raw.decode("ascii", "replace").rstrip("\n").split("\t")
            if fields[0] not in ("S", "C") or len(fields) < 7:
                tests.setdefault("#malformed", OrderedDict()).setdefault(len(tests.get("#malformed", {})), {"sends": []})
                continue
            calls = tests.setdefault(fields[1], OrderedDict())
            call = calls.setdefault(int(fields[2]), {"sends": []})
            if fields[0] == "S":
                call["sends"].append(dict(ethertype=int(fields[4], 16), rc=int(fields[6]),
                                          length=int(fields[7]), hex=fields[8]))
            else:
                call.update(ethertype=int(fields[3], 16), capacity=int(fields[5]), result=int(fields[6]),
                            nsends=int(fields[7]))
    return tests


def pdu_of(send):
    try:
        data = bytes.fromhex(send["hex"])
    except ValueError:
        raise Bad(f"record truncated: {len(send['hex'])} hex digits for {send['length']} octets")
    if len(data) != send["length"]:
        raise Bad(f"record holds {len(data)} of {send['length']} octets")
    return data


def compare(base_path, cand_path):
    base, cand = read(base_path), read(cand_path)
    stats = Counter()
    problems, notes = [], []
    for test in OrderedDict.fromkeys(list(base) + list(cand)):
        old, new = base.get(test, {}), cand.get(test, {})
        if list(old) != list(new):
            problems.append(f"{test}: opportunity keys differ ({len(old)} vs {len(new)})")
        for idx in new:
            stats["opportunities"] += 1
            a, b = old.get(idx, {"sends": []}), new[idx]
            if a.get("result") != b.get("result") or len(a["sends"]) != len(b["sends"]):
                problems.append(f"{test}#{idx}: result {a.get('result')}->{b.get('result')}, "
                                f"sends {len(a['sends'])}->{len(b['sends'])}")
            for x, y in zip(a["sends"], b["sends"]):
                stats["pdus"] += 1
                try:
                    px, py = pdu_of(x), pdu_of(y)
                    mx, ex, tx = decode(px, x["ethertype"])
                    my, ey, ty = decode(py, y["ethertype"])
                except Bad as err:
                    problems.append(f"{test}#{idx}: undecodable ({err})")
                    continue
                if len(py) > b.get("capacity", 1 << 30):
                    problems.append(f"{test}#{idx}: candidate PDU {len(py)} > capacity {b['capacity']}")
                if x["rc"] != y["rc"] or events_of(mx) != events_of(my):
                    stats["different"] += 1
                    problems.append(f"{test}#{idx}: decoded events differ")
                    continue
                if px == py:
                    stats["identical"] += 1
                else:
                    stats["layout_only"] += 1
                    oe, ne = ordered_events(mx), ordered_events(my)
                    tag = "same order" if oe == ne else "reordered"
                    # Cross-type reorder: does the relative order of events of
                    # different types change?
                    cross = [e for e in oe], [e for e in ne]
                    def proj(seq):
                        return [e[0] if e[0] != "LA" else ("LA", e[1]) for e in seq]
                    if proj(oe) != proj(ne):
                        tag += "; cross-type order changed"
                    notes.append(f"{test}#{idx} ({x['ethertype']:04x}, {len(px)}->{len(py)} octets): {tag}")
                    notes.append(f"    base: {px.hex()}")
                    notes.append(f"    head: {py.hex()}")
                g = grade(my, ey, ty, y["ethertype"])
                if g:
                    problems.append(f"{test}#{idx}: candidate not grouped: {g}")
    print("opportunities={opportunities} pdus={pdus} identical={identical} "
          "layout_only={layout_only} different={different}".format(**{k: stats[k] for k in
          ("opportunities", "pdus", "identical", "layout_only", "different")}))
    print(f"problems={len(problems)}")
    for p in problems:
        print("FAIL", p)
    print("layout-only PDUs:")
    for n in notes:
        print(n)
    return 1 if problems or stats["pdus"] == 0 else 0


def grade_trace(path):
    tests = read(path)
    stats, problems = Counter(), []
    for test, calls in tests.items():
        for idx, call in calls.items():
            for s in call["sends"]:
                stats["pdus"] += 1
                try:
                    p = pdu_of(s)
                    m, e, t = decode(p, s["ethertype"])
                except Bad as err:
                    stats["unreadable"] += 1
                    problems.append(f"{test}#{idx}: {err}")
                    continue
                if len(p) > call.get("capacity", 1 << 30):
                    problems.append(f"{test}#{idx}: PDU {len(p)} > capacity {call['capacity']}")
                stats["vectors"] += sum(len(v) for _, v, _ in m)
                g = grade(m, e, t, s["ethertype"])
                if g:
                    problems.append(f"{test}#{idx}: {g}")
    print(f"pdus={stats['pdus']} vectors={stats['vectors']} unreadable={stats['unreadable']} problems={len(problems)}")
    for p in problems:
        print("FAIL", p)
    return 1 if problems else 0


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--grade":
        sys.exit(grade_trace(sys.argv[2]))
    if len(sys.argv) == 3:
        sys.exit(compare(sys.argv[1], sys.argv[2]))
    print(__doc__)
    sys.exit(2)
