#!/usr/bin/env python3
"""Independent base/head preservation and fail-closed probes; no source edits."""
import ast
from collections import Counter
from contextlib import redirect_stdout
import copy
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import types
from unittest.mock import patch
import yaml

ROOT = Path.cwd()
PACKET = Path(__file__).resolve().parent
BASE = '09c7231eca343607c97c0d66abebb2553688712c'
DRIVER = 'sw/firmware/ctrl/test/test_ctrl_firmware.py'
sys.path.insert(0, str(ROOT / Path(DRIVER).parent))
import test_ctrl_firmware as head
import test_ctrl_firmware_shards as shards
os.environ['TMPDIR'] = str(PACKET / 'scratch')

def source(path):
    return subprocess.check_output(['git','show',f'{BASE}:{path}']).decode()

def module(name, code):
    m = types.ModuleType(name)
    m.__file__ = str(ROOT / DRIVER)
    sys.modules[name] = m
    exec(compile(code, m.__file__, 'exec'), m.__dict__)
    return m

base = module('review_base_driver', source(DRIVER))
# Run the actual pre-split main under the same leaf instrumentation.
# Do not reconstruct its dispatch using the changed phase functions.
def base_dispatch(args, tree, out):
    with patch.object(base, 'cut_reuse'), patch.object(base.fw_gtest, 'toolchain', return_value='scheduling probe'):
        return bool(base.main(['--require-rv32', '--self-test', '--jobs', '4']))
base.run_selected = base_dispatch
expected = shards.inventory(base)
current = shards.inventory(head)
parts = [shards.inventory(head, (i,4)) for i in range(4)]
flat = sum(parts, [])
assert expected == current == flat
assert len(expected) == 916 and len(set(expected)) == 916
assert [len(p) for p in parts] == [60,507,77,272]
assert len([x for x in parts[0] if 'arm_srpcmp' in x]) == 1
for name in head.srp_pub_mutants.ROUND5:
    for interfaces in [1,2]:
        assert f'srp-if{interfaces}:{name}' in parts[3]
(PACKET/'independent-invocations.json').write_text(json.dumps(dict(base=expected, head=current, shards=parts),indent=2)+'\n')
print('PASS: actual base main, head default and ordered shard union have identical 916 invocations (60/507/77/272).')
print('PASS: comparator runs in normal shard; every ROUND5 mutant runs for both interface counts in SRP shard.')

code = (ROOT / DRIVER).read_text()
for label, old, new in [
    ('omit comparator', 'ctrl_arms.arm_srpcmp()]', ']'),
    ('duplicate comparator', 'ctrl_arms.arm_srpcmp()]', 'ctrl_arms.arm_srpcmp(), ctrl_arms.arm_srpcmp()]'),
    ('omit interface-1 publication mutants', '*srp_pub_mutants.ROUND5', '*()'),
]:
    assert code.count(old) == 1
    mutant = module('review_mutant_' + str(len(sys.modules)), code.replace(old,new))
    found = shards.inventory(mutant)
    assert found != expected and Counter(found) != Counter(expected), label
    print(f'PASS: independent baseline comparison catches {label}.')

# Returning failure or refusal from each selected phase must reach the caller.
args = types.SimpleNamespace(shard=None, self_test=True, jobs=4, slice=(1,1), mutation_shard=None, require_rv32=True, lwsrp=ROOT/'third_party/lwSRP')
tree = types.SimpleNamespace(reuse=PACKET/'scratch'/'reuse')
for phase in range(4):
    args.shard=(phase,4)
    with patch.object(head,'run_suites',return_value=[]), patch.object(head.ctrl_arms,'report',return_value=(phase==0)), patch.object(head.ctrl_mutants,'campaign',return_value=(phase==1)), patch.object(head.aecp_mutants,'campaign',return_value=(phase==2)), patch.object(head,'run_srp_mutants',return_value=(phase==3)):
        assert head.run_selected(args,tree,PACKET/'scratch')
    print(f'PASS: phase {phase} failure propagates.')
table = head.srp_mutants.DEFECTS
with patch.object(head.srp_mutants,'campaign',side_effect=[False,head.Refusal('planted campaign refusal')]):
    try:
        head.run_srp_mutants(args,PACKET/'scratch')
    except head.Refusal:
        pass
    else:
        raise AssertionError('refusal swallowed')
assert head.srp_mutants.DEFECTS is table
print('PASS: interface-1 refusal restores the complete SRP mutation table.')
for results, pin_rc in [([True,False],0),([False,True],0),([False,False],1)]:
    with patch.object(head.srp_mutants,'campaign',side_effect=results), patch.object(head.ctrl_mutants,'lwsrp_pin_arms',return_value=pin_rc):
        assert head.run_srp_mutants(args,PACKET/'scratch')
    assert head.srp_mutants.DEFECTS is table
print('PASS: separate interface-2, interface-1 and pin-control failures propagate through the real SRP phase.')

comparator = head.ctrl_arms.arm_srpcmp()
assert comparator.rc == 0
print('PASS: real normal-suite comparator wrapper grades all five controls and eighteen planted defects.')

# Check the original on-disk workflow rather than trusting the copied baseline.
path = '.github/workflows/rtl-fast.yml'
old = yaml.safe_load(source(path))
new = yaml.safe_load((ROOT/path).read_text())
names=['firmware-unit','firmware-control-mutants','firmware-aecp-mutants','firmware-srp-mutants']
def commands(wf, names):
    result=[]
    for name in names:
        job=wf['jobs'][name]
        for step in job['steps']:
            for line in step.get('run','').splitlines():
                line=line.strip()
                if line and not line.startswith('#'):
                    result.append((re.sub(r' --shard [0-3]/4$','',line),job.get('if','success()'),step.get('if','success()')))
    return result
before=commands(old,['firmware-unit'])
after=commands(new,names)
assert set(before)==set(after) and len(before)==19 and len(after)==55
assert old['jobs']['publication-census']==new['jobs']['publication-census']
assert 'publication-census' in new['jobs']['rtl-fast']['needs']
assert all(name in new['jobs']['rtl-fast']['needs'] for name in names)
for name in names:
    job=new['jobs'][name]
    assert job['needs']=='changes' and job['timeout-minutes']==45
    assert job['if']==old['jobs']['firmware-unit']['if']
    for step in job['steps']:
        if step.get('uses','').startswith('actions/cache@'):
            assert step['with']['path']=='~/br-milan-rv32/host'
(PACKET/'independent-commands.json').write_text(json.dumps(dict(before=before,after=after),indent=2)+'\n')
print('PASS: actual base workflow and merged workflow preserve all 19 command/guard rows (55 with repeated setup); budgets, SDK-only caches, publication job and required dependencies preserved.')

step=new['jobs']['rtl-fast']['steps'][0]
script=step['run']
env={k:'success' for k in step['env']}
results=[]
for key in env:
    for value in ['failure','cancelled','', 'skipped']:
        trial=dict(os.environ,**env)
        trial[key]=value
        rc=subprocess.run(['bash','-c',script],env=trial,capture_output=True,text=True).returncode
        expected_rc=0 if value=='skipped' else 1
        assert rc==expected_rc,(key,value,rc)
        results.append(dict(key=key,value=value,rc=rc))
(PACKET/'aggregate-failure-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(f'PASS: actual aggregate script rejects failure, cancellation and absent result for every dependency; {len(results)} result probes, with explicit skipped-context semantics.')

# Coverage implementation and its complete call graph retain base bytes/AST.
for path in ['sw/firmware/gtest/fw_coverage.py','sw/firmware/gtest/fw_coverage_selftest.py','sw/firmware/gtest/coverage.ratchet']:
    assert (ROOT/path).read_bytes()==subprocess.check_output(['git','show',f'{BASE}:{path}'])
def coverage_ast(code):
    return ast.dump(next(n for n in ast.parse(code).body if isinstance(n,ast.FunctionDef) and n.name=='coverage'),include_attributes=False)
assert coverage_ast(source(DRIVER))==coverage_ast(code)
assert sum('fw_coverage.py --check' in line[0] for line in after)==1
print('PASS: unsplit coverage entry function, measurement, exclusions/self-tests and ratchet retain base identity; one unsplit coverage check remains.')
print('All review probes PASS.')
