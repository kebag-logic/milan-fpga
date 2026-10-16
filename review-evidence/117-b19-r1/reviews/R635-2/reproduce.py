#!/usr/bin/env python3
"""Read-only input audit and offline regeneration. Supply published packet, raw root, and output packet.

Usage: python3 reproduce.py AUTHOR_PACKET RAW_ROOT OUTPUT_PACKET
All disposable copies stay in OUTPUT_PACKET/scratch. No hardware access.
"""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

source, raw, out = map(lambda x: Path(x).resolve(), sys.argv[1:])
work = out / 'scratch' / 'regenerated'
shutil.copytree(source, work, dirs_exist_ok=True)
checks = []
for entry in json.loads((source / 'RAW-ARTIFACTS.json').read_text())['files']:
    name = entry['path'].split('/raw/', 1)[1]
    data = (raw / name).read_bytes()
    checks.append(dict(file=name, bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                       equal=len(data) == entry['bytes'] and hashlib.sha256(data).hexdigest() == entry['sha256']))
(out / 'raw-verification.json').write_text(json.dumps(checks, indent=2) + '\n')
assert all(x['equal'] for x in checks)

def run(tool, args, label):
    with (out / (label + '.log')).open('w') as log:
        proc = subprocess.run([sys.executable, str(work / 'tools' / tool), *map(str, args)],
                              stdout=log, stderr=subprocess.STDOUT, timeout=180)
    (out / (label + '.rc')).write_text(str(proc.returncode) + '\n')
    assert proc.returncode == 0, label

def box3():
    run('r2_box3_model.py', [raw, work], 'box3-model')
    run('r2_box3_grade.py', [work], 'box3-grade')
    run('r2_box3_grade.py', [work, '--selftest'], 'box3-controls')

def gm():
    run('r2_gm.py', [raw, work], 'gm-grade')
    run('r2_gm.py', [raw, work, '--selftest'], 'gm-controls')

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    futures = [pool.submit(box3), pool.submit(gm),
               pool.submit(run, 'r2_box4.py', [raw, work], 'box4-figures')]
    for future in futures:
        future.result()
equal = {}
for name in ['box3-model.json', 'box3-grade.json', 'gm-steps-r2.json', 'box4-derivations.json']:
    data = (work / 'round2' / name).read_bytes()
    equal[name] = dict(equal=data == (source / 'round2' / name).read_bytes(),
                      sha256=hashlib.sha256(data).hexdigest())
    (out / name).write_bytes(data)
(out / 'reproduction.json').write_text(json.dumps(equal, indent=2) + '\n')
assert all(x['equal'] for x in equal.values())
print('151 raw hashes verified; six offline commands succeeded; four outputs byte-identical.')
