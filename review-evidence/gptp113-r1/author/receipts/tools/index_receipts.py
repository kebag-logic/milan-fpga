#!/usr/bin/env python3
"""Copy the lane's logs into the packet's receipts with host paths replaced, and write receipts/INDEX.md.

usage: python3 -I index_receipts.py PACKET SOURCE_DIR [SOURCE_DIR...]
Every file of each SOURCE_DIR is copied to PACKET/receipts/<dir name>/, its text with each host path below
replaced by a placeholder. INDEX.md lists each receipt: its size, the first 16 hex digits of its sha256, and
its first line.
"""
import hashlib
import sys
from pathlib import Path

REPLACE = (
    ("<scratch>", "<scratch>"),
    ("<consumer>", "<consumer>"),
    ("<tools>", "<tools>"),
    ("<logs>", "<logs>"),
    ("<gptp>", "<gptp>"),
    ("<ccache>", "<ccache>"),
    ("<verilator-5.050>", "<verilator-5.050>"),
    ("<home>", "<home>"),
    ("<tmp>/", "<tmp>/"),
)


def clean(text: str) -> str:
    """`text` with every host path above replaced."""
    for old, new in REPLACE:
        text = text.replace(old, new)
    return text


def main() -> int:
    """Copy, clean and index."""
    packet = Path(sys.argv[1])
    out = packet / "receipts"
    rows = []
    for src in map(Path, sys.argv[2:]):
        for f in sorted(p for p in src.rglob("*") if p.is_file()):
            rel = Path(src.name) / f.relative_to(src)
            dest = out / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            data = clean(f.read_text(errors="replace"))
            dest.write_text(data)
    for f in sorted(p for p in out.rglob("*") if p.is_file() and p.name != "INDEX.md"):
        data = f.read_bytes()
        first = data.decode(errors="replace").splitlines()[0][:110] if data.strip() else "(empty)"
        rows.append(f"| `{f.relative_to(out)}` | {len(data):,} | `{hashlib.sha256(data).hexdigest()[:16]}` | "
                    f"{first.replace('|', '/')} |")
    (out / "INDEX.md").write_text("# Receipts\n\nHost paths are replaced by `<scratch>`, `<consumer>`, `<gptp>`, "
                                  "`<tools>`, `<logs>` and similar placeholders.\n\n"
                                  "| Receipt | Bytes | sha256 (16) | First line |\n|---|---:|---|---|\n"
                                  + "\n".join(rows) + "\n")
    print(f"{len(rows)} receipts indexed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
