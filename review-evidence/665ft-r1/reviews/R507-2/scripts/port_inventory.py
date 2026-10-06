#!/usr/bin/env python3
"""Check migration labels/names without executing the retired harness.

This is an inventory check, not a proof that predicates are equivalent.
"""
import ast
from pathlib import Path
import re
import subprocess
import sys

root=Path(sys.argv[1]).resolve()
base='423ac5d910d09ab189b3acc39ae3ae1d10d50b19'
def old(path):
    return subprocess.check_output(['git','-C',str(root),'show',f'{base}:{path}'],text=True)
def literals(text):
    token = r'"(?:\\.|[^"\\])*"|//[^\n]*|/\*.*?\*/'
    code = re.sub(token, lambda m: m.group(0) if m.group(0).startswith('"') else '', text, flags=re.S)
    return [ast.literal_eval(x) for x in re.findall(r'"(?:\\.|[^"\\])*"',code)]
def squashed(text):
    return ' '.join(' '.join(literals(text)).split())
for before,after in [
    ('sw/firmware/ctrl/test/test_port_loop.c','sw/firmware/ctrl/test/test_port_loop.cpp'),
    ('sw/firmware/ctrl/test/test_adp.c','sw/firmware/ctrl/test/test_adp.cpp'),
    ('sw/firmware/ctrl/test/lwsrp_port.c','sw/firmware/ctrl/test/lwsrp_port.cpp'),
]:
    labels=[ast.literal_eval(s) for s in re.findall(r'\b(?:check(?:_eq)?|bound)\(\s*("(?:\\.|[^"\\])*")',old(before))]
    now=squashed((root/after).read_text())
    missing=[l for l in labels if ' '.join(l.split()) not in now]
    print(f'{before} -> {after}: {len(labels)} literal check labels, missing={missing}')
    assert not missing
names=[]
for file in ('nvm_checks.py','nvm_checks_write.py'):
    text=old('sw/firmware/ctrl_nvm/test/'+file)
    names+=re.findall(r'^def check_(\w+)\(',text,re.M)
now='\n'.join(f.read_text() for f in (root/'sw/firmware/ctrl_nvm/test').glob('test_nvm_*.cpp'))
testnames=set(re.findall(r'TEST(?:_P|_F)?\([^,]+,\s*(\w+)\)',now))
missing=sorted(set(names)-testnames)
print(f'NVM: {len(names)} old check functions; missing tests={missing}')
assert not missing
print('migration name/label inventory PASS; predicate review and executable controls remain separate evidence')
