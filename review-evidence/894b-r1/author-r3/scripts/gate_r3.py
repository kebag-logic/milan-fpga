"""Round 3's 8x8/1if gate (round 2 phase B's gate_b.py, its groups and criteria; #894's round 3 ruling issuecomment-6878014227) from CPU budget harness legs on the built image (#894's round 2 ruling issuecomment-6871343905,
with #902's bounds, issuecomment-6867990126): every group's grade (<leg>/results/<group>.json) and each leg's own log.
Read only. Prints:
- by row family, the worst measured instance the CPU decides (the held-egress rows apart) against the ruling's bound:
  AECP 20, ACMP/ADP/MAAP 30, SRP 90, MRPDU 49 ms; AECP's notices (the retried notice and the largest notice's fan-out)
  20 ms;
- the queued notices (path notice.queued, the answering-every-port arm), per group: the first (the least, from the
  port's answer) against 20 ms and the last (the most) against 130 ms;
- the largest legal command's measured rows (aecp-largest-notice, the answering-ports arm: each 550 B response and its
  notices, the paced R4L row as measured) against 238 ms;
- the held-egress rows (backlog-owed's seven, set by the scenario's 60 ms egress hold), each against section 13's
  ledger figure at 8x8/1if and 1x1/1if's at 8a3791e4: recorded misses, never ruled passing;
- every budget miss, recorded (one of the seven) or new; a new one fails the gate;
- the join intervals against the harness's commit-side gate, 181.0 to 239.0 ms;
- each kind's longest tier-2 slice against the stated slice (over it fails: a stated cost under its measurement) and
  the ruling's 1,600 us (over it is a STOP), each kind's heaviest pass given whole against its stated figure; the
  passes over THE SHARE; and the legs' STATED, REFUSED, BUDGET, SHARE and END lines.
- THE RETRY's rounds (passes.rounds of every group): how many, the stated costs each was held to, the heaviest by
  notices built, and every round over its stated cost (round 3: none may be, in any arm).
Exits 1 when a CPU-decided row is over its bound, a budget miss is new, a join interval is outside the gate, a slice is
over the stated slice, a round or any other cost is over its statement (a STATED line), or a leg did not end rc 0.
usage: python3 -I gate_b.py DIR[:LOG] ...   (a leg dir holding results/; LOG its leg's log)"""
import json
import re
import sys
from pathlib import Path

#: The ruling's bound for each family's rows, in ms (the round 2 ruling, item (a); #902's round 8 for MRPDU).
RULED = {'aecp': (20, 'AECP'), 'notify': (20, "AECP's notices (retried, the largest notice's fan-out)"),
         'acmp': (30, 'ACMP'), 'adp': (30, 'ADP'), 'disc': (30, "ADP (a bound talker's ENTITY_AVAILABLE)"),
         'maap': (30, 'MAAP'), 'srp': (90, 'SRP'), 'mrpdu': (49, 'MRPDU (a timer-owed MRPDU)')}
FIRST_MS, LAST_MS, R4L_MS = 20, 130, 238
JOIN_GATE = (181.0, 239.0)
#: The ruling's slice cap, 1,600 us, in CPU cycles at 100 MHz (a slice over it is a STOP trigger).
SLICE_MOST_CYCLES = 160_000
QUEUED = 'notice.queued'
LARGEST = 'aecp-largest-notice'
#: The held-egress rows (group backlog-owed): section 13's ledger at 8x8/1if (round 1, 93afe385) and 1x1/1if's at
#: 8a3791e4 (round 7's H-L1O), in ms.
EGRESS = {'backlog.owed.if0': (63.24, 62.94), 'backlog.owed_behind0.if0': (63.47, 63.11),
          'backlog.owed_behind1.if0': (63.69, 63.29), 'backlog.owed_behind2.if0': (63.91, 63.46),
          'backlog.owed_behind3.if0': (64.20, 63.64), 'backlog-owed.service.acmp.last.if0': (62.18, 62.08),
          'backlog-owed.service.aecp.last.if0': (61.83, 61.82)}


def family(p: dict) -> str:
    """A probe's row family: a timer-owed MRPDU's (mrpdu_grade.rows, family srp) is its own."""
    return 'mrpdu' if '.mrpdu.' in p['probe'] else p.get('family', '?')


def egress(p: dict) -> bool:
    """One of the seven rows the egress decides."""
    return p['group'] == 'backlog-owed' and p['probe'] in EGRESS


legs = [a.split(':', 1) if ':' in a else (a, None) for a in sys.argv[1:]]
probes, joins, groups, slices, whole, share, lines, limits = [], [], 0, {}, {}, [], [], {}
rounds = dict(count=0, stated=set(), heaviest={}, over=[])
for leg, log in legs:
    leg = Path(leg)
    for f in sorted(((leg / 'results') if (leg / 'results').is_dir() else leg).glob('*.json')):
        if f.name == 'results.json':
            continue
        g = json.loads(f.read_text())
        if 'probes' not in g:
            continue
        groups += 1
        probes += [dict(p, group=g['group']) for p in g['probes']]
        p = g['passes']
        r = p.get('rounds') or {}
        rounds['count'] += r.get('rounds', 0)
        if r.get('stated'):
            rounds['stated'].add(tuple(sorted(r['stated'].items())))
        for n, c in (r.get('heaviest') or {}).items():
            rounds['heaviest'][n] = max(rounds['heaviest'].get(n, (0, '')), (c, g['group']))
        rounds['over'] += [dict(o, group=g['group']) for o in r.get('over', [])]
        j = p.get('joins') or {}
        if j.get('count'):
            joins.append((j['shortest'], j['longest'], j['count'], g['group']))
        for kind, cycles in (p.get('slices') or {}).get('longest', {}).items():
            slices[kind] = max(slices.get(kind, (0, '')), (cycles, g['group']))
        limits['slice'] = (p.get('slices') or {}).get('limit', limits.get('slice'))
        for kind, cycles in (p.get('stated') or {}).get('heaviest', {}).items():
            whole[kind] = max(whole.get(kind, (0, '')), (cycles, g['group']))
        limits.update({f'pass {k}': v for k, v in (p.get('stated') or {}).get('limits', {}).items()})
        s = p.get('share') or {}
        if s.get('over'):
            share.append((g['group'], s['over'], max((o['cycles'] for o in s.get('over_passes', [])), default=0)))
    if log:
        lines += [l.rstrip() for l in Path(log).read_text().splitlines()
                  if l.startswith(('STATED', 'REFUSED', 'BUDGET', 'SHARE', 'END', 'CONTROL', 'HEAD'))
                  or ' groups graded, ' in l]
measured = [p for p in probes if p.get('status') == 'measured']
fail = []
print(f'# {groups} groups graded over {len(legs)} leg(s); {len(probes)} probe instances, {len(measured)} measured')
print('\n## The rows the CPU decides (the seven held-egress rows apart; the queued notices and the largest legal '
      'command below)\n')
print('| Family | Row | Instances | Worst, ms | Worst instance (group) | Its budget, ms | Ruling, ms | Over the ruling |')
print('|---|---|---:|---:|---|---:|---:|---:|')
by: dict[str, list] = {}
for p in measured:
    if not egress(p) and p['path'][0] != QUEUED and p['group'] != LARGEST:
        by.setdefault(family(p), []).append(p)
for fam in sorted(by):
    ps = by[fam]
    worst = max(ps, key=lambda p: p['ms'])
    bound, name = RULED.get(fam, (None, 'not a ruled row'))
    over = [p for p in ps if bound is not None and p['ms'] > bound]
    fail += [f"{p['probe']} ({p['group']}): {p['ms']:.3f} ms over the ruling's {bound} ms" for p in over]
    print(f"| {fam} | {name} | {len(ps)} | {worst['ms']:.3f} | `{worst['probe']}` ({worst['group']}) | "
          f"{worst.get('budget_ms')} | {bound if bound is not None else ''} | {len(over)} |")
queued: dict[str, list] = {}
for p in measured:
    if p['path'][0] == QUEUED:
        queued.setdefault(p['group'], []).append(p)
print(f'\n## The queued notices (the answering-every-port arm), from the port\'s answer: the first against {FIRST_MS} '
      f'ms, the last against {LAST_MS} ms\n')
if queued:
    print('| Group | Notices | First, ms | Last, ms | Last instance | Its budget, ms |')
    print('|---|---:|---:|---:|---|---:|')
    for g, ps in sorted(queued.items()):
        first, last = min(ps, key=lambda p: p['ms']), max(ps, key=lambda p: p['ms'])
        print(f"| {g} | {len(ps)} | {first['ms']:.3f} | {last['ms']:.3f} | `{last['probe']}` | {last.get('budget_ms')} |")
        if first['ms'] > FIRST_MS:
            fail.append(f"{g}: the first queued notice {first['ms']:.3f} ms over {FIRST_MS} ms")
        if last['ms'] > LAST_MS:
            fail.append(f"{g}: the last queued notice {last['ms']:.3f} ms over {LAST_MS} ms")
    allq = [p for ps in queued.values() for p in ps]
    print(f"\nOver every group: the first at most {max(min(p['ms'] for p in ps) for ps in queued.values()):.3f} ms, "
          f"the last at most {max(p['ms'] for p in allq):.3f} ms; {len(allq)} queued notices in {len(queued)} groups")
else:
    print('none measured')
largest = [p for p in measured if p['group'] == LARGEST]
print(f'\n## The largest legal command\'s measured rows ({LARGEST}, the answering-ports arm), against paced R4L\'s '
      f'{R4L_MS} ms\n')
if largest:
    print('| Instance | Family | ms | Its budget, ms |')
    print('|---|---|---:|---:|')
    for p in sorted(largest, key=lambda p: -p['ms']):
        print(f"| `{p['probe']}` | {family(p)} | {p['ms']:.3f} | {p.get('budget_ms')} |")
    top = max(largest, key=lambda p: p['ms'])
    print(f"\nThe most: {top['ms']:.3f} ms (`{top['probe']}`), against {R4L_MS} ms")
    fail += [f"{p['probe']} ({LARGEST}): {p['ms']:.3f} ms over {R4L_MS} ms" for p in largest if p['ms'] > R4L_MS]
else:
    print('none measured')
print('\n## The held-egress rows (backlog-owed, the scenario\'s 60 ms egress hold): recorded misses\n')
print('| Row | Measured, ms | Ledger at 8x8/1if, ms | Difference, ms | 1x1/1if at 8a3791e4, ms | Within its budget |')
print('|---|---:|---:|---:|---:|---|')
for name, (ledger, one) in EGRESS.items():
    ps = [p for p in measured if p['group'] == 'backlog-owed' and p['probe'] == name]
    if not ps:
        print(f'| `{name}` | not measured | {ledger} | | {one} | |')
        fail.append(f'{name}: the held-egress row was not measured')
        continue
    p = max(ps, key=lambda p: p['ms'])
    print(f"| `{name}` | {p['ms']:.3f} | {ledger} | {p['ms'] - ledger:+.3f} | {one} | {p.get('within_budget')} |")
unmeasured = [p for p in probes if p.get('status') != 'measured']
print(f'\nInstances not measured: {len(unmeasured)}' + ''.join(f"\n- {p['probe']} ({p['group']}): {p.get('status')}"
                                                       for p in unmeasured[:20]))
missed = [p for p in measured if not p.get('within_budget', True)]
new = [p for p in missed if not egress(p)]
print(f'Instances over their budget: {len(missed)}, of which {len(missed) - len(new)} are the recorded held-egress '
      f'rows and {len(new)} new' + ''.join(f"\n- NEW {p['probe']} ({p['group']}): {p['ms']:.3f} ms, budget "
                                           f"{p.get('budget_ms')} ms" for p in new))
fail += [f"{p['probe']} ({p['group']}): a new budget miss, {p['ms']:.3f} ms" for p in new]
if joins:
    lo, hi = min(s for s, _, _, _ in joins), max(l for _, l, _, _ in joins)
    print(f'\nJoin intervals: {sum(c for _, _, c, _ in joins)} in {len(joins)} groups, the shortest {lo:.3f} ms '
          f'({min(joins)[3]}), the longest {hi:.3f} ms ({max(joins, key=lambda j: j[1])[3]}), against the commit-side '
          f'gate {JOIN_GATE[0]} to {JOIN_GATE[1]}')
    if lo < JOIN_GATE[0] or hi > JOIN_GATE[1]:
        fail.append(f'a join interval outside {JOIN_GATE}: {lo:.3f} to {hi:.3f} ms')
print('\nThe longest tier-2 slice of each kind, against the stated slice ' + f'{limits.get("slice") or 0:,} CPU cycles:')
for kind, (cycles, g) in sorted(slices.items()):
    over = limits.get('slice') and cycles > limits['slice']
    print(f'- {kind}: {cycles:,} ({g})' + (', OVER the stated slice' if over else '') +
          (f', over the ruling\'s {SLICE_MOST_CYCLES:,} (STOP)' if cycles > SLICE_MOST_CYCLES else ''))
    if over:
        fail.append(f'a {kind} slice of {cycles:,} CPU cycles ({g}), over the stated slice {limits["slice"]:,}')
    if cycles > SLICE_MOST_CYCLES:
        fail.append(f'STOP: a {kind} slice of {cycles:,} CPU cycles ({g}), over 1,600 us')
print('The heaviest pass given whole of each kind, whose round found nothing to do, against its stated figure:')
for kind, (cycles, g) in sorted(whole.items()):
    print(f'- {kind}: {cycles:,} ({g}), stated {limits.get("pass " + kind, 0):,}')
print(f'\nGroups with work passes over THE SHARE: {len(share)}' +
      ''.join(f'\n- {g}: {n} pass(es), the longest {c:,} CPU cycles' for g, n, c in share))
stated: dict[str, list] = {}
for line in lines:
    if line.startswith('STATED '):
        group, what = line[7:].split(': ', 1)
        kind = re.sub(r'\d[\d,]*(?= CPU cycles)', 'C', what)
        kind = re.sub(r'(round of )\d+ (notice\(s\) and )\d+', r'\1n \2k', kind)
        cost = int(re.search(r'([\d,]+) CPU cycles', what)[1].replace(',', '')) if 'CPU cycles' in what else 0
        s = stated.setdefault(kind, [0, 0, ''])
        s[0] += 1
        if cost >= s[1]:
            s[1], s[2] = cost, f'{group}: {what}'
print(f'\nTHE RETRY\'s rounds: {rounds["count"]:,}, held to ' +
      '; '.join(', '.join(f'{k} {v} us' for k, v in st) for st in sorted(rounds['stated'])) +
      '; the heaviest by notices built: ' +
      ', '.join(f'{n}: {c:,} ({g})' for n, (c, g) in sorted(rounds['heaviest'].items(), key=lambda kv: int(kv[0]))) +
      f'; over their stated cost: {len(rounds["over"])}')
fail += [f"{o['group']}: a round of {o['notices']} notice(s) and {o['refused']} refused attempt(s), {o['cycles']:,} "
         f"CPU cycles, over its stated {o['limit']:,}" for o in rounds['over'][:20]]
print(f'\nThe legs\' STATED lines, by kind: {sum(s[0] for s in stated.values())}')
for kind, (n, _, worst) in sorted(stated.items()):
    print(f'- {n} x "{kind}"; the dearest: {worst}')
fail += [f'{n} STATED line(s) "{kind}"' for kind, (n, _, _) in sorted(stated.items())]
ends = [l for l in lines if l.startswith('END ')]
fail += [f'a leg ended {l}' for l in ends if not l.startswith('END rc=0')]
if len(ends) != len([log for _, log in legs if log]):
    fail.append(f'{len(ends)} END lines for {len([log for _, log in legs if log])} leg logs')
print('\nThe legs\' own lines (STATED lines above):')
for line in lines:
    if not line.startswith('STATED '):
        print(line)
print('\nRESULT: ' + ('FAIL\n' + '\n'.join(f'- {f}' for f in fail) if fail else
                      'PASS: every row the CPU decides within its bound, no new budget miss, the joins within the gate'))
sys.exit(1 if fail else 0)
