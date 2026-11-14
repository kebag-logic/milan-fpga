"""Check every row of a packet INDEX.md (| `file` | bytes | `sha256` |) against the files beside it, and list unindexed files."""
import hashlib, re, sys
from pathlib import Path
root = Path(sys.argv[1]); bad = 0; seen = set()
for m in re.finditer(r"^\| `([^`]+)` \| ([\d,]+) \| `([0-9a-f]{64})` \|$", (root / "INDEX.md").read_text(), re.M):
    f = root / m[1]; seen.add(m[1]); b = f.read_bytes()
    ok = len(b) == int(m[2].replace(",", "")) and hashlib.sha256(b).hexdigest() == m[3]
    bad += not ok; print(("ok  " if ok else "BAD ") + m[1])
extra = sorted(str(p.relative_to(root)) for p in root.rglob("*") if p.is_file() and str(p.relative_to(root)) not in seen | {"INDEX.md"})
print(f"rows {len(seen)} bad {bad} unindexed {extra}")
sys.exit(1 if bad or extra else 0)
