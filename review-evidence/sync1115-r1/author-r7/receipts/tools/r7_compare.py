#!/usr/bin/env python3
"""r7_compare.py HARNESS OUT.md OUT.json: round 4's thirteen legs re-simulated with the round-7 testbench (each MRPDU
build names its participant) and regraded by the round-7 harness (HARNESS, a checkout; r7/legs/<leg>/), against round
4's traces and round 6's grading of them (r6/legs/<leg>/).

Per leg: the regrade's rc beside round 6's, and its table.md against round 6's. Per group:
- the new trace against round 4's, line for line, once each build_mrpdu ENTRY's participant is taken off;
- the builds by recorded participant, and whether each build that commits an MRPDU of its own names its participant;
- the MRPDU rows, run-outs by outcome, failing run-outs, join intervals and LeaveAlls against round 6's;
- every owned MRP run-out whose outcome moves from round 6's rule, round 7's resolved both ways on the new trace
  (round 6's rule is round 7's with every build a candidate, selftest_mutants' first-build plant), with the build that
  settled it under each, its recorded participant and time, and for round 7 whether it settled on the owner's frame;
- for every run-out round 7 grades `empty`, where the owner's own build came after the owner's opportunity.
"""
import itertools
import json
import re
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(sys.argv[1]) / 'tb/verilator/ctrl_service_budget'))
import grade  # noqa: E402
import mrpdu_grade as m  # noqa: E402

S = Path('<scratch>')
SEEDS = ('10092', '10592', '11102', '11602', '12102', '12602', '13102', '13602', '14602', '15032')
TRACES = {**{f's{t}': (S / f'seeds/b7-sync-{t}/results', S / f'seeds/b4-sync-{t}/results') for t in SEEDS},
          'p81': (S / 'r7/b81/results', S / 'r4/b81/results'), 'v1': (S / 'r7/b1x1-V/results', S / 'r4/b1x1-V/results'),
          'v81': (S / 'r7/b81-V/results', S / 'r4/b81-V/results')}
BUILD = re.compile(r'^(ENTRY \d+ build_mrpdu)(?: (if\d+ (?:MSRP|MVRP)|unresolved [0-9a-f]{8}))?$')


def same_but_builder(old: Path, new: Path) -> dict:
    def stripped(lines):
        for line in lines:
            mt = BUILD.match(line.rstrip('\n'))
            yield (mt.group(1) + '\n') if mt else line
    differ = n = 0
    with old.open(errors='replace') as a, new.open(errors='replace') as b:
        for n, (x, y) in enumerate(itertools.zip_longest(a, stripped(b)), 1):
            differ += x != y
    return dict(lines=n, differ=differ)


def settling(log: grade.Log, entry: int, who: str) -> dict | None:
    """The build that settles the owned run-out (mrpdu_grade.settle's walk), its participant and time, and whether it
    settled on the owner's frame; None where none settles it."""
    builds = m.index(log)[0]
    start = m.opportunity(log, who, entry)
    for k in range(m.bisect_right(builds, entry), len(builds)):
        b = builds[k]
        kind = m.candidate(log, b, who, start)
        if kind is None:
            continue
        mine, _ = m.served(log, entry, who, m.run_from(log, k)[1])
        if mine or kind == 'own':
            ms = lambda c: round((c - start) * 1000 / log.sys_hz, 3)
            return dict(build_after_opportunity_ms=ms(b), builder=m.builder(log, b), on_owner_frame=bool(mine),
                        frame_after_opportunity_ms=ms(mine[0][0]) if mine else None)
    return None


def moves(log_path: Path) -> dict:
    text = log_path.read_text(errors='replace')
    log = grade.parse(text[:text.rfind('\n') + 1], 100_000_000, 100_000_000)
    ms = lambda c: round(c * 1000 / log.sys_hz, 3)
    builds = m.index(log)[0]
    named = [m.builder(log, b) for b in builds]
    entries = [(e, n) for e, n in log.entries if n in m.TIMERS]
    now = {e: m.resolve(log, e)[0] for e, _ in entries}
    detail_now = {e: settling(log, e, m.recorded_owner(log, e)) for e, _ in entries if m.recorded_owner(log, e)}
    with patch.object(m, 'candidate', lambda log, b, who, start: 'own'):
        then = {e: m.resolve(log, e)[0] for e, _ in entries}
        detail_then = {e: settling(log, e, m.recorded_owner(log, e)) for e, _ in entries if m.recorded_owner(log, e)}
    moved = [dict(timer=m.TIMERS[n], at_ms=ms(e), owner=m.recorded_owner(log, e), round6=then[e], round7=now[e],
                  round6_settled_by=detail_then.get(e), round7_settled_by=detail_now.get(e))
             for e, n in entries if then[e] != now[e]]
    empties = [detail_now[e]['build_after_opportunity_ms'] for e, _ in entries if now[e] == 'empty' and detail_now.get(e)]
    at, sent = m.sends(log)[1], m.index(log)[2]
    agree = disagree = 0
    for k, b in enumerate(builds):
        stop = builds[k + 1] if k + 1 < len(builds) else 1 << 62
        mine = {w for c in sent if b < c[0] < stop for w in at.get(c, ())}
        if mine and named[k]:
            agree, disagree = (agree + 1, disagree) if named[k] in mine else (agree, disagree + 1)
    by = {}
    for w in named:
        by[w or 'none'] = by.get(w or 'none', 0) + 1
    return dict(run_outs=len(entries), builds=len(builds), builds_by_participant=by,
                frame_bearing_builds_agreeing=agree, disagreeing=disagree, moved=len(moved),
                by_change={f"{x['round6']}->{x['round7']}": sum(1 for y in moved if (y['round6'], y['round7']) ==
                                                                 (x['round6'], x['round7'])) for x in moved},
                empties=len(empties), latest_owner_empty_build_ms=max(empties, default=None), every=moved)


def graded(path: Path) -> dict:
    d = json.loads(path.read_text())
    joins = (d.get('passes') or {}).get('joins') or {}
    return dict(rows={p['probe'].split('.mrpdu.')[1]: p['ms'] for p in d['probes'] if '.mrpdu.' in p['probe']},
                runs={k: n for k, n in (joins.get('runs') or {}).items() if n}, failing=joins.get('failing'),
                intervals=(joins.get('count'), joins.get('shortest'), joins.get('longest')),
                leave_all=(joins.get('leave_all') or {}).get('runs'),
                leave_all_failing=(joins.get('leave_all') or {}).get('failing'),
                probes={p['probe']: (p.get('ms'), p.get('status')) for p in d['probes']})


def main() -> int:
    report = []
    for leg, (new_dir, old_dir) in TRACES.items():
        reg, r6 = S / f'r7/legs/{leg}', S / f'r6/legs/{leg}'
        rc = (S / f'r7/legs/{leg}.log.rc').read_text().strip() if (S / f'r7/legs/{leg}.log.rc').exists() else 'none'
        e = dict(leg=leg, rc=rc, rc_round6=(S / f'r6/legs/{leg}.log.rc').read_text().strip(),
                 table_same=(reg / 'table.md').read_bytes() == (r6 / 'table.md').read_bytes()
                 if (reg / 'table.md').exists() else None, groups={})
        for log_path in sorted(new_dir.glob('*.log')):
            g = log_path.stem
            if not (old_dir / f'{g}.log').exists():
                continue
            a, b = graded(r6 / f'{g}.json'), graded(reg / f'{g}.json')
            e['groups'][g] = dict(trace=same_but_builder(old_dir / f'{g}.log', log_path),
                                  same={k: a[k] == b[k] for k in a}, round7={k: v for k, v in b.items() if k != 'probes'},
                                  probes_differ={p: (a['probes'].get(p), v) for p, v in b['probes'].items()
                                                 if a['probes'].get(p) != v},
                                  moves=moves(log_path))
        report.append(e)
        print(leg, rc, e['table_same'], {g: (v['trace']['differ'], v['moves']['disagreeing'], v['moves']['by_change'],
                                             {k: s for k, s in v['same'].items() if not s}, v['round7']['failing'])
                                         for g, v in e['groups'].items()}, flush=True)
    Path(sys.argv[3]).write_text(json.dumps(report, indent=1) + '\n')
    Path(sys.argv[2]).write_text(table(report))
    return 0


def table(report: list[dict]) -> str:
    lines = ['| Leg | rc (round 6) | table.md as round 6 | Group | trace as round 4, build participant out | '
             'builds by participant (frame-bearing agreeing / not) | outcomes moved | failing run-outs | rows, '
             'intervals, LeaveAlls as round 6 | latest owner empty build after its opportunity, ms |',
             '|---|---|---|---|---|---|---|---|---|---|']
    for e in report:
        for g, v in e['groups'].items():
            mv, tr = v['moves'], v['trace']
            same = 'same' if all(v['same'][k] for k in ('rows', 'intervals', 'leave_all', 'failing')) else 'differs'
            lines.append(f"| {e['leg']} | {e['rc']} ({e['rc_round6']}) | {'same' if e['table_same'] else 'differs'} | "
                         f"{g} | {'identical' if tr['differ'] == 0 else str(tr['differ']) + ' lines differ'} "
                         f"({tr['lines']:,} lines) | {mv['builds_by_participant']} ({mv['frame_bearing_builds_agreeing']}"
                         f" / {mv['disagreeing']}) | {mv['by_change'] or 'none'} | {len(v['round7']['failing'] or [])} | "
                         f"{same} | {mv['latest_owner_empty_build_ms']} |")
    return '\n'.join(lines) + '\n'


if __name__ == '__main__':
    sys.exit(main())
