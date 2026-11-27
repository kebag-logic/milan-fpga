"""Audit published hashes, census summaries and the installed-row derivation."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

source, packet, public = map(Path, sys.argv[1:4])
receipts = public / 'author-r7/receipts'
sys.path.insert(0, str(source / 'tb/verilator/ctrl_service_budget'))
import receipt_regrade as rr
import arty_grade

def read(name):
    return json.loads((receipts / name).read_text())

manifest = json.loads((public / 'MANIFEST.json').read_text())
rows = [r for r in manifest if not r['file'].startswith('reviews/')]
missing, wrong = [], []
for row in rows:
    path = public / row['file']
    if not path.is_file():
        missing.append(row['file'])
    elif hashlib.sha256(path.read_bytes()).hexdigest() != row['published_sha256']:
        wrong.append(row['file'])
print('PUBLIC MANIFEST', len(rows), 'missing', len(missing), 'hash mismatch', len(wrong))
assert not missing and not wrong, (missing, wrong)
files = rr.read_parts(receipts, read('FILES.manifest.json')).decode().splitlines()
files = [line.split('\t') for line in files[1:]]
available, absent, bad = [], [], []
for name, size, digest in files:
    path = receipts / name
    if not path.is_file():
        absent.append(name)
        continue
    available.append(name)
    data = path.read_bytes()
    if len(data) != int(size) or rr.sha(data) != digest:
        bad.append(name)
print('FILES.tsv',len(files),'available',len(available),'absent',len(absent),'mismatches',len(bad))
print('FILES mismatches', bad)
(packet/'missing-census.json').write_text(json.dumps(dict(
    count=len(absent), case_manifests=[p for p in absent if p.endswith('/manifest.json')],
    first_absent=absent[:20]), indent=2)+'\n')

for index in ['qualification/manifest.json', 'validation/manifest.json', 'derivation/manifest.json']:
    if (receipts/index).exists():
        counts = 0
        for record in read(index):
            entry = record.get('receipt', record.get('published'))
            if entry:
                rr.read_parts((receipts/index).parent, entry)
                counts += 1
        print('PART MANIFEST', index, counts, 'verified')

census = read('census.json')
cases = {r['case'] for r in census['cases']}
log = (receipts/'validation/receipt-regrade.log').read_text()
reported = re.findall(r'^PASS (.+): complete grade reproduced$', log, re.M)
assert len(reported) == len(cases) == 147 and set(reported) == cases
assert 'RESULT: PASS cases=147 worst_pass_cycles=142775' in log
print('AUTHOR regrade log matches all 147 indexed cases; full local reproduction unavailable without census files')
control = (receipts/'validation/receipt-regrade-control.log').read_text()
assert 'this run graded srp-kept alone' in control and 'cross-case qualification failed' in control
assert not re.search(r'^RESULT: PASS cases=', control, re.M)
print('AUTHOR missing-bound control refuses the disposition and cross-case grade')
summary = read('published-qualification.json')
model, failures = arty_grade.inspect(source)
assert not failures and summary['model'] == model and summary['groups'] == 147
assert summary['worst_pass']['worst_pass_cycles'] == 142775
print('INSTALLED model equals published qualification', json.dumps(model, sort_keys=True))

measured = read('qualification/census.json')
for name, cost in measured['costs'].items():
    assert cost['rule_us'] == -(-cost['cycles']*105//(80*100*5))*5, name
assert set(measured['groups']) == cases
print('CENSUS cost rounding: all',len(measured['costs']),'costs correct; group set identical')
derived = read('qualification/derived-model.json')
script = receipts/'recipes/derive-own.py.txt'
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(packet/'scratch'))
result = subprocess.run(['python3',str(script),str(receipts/'qualification/merged-census.json')],
                        cwd=source, env=env, capture_output=True, text=True, timeout=180)
(packet/'derived-model.json').write_text(result.stdout)
assert result.returncode == 0, result.stderr
assert json.loads(result.stdout) == derived
assert derived == read('derivation/model-installed-r7-step2.json')
assert derived['choices'][0]['rows_ms'] == model['rows_ms']
print('DERIVATION reproduced; fixed point identical to installed step-2 model')
unruled = read('qualification/merged-census.json')
for owed in measured['owed_969']:
    key = owed['key']
    if owed['cycles'] > unruled['costs'][key]['cycles']:
        unruled['costs'][key] = dict(owed, us=owed['cycles']/80)
control_path = packet/'scratch/without-disposition.json'
control_path.write_text(json.dumps(unruled))
result = subprocess.run(['python3',str(script),str(control_path)],cwd=source,env=env,
                        capture_output=True,text=True,timeout=180)
(packet/'without-disposition.json').write_text(result.stdout)
assert result.returncode == 0, result.stderr
negative = json.loads(result.stdout)
assert not negative['choices']
print('CONTROL all owed costs restored:',negative['status'],'zero qualified rows')

identity = (receipts/'validation/identity.log').read_text()
identities = json.loads(identity[:identity.rfind('IDENTICAL')])
assert len(identities) == 8
assert sum(r['stimuli_compared'] for r in identities.values()) == 147
assert all(len(r['executable']) == len(r['elf']) == 64 for r in identities.values())
print('IDENTITY author receipt: 8 executable/ELF pairs; 147 stimuli; flash=None in all eight (non-XIP builds)')
print('No independent byte comparison possible from one-sided identity summary alone')

util = receipts/'timing-r7/AltSpreadLogic_high/digilent_arty_utilization_place.rpt'
for line in util.read_text().splitlines():
    if any(token in line for token in ('Design State', '| Slice LUTs ', '| Slice Registers ', '| Block RAM Tile ')):
        print('RESOURCE', line)
print('RESOURCE indexed utilization reports:', [p[0] for p in files if 'utilization' in p[0]])

commit = subprocess.check_output(['git','cat-file','commit','907764ebbc99dad85babf522da92c13d92ab20aa'],cwd=source)
print('Evidence commit has embedded signature:', b'\ngpgsig ' in commit)
print('PASS available-packet audit; unavailable measurements are explicitly not reproduced')
