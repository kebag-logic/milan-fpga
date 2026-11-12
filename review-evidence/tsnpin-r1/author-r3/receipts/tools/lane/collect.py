"""collect.py <dest receipts dir> <src>=<rel dest> ...: copy receipts with host paths scrubbed; files over 200 KB are
listed by sha256 and size instead of copied. Then write INDEX.md from the files present."""
import hashlib, sys, os
from pathlib import Path
dest = Path(sys.argv[1])
SCRUB = (("<scratch>", "<scratch>"), ("<lane>", "<lane>"),
         ("<shard-clone>", "<shard-clone>"), ("<mgmt>", "<mgmt>"),
         ("<litex-env>", "<litex-env>"), ("<rv32-sdk>", "<rv32-sdk>"), ("<home>", "<home>"),
         ("<tools>", "<tools>"), ("<tools-scratch>", "<tools-scratch>"), ("<tmp>", "<tmp>"))
LIMIT = 200 * 1024
big = []
def scrub(b: bytes) -> bytes:
    for a, r in SCRUB:
        b = b.replace(a.encode(), r.encode())
    return b
def put(src: Path, rel: Path):
    data = src.read_bytes()
    h = hashlib.sha256(data).hexdigest()
    out = scrub(data)
    if len(out) > LIMIT:
        big.append((str(rel), len(data), h))
        return
    t = dest / rel
    t.parent.mkdir(parents=True, exist_ok=True)
    t.write_bytes(out)
for arg in sys.argv[2:]:
    s, r = arg.split("=", 1)
    s, r = Path(s), Path(r)
    if s.is_dir():
        for f in sorted(s.rglob("*")):
            if f.is_file():
                put(f, r / f.relative_to(s))
    elif s.is_file():
        put(s, r)
    else:
        print("missing", s, file=sys.stderr)
if big:
    lst = dest / "LARGE-FILES.md"
    old = lst.read_text() if lst.exists() else "| Receipt not copied (over 200 KB) | Bytes | sha256 of the original |\n|---|---:|---|\n"
    lst.write_text(old + "".join(f"| `{p}` | {n:,} | `{h}` |\n" for p, n, h in big))
rows = []
for f in sorted(dest.rglob("*")):
    if f.is_file() and f.name != "INDEX.md":
        rows.append(f"| `{f.relative_to(dest)}` | {f.stat().st_size:,} | `{hashlib.sha256(f.read_bytes()).hexdigest()[:16]}` |")
(dest / "INDEX.md").write_text("# Receipts index\n\nGenerated from the files present (collect.py). Host paths in each copy are "
                               "replaced by placeholders such as `<scratch>` and `<lane>`; files over 200 KB are listed in "
                               "`LARGE-FILES.md` by the sha256 of the original.\n\n| File | Bytes | sha256 (first 16) |\n"
                               "|---|---:|---|\n" + "\n".join(rows) + "\n")
print(f"{len(rows)} files indexed, {len(big)} large listed")
