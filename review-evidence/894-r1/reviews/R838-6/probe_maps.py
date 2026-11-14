#!/usr/bin/env python3
"""Run the map oracle and the twelve new plants against disposable source."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path.cwd()
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'sw/firmware/ctrl/test'))
import aecp_arms
import aecp_mutants
import fw_gtest
from ctrl_build import Tree, CTRL, STACK

work = OUT/'scratch/map-probe'
src = work/'ctrl'
shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
tree = Tree(src, work/'build', work/'reuse', fw_gtest.Build(jobs=16), STACK)
config = ROOT/'configs/endstation_ax7101_1x1_tdm8.yaml'
test = 'TEST_F(Core, MapEditsAreTheirDefinitionRowForRow)'
old = subprocess.check_output(['git','show','7398ec0a:sw/firmware/ctrl/test/test_aecp.cpp']).decode()
now = (ROOT/'sw/firmware/ctrl/test/test_aecp.cpp').read_text()
def oracle(s):
    return s[s.index(test):s.index('\nTEST_F(', s.index(test)+len(test))]
assert oracle(old) == oracle(now)
print('Definition test unchanged:', hashlib.sha256(oracle(now).encode()).hexdigest(), flush=True)
baseline = aecp_arms.core_arm(tree, config, mode='work', selected='Core.*Map*:Core.Every*')
(OUT/'receipts/maps-baseline.log').write_text(baseline.log)
assert baseline.rc == 0
print('Map baseline PASS', flush=True)
delta = subprocess.check_output(['git','diff','7398ec0a..HEAD','--','sw/firmware/ctrl/test/aecp_map_mutants.py']).decode()
names = re.findall(r"^\+    \('([^']+)'", delta, re.M)
assert len(names) == 12
results = []
for d in aecp_mutants.DEFECTS:
    if d.name not in names:
        continue
    target = src/d.path
    original = target.read_text()
    assert original.count(d.old) == 1, d.name
    target.write_text(original.replace(d.old, d.new))
    try:
        result = aecp_arms.core_arm(tree, config, mode='work', selected=':'.join(t for t,_ in d.checks))
        caught = all(aecp_mutants.caught(t,w,result) for t,w in d.checks)
        (OUT/'receipts'/('plant-'+d.name+'.log')).write_text(result.log)
        results.append({'name':d.name, 'caught':caught, 'checks':d.checks})
        print(d.name, 'CAUGHT' if caught else 'ESCAPED', flush=True)
    finally:
        target.write_text(original)
(OUT/'receipts/map-plants.json').write_text(json.dumps(results,indent=2)+'\n')
assert len(results)==12 and all(r['caught'] for r in results)
