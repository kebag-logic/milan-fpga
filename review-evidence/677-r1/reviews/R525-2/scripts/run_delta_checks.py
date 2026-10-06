#!/usr/bin/env python3
"""Foreground, read-only delta checks with individual raw logs and exit receipts."""
import argparse
import datetime
import json
import subprocess
import sys
import time
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('repository', type=Path)
ap.add_argument('packet', type=Path)
args = ap.parse_args()
repo, packet = args.repository.resolve(), args.packet.resolve()
receipts = packet / 'receipts'
checks = [
    ('public-final', [sys.executable, str(packet / 'scripts/capture_public.py'), str(receipts)]),
    ('delta-check', [sys.executable, str(packet / 'scripts/verify_delta.py'), str(repo), str(receipts)]),
    ('integrity-final', [sys.executable, str(packet / 'scripts/verify_integrity.py'), str(repo)]),
    ('source-whitespace', ['git', '-C', str(repo), 'diff', '--check',
                           '6714181d0c8a16e2983f85b724f4d688f5111835',
                           '6c94e9f5f496ac25f8c4e31f9e3685c725de29f3']),
]
records = []
for name, command in checks:
    start = time.monotonic()
    with (receipts / (name + '.log')).open('wb') as log:
        result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, timeout=60)
    (receipts / (name + '.rc')).write_text(str(result.returncode) + '\n')
    records.append({'check': name, 'argv': [arg.replace(str(repo), '<source>').replace(str(packet), '<packet>')
                                           for arg in command],
                    'rc': result.returncode, 'seconds': round(time.monotonic() - start, 3),
                    'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()})
    print(f'{name}: rc {result.returncode}')
    if result.returncode:
        break
(receipts / 'commands.json').write_text(json.dumps(records, indent=2) + '\n')
sys.exit(int(any(item['rc'] for item in records)))
