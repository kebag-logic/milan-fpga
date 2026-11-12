"""collect.py <dest receipts dir> <src>=<rel dest> ...: copy receipts with host paths scrubbed; files over 200 KB are
listed by sha256 and size instead of copied. Then write INDEX.md from the files present."""
import hashlib, sys, os
from pathlib import Path
dest = Path(sys.argv[1])
SCRUB = (("<pinned-rv32-sdk>", "<pinned-rv32-sdk>"), ("<scratch>", "<scratch>"), ("<lane>", "<lane>"),
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
import collections
groups = collections.defaultdict(list)
for f in sorted(dest.rglob("*")):
    if f.is_file() and f.name != "INDEX.md":
        rel = f.relative_to(dest)
        top = rel.parts[0] if len(rel.parts) > 1 else "."
        groups[top].append(f"| `{rel}` | {f.stat().st_size:,} | `{hashlib.sha256(f.read_bytes()).hexdigest()[:16]}` |")
for old in dest.rglob("INDEX.md"):
    old.unlink()
note = ("Generated from the files present (collect.py). Host paths in each copy are replaced by placeholders such as "
        "`<scratch>` and `<lane>`; files over 200 KB are listed in `LARGE-FILES.md` by the sha256 of the original.")
top_rows = []
for top, rows in sorted(groups.items()):
    where = dest if top == "." else dest / top
    (where / "INDEX.md").write_text(f"# Receipts index: {top}\n\n{note}\n\n| File | Bytes | sha256 (first 16) |\n"
                                    "|---|---:|---|\n" + "\n".join(rows) + "\n")
    top_rows.append(f"| `{top}/` | {len(rows):,} | [{top}/INDEX.md]({top}/INDEX.md) |" if top != "." else
                    f"| top level | {len(rows):,} | (below) |")
files = "\n".join(groups.get(".", []))
(dest / "INDEX.md").write_text("# Receipts index\n\n" + note + " Each directory has its own index.\n\n"
                               "| Directory | Files | Index |\n|---|---:|---|\n" + "\n".join(top_rows) + "\n\n"
                               "| File | Bytes | sha256 (first 16) |\n|---|---:|---|\n" + files + "\n")
print(f"{sum(len(r) for r in groups.values())} files indexed in {len(groups)} indexes, {len(big)} large listed")
