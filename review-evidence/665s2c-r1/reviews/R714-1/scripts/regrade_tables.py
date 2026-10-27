#!/usr/bin/env python3
"""Rebuild every archived S2c arm's table.md and composed maximum with the reviewed head's run.py.

usage: regrade_tables.py HEAD_CHECKOUT RUNS_DIR AUTHOR_REGRADE_DIR S2_FINAL_DIR OUT_DIR

RUNS_DIR holds one directory per arm with the per-group graded JSON the run
wrote (<group>.json) and the run's table.md. The group order is the order
the archived table's probe section lists them (run.py writes results in
group order). For each arm this writes OUT_DIR/<arm>/table.md and
OUT_DIR/<arm>/summary.json (counts, windows, composed maximum, fan-out
cells) and prints one comparison line against the author's head regrade and,
for the cacheless arms, against S2's final A1/A8 tables.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

head, runs, author, s2, out = (Path(a).resolve() for a in sys.argv[1:6])
sys.path.insert(0, str(head / 'tb/verilator/ctrl_service_budget'))
import run  # noqa: E402  the head's own aggregation

POINT = {'1': '1x1', '8': '8x8'}
NON_GROUP = {'table.md', 'results.json'}


def ordered(arm: Path) -> list[dict]:
    groups = {}
    for f in sorted(arm.glob('*.json')):
        if f.name in NON_GROUP:
            continue
        g = json.loads(f.read_text())
        groups[g['group']] = g
    # The probe section lists every group's probes contiguously, in group order: match each
    # group's whole probe sequence at the next row (a probe name may recur across groups).
    rows = [m.group(1) for line in (arm / 'table.md').read_text().splitlines()
            if (m := re.match(r'\| [^|]+ \| `([^`]+)` \| (?:[\d,]+|-) \|', line))]
    order, at = [], 0
    while at < len(rows):
        fit = [n for n, g in groups.items() if n not in order
               and [r['probe'] for r in g['probes']] == rows[at:at + len(g['probes'])]]
        if len(fit) != 1:
            raise SystemExit(f'{arm.name}: row {at} ({rows[at]}) matches {fit}')
        order.append(fit[0])
        at += len(groups[fit[0]]['probes'])
    order += [n for n, g in groups.items() if not g['probes'] and n not in order]
    missing = set(groups) - set(order)
    if missing:
        raise SystemExit(f'{arm.name}: groups without a probe row {sorted(missing)}')
    return [groups[n] for n in order]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


out.mkdir(parents=True, exist_ok=True)
for arm in sorted(p for p in runs.iterdir() if p.is_dir()):
    point = POINT[arm.name[1]]
    results = ordered(arm)
    text = run.table(results, point)
    dest = out / arm.name
    dest.mkdir(exist_ok=True)
    (dest / 'table.md').write_text(text)
    top = run.composed_maximum(results)
    fanout = [dict(group=g['group'], probe=r['probe'], cpu_cycles=r['cpu_cycles'], ms=r['ms'],
                   within=r['within_t_svc'], ceiling=r['within_ceiling'], **{k: r[k] for k in r if 'recipient' in k})
              for g in results for r in g['probes']
              if r['status'] == 'measured' and 'fanout' in r['probe']]
    (dest / 'summary.json').write_text(json.dumps(dict(counts=run.counts(results), windows=run.windows(results),
                                                       composed_maximum=top, fanout=fanout), indent=1) + '\n')
    ref = author / arm.name / 'table.md'
    verdict = ('author-head-regrade ' + ('IDENTICAL' if ref.is_file() and ref.read_bytes() == text.encode()
                                         else 'DIFFERS' if ref.is_file() else 'absent'))
    if arm.name in ('P1-none', 'P8-none'):
        s2t = s2 / ('A1' if arm.name == 'P1-none' else 'A8') / 'table.md'
        verdict += ' s2-final ' + ('IDENTICAL' if s2t.read_bytes() == text.encode() else 'DIFFERS')
    c = run.counts(results)
    cm = (f"composed {'>=' if top['lower_bound'] else ''}{top['cycles']} ({top['ms']:.3f} ms) {top['group']} "
          f"windows {top['windows']}/{top['rows']} partial={top['partial']} "
          f"released={top['released']['cycles'] if top['released'] else None} "
          f"({top['released']['ms'] if top['released'] else None} ms) {top['released']['group'] if top['released'] else ''}"
          if top else 'composed none')
    print(f"{arm.name}: {len(results)} groups, {c['path_misses']} of {c['paths']} paths, "
          f"{c['instance_misses']} of {c['instances']} instances; {cm}; {verdict}; sha {sha(dest / 'table.md')[:16]}")
