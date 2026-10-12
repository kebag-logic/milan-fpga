#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Regrade published, exact-head gate and mutation receipts."""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

p = argparse.ArgumentParser()
p.add_argument('--repo', type=Path, required=True)
p.add_argument('--hosted', type=Path, required=True)
p.add_argument('--author', type=Path, required=True)
p.add_argument('--out', type=Path, required=True)
a = p.parse_args()
plants = json.loads((a.repo / 'tests/mutations.json').read_text())
snapshot = json.loads((a.author / 'round2/tree-sha256.json').read_text())
for name, digest in snapshot.items():
    assert hashlib.sha256((a.repo / name).read_bytes()).hexdigest() == digest, name
gates = json.loads((a.hosted / 'gates.json').read_text())
assert len(gates) == 28 and all(g['rc'] == 0 for g in gates)
for gate in gates:
    assert (a.hosted / (gate['gate'] + '.rc')).read_text().strip() == '0'

def parse_xml(file):
    root = ET.parse(file).getroot()
    cases = root.findall('.//testcase')
    assert root.tag == 'testsuites'
    assert int(root.get('tests')) == len(cases)
    assert int(root.get('disabled', '0')) == int(root.get('errors', '0')) == 0
    names, failures = set(), {}
    for case in cases:
        name = case.get('classname') + '.' + case.get('name')
        assert name not in names
        names.add(name)
        assert case.get('status') == 'run' and case.get('result') == 'completed'
        assert case.find('skipped') is None and case.find('error') is None
        failed = case.findall('failure')
        if failed:
            failures[name] = '\n'.join(f.get('message', '') for f in failed)
    assert int(root.get('failures')) == len(failures)
    return names, failures

markers = json.loads((a.hosted / 'mutations/message-markers.json').read_text())
summary = json.loads((a.hosted / 'mutations/results.json').read_text())
assert {r['name'] for r in summary} == {m['name'] for m in plants}
assert len(summary) == len(plants) == 365
assert all(r['status'] == 'CAUGHT' and r['rc'] == 1 for r in summary)
mutation_rows = []
for m in plants:
    files = sorted((a.hosted / 'mutations' / m['name']).glob('*.xml'))
    assert files, m['name']
    failures = []
    for file in files:
        _, failed = parse_xml(file)
        failures.extend((file.stem, name, text) for name, text in failed.items())
    for kill in m['kills']:
        matched = False
        for arm, name, text in failures:
            if 'arm' in kill and kill['arm'] != arm:
                continue
            if name != kill['test'] and not (kill['test'].endswith('/') and name.startswith(kill['test'])):
                continue
            begin, end = ('\n' + marker + '\n' for marker in markers)
            chunks = []
            while begin in text:
                _, _, text = text.partition(begin)
                body, found, text = text.partition(end)
                assert found
                chunks.append(body)
            matched |= kill['needle'] in '\0'.join(chunks)
        assert matched, (m['name'], kill)
    mutation_rows.append(dict(plant=m['name'], xml_files=len(files), named_assertions_verified=len(m['kills'])))

def complete(directory):
    files = sorted((directory / 'xml').glob('*.xml'))
    assert len(files) == 8
    names, failures = set(), {}
    for file in files:
        ns, fs = parse_xml(file)
        names.update((file.stem, n) for n in ns)
        failures.update(fs)
    return names, failures

suite = a.author / 'round2/complete-suite'
baseline, failures = complete(suite / 'baseline')
assert len(baseline) == 418 and not failures
focused = [m for m in plants if m['name'].startswith('dafresh-') or m['name'] == 'x-zero-never-expires']
for m in focused:
    killer = m['kills'][0]
    full, failures = complete(suite / m['name'] / 'full')
    assert full == baseline and set(failures) == {killer['test']}
    assert killer['needle'] in failures[killer['test']]
    removed, failures = complete(suite / m['name'] / 'removed')
    assert removed == {key for key in baseline if key[1] != killer['test']}
    assert len(removed) == 417 and not failures

result = dict(snapshot_files_verified=len(snapshot), hosted_gates_verified=len(gates),
              hosted_mutations_regraded=len(mutation_rows), named_assertions_verified=sum(r['named_assertions_verified'] for r in mutation_rows),
              published_complete_suite_proofs_regraded=len(focused), complete_binaries=8,
              complete_tests=418, removed_tests=417, errors=[], mutations=mutation_rows)
a.out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k:v for k,v in result.items() if k != 'mutations'}, indent=2))
