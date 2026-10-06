#!/usr/bin/env python3
"""Publish the completed report and hash only the explicitly publishable files.

Usage: python3 -B finalize_packet.py CHECKOUT PACKET
Requires the foreground campaigns to have completed and the draft to have
no pending markers. All scratch material stays outside the manifest.
"""
import hashlib
from pathlib import Path
import subprocess
import sys

root, packet = map(lambda p: Path(p).resolve(), sys.argv[1:3])
receipts = packet / 'receipts'
negative_controls = {'listener-skip.rc', 'listener-setup.rc', 'listener-crash.rc'}
required = ('ctrl', 'nvm', 'coverage', 'tally', 'mailbox', 'focused-probes',
            'listener-probes', 'environment-probe', 'port-inventory',
            'coverage-selftest', 'ci-scope', 'ci-events-check', 'ci-events-selftest',
            'docs-check', 'doc-paths', 'cpp-idiom', 'python-idiom', 'diff-check')
for name in required:
    assert (receipts / f'{name}.rc').read_text().strip() == '0', name
for path in receipts.glob('*.rc'):
    expected = '1' if path.name in negative_controls else '0'
    assert path.read_text().strip() == expected, path.name
with (receipts / 'final-audit.log').open('w') as output:
    subprocess.run([sys.executable, '-B', str(packet/'scripts/audit_checkout.py'), str(root)],
                   stdout=output, stderr=subprocess.STDOUT, check=True)
status = subprocess.check_output(['git', '-C', str(root), 'status', '--porcelain=v1',
                                  '--untracked-files=all'])
assert not status, 'candidate worktree is not clean'
(receipts/'final-status.log').write_text('git status --porcelain=v1 --untracked-files=all: empty\n')
report = (packet/'scratch/report-draft.md').read_text()
assert report.splitlines()[0] == '[R507] POSITIVE - exact head e7e0c10f4d4e9f3180b5650507a83aa300c5d4d7'
assert report.splitlines()[-1] == 'R507-2 FINISHED'
assert 'SKELETON' not in report and 'NVM_PENDING' not in report
assert report.count('| CLEAN |') == 5
(packet/'REPORT.md').write_text(report)
files = [packet/'REPORT.md', *sorted((packet/'scripts').glob('*.py')), *sorted(receipts.iterdir())]
assert all(p.is_file() for p in files)
for p in files:
    if p.parent == receipts or p.name == 'REPORT.md':
        assert b'/home/' not in p.read_bytes(), f'private path in {p.name}'
manifest = ''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(packet)}\n' for p in files)
(packet/'MANIFEST.sha256').write_text(manifest)
subprocess.run(['sha256sum', '--check', '--quiet', 'MANIFEST.sha256'], cwd=packet, check=True)
print(f'final audit PASS; clean checkout; {len(files)} publishable files verified; scratch excluded')
print('R507-2 FINISHED')
