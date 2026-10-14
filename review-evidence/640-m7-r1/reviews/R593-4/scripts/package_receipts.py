#!/usr/bin/env python3
"""Publish path-neutral receipts; retain original bytes only in scratch."""
import argparse
import hashlib
import json
from pathlib import Path
import re

ap = argparse.ArgumentParser()
ap.add_argument('--packet', type=Path, required=True)
ap.add_argument('--repo', type=Path, required=True)
a = ap.parse_args()
packet, repo = a.packet.resolve(), a.repo.resolve()
raw_dir = packet / 'scratch/raw-receipts'
raw_dir.mkdir(parents=True, exist_ok=True)
records = []
for path in sorted((packet / 'receipts').iterdir()):
    if path.name in ['publication-redactions.json', 'receipt-index.json']:
        continue
    if path.suffix == '.diff':
        # The original source diffs remain available locally; commit URLs in
        # the report provide their public source without duplicating the tree.
        continue
    if not path.is_file():
        continue
    raw_path = raw_dir / path.name
    if not raw_path.exists():
        raw_path.write_bytes(path.read_bytes())
    original = raw_path.read_bytes()
    body = original.decode('utf-8')
    body = re.sub(r'/home/[^/\s]+/\.local/share/containers/storage/overlay/[^/\s]+/diff/usr/share/verilator',
                  '$PINNED_COMPILER_ROOT', body)
    body = body.replace(str(packet), '$REVIEW_PACKET').replace(str(repo), '$REVIEW_CLONE')
    body = re.sub(r'/data/[^\s"\']*/tools/pinned-verilator-5\.050', '$PINNED_COMPILER_DIR', body)
    body = re.sub(r'/home/[^/\s]+', '$HOME', body)
    published = body.encode('utf-8')
    path.write_bytes(published)
    records.append({'path': path.relative_to(packet).as_posix(),
                    'original_sha256': hashlib.sha256(original).hexdigest(),
                    'published_sha256': hashlib.sha256(published).hexdigest(),
                    'path_substitutions': original != published})
(packet / 'receipts/publication-redactions.json').write_text(json.dumps(records, indent=2) + '\n')
files = sorted(path for directory in ['scripts', 'receipts']
               for path in (packet / directory).iterdir()
               if path.is_file() and path.suffix != '.diff')
files.append(packet / 'REPORT.md')
manifest = ''.join(hashlib.sha256(path.read_bytes()).hexdigest() + '  ' +
                   path.relative_to(packet).as_posix() + '\n' for path in sorted(files))
(packet / 'MANIFEST.sha256').write_text(manifest)
print('Publication set:', len(files), 'files; scratch and fetched source metadata excluded')
print('Report SHA-256:', hashlib.sha256((packet / 'REPORT.md').read_bytes()).hexdigest())
