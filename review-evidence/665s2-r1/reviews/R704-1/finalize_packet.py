#!/usr/bin/env python3
"""Check completed evidence, install the report, and hash the publication packet."""
import hashlib
import json
import os
from pathlib import Path
import subprocess

packet = Path(os.environ['REVIEW_PACKET'])
root = Path(os.environ['REVIEW_ROOT'])
head = 'd58c8e22e9bd96237b9a28ea1ddd55b0426380c4'
audit = json.loads((packet / 'measurement-audit.json').read_text())
for arm, cycles, composed in [('A1', 1552161, 1391312), ('A8', 2989496, 2141242)]:
    item = audit[arm]
    assert len(item['groups_completed']) == 14
    assert all(all(value.values()) for value in item['comparisons'].values())
    assert all(item['build_equal'].values())
    assert item['worst'][0] == cycles and item['composed'][0] == composed
    results = json.loads((packet / 'measurements' / arm / 'results.json').read_text())
    assert not results['refusals'] and len(results['results']) == 14
    assert json.loads((packet / (arm + '-run.rc.json')).read_text())['returncode'] == 0
identity = json.loads((packet / 'identity-final.json').read_text())
assert identity['head'] == head and identity['raw_bytes_modes_index'] == 'PASS'
assert not subprocess.check_output(['git', '-C', str(root), 'status', '--porcelain=v1'])
text = (packet / 'scratch/final-report.txt').read_text()
assert text.splitlines()[0] == '[R704] NEGATIVE - exact head ' + head
assert text.splitlines()[-1] == 'R704-1 FINISHED' and 'SKELETON' not in text
(packet / 'REPORT.md').write_text(text)
files = sorted(p for p in packet.rglob('*') if p.is_file()
               and 'scratch' not in p.relative_to(packet).parts and p.name != 'MANIFEST.sha256')
manifest = ''.join(hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + str(p.relative_to(packet)) + '\n'
                   for p in files)
(packet / 'MANIFEST.sha256').write_text(manifest)
print('Final report and', len(files), 'publishable files; all receipt completion checks passed.')
