#!/usr/bin/env python3
"""Run the two independent target campaigns and retain return codes."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument('source', type=Path)
p.add_argument('packet', type=Path)
p.add_argument('--gtest-prefix', type=Path)
p.add_argument('--clang-bin', type=Path)
a = p.parse_args()
source, packet = a.source.resolve(), a.packet.resolve()
env = dict(os.environ)
for key in ('CPATH', 'CPLUS_INCLUDE_PATH', 'C_INCLUDE_PATH', 'LIBRARY_PATH'):
    env.pop(key, None)
if a.gtest_prefix:
    prefix = a.gtest_prefix.resolve()
    env.update(CMAKE_PREFIX_PATH=str(prefix), PKG_CONFIG_PATH=str(prefix / 'lib/pkgconfig'),
               LD_LIBRARY_PATH=str(prefix / 'lib') + ':' + env.get('LD_LIBRARY_PATH', ''))
if a.clang_bin:
    env['PATH'] = str(a.clang_bin.resolve()) + ':' + env['PATH']
env['PYTHONDONTWRITEBYTECODE'] = '1'
commands = [
    ('validate', [sys.executable, 'scripts/validate.py', '--work', str(packet / 'scratch/validate'), '--jobs', '3']),
    ('rv32', [sys.executable, 'scripts/baremetal.py', '--work', str(packet / 'scratch/rv32'), '--jobs', '2']),
]

def run(item):
    name, command = item
    with (packet / 'receipts' / (name + '.log')).open('w') as log:
        result = subprocess.run(command, cwd=source, env=env, stdout=log, stderr=subprocess.STDOUT)
    (packet / 'receipts' / (name + '.rc')).write_text(str(result.returncode) + '\n')
    print(name, result.returncode, flush=True)
    return {'name': name, 'rc': result.returncode, 'command': command}

with ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(run, commands))
(packet / 'receipts/independent-gates.json').write_text(json.dumps(results, indent=2) + '\n')
sys.exit(int(any(row['rc'] for row in results)))
