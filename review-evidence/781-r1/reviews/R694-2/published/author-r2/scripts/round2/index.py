"""Write <dir>/INDEX.md from the files present under <dir>: path, bytes, sha256.
usage: python3 -I index.py <receipts dir>"""
import hashlib, pathlib, sys

root = pathlib.Path(sys.argv[1])
rows = []
for p in sorted(x for x in root.rglob("*") if x.is_file() and x.name != "INDEX.md"):
    data = p.read_bytes()
    rows.append(f"| `{p.relative_to(root)}` | {len(data)} | `{hashlib.sha256(data).hexdigest()}` |")
text = ["# Receipt index (generated from the files present)", "", f"{len(rows)} files.", "",
        "| File | Bytes | sha256 |", "|---|---|---|", *rows, ""]
(root / "INDEX.md").write_text("\n".join(text))
print(f"{len(rows)} files indexed")
