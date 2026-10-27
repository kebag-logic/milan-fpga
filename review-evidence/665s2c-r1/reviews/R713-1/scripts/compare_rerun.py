"""Compare a reviewer rerun's results with an archived arm: table.md byte for byte (against the head
regrade), each group's graded JSON (against the archived run), and the composed lines.
usage: compare_rerun.py RERUN_RESULTS ARCHIVED_RUN_DIR ARCHIVED_REGRADE_DIR"""
import hashlib
import json
import sys
from pathlib import Path
new, old, reg = map(Path, sys.argv[1:4])
t_new, t_reg = (new / 'table.md').read_bytes(), (reg / 'table.md').read_bytes()
print('table.md identical to the archived head regrade:', t_new == t_reg,
      hashlib.sha256(t_new).hexdigest()[:16], hashlib.sha256(t_reg).hexdigest()[:16])
same, diff = 0, []
for p in sorted(old.glob('*.json')):
    q = new / p.name
    if not q.is_file():
        diff.append((p.name, 'missing in rerun'))
    elif json.loads(q.read_text()) == json.loads(p.read_text()):
        same += 1
    else:
        diff.append((p.name, 'differs'))
print(f'graded group JSONs equal to the archive: {same}; differing or missing: {diff or "none"}')
for line in t_new.decode().splitlines():
    if line.startswith(('Composed maximum', 'Over the windows')):
        print(line)
