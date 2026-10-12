#!/usr/bin/env python3
"""Catch a broadened freshness value and remove its sole schema test."""
import argparse
import io
import json
from pathlib import Path
import sys
import types
import unittest

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--root', type=Path, required=True)
parser.add_argument('--work', type=Path, required=True)
args = parser.parse_args()
root, work = args.root.resolve(), args.work.resolve()
work.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(root / 'scripts'))
import entity_selftest as checks
import entity_yaml as original
checks.WORK = work
name = 'test_dafresh_configuration'
path = root / 'scripts/entity_yaml.py'
old = "integer(acmp['da_fresh_ms'], 15000, 15000, 'acmp.da_fresh_ms')"
new = "integer(acmp['da_fresh_ms'], 15000, 15001, 'acmp.da_fresh_ms')"
text = path.read_text()
assert text.count(old) == 1
planted = types.ModuleType('planted_entity')
planted.__file__ = str(path)
exec(compile(text.replace(old, new), str(path), 'exec'), planted.__dict__)
planted.Invalid = original.Invalid

def run(module, remove, label):
    checks.entity = module
    tests = unittest.defaultTestLoader.getTestCaseNames(checks.EntityTests)
    if remove:
        tests.remove(name)
    suite = unittest.TestSuite(checks.EntityTests(test) for test in tests)
    log = io.StringIO()
    result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
    (work / (label + '.log')).write_text(log.getvalue())
    row = dict(tests=result.testsRun, failures=[case.id() for case, _ in result.failures],
               errors=[case.id() for case, _ in result.errors], skipped=result.skipped)
    return row

baseline = run(original, False, 'baseline')
caught = run(planted, False, 'planted')
escaped = run(planted, True, 'removed')
assert not baseline['failures'] and not baseline['errors'] and not baseline['skipped']
assert caught['failures'] == ['entity_selftest.EntityTests.' + name] and not caught['errors'] and not caught['skipped']
assert escaped['tests'] == baseline['tests'] - 1
assert not escaped['failures'] and not escaped['errors'] and not escaped['skipped']
(work / 'results.json').write_text(json.dumps(dict(name='dafresh-schema-range', old=old, new=new,
    baseline=baseline, caught=caught, escaped=escaped), indent=2) + '\n')
print('Freshness schema mutation caught; all remaining schema tests pass after removal')
