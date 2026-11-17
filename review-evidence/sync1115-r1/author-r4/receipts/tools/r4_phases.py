#!/usr/bin/env python3
"""r4_phases.py HARNESS OUT.md OUT.json: the round-4 re-simulations, graded by HARNESS's checkout (the head's harness).

Per leg and group:
- every MRP timer callback's ENTRY line and the owner it names (an owned ENTRY with no owner, or `unresolved`, is
  counted), and the PARTICIPANT bindings;
- every LeaveAll expiry from mrpdu_grade.leave_alls: its recorded owner, outcome, the owner's first transmit
  opportunity, the owner's first MRPDU and LeaveAll after it, and the LeaveAll's delay after the opportunity;
- the MRPDU rows and the JOINS LeaveAll counts of the run's own result JSON, beside the ones the earlier log's result
  JSON holds (round 3's regrade);
- the new log against the earlier one it repeats with the owner record taken out (each PARTICIPANT line dropped and
  the owner taken off each timer callback's ENTRY line): every other line must be identical.
"""
import itertools
import json
import re
import sys
from pathlib import Path

HARNESS = Path(sys.argv[1]) / 'tb/verilator/ctrl_service_budget'
sys.path.insert(0, str(HARNESS))
import grade  # noqa: E402
import mrpdu_grade  # noqa: E402

S = Path('<scratch>')
B2 = S / 'budget2'
SEEDS = ('10092', '10592', '11102', '11602', '12102', '12602', '13102', '13602', '14602', '15032')
OWNED = re.compile(r'^(ENTRY \d+ on_(?:la|pt|join)_timer)(?: (if\d+ (?:MSRP|MVRP)|unresolved [0-9a-f]{8}))?$')


def legs() -> list[dict]:
    """Each re-simulated leg: name, the phase's MAC source, its new results, and each group's earlier results."""
    out = [dict(leg=f's{t}', phase=True, clone=S / f'seeds/c-sync-{t}', new=S / f'seeds/b4-sync-{t}/results',
                old={g: S / f'seeds/b-sync-{t}/results' for g in ('save-held', 'save-starved')}) for t in SEEDS]
    out.append(dict(leg='p81', phase=True, clone=S / 'r4/c-head', new=S / 'r4/b81/required-results',
                    old={'save-held': B2 / 'b81/results-a1', 'save-starved': B2 / 'b81/results-a2'}))
    for leg, build in (('v1', 'b1x1-V'), ('v81', 'b81-V')):
        out.append(dict(leg=leg, phase=False, clone=S / 'r4/c-head', new=S / f'r4/{build}/results',
                        old={g: B2 / f'{build}/results' for g in ('srp-talker', 'srp-talker-loss')}))
    return out


def same_but_owner(old: Path, new: Path) -> dict:
    """The new log, its owner record taken out, line for line against the old one."""
    kinds = dict(participant=0, owned=0, owner_named=0, owner_unresolved=0, owner_missing=0)
    def stripped(lines):
        for line in lines:
            if line.startswith('PARTICIPANT '):
                kinds['participant'] += 1
                continue
            m = OWNED.match(line.rstrip('\n'))
            if m:
                kinds['owned'] += 1
                who = m.group(2)
                kinds['owner_missing' if who is None else 'owner_unresolved' if who.startswith('unresolved')
                      else 'owner_named'] += 1
                line = m.group(1) + '\n'
            yield line
    differ, first, n = 0, None, 0
    with old.open(errors='replace') as a, new.open(errors='replace') as b:
        for n, (x, y) in enumerate(itertools.zip_longest(a, stripped(b)), 1):
            if x != y:
                differ += 1
                first = first or n
    return dict(lines=n, differ=differ, first_differing_line=first, **kinds)


def ms(c):
    return None if c is None else round(c / 1e5, 3)


def graded(log_path: Path) -> dict:
    text = log_path.read_text(errors='replace')
    log = grade.parse(text[:text.rfind('\n') + 1], 100_000_000, 100_000_000)
    alls = []
    for r in mrpdu_grade.leave_alls(log):
        opp, sent = r.get('opportunity'), r.get('sent')
        alls.append(dict(at_ms=ms(r['at']), owner=r.get('who'), outcome=r['outcome'], opportunity_ms=ms(opp),
                         first_ms=ms(r.get('first')), sent_ms=ms(sent),
                         after_opportunity_ms=None if sent is None or opp is None else round((sent - opp) / 1e5, 3)))
    owners = {}
    for (_, name), who in log.owners.items():
        owners.setdefault(name, {}).setdefault(who or 'unresolved', 0)
        owners[name][who or 'unresolved'] += 1
    return dict(leave_alls=alls, owners=owners, participants=[(ms(c), f'{a:08x}', who) for c, a, who in log.participants],
                late_ms=mrpdu_grade.LATE_MS)


def result(results: Path, group: str) -> dict:
    p = results / f'{group}.json'
    if not p.exists():
        return {}
    d = json.loads(p.read_text())
    rows = {q['probe'].split('.mrpdu.')[1]: q['ms'] for q in d['probes'] if '.mrpdu.' in q['probe']}
    joins = (d.get('passes') or {}).get('joins') or {}
    return dict(rows=rows, leave_all=joins.get('leave_all'), joins_failing=joins.get('failing'),
                probe_instances=len(d['probes']), row_misses=[q['probe'] for q in d['probes'] if not q.get('within_budget')])


def mac_of(clone: Path) -> str:
    m = re.search(r'^  mac_address: "([0-9a-f:]+)"', (clone / 'configs/endstation_ax7101_8x8.yaml').read_text(), re.M)
    return m[1]


def main() -> int:
    out = []
    for leg in legs():
        rc_name = "p81-required" if leg["leg"] == "p81" else leg["leg"]
        rc_file = S / f"r4/logs/{rc_name}.log.rc"
        entry = dict(leg=leg['leg'], phase=leg['phase'], mac=mac_of(leg['clone']),
                     rc=rc_file.read_text().strip() if rc_file.exists() else 'running', groups={})
        for g, old in leg['old'].items():
            new_log = leg['new'] / f'{g}.log'
            if not new_log.exists():
                entry['groups'][g] = dict(missing=True)
                continue
            entry['groups'][g] = dict(same_but_owner=same_but_owner(old / f'{g}.log', new_log), **graded(new_log),
                                      new=result(leg['new'], g), earlier=result(old, g))
        out.append(entry)
        print(leg['leg'], entry['rc'], {g: (v.get('same_but_owner', {}).get('differ'),
                                            [a['outcome'] for a in v.get('leave_alls', [])]) for g, v in
                                        entry['groups'].items()}, flush=True)
    Path(sys.argv[3]).write_text(json.dumps(out, indent=1) + '\n')
    Path(sys.argv[2]).write_text(table(out))
    return 0


def table(out: list[dict]) -> str:
    lines = ['| Leg | MAC in the config | rc | Group | log vs the earlier one, owner record out | timer ENTRY owners '
             '(named / unresolved / none) | LeaveAll expiries: ms, owner, outcome, LeaveAll ms after the owner\'s first '
             'opportunity | MRPDU rows, ms (leaveall / periodic / join, if0) | rows as the earlier log graded |',
             '|---|---|---|---|---|---|---|---|---|']
    for e in out:
        for g, v in e['groups'].items():
            if v.get('missing'):
                lines.append(f"| {e['leg']} | {e['mac']} | {e['rc']} | {g} | (no log) | | | | |")
                continue
            sb = v['same_but_owner']
            same = 'identical' if sb['differ'] == 0 else f"{sb['differ']} lines differ, first {sb['first_differing_line']}"
            same += f" ({sb['lines']:,} lines; {sb['participant']} PARTICIPANT)"
            own = f"{sb['owner_named']} / {sb['owner_unresolved']} / {sb['owner_missing']}"
            alls = '; '.join(f"{a['at_ms']:,.1f} {a['owner']} {a['outcome']}"
                             + (f" +{a['after_opportunity_ms']:.2f}" if a['after_opportunity_ms'] is not None else '')
                             for a in v['leave_alls']) or '(none)'
            def rows(r):
                return ' / '.join(f"{r.get('rows', {}).get(k + '.if0', '-')}" for k in ('leaveall', 'periodic', 'join'))
            same_rows = 'same' if v['new'].get('rows') == v['earlier'].get('rows') else rows(v['earlier'])
            lines.append(f"| {e['leg']} | {e['mac']} | {e['rc']} | {g} | {same} | {own} | {alls} | {rows(v['new'])} | "
                         f"{same_rows} |")
    return '\n'.join(lines) + '\n'


if __name__ == '__main__':
    sys.exit(main())
