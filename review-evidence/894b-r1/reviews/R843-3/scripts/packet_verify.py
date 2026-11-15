"""Verify the author packets of the evidence archive (argument: the extracted review-evidence/894b-r1 directory).

For author-r5 and author-r6: every INDEX.md row's bytes and sha256, with a mismatch accepted only where the archive's
MANIFEST.json records the file as path-redacted with the INDEX's sha256 as its original; then every MANIFEST.json
entry's published sha256 over the whole archive.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

base = Path(sys.argv[1])
manifest = {e['file']: e for e in json.loads((base / 'MANIFEST.json').read_text())}
for d in ('author-r5', 'author-r6'):
    rows = re.findall(r'^\| `([^`]+)` \| ([\d,]+) \| `([0-9a-f]{64})` \|$', (base / d / 'INDEX.md').read_text(), re.M)
    ok, redacted, bad = 0, [], []
    for f, size, h in rows:
        data = (base / d / f).read_bytes()
        if hashlib.sha256(data).hexdigest() == h and len(data) == int(size.replace(',', '')):
            ok += 1
            continue
        e = manifest.get(f'{d}/{f}')
        if e and e['path_redacted'] and e['original_sha256'] == h:
            redacted.append(f)
        else:
            bad.append(f)
    listed = {r[0] for r in rows}
    files = {str(p.relative_to(base / d)) for p in (base / d).rglob('*') if p.is_file()} - {'INDEX.md'}
    print(f'{d}: {len(rows)} indexed, {ok} byte-identical, {len(redacted)} path-redacted with the indexed original '
          f'sha256 {redacted}, {len(bad)} bad {bad}, unindexed {sorted(files - listed)}')
bad = [f for f, e in manifest.items() if (base / f).exists()
       and hashlib.sha256((base / f).read_bytes()).hexdigest() != e['published_sha256']]
print(f'MANIFEST.json: {len(manifest)} entries, {len(bad)} published sha256 mismatches')
