"""Check final receipt outcomes without promoting them to review verdicts."""
import json
from pathlib import Path

out = Path(__file__).resolve().parent
results = [json.loads(line) for line in (out / 'gate-results.jsonl').read_text().splitlines()]
required = {
    'builder-present', 'builder-absent', 'declarations', 'descriptor-audit',
    'aem-store-selftest', 'rtl-lint', 'python-idiom', 'naming', 'docs-git',
    'docs-no-git', 'em-dash', 'doc-style', 'toc', 'anchors', 'doc-paths',
    'diff-worktree', 'diff-branch', 'reviewer-round2-probes',
    'reviewer-scalar-spellings', 'reviewer-internal-mutants',
    'reviewer-external-mutants', 'author-mutants', 'archive-integrity',
    'historical-internal-probes', 'historical-buffer-wrap',
    'historical-bypass-probes', 'historical-format-boundary',
    'historical-internal-mutants', 'historical-external-mutants',
    'artifacts-base', 'artifacts-head', 'shipping-base', 'shipping-head',
}
assert required <= {row['gate'] for row in results}
assert all(row['returncode'] == 0 for row in results)
for label in ('base', 'head'):
    assert len(json.loads((out / f'artifacts-{label}.json').read_text())) == 85
    assert len((out / f'shipping-{label}.sha256').read_text().splitlines()) == 80
assert (out / 'artifacts-base.json').read_bytes() == (out / 'artifacts-head.json').read_bytes()
assert (out / 'shipping-base.sha256').read_bytes() == (out / 'shipping-head.sha256').read_bytes()
for row in json.loads((out / 'round2-probes.json').read_text()):
    assert row.get('resolved_equals_written_hex') is not False
    if row.get('yaml_type') in ('int', 'bool'):
        assert row['loader'] == 'refused' and 'quote' in row['reason']
scalar_rows = [json.loads(line) for line in (out / 'reviewer-scalar-spellings.log').read_text().splitlines()]
assert len(scalar_rows) == 15
assert all(row['equal'] or 'quote' in row['unquoted'] for row in scalar_rows)
for name in ('author-mutants.json', 'internal-mutants.json', 'historical-internal-mutants.json'):
    rows = json.loads((out / name).read_text())
    assert rows[-2]['returncode'] == 0 and rows[-1]['identical']
    for row in rows[:-2]:
        if row.get('applied') is False or row.get('expect') == 'PROBE':
            continue
        assert row['verdict'] == 'KILLED'
for name in ('reviewer-external-mutants.log', 'historical-external-mutants.log'):
    result = json.loads((out / name).read_text())
    assert result['restored_control_returncode'] == 0
    assert all(row.get('applied') is False or row['verdict'] == 'KILLED'
               for row in result['cases'])
for row in json.loads((out / 'audit-l4-probes.json').read_text()):
    if 'formats at 2021' in row['probe'] or 'formats above 2021' in row['probe']:
        assert row['result'] == 'accepted'
assert 'ALL GATES PASS EXCEPT 1 NOT RUN' in (out / 'builder-present.log').read_text()
absent = (out / 'builder-absent.log').read_text()
assert 'Absent-mode compiler probes blocked:' in absent
assert 'ALL GATES PASS EXCEPT' in absent and 'SKIP: the compiled CSR-address census' in absent
assert 'format count 47 exceeds 46' in (out / 'format-reproducer-raw.log').read_text()
assert all(p.stat().st_size <= 200000 for p in out.rglob('*') if p.is_file())
print(f'{len(required)} required receipt groups returned zero.')
print('Artifact equality: 85/85 inventory entries and 80/80 CLI entries.')
print('Current scalar outcomes, required mutations and restored controls verified.')
print('Expected raw historical exit 1 and optional null-source PROBE survivor remain explicit.')
