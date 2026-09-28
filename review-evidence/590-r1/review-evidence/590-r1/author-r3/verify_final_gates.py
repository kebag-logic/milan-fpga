"""Verify final-head gate records and the bytes retained for every gate."""
from pathlib import Path
import gzip
import hashlib
import json
import subprocess

out = Path(__file__).parent
root = Path('$LANES/590-592-599-firmware')
head = subprocess.check_output(['rtk', 'proxy', 'git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
count = 0
manifests = []
for filename in ('final-builder-gates.json', 'final-gates.json', 'final-target-gates.json',
                 'final-probes.json'):
    path = out / filename
    for entry in json.loads(path.read_text()):
        assert entry['head'] == head and entry['rc'] == 0, entry['name']
        if 'stored' in entry:
            parts = []
            for item in entry['stored']:
                data = (out / item['path']).read_bytes()
                assert len(data) == item['size']
                assert hashlib.sha256(data).hexdigest() == item['sha256']
                parts.append(data)
            raw = b''.join(parts)
            if '.gz' in entry['stored'][0]['path']:
                raw = gzip.decompress(raw)
        else:
            raw = Path(entry['path']).read_bytes()
        assert len(raw) == entry['size'], entry['name']
        assert hashlib.sha256(raw).hexdigest() == entry['sha256'], entry['name']
        count += 1
    manifests.append(dict(path=filename, size=path.stat().st_size,
                          sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
for path in out.rglob('*'):
    if path.is_file():
        assert path.stat().st_size <= 200000, path
result = dict(head=head, gates=count, rc=0, manifests=manifests)
(out / 'final-audit.json').write_text(json.dumps(result, indent=2) + '\n')
print(f'PASS: {count} final-head gates and retained log bindings')
