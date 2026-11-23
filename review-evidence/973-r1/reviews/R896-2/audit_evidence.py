#!/usr/bin/env python3
"""Verify the public Round 2 receipts already extracted below PACKET/scratch."""
import hashlib
import json
from pathlib import Path
import sys

p = Path(sys.argv[1]).resolve()
b = p / 'scratch/review-evidence/973-r1'
manifest = json.loads((b / 'MANIFEST.json').read_text())
checks = []
for row in manifest:
    if not row['file'].startswith('author-r2/receipts/'):
        continue
    digest = hashlib.sha256((b / row['file']).read_bytes()).hexdigest()
    checks.append({'file': row['file'], 'sha256': digest,
                   'matches': digest == row['published_sha256'], 'redacted': row['path_redacted']})
assert checks and all(c['matches'] for c in checks)
(p / 'packet-hashes.json').write_text(json.dumps(checks, indent=2) + '\n')
print(f'PASS {len(checks)} published receipt SHA-256 values; zero mismatches')
a = b / 'author-r2/receipts'
for shape in ['1x1', '8x8-1if']:
    rows = [r.split('|')[1:-1] for r in (a / f'cpu/compare/probes-{shape}.md').read_text().splitlines()
            if r.startswith('| `')]
    bad = [r for r in rows if r[5].strip() != 'fits / fits' or float(r[2]) > float(r[4])]
    assert not bad
    print(f'{shape}: {len(rows)} probe pairs; zero verdict/budget misses; max absolute rounded delta '
          f'{max(abs(float(r[3])) for r in rows)} ms')
for name in ['flip_grade.py_--check_--point_1x1_1if.txt', 'flip_grade.py_--check_--point_8x8_1if.txt',
             'load_grade.py_--check.txt', 'shape_costs.py_--check.txt']:
    assert (a / ('cpu/graders/base-' + name)).read_bytes() == (a / ('cpu/graders/head-' + name)).read_bytes()
    print(f'PASS identical base/head grader receipt: {name}')
for shape in ['1x1-if1', '1x1-if2', '8x8-if1', '8x8-if2']:
    base, head = [json.loads((a / f'images/{rev}-{shape}-size.json').read_text())['split'] for rev in ['base', 'head']]
    assert head['sram']['bytes'] == base['sram']['bytes'] and head['tiles'] == base['tiles']
    limit = head.get('ledgered_tiles', head['budget_tiles'])
    assert head['tiles'] <= limit
    print(f"PASS {shape}: ROM {base['rom']['bytes']} -> {head['rom']['bytes']}; "
          f"SRAM {head['sram']['bytes']}; RAMB36 {head['tiles']} <= {limit}")
