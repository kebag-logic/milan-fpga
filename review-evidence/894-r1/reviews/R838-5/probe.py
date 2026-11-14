#!/usr/bin/env python3
"""Focused review probes. Usage: python3 -B probe.py CHECKOUT PACKET."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

repo, packet = map(lambda x: Path(x).resolve(), sys.argv[1:3])
scratch = packet / 'scratch'
evidence = scratch / 'review-evidence/894-r1'
author = evidence / 'author-r10'

def run(name, args, expected=0):
    p = subprocess.run(args, cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       text=True, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    log = p.stdout.replace(str(repo), '<checkout>').replace(str(packet), '<packet>')
    (packet / (name + '.log')).write_text(log)
    (packet / (name + '.rc')).write_text(str(p.returncode) + '\n')
    return {'name': name, 'command': [str(x).replace(str(repo), '<checkout>').replace(str(packet), '<packet>') for x in args],
            'rc': p.returncode, 'expected': expected, 'pass': p.returncode == expected}

jobs = [
    ('flip-1x1', [sys.executable, '-B', 'tb/verilator/ctrl_service_budget/flip_grade.py', '--check', '--point', '1x1/1if']),
    ('flip-8x8', [sys.executable, '-B', 'tb/verilator/ctrl_service_budget/flip_grade.py', '--check', '--point', '8x8/2if'], 1),
    ('core-filter', [sys.executable, '-B', 'sw/firmware/ctrl/test/aecp_arms.py', '--output', str(scratch/'core'), '--core', '--filter', 'Core.*Map*:Core.Every*']),
    ('compile-row', [sys.executable, '-B', 'sw/firmware/ctrl/test/aecp_mutants.py', '--output', str(scratch/'campaign'), '--shard', '257', '274']),
]
if '--audit-only' in sys.argv:
    results = json.loads((packet/'probe-results.json').read_text())
else:
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda x: run(*x), jobs))
(packet/'probe-results.json').write_text(json.dumps(results, indent=2)+'\n')
print(json.dumps(results, indent=2), flush=True)

rows = json.loads((evidence/'MANIFEST.json').read_text())
verified=[]
for r in rows:
    if r['file'].startswith(('author-r10/', 'author-r9/')):
        p = evidence/r['file']
        assert p.is_file(), r['file']
        assert hashlib.sha256(p.read_bytes()).hexdigest() == r['published_sha256'], r['file']
        verified.append(r['file'])
def hashes(name):
    entries = {}
    for line in (author/'receipts/images'/name).read_text().splitlines():
        if not line or line.startswith('#'):
            continue
        digest, name = line.split(maxsplit=1)
        assert name not in entries
        entries[name] = digest
    return entries
before = hashes('image-sha256-5b264bf2.txt')
after = hashes('image-sha256-7398ec0a.txt')
assert before == after and len(after) == 332
groups = {}
for path in after:
    group = path.split('/')[1]
    groups.setdefault(group, []).append(path)
assert len(groups) == 8
assert sum(p.endswith('.elf') for p in after) == 8
assert sum(p.endswith('.bin') for p in after) == 8
assert sum(p.endswith('.o') for p in after) == 316
audit = {'archive': '56e8f05bc2fa6d733d6b5c637bf1501d19dbe8dc', 'published_hashes_verified': len(verified),
         'verified_files': verified, 'image_entries': len(after), 'identical': True,
         'image_groups': {k:len(v) for k,v in groups.items()}}
(packet/'packet-audit.json').write_text(json.dumps(audit, indent=2)+'\n')
print('Published hashes verified:', len(verified), '; identical image entries:',len(after))
assert all(x['pass'] for x in results)
