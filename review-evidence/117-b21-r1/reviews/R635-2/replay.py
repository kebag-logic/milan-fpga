#!/usr/bin/env python3
"""Replay published issue #117 evidence; inputs are read-only.

Usage: replay.py PUBLIC_PACKET_ROOT RAW_ARCHIVE OUTPUT_DIRECTORY
Disposable files remain under OUTPUT_DIRECTORY/scratch.
"""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

packet, archive, out = map(lambda x: Path(x).resolve(), sys.argv[1:4])
work = out / 'scratch' / 'replay'
work.mkdir(parents=True, exist_ok=True)
receipts = out / 'receipts'
receipts.mkdir(exist_ok=True)
author = packet / 'author-r2'
new = author / 'tools/pr2'

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(8 << 20), b''):
            h.update(b)
    return h.hexdigest()

manifest = json.loads((packet / 'MANIFEST.json').read_text())
checked = [x for x in manifest if x['file'].startswith('author-r2/')]
bad = [x['file'] for x in checked if digest(packet / x['file']) != x['published_sha256']]
(receipts / 'packet-integrity.json').write_text(json.dumps(dict(files=len(checked), mismatches=bad), indent=2)+'\n')
assert not bad

wanted = {
    'restart-peer': ('rA', '.pcap', 'f8c177c3c1b4957d2df56d68d5eeb918a8ee02ec4ff1c1c69549bcfab05183cd'),
    'direction-b-dut': ('dB', '.pcap', '6cd1c9b4929025078ad29e2a7c659351fe09c9b3c6f8dfc792ba3a782b878e1f'),
    'direction-a-dut': ('dA', '.pcap', '59a86f99427ce8ef62530e4da87fa16eaf17ea51a37f3552493f56311b31212f'),
    'direction-a-peer': ('dA', '.pcap', 'a848c00b319904d337da99cf19a3ff2ca3d8dc6b52d7d568562cdb1929c34b85'),
}
cache = {}
inputs = {}
for role, (directory, suffix, expected) in wanted.items():
    for path in sorted((archive / directory).glob('*'+suffix)):
        if path not in cache:
            cache[path] = digest(path)
        if cache[path] == expected:
            inputs[role] = path
            break
    assert role in inputs, role
fixed = {
    'capture': ('dB/dB.pcm', 'da175f5d24f9191b3101d756babf6901ed2f1bb3590da2b4d5d0d656fddcfc54'),
    'restart-output': ('rA-ext/cap-lr.raw', 'e855f403a95031c26308a27705e2e1348697f40d3f84046460119f9379bf3427'),
    'restart-times': ('rA-ext/cap-ts.bin', '728ffb1e1c97dfbd39e9f3eda7958e3806ec934dfc4162dc659a3a20bef991c4'),
    'selftest-times': ('mst-long/mst-long.ts', 'ab78ee6b3b3f719a977df6dc049b54223a74fb3f593f35a3548568ab20600ecf'),
    'selftest-sampler': ('mst-long/mst-long.samp', '17a8a5a8792592dc96ca1fa6702d44d0724af9bbdbd34267ea192b0d2d8fabee'),
    'probe': ('probe/peer.samples', '8f592556c1b93fb7d2395cd138c5880a6345c1654ca11d77240eb6cca77dc6b6'),
}
for role, (name, expected) in fixed.items():
    path = archive / name
    cache[path] = digest(path)
    assert cache[path] == expected, role
    inputs[role] = path
(receipts / 'input-integrity.json').write_text(json.dumps({k: dict(bytes=v.stat().st_size, sha256=cache[v]) for k,v in inputs.items()}, indent=2)+'\n')
print('Public packet and ten raw inputs verified', flush=True)

results = {}
def run(tag, tool, args, env=None):
    cmd = [sys.executable, '-I', '-B', str(tool), *map(str,args)]
    e = os.environ.copy()
    e.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
    if env:
        e.update(env)
    p = subprocess.run(cmd, cwd=work, env=e, capture_output=True, text=True, timeout=900)
    text = p.stdout+p.stderr
    # Public receipts use roles, never physical interface labels or host paths.
    for role, path in inputs.items():
        text = text.replace(str(path), role).replace(path.name, role)
    for path, role in [(out, '$OUTPUT'), (packet, '$PACKET'), (archive, '$ARCHIVE')]:
        text = text.replace(str(path), role)
    (receipts / (tag+'.txt')).write_text(text)
    (receipts / (tag+'.rc')).write_text(str(p.returncode)+'\n')
    results[tag] = p.returncode
    print(tag, 'rc', p.returncode, flush=True)
    assert p.returncode == 0, tag

def restart():
    run('restart-controls', new/'b21_restart_controls.py', [new/'b21_restart_bound.py', author/'r3/runs/rA/cycles.jsonl', inputs['restart-peer'], inputs['restart-output'], inputs['restart-times'], work/'plants', receipts/'restart-controls.json'])
    for name in ['bound-as-measured.json','bound-plant-24000.json','bound-plant-43344.json','bound-plant-48000.json']:
        (receipts/name).write_bytes((work/'plants'/name).read_bytes())

def small():
    run('grader-controls', new/'b21_probes.py', [inputs['probe'], author/'tools/b21_grade.py', new/'b21_grade.py', work/'probes', receipts/'grader-controls.json'])
    rec = author/'r3/selftest/mst-long/mst-long-reads.u16'
    run('floor-groups', new/'b21_floor_groups.py', [rec, inputs['selftest-times'], inputs['selftest-sampler'], work/'floors.txt'], {'B5_W':'110'})
    run('step1', new/'b21_step1_verdict.py', [rec, rec.with_suffix('.json'), receipts/'step1.json'])

def direction_b():
    run('extract-direction-b', new/'b21_aaf.py', ['extract', inputs['direction-b-dut'], '3cc0c60102030000', 2, work/'dut-link'])
    samples = work/'dut-link.samples'
    d = digest(samples)
    assert d == '1976539998f6c7590c2bfe7a5efcbb8cb8f733a1e77f88f20e614082cafe2468'
    (receipts/'derived-integrity.json').write_text(json.dumps(dict(bytes=samples.stat().st_size, sha256=d),indent=2)+'\n')
    run('direction-b-grade', new/'b21_grade.py', ['mcasp', archive/'dB', 'dB', samples, 4, receipts/'direction-b'])
    run('direction-b-exact', new/'b21_exact.py', [inputs['capture'], samples, 4, receipts/'direction-b-exact.json'])

def transit():
    target = work/'transit.json'
    run('transit-crf', new/'b21_transit_crf.py', [inputs['direction-a-dut'], inputs['direction-a-peer'], target])
    obj = json.loads(target.read_text())
    obj['inputs'] = ['dut-link', 'peer-link']
    (receipts/'transit-crf.json').write_text(json.dumps(obj,indent=2)+'\n')

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    futures = [pool.submit(f) for f in [restart, small, direction_b, transit]]
    errors = []
    for future in futures:
        try:
            future.result()
        except Exception as e:
            errors.append(str(e))
(receipts/'replay-status.json').write_text(json.dumps(dict(returncodes=results,errors=errors),indent=2)+'\n')
assert not errors, errors
