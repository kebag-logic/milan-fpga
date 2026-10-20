"""usage: index.py <receipts-dir>   write INDEX.md and index/<area>.md from the files present
(bytes, sha256), one index file per top-level directory so that none exceeds 200 KB"""
import hashlib
import sys
from pathlib import Path

root = Path(sys.argv[1])
idx = root / "index"
files = sorted(p for p in root.rglob("*") if p.is_file() and p.name != "INDEX.md"
               and idx not in p.parents)
areas: dict[str, list[Path]] = {}
for p in files:
    rel = p.relative_to(root)
    areas.setdefault(rel.parts[0] if len(rel.parts) > 1 else ".", []).append(p)
idx.mkdir(exist_ok=True)
for old in idx.glob("*.md"):
    old.unlink()
out = ["# Receipts index", "",
       "Generated from the files present under `receipts/` (size in bytes, sha256), one index",
       "file per top-level directory under `index/`.",
       "Host paths in the logs are masked: `<scratch>` (the lane's scratch root), `<lane>` (the",
       "lane tree), `<toolroot>` (the pinned tool image), `<management>`, `<home>`, `<data>`,",
       "`<vivado-lock>` (the host-wide Vivado lock file).",
       "A file over 200 KB after masking is not copied; `OVER-200KB.sha256` lists its sha256,",
       "size and path, and `<file>.excerpt.txt` beside it keeps its FAIL, tally and verdict",
       "lines. Campaign units' source-tree copies and build directories are not copied.",
       f"{len(files)} files.", "",
       "| Directory | Files | Bytes | Index |", "|---|---|---|---|"]
for area in sorted(areas):
    ps = areas[area]
    name = "top" if area == "." else area
    lines = [f"# Receipts index: `{'receipts/' if area == '.' else 'receipts/' + area + '/'}`", "",
             f"{len(ps)} files.", ""]
    groups: dict[str, list[Path]] = {}
    for p in ps:
        groups.setdefault(str(p.parent.relative_to(root)) + "/", []).append(p)
    for g in sorted(groups):
        lines += [f"## {g}", "", "| File | Bytes | sha256 |", "|---|---|---|"]
        for p in groups[g]:
            lines.append(f"| `{p.name}` | {p.stat().st_size} | "
                         f"`{hashlib.sha256(p.read_bytes()).hexdigest()}` |")
        lines.append("")
    (idx / f"{name}.md").write_text("\n".join(lines))
    out.append(f"| `{area}/` | {len(ps)} | {sum(p.stat().st_size for p in ps)} | `index/{name}.md` |")
out.append("")
(root / "INDEX.md").write_text("\n".join(out))
print(f"{len(files)} files indexed in {len(areas)} index files")
