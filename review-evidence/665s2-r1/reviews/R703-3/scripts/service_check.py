#!/usr/bin/env python3
"""Reviewer's independent recomputation of each composed window's load and its service, from
the raw log only (the mailbox contract read for offsets, ring sizes and buckets; never grade.py
or scenario.py), compared with the harness's own graded rows.

Usage: service_check.py CHECKOUT RESULTS_DIR GROUP...
For each group: the population committed in [composed, composed_end] against the population
derived here from the contract (each channel min(burst, ring room at the load frame's size);
16 event records less the row's own; ADP the ring's room in the refill leg); then, per channel,
the first and last record committed in the window: the RX_TAIL write whose cumulative count
(mod 2^16) first covers the record's last word, and the end of the pass carrying that write
(start + CPU cycles x 2 bus cycles). A record no write covers is 'never'. Each is printed with
the harness's figure from RESULTS_DIR/<group>.json and whether the two agree to 0.01 ms.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1] + '/sw/mailbox')
from mailbox_model import load  # noqa: E402

c = load()
names = [x.name for x in c.channels]
chreg = {r.name: r.offset for r in c.ch_registers}
tail_word = {(c.ch_base + n * c.ch_stride + chreg['RX_TAIL']) // 4: n for n in range(len(names))}
HDR = len(c.rx_header)
# Load frame sizes from their clauses: ADPDU 68 + 14, ACMPDU 56 + 14, the others padded to 60.
SIZE = {'adp': 82, 'acmp': 70, 'aecp': 60, 'maap': 60, 'srp': 60}


def contract_load(group: str) -> dict:
    """The population a composed row must commit, from the contract only."""
    out = {}
    for ch in c.channels:
        room = ch.rx_words // (HDR + (SIZE[ch.name] + 3) // 4)
        out[ch.name] = min(ch.burst, room)
        if group == 'backlog-adp-refill' and ch.name == 'adp':
            out[ch.name] = room
    out['GM'] = c.evt_words // c.ev_words - 1
    if group == 'backlog':
        out['LINK'] = 1
    return out


def audit(results: Path, group: str) -> list[str]:
    lines = (results / f'{group}.log').read_text().splitlines()
    marks = {l.split()[2]: int(l.split()[1]) for l in lines if l.startswith('MARK')}
    t0, t1 = marks['composed'], marks['composed_end']
    size, rx, passes, pads = 0, [], [], []
    for l in lines:
        f = l.split()
        if not f:
            continue
        if f[0] == 'RXS':
            size = int(f[3])
        elif f[0] == 'RXC':
            rx.append((int(f[1]), int(f[2]), size))
        elif f[0] == 'PASS':
            start, cyc = int(f[2]), int(f[4])
            writes = [w.split(':') for w in l.split(' W', 1)[1].split()] if ' W' in l else []
            passes.append((start, start + 2 * cyc, [(int(w[0]), int(w[1], 16), int(w[2], 16)) for w in writes]))
        elif f[0] in ('GM', 'LINK'):
            pads.append((int(f[1]), f[0]))
    got = {}
    for cyc, ch, _ in rx:
        if t0 <= cyc <= t1:
            got[names[ch]] = got.get(names[ch], 0) + 1
    for cyc, kind in pads:
        if t0 <= cyc <= t1:
            got[kind] = got.get(kind, 0) + 1
    want = contract_load(group)
    out = [f'== {group}: window {(t1 - t0) / 1e5:.2f} ms; committed {got}; contract {want}; '
           f'{"AGREE" if got == want else "DIFFER"}']
    graded = json.loads((results / f'{group}.json').read_text())
    rows = {r['probe']: r for r in graded['probes']}
    finish = max(p[1] for p in passes)
    for n, name in enumerate(names):
        tails = [(cyc, val, end) for start, end, ws in passes for cyc, word, val in ws if tail_word.get(word) == n]
        released, last, k, rec = 0, 0, 0, []
        acc = 0
        for cyc, ch, sz in rx:
            if ch != n:
                continue
            acc += HDR + (sz + 3) // 4
            at = None
            while released < acc and k < len(tails):
                released += (tails[k][1] - last) & 0xFFFF
                last = tails[k][1]
                k += 1
            if released >= acc:
                at = tails[k - 1][2]
            rec.append((cyc, at))
        inside = [r for r in rec if t0 <= r[0] <= t1]
        if not inside:
            continue
        for which, (cyc, end) in (('first', inside[0]), ('last', inside[-1])):
            mine = f'{(end - cyc) / 1e5:.2f} ms' if end is not None else f'never (>= {(finish - cyc) / 1e5:.2f} ms)'
            theirs = [r for p, r in rows.items() if f'.service.{name}.{which}.' in p]
            t = theirs[0] if theirs else None
            tv = (f"{'never' if t.get('starved') else ''} {t['ms']:.2f} ms".strip()) if t else 'absent'
            ok = t is not None and bool(t.get('starved')) == (end is None) and (
                end is None or abs(t['ms'] - (end - cyc) / 1e5) < 0.01)
            out.append(f'  {name} {which}: mine {mine}; harness {tv}; {"AGREE" if ok else "DIFFER"}')
    comp = graded['passes']['composed']
    out.append(f"  harness window: serviced {comp.get('serviced')}, unreleased {comp.get('unreleased')}, "
               f"longest pass {comp['cycles']:,}")
    return out


if __name__ == '__main__':
    for g in sys.argv[3:]:
        print('\n'.join(audit(Path(sys.argv[2]), g)))
