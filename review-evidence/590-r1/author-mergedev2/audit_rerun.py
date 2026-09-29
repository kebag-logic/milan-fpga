"""Re-hash the continuation's native evidence and regrade logs; check the packet's size rule."""
from pathlib import Path
import gzip
import hashlib
import json

out = Path(__file__).parent
artifacts = json.loads((out / 'native-artifacts.json').read_text())
for item in artifacts:
    body = b''
    for stored in item['stored']:
        raw = (out / stored['path']).read_bytes()
        assert len(raw) == stored['size'] and hashlib.sha256(raw).hexdigest() == stored['sha256'], stored['path']
        body += raw
    if item['name'].endswith('.gz'):
        body = gzip.decompress(body)
    assert len(body) == item['raw_size'] and hashlib.sha256(body).hexdigest() == item['raw_sha256'], item['name']
regrades = json.loads((out / 'native-regrades.json').read_text())
for row in regrades:
    stored = (out / row['path']).read_bytes()
    assert len(stored) == row['stored_size'] and hashlib.sha256(stored).hexdigest() == row['stored_sha256']
    raw = gzip.decompress(stored) if row['path'].endswith('.gz') else stored
    assert len(raw) == row['size'] and hashlib.sha256(raw).hexdigest() == row['sha256'], row['path']
commands = json.loads((out / 'native-commands.json').read_text())
large = [str(p) for p in out.rglob('*') if p.is_file() and p.stat().st_size > 200000]
assert not large, large
summary = dict(native_artifacts=len(artifacts), native_commands=len(commands),
               failing_commands=[c['name'] for c in commands if c['rc'] != 0],
               heads=sorted({c['head'] for c in commands} | {r['head'] for r in regrades}),
               regrades=len(regrades), failing_regrades=[r['name'] for r in regrades if r['rc'] != 0],
               gzip_stored=sorted(item['name'] for item in artifacts if item['name'].endswith('.gz'))
               + sorted(r['path'] for r in regrades if r['path'].endswith('.gz')),
               large_files=large)
(out / 'audit-rerun.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(dict((k, v) for k, v in summary.items() if k != 'gzip_stored')))
