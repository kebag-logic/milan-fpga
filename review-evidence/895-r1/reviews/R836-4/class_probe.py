#!/usr/bin/env python3
"""Falsify the published cost survey's paced-class lookup without source edits."""
import ast
from pathlib import Path
import sys
src,ev=map(Path,sys.argv[1:])
sys.path.insert(0,str(src/'tb/verilator/ctrl_service_budget'))
import record_classes as rc
p=ev/'author-r8/scripts/costs_vs_stated.py'
tree=ast.parse(p.read_text())
node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='sources')
ns={}
exec(compile(ast.Module(body=[node],type_ignores=[]),str(p),'exec'),ns)
legs,arm,stated=rc.synthetic()
# The staged accepted configuration takes 400 us, so its rule cost is 420 > 300.
legs[1].groups['aecp-fanout'][1].cycles=40_000
most={}
for leg in legs:
    for group in leg.groups:
        for kind,r,cost,bound,why in rc.classes(leg,group,stated):
            if rc.held(leg,group,kind):
                key='classes.'+kind
                most[key]=max(most.get(key,0),r.cycles)
keys=ns['sources']('edit_rows.EDIT_RECORD_US','record.aecp.edit')
found=[most[k] for k in keys if k in most]
print('Collected measured classes:',most)
print('Published survey lookup:',keys,'found:',found)
print('Published survey result for EDIT_RECORD_US: not staged, measured 0; contributes no UNDER')
assert most['classes.paced']==40_000 and not found
correct=rc.findings(legs,arm,lambda _:stated)[0]
print('Actual head class grader findings:',correct)
assert any('420 us' in f and 'paced' in f for f in correct)
# The survey also omits the command argument for held(), losing SET_STREAM_INFO.
ordinary=legs[1].groups['aecp-fanout'][2]
print('SET_STREAM_INFO held by head:',rc.held(legs[1],'aecp-fanout','other',ordinary.command))
print('SET_STREAM_INFO held by survey call:',rc.held(legs[1],'aecp-fanout','other'))
assert rc.held(legs[1],'aecp-fanout','other',ordinary.command)
assert not rc.held(legs[1],'aecp-fanout','other')
legs[1].groups['aecp-fanout'][1].cycles=28_000
ordinary.cycles=40_000
correct=rc.findings(legs,arm,lambda _:stated)[0]
print('Over-cost SET_STREAM_INFO:',correct)
assert any('420 us' in f and 'other' in f and '0x000e' in f for f in correct)
print('PROBE PASS: two coverage holes reproduced; this is synthetic, not a claim of an actual over-cost record.')
