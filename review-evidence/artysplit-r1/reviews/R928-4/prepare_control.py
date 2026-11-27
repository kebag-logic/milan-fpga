#!/usr/bin/env python3
"""Remove only none/srp-bound from the census index; preserve all files."""
import hashlib, json, shutil, sys
from pathlib import Path
source, target = map(Path, sys.argv[1:])
shutil.copytree(source, target)
census = json.loads((target / 'census.json').read_text())
old = census['cases']
census['cases'] = [r for r in old if r['case'] != 'none/srp-bound']
assert len(old) == 147 and len(census['cases']) == 146
(target / 'census.json').write_text(json.dumps(census, indent=1) + '\n')
count = 0
for path in source.rglob('*'):
    if path.is_file() and path.name != 'census.json':
        assert hashlib.sha256(path.read_bytes()).digest() == hashlib.sha256((target / path.relative_to(source)).read_bytes()).digest()
        count += 1
assert (target / 'census/none/srp-bound/manifest.json').is_file()
print(f'PASS removed none/srp-bound index entry only; {count} other files byte-identical and retained')
