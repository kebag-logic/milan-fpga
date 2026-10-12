#!/usr/bin/env python3
"""Exercise retained reset checks and restore the old unpublished-zero guard.

No checkout file is changed. Production text is changed only in memory at the
existing source-reader seam; helper tests execute the changed function body.
Usage: python3 check_standing_controls.py ROOT
"""
import importlib.util
import io
from pathlib import Path
import re
import sys
import unittest
from unittest.mock import patch

root = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location('counter_steps', root / 'tests/steps/counters_contract_steps.py')
steps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(steps)
original = steps._crf_rx_source()
key = 'if (w_bind_rise_w) begin'
offset = original.index(key)
regs = list(steps.CRF_COUNTER_REG.values()) + ['iv_uf_r', 'iv_sm_r', 'iv_mr_r', 'iv_tu_r', 'iv_lt_r', 'iv_et_r']
for reg in regs:
    tail, n = re.subn(r'\b' + re.escape(reg) + r"\s*<=\s*(?:'0|1'b0)\s*;", '', original[offset:], count=1)
    assert n == 1, reg
    with patch.object(steps, '_crf_rx_source', return_value=original[:offset]+tail):
        try:
            steps.step_cc_crf_era_wipe(None)
        except AssertionError as exc:
            assert reg in str(exc), (reg, exc)
            print('DETECTED retained reset:', reg)
        else:
            raise AssertionError('missed retained reset: ' + reg)
        steps.step_cc_crf_era_edge(None)
        steps.step_cc_crf_era_lock(None)
        print('OMISSION other era checks PASS:', reg)
steps.step_cc_crf_era_wipe(None)

tc = steps.tc
source = (root / 'tb/tools/torture_campaign.py').read_text()
start = source.index('def check_tv_tnv(')
end = source.index('\ndef frames_rate_reading(', start)
function = source[start:end]
assert function.count('if total > frx:') == 1
scope = dict(tc.__dict__)
exec(compile(function.replace('if total > frx:', 'if frx and total > frx:'), '<old-snapshot-guard>', 'exec'), scope)
classes = [value for name, value in vars(tc).items() if isinstance(value, type)
           and name.startswith('_') and name.endswith('Checks')]
Test = type('StandingChecks', (*classes, unittest.TestCase), {})
loader = unittest.TestLoader()
with patch.object(tc, 'check_tv_tnv', scope['check_tv_tnv']):
    output = io.StringIO()
    result = unittest.TextTestRunner(stream=output).run(loader.loadTestsFromTestCase(Test))
    print(output.getvalue())
    assert len(result.failures) == 1 and not result.errors, (result.failures, result.errors)
    assert result.failures[0][0]._testMethodName == 'test_unpublished_zero_receive_snapshot'
    cases = loader.loadTestsFromTestCase(Test)
    omitted = unittest.TestSuite(test for test in cases if test._testMethodName != 'test_unpublished_zero_receive_snapshot')
    result = unittest.TextTestRunner(stream=sys.stdout).run(omitted)
    assert result.wasSuccessful()
print('Standing controls PASS: retained resets and old snapshot guard detected; omission controls pass')
