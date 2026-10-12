#!/usr/bin/env python3
"""Independently re-derive hosted windows with decimal timestamp arithmetic."""
import argparse
import ast
import csv
from datetime import datetime, timezone
from decimal import Decimal, ROUND_CEILING
import hashlib
import json
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('repo', type=Path)
p.add_argument('packet', type=Path)
a = p.parse_args()
repo, packet = a.repo.resolve(), a.packet.resolve()
out = packet / 'receipts'
constants = {}
for node in ast.parse((repo / 'scripts/suite_shards.py').read_text()).body:
    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
        if node.targets[0].id in ('SUITE_SECONDS', 'WORKER_OVERHEAD_SECONDS'):
            constants[node.targets[0].id] = ast.literal_eval(node.value)

def ceil(value):
    return int(value.to_integral_value(rounding=ROUND_CEILING))

def stamp(value):
    value = value.lstrip('\ufeff').removesuffix('Z')
    whole, _, fraction = value.partition('.')
    base = int(datetime.strptime(whole, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc).timestamp())
    return Decimal(base) + Decimal('0.' + (fraction or '0'))

def measure(path):
    rows = []
    for line_no, line in enumerate(path.read_text().splitlines(), 1):
        parts = line.split('\t', 2)
        if len(parts) != 3:
            continue
        timestamp, _, message = parts[2].partition(' ')
        try:
            timestamp = stamp(timestamp)
        except ValueError:
            continue
        rows.append((line_no, timestamp, message))
    begin = next(r for r in rows if r[2].startswith('shard: '))
    shard = begin[2].split()[1]
    previous = begin
    windows = []
    summary = False
    for row in rows:
        if row[0] <= begin[0]:
            continue
        if row[2].startswith('suites: '):
            summary = True
            break
        tokens = row[2].split()
        if tokens and tokens[0] in ('PASS', 'FAIL', 'TIMEOUT'):
            assert tokens[0] == 'PASS', row
            duration = row[1] - previous[1]
            assert duration > 0
            windows.append({'suite': tokens[1], 'file': str(path.relative_to(packet)),
                            'worker': shard, 'start_line': previous[0], 'end_line': row[0],
                            'seconds_exact': str(duration), 'seconds_ceil': ceil(duration)})
            previous = row
    overhead = None
    if summary:
        assert len(windows) == int(begin[2].split()[-1])
        pre, post = begin[1] - rows[0][1], rows[-1][1] - previous[1]
        overhead = {'worker': shard, 'file': str(path.relative_to(packet)),
                    'first_line': rows[0][0], 'shard_line': begin[0],
                    'last_result_line': previous[0], 'last_line': rows[-1][0],
                    'setup_seconds': str(pre), 'tail_seconds': str(post),
                    'outside_seconds': str(pre + post), 'seconds_ceil': ceil(pre + post)}
    return windows, overhead

dev, overheads = [], []
for path in sorted((out / 'calibration-dev').glob('*.log')):
    windows, overhead = measure(path)
    dev.extend(windows)
    assert overhead is not None
    overheads.append(overhead)
maap, incomplete = measure(out / 'calibration-maap.log')
assert incomplete is None
maap = next(row for row in maap if row['suite'] == 'maap')
chosen = sorted([row for row in dev if row['suite'] != 'maap'] + [maap], key=lambda r: r['suite'])
assert len(chosen) == len(constants['SUITE_SECONDS']) == 62
for row in chosen:
    row['committed_seconds'] = constants['SUITE_SECONDS'][row['suite']]
    row['match'] = row['seconds_ceil'] == row['committed_seconds']
assert all(row['match'] for row in chosen)
overheads.sort(key=lambda r: int(r['worker'].split('/')[0]))
assert tuple(row['seconds_ceil'] for row in overheads) == constants['WORKER_OVERHEAD_SECONDS']
for name, rows in [('suite-measurements.csv', chosen), ('overhead-measurements.csv', overheads)]:
    with (out / name).open('w') as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

# Compare the production --measure output too, independently of the arithmetic above.
command = ['python3', 'scripts/suite_shards.py', '--measure'] + [str(path) for path in sorted((out / 'calibration-dev').glob('*.log'))]
r = subprocess.run(command, cwd=repo, capture_output=True, text=True, timeout=30)
(out / 'measure-dev.log').write_text(r.stdout + r.stderr)
(out / 'measure-dev.rc').write_text(str(r.returncode) + '\n')
assert r.returncode == 0
measured = {n.targets[0].id: ast.literal_eval(n.value) for n in ast.parse(r.stdout).body}
assert measured['SUITE_SECONDS'] == {row['suite']: row['seconds_ceil'] for row in dev}
assert measured['WORKER_OVERHEAD_SECONDS'] == constants['WORKER_OVERHEAD_SECONDS']
maap_output = ast.parse((out / 'measure-maap.log').read_text())
assert ast.literal_eval(maap_output.body[0].value)['maap'] == maap['seconds_ceil']

published = out / 'published'
manifest = json.loads((published / 'MANIFEST.json').read_text())
for entry in manifest:
    assert hashlib.sha256((published / entry['file']).read_bytes()).hexdigest() == entry['published_sha256']
hashes = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted((out / 'calibration-dev').glob('*.log'))}
hashes['calibration-maap.log'] = hashlib.sha256((out / 'calibration-maap.log').read_bytes()).hexdigest()
(out / 'measurement-summary.json').write_text(json.dumps({
    'verdict': 'PASS', 'suite_figures_checked': len(chosen), 'worker_overheads_checked': len(overheads),
    'maap': maap, 'production_measure_matches_independent_arithmetic': True,
    'dev_maap_superseded_seconds': measured['SUITE_SECONDS']['maap'], 'input_hashes': hashes,
    'published_author_manifest_verified': True,
}, indent=2) + '\n')
print('PASS: all 62 suite figures and five overheads equal independently measured hosted windows.')
print('maap', maap['seconds_exact'], 'seconds, rounded up to', maap['seconds_ceil'])
print('overheads', [row['seconds_ceil'] for row in overheads])
