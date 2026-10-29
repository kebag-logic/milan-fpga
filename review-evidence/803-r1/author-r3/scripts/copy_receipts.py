"""copy_receipts.py <dest-dir> <file> [...]: copy small text receipts with host paths redacted (<scratch>, <tools>,
<home>); a file over 200 KB is not copied but its SHA-256 and size go to <dest>/large.sha256. Logs of a directory are
recorded by digest only: pass `--digest <dir>` to write <dest>/<name>.sha256 for every file below <dir>."""
import hashlib
import sys
from pathlib import Path

REDACT = (('$VALIDATION_STORAGE/scratch/803-a693c', '<scratch>'), ('$VALIDATION_STORAGE/scratch/803-a693', '<round1-scratch>'),
          ('$VALIDATION_STORAGE/scratch', '<scratch-root>'), ('$VALIDATION_TOOLS', '<tools>'), ('$LANES', '<lanes>'),
          ('$VALIDATION_STORAGE', '<tmp>'), ('$WORKSPACE_HOME', '<home>'))
dest = Path(sys.argv[1]); dest.mkdir(parents=True, exist_ok=True)
args = sys.argv[2:]
i = 0
while i < len(args):
    if args[i] == '--digest':
        root = Path(args[i + 1]); i += 2
        rows = []
        for f in sorted(p for p in root.rglob('*') if p.is_file()):
            data = f.read_bytes()
            rows.append(f'{hashlib.sha256(data).hexdigest()}  {len(data)}  {f.relative_to(root)}')
        (dest / (root.name + '.sha256')).write_text('\n'.join(rows) + '\n')
        continue
    f = Path(args[i]); i += 1
    data = f.read_bytes()
    if len(data) > 200 * 1024:
        with open(dest / 'large.sha256', 'a') as h:
            h.write(f'{hashlib.sha256(data).hexdigest()}  {len(data)}  {f.name}\n')
        continue
    text = data.decode(errors='replace')
    for a, b in REDACT:
        text = text.replace(a, b)
    (dest / f.name).write_text(text)
