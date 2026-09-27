"""Check packet identities and displayed maxima independently of the table generator.

Usage: python3 -B CHECK-EVIDENCE.py /absolute/path/to/candidate
"""
from pathlib import Path
import hashlib
import json
import re
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent / 'receipts'
doc = (root / 'docs/findings/397_SERVICE_BUDGET.md').read_text()
plans = ('all', 'uart-paced', 'queued-input', 'device-wait')
receipts = {(shape, plan): json.loads((packet / f'round2-{shape}-{plan}.json').read_text())
            for shape in ('1x1', '8x8') for plan in plans}
for receipt in receipts.values():
    assert hashlib.sha256(receipt['raw_log'].encode()).hexdigest() == receipt['log_sha256']
    assert receipt['raw_log'].endswith('RESULT: PASS\n')
    for path, digest in receipt['input_hashes'].items():
        assert hashlib.sha256((root / path).read_bytes()).hexdigest() == digest, path
    for row in receipt['rows']:
        count = row['end_sys_cycle'] - row['start_sys_cycle']
        assert count == row['sys_cycles'] and (count + 1) // 2 == row['cpu_cycles']
        assert row['ms'] == count / 100000
        assert abs(row['service_ms'] + row['device_wait_ms'] - row['ms']) < 1e-9
        assert row['no_tick_sys_cycles'] == row['no_tick_end'] - row['no_tick_start']
        assert row['no_tick_ms'] == row['no_tick_sys_cycles'] / 100000
    assert receipt['rows'][-1]['plan'] == receipt['media']['plan']

digests = re.findall(r'^\| `(round[^`]+\.json)` \| `([a-f0-9]{64})` \|$', doc, re.M)
assert len(digests) == 10
for name, digest in digests:
    assert hashlib.sha256((packet / name).read_bytes()).hexdigest() == digest, name

mapping = {
    'Boot to entity enabled': 'boot_to_entity_enabled', 'AEM copy/CRC': 'aem_copy_crc',
    'Binding restore walk': 'restore_walk', 'Journal erase envelope': 'erase_enclosed_to_first_program',
    'Journal START-to-ACK': 'journal_commit_bracket', '`milan_status`': 'milan_status',
    '`milan_gettime`': 'milan_gettime', '`milan_settime`, maximum tested case': 'milan_settime',
    '`milan_utc`, maximum tested case': 'milan_utc', '`milan_nvm` status': 'milan_nvm',
    '`milan_nvm commit`': 'milan_nvm commit', '`milan_nvm wipe`, whole command': 'milan_nvm wipe',
    'Wipe erase envelope, maximum of two': 'wipe_erase_envelope', '`milan_nvm invalid`': 'milan_nvm invalid',
}
shape = None
duties = opportunities = 0
for line in doc.splitlines():
    if line.startswith(('**1x1', '**8x8')):
        shape = line[2:5]
    if not line.startswith('| '):
        continue
    cells = [c.strip() for c in line.strip('|').split('|')]
    if cells[0] not in mapping:
        continue
    key = mapping[cells[0]]
    cases = [(plan, row) for plan in plans for row in receipts[shape, plan]['rows']
             if row['duty'] == key or (key in ('milan_settime', 'milan_utc') and row['duty'].startswith(key))]
    if len(cells) == 6:
        maximum = max(row['sys_cycles'] for _, row in cases)
        matches = [row for plan, row in cases if plan == cells[1].strip('`') and row['sys_cycles'] == maximum]
        assert matches
        row = matches[0]
        assert int(cells[2].replace(',', '')) == (maximum + 1) // 2
        assert abs(float(cells[3]) - maximum / 100000) < 0.000006
        if row['budget_ms'] is None:
            assert cells[4:] == ['N/A', 'N/A']
        else:
            assert int(cells[4].replace(',', '')) == row['budget_ms']
            assert abs(float(cells[5]) - (row['budget_ms'] - maximum / 100000)) < 0.000006
        duties += 1
    else:
        assert len(cells) == 7
        maximum = max(row['no_tick_sys_cycles'] for _, row in cases)
        assert any(plan == cells[2].strip('`') and row['no_tick_sys_cycles'] == maximum for plan, row in cases)
        assert abs(float(cells[1]) - maximum / 100000) < 0.000006
        tx = max(row['uart_tx_allowance_ms'] for _, row in cases)
        assert abs(float(cells[3]) - tx) < 0.000006
        if key == 'boot_to_entity_enabled':
            assert cells[4:] == ['Unarmed prefix', 'N/A', 'N/A']
        else:
            period = 250 + maximum / 100000 + tx
            assert all(abs(float(got) - expected) < 0.000006
                       for got, expected in zip(cells[4:], (period, 500 - period, 2000 - period)))
        opportunities += 1
assert (duties, opportunities) == (28, 28)
print('PASS: 8 bound receipts, 10 file digests, 28 duty rows and 28 opportunity rows')
