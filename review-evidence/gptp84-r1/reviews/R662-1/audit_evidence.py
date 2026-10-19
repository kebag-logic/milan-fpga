#!/usr/bin/env python3
"""Verify the downloaded pinned public receipts and their two indexes."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
sys.dont_write_bytecode = True

p = Path(__file__).resolve().parent
e = p / 'scratch/public-evidence'
r = e / 'author/receipts'
index = (r / 'INDEX.md').read_text()
rows = re.findall(r'^\| `([^`]+)` \| (\d+) \| `([0-9a-f]+)` \|$', index, re.M)
files = {str(f.relative_to(r)) for f in r.rglob('*') if f.is_file() and f.name != 'INDEX.md'}
assert files == {x[0] for x in rows}
for path, size, digest in rows:
    data = (r / path).read_bytes()
    assert len(data) == int(size) and hashlib.sha256(data).hexdigest().startswith(digest), path
manifest = json.loads((e / 'MANIFEST.json').read_text())
checked = 0
for row in manifest:
    f = e / row['file']
    if f.exists():
        assert hashlib.sha256(f.read_bytes()).hexdigest() == row['published_sha256'], row['file']
        checked += 1
root = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location('mutants', root / 'tb/verilator/engine/mutants.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
seen = []
for i in range(24):
    log = (r / f'lane-head/engine-mutants/mut-{i}.log').read_text()
    assert '[PASS] the unmutated engine still passes the harness' in log
    assert '4 checks: 4 PASS, 0 FAIL' in log
    for mutation in m.MUTATIONS[i*3:i*3+3]:
        name, _, _, _, breaks = mutation
        assert '[PASS] mutant caught: ' + name + ' - breaks ' in log, name
        if breaks.startswith(('#82 ', '#84 ', '#85 ', 'p1 255 ')):
            failed = [line for line in log.splitlines() if line.startswith('FAIL ')]
            assert all(any(w in line for line in failed) for w in breaks.split(' | ')), name
        seen.append(name)
assert len(seen) == len(set(seen)) == len(m.MUTATIONS) == 72
patch = (e / 'author/parent-adoption-gptp_shadow-85.patch').read_bytes()
assert patch == (r / 'parent-adoption/parent-adoption-gptp_shadow-85.patch').read_bytes()
out = {'receipt_index_files': len(rows), 'receipt_index_exact_match': True,
       'published_manifest_hashes_verified': checked,
       'exact_head_mutants_verified': len(seen),
       'mutation_positive_controls': 24,
       'named_failures_verified': True,
       'companion_copies_identical': True,
       'parent_gate_rc_rows': (r / 'parent-adoption/rc.txt').read_text().splitlines(),
       'builder_union': (r / 'parent-adoption/builder/union.txt').read_text().splitlines()}
(p / 'evidence-audit.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
