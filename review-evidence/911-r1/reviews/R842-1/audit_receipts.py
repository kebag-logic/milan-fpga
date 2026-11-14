#!/usr/bin/env python3
"""Check archived receipts against their manifest and independent arithmetic."""
import hashlib
import json
from pathlib import Path
import re
import sys

repo, packet = map(Path, sys.argv[1:3])
archive = packet / 'scratch/review-evidence/911-r1'
receipts = archive / 'author-r1/receipts'
manifest = json.loads((archive / 'MANIFEST.json').read_text())
for entry in manifest:
    assert hashlib.sha256((archive / entry['file']).read_bytes()).hexdigest() == entry['published_sha256'], entry['file']
print('Published archive manifest:', len(manifest), 'files match their SHA-256')
before = (receipts / 'ax7101-identity/sources-b7d69295.sha256').read_bytes()
after = (receipts / 'ax7101-identity/sources-1e604e1b.sha256').read_bytes()
assert before == after
lines = before.decode().splitlines()
assert len(lines) == 140
print('AX7101 input lists: 140 identical rows; list SHA-256', hashlib.sha256(before).hexdigest())
present, absent, different = [], [], []
for line in lines:
    digest, relative = line.split(None, 1)
    path = repo / relative.strip()
    if not path.is_file():
        absent.append(relative)
    elif hashlib.sha256(path.read_bytes()).hexdigest() != digest:
        different.append(relative)
    else:
        present.append(relative)
print('At review head:', len(present), 'available input files match,', len(absent), 'generated/unavailable,', len(different), 'different')
assert not different, different
rows = []
for line in (receipts / 'gates/workflow-steps.md').read_text().splitlines()[2:]:
    if line.startswith('|'):
        rows.append([v.strip() for v in line.split('|')[1:-1]])
passed = [r for r in rows if r[4] == '0']
skipped = [r for r in rows if r[4] == 'NOT RUN']
assert len(passed) == 150 and len(skipped) == 522 and len(rows) == 672
assert all(r[5] and '.log`' not in r[5] for r in skipped)
not_run = json.loads((receipts / 'gates/not_run.json').read_text())
print('Workflow table: 150 rc=0, 522 NOT RUN, all with reasons; not_run.json entries', len(not_run))
print('Author source execution only; no manager source bank inferred.')
sweep = (receipts / 'gates/sweep.txt').read_text()
counts = re.findall(r'suites: (\d+)\s+passed: (\d+)\s+failed: (\d+)\s+timed out: (\d+)', sweep)
assert len(counts) == 4
totals = [sum(int(row[i]) for row in counts) for i in range(4)]
assert totals == [65, 65, 0, 0], totals
print('Published sweep summaries: 65 suites, 65 pass, 0 failed, 0 timeout')
for row in passed:
    if row[1] == 'elaborate-gates-2':
        print('Fresh-clone rerun receipt row:', row)
pins = {}
for line in (receipts / 'io-200t-vs-ax7101.md').read_text().splitlines():
    cols = [c.strip() for c in line.split('|')[1:-1]]
    if len(cols) == 7 and re.fullmatch(r'[A-Z]+\d+', cols[0]):
        pins[cols[0]] = (cols[1], cols[2], cols[3], cols[4], cols[6])
assert len(pins) == 113
for build in ('buildA-compressed', 'buildB', 'buildC-release'):
    raw = (receipts / build / (build + '-io-used.txt')).read_text()
    measured = {}
    for line in raw.splitlines():
        cols = [c.strip() for c in line.split('|')[1:-1]]
        measured[cols[0]] = (cols[1], cols[3], cols[6], cols[5], cols[4])
    assert measured == pins, build
print('All 113 published pin rows agree with release comparison in all three builds (signal, pin name, bank, standard, use).')
for suffix in ('svg', 'drawio'):
    for stem in ('flash_layout', 'flash_layout_xc7a200t'):
        assert (packet / 'scratch' / (stem + '.' + suffix)).read_bytes() == (repo / 'docs/diagrams' / (stem + '.' + suffix)).read_bytes()
print('Both regenerated diagram SVG and editable master pairs are byte-identical.')
assert 5566832 - 4 * 1024**2 == 1372528
assert 10 * 1024**2 - 9730652 == 755108
assert 9730856 - 9730652 == 204
print('Compressed payload exceeds 4 MiB by 1,372,528 B; uncompressed payload leaves 755,108 B at 10 MiB; .bit header is 204 B.')
