#!/usr/bin/env python3
"""Validate verdict receipts, redact only local include roots, and seal publication."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--packet', type=Path, required=True)
a = p.parse_args()
packet, source = a.packet.resolve(), a.source.resolve()
receipts = packet / 'receipts'
report = (packet / 'REPORT.md').read_text()
assert report.splitlines()[0] == '[R489] POSITIVE - exact head 9050c4bbd25556929a0f24fb98258bc98e3bcfbe'
assert report.splitlines()[-1] == 'R489-2 FINISHED' and 'SKELETON' not in report
for name in ['srp-top', 'stream-fsms', 'expanded-events', 'lv-mutants', 'docs-focused', 'patch-planting']:
    assert (receipts / (name + '.rc')).read_text().strip() == '0', name
assert (receipts / 'masked-integrated.rc').read_text().strip() == '2'
top = (receipts / 'srp-top.log').read_text()
assert '8656 checks: 8656 PASS, 0 FAIL' in top
assert 'TOTAL_CLOCKS 210547557' in top
assert top.count('LV_COLLISION ') == 6416 and 'STUCK' not in top and 'FAIL:' not in top
lv = [line for line in top.splitlines() if line.startswith('LV_LEAVE ')]
assert len(lv) == 8 and all('leave_time_ms=5000 stream_stop=1 stream_start=0' in line for line in lv)
masked = (receipts / 'masked-integrated.log').read_text()
assert len([l for l in masked.splitlines() if l.startswith('FAIL: SC2:')]) == 16
assert '6432 checks: 6416 PASS, 16 FAIL' in masked
reversed_files = []
for filename in ['KL_srp_talker_fsm.sv', 'KL_srp_listener_fsm.sv']:
    rel = 'hdl/srp/' + filename
    base = subprocess.check_output(['git', '-C', str(source), 'show',
        'ead8036035affd53ef4b29979190f2f4f67084c0:' + rel])
    actual = (packet / 'scratch/masked-integrated' / rel).read_bytes()
    assert base == actual, filename
    reversed_files.append(rel)
with (receipts / 'tree-after.json').open('w') as out:
    subprocess.run(['python3', str(packet / 'scripts/verify_tree.py'), str(source)], stdout=out, check=True)
status = subprocess.check_output(['git', '-C', str(source), 'status', '--porcelain=v1', '--untracked-files=all'])
assert not status, status
(receipts / 'final-status.txt').write_bytes(status)
(receipts / 'review-audit.json').write_text(json.dumps(dict(
    integrated_checks=8656, executed_clocks=210547557, collision_offsets=6416,
    leave_cases=8, measured_leave_ms=5000, expected_masked_failures=16,
    reverse_patch_restores_base_bytes=reversed_files, tracked_integrity='PASS'), indent=2) + '\n')
# Only the scoped installation's private include root is redacted. Preserve raw
# originals outside the publication boundary and retain both hashes for audit.
root_pattern = re.compile(rb'/home/[^/\s]+/\.local/share/containers/storage/overlay/[0-9a-f]+/diff/usr/share/verilator')
redactions = []
for f in sorted(receipts.rglob('*.log')):
    original = f.read_bytes()
    public = root_pattern.sub(b'<SCOPED_SIMULATOR_ROOT>', original)
    if original != public:
        raw = packet / 'scratch/raw-receipts' / f.relative_to(receipts)
        raw.parent.mkdir(parents=True, exist_ok=True)
        raw.write_bytes(original)
        f.write_bytes(public)
        redactions.append(dict(path=f.relative_to(packet).as_posix(),
            raw_sha256=hashlib.sha256(original).hexdigest(),
            published_sha256=hashlib.sha256(public).hexdigest(),
            change='local include root only; no result or diagnostic altered'))
redaction_file = receipts / 'path-redactions.json'
if redactions:
    redaction_file.write_text(json.dumps(redactions, indent=2) + '\n')
files = [packet / 'REPORT.md'] + sorted((packet / 'scripts').rglob('*')) + sorted(receipts.rglob('*'))
files = [f for f in files if f.is_file() and '__pycache__' not in f.parts]
manifest = ''.join(hashlib.sha256(f.read_bytes()).hexdigest() + '  '
                   + f.relative_to(packet).as_posix() + '\n' for f in files)
(packet / 'MANIFEST.sha256').write_text(manifest)
print('Publication sealed: %d files; source bytes, modes, index and zero gitlinks verified.' % len(files))
