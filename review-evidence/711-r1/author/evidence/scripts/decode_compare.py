"""Compare SRP-channel TX frames from base and candidate firmware arms, decoded per IEEE 802.1Q-2018.

Usage: python3 decode_compare.py BASE_DUMP_DIR CAND_DUMP_DIR [--report FILE] [--plant NAME]

Written from 802.1Q-2018 10.8.1.2 (MRPDU structure), 10.8.2.4-10.8.2.10.2 (field encodings),
35.2.2.4-35.2.2.9 (MSRP types, lengths, FourPackedEvents, FirstValue increments) and 11.2.3.1
(MVRP VID). It shares no code with lwSRP, the firmware or its test fixtures.

A frame's decoded form is its Ethernet header, the set of AttributeTypes flagged LeaveAll and the
multiset of (AttributeType, value, AttributeEvent, FourPackedType) for every value, FirstValue
incremented per the application. Frames are paired in order inside each model reset (one test).
Each pair is IDENTICAL (same bytes), LAYOUT-ONLY (same decoded form, same interface, time and
EtherType) or DIFFERENT. Every candidate MRPDU is also graded for the grouped form.
--plant applies a named defect to the candidate's decoded events in memory (a negative control).
"""
import argparse
import collections
import json
import sys
from pathlib import Path

MSRP, MVRP = 0x22EA, 0x88F5
MSRP_LEN = {1: 25, 2: 34, 3: 8, 4: 4}


class Bad(Exception):
    pass


def increment(ethertype, attr_type, first, n):
    """FirstValue + n per 35.2.2.8 (stream: UniqueID and destination_address), 35.2.2.9 (Domain), 11.2.3.1 (VID)."""
    v = bytearray(first)
    def add(lo, width):
        total = int.from_bytes(v[lo:lo + width], 'big') + n
        v[lo:lo + width] = (total % (1 << (8 * width))).to_bytes(width, 'big')
    if ethertype == MVRP:
        add(0, 2)
    elif attr_type == 4:
        v[0] = (v[0] + n) & 255
        v[1] = (v[1] + n) & 255
    else:
        add(6, 2)
        if attr_type in (1, 2):
            add(8, 6)
    return bytes(v)


def decode(frame):
    """Decode one Ethernet frame carrying an MRPDU; return (header, structure, leaveall types, events)."""
    if len(frame) < 15:
        raise Bad('short frame')
    ethertype = int.from_bytes(frame[12:14], 'big')
    if ethertype not in (MSRP, MVRP):
        raise Bad(f'EtherType {ethertype:#06x}')
    p = frame[14:]
    if p[0] != 0:
        raise Bad('ProtocolVersion')
    off = 1
    messages = []          # (type, [(leaveall, n, first)]) in wire order
    events = []
    leaveall = set()
    while off + 2 <= len(p) and (p[off] or p[off + 1]):
        attr_type, attr_len = p[off], p[off + 1]
        off += 2
        if attr_type == 0 or attr_len == 0:
            raise Bad('zero AttributeType or AttributeLength (10.8.2.2, 10.8.2.3)')
        if ethertype == MSRP and MSRP_LEN.get(attr_type) != attr_len:
            raise Bad(f'MSRP type {attr_type} length {attr_len} (35.2.2.5)')
        if ethertype == MVRP and (attr_type, attr_len) != (1, 2):
            raise Bad(f'MVRP type {attr_type} length {attr_len} (11.2.3.1)')
        end = len(p)
        if ethertype == MSRP:
            end = off + 2 + int.from_bytes(p[off:off + 2], 'big')
            off += 2
            if end > len(p):
                raise Bad('AttributeListLength past the PDU (10.8.2.4)')
        vectors = []
        while True:
            if off + 2 > end:
                raise Bad('AttributeList without EndMark')
            header = int.from_bytes(p[off:off + 2], 'big')
            if header == 0:
                off += 2
                break
            la, n = header >> 13, header & 8191
            if la > 1:
                raise Bad('reserved LeaveAllEvent (10.8.2.6)')
            if la == 0 and n == 0:
                raise Bad('NullLeaveAllEvent with no values (10.8.2.8 g)')
            first = bytes(p[off + 2:off + 2 + attr_len])
            off += 2 + attr_len
            three = p[off:off + (n + 2) // 3]
            off += (n + 2) // 3
            four = b''
            if ethertype == MSRP and attr_type == 3:
                four = p[off:off + (n + 3) // 4]
                off += (n + 3) // 4
            if off > end or len(first) != attr_len:
                raise Bad('incomplete VectorAttribute (10.8.3.4 b)')
            if la:
                leaveall.add(attr_type)
            for i in range(n):
                packed = three[i // 3]
                if packed > 215:
                    raise Bad('ThreePackedEvents above 215')
                event = (packed // 36, (packed // 6) % 6, packed % 6)[i % 3]
                sub = (four[i // 4] >> (6 - 2 * (i % 4))) & 3 if four else None
                events.append((attr_type, increment(ethertype, attr_type, first, i).hex(), event, sub))
            vectors.append((la, n, first))
        if ethertype == MSRP and off != end:
            raise Bad('AttributeListLength disagrees with the AttributeList (35.2.2.6)')
        messages.append((attr_type, vectors))
    if off + 2 > len(p):
        raise Bad('MRPDU without EndMark')
    off += 2
    if any(p[off:]):
        raise Bad('nonzero octets after the MRPDU EndMark')
    header = bytes(frame[:14])
    return header, messages, frozenset(leaveall), events


def grouped_findings(ethertype, messages):
    """The grouped form of lwSRP #17: one Message per type, ascending types, LeaveAll first, NumberOfValues 1, ascending FirstValue."""
    found = []
    types = [t for t, _ in messages]
    if len(types) != len(set(types)):
        found.append('a type has more than one Message')
    if types != sorted(types):
        found.append('Messages not in AttributeType order')
    for t, vectors in messages:
        values = [v for v in vectors if v[1]]
        if any(v[0] for v in values) or any(la and n for la, n, _ in vectors):
            found.append(f'type {t}: LeaveAll on a value vector')
        if any(la for la, _, _ in vectors[1:]):
            found.append(f'type {t}: LeaveAll vector not first')
        if any(n != 1 for _, n, _ in values):
            found.append(f'type {t}: NumberOfValues other than 1')
        firsts = [f for _, _, f in values]
        if firsts != sorted(firsts) or len(set(firsts)) != len(firsts):
            found.append(f'type {t}: FirstValue not strictly ascending')
    return found


def leaveall_precedes(messages):
    """Per type, a LeaveAll vector precedes that type's values (10.8 NOTE 2)."""
    seen_value = set()
    for t, vectors in messages:
        for la, n, _ in vectors:
            if la and t in seen_value:
                return False
            if n:
                seen_value.add(t)
    return True


def load(path):
    blocks, current = [], None
    for line in path.read_text().splitlines():
        if line == 'RESET':
            current = []
            blocks.append(current)
            continue
        fields = dict(item.split('=', 1) for item in line.split()[1:])
        frame = bytes.fromhex(fields['hex'])
        if len(frame) != int(fields['len']):
            raise SystemExit(f'{path}: length field disagrees with the bytes')
        current.append((int(fields['if']), int(fields['ms']), frame))
    return blocks


PLANTS = {
    'drop-one-event': lambda ev: ev[1:],
    'swap-event': lambda ev: [(ev[0][0], ev[0][1], (ev[0][2] + 1) % 6, ev[0][3])] + ev[1:],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('base', type=Path)
    ap.add_argument('cand', type=Path)
    ap.add_argument('--report', type=Path)
    ap.add_argument('--plant', choices=sorted(PLANTS))
    args = ap.parse_args()
    arms = sorted({p.name for p in args.base.glob('*.txt')} | {p.name for p in args.cand.glob('*.txt')})
    totals = collections.Counter()
    rows, problems = [], []
    planted = False
    for arm in arms:
        b_path, c_path = args.base / arm, args.cand / arm
        if not b_path.exists() or not c_path.exists():
            problems.append(f'{arm}: present on one side only')
            continue
        b_blocks, c_blocks = load(b_path), load(c_path)
        counts = collections.Counter()
        if len(b_blocks) != len(c_blocks):
            problems.append(f'{arm}: {len(b_blocks)} base resets, {len(c_blocks)} candidate resets')
        for k, (bb, cb) in enumerate(zip(b_blocks, c_blocks)):
            if len(bb) != len(cb):
                problems.append(f'{arm} block {k}: {len(bb)} base frames, {len(cb)} candidate frames')
            for j, ((bi, bms, bf), (ci, cms, cf)) in enumerate(zip(bb, cb)):
                where = f'{arm} block {k} frame {j}'
                if not all(len(f) >= 14 and int.from_bytes(f[12:14], 'big') in (MSRP, MVRP) for f in (bf, cf)):
                    # Test-written filler on the SRP channel, not an MRPDU: bytes must match.
                    counts['other'] += 1
                    if (bi, bms, bf) != (ci, cms, cf):
                        problems.append(f'{where}: non-MRP frame differs')
                    continue
                try:
                    bh, bmsg, bla, bev = decode(bf)
                    ch, cmsg, cla, cev = decode(cf)
                except Bad as exc:
                    problems.append(f'{where}: undecodable: {exc}')
                    counts['undecodable'] += 1
                    continue
                if args.plant and not planted and cev:
                    cev = PLANTS[args.plant](cev)
                    planted = True
                for finding in grouped_findings(ch[12] << 8 | ch[13], cmsg):
                    problems.append(f'{where}: candidate not grouped: {finding}')
                for side, msg in (('base', bmsg), ('candidate', cmsg)):
                    if not leaveall_precedes(msg):
                        problems.append(f'{where}: {side} LeaveAll after a value of its type')
                same_context = (bi, bms, bh) == (ci, cms, ch)
                same_decoded = bla == cla and sorted(bev, key=repr) == sorted(cev, key=repr)
                if same_context and same_decoded and bf == cf:
                    kind = 'identical'
                elif same_context and same_decoded:
                    kind = 'layout-only'
                else:
                    kind = 'different'
                    problems.append(f'{where}: DIFFERENT (if {bi}/{ci}, ms {bms}/{cms}, '
                                    f'LeaveAll {sorted(bla)}/{sorted(cla)}, {len(bev)}/{len(cev)} events)')
                counts[kind] += 1
                counts['events'] += len(cev)
                counts['leaveall'] += len(cla)
                counts['bytes_base'] += len(bf)
                counts['bytes_cand'] += len(cf)
        counts['tests'] = len(b_blocks)
        rows.append((arm, counts))
        totals.update(counts)
    lines = ['| Arm | Tests | MRPDUs | Identical | Layout-only | Different | Values | LeaveAll types | Octets base / candidate | Other frames |',
             '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for arm, c in rows + [('**Total**', totals)]:
        frames = c['identical'] + c['layout-only'] + c['different'] + c['undecodable']
        lines.append(f"| {arm.removesuffix('.txt')} | {c['tests']} | {frames} | {c['identical']} | {c['layout-only']} | "
                     f"{c['different']} | {c['events']} | {c['leaveall']} | {c['bytes_base']} / {c['bytes_cand']} | {c['other']} |")
    text = '\n'.join(lines) + '\n\nproblems: ' + str(len(problems)) + '\n' + '\n'.join(problems[:200]) + '\n'
    print(text)
    if args.report:
        args.report.write_text(text)
        args.report.with_suffix('.json').write_text(json.dumps(
            {'totals': dict(totals), 'arms': {a: dict(c) for a, c in rows}, 'problems': problems}, indent=1))
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
