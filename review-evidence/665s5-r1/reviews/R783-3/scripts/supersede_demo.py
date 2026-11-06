#!/usr/bin/env python3
"""What the supersede rule does on the two cases the self-test does not reach, at head and with each term dropped.

usage: supersede_demo.py TREE   (nothing in TREE is written)
"""
import sys, types
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
H = tree / 'tb/verilator/ctrl_service_hooks'
sys.path.insert(0, str(H)); sys.dont_write_bytecode = True
RULE = "(x['group'], x['path'], x['interface']) == (by, *r['path'])"
SHAPES = {'head': RULE, 'path term dropped': "(x['group'], x['interface']) == (by, r['path'][1])",
          'group term dropped': "(x['path'], x['interface']) == tuple(r['path'])"}
import hooks  # noqa: E402
def load(text):
    path = H / 'run.py'; src = path.read_text(); assert src.count(RULE) == 1
    m = types.ModuleType('run'); m.__file__ = str(path); sys.modules['run'] = m
    exec(compile(src.replace(RULE, text), str(path), 'exec'), m.__dict__); return m
for label, text in SHAPES.items():
    load(text)
    sys.modules.pop('hooks_selftest', None)
    import hooks_selftest as st
    lost = dict(probe='acmp.tmr_no_adp.if1', path=['acmp.tmr_no_adp', 1], status='no start', reason='late')
    wrong_path = dict(st.row('disc', 2.0, probe='hooks-disc-aging.available.if1'), path=['acmp.entity_available', 1], interface=1, status='measured')
    right_row = dict(st.row('disc', 2.0, probe='hooks-disc-aging.tmr_no_adp.if1'), path=['acmp.tmr_no_adp', 1], interface=1, status='measured')
    a = st.graded_with({'acmp-disc': [lost], 'hooks-disc-aging': [wrong_path]})
    aging_lost = dict(lost, probe='hooks-disc-aging.tmr_no_adp.if1')
    other_row = dict(right_row, probe='acmp.tmr_no_adp.if1')
    b = st.graded_with({'hooks-disc-aging': [aging_lost], 'acmp-disc': [other_row]})
    failing = [k for k, v in st.run_checks().items() if v]
    print(f"{label}: aging group lost TMR_NO_ADP but measured ENTITY_AVAILABLE on the interface -> refusals {len(a['refusals'])} superseded {len(a['superseded'])}; "
          f"aging group lost TMR_NO_ADP, acmp-disc measured that path -> refusals {len(b['refusals'])} superseded {len(b['superseded'])}; checks failing {failing} (the mutant list is read by source_probe.py)")
