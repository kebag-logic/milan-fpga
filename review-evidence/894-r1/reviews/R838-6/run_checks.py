#!/usr/bin/env python3
"""Read-only focused checks; run from the exact candidate checkout."""
import concurrent.futures
import hashlib
import json
import pathlib
import subprocess
import sys

OUT = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path.cwd()
HEAD = '9606b3a915de284c71d3063c2e8d94b097f18241'
ARCHIVE = 'f3320c19d0d394ee7dd4a835e81c7a390df3fedb'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

assert git('rev-parse', 'HEAD').decode().strip() == HEAD
(OUT / 'receipts').mkdir(exist_ok=True)
manifest = json.loads(git('show', ARCHIVE + ':review-evidence/894-r1/MANIFEST.json'))
base = OUT / 'scratch/review-evidence/894-r1'
checked = []
for item in manifest:
    if not item['file'].startswith('author-r11/'):
        continue
    p = base / item['file']
    digest = hashlib.sha256(p.read_bytes()).hexdigest()
    assert digest == item['published_sha256'], item['file']
    checked.append({'file': item['file'], 'sha256': digest})
(OUT / 'receipts/packet-integrity.json').write_text(json.dumps({'archive': ARCHIVE, 'files': checked}, indent=2) + '\n')
print('Published manifest verified:', len(checked), 'files', flush=True)

B = 'tb/verilator/ctrl_service_budget/'
checks = {
    'flip-1x1': ['python3', '-B', B+'flip_grade.py', '--check', '--point', '1x1/1if'],
    'flip-selftest': ['python3', '-B', B+'flip_grade.py', '--selftest'],
    'tiers-selftest': ['python3', '-B', B+'rows_tiers.py', '--selftest'],
    'classes-selftest': ['python3', '-B', B+'record_classes.py', '--selftest'],
    'load-check': ['python3', '-B', B+'load_grade.py', '--check'],
    'tier-grid': ['python3', '-B', B+'tier_grid.py', '--point', '1x1/1if'],
}

def run(pair):
    name, argv = pair
    with (OUT / 'receipts' / (name+'.log')).open('w') as log:
        log.write('head: '+HEAD+'\ncommand: '+' '.join(argv)+'\n')
        log.flush()
        rc = subprocess.run(argv, stdout=log, stderr=subprocess.STDOUT, cwd=ROOT).returncode
        log.write('\nexit: '+str(rc)+'\n')
    (OUT / 'receipts' / (name+'.rc')).write_text(str(rc)+'\n')
    return name, rc

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    for name, rc in pool.map(run, checks.items()):
        print(name, rc, flush=True)
