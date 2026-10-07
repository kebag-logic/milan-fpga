#!/usr/bin/env python3
"""Copy execution logs with declared location-only redaction; bind both digests."""
import argparse
import hashlib
import json
from pathlib import Path

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--root', required=True)
p.add_argument('--packet', required=True)
p.add_argument('--dependency-root', required=True)
args = p.parse_args()
packet = Path(args.packet).resolve()
scratch = packet / 'scratch'
sources = [scratch / 'cpu-campaign.log', scratch / 'refusals.log']
sources += sorted(scratch.glob('ax-*.log'))
sources += sorted((scratch / 'cpu-exports').glob('*.log'))
replacements = [(str(packet), '$PACKET'), (str(Path(args.root).resolve()), '$SOURCE_ROOT'),
                (str(Path(args.dependency_root).resolve()), '$DEPENDENCIES'), (str(Path.home()), '$HOME')]
records = []
for source in sources:
    raw = source.read_bytes()
    redacted = raw
    for old, new in replacements:
        redacted = redacted.replace(old.encode(), new.encode())
    dest = packet / 'receipts' / source.relative_to(scratch)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(redacted)
    records.append({'file': str(dest.relative_to(packet)), 'original_sha256': hashlib.sha256(raw).hexdigest(),
                    'published_sha256': hashlib.sha256(redacted).hexdigest(), 'location_redaction': raw != redacted})
    rc = source.with_suffix('.rc')
    if rc.exists():
        dest.with_suffix('.rc').write_bytes(rc.read_bytes())
(packet / 'receipts/log-provenance.json').write_text(json.dumps(records, indent=2) + '\n')
print(f'Published {len(records)} log receipts; original outputs retained only in scratch')
