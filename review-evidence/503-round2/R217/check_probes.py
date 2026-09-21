import json
from pathlib import Path

p = Path(__file__).parent
data = json.loads((p / 'probe-results.json').read_text())
by_variant = {r['variant']: r for r in data}
for r in data:
    assert r['rc'] == 0 and r['completed'], r['variant']
for variant in ['', 'original-second-pass']:
    result = by_variant[variant]
    rows = result['snaps']['terminal']['rows']
    assert all(row[3] == 0 for row in rows), variant
    obs = result['obs']['restored']
    assert obs['restore_fail'] == 1
    assert obs['d3_rb'] == (variant == 'original-second-pass')
for variant, missing in [('header-repeat',5), ('header-balanced',5), ('descriptor-error',2), ('descriptor-timeout',2)]:
    result = by_variant[variant]
    obs = result['obs']['observed']
    assert obs['restore_done'] == 1 and obs['restore_fail'] == 0 and obs['entity_en'] == 1
    assert obs['rs_app'] == 9 and obs['d3_rb'] == 0
    rows = result['snaps']['terminal']['rows']
    assert next(row for row in rows if row[:2] == [missing,0])[3] == 0
    assert any(row[3] for row in rows)
    print('COUNTEREXAMPLE',variant,': partial restore, done=1 fail=0 enabled=1')
result = by_variant['header-pass0']
assert result['obs']['observed']['restore_fail'] == 1
assert result['obs']['observed']['d3_rb'] == 1
assert all(row[3] == 0 for row in result['snaps']['terminal']['rows'])
result = by_variant['descriptor-initial-error']['obs']['observed']
assert result['desc_valid'] == 0 and result['restore_fail'] == 0 and result['entity_en'] == 1
assert result['rs_app'] == 0 and result['rs_ref'] == 10
print('COUNTEREXAMPLE descriptor-initial-error: unvalidated image, done=1 fail=0 enabled=1')
print('Original payload faults contained; header-pass0-only control rolls back; five adjacent counterexamples confirmed.')
