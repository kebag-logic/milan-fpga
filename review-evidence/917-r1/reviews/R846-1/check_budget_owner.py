#!/usr/bin/env python3
"""Exercise the exact source-head RX attribution helper on held-record histories.

Only the named function and its scalar bound are loaded; no campaign runs.
Usage: python3 check_budget_owner.py CHECKOUT
"""
import ast
from pathlib import Path
import sys
p=Path(sys.argv[1])/'tb/verilator/ctrl_service_budget/grade.py'
tree=ast.parse(p.read_text())
body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='owner']
body += [n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='COMMIT_LATENCY_MAX' for t in n.targets)]
class Refusal(Exception): pass
env={'Refusal':Refusal}
exec(compile(ast.Module(body=body,type_ignores=[]),str(p),'exec'),env)
owner=env['owner']
assert owner([(0,'immediate',60,100)],106,[]) == (0,'immediate',60)
print('Positive control: a token-backed frame at cycle 100 is attributed correctly at 106.')
try:
    owner([(0,'held',60,100)],500100,[])
except Refusal as e:
    print('Held frame at cycle 100, release 5 ms later at 100 MHz:',str(e))
else: raise AssertionError('The delayed held record unexpectedly accepted')
refused=[]
result=owner([(0,'held',60,100),(0,'refused-follower',60,500090)],500100,refused)
print('Held frame plus refused follower near refill: returned',result,'refused',refused)
assert result==(0,'refused-follower',60) and refused==[(100,0,'held',60)]
print('Confirmed: delayed publication is either refused or assigned to the wrong frame.')
