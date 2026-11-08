"""gen_index.py <output-dir>: receipts/INDEX.md generated from the files present, with size and SHA-256 of each."""
import hashlib
import sys
from pathlib import Path

root = Path(sys.argv[1])
rows = []
for path in sorted(p for p in root.rglob('*') if p.is_file() and p.name != 'INDEX.md'):
    data = path.read_bytes()
    rows.append(f'| `{path.relative_to(root)}` | {len(data)} | `{hashlib.sha256(data).hexdigest()[:16]}` |')
(root / 'receipts' / 'INDEX.md').write_text('# Receipts index\n\nGenerated from the files present.\n\n| File | Bytes | SHA-256 (first 16) |\n|---|---:|---|\n'
                                            + '\n'.join(rows) + '\n')
print(len(rows), 'files')
