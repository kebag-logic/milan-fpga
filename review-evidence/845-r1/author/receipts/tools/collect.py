#!/usr/bin/env python3
"""Copy gate logs into the receipts tree with host paths masked.

usage: collect.py <dest dir> <file>...

A file of at most 200 KB is copied whole, masked. A larger one is recorded by its size and sha256 in
<dest>/RAW-RECORDS.txt and represented by its last 300 lines, masked, as <name>.tail.
"""
import hashlib
import re
import sys
from pathlib import Path

LIMIT = 200 * 1024
MASKS = (
    (r"<scratch>", "<scratch>"),
    (r"<lanes>", "<lanes>"),
    (r"<worktrees>", "<worktrees>"),
    (r"<toolchain>", "<toolchain>"),
    (r"<make-4.3>", "<make-4.3>"),
    (r"<tmp>", "<tmp>"),
    (r"<mgmt>", "<mgmt>"),
    (r"<mgmt-root>", "<mgmt-root>"),
    (r"<litex>", "<litex>"),
    (r"<home>", "<home>"),
    (r"<console> "<console>"),
    (r"\b<cable>\b", "<cable>"),
    (r"\b<host>\b", "<host>"),
)


def mask(text: str) -> str:
    for pat, rep in MASKS:
        text = re.sub(pat, rep, text)
    return text


dest = Path(sys.argv[1])
dest.mkdir(parents=True, exist_ok=True)
raw = dest / "RAW-RECORDS.txt"
for name in sys.argv[2:]:
    src = Path(name)
    data = src.read_bytes()
    text = data.decode("utf-8", "replace")
    if len(data) <= LIMIT:
        (dest / src.name).write_text(mask(text))
    else:
        tail = "\n".join(text.splitlines()[-300:]) + "\n"
        (dest / (src.name + ".tail")).write_text(mask(tail))
        with raw.open("a") as out:
            out.write(f"{hashlib.sha256(data).hexdigest()}  {len(data)}  {mask(str(src))}\n")
