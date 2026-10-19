#!/usr/bin/env python3
"""Copy receipts into the output directory with host paths scrubbed, and
write an index generated from the files actually present.

usage: receipts.py copy <src> <dst-relative-to-receipts>
       receipts.py index
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

OUT = Path("<home>/milan-fpga-management/2026-09-23/gptp84-a655")
RECEIPTS = OUT / "receipts"
MAX_BYTES = 200 * 1024

#: longest first, so a nested path is named by its most specific placeholder
SCRUB = [
    (re.compile(r"<home>/\.local/share/containers/storage/overlay/[0-9a-f]+/diff"),
     "<pinned-tools>"),
    (re.compile(r"<scratch>/(wt-[A-Za-z0-9-]+)"), r"<parent-\1>"),
    (re.compile(r"<parent-apply-check>"), "<parent-apply-check>"),
    (re.compile(r"<parent-head-snapshot>"), "<parent-head-snapshot>"),
    (re.compile(r"<parent-c-checkout>"), "<parent-c-checkout>"),
    (re.compile(r"<parent-base-snapshot>"), "<parent-base-snapshot>"),
    (re.compile(r"<lane-base>"), "<lane-base>"),
    (re.compile(r"<lane-head>"), "<lane-head>"),
    (re.compile(r"<scratch>"), "<scratch>"),
    (re.compile(r"<lane>"), "<lane>"),
    (re.compile(r"<data>/lanes/[A-Za-z0-9._-]+"), "<other-lane>"),
    (re.compile(r"<data>/tools/[A-Za-z0-9._-]+"), "<pinned-tools>"),
    (re.compile(r"<data>"), "<data>"),
    (re.compile(r"<home>"), "<home>"),
    (re.compile(r"/tmp/[A-Za-z0-9._-]+"), "<tmp>"),
    (re.compile(r"\balex\b"), "<user>"),
    (re.compile(r"<author>"), "<author>"),
    (re.compile(r"<author>"), "<author>"),
]


def scrub(text: str) -> str:
    """The text with every known host path replaced by its placeholder."""
    for pattern, placeholder in SCRUB:
        text = pattern.sub(placeholder, text)
    return text


def copy(src: Path, rel: str) -> None:
    """Scrub `src` into receipts/`rel`, keeping it under MAX_BYTES."""
    text = scrub(src.read_text(encoding="utf-8", errors="replace"))
    data = text.encode("utf-8")
    if len(data) > MAX_BYTES:
        keep = MAX_BYTES // 2 - 512
        head = data[:keep].decode("utf-8", errors="ignore")
        tail = data[-keep:].decode("utf-8", errors="ignore")
        text = (head + f"\n\n[... {len(data) - 2 * keep} bytes elided to stay "
                "under the 200 KB receipt limit; the full log is kept in the "
                "lane's scratch ...]\n\n" + tail)
    dst = RECEIPTS / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="utf-8")


def index() -> None:
    """Write receipts/INDEX.md from the files present under receipts/."""
    rows = []
    for path in sorted(RECEIPTS.rglob("*")):
        if not path.is_file() or path.name == "INDEX.md":
            continue
        data = path.read_bytes()
        rows.append(f"| `{path.relative_to(RECEIPTS)}` | {len(data)} | "
                    f"`{hashlib.sha256(data).hexdigest()[:16]}` |")
    body = ["# Receipt index", "",
            "Generated from the files present under this directory.", "",
            f"{len(rows)} files.", "",
            "| File | Bytes | SHA-256 (first 16) |", "|---|---:|---|", *rows, ""]
    (RECEIPTS / "INDEX.md").write_text("\n".join(body), encoding="utf-8")


if __name__ == "__main__":
    if sys.argv[1] == "copy":
        copy(Path(sys.argv[2]), sys.argv[3])
    else:
        index()
