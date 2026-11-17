#!/usr/bin/env python3
"""r5_compare.py HARNESS OUT.md OUT.json: round 4's re-simulated legs as the round-5 harness (HARNESS, a checkout)
regraded them (r5/legs/<leg>/, r5_regrade.sh), against round 4's own grading of the same logs.

Per leg: the regrade's rc beside round 4's, and its table.md against round 4's. Per group: the MRPDU rows, the MRP
timer run-outs by outcome and the failing ones, and the LeaveAlls by outcome and owner, each against round 4's; and,
from the log itself, every run-out whose first build sends nothing (mrpdu_grade.resolve's `empty` and `late`): where
the round-5 anchor (mrpdu_grade.anchor, the recorded owner's transmit opportunity) puts its lateness, where round 4's
rule put it (the last on_join_timer callback, any participant's, between the run-out and that build), and whether its
outcome moves.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]) / 'tb/verilator/ctrl_service_budget'))
import grade  # noqa: E402
import mrpdu_grade  # noqa: E402

S = Path('<scratch>')
SEEDS = ('10092', '10592', '11102', '11602', '12102', '12602', '13102', '13602', '14602', '15032')


def legs() -> list[tuple[str, Path, str]]:
    """Each leg, round 4's graded results and round 4's rc file name."""
    out = [(f's{t}', S / f'seeds/b4-sync-{t}/results', f's{t}') for t in SEEDS]
    out += [('p81', S / 'r4/b81/required-results', 'p81-required'), ('v1', S / 'r4/b1x1-V/results', 'v1'),
            ('v81', S / 'r4/b81-V/results', 'v81')]
    return out


def graded(path: Path) -> dict:
    d = json.loads(path.read_text())
    joins = (d.get('passes') or {}).get('joins') or {}
    return dict(rows={p['probe'].split('.mrpdu.')[1]: p['ms'] for p in d['probes'] if '.mrpdu.' in p['probe']},
                runs=joins.get('runs'), failing=joins.get('failing'),
                leave_all=(joins.get('leave_all') or {}).get('runs'),
                leave_all_failing=(joins.get('leave_all') or {}).get('failing'),
                probes={p['probe']: (p.get('ms'), p.get('status')) for p in d['probes']})


def earlier_anchor(log: grade.Log, entry: int, build: int) -> int:
    """Round 4's rule: the last on_join_timer callback, of any participant, after the run-out and at or before its
    first build."""
    return max([entry] + [c for c, name in log.entries if name == 'on_join_timer' and entry < c <= build])


def empties(log_path: Path) -> dict:
    """Every run-out whose first build sends nothing, by the round-5 anchor and round 4's rule."""
    text = log_path.read_text(errors='replace')
    log = grade.parse(text[:text.rfind('\n') + 1], 100_000_000, 100_000_000)
    builds = mrpdu_grade.index(log)[0]
    bound = int(mrpdu_grade.LATE_MS * log.sys_hz / 1000)
    ms = lambda c: round(c * 1000 / log.sys_hz, 3)
    out, owners = [], dict.fromkeys(('recorded', 'none'), 0)
    for entry, name, outcome in mrpdu_grade.outcomes(log):
        if outcome not in ('empty', 'late') or mrpdu_grade.released(log, entry):
            continue
        build = next(b for b in builds if b > entry)
        now, then = mrpdu_grade.anchor(log, entry), earlier_anchor(log, entry, build)
        owners['recorded' if mrpdu_grade.recorded_owner(log, entry) else 'none'] += 1
        before = 'late' if build > then + bound else 'empty'
        out.append(dict(timer=name, at_ms=ms(entry), owner=mrpdu_grade.recorded_owner(log, entry),
                        build_after_anchor_ms=ms(build - now), build_after_earlier_ms=ms(build - then),
                        outcome=outcome, earlier_outcome=before, anchor_moved=now != then))
    return dict(count=len(out), owners=owners, moved=sum(e['anchor_moved'] for e in out),
                outcome_changed=[e for e in out if e['outcome'] != e['earlier_outcome']],
                worst_after_anchor_ms=max([e['build_after_anchor_ms'] for e in out], default=None),
                late_ms=mrpdu_grade.LATE_MS, every=out)


def main() -> int:
    report = []
    for leg, r4, rc4 in legs():
        new = S / f'r5/legs/{leg}'
        rc = (S / f'r5/legs/{leg}.log.rc').read_text().strip() if (S / f'r5/legs/{leg}.log.rc').exists() else 'none'
        e = dict(leg=leg, rc=rc, rc_round4=(S / f'r4/logs/{rc4}.log.rc').read_text().strip(),
                 table_same=(new / 'table.md').read_bytes() == (r4 / 'table.md').read_bytes()
                 if (new / 'table.md').exists() else None, groups={})
        for log_path in sorted(new.glob('*.log')):
            g = log_path.stem
            a, b = graded(r4 / f'{g}.json'), graded(new / f'{g}.json')
            e['groups'][g] = dict(same={k: a[k] == b[k] for k in a}, round5={k: b[k] for k in b if k != 'probes'},
                                  probes_differ={p: (a['probes'].get(p), v) for p, v in b['probes'].items()
                                                 if a['probes'].get(p) != v},
                                  empty_builds=empties(log_path))
        report.append(e)
        print(leg, rc, e['table_same'], {g: (all(v['same'].values()), v['empty_builds']['count'],
                                             v['empty_builds']['moved'], len(v['empty_builds']['outcome_changed']))
                                         for g, v in e['groups'].items()}, flush=True)
    Path(sys.argv[3]).write_text(json.dumps(report, indent=1) + '\n')
    Path(sys.argv[2]).write_text(table(report))
    return 0


def table(report: list[dict]) -> str:
    lines = ['| Leg | rc (round 4) | table.md as round 4 | Group | rows, run-outs, LeaveAlls as round 4 | LeaveAlls '
             '(round 5) | builds that send nothing: count / anchor moved / outcome moved / worst after the anchor, ms |',
             '|---|---|---|---|---|---|---|']
    for e in report:
        for g, v in e['groups'].items():
            eb = v['empty_builds']
            same = 'same' if all(v['same'].values()) else 'differs: ' + ', '.join(k for k, s in v['same'].items() if not s)
            la = v['round5']['leave_all']
            lines.append(f"| {e['leg']} | {e['rc']} ({e['rc_round4']}) | {'same' if e['table_same'] else 'differs'} | {g} | "
                         f"{same} | {', '.join(f'{k} {n}' for k, n in la.items() if n) or 'none'} | "
                         f"{eb['count']} / {eb['moved']} / {len(eb['outcome_changed'])} / {eb['worst_after_anchor_ms']} |")
    return '\n'.join(lines) + '\n'


if __name__ == '__main__':
    sys.exit(main())
