#!/usr/bin/env python3
"""Reviewer's raw-log audit, without the harness's grade.py or scenario.py.

Usage: population_fanout.py CHECKOUT RESULTS_DIR
For every group log in RESULTS_DIR it prints, from the raw RXS/RXE/RXC, EVW, PASS-write, TXC, WIRE
and MARK lines (the mailbox contract read only for offsets and enumerations):
  - each composed window's committed population: receive commits per channel, GM and LINK
    event records posted, and frames offered whose commit never came (refused);
  - for each tagged probe frame: the records ahead of it on its own ring at its commit
    (committed earlier, not yet released by RX_TAIL);
  - every AECP SET_NAME (0x0010) probe's fan-out: the solicited response and every unsolicited
    SET_NAME response committed after the probe's commit and before the next MARK, each with its
    commit cycle, interface and controller_entity_id (TX commits paired in order with the frames
    the channel put on the wire).
"""
import sys
from pathlib import Path

checkout, results = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(checkout / 'sw/mailbox'))
from mailbox_model import load  # noqa: E402

c = load()
names = [x.name for x in c.channels]
chreg = {r.name: r.offset for r in c.ch_registers}
tail_word = {(c.ch_base + n * c.ch_stride + chreg['RX_TAIL']) // 4: n for n in range(len(names))}
ev_name = {e.value: e.name for e in c.event_types}
AECP = names.index('aecp')


def audit(path: Path) -> list[str]:
    rxs, rxe, rxc, evw, recs, writes, txc, wire, marks = [], [], [], {}, [], [], [], [], []
    for line in path.read_text().splitlines():
        f = line.split()
        if not f:
            continue
        k = f[0]
        if k == 'RXS':
            rxs.append((int(f[1]), int(f[2]), int(f[3]), f[4] if len(f) > 4 else '-'))
        elif k == 'RXE':
            rxe.append(int(f[1]))
        elif k == 'RXC':
            rxc.append((int(f[1]), int(f[2])))
        elif k == 'EVW':
            cyc, a, d = int(f[1]), int(f[2]), int(f[3], 16)
            evw[a] = d
            if a % 4 == 3 and all(x in evw for x in range(a - 3, a + 1)):
                recs.append((cyc, evw[a - 3] & 0xFF))
                for x in range(a - 3, a + 1):
                    evw.pop(x)
        elif k == 'PASS' and ' W' in line:
            for w in line.split(' W', 1)[1].split():
                cy, word, val = w.split(':')
                writes.append((int(cy), int(word, 16), int(val, 16)))
        elif k == 'TXC':
            txc.append((int(f[1]), int(f[2])))
        elif k == 'WIRE':
            wire.append((int(f[1]), int(f[2]), int(f[3]), bytes.fromhex(f[4])))   # cycle, if, ch, frame
        elif k == 'MARK':
            marks.append((int(f[1]), f[2]))
    writes.sort()
    # Each receive commit belongs to the frame whose last byte passed just before it (one RX stream).
    frames = []                                  # (start, if, bytes, tag, end)
    for s, e in zip(rxs, rxe):
        frames.append((*s, e))
    committed = []                               # (cycle, ch, if, bytes, tag)
    for cyc, ch in rxc:
        fr = max((x for x in frames if x[4] <= cyc), key=lambda x: x[4])
        committed.append((cyc, ch, fr[1], fr[2], fr[3]))
    out = [f'== {path.name}: {len(rxs)} frames offered, {len(rxc)} receive commits, {len(recs)} event records']
    m = dict((n, cy) for cy, n in marks)
    if 'composed' in m and 'composed_end' in m:
        a, b = m['composed'], m['composed_end']
        pop = {n: 0 for n in names}
        for cyc, ch, *_ in committed:
            if a <= cyc <= b:
                pop[names[ch]] += 1
        evs = {}
        for cyc, t in recs:
            if a <= cyc <= b:
                evs[ev_name.get(t, t)] = evs.get(ev_name.get(t, t), 0) + 1
        ends = {x[4] for x in frames if a <= x[4] <= b}
        used = {max((x for x in frames if x[4] <= cyc), key=lambda x: x[4])[4] for cyc, _ in rxc}
        out.append(f'  composed window {(b - a) / 1e5:.2f} ms: commits {pop}; events {evs}; '
                   f'frames offered in window {len(ends)}, never committed {len(ends - used)}')
    # Records ahead of each tagged probe frame on its own ring at its commit.
    for cyc, ch, iface, size, tag in committed:
        if tag == '-' or not tag.startswith('backlog'):
            continue
        released = 0
        last = 0
        for wc, w, v in writes:
            if wc < cyc and tail_word.get(w) == ch:
                released += (v - last) & 0xFFFF
                last = v
        total = ahead = 0
        for c2, ch2, _, sz, _ in committed:
            if ch2 == ch and c2 < cyc:
                total += 2 + (sz + 3) // 4
                ahead += total > released
        out.append(f'  {tag}: committed at {cyc} on {names[ch]} if{iface}; {ahead} records ahead on its ring')
    # SET_NAME fan-out (AECP channel): TX commits paired with wire frames in order.
    tx = [cy for cy, ch in txc if ch == AECP]
    wf = [(cy, i, fr) for cy, i, ch, fr in wire if ch == AECP]
    out_pairs = list(zip(tx, wf))
    for cyc, ch, iface, size, tag in committed:
        if 'set_name' not in tag:
            continue
        nxt = min([cy for cy, n in marks if cy > cyc] or [1 << 62])
        out.append(f'  {tag}: commit {cyc} if{iface} (TX commits {len(tx)}, AECP wire frames {len(wf)})')
        for tc, (wc, wi, fr) in out_pairs:
            if cyc <= tc < nxt and len(fr) > 41 and fr[14] == 0xFB and int.from_bytes(fr[36:38], 'big') & 0x7FFF == 0x10:
                u = 'UNSOLICITED' if fr[36] & 0x80 else 'solicited'
                out.append(f'    TX commit {tc} if{wi} {u} controller {int.from_bytes(fr[26:34], "big"):016x} '
                           f'seq {int.from_bytes(fr[34:36], "big"):04x} at {(tc - cyc) / 1e5:.3f} ms')
    return out


for log in sorted(results.glob('*.log')):
    print('\n'.join(audit(log)))
