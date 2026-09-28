"""Re-hash every recorded log of this round and check the packet's size rule."""
from pathlib import Path
import hashlib
import json

out = Path(__file__).parent
records = []
for receipt in ('gates.json', 'regrade-gates.json', 'probes.json', 'builder-gates.json'):
    for row in json.loads((out / receipt).read_text()):
        parts = row['stored'] if 'stored' in row else [dict(path=row['path'], size=row['size'], sha256=row['sha256'])]
        for stored in parts:
            raw = (out / stored['path']).read_bytes()
            assert len(raw) == stored['size'] and hashlib.sha256(raw).hexdigest() == stored['sha256'], stored['path']
        records.append(dict(receipt=receipt, name=row['name'], rc=row['rc']))
large = [str(p) for p in out.rglob('*') if p.is_file() and p.stat().st_size > 200000]
assert not large, large
summary = dict(records=len(records), failing=[r['name'] for r in records if r['rc'] != 0], large_files=large)
(out / 'audit.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
