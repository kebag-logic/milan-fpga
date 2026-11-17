#!/usr/bin/env python3
"""r6_compare.py HARNESS OUT.md OUT.json: round 4's re-simulated legs as the round-6 harness (HARNESS, a checkout)
regraded them (r6/legs/<leg>/, r6_regrade.sh), against round 5b's grading of the same logs (r5b/legs/<leg>/).

Per leg: the regrade's rc beside round 5b's, and its table.md against round 5b's. Per group: the MRPDU rows, the MRP
run-outs by outcome and the failing ones, and the LeaveAlls by outcome, each against round 5b's. And, from the log
itself, every MRP run-out whose outcome the owner rule moves: round 5b's rules are round 6's with its three earlier
rules restored (selftest_mutants' horizon, served and start_of plants), so each run-out is resolved both ways; for each
that moves, its timer, time, owner, both outcomes, the participants of the frame that answered it before, and the
owner's own first frame after it, if any, and its delay after the owner's opportunity.
"""
import json
import sys
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(sys.argv[1]) / 'tb/verilator/ctrl_service_budget'))
import grade  # noqa: E402
import mrpdu_grade as m  # noqa: E402

S = Path('<scratch>')
SEEDS = ('10092', '10592', '11102', '11602', '12102', '12602', '13102', '13602', '14602', '15032')
LEGS = [f's{t}' for t in SEEDS] + ['p81', 'v1', 'v81']


def earlier() -> list:
    """Round 5b's three rules: the missing-build horizon the latest of every participant's opportunity, a build's
    frames any participant's timed from the first frame's participant, a row's start the earliest of its commit's."""
    return [patch.object(m, 'horizon', lambda log, entry, who: max([entry] + [
                m.opportunity(log, o, entry) for o in m.sends(log)[0]])),
            patch.object(m, 'served', lambda log, entry, who, frames: (frames, min([
                m.opportunity(log, o, entry) for o in m.sends(log)[1].get(frames[0], ())] or [entry])
                if frames else entry)),
            patch.object(m, 'start_of', lambda log, entry, whose: min([
                m.opportunity(log, o, entry) for o in whose] or [entry]))]


def graded(path: Path) -> dict:
    d = json.loads(path.read_text())
    joins = (d.get('passes') or {}).get('joins') or {}
    return dict(rows={p['probe'].split('.mrpdu.')[1]: p['ms'] for p in d['probes'] if '.mrpdu.' in p['probe']},
                runs={k: n for k, n in (joins.get('runs') or {}).items() if n}, failing=joins.get('failing'),
                intervals=(joins.get('count'), joins.get('shortest'), joins.get('longest')),
                leave_all=(joins.get('leave_all') or {}).get('runs'),
                leave_all_failing=(joins.get('leave_all') or {}).get('failing'))


def moved(log_path: Path) -> dict:
    """Each MRP run-out of the log whose outcome round 6's owner rule moves from round 5b's."""
    text = log_path.read_text(errors='replace')
    log = grade.parse(text[:text.rfind('\n') + 1], 100_000_000, 100_000_000)
    ms = lambda c: round(c * 1000 / log.sys_hz, 3)
    entries = [(e, n) for e, n in log.entries if n in m.TIMERS]
    now = {e: m.resolve(log, e) for e, _ in entries}
    with ExitStack() as st:
        for p in earlier():
            st.enter_context(p)
        then = {e: m.resolve(log, e) for e, _ in entries}
    at = m.sends(log)[1]
    out = []
    for e, n in entries:
        if now[e][0] == then[e][0]:
            continue
        who = m.recorded_owner(log, e)
        opp = m.opportunity(log, who, e) if who else e
        out.append(dict(timer=m.TIMERS[n], at_ms=ms(e), owner=who, round5b=then[e][0], round6=now[e][0],
                        answered_by=list(at.get(then[e][1][0], ())) if then[e][1] else [],
                        owner_frame_after_opportunity_ms=ms(now[e][1][0][0] - opp) if now[e][1] else None))
    return dict(run_outs=len(entries), moved=len(out), by_change=_count(out), every=out)


def _count(out: list) -> dict:
    c: dict = {}
    for x in out:
        k = f"{x['round5b']}->{x['round6']}"
        c[k] = c.get(k, 0) + 1
    return c


def main() -> int:
    report = []
    for leg in LEGS:
        new, old = S / f'r6/legs/{leg}', S / f'r5b/legs/{leg}'
        rc = (S / f'r6/legs/{leg}.log.rc').read_text().strip() if (S / f'r6/legs/{leg}.log.rc').exists() else 'none'
        e = dict(leg=leg, rc=rc, rc_round5b=(S / f'r5b/legs/{leg}.log.rc').read_text().strip(),
                 table_same=(new / 'table.md').read_bytes() == (old / 'table.md').read_bytes()
                 if (new / 'table.md').exists() else None, groups={})
        for log_path in sorted(new.glob('*.log')):
            g = log_path.stem
            a, b = graded(old / f'{g}.json'), graded(new / f'{g}.json')
            e['groups'][g] = dict(same={k: a[k] == b[k] for k in a}, round6=b, round5b=a, moves=moved(log_path))
        report.append(e)
        print(leg, rc, e['table_same'], {g: ({k: s for k, s in v['same'].items() if not s},
                                             v['moves']['by_change'], v['round6']['failing'])
                                         for g, v in e['groups'].items()}, flush=True)
    Path(sys.argv[3]).write_text(json.dumps(report, indent=1) + '\n')
    Path(sys.argv[2]).write_text(table(report))
    return 0


def table(report: list[dict]) -> str:
    lines = ['| Leg | rc (round 5b) | table.md as round 5b | Group | run-outs released / empty (round 5b) | '
             'outcomes moved | failing run-outs | MRPDU rows, ms (leaveall / periodic / join, if0), and round 5b\'s | '
             'join intervals as round 5b | LeaveAlls |', '|---|---|---|---|---|---|---|---|---|---|']
    for e in report:
        for g, v in e['groups'].items():
            a, b = v['round5b'], v['round6']
            rows = lambda r: ' / '.join(f"{r['rows'].get(k + '.if0', '-')}" for k in ('leaveall', 'periodic', 'join'))
            la = ', '.join(f'{k} {n}' for k, n in (b['leave_all'] or {}).items() if n) or 'none'
            lines.append(f"| {e['leg']} | {e['rc']} ({e['rc_round5b']}) | {'same' if e['table_same'] else 'differs'} | "
                         f"{g} | {b['runs'].get('released', 0)} / {b['runs'].get('empty', 0)} "
                         f"({a['runs'].get('released', 0)} / {a['runs'].get('empty', 0)}) | "
                         f"{v['moves']['by_change'] or 'none'} | {len(b['failing'] or [])} | {rows(b)} ({rows(a)}) | "
                         f"{'same' if v['same']['intervals'] else 'differs'} | {la} |")
    return '\n'.join(lines) + '\n'


if __name__ == '__main__':
    sys.exit(main())
