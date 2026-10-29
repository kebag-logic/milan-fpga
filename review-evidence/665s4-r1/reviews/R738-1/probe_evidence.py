#!/usr/bin/env python3
"""Check published target traces, timing boundaries, and standalone report provenance.

Usage: python3 probe_evidence.py CHECKOUT PUBLIC_PACKET
PUBLIC_PACKET contains author/receipts from the cited immutable evidence commit.
"""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

root, public = map(lambda p: Path(p).resolve(), sys.argv[1:3])
packet = Path(__file__).resolve().parent
sys.path.insert(0, str(root / 'tb/verilator/nvm_split_target'))
import target_grade as tg
import target_cases as tc
import target_selftest as st

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    sys.modules[name] = obj
    spec.loader.exec_module(obj)
    return obj

run = module('review_target_run', root / 'tb/verilator/nvm_split_target/run.py')
evidence = public / 'author/receipts/target-8x8'
cpu_hz, sys_hz = 50_000_000, 100_000_000
print(f'Target traces: CPU {cpu_hz} Hz, bus {sys_hz} Hz; published inputs, no simulation rerun.')
observed = {name: tg.observe((evidence / (name + '.log')).read_text(), sys_hz, cpu_hz)
            for name in ['valid', 'absent', 'torn', 'version', 'guard',
                         'reorder-bindings', 'reorder-settle', 'slow-step', 'guard-removed']}
for name in ['valid', 'absent', 'torn', 'version', 'guard']:
    obs = observed[name]
    assert not tg.completed(obs), (name, tg.completed(obs))
    assert not tg.over_t_svc(obs, cpu_hz)
    restoring = name in ('valid', 'torn')
    assert not tg.held_to(obs, tc.SAVED_NAME if restoring else None, tc.scenario.TALKER_A if restoring else 0)
    print(name, 'PASS wire answers and per-step timing', len(tg.service(obs)), 'steps')
assert not tg.guarded(observed['guard'])
assert 'flash write escaped the journal' in observed['guard-removed'].text
print('PASS independent device rejection of guard removal')
# Eight AAF listeners plus the CRF sink; eight maps in each direction.
expected = ['acmp_restore_binding'] * 9 + ['aecp_map_restore'] * 16 + ['aecp_restore_settle'] + ['aecp_value_restore'] * 107
for name in ['valid', 'torn']:
    seen, findings = tg.apply_order(observed[name], expected)
    assert not findings, findings
    print(name, 'PASS 9 bindings, 16 maps, settle, 107 names; 133 owner entries')
for name in ['reorder-bindings', 'reorder-settle']:
    findings = tg.apply_order(observed[name], expected)[1]
    assert findings
    print(name, findings)
for name in ['absent', 'version']:
    assert not tg.apply_order(observed[name], [])[1]
slow = tg.over_t_svc(observed['slow-step'], cpu_hz)
assert len(slow) == 1 and '30.2139' in slow[0]
print('PASS real slow step rejected:', slow[0])

# Probe the actual report generator, with published measured results.
results = json.loads((evidence / 'results.json').read_text())
text = run.table(results, '8x8')
(packet / 'generated-timing-table.md').write_text(text)
assert not any(token in text for token in ['50 MHz', '50000000', '50,000,000', 'cpu_hz'])
assert all('cpu_hz' not in row and 'sys_hz' not in row for row in results)
print('REPRODUCED: generated table and results carry timing figures but no CPU/bus clock fields.')
print('Report generator accepts only results and point; the clock is not passed to it.')

# Exercise the unchanged current-writer gate with precisely its bound removed,
# replacing only the loaded grader; no checkout source is edited.
sys.path.insert(0, str(root / 'scripts'))
with tempfile.TemporaryDirectory(dir=packet / 'scratch') as tmp:
    with patch.object(st, 'shipping_source', st._shipping_check_removed):
        mutant = st.shipping_grader(Path(tmp))
    # check_nvm_capture imports a module named run; explicitly bind that import.
    with patch.dict(sys.modules, {'run': mutant}):
        gate = module('review_capture_gate', root / 'scripts/check_nvm_capture.py')
    with patch.object(sys, 'argv', ['check_nvm_capture.py']):
        status = gate.main()
    assert status == 1, status
    print('PASS current-writer gate with removed D5 bound exits', status)
