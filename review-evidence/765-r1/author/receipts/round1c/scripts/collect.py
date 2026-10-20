#!/usr/bin/env python3
"""Copy one log into the receipts tree with host paths replaced.

Usage: collect.py <src> <dest-relative-to-receipts>
A file over 200 KB is kept as a stub: its SHA-256 and size (of the original),
then its last 200 lines.
"""
import hashlib
import sys
from pathlib import Path

RECEIPTS = Path("<home>/milan-fpga-management/2026-09-23/765-a657/receipts")
LIMIT = 200 * 1024
SUBST = [
    ("<scratch>", "<scratch>"),
    ("<base-lane-scratch>", "<base-lane-scratch>"),
    ("<sdk>", "<sdk>"),
    ("<lane>", "<lane>"),
    ("<tools>", "<tools>"),
    ("<home>", "<home>"),
]


def clean(text: str) -> str:
    for old, new in SUBST:
        text = text.replace(old, new)
    return text


def main() -> int:
    src = Path(sys.argv[1])
    dest = RECEIPTS / sys.argv[2]
    dest.parent.mkdir(parents=True, exist_ok=True)
    raw = src.read_bytes()
    text = clean(raw.decode("utf-8", errors="replace"))
    if len(text.encode()) > LIMIT:
        lines = text.splitlines()[-200:]
        digest = hashlib.sha256(raw).hexdigest()
        text = (f"full log sha256 {digest} size {len(raw)} bytes "
                f"(kept in scratch, over 200 KB); last 200 lines:\n" + "\n".join(lines) + "\n")
        dest = dest.with_name(dest.name + ".tail")
    dest.write_text(text)
    print(dest.relative_to(RECEIPTS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
