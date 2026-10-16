#!/usr/bin/env python3
"""Mutation probes of the packet's gm_summary.py grader, run on a disposable
copy of the packet. Usage: probe_gm_summary.py <copy-of-author-dir>"""
import copy, json, subprocess, sys
from pathlib import Path
root = Path(sys.argv[1]); tool = root / 'tools' / 'gm_summary.py'
runs = ['gm01', 'gm02', 'gm03', 'gm04', 'gm05']
orig = {r: json.loads((root / 'bench' / r / 'analysis.json').read_text()) for r in runs}
def grade(label, mutate=None):
    for r in runs:
        a = copy.deepcopy(orig[r])
        if mutate and r == 'gm03': mutate(a)
        (root / 'bench' / r / 'analysis.json').write_text(json.dumps(a))
    subprocess.run([sys.executable, '-I', str(tool)] + runs, capture_output=True, check=True)
    s = json.loads((root / 'summary' / 'gm-steps.json').read_text())
    res = [(e['run'], e['edge'], e['pass'], [k for k, v in e['grade'].items() if not v]) for e in s['edges']]
    fails = [x for x in res if not x[2]]
    print('%-58s PASS %d/10 failing %s' % (label, 10 - len(fails), fails))
    return s
base = grade('baseline (published analyses)')
pub = json.loads((Path(sys.argv[1]).parent / 'published-gm-steps.json').read_text()) if (Path(sys.argv[1]).parent / 'published-gm-steps.json').exists() else None
def asc0(a):  # one console sample with asCapable 0 at 10 s
    a['health'] = sorted(a['health'] + [[10.0, 'sync1 asc0 tu0'], [10.25, 'sync1 asc1 tu0']])
def extra_tu(a):  # a second console tu episode inside the takeover window
    a['health'] = sorted(a['health'] + [[12.0, 'sync1 asc1 tu1'], [12.5, 'sync1 asc1 tu0']])
def extra_gm(a):  # GPTP_GM_CHANGED +2 in the takeover window
    t = a['counter_transitions']['dut:counter-9-0']; v = dict(t[1][1]); v['5'] += 1
    t.insert(2, [20.0, v]); [x[1].__setitem__('5', x[1]['5'] + 1) for x in t[3:]]
def mr(a):  # an mr toggle on the DUT's CRF output
    a['wire']['dut']['mr'] = a['wire']['dut']['mr'] + [[10.0, 1]]
def unlock(a):  # MEDIA_UNLOCKED +1 on the peer CRF listener
    t = a['counter_transitions']['peer:counter-5-8']; v = dict(t[-1][1]); v['1'] += 1; t.append([20.0, v])
def ctrl_asc0(a):  # a controller poll reporting asCapable 0: nowhere to put it
    a['controller_dut_avb'] = [[10.0, 'SUCCESS', 'x', 0]]
for lbl, m in [('console sample asCapable 0', asc0), ('second console tu episode', extra_tu),
               ('GPTP_GM_CHANGED +2', extra_gm), ('DUT CRF mr toggle', mr), ('peer CRF MEDIA_UNLOCKED +1', unlock),
               ('controller poll asCapable 0 (field the grader never reads)', ctrl_asc0)]:
    grade('mutant: ' + lbl, m)
grade('restored')
for r in runs:
    (root / 'bench' / r / 'analysis.json').write_text(json.dumps(orig[r], indent=1) + '\n')
