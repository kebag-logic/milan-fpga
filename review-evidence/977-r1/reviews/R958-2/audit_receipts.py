#!/usr/bin/env python3
"""Audit the public author packet extracted by check_packet.py; no review reports read."""
import csv
import json
from pathlib import Path
import re

p = Path(__file__).resolve().parent
r = p / 'scratch/public-packet/author-r10/receipts'
out = {}
for name in ('pins/elf-identity.txt', 'r10d/elf-identity-final.txt',
             'r10d/tx80-elf-identity-e59cf6ea.txt'):
    sections, current = {}, None
    for line in (r / name).read_text().splitlines():
        if line.startswith('## '):
            current = line[3:]
            sections[current] = {}
        m = re.fullmatch(r'([0-9a-f]{64})  (.+\.elf)', line)
        if m:
            assert current is not None
            assert m[2] not in sections[current], (name, current, m[2])
            sections[current][m[2]] = m[1]
    sections = {k: v for k, v in sections.items() if v}
    assert len(sections) == (3 if name.startswith('pins/') else 2), name
    values = list(sections.values())
    assert all(len(v) == 80 and v == values[0] for v in values), name
    out[name] = {'sections': list(sections), 'elf_paths_each': 80, 'all_hash_maps_identical': True}
    if name == 'r10d/elf-identity-final.txt':
        out['final_platform_elf_sha256'] = {k: v for k, v in values[0].items() if '/ledger/' in k}

rows = list(csv.DictReader((r / 'r10d/meas/groups-e59cf6ea.csv').open()))
assert len(rows) == 586
single, paired = rows[:578], rows[578:]
out['campaign'] = {'single_runs': len(single), 'paired_runs': 4, 'paired_group_rows': len(paired), 'points': {}}
for point, maximum in (('1x1', 155676), ('8x8-1if', 193036)):
    own = [x for x in single if x['point'] == point]
    failures = [f"{x['arm']}/{x['group']}" for x in own if int(x['rc'])]
    expected = sorted(f'{arm}/{group}' for arm in ('none', 'answering-ports') for group in ('srp-kept', 'srp-bound'))
    assert len(own) == 289 and sorted(failures) == expected
    assert max(int(x['longest_pass_cycles']) for x in own) == maximum
    assert all(int(x['over_statements']) == 0 for x in own)
    assert all(int(x['rc']) == 0 for x in paired if x['point'] == point)
    out['campaign']['points'][point] = {
        'single_runs': len(own), 'pair_required_nonzero': failures,
        'maxima_cycles': {k: max(int(x[k]) for x in own) for k in
                         ('longest_pass_cycles', 'polls_base', 'polls_walk', 'srp_slice', 'build_slice', 'round_slice')},
        'over_statements': 0}

gates = r / 'r10d/gates/final'
out['final_gate_receipts'] = {}
for f in sorted(gates.glob('*.txt')):
    lines = f.read_text().splitlines()
    out['final_gate_receipts'][f.name] = {'first_line': lines[0], 'last_lines': lines[-3:]}
for n in range(4):
    text = (gates / f'fwgate-shard{n}-25ff0632.txt').read_text()
    assert 'test_ctrl_firmware: PASS' in text and re.search(r'\[unit end .* rc 0\]', text)
out['focused_published_mutant_lines'] = []
for n in (1, 3):
    f = gates / f'fwgate-shard{n}-25ff0632.txt'
    for line_no, line in enumerate(f.read_text().splitlines(), 1):
        if re.search(r'\[ok\].*(drain-alone|zero-leave|zero.*Leave|sink-cap|keep-past-v|bound-sinks-uncounted|fallback|D6|D7|both-owed)', line):
            out['focused_published_mutant_lines'].append({'file': f.name, 'line': line_no, 'text': line})
out['routes'] = {}
for f in sorted((r / 'r10d/routes').glob('route-*.txt')):
    text = f.read_text()
    corners = re.findall(r'^(Slow_\w+|Fast_\w+): WNS ([+\d.]+) ns \(0 failing\), WHS ([+\d.]+) ns \(0 failing\)', text, re.M)
    assert len(corners) == 4 and all(float(w) >= .030 and float(h) >= 0 for _, w, h in corners)
    assert re.search(r'nets with routing errors\.+ :\s+0', text)
    out['routes'][f.name] = {'corners': corners, 'reported_routing_errors': 0}
out['packet_integrity_files'] = json.loads((p / 'packet-integrity.json').read_text())['checked']
print(json.dumps(out, indent=2))
