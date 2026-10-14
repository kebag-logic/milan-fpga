#!/usr/bin/env python3
"""Reproduce the merged inventory refusal without running simulation banks."""
import argparse
import concurrent.futures
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--repo', type=Path, required=True)
p.add_argument('--packet', type=Path, required=True)
a = p.parse_args()
repo, packet = a.repo.resolve(), a.packet.resolve()
receipts = packet / 'receipts'

def git(*args):
    return subprocess.check_output(['git', '--no-replace-objects', '-C', str(repo), *args])

def probe(label, revision, expected):
    if label == 'head':
        root = repo
    else:
        root = packet / 'scratch' / ('inventory-' + label)
        names = git('ls-tree', '-r', '--name-only', revision).decode().splitlines()
        paths = [name for name in names if
                 (name.startswith('tb/verilator/') and name.count('/') == 3 and name.endswith('/Makefile'))
                 or name in ['scripts/suite_shards.py', 'scripts/run_all_suites.sh', '.github/workflows/rtl.yml']]
        for name in paths:
            dest = root / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(git('show', revision + ':' + name))
    cmd = ['python3', 'scripts/suite_shards.py', '--selftest']
    result = subprocess.run(cmd, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (receipts / ('inventory-' + label + '.log')).write_bytes(result.stdout)
    (receipts / ('inventory-' + label + '.rc')).write_text(str(result.returncode) + '\n')
    assert result.returncode == expected, (label, result.stdout.decode())
    if label == 'head':
        assert b'gptp_tables: inventory suite with no recorded duration' in result.stdout
    print(label, revision, 'expected rc', expected, 'observed', result.returncode)
    print('\n'.join(row for row in result.stdout.decode().splitlines()
                    if 'FAIL' in row or 'skip head' in row or row.startswith('selftest:')))

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    futures = [pool.submit(probe, 'head', '412e3f6c8c402bce63e94c291d2782b5579aaa1d', 1),
               pool.submit(probe, 'dev', 'fa8209889411e8ca95757174c981f720dbcd95a2', 0),
               pool.submit(probe, 'round3', '354f781828d8b4d73037129f297b072320a10f9c', 0)]
    for future in futures:
        future.result()
print('REPRODUCED: both input inventories pass; the merged inventory fails')
