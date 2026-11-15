#!/usr/bin/env python3
"""Copy gate logs into receipts/, with host prefixes replaced by named placeholders.

collect.py <table.tsv> <src-dir> <dest-dir> [<glob>...]: <table.tsv> holds one `prefix<TAB>placeholder`
row per host prefix, longest first, and stays outside receipts/. Every matching file at most 200 KB after
the substitution is copied; a larger one is listed in <dest-dir>/LARGE.tsv by its bytes and sha256
instead. <dest-dir>/RAW.tsv records the bytes and sha256 of every source file as it was, before the
substitution, so a copy can be checked against the scratch original.
"""
import hashlib
import sys
from pathlib import Path

LIMIT = 200 * 1024


def main() -> int:
    """Copy, list the large and record the raw digests."""
    table, src, dest = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    globs = sys.argv[4:] or ["*"]
    pairs = [tuple(line.split("\t")) for line in table.read_text().splitlines() if line.strip()]
    dest.mkdir(parents=True, exist_ok=True)
    files = sorted({p for g in globs for p in src.glob(g) if p.is_file()})
    raw, large, copied = [], [], 0
    for path in files:
        body = path.read_bytes()
        rel = path.relative_to(src)
        raw.append(f"{rel}\t{len(body)}\t{hashlib.sha256(body).hexdigest()}")
        clean = body
        for old, new in pairs:
            clean = clean.replace(old.encode(), new.encode())
        if len(clean) > LIMIT:
            large.append(f"{rel}\t{len(clean)}\t{hashlib.sha256(clean).hexdigest()}")
            continue
        out = dest / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(clean)
        copied += 1
    with (dest / "RAW.tsv").open("a") as stream:
        stream.write("".join(f"{row}\n" for row in raw))
    if large:
        with (dest / "LARGE.tsv").open("a") as stream:
            stream.write("".join(f"{row}\n" for row in large))
    print(f"{copied} copied, {len(large)} listed as large, {len(raw)} raw digests -> {dest.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
