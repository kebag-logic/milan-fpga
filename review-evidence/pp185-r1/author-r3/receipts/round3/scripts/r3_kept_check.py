"""usage: r3_kept_check.py <receipts-dir> <index-before-round-3>
Every file the round-2 receipts index lists must still be present and byte-identical, and
every file not in it must be under round3/. rc 1 otherwise."""
import hashlib
import re
import sys
from pathlib import Path

root, index = Path(sys.argv[1]), Path(sys.argv[2])
d, listed = None, {}
for line in index.read_text().splitlines():
    if line.startswith("## Over"):
        d = None
    elif line.startswith("## ") and line.endswith("/"):
        d = line[3:-1]
    elif d is not None and (m := re.match(r"\| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|", line)):
        listed[(Path(d) / m.group(1)).as_posix()] = m.group(3)
bad = 0
for rel, h in sorted(listed.items()):
    p = root / rel
    got = hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "absent"
    if got != h:
        bad += 1
        print(f"CHANGED {rel}")
present = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and p.name != "INDEX.md"}
new = sorted(present - set(listed))
outside = [n for n in new if not n.startswith("round3/")]
print(f"round-2 index sha256 {hashlib.sha256(index.read_bytes()).hexdigest()}")
print(f"{len(listed)} files listed in the round-2 index: {len(listed) - bad} byte-identical, {bad} changed or absent")
print(f"{len(new)} files not in it, {len(outside)} of them outside round3/" + (f": {outside}" if outside else ""))
sys.exit(1 if bad or outside else 0)
