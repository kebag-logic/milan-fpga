from pathlib import Path
import hashlib

root = Path(__file__).resolve().parent
lines = ['# Receipt and artifact index', '', '| Relative file | Bytes | SHA-256 |', '|---|---:|---|']
for path in sorted(root.rglob('*')):
    if not path.is_file() or path == root / 'INDEX.md':
        continue
    data = path.read_bytes()
    if len(data) > 200_000:
        raise SystemExit(f'File exceeds output limit: {path.relative_to(root)}')
    lines.append(f'| {path.relative_to(root)} | {len(data)} | `{hashlib.sha256(data).hexdigest()}` |')
(root / 'INDEX.md').write_text('\n'.join(lines) + '\n')
print(f'Indexed {len(lines) - 4} files; each below 200 KB.')
