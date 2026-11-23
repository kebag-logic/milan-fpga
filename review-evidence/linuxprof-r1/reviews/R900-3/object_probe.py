#!/usr/bin/env python3
"""Compile the unchanged loop with each revision's header and compare bytes."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
sys.dont_write_bytecode = True
repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
work = packet / 'scratch/objects'
work.mkdir(parents=True, exist_ok=True)
tempfile.tempdir = str(packet / 'scratch')
os.environ['TMPDIR'] = tempfile.tempdir
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
sys.path.insert(0, str(repo / 'sw/builder'))
import test_builder as gate
revs = ['854bd7236792ce1adbd10c43b13a6a5002ad3bb6', '58f7673b8c57a80230e716bc1774ff9cc2f71ddc']
for rev in revs:
    target = work / rev / 'loop'
    target.mkdir(parents=True, exist_ok=True)
    for name in ('ctrl_loop.c', 'ctrl_loop.h'):
        (target / name).write_bytes(subprocess.check_output(['git', '-C', str(repo), 'show', rev + ':sw/firmware/ctrl/loop/' + name]))
    host = target.parent / 'host'
    host.mkdir(exist_ok=True)
    if rev == revs[1]:
        (host / 'ctrl_loop_host.h').write_bytes((repo / 'sw/firmware/ctrl/host/ctrl_loop_host.h').read_bytes())
headers = {'none': None}
for name in ('ax7101_1x1_tdm8', 'ax7101_8x8'):
    headers[name] = gate._host_generated(work, gate.CONFIGS[name])['srp_entity']
ctrl = repo / 'sw/firmware/ctrl'
inc = [str(ctrl / p) for p in ('mbx', 'loop', 'port', 'app', 'aecp', 'srp', 'adp', 'acmp', 'maap')]
inc += [str(repo / p) for p in ('third_party/tsn-c-stack/include', 'third_party/lwSRP/src/include', 'sw/firmware/ctrl_nvm')]
print(subprocess.check_output(['cc', '--version']).decode().splitlines()[0])
def pair(point):
    n_if, name = point
    contract = work / f'mbx_contract_if{n_if}.h'
    digests = []
    for rev in revs:
        dest = work / rev / f'{n_if}-{name}.o'
        cmd = ['cc', '-std=c11', '-O2', '-DNDEBUG', '-Wall', '-Wextra', '-Werror', '-pedantic', '-include', str(contract)]
        if headers[name]:
            cmd += ['-include', str(headers[name])]
        cmd += ['-I' + p for p in inc] + ['-c', str(work / rev / 'loop/ctrl_loop.c'), '-o', str(dest)]
        p = subprocess.run(cmd, capture_output=True)
        assert p.returncode == 0, p.stderr.decode()
        digests.append(hashlib.sha256(dest.read_bytes()).hexdigest())
    assert digests[0] == digests[1], (point, digests)
    return f'{n_if}if {name}: ctrl_loop.o IDENTICAL sha256 {digests[0]}'
# Contracts created serially to avoid concurrent writes to one input.
for n in (1, 2):
    gate._contract_at(n, work)
with ThreadPoolExecutor(max_workers=2) as pool:
    for result in pool.map(pair, [(n, name) for n in (1, 2) for name in headers]):
        print(result)
print('RESULT: PASS; 6/6 independently compiled object pairs byte-identical')
