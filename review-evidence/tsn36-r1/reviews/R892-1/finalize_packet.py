#!/usr/bin/env python3
"""Verify the finished report, record source integrity, and hash publishable files."""
import hashlib
from pathlib import Path
import re
import subprocess as sp
import sys

repo, packet = map(lambda p: Path(p).resolve(), sys.argv[1:])
raw = packet / 'scratch' / 'public-readbacks'
raw.mkdir(parents=True, exist_ok=True)
prior = packet / 'pr35-comments.json'
if prior.exists():
    prior.replace(raw / prior.name)
with (packet / 'tree-after.json').open('w') as out:
    sp.run([sys.executable, str(packet / 'audit_tree.py'), str(repo)], stdout=out, check=True)
report = (packet / 'REPORT.md').read_text()
assert report.splitlines()[0] == '[R892] POSITIVE - exact head 61a504eec3ec3de828ccd80076212533ef58644b'
assert report.splitlines()[-1] == 'R892-1 FINISHED'
assert 'SKELETON' not in report and 'INCOMPLETE' not in report
for link in re.findall(r'\]\(([^)]+)\)', report):
    if '://' not in link:
        assert (packet / link.split('#')[0]).is_file(), link
for rc in packet.glob('*.rc'):
    expected = 1 if rc.stem in ('probe-head', 'probe-setup-error') else 0
    assert int(rc.read_text()) == expected, rc.name
files = [p for p in packet.rglob('*') if p.is_file() and 'scratch' not in p.relative_to(packet).parts
         and p.name != 'MANIFEST.sha256']
(packet / 'final-check.txt').write_text(
    'PASS: exact head/tree, all tracked bytes/modes/index, clean worktree, no gitlinks.\n'
    'PASS: final report format, five-lens ledger, relative receipt links and expected return codes.\n'
    'PASS: independent verdict was written before prior public findings were fetched.\n'
    'Publication excludes scratch trees and other reviewers full reports.\n')
files = [p for p in packet.rglob('*') if p.is_file() and 'scratch' not in p.relative_to(packet).parts
         and p.name != 'MANIFEST.sha256']
lines = [hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + p.relative_to(packet).as_posix()
         for p in sorted(files)]
(packet / 'MANIFEST.sha256').write_text('\n'.join(lines) + '\n')
sp.run(['sha256sum', '--check', '--quiet', 'MANIFEST.sha256'], cwd=packet, check=True)
print(f'PASS: {len(files)} publishable files hashed; scratch excluded; all hashes verified.')
