"""Verify every `| path | bytes | sha256 |` row of an INDEX.md against files under a root."""
import hashlib, re, sys
from pathlib import Path
index, root = Path(sys.argv[1]), Path(sys.argv[2])
row = re.compile(r"^\| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|")
ok = bad = 0
listed = set()
for line in index.read_text().splitlines():
    m = row.match(line)
    if not m:
        continue
    rel, size, digest = m.group(1), int(m.group(2)), m.group(3)
    listed.add(rel)
    f = root / rel
    if not f.is_file():
        print("MISSING", rel); bad += 1; continue
    data = f.read_bytes()
    if len(data) != size or hashlib.sha256(data).hexdigest() != digest:
        print("MISMATCH", rel); bad += 1
    else:
        ok += 1
present = {str(p.relative_to(root)) for p in (root / "receipts").rglob("*") if p.is_file()}
unlisted = sorted(present - listed - {"receipts/INDEX.md"})
print(f"rows ok={ok} bad={bad} unlisted_files={len(unlisted)}")
for u in unlisted[:20]:
    print("UNLISTED", u)
sys.exit(1 if bad else 0)
