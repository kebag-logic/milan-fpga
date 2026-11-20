#!/usr/bin/env python3
"""Focused composition probes. Run from the reviewed checkout; output stays beside this script."""
import sys
from pathlib import Path

ROOT = Path.cwd()
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'sw/firmware/ctrl/test'))
import ctrl_build as b
import srp_arms as s
import srp_mutants as m
import plat_arms as p

mode = sys.argv[1]
work = OUT / 'scratch' / mode
work.mkdir(parents=True, exist_ok=True)
tree = b.Tree(b.CTRL, work / 'build', work / 'reuse', b.fw_gtest.Build(jobs=4))
lw = ROOT / 'third_party/lwSRP'
if mode == 'listeners':
    outcomes = s.listener_arms(tree, lw)
elif mode == 'sinks':
    outcomes = p.sink_arms(tree)
elif mode.startswith('mutants'):
    m.DEFECTS = tuple(d for d in m.DEFECTS if d.name.startswith('srp-cut-') or d.name in (
        'same-skips-the-last-byte', 'feedback-latest-filter-failed-first'))
    point = mode.removeprefix('mutants-')
    interfaces = 2 if point == '2if' else 1
    entity = s.ENTITY_8X8.stem if point == '81' else ''
    raise SystemExit(m.campaign(work, lw, jobs=4, interfaces=interfaces, entity=entity))
else:
    raise SystemExit('unknown probe')
for result in outcomes:
    print(result.arm, 'rc', result.rc)
    print(result.log)
raise SystemExit(any(x.rc for x in outcomes))
