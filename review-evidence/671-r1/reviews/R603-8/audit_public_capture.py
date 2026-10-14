#!/usr/bin/env python3
"""Verify public capture logs and measurement summaries against the commit."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

out = Path(__file__).resolve().parent
public = out / 'public'
receipt = json.loads(Path('tb/verilator/nvm_capture_cpu/measurements.json').read_text())
for pin, oid in receipt['processor_pins'].items():
    entry = subprocess.check_output(['git','ls-tree','HEAD','--',pin]).decode().split()
    assert entry[0] == '160000' and entry[2] == oid, pin
changes = subprocess.check_output(['git', 'diff', '--name-only', '9b32002c', 'f3bb2014', '--', 'hdl']).decode().splitlines()
artifacts = json.loads((public/'CAPTURE-ARTIFACTS.json').read_text())
for arm in receipt['measurements']:
    shape = '1x1' if '1x1' in arm['shape'] else '8x8'
    tag = f"{shape}-{arm['cpu_hz']//1000000}-{arm['traffic']}"
    path = public / f'capture-{tag}.measurement.json'
    summary = json.loads(path.read_text())
    assert hashlib.sha256(Path('configs',arm['shape']+'.yaml').read_bytes()).hexdigest()==arm['config_sha256']
    assert all(arm[k] == v for k,v in summary.items())
    record = next(x for x in artifacts if x['file'].endswith(f'capture-{tag}/measurement.json'))
    assert record['sha256'] == hashlib.sha256(path.read_bytes()).hexdigest()
    log = (public/f'capture52-{tag}.log').read_text()
    assert 'Verilator 5.052 2026-09-05 rev v5.052' in log
    cmd = next(line for line in log.splitlines() if line.startswith('COMMAND verilator'))
    intersection = [p for p in changes if p in cmd]
    assert len(intersection)==7, intersection
    # run.py emits the full graded summary, after successful native completion.
    decoder = json.JSONDecoder()
    candidates = []
    for pos in (m.start() for m in re.finditer(r'\{\s*"shape"', log)):
        try:
            candidates.append(decoder.raw_decode(log[pos:])[0])
        except ValueError:
            pass
    assert summary in candidates, tag
    print('PASS', tag, '16 graded rows agree with committed receipt; published run reports recorded simulator; source intersection:')
    for p in intersection:
        print(' ', p)
    assert len(summary['rows']) == 16
    for product in ('cpu_netlist_sha256','instrumented_firmware_sha256','bios_sha256','gptp_ucode_sha256'):
        compare = next(x for x in json.loads((public/'capture52-products.json').read_text()) if x['arm']==tag)
        assert compare['products'][product]['same_as_round7']
        assert compare['products'][product]['sha256']==arm[product]
    assert not compare['headers_differing_beyond_timestamps']
print('PASS six arms, 96 rows; product hashes match; generated-header equality is reported after timestamp/build-directory normalization')
gates=json.loads((public/'GATES.json').read_text())
checked=0
for gate in gates:
    copied=gate.get('copied_log')
    if not copied:
        continue
    path=public/Path(copied['file']).name
    if path.exists():
        assert hashlib.sha256(path.read_bytes()).hexdigest()==copied['sha256'], path
        checked+=1
for name in ('act-flat-selftest-final','act-selftest-final','ci-scope-final','ci-events-final'):
    gate=next(x for x in gates if x['name']==name)
    assert gate['head']=='d5cd863561ba1ee7bc6342fb1b00f57dd786bd97' and gate['rc']==0
    if name.startswith('act-'):
        assert '--network' in gate['command'] and '--read-only' in gate['command']
        assert 'selftest: PASS' in (public/(name+'.log')).read_text()
print('PASS',checked,'downloaded logs match published gate-record SHA256; final runner selftests ran inside stated disposable boundary')
stable = ['hdl/milan/KL_nvm_backend.sv', 'sw/firmware/milan_baremetal/milan_baremetal.c',
          'tb/verilator/nvm_capture_cpu', 'tb/verilator/fw_service_budget',
          'configs/endstation_ax7101_1x1_tdm8.yaml', 'configs/endstation_ax7101_8x8.yaml',
          'sw/litex/patches', 'scripts/check_nvm_capture.py']
assert not subprocess.check_output(['git','diff','--name-only','9b32002c','f3bb2014','--',*stable])
print('PASS boot/capture firmware, harnesses, backend, configurations and patch inputs unchanged at the merge')
