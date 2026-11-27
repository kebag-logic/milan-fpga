#!/usr/bin/env python3
"""Audit public receipts without loading any other review report."""
import hashlib
import json
import math
import re
import subprocess
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
commit = 'be39b0e1bf12fe4f1b93cf092bccc94e4264cd06'
prefix = 'review-evidence/977-r1/'

def blob(path):
    return subprocess.check_output(['git', '-C', str(repo), 'show', f'{commit}:{prefix}{path}'])

manifest = json.loads(blob('MANIFEST.json'))
verified = []
for row in manifest:
    if not row['file'].startswith(('author/', 'author-r10/', 'author-r11/', 'author-text/')):
        continue
    got = hashlib.sha256(blob(row['file'])).hexdigest()
    assert got == row['published_sha256'], row['file']
    verified.append({'file': row['file'], 'sha256': got})

def maps(path):
    text = blob(path).decode()
    sections = []
    current = {}
    for line in text.splitlines():
        m = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
        if m:
            assert m[2] not in current, (path, m[2])
            current[m[2]] = m[1]
        elif current:
            sections.append(current)
            current = {}
    if current:
        sections.append(current)
    assert len(sections) >= 2, path
    assert all(len(s) == 80 for s in sections), [len(s) for s in sections]
    assert all(s == sections[0] for s in sections), path
    return sections[0], len(sections)

identities = {}
last = None
for path in ['author-r10/receipts/r10d/elf-identity-final.txt',
             'author-r11/receipts/elf-identity-9976b94f.txt',
             'author-r11/receipts/r11b/elf-identity-3181a3ec.txt']:
    m, n = maps(path)
    if last is not None:
        assert m == last, path
    last = m
    identities[path] = {'maps': n, 'identical_paths': len(m)}

deliveries = {}
for point, sinks in [('1x1', 2), ('8x8-1if', 9)]:
    text = blob(f'author-r11/receipts/meas/deliveries-{point}.txt').decode()
    rows = []
    for line in text.splitlines():
        m = re.search(r': (median|dearest) base before ([\d,]+) \((\d+) passes\); window (\d+) passes, excess ([\d,]+) cycles, ([\d,]+) a sink', line)
        if m:
            kind, base, prior, count, excess, share = m.groups()
            excess = int(excess.replace(',', ''))
            assert int(count) == 2 * sinks + 1
            assert abs(excess / sinks - int(share.replace(',', ''))) <= 0.501
            rows.append((kind, excess, line))
    assert rows
    results = {}
    for kind in ['median', 'dearest']:
        best = max((r for r in rows if r[0] == kind), key=lambda r: r[1])
        share = best[1] / sinks
        results[kind] = {'cycles_per_sink': share, 'stated_us': 5 * math.ceil(share / 100 * 1.05 / 5), 'row': best[2]}
    deliveries[point] = {'rows': len(rows), 'maxima': results}

out = {'evidence_commit': commit, 'verified_count': len(verified), 'verified': verified,
       'elf_identity': identities, 'delivery_arithmetic': deliveries,
       'limits': 'Published hashes and summarized measurements independently checked; raw ELF binaries and full CPU traces are not in this packet.'}
(packet / 'evidence-audit.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({k: v for k, v in out.items() if k != 'verified'}, indent=2))
