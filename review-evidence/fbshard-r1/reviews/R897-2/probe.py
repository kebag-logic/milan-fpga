#!/usr/bin/env python3
"""Focused, offline watcher probes. Usage: probe.py CHECKOUT PACKET."""
import copy
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from contextlib import redirect_stdout
from unittest.mock import patch

root, packet = map(lambda s: Path(s).resolve(), sys.argv[1:])
os.environ['TMPDIR'] = str(packet / 'scratch')
tempfile.tempdir = str(packet / 'scratch')
sys.dont_write_bytecode = True
sys.path.insert(0, str(root / 'scripts'))
import yaml
import ci_fail_fast as consumer
import ci_fail_fast_selftest as control
import ci_runtime_workflows as runtime
from ci_gate_workflows import generate, load_template
from ci_workflow_plan import skipped_matrices

old = 'b7b351935f65416c8632c21dd13e08fb2e9c1d9c'
head = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
print('head:', head)
results = {}
for name in ('docs', 'elaborate', 'rtl', 'rtl-fast'):
    path = '.github/workflows/' + name + '.yml'
    workflow = yaml.safe_load((root / path).read_text())
    step = next(s for s in workflow['jobs']['ci-fail-fast']['steps'] if s.get('id') == 'ci_observe')
    env = step['env']
    for key in ('EXPECTED_JOBS', 'SKIPPED_MATRICES'):
        assert '${{' not in env[key], (name, key)
    expected = set(json.loads(env['EXPECTED_JOBS']))
    skipped = json.loads(env['SKIPPED_MATRICES'])
    assert skipped == skipped_matrices(workflow)
    assert not (expected & set(skipped))
    control.watcher_runtime_control(workflow)
    print(name, 'committed runtime control PASS; raw matrices:', sorted(skipped))
    previous = yaml.safe_load(subprocess.check_output(['git', '-C', str(root), 'show', old + ':' + path]))
    if skipped:
        try:
            control.watcher_runtime_control(previous)
        except AssertionError as exc:
            assert 'watcher stopped observing: observer_error after 1 read(s), rc=0' == str(exc)
            print(name, 'previous committed workflow CAUGHT:', exc)
        else:
            raise AssertionError('previous committed workflow escaped')
    else:
        control.watcher_runtime_control(previous)
    for jobid, job in workflow['jobs'].items():
        if not job.get('strategy', {}).get('matrix'):
            assert not re.search(r'\$\{\{\s*matrix\.', json.dumps(job)), (name, jobid)
    # Independently drive the consumer, retaining each read and failure output.
    covered = {label for rows in skipped.values() for label in rows}
    waiting = sorted(expected - covered)
    raw = [{'name': key, 'status': 'completed', 'conclusion': 'skipped', 'steps': []} for key in skipped]
    first = raw + [{'name': label, 'status': 'completed', 'conclusion': 'success'} for label in waiting]
    first[len(raw)].update(status='in_progress', conclusion=None)
    for conclusion in ('failure', 'cancelled', 'timed_out', 'action_required'):
        second = copy.deepcopy(first)
        second[len(raw)].update(status='completed', conclusion=conclusion)
        api = control.ReadsAPI([first, second])
        with tempfile.TemporaryDirectory(dir=packet / 'scratch') as tmp:
            output = Path(tmp) / 'output'
            with patch.dict(os.environ, {'GITHUB_OUTPUT': str(output)}), patch.object(consumer.time, 'sleep') as sleep, redirect_stdout(io.StringIO()) as stdout:
                rc = consumer.watch(api, 1, expected, skipped)
            assert (rc, api.calls, sleep.call_count) == (1, 2, 1)
            assert not output.exists()
            assert json.loads(stdout.getvalue()) == {'first_failure': waiting[0], 'conclusion': conclusion}
        print(name, conclusion, 'detected on read 2; no observer error')
    for raw_name, legs in skipped.items():
        mixed = raw + [{'name': legs[0], 'status': 'completed', 'conclusion': 'success'}]
        try:
            consumer.observe(mixed, expected, skipped)
        except ValueError as exc:
            assert str(exc) == 'expanded and unexpanded matrix jobs overlap'
        else:
            raise AssertionError('mixed identities accepted')
    results[name] = {'raw_names': sorted(skipped), 'expanded_names': sorted(expected), 'runtime_control': 'PASS', 'old_form': 'CAUGHT' if skipped else 'no matrix', 'failure_conclusions': 4}

control.cancellation_control()
print('all same-head sibling cancellation requests PASS (offline fixture)')
source = load_template(root, 'rtl-fast')
source['jobs']['firmware-boundary-shards'].pop('name')
generate('rtl-fast', copy.deepcopy(source))
source['jobs']['collision-probe'] = {'name': 'firmware-boundary-shards', 'runs-on': 'ubuntu-24.04', 'steps': [{'run': 'true'}]}
try:
    generate('rtl-fast', source)
except ValueError as exc:
    assert 'unexpanded matrix name equals an expanded job name' in str(exc)
    print('generator collision plant REFUSED:', exc)
else:
    raise AssertionError('generator collision escaped')
try:
    consumer.observe([], {'same'}, {'same': ['same 0']})
except ValueError as exc:
    assert str(exc) == 'an unexpanded matrix name equals an expanded job name'
    print('consumer collision plant REFUSED:', exc)
else:
    raise AssertionError('consumer collision escaped')
for value in ({'x ${{ matrix.shard }}': ['a', 'b']}, ['literal \\u0024{{', '${{ matrix.total }}', 'quotes " and $ and \\']):
    encoded = runtime.literal_json(value)
    assert '${{' not in encoded and json.loads(encoded) == value
print('literal JSON round-trip including backslashes and quotes PASS')
results['head'] = head
(packet / 'probe.json').write_text(json.dumps(results, indent=2) + '\n')
print('focused probe PASS')
