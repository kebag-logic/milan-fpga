#!/usr/bin/env python3
"""Check published receipt bytes, inherited inputs, and generated records."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
ref = '999e04e9c417e080d988a0747359c60d2e9edb8a'
prefix = 'review-evidence/70b-r1/'
head = 'b6a1c189fa83de85b470c77a2c7c1e5996138909'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=root)

def published(path):
    return git('show', ref + ':' + prefix + path)

manifest = json.loads(published('MANIFEST.json'))
count = 0
for row in manifest:
    if not row['file'].startswith(('author/receipts/', 'author/scripts/')):
        continue
    assert hashlib.sha256(published(row['file'])).hexdigest() == row['published_sha256'], row['file']
    count += 1
print('PASS published receipt/script manifest:', count, 'files; source', ref)

for ancestor, scopes in [
    ('c71364bd', ['sw/builder', 'sw/firmware', 'hdl', 'configs', 'protocol-processor', 'gptp-processor', 'tb/verilator/nvm_cosim']),
    ('dc7b1417', ['sw/firmware/ctrl', 'sw/firmware/ctrl_nvm', 'sw/firmware/gtest', 'third_party/tsn-c-stack']),
    ('1767346a', ['tb/verilator/milan_dp', 'hdl', 'protocol-processor', 'gptp-processor', 'configs']),
]:
    changed = git('diff', '--name-only', ancestor, head, '--', *scopes).decode()
    assert not changed, changed
    print('PASS inherited input scopes:', ancestor, ', '.join(scopes))
print('All later paths after c71364bd:', git('diff', '--name-only', 'c71364bd', head).decode().strip())

receipt = json.loads((root / 'tb/verilator/nvm_capture_cpu/measurements.json').read_text())
firmware_digest = hashlib.sha256((root / 'sw/firmware/milan_baremetal/milan_baremetal.c').read_bytes()).hexdigest()
assert receipt['product_firmware_sha256'] == firmware_digest
assert git('rev-parse', receipt['base'] + '^{tree}').decode().strip() == '69b8ed0ff4b699434720bd96d8a0bcfabe5dc636'
print('PASS capture firmware digest:', firmware_digest)
for item in receipt['measurements']:
    shape = '1x1' if '1x1' in item['shape'] else '8x8'
    clock = item['cpu_hz'] // 1_000_000
    name = f'author/receipts/capture/measurement-{shape}-{clock}-{item["traffic"]}.json'
    original = json.loads(published(name))
    assert item['rows'] == original['rows'], name
    maximum = max(row['sys_cycles'] for row in item['rows']) / item['sys_hz'] * 1000
    assert abs(maximum - item['maximum_ms']) < 1e-8
    assert len(item['rows']) == 16
    print('PASS capture raw rows:', name, 'maximum_ms', maximum)

oracle = json.loads((root / 'tb/verilator/fw_service_budget/oracle.json').read_text())
sys.path.insert(0, str(root / 'tb/verilator/fw_service_budget'))
import run as service
old_oracle = json.loads(git('show', '1e80128f:tb/verilator/fw_service_budget/oracle.json'))
for old_item, item in zip(old_oracle, oracle, strict=True):
    shape = '1x1' if '1x1' in item['shape'] else '8x8'
    name = f'author/receipts/service/service-{shape}-{item["media"]["plan"]}-1-0-0.json'
    original = json.loads(published(name))
    for key in ('shape', 'raw_log', 'log_sha256', 'rows', 'budget_findings', 'heartbeat', 'liveness'):
        assert item[key] == original[key], (name, key)
    assert hashlib.sha256(item['raw_log'].encode()).hexdigest() == item['log_sha256']
    assert item['budget_findings'] == old_item['budget_findings']
    print('PASS service oracle exact published fields:', name,
          'budget findings unchanged from base:', item['budget_findings'])
    findings = service.service_findings(original, original['raw_log'])
    assert not findings, findings
    print('PASS enforced service rule:', name, findings,
          'heartbeat gap ms', original['heartbeat_max_gap_ms'],
          'maximum PHY bound ms', max(row.get('phy_publication_bound_ms', 0)
                                     for row in original['rows']))
oracle_digest = hashlib.sha256((root / 'tb/verilator/fw_service_budget/oracle.json').read_bytes()).hexdigest()
assert oracle_digest in published('author/receipts/service/oracle-generate.log').decode()
print('PASS oracle regeneration digest:', oracle_digest)
print('PASS evidence audit; execution receipts remain author evidence, not reviewer or manager runs')
