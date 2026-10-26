#!/usr/bin/env python3
"""Independent recipe-key, preserved-command and failure-path probes."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(root / 'scripts'))
import yaml
import ci_gate_workflows as generator
import ci_workflow_plan as planner

base = '76de691e5625cc4ea2f9a19def9e07c1183a14ee'
head = 'fddf3671ebc96a953755fa1b9a3ecec5f071a350'
def git(*args):
    return subprocess.check_output(['git', *args], cwd=root, env={**os.environ, 'GIT_NO_REPLACE_OBJECTS':'1'})
assert git('rev-parse','HEAD').decode().strip() == head
template = generator.load_template(root, 'rtl-fast')
current = yaml.safe_load((root / '.github/workflows/rtl-fast.yml').read_text())
old = yaml.safe_load(git('show', base + ':.github/workflows/rtl-fast.yml'))
assert generator.generate('rtl-fast', template) == current

def named(job, label):
    found = [s for s in job['steps'] if s.get('name') == label]
    assert len(found) == 1, label
    return found[0]

def keys(doc):
    tool = named(doc['jobs']['yosys-tool'], 'Cache the pinned Yosys build')['with']
    consumer = named(doc['jobs']['yosys-elaboration'], 'Restore the pinned Yosys build')['with']
    assert set(tool) == {'path','key'}
    assert set(consumer) == {'path','key','fail-on-cache-miss'}
    assert tool['key'] == consumer['key'] and tool['path'] == consumer['path'] == '/opt/yosys'
    assert consumer['fail-on-cache-miss'] is True
    assert 'hashFiles' not in tool['key']
    return tool['key'].replace('${{ env.YOSYS_VERSION }}', doc['env']['YOSYS_VERSION']).replace('${{ runner.os }}', 'Linux')

key = keys(current)
build = named(template['jobs']['yosys-elaboration'], 'Build Yosys from source on cache miss')
digest = hashlib.sha256(json.dumps(build, sort_keys=True, separators=(',',':')).encode()).hexdigest()
assert '-recipe-' + digest + '-ubuntu-24.04-Linux' in key
print('Independent sorted-JSON recipe digest:', digest)

# This fixture plants a prior installation under its complete key. It tests
# generated lookup identity and policy, not a remote cache implementation.
cache = {key: 'ORIGINAL_RECIPE_AND_VERSION'}
for label in ['recipe', 'version', 'image', 'build-step-environment', 'unrelated-check']:
    changed = copy.deepcopy(template)
    consumer = changed['jobs']['yosys-elaboration']
    if label == 'recipe':
        step = named(consumer, 'Build Yosys from source on cache miss')
        step['run'] = step['run'].replace('ENABLE_PLUGINS := 0', 'ENABLE_PLUGINS := 1')
    elif label == 'version':
        changed['env']['YOSYS_VERSION'] = 'v0.67'
    elif label == 'image':
        consumer['runs-on'] = 'ubuntu-22.04'
    elif label == 'build-step-environment':
        named(consumer, 'Build Yosys from source on cache miss')['env'] = {'CXXFLAGS':'-O0'}
    else:
        named(consumer, 'Elaborate the integration-heavy tops')['run'] += '\necho unrelated\n'
    derived = generator.generate('rtl-fast', changed)
    newkey = keys(derived)
    hit = cache.get(newkey)
    assert (hit is not None) == (label == 'unrelated-check')
    print(json.dumps({'plant':label,'key':newkey,'old_cache_hit':hit is not None,
                      'miss_policy':'fail-on-cache-miss=true, no fallback'}))

for job_id, job in old['jobs'].items():
    if job_id not in {'yosys-elaboration','rtl-fast','ci-manifest','ci-fail-fast'}:
        assert job == current['jobs'][job_id], job_id
        print('Other job exactly preserved:', job_id)
before = old['jobs']['yosys-elaboration']
after = current['jobs']['yosys-elaboration']
start = next(i for i,s in enumerate(before['steps']) if s.get('name') == 'Install the pinned Yosys and prove the version')
preserved = []
for step in before['steps'][start:]:
    matched = named(after, step['name'])
    assert {k:v for k,v in matched.items() if k != 'id'} == {k:v for k,v in step.items() if k != 'id'}
    preserved.append(step['name'])
assert not any('/tmp/yosys-src' in s.get('run','') for s in after['steps'])
print('Consumer suffix preserved except generated IDs:', json.dumps(preserved))
assert all(current['jobs'][j].get('timeout-minutes') == job.get('timeout-minutes') for j,job in old['jobs'].items())
assert current['jobs']['yosys-tool']['timeout-minutes'] == 30
print('Existing timeouts unchanged; new job timeout 30')

verdict = named(current['jobs']['rtl-fast'], 'Require every applicable fast gate to pass')
for status, expected in [('success',0),('failure',1),('cancelled',1),('skipped',0),('',1)]:
    env = {**os.environ, **{k:'success' for k in verdict['env']}}
    env.update(YOSYS_TOOL_RESULT=status, YOSYS_ELABORATION_RESULT='skipped' if status != 'success' else 'success')
    run = subprocess.run(['bash','-c',verdict['run']],env=env,capture_output=True,text=True)
    assert bool(run.returncode) == bool(expected), (status,run.stdout,run.stderr)
    print(json.dumps({'tool_result':status,'consumer_result':env['YOSYS_ELABORATION_RESULT'],'verdict_rc':run.returncode,'output':run.stdout.strip()}))

path = '.github/workflows/rtl-fast.yml'
plan, labels = planner.expand_workflow(path,(root/path).read_text())
assert labels[path+':yosys-tool'] == 'Prepare pinned Yosys'
assert path+':yosys-tool' in plan[path+':yosys-elaboration']['needs']
assert path+':yosys-tool' in plan[path+':rtl-fast']['needs']
print('Planner tool entry:',json.dumps(plan[path+':yosys-tool']))
print('Runner unchanged blob:',git('rev-parse',head+':scripts/act_ci.py').decode().strip())
assert git('show',head+':scripts/act_ci.py') == git('show',base+':scripts/act_ci.py')
sentence = 'used a hosted `ubuntu-latest` runner, which resolved to the `ubuntu-24.04` image, and sequential `make -C` invocations.'
assert (root/'docs/testing/TESTING.md').read_text().splitlines()[330] == sentence
print('R705-1-01 exact sentence: PASS')
print('Independent probes: PASS')
