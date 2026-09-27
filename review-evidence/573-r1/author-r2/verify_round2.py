"""Check artifact identity and actual mutation outcomes, including old probes."""
from pathlib import Path
import json

ROOT = Path('/tmp/573-a352')
OUT = Path(__file__).resolve().parent
before = json.loads((ROOT/'hashes-base.json').read_text())
after = json.loads((ROOT/'hashes-head.json').read_text())
assert len(before) == len(after) == 85
assert before == after, 'shipping artifact drift'
assert len({r['configuration'] for r in before}) == 5
for name, count in [('review-mutants-340',30),('round2-mutants-result',8)]:
    rows = json.loads((ROOT/f'{name}.json').read_text())
    cases = rows[:-2]
    assert len(cases) == count
    assert all(c['verdict'] == 'KILLED' for c in cases), cases
    assert rows[-2]['returncode'] == 0 and rows[-1]['identical'] is True
    if count == 8:
        crf = next(c for c in cases if c['id'] == 'CRF output arm removed')
        assert crf['last_line'] == 'AssertionError: CRF output accepted without INTERNAL'
rows = json.loads((ROOT/'review-mutants-341.log').read_text())
assert rows['restored_control_returncode'] == 0
applied = [c for c in rows['cases'] if c['applied']]
assert len(applied) == 26 and all(c['verdict'] == 'KILLED' for c in applied)
missing = [c['case'] for c in rows['cases'] if not c['applied']]
assert len(missing) == 2 and missing[0].startswith('R-M8 ') and missing[1].startswith('R-M14 ')
probe = (ROOT/'review-format-length.log').read_text()
receipt = json.loads((OUT/'review-format-length.result.json').read_text())
assert receipt['returncode'] == 1
assert 'final formats=46: loader ACCEPTED' in probe and 'descriptor length 506 octets' in probe
assert 'ConfigError: streams.talkers[0].formats: format count 47 exceeds 46' in probe
assert 'final formats=47: loader ACCEPTED' not in probe
print('PASS: 85/85 shipping artifacts identical across five configurations.')
print('PASS: 30 + 26 applicable original mutants and eight round-2 mutants killed.')
print('PASS: all mutation sources restored and every restored control returns 0.')
print('PASS: CRF-output removal detected by its direct behavioral control.')
print('Historical probe: raw rc 1 is the required 47-format refusal; unchanged.')
print('Historical patterns R-M8/R-M14 target the removed literal cap; unchanged.')
