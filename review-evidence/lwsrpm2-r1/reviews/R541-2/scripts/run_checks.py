# SPDX-License-Identifier: Apache-2.0
"""Run independent small campaigns concurrently; retain every command and result."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--packet', type=Path, required=True)
p.add_argument('--jobs', type=int, default=4)
p.add_argument('--phase', choices=['main', 'reversals'], default='main')
a = p.parse_args()
source, packet = a.source.resolve(), a.packet.resolve()
scratch, receipts = packet / 'scratch', packet / 'receipts'
prefix = scratch / 'deps'
env = os.environ.copy()
env['PYTHONDONTWRITEBYTECODE'] = '1'
env['LD_LIBRARY_PATH'] = str(prefix / 'lib') + ':' + env.get('LD_LIBRARY_PATH', '')

def clean(s):
    return s.replace(str(source), '$SOURCE').replace(str(packet), '$PACKET')

def run(label, cmd, extra=None, cwd=source, timeout=480):
    e = env.copy()
    e.update(extra or {})
    r = subprocess.run(list(map(str, cmd)), cwd=cwd, env=e, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, text=True, timeout=timeout)
    (scratch / (label + '.raw.log')).write_text(r.stdout)
    (receipts / (label + '.log')).write_text(clean(r.stdout))
    (receipts / (label + '.rc')).write_text(str(r.returncode) + '\n')
    (receipts / (label + '.command.json')).write_text(json.dumps({
        'argv': [clean(str(x)) for x in cmd], 'cwd': clean(str(cwd)),
        'environment': {k: clean(v) for k, v in (extra or {}).items()},
        'rc': r.returncode}, indent=2) + '\n')
    print(label, 'rc', r.returncode, flush=True)
    return r.returncode

def profile(mode):
    b = scratch / ('build-' + mode)
    assert run('configure-' + mode, ['cmake', '-S', source, '-B', b,
        '-DCMAKE_BUILD_TYPE=Debug', '-DCMAKE_PREFIX_PATH=' + str(prefix),
        '-DLWSRP_MILAN=' + mode]) == 0
    assert run('build-' + mode, ['cmake', '--build', b, '--parallel', '4']) == 0
    for label, cmd, extra in [
        ('unit', [b / 'unit_tests'], {}),
        ('ctest', ['ctest', '--test-dir', b, '--output-on-failure'], {}),
        ('behave', ['behave'], {'SHLAN_LIBRARY': str(b / 'libshlan.so')})]:
        assert run(label + '-' + mode, cmd, extra) == 0

def docs():
    for label, cmd in [
        ('sentences', ['python3', 'doc/tools/check_sentences.py']),
        ('references', ['python3', 'doc/tools/check_references.py']),
        ('reference-selftest', ['python3', 'doc/tools/check_references.py', '--self-test']),
        ('links', ['python3', 'doc/tools/check_links.py', '--github-auth']),
        ('graphs', ['python3', 'doc/tools/render_mermaid.py', '--output', scratch / 'graphs'])]:
        run(label, cmd)

def embedded():
    run('embedded', ['python3', 'tests/check_embedded.py', '--work-dir', scratch / 'embedded'])
    run('freestanding-OFF', ['python3', 'tests/check_freestanding.py'])
    run('freestanding-ON', ['python3', 'tests/check_freestanding.py'], {'CC': 'cc -DLWSRP_MILAN=1'})
    run('behave-dry', ['behave', '--dry-run'])

def reversals(mode):
    run('reversals-' + mode, ['python3', 'tests/check_reversals.py',
        '--work-dir', scratch / ('reversals-' + mode), '--prefix', prefix, '--milan', mode], timeout=590)
    d = scratch / ('reversals-' + mode)
    out = receipts / ('reversals-' + mode)
    out.mkdir(exist_ok=True)
    for f in d.iterdir():
        if f.is_file() and f.suffix in ['.log', '.json']:
            (out / f.name).write_text(clean(f.read_text()))

tasks = [(profile, 'OFF'), (profile, 'ON'), (docs,), (embedded,)] if a.phase == 'main' else [(reversals, 'OFF'), (reversals, 'ON')]
with ThreadPoolExecutor(max_workers=min(a.jobs, 4)) as pool:
    futures = [pool.submit(t[0], *t[1:]) for t in tasks]
    for f in futures:
        f.result()
