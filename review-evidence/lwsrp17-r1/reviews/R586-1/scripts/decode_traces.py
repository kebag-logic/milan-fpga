# SPDX-License-Identifier: Apache-2.0
"""Reviewer-owned MRPDU decoder (IEEE 802.1Q-2018 10.8.1.2, 10.8.2; MSRP 35.2.2.6,
35.2.2.7.2), independent of the library parser and of the author's test decoder.

Usage:
  decode_traces.py compare <base.trace> <candidate.trace>
  decode_traces.py grade <trace>

Reads only the raw PDU hex, the EtherType and the send result from each trace
"S" record; the author's decoded columns are ignored.
"""
import sys
from collections import OrderedDict, Counter

MSRP, MVRP, MMRP = 0x22EA, 0x88F5, 0x88F6


class Bad(Exception):
    pass


def decode(pdu, ethertype):
    """Return (messages, endmarks, trailing); messages = [(type, [vectors])],
    vector = (leave_all, first_value_hex, [events], [four_packed])."""
    list_length = ethertype == MSRP
    four_type = 3 if ethertype == MSRP else None
    if len(pdu) < 1:
        raise Bad("empty")
    off, messages, endmarks = 1, [], 0
    while off < len(pdu):
        if len(pdu) - off < 2:
            raise Bad("odd tail")
        if pdu[off] == 0 and pdu[off + 1] == 0:
            endmarks += 1
            return messages, endmarks, len(pdu) - off - 2
        mtype, alen = pdu[off], pdu[off + 1]
        off += 2
        if mtype == 0 or alen == 0:
            raise Bad("zero type/length")
        end = len(pdu)
        if list_length:
            if len(pdu) - off < 2:
                raise Bad("no list length")
            ll = pdu[off] << 8 | pdu[off + 1]
            off += 2
            if ll > len(pdu) - off:
                raise Bad("list length overrun")
            end = off + ll
        vectors, closed = [], False
        while off < end:
            if end - off < 2:
                raise Bad("vector header cut")
            vh = pdu[off] << 8 | pdu[off + 1]
            if vh == 0:
                endmarks += 1
                off += 2
                closed = True
                break
            la, nv = vh >> 13, vh & 0x1FFF
            if la > 1:
                raise Bad("reserved LeaveAllEvent")
            n3 = (nv + 2) // 3
            n4 = (nv + 3) // 4 if mtype == four_type else 0
            need = 2 + alen + n3 + n4
            if need > end - off:
                raise Bad("vector cut")
            fv = pdu[off + 2:off + 2 + alen]
            tp = pdu[off + 2 + alen:off + 2 + alen + n3]
            fp = pdu[off + 2 + alen + n3:off + need]
            events, types4 = [], []
            for k in range(nv):
                b = tp[k // 3]
                if b > 215:
                    raise Bad("event > 5")
                events.append([b // 36, (b // 6) % 6, b % 6][k % 3])
                if n4:
                    types4.append((fp[k // 4] >> (6 - 2 * (k % 4))) & 3)
            vectors.append((la, fv.hex(), events, types4))
            off += need
        if not vectors:
            raise Bad("empty AttributeList")
        if list_length and off != end:
            raise Bad("list length mismatch")
        messages.append((mtype, vectors, closed))
    return messages, endmarks, 0  # 10.8.1.2 f: PDU end acts as EndMark


def events_of(messages):
    out = Counter()
    for mtype, vectors, _ in messages:
        for la, fv, events, t4 in vectors:
            if la:
                out[("LA", mtype)] += 1
            for k, ev in enumerate(events):
                if k:
                    raise Bad("packed vector (+k) not expected from either encoder")
                out[(mtype, fv, ev, t4[k] if t4 else None)] += 1
    return out


def grouped_violations(messages, endmarks, trailing, ethertype):
    v = []
    types = [m[0] for m in messages]
    if types != sorted(set(types)):
        v.append("types not strictly ascending")
    if endmarks != len(messages) + 1:
        v.append(f"endmarks {endmarks} != messages+1")
    if trailing:
        v.append("trailing octets")
    last = {MSRP: 4, MMRP: 2, MVRP: 1}[ethertype]
    flagged = 0
    for mtype, vectors, closed in messages:
        if not closed:
            v.append("message without EndMark")
        prev = None
        for i, (la, fv, events, _) in enumerate(vectors):
            if la:
                if i or events:
                    v.append("LeaveAll vector not first or not empty")
                flagged += 1
                continue
            if len(events) != 1:
                v.append("NumberOfValues != 1")
            if prev is not None and not prev < fv:  # equal-length hex: lexical = numeric
                v.append("FirstValue not strictly ascending")
            prev = fv
    if flagged not in (0, last):
        v.append(f"LeaveAll on {flagged} of {last} types")
    return v


def la_after_value(messages):
    """True if a LeaveAll vector follows a value of an earlier type in the PDU."""
    seen_value = False
    for _, vectors, _ in messages:
        for la, _, events, _ in vectors:
            if la and seen_value:
                return True
            if events:
                seen_value = True
    return False


def read(path):
    tests = OrderedDict()
    for line in open(path, encoding="ascii"):
        f = line.rstrip("\n").split("\t")
        if f[0] != "S":
            continue
        opp = tests.setdefault(f[1], OrderedDict()).setdefault(int(f[2]), [])
        length, hexbytes = int(f[7]), f[8]
        opp.append({"eth": int(f[4], 16), "rc": int(f[6]), "len": length,
                    "pdu": bytes.fromhex(hexbytes) if len(hexbytes) == 2 * length else None})
    return tests


def main():
    mode = sys.argv[1]
    if mode == "compare":
        base, cand = read(sys.argv[2]), read(sys.argv[3])
        totals = Counter()
        problems = []
        for test in OrderedDict.fromkeys(list(base) + list(cand)):
            b, c = base.get(test, {}), cand.get(test, {})
            if list(b) != list(c):
                problems.append(f"{test}: opportunity keys differ")
            for idx in c:
                bs, cs = b.get(idx, []), c[idx]
                if len(bs) != len(cs):
                    problems.append(f"{test}#{idx}: send count {len(bs)} != {len(cs)}")
                for x, y in zip(bs, cs):
                    totals["pdus"] += 1
                    mx, ex, tx = decode(x["pdu"], x["eth"])
                    try:
                        my, ey, ty = decode(y["pdu"], y["eth"])
                        events_of(my)
                    except Bad as err:
                        totals["different"] += 1
                        problems.append(f"{test}#{idx}: candidate undecodable: {err}")
                        continue
                    if x["rc"] != y["rc"] or events_of(mx) != events_of(my):
                        totals["different"] += 1
                        problems.append(f"{test}#{idx}: decoded events differ")
                    elif x["pdu"] == y["pdu"]:
                        totals["identical"] += 1
                    else:
                        totals["layout_only"] += 1
                    g = grouped_violations(my, ey, ty, y["eth"])
                    if g:
                        problems.append(f"{test}#{idx}: candidate not grouped: {g}")
                    totals["la_after_value_base"] += la_after_value(mx)
                    totals["la_after_value_candidate"] += la_after_value(my)
            totals["tests"] += 1
            totals["opportunities"] += len(c)
        print(dict(totals))
        for p in problems:
            print("FAIL", p)
        return int(bool(problems))
    if mode == "grade":
        tests = read(sys.argv[2])
        totals, problems = Counter(), []
        for test, opps in tests.items():
            for idx, sends in opps.items():
                for s in sends:
                    if s["pdu"] is None:
                        totals["skipped_truncated_record"] += 1
                        continue
                    try:
                        m, e, t = decode(s["pdu"], s["eth"])
                        events_of(m)
                    except Bad as err:
                        problems.append(f"{test}#{idx}: undecodable: {err}")
                        continue
                    totals["pdus"] += 1
                    totals["vectors"] += sum(len(v) for _, v, _ in m)
                    g = grouped_violations(m, e, t, s["eth"])
                    if g:
                        problems.append(f"{test}#{idx}: {g}")
                    totals["la_after_value"] += la_after_value(m)
                totals["tests_with_sends"] += 0
            totals["tests"] += 1
        print(dict(totals))
        for p in problems:
            print("FAIL", p)
        return int(bool(problems))
    raise SystemExit(__doc__)


if __name__ == "__main__":
    sys.exit(main())
