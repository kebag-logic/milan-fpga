#!/usr/bin/env python3
"""Reviewer's independent recomputation of the budget figures from the raw observation logs.

Usage: recompute.py CHECKOUT RESULTS_DIR INTERFACES
It does not import the harness's grade.py or scenario.py. It reads the mailbox
contract (sw/mailbox) for register offsets only, and recomputes from the raw
PASS / MS / MARK / LINK / RXS / RXE / RXC / W(rite) / WIRE lines:
  - the testbench clock ratio (consecutive printed passes: sys delta = 2 x CPU cycles),
    and the NOW_MS spacing (100,000 bus cycles);
  - each group's worst pass and the composed maximum, in CPU cycles and ms at 50 MHz;
  - the four backlog rows: start by the probe's own rule, end by an independent rule
    (the TMR_CMD write, or the response frame's wire departure as an upper bound).
"""
import json
import re
import sys
from pathlib import Path

CPU_PER_MS = 50_000
SYS_PER_MS = 100_000


def load_contract(checkout: Path):
    sys.path.insert(0, str(checkout / 'sw/mailbox'))
    from mailbox_model import load
    c = load()
    regs = {r.name: r.offset for r in c.registers}
    ch = {x.name: n for n, x in enumerate(c.channels)}
    return regs['TMR_CMD'] // 4, ch


def parse(path: Path) -> dict:
    out = dict(passes=[], ms=[], marks={}, link=[], rxs=[], rxe=[], rxc=[], writes=[], wire=[])
    for line in path.read_text().splitlines():
        if not line:
            continue
        kind, *rest = line.split()
        if kind == 'PASS':
            idx, s_sys, s_cpu, cyc = (int(v) for v in rest[:4])
            out['passes'].append((idx, s_sys, s_cpu, cyc))
            if ' W' in line:
                for w in line.split(' W', 1)[1].split():
                    c, word, val = w.split(':')
                    out['writes'].append((int(c), int(word, 16), int(val, 16)))
        elif kind == 'MS':
            out['ms'].append(int(rest[0]))
        elif kind == 'MARK':
            out['marks'][rest[1]] = int(rest[0])
        elif kind == 'LINK':
            out['link'].append((int(rest[0]), int(rest[1]), int(rest[2])))
        elif kind == 'RXS':
            out['rxs'].append((int(rest[0]), rest[3] if len(rest) > 3 else '-'))
        elif kind == 'RXE':
            out['rxe'].append(int(rest[0]))
        elif kind == 'RXC':
            out['rxc'].append((int(rest[0]), int(rest[1])))
        elif kind == 'WIRE':
            out['wire'].append((int(rest[0]), int(rest[2]), int(rest[1]), bytes.fromhex(rest[3])))  # WIRE cycle if ch hex
    out['writes'].sort()
    return out


def clock_checks(log: dict) -> dict:
    ok = bad = 0
    p = log['passes']
    for a, b in zip(p, p[1:]):
        if b[0] == a[0] + 1:
            if b[1] - a[1] == 2 * a[3] and b[2] - a[2] == a[3]:
                ok += 1
            else:
                bad += 1
    ms = log['ms']
    spacing = sorted({b - a for a, b in zip(ms, ms[1:])})
    return dict(consecutive_pass_pairs_ok=ok, consecutive_pass_pairs_bad=bad, ms_spacing=spacing)


def tagged_commit(log: dict, tag: str, ch: int) -> int | None:
    """The receive commit on ch that follows the tagged frame's last byte."""
    starts = [c for c, t in log['rxs'] if t == tag]
    if not starts:
        return None
    rxe = min(e for e in log['rxe'] if e > starts[0])
    hits = [c for c, k in log['rxc'] if c >= rxe and k == ch]
    return hits[0] if hits else None


def first_write(log: dict, word: int, after: int, pred) -> int | None:
    hits = [c for c, w, v in log['writes'] if c >= after and w == word and pred(v)]
    return hits[0] if hits else None


def first_wire(log: dict, after: int, ch: int, pred) -> int | None:
    hits = [c for c, k, _, fr in log['wire'] if c >= after and k == ch and pred(fr)]
    return hits[0] if hits else None


def acmp_seq(fr: bytes) -> int | None:
    return int.from_bytes(fr[62:64], 'big') if len(fr) > 63 and fr[14] == 0xFC and fr[15] & 1 else None


def main() -> int:
    checkout, results, n_if = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
    tmr, ch = load_contract(checkout)
    report = dict(results=str(results), interfaces=n_if, groups={})
    for log_path in sorted(results.glob('*.log')):
        log = parse(log_path)
        if not log['passes']:
            report['groups'][log_path.stem] = dict(passes=0)
            continue
        worst = max(log['passes'], key=lambda p: p[3])
        g = dict(passes=len(log['passes']), worst_cpu=worst[3], worst_ms=round(worst[3] / CPU_PER_MS, 3),
                 clock=clock_checks(log))
        m = log['marks']
        if 'composed' in m and 'composed_end' in m:
            inside = [p for p in log['passes'] if m['composed'] <= p[1] <= m['composed_end']]
            top = max(inside, key=lambda p: p[3])
            g.update(composed_cpu=top[3], composed_ms=round(top[3] / CPU_PER_MS, 3))
        rows = {}
        if 'backlog.event.if0' in m:
            start = [c for c, i, v in log['link'] if c >= m['backlog.event.if0'] and i == 0 and v == 0][0]
            end = first_write(log, tmr, start, lambda v: v & 0xFF == 0 and v >> 30 == 2)
            rows['event behind 15 others'] = dict(start=start, end=end, ms=None if end is None or start is None else round((end - start) / SYS_PER_MS, 3))
        if 'backlog.acmp_command.if0' in m:
            start = tagged_commit(log, 'backlog.acmp_command.if0', ch['acmp'])
            wire = first_wire(log, start, ch['acmp'], lambda fr: acmp_seq(fr) == 0x72FF)
            rows['ACMP command behind a full acmp ring'] = dict(
                start=start, wire=wire, wire_ms=None if wire is None or start is None else round((wire - start) / SYS_PER_MS, 3))
        if 'backlog.owed.if0' in m:
            start = tagged_commit(log, 'backlog.owed.if0', ch['acmp'])
            wire = first_wire(log, start, ch['acmp'], lambda fr: acmp_seq(fr) == 0x7387)
            rows['response with 7 owed ahead'] = dict(start=start, wire=wire,
                                                      wire_ms=None if wire is None or start is None else round((wire - start) / SYS_PER_MS, 3),
                                                      room=m.get('room'))
        if 'backlog.adp_available.if0' in m:
            start = tagged_commit(log, 'backlog.adp_available.if0', ch['adp'])
            end = first_write(log, tmr, start, lambda v: v & 0xFF == n_if and v >> 30 == 1)
            rows['ENTITY_AVAILABLE behind the adp ring'] = dict(start=start, end=end,
                                                                ms=None if end is None or start is None else round((end - start) / SYS_PER_MS, 3))
        if rows:
            g['backlog_rows'] = rows
        report['groups'][log_path.stem] = g
    print(json.dumps(report, indent=1))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
