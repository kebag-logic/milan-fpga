#!/usr/bin/env python3
"""index3.py <receipts dir> - the receipts' indexes, generated from the files present: receipts/INDEX.md for round 1's
areas (every top-level area but r2 and r3) and receipts/r2/INDEX.md and receipts/r3/INDEX.md for theirs, each file with
its size and its first line; the top index names the two round indexes. Split so that no index is over 200 KB."""
import sys
from pathlib import Path
root = Path(sys.argv[1])
def rows(files, base):
    out = ["| File | Bytes | First line |", "|---|---|---|"]
    for p in files:
        first = p.read_text(errors="replace").splitlines()[0][:100].replace("|", "/") if p.stat().st_size else ""
        out.append(f"| `{p.relative_to(base)}` | {p.stat().st_size} | {first} |")
    return out
for sub in ("r2", "r3"):
    d = root / sub
    files = sorted(x for x in d.rglob("*") if x.is_file() and x.name != "INDEX.md")
    text = [f"# Receipts index, {'round 2' if sub == 'r2' else 'round 3'}", "",
            "Generated from the files present (tools/index3.py); each receipt's first line names its head.", ""]
    (d / "INDEX.md").write_text("\n".join(text + rows(files, d)) + "\n")
    print(sub, len(files), "files", (d / "INDEX.md").stat().st_size, "bytes")
files = sorted(x for x in root.rglob("*") if x.is_file() and x.name != "INDEX.md"
               and x.relative_to(root).parts[0] not in ("r2", "r3"))
text = ["# Receipts index", "", "Generated from the files present (tools/index3.py); each receipt's first line names its head.",
        "Round 2's receipts are indexed in `r2/INDEX.md`, round 3's in `r3/INDEX.md`; this index lists round 1's.", ""]
(root / "INDEX.md").write_text("\n".join(text + rows(files, root)) + "\n")
print("round 1", len(files), "files", (root / "INDEX.md").stat().st_size, "bytes")
