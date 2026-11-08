#!/usr/bin/env python3
"""Copy receipts into the output directory, host paths replaced by placeholders, big files by their digest.

usage: receipts_copy.py <dest dir> <file or dir>...
A file over 200 KB is not copied: <name>.sha256 records its sha256, size and original name instead.
Each copied text file has the host's path prefixes replaced (PREFIXES), so no receipt names a host path.
"""
import hashlib
import sys
from pathlib import Path

LIMIT = 200 * 1024
PREFIXES = (
    ("$VALIDATION_STORAGE/scratch/665s6-a745c", "<scratch>"),
    ("$VALIDATION_STORAGE/scratch/665s6-a745b", "<round2-scratch>"),
    ("$LANES/665-s6-placement", "<lane>"),
    ("$LANES/665s6-a745b-526f937c-shard", "<sweep-clone>"),
    ("$HOME/milan-fpga-management/2026-09-23", "<mgmt>"),
    ("$VALIDATION_TOOLS", "<tools>"),
    ("$VALIDATION_STORAGE", "<tmp>"),
    ("$VALIDATION_STORAGE/scratch", "<scratch-root>"),
    ("$LANES", "<lanes>"),
    ("/tmp/" + "agent-tmp", "<tmp>"),  # session tmp prefix redacted for the packet
    ("$HOME", "~"),
)


def copy(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    data = src.read_bytes()
    if len(data) > LIMIT:
        digest = hashlib.sha256(data).hexdigest()
        dest.with_name(dest.name + ".sha256").write_text(f"{digest}  {len(data)} bytes  {src.name}\n")
        return
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        dest.write_bytes(data)
        return
    for old, new in PREFIXES:
        text = text.replace(old, new)
    dest.write_text(text)


def main() -> int:
    dest = Path(sys.argv[1])
    for arg in sys.argv[2:]:
        src = Path(arg)
        if src.is_dir():
            for f in sorted(src.rglob("*")):
                if f.is_file():
                    copy(f, dest / src.name / f.relative_to(src))
        else:
            copy(src, dest / src.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
