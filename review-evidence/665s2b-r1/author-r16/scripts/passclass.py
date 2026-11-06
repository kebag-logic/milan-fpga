#!/usr/bin/env python3
"""Every pass of a harness run, by its class (#665, ctrl_loop.h, THE SHARE; round 16 item 2), read off each group's
log: the heaviest of each class, its CPU cycles, its group, its start, its four costliest modules.

A PASS line's writes (its W list, word addresses) say what it took: EVT_TAIL (0x64, word 0x19) once an event, a
channel's RX_TAIL (0x104 + 0x20 k, word 0x41 + 8 k) once a record; its modules say which callbacks ran. The
classes:
  whole-step      a pass given whole to an aged step (aged=1): the step and THE RETRY's round
  whole           a pass given whole to an aged retry or an aged build: no poll ran (no ADP, MAAP or SRP poll)
                  and it took nothing; whole-transmit when it wrote SRP's TX_HEAD (0x188, word 0x62)
  records         a pass that took a record: its events, records and polls, no deferrable work
  events          a pass that took events and no record: one event carries THE TRANSMIT's build
  none            a pass that took nothing and wrote to the mailbox: the polls' owed output, THE TRANSMIT's build,
                  THE RETRY's round, THE STEP before its deadline
  step            any pass that carries the store's step (STEPPASS, or step=1 on a work pass), also counted above
  build           a pass that took no record and wrote SRP's TX_HEAD: THE TRANSMIT's build, or the poll's
                  owed frame, also counted above
  idle            a run of passes that wrote nothing (IDLE: the run's longest only)

usage: passclass.py RESULTS_DIR [RESULTS_DIR...]   (prints one table; JSON with --json)
"""
import json
import re
import sys
from pathlib import Path

EVT_TAIL, SRP_TX_HEAD = 0x19, 0x62
RX_TAILS = {0x41 + 8 * k for k in range(5)}
POLLS = ('adp_mbx', 'maap_mbx', 'srp_mbx')


def classify(line: str) -> tuple[str, dict]:
    k = line.split(' W', 1)[0].split()
    writes = line.split(' W', 1)[1].split() if ' W' in line else []
    addrs = [int(w.split(':')[1], 16) for w in writes if w.count(':') == 2]
    mods = dict((m.split(':')[0], int(m.split(':')[1]))
                for m in line.split(' mods=')[1].split(' W')[0].split(',') if m) if ' mods=' in line else {}
    events = sum(a == EVT_TAIL for a in addrs)
    records = sum(a in RX_TAILS for a in addrs)
    if ' aged=1' in line:
        cls = 'whole-step'
    elif not any(p in mods for p in POLLS) and not events and not records:
        cls = 'whole-transmit' if SRP_TX_HEAD in addrs else 'whole'
    elif records:
        cls = 'records'
    elif events:
        cls = 'events'
    else:
        cls = 'none'
    return cls, dict(cycles=int(k[4]), start=int(k[2]), mods=mods, events=events, records=records,
                     step=' step=1' in line, tx=SRP_TX_HEAD in addrs)


def main() -> int:
    dirs = [Path(a) for a in sys.argv[1:] if a != '--json']
    best: dict[str, dict] = {}
    counts: dict[str, int] = {}

    def keep(cls: str, rec: dict) -> None:
        counts[cls] = counts.get(cls, 0) + 1
        if cls not in best or rec['cycles'] > best[cls]['cycles']:
            best[cls] = rec

    for d in dirs:
        for log in sorted(d.glob('*.log')):
            group = log.stem
            lines = log.read_text(errors='replace').splitlines()
            if lines and not lines[-1].endswith(('-', ' ')) and not lines[-1].split()[0].isupper():
                lines = lines[:-1]
            for line in lines:
                if len(line.split()) < 4:   # a line a running group has not finished writing
                    continue
                if line.startswith('PASS '):
                    try:
                        cls, rec = classify(line)
                    except (IndexError, ValueError):   # a line a running group has not finished writing
                        continue
                    rec['group'] = group
                    keep(cls, rec)
                    if rec['step']:
                        keep('step', rec)
                    if rec.pop('tx') and cls in ('events', 'none'):
                        keep('build', rec)
                elif line.startswith('STEPPASS '):
                    k = line.split()
                    if len(k) < 5 or not k[4].isdigit():   # a line a running group has not finished writing
                        continue
                    rec = dict(cycles=int(k[4]), start=int(k[2]), mods={}, group=group,
                               aged=' aged=1' in line)
                    keep('whole-step' if rec['aged'] else 'step', rec)
                elif line.startswith('IDLE '):
                    keep('idle', dict(cycles=int(line.split()[3]), start=0, mods={}, group=group))
    if '--json' in sys.argv:
        print(json.dumps(dict(best=best, counts=counts), indent=1))
        return 0
    print('| Class | Passes | Heaviest, CPU cycles | Under the share (200,000) | Group | Costliest modules |')
    print('|---|---:|---:|---:|---|---|')
    for cls in ('records', 'events', 'none', 'build', 'step', 'whole-step', 'whole', 'whole-transmit', 'idle'):
        if cls not in best:
            continue
        b = best[cls]
        top = ', '.join(f'{n} {c:,}' for n, c in sorted(b['mods'].items(), key=lambda x: -x[1])[:4])
        print(f"| {cls} | {counts[cls]:,} | {b['cycles']:,} | {200_000 - b['cycles']:,} | {b['group']} | {top} |")
    return 0


if __name__ == '__main__':
    sys.exit(main())
