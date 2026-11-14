"""Lane 897's receipts: scrub host paths from every text receipt, refuse a file over 200 KB, and write INDEX.md from
the files present (name, size, sha256). usage: receipts.py OUTPUT_DIR"""
import hashlib, re, sys
from pathlib import Path
out = Path(sys.argv[1]); rec = out / 'receipts'
SUBS = [('$LANES/897-a776-r3-shard', '<shard-clone>'), ('$LANES/897-a776-r2-shard', '<shard-clone>'), ('/tmp/<session-tmp>', '<tmp>'), ('/data-2/milan/tmp/665s2b-a683zo', '<round-30-scratch>'),('/data-2/milan/tmp/897-a776', '<scratch>'), ('$LANES/897-aspath', '<worktree>'),
        ('$VALIDATION_STORAGE/665s2b-a683zn-legs', '<round-29-legs>'), ('/data-2/milan/tmp/665s2b-a683zn', '<round-29-scratch>'),
        ('$VALIDATION_STORAGE/665s2b-a683zn-gates', '<round-29-gates>'), ('$VALIDATION_TOOLS', '<tools>'),
        ('$VALIDATION_STORAGE/scratch', '<tools>'), ('$MANAGEMENT', '<management>'),
        ('$WORKSPACE_HOME', '<home>')]
bad = []
for f in sorted(p for p in rec.rglob('*') if p.is_file()):
    if f.stat().st_size > 200_000:
        bad.append(f'{f}: {f.stat().st_size} B over 200 KB')
        continue
    try:
        t = f.read_text()
    except UnicodeDecodeError:
        continue
    s = t
    for a, b in SUBS:
        s = s.replace(a, b)
    s = re.sub(r'\balex\b', '<account>', s)
    if s != t:
        f.write_text(s)
    if re.search(r'(?<![<\w])/(home|data|data-2)/', s):
        bad.append(f'{f}: a host path remains')
rows = ['# Receipts index (generated from the files present by receipts.py)', '', '| File | Bytes | sha256 |', '|---|---:|---|']
for f in sorted(p for p in rec.rglob('*') if p.is_file() and p.name != 'INDEX.md'):
    rows.append(f'| `{f.relative_to(out)}` | {f.stat().st_size} | `{hashlib.sha256(f.read_bytes()).hexdigest()}` |')
(rec / 'INDEX.md').write_text('\n'.join(rows) + '\n')
print('\n'.join(bad) if bad else f'{len(rows) - 4} files indexed, no host path, none over 200 KB')
sys.exit(1 if bad else 0)
