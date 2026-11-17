#!/usr/bin/env python3
"""Finalize receipts after all foreground runs complete.
Usage: seal_packet.py PACKET ORIGINAL_CHECKOUT
Raw logs are retained in scratch/raw; publishable logs redact host paths only.
"""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

packet, original = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
for name in ('twin', 'twin-plants', 'srp-focused', 'dynmap-probes', 'dynmap-focused', 'twin-trace'):
    assert (packet / (name + '.rc')).read_text().strip() == '0', name
refused = re.findall(r'^plant ([\w-]+): REFUSED', (packet / 'twin-plants.log').read_text(), re.M)
assert len(refused) == 42 and len(set(refused)) == 21
assert all(refused.count(p) == 2 for p in set(refused))
assert '4 checks: 4 PASS, 0 FAIL' in (packet / 'dynmap-focused.log').read_text()
for file in packet.glob('srp-control-*.log'):
    assert '[  PASSED  ] 74 tests.' in file.read_text()
with (packet / 'tree-integrity.log').open('w') as out:
    subprocess.run([sys.executable, '-B', str(packet / 'verify_tree.py'), str(original)], stdout=out, check=True)
captures = packet / 'captures'
captures.mkdir(exist_ok=True)
for name in ('fabric.json', 'split.json', 'split-talker-failed-back.json', 'report.json'):
    shutil.copyfile(packet / 'scratch/tree/tb/verilator/milan_dp/obj_twin' / name, captures / name)
raw = packet / 'scratch/raw'
raw.mkdir(exist_ok=True)
for file in packet.glob('*.log'):
    shutil.copyfile(file, raw / file.name)
    text = file.read_text()
    text = text.replace(str(packet), '<packet>').replace(str(original), '<review-checkout>')
    text = re.sub(r'/home/[^/\s]+/\.local/share/containers/storage/overlay/[^/\s]+/diff/usr/share/verilator',
                  '<simulator-includes>', text)
    text = re.sub(r'/home/[^/\s]+', '<home>', text)
    text = text.replace('$VALIDATION_TOOLS/pinned-verilator-5.050/verilator', '<scoped-simulator>')
    file.write_text(text)
report = (packet / 'REPORT.md').read_text()
assert report.startswith('[R856] POSITIVE - exact head 372556835d03b70134b2e76567b63b25c4cca005\n')
assert report.rstrip().endswith('R856-1 FINISHED') and 'SKELETON' not in report
files = sorted(p for p in packet.rglob('*') if p.is_file() and 'scratch' not in p.relative_to(packet).parts
               and p.name != 'MANIFEST.sha256')
with (packet / 'MANIFEST.sha256').open('w') as out:
    for file in files:
        out.write(hashlib.sha256(file.read_bytes()).hexdigest() + '  ' + str(file.relative_to(packet)) + '\n')
print(f'Sealed {len(files)} publishable files including REPORT.md; scratch excluded')
