#!/usr/bin/env python3
"""collect.py <src-dir> <dest-dir>: copy a run's text receipts into the output directory.

Every file under <src-dir> is copied to <dest-dir> with host paths replaced by
placeholders. A file over 200 KB (after the replacement) is kept as its
SHA-256, size and last 200 lines (<name>.tail) instead; build trees
(obj_*, __pycache__) and binaries are skipped and listed in SKIPPED.txt.
"""
import hashlib
import sys
from pathlib import Path

LIMIT = 200 * 1024
# The host paths are elided in this receipt copy: each entry maps one host
# directory (named by its placeholder) to that placeholder.
SUBS = [
    ("<lane>-host-path", "<lane>"),
    ("<clone>--host-path", "<clone>-"),
    ("<scratch>-host-path", "<scratch>"),
    ("<tools-ci>-host-path", "<tools-ci>"),
    ("<tools>-host-path", "<tools>"),
    ("<sdk>-host-path", "<sdk>"),
    ("<out>-host-path", "<out>"),
    ("<home>-host-path", "<home>"),
    ("<data>-host-path", "<data>"),
]


def scrub(text: str) -> str:
    for old, new in SUBS:
        text = text.replace(old, new)
    return text


def main() -> int:
    src, dest = Path(sys.argv[1]), Path(sys.argv[2])
    skipped = []
    for path in sorted(p for p in src.rglob("*") if p.is_file()):
        rel = path.relative_to(src)
        if any(part.startswith("obj_") or part == "__pycache__" for part in rel.parts):
            skipped.append(f"{rel}\tbuild tree")
            continue
        data = path.read_bytes()
        try:
            text = scrub(data.decode("utf-8"))
        except UnicodeDecodeError:
            skipped.append(f"{rel}\tbinary {len(data)} B sha256 {hashlib.sha256(data).hexdigest()}")
            continue
        out = dest / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        body = text.encode("utf-8")
        if len(body) > LIMIT:
            tail = "\n".join(text.splitlines()[-200:]) + "\n"
            out.with_name(out.name + ".tail").write_text(tail)
            out.with_name(out.name + ".sha256").write_text(
                f"{hashlib.sha256(data).hexdigest()}  {len(data)} B  {rel} (original bytes, host paths unscrubbed)\n")
        else:
            out.write_bytes(body)
    if skipped:
        (dest / "SKIPPED.txt").write_text("\n".join(skipped) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
