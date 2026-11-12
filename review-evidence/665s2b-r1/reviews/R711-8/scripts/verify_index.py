"""Reviewer check (R711-8): every row of the author packet's receipts/INDEX.md against the archived bytes, and every
archived file listed. Run: python3 -I <this> <packet root, the directory holding HANDOFF.md>."""
import hashlib, re, sys
from pathlib import Path
root = Path(sys.argv[1])
rows = re.findall(r'^\| `([^`]+)` \| ([\d,]+) \| `([0-9a-f]{64})` \|$', (root / 'receipts/INDEX.md').read_text(), re.M)
bad = [p for p, n, h in rows if not (root / p).is_file() or (root / p).stat().st_size != int(n.replace(',', ''))
       or hashlib.sha256((root / p).read_bytes()).hexdigest() != h]
listed = {p for p, _, _ in rows}
files = {str(f.relative_to(root)) for f in root.rglob('*') if f.is_file()}
print(f'rows {len(rows)}, bad {len(bad)}, unlisted {sorted(files - listed - {"receipts/INDEX.md"})[:10]}', bad[:5])
