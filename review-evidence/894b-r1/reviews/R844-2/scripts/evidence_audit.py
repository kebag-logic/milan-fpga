"""Check published receipts. Usage: evidence_audit.py CHECKOUT ARCHIVE_ROOT."""
import collections
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

root, archive = map(Path, sys.argv[1:3])
rows = json.loads((archive / 'MANIFEST.json').read_text())
selected = [r for r in rows if r['file'].startswith(('author-r3/', 'author-r4/'))]
for r in selected:
    p = archive / r['file']
    assert hashlib.sha256(p.read_bytes()).hexdigest() == r['published_sha256'], r['file']
print(f'PASS: {len(selected)} author receipt files match the published manifest; reviewer files not opened')
a = archive / 'author-r4'
indexed = re.findall(r'^\| `([^`]+)` \| [\d,]+ \| `([0-9a-f]{64})` \|$',
                     (a / 'INDEX.md').read_text(), re.M)
redactions = {r['file']: r for r in selected}
for name, digest in indexed:
    data = (a / name).read_bytes()
    if hashlib.sha256(data).hexdigest() != digest:
        r = redactions['author-r4/' + name]
        assert r['path_redacted'] and r['original_sha256'] == digest, name
print(f'PASS: {len(indexed)} index entries match original hashes or manifest-declared redactions')
commit = subprocess.check_output(['git', '-C', str(root), 'cat-file', 'commit',
                                 '843c40b1e9249d89862a9174da7e2b4c32c300d1'])
print('Archive signature header:', b'\ngpgsig ' in commit)
images = a / 'receipts/images'
base = (archive / 'author-r3/receipts/images/raw-4-fullpass-716a8ae7.txt').read_text()
def digests(text):
    return re.findall(r'^(\S+):.*?elf sha256 ([0-9a-f]{64}), loadable sha256 ([0-9a-f]{64})', text, re.M)
assert len(digests(base)) == 8
for name in ('raw-0-base-716a8ae7.txt', 'raw-1-comments.txt', 'raw-2-guard.txt', 'raw-3-final-98c0b62b.txt'):
    assert digests((images / name).read_text()) == digests(base), name
    print(f'PASS: {name}: eight ELF and loadable hash pairs match round 3')
wf = (a / 'receipts/gates/workflows-verify-98c0b62b.md').read_text()
counts = collections.Counter()
for line in wf.splitlines():
    if line.startswith('| ') and not line.startswith('| Workflow'):
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if len(cells) == 6:
            counts[cells[4]] += 1
print('Workflow receipt row counts:', dict(counts))
assert counts == {'0': 139, 'NOT RUN': 226}, counts
lane = (a / 'receipts/gates/lane-gates-98c0b62b.txt').read_text()
results = re.findall(r'^(\S+) rc=(\d+):', lane, re.M)
assert len(results) == 59
expected = {'rows_tiers_report_exits_1', 'flip_check_exits_1', 'flip_check_1x1_as_built_exits_1',
            'flip_check_8x8_exits_1'}
assert {n for n, rc in results if rc != '0'} == expected
assert all(rc == '1' for n, rc in results if n in expected)
print('PASS: 59 lane receipts; 55 rc 0; four named design exits:', ', '.join(sorted(expected)))
legs = a / 'receipts/regrade/legs-r3'
groups = budgets = refusals = 0
for name in ('C-A0', 'C-A1', 'C-A2', 'C-A3', 'C-AE', 'C-AL'):
    text = (legs / (name + '.log')).read_text()
    s = re.findall(r'^(\d+) groups graded, (\d+) refusals, (\d+) budget misses', text, re.M)
    assert len(s) == 1 and s[0][1] == '0'
    g, r, b = map(int, s[0])
    assert len(re.findall(r'^BUDGET ', text, re.M)) == b
    assert len(re.findall(r'^END rc=0\b', text, re.M)) == 1
    assert not re.search(r'^(STATED|REFUSED) ', text, re.M)
    groups += g
    budgets += b
    refusals += r
    print(f'{name}: {g} groups, {r} refusals, {b} budget lines, rc 0')
assert (groups, budgets, refusals) == (112, 7, 0)
print('PASS: six legs, 112 groups, seven recorded misses, zero refusals')
