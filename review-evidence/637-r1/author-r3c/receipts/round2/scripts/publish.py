#!/usr/bin/env python3
"""Copy receipts into the output directory with host paths redacted.

usage: publish.py <dest-dir> <file>...   (each file is copied flat into dest)

A file whose redacted text is over 190 KB is not copied whole: an excerpt (the
first 120 and last 400 lines) is written as <name>.excerpt, and its full size
and sha256 (of the original bytes) are appended to <dest>/LARGE-FILES.tsv.
"""
import hashlib
import sys
from pathlib import Path

SUBS = [
    ("<scratch>", "<scratch>"),
    ("<lane>", "<lane>"),
    ("<tools>", "<tools>"),
    ("<act>", "<act>"),
    ("<home>", "<home>"),
    ("<tmp>", "<tmp>"),
]
LIMIT = 190 * 1024


def redact(text: str) -> str:
    for a, b in SUBS:
        text = text.replace(a, b)
    return text


def main() -> int:
    dest = Path(sys.argv[1])
    dest.mkdir(parents=True, exist_ok=True)
    for name in sys.argv[2:]:
        src = Path(name)
        raw = src.read_bytes()
        text = redact(raw.decode("utf-8", errors="replace"))
        if len(text.encode()) <= LIMIT:
            (dest / src.name).write_text(text)
            continue
        lines = text.splitlines()
        cut = lines[:120] + [f"... {len(lines) - 520} lines omitted ..."] + lines[-400:]
        (dest / (src.name + ".excerpt")).write_text("\n".join(cut) + "\n")
        with (dest / "LARGE-FILES.tsv").open("a") as f:
            f.write(f"{src.name}\t{len(raw)}\t{hashlib.sha256(raw).hexdigest()}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
