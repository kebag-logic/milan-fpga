"""Check fresh target records, collect raw receipts and probe a real refused regrade."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

packet = Path(__file__).resolve().parent
build = packet / 'scratch/target-1x1'
results = build / 'results'
rec = json.loads((results/'results.json').read_text())
assert (rec['cpu_hz'], rec['sys_hz']) == (50_000_000, 100_000_000)
assert all(r['passed'] for r in rec['results'])
published = json.loads((packet/'scratch/public/author-r3/receipts/target-1x1/results.json').read_text())
assert rec == published, 'Fresh record differs from published 1x1 record'
print('PASS: fresh 1x1 record equals author published record, including every case, cycle count and verdict')
specs = {}
for path in sorted(build.glob('*/build.json')):
    raw = path.read_bytes()
    spec = json.loads(raw)
    assert (spec['cpu_hz'], spec['sys_hz']) == (rec['cpu_hz'], rec['sys_hz'])
    specs[path.parent.name] = {k: spec[k] for k in ('cpu_hz','sys_hz','shape','variant','mutation','executable_sha256')}
    specs[path.parent.name]['raw_build_json_sha256'] = hashlib.sha256(raw).hexdigest()
(packet/'build-clock-receipt.json').write_text(json.dumps(specs, indent=2)+'\n')
print(f'PASS: all {len(specs)} build.json records agree with result clocks')
out = packet/'target-1x1'
out.mkdir(exist_ok=True)
for source in results.iterdir():
    if source.is_file():
        shutil.copyfile(source, out/source.name)
print('PASS: raw result, table, case scripts, simulation logs and journals retained')

# Reuse the real freshly built models. Delete one build clock, restore bytes
# afterwards, and inspect the supported --regrade output without running a model.
path = build/'capture-all/build.json'
original = path.read_bytes()
table = (results/'table.md').read_bytes()
try:
    broken = json.loads(original)
    del broken['cpu_hz']
    path.write_text(json.dumps(broken))
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(packet/'scratch/tmp'))
    command = [sys.executable, '-B', 'tb/verilator/nvm_split_target/run.py', '--point', '1x1',
               '--jobs', '16', '--build-dir', str(build), '--regrade']
    probe = subprocess.run(command, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print('Real regrade missing-clock rc:', probe.returncode)
    print(probe.stdout.strip())
    assert probe.returncode == 2 and 'clocks' in probe.stdout
    assert (results/'table.md').read_bytes() == table
    print('OBSERVED: real missing-clock refusal retains the previous successful table byte-for-byte')
finally:
    path.write_bytes(original)
assert path.read_bytes() == original
print('PASS: disposable build record restored byte-for-byte')
