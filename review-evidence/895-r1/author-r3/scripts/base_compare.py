#!/usr/bin/env python3
"""base_compare.py HARNESS GROUP INTERFACES LABEL=RESULTS_DIR...: for each leg's results directory, the heaviest
polls' base over its groups' graded JSON (polls.heaviest.base), and in GROUP's log the pass whose polls' base is the
heaviest, by HARNESS's own poll_grade (spans, sections, instances), with that pass's cycles by module (its PASS line's
mods=). Read-only; prints one block per leg."""
import json
import re
import sys
from pathlib import Path

harness, group, n_if = Path(sys.argv[1]), sys.argv[2], int(sys.argv[3])
sys.path.insert(0, str(harness))
import grade  # noqa: E402
import poll_grade  # noqa: E402

for spec in sys.argv[4:]:
    label, d = spec.split('=', 1)
    d = Path(d)
    heavy = []
    for j in sorted(d.glob('*.json')):
        try:
            doc = json.loads(j.read_text())
        except ValueError:
            continue
        polls = (doc.get('passes') or {}).get('polls') or doc.get('polls')
        if isinstance(polls, dict) and 'heaviest' in polls:
            heavy.append((polls['heaviest'].get('base', 0), j.stem))
    heavy.sort(reverse=True)
    print(f"== {label}: heaviest polls' base by group (cycles): {heavy[:4]}")
    text = (d / f'{group}.log').read_text(errors='replace')
    log = grade.parse(text, 100_000_000, 100_000_000)
    traced, commits = poll_grade.spans(log), poll_grade.committed(log)
    best = None
    for start, end, start_sys in poll_grade.sections(traced):
        items = poll_grade.instances(log, traced, commits, start, end)
        base = end - start - sum(c for _, c in items)
        if best is None or base > best[0]:
            best = (base, start_sys, end - start, items)
    base, start_sys, span, items = best
    print(f"   {group}: heaviest base {base} cycles (polls span {span}, items {items}) at sys {start_sys}")
    passes = [l for l in text.splitlines() if l.startswith('PASS ')]
    pick = None
    for l in passes:
        f = l.split()
        if int(f[2]) <= start_sys:
            pick = l
        else:
            break
    if pick:
        mods = re.search(r'mods=(\S+)', pick).group(1)
        print('   its pass: ' + ' '.join(pick.split()[:5]) + ' ' + mods)
