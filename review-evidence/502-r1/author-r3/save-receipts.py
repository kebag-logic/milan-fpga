from pathlib import Path
import hashlib
import json
import shutil

root = Path('/tmp/502-a345')
out = Path('$MANAGEMENT/2026-09-23/502-a345')
records = [json.loads(line) for line in (root / 'gates.jsonl').read_text().splitlines()]
(out / 'resume-gates.json').write_text(json.dumps(records, indent=2) + '\n')
for record in records:
    source = Path(record['log'])
    data = source.read_bytes()
    assert hashlib.sha256(data).hexdigest() == record['sha256']
    target = out / 'receipts' / ('resume-' + source.name)
    if len(data) <= 200000:
        target.write_bytes(data)
    else:
        (target.with_suffix('.tail.txt')).write_bytes(data[-60000:])
for name in ['priority-probe.py', 'export-tree.py', 'save-receipts.py']:
    shutil.copy2(root / name, out / name)
print(f'Saved {len(records)} bounded receipts and metadata.')
