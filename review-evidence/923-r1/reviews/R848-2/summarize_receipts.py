#!/usr/bin/env python3
"""Retain the public receipts used by this delta review and check their stated totals and identity links."""
import collections
from pathlib import Path
import re
import shutil

packet = Path(__file__).resolve().parent
source = packet / 'scratch/public-author'
dest = packet / 'public-evidence'
paths = []
paths += list((source / 'author-r3/receipts').rglob('*.txt'))
paths += [source / 'author-r3/receipts/workflows/README.md',
          source / 'author-r3/receipts/workflows/verify-d06ded5a.md']
paths += list((source / 'author-r2/receipts/sweep').glob('*.txt'))
paths += list((source / 'author-r2/receipts/route').glob('head-*/signoff.txt'))
paths += list((source / 'author-r2/receipts/route').glob('head-*/bitstream.sha256'))
paths += [source / p for p in (
    'author-r2/receipts/twin/twin-maps-70c100da.txt',
    'author-r2/receipts/budget/record-classes-every-leg-both-points.txt',
    'author-r2/receipts/budget/edits-and-classes-answering-1x1-head.txt',
    'author-r1/receipts/release/IMAGES-base.sha256',
    'author-r1/receipts/release/IMAGES-head.sha256',
    'author-r1/receipts/rom/images-base-16ba667d.txt',
    'author-r1/receipts/rom/images-head-def26a61.txt')]
for path in paths:
    # Keep receipts, not environment-specific runner copies.
    if path.name in ('run_wf.py.txt', 'verify_wf.py.txt', 'wf_batch.sh.txt', 'some_plants.py.txt'):
        continue
    target = dest / path.relative_to(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, target)

table = (source / 'author-r3/receipts/workflows/verify-d06ded5a.md').read_text()
rows = [line.split('|') for line in table.splitlines() if line.startswith('| ')][1:]
counts = collections.Counter(row[5].strip() for row in rows)
assert counts == {'0': 118, 'NOT RUN': 130}, counts
print('Published workflow table independently counted:', dict(counts))
print('Campaign totals are author attestations in the companion receipt: AECP 331, SRP 421, control 716; coverage 39 files.')
print('The table contains step results, not the full referenced job logs. No manager source execution is inferred.')
suites = checks = 0
for p in (source / 'author-r2/receipts/sweep').glob('*.txt'):
    text = p.read_text()
    suites += int(re.search(r'suites: (\d+)\s+passed:', text)[1])
    checks += int(re.search(r'checks: (\d+)', text)[1])
    assert 'failed: 0   timed out: 0' in text and '"exit_code": 0' in text
assert (suites, checks) == (65, 2713040)
print('Prior sweep receipts independently counted:', suites, 'suites;', checks, 'checks; all exits 0.')
identity = (source / 'author-r3/receipts/images/IDENTITY.txt').read_text()
for shape, expected in [('1x1', 'caec0abc5d730cbeeb4c82a628406ed51161a2ccb783523afc90d20004c0587d'),
                        ('8x8', '59b9b736f410e2b2de2f8e7bd27d21f3ee16870081c778fa296e6cf3149c84cd')]:
    assert f'{shape}/1if  d06ded5a {expected}' in identity
    assert f'{shape}/1if  70c100da {expected}' in identity
    for path in (source / 'author-r2/receipts/route').glob(f'head-{shape}-*/bitstream.sha256'):
        assert expected in path.read_text(), path
    print(shape, 'published platform image hashes match source/prior/routed receipts:', expected)
for digest in ('860d4771decf5b92bd167e57c690892d665eec8075902a3468b68e3b3f56041f',
               'd8851b6d470e811cfd1c95b3aa3a6d3e9c367f3e1fddaac38270d484291aea99'):
    assert f'd06ded5a {digest}' in identity
    for label in ('base', 'head'):
        assert digest in (source / f'author-r1/receipts/release/IMAGES-{label}.sha256').read_text()
    print('Published release bios.bin hash chain matches:', digest)
print('Image bytes were not rebuilt or independently hashed here; the public receipt hash chains were checked.')
