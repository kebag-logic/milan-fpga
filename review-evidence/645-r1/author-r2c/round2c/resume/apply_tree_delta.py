"""Bring an external source export from one lane commit to another by
writing the changed blobs (no checkout): A/M write, D delete, R move."""
import os
import subprocess
import sys
from pathlib import Path

lane = Path('$LANES/645-ring-slip')
old, new, roots = sys.argv[1], sys.argv[2], [Path(p) for p in sys.argv[3:]]
rows = subprocess.check_output(['git', '-C', str(lane), 'diff', '--name-status', '-z', '--no-renames', old, new]).split(b'\0')
items = []
it = iter(filter(None, rows))
for status in it:
    items.append((status.decode(), next(it).decode()))
for root in roots:
    for status, path in items:
        target = root / path
        if status == 'D':
            target.unlink()
            continue
        mode, kind, sha = subprocess.check_output(['git', '-C', str(lane), 'ls-tree', new, '--', path], text=True).split('\t')[0].split()
        assert kind == 'blob', (path, kind)
        data = subprocess.check_output(['git', '-C', str(lane), 'cat-file', 'blob', sha])
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.is_symlink() or target.exists():
            target.unlink()
        if mode == '120000':
            os.symlink(data.decode(), target)
        else:
            target.write_bytes(data)
            os.chmod(target, 0o755 if mode == '100755' else 0o644)
    print(root, len(items), 'paths applied')
