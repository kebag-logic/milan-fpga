#!/usr/bin/env python3
"""Disposable probes, nothing written to the tree: the self-test re-executed from altered source text in memory, and
sharper mutants of two named rules."""
import dataclasses, sys, types
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch
root = Path(sys.argv[1]).resolve()
path = root / 'tb/verilator/ctrl_service_hooks/hooks_selftest.py'
sys.path.insert(0, str(path.parent))
SRC = path.read_text()

def load(src, name):
    m = types.ModuleType(name); m.__file__ = str(path); sys.modules[name] = m
    exec(compile(src, str(path), 'exec'), m.__dict__)
    return m

def tally(s):
    base = s.run_checks()
    bad = [k for k, v in base.items() if v]
    escaped = []
    for name, make, named in s.MUTANTS:
        with ExitStack() as st:
            st.enter_context(make())
            if s.run_checks()[named] is None: escaped.append(name)
    return f'{len(base)-len(bad)} of {len(base)} checks; {len(s.MUTANTS)-len(escaped)} of {len(s.MUTANTS)} mutants caught; escaped {escaped}'

def drop(src, text):
    assert src.count(text) == 1, text
    return src.replace(text, 'pass\n' if False else '')

ARM = """        expect(armed < mark, f'interface {i}: the window opens before the arm ({armed} > {mark})')\n"""
GRADES = """    expect((srp['bound_ms'], srp['within'], whole['bound_ms'], whole['within']) == (18.0, False, 20.0, False),
           'the amended bounds graded a path')\n"""
LATE = """    expect(sorted(late) == ['counters.all.if0', 'counters.all.t5.i1.if0', 'srp.x.if0'], f'findings {late}')\n"""
print('A. head, unaltered:', tally(load(SRC, 'st_head')))
print('B. the arm rule (armed < mark) deleted from its check:', tally(load(drop(SRC, ARM), 'st_noarm')))
print('C. both grades-nothing assertions deleted from check_amended:', tally(load(drop(drop(SRC, GRADES), LATE), 'st_nogrades')))

s = load(SRC, 'st_probe')
import hooks, run, scenario
AGING = hooks.aging_group
def arm_late(p):
    g = AGING(p)
    for i in range(p.interfaces):
        m = f'mark hooks-disc-aging.tmr_no_adp.if{i}'
        g.steps.remove(m)
        g.steps.insert(g.steps.index(f'mark hooks-disc-aging.available.if{i}') + 1, m)
    return g
HR, SUM, GA, SL = s.HOOK_ROW, s.SUMMARY, run.grade_all, s.SLACK
def verdict_only(r, group):
    out = HR(r, group)
    return dict(out, within=not out['unbounded'] and out['ms'] <= hooks.amended_ms(out, 2))
def findings_only(*a):
    g = GA(*a)
    keep = {r['probe'] for r in g['rows'] if r['ms'] > hooks.amended_ms(r, 2)}
    return dict(g, findings=[x for x in g['findings'] if not x.startswith('LATE ') or x.split(':')[1].strip() in keep])
def counts_only(g):
    out = SUM(g)
    for h, v in out.items():
        v['misses'] = sum(r['ms'] > hooks.amended_ms(r, 2) for r in g['rows'] if r['hook'] == h)
    return out
def slack_amended(r, hz):
    return SL(dict(r, bound_ms=hooks.amended_ms(r, 2)), hz)
for label, target, attr, value, named in (
        ('D1 real aging group, each TMR_NO_ADP mark moved before its arm', hooks, 'aging_group', arm_late, 'the aging window opens after the arm'),
        ('D2 a verdict reads the amended bound, bound_ms left as it is', run, 'hook_row', verdict_only, 'the amended column grades nothing'),
        ('D3 a LATE finding reads the amended bound', run, 'grade_all', findings_only, 'the amended column grades nothing'),
        ('D4 a hook\'s over-its-bound count reads the amended bound', run, 'summary', counts_only, 'the amended column grades nothing'),
        ('D5 NARROW slack reads the amended bound', run, 'slack_cycles', slack_amended, 'the amended column grades nothing')):
    with patch.object(target, attr, value):
        got = s.run_checks()
    failed = {k: v for k, v in got.items() if v}
    print(f'{label}: named check -> {str(got[named])[:110]}; failing checks: {sorted(failed)}')
