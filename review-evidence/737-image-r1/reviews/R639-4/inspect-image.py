#!/usr/bin/env python3
"""Authenticate published exports and pinned public inputs; inspect without Docker."""
import hashlib
import json
from pathlib import Path
import shutil
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
sys.path.insert(0, str(root / 'ci/image'))
import build
import image_archive
import image_lock
import privacy

work = packet / 'scratch/image'
work.mkdir(parents=True, exist_ok=True)
pins = json.loads((root / 'ci/image/sources.lock.json').read_text())
lock = json.loads((root / 'ci/image/image.lock.json').read_text())
published = json.loads((packet / 'scratch/public/round4-build-artifacts.json').read_text())

def copy_verified(source, target, size, expected):
    assert source.stat().st_size == size
    assert build.sha256(source) == expected
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        try:
            target.hardlink_to(source)
        except OSError:
            shutil.copyfile(source, target)
    assert build.sha256(target) == expected

for which in ('a', 'b'):
    row = next(r for r in published if r['artifact'] == f'cold-lock-{which}/image.tar')
    source = Path(sys.argv[2]) / row['artifact']
    copy_verified(source, work / f'image-{which}.tar', row['bytes'], row['sha256'])
    print('Authenticated published cold export', which, flush=True)

# These are public, checksum-pinned distribution inputs, not author source or notes.
source_work = Path(sys.argv[3])
for row in pins['packages'] + pins['sources']:
    relative = Path('debs') / row['filename'] if row in pins['packages'] else Path(row['filename'])
    copy_verified(source_work / 'context' / relative, work / 'context' / relative,
                  row['size'], row['sha256'])
base = source_work / 'base-locked.tar'
target = work / 'base-locked.tar'
if not target.exists():
    try:
        target.hardlink_to(base)
    except OSError:
        shutil.copyfile(base, target)

upstream = privacy.provenance(pins, work / 'context', privacy.Policy())
artifact = image_archive.inspect(work / 'image-a.tar', pins['platform'], upstream)
image_lock.validate(lock, pins, build.recipe_digest(), build.layer_records(pins))
image_lock.verify_artifact(lock, artifact)
first = image_archive.metadata(work / 'image-a.tar', pins['platform'])
second = image_archive.metadata(work / 'image-b.tar', pins['platform'])
assert first == second
assert first[0]['digest'] == lock['image_digest']
assert len(artifact['layers']) == 14
summary = {
    'image_digest': artifact['image_digest'], 'config_digest': artifact['image_id'],
    'recipe_digest': build.recipe_digest(), 'layers': artifact['layers'],
    'export_sha256': build.sha256(work / 'image-a.tar'),
    'two_exports_byte_identical': build.sha256(work / 'image-a.tar') == build.sha256(work / 'image-b.tar'),
    'authenticated_public_source_archives': len(pins['packages']) + len(pins['sources']),
    'privacy_allowances': len(artifact['upstream_allowances']),
    'patched_allowances': sum('patches' in a for a in artifact['upstream_allowances']),
    'full_config_and_history_scanned': True, 'every_layer_member_scanned': True,
}
(packet / 'image-authentication.json').write_text(json.dumps(summary, indent=2) + '\n')
(packet / 'image-config-history.json').write_text(json.dumps(first[2], indent=2) + '\n')
(packet / 'image-provenance.json').write_text(json.dumps(artifact['upstream_allowances'], indent=2) + '\n')
print(json.dumps(summary, indent=2), flush=True)
