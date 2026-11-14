#!/usr/bin/env python3
"""buildone.py HARNESS UPTO_SYS LABEL=LOG...: each build-one pass (whole_grade's kind) that starts before UPTO_SYS, its
start and CPU cycles, from each (possibly partial) log; and the heaviest. Read-only."""
import sys
sys.path.insert(0, sys.argv[1])
import grade, whole_grade
upto = int(sys.argv[2])
for spec in sys.argv[3:]:
    label, path = spec.split('=', 1)
    text = open(path, errors='replace').read()
    log = grade.parse(text, 100_000_000, 100_000_000)
    builds = sorted(c for c, n in log.entries if n == whole_grade.mrpdu_grade.BUILD)
    frames = sorted(c for c, ch, _ in log.commits if ch == whole_grade.scenario.CH['srp'])
    rows = []
    for p in log.passes:
        if p.start_sys >= upto or not whole_grade.round_idle(p.modules):
            continue
        end = p.start_sys + p.cycles
        if whole_grade.within(builds, p.start_sys, end):
            kind = 'build' if whole_grade.within(frames, p.start_sys, end) > 1 else 'build-one'
            rows.append((kind, p.start_sys, p.cycles, dict(sorted(p.modules.items(), key=lambda x: -x[1])[:5])))
    one = [r for r in rows if r[0] == 'build-one']
    print(f"{label}: {len(one)} build-one passes before {upto}; heaviest {max((r[2] for r in one), default=None)}")
    for r in sorted(one, key=lambda r: -r[2])[:3]:
        print('   ', r)
