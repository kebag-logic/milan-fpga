#!/usr/bin/env python3
"""Copy the gate logs into the receipts, with host paths replaced. A log over
190 KB is kept as its digest, size and tail. Other receipts are rewritten the
same way, and an index is generated from the files present.
Usage: collect_receipts.py <gate logs> <receipts> <head> <tree>"""
import hashlib
import re
import sys
from pathlib import Path

logs, receipts, head, tree = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4]
LIMIT = 190_000
TEXT = (".log", ".txt", ".rc", ".json", ".tsv", ".tail", ".csv", ".md")
PATHS = (
    (r"$VALIDATION_STORAGE/797-a711c/gates/wt", "<clone>"),
    (r"$VALIDATION_STORAGE/797-a711c/aux/wt", "<clone>"),
    (r"$VALIDATION_STORAGE/797-a711c/[A-Za-z0-9_./-]*", "<scratch>"),
    (r"$VALIDATION_STORAGE/797-a711b/[A-Za-z0-9_./-]*", "<scratch>"),
    (r"$VALIDATION_STORAGE/640-a720e/home", "<scratch-home>"),
    (r"$VALIDATION_STORAGE/640-a720e/gates/venv", "<venv>"),
    (r"$VALIDATION_STORAGE/818-mdvenv", "<md-venv>"),
    (r"$LANES/797-r1-regref", "<lane>"),
    (r"$REVIEWS/797r1-r75[34]-[12]-packet", "<review-packet>"),
    (r"$WORKSPACE_HOME", "<home>"),
)


def clean(text: str) -> str:
    """The text with every host path replaced by its placeholder."""
    for pattern, placeholder in PATHS:
        text = re.sub(pattern, placeholder, text)
    return text


gates = receipts / "gates"
gates.mkdir(parents=True, exist_ok=True)
for source in sorted(logs.iterdir()):
    raw = source.read_bytes()
    text = clean(raw.decode("utf-8", "replace"))
    if len(raw) > LIMIT:
        digest = hashlib.sha256(raw).hexdigest()
        tail = "\n".join(text.splitlines()[-60:])
        (gates / (source.name + ".tail")).write_text(
            f"sha256 {digest} size {len(raw)}; the whole log stays out of the packet.\n{tail}\n", encoding="utf-8")
    else:
        (gates / source.name).write_text(text, encoding="utf-8")
(gates / "HEAD.txt").write_text(f"{head}\n{tree}\n", encoding="utf-8")
for path in sorted(receipts.rglob("*")):
    if path.is_file() and path.suffix in TEXT and not path.is_relative_to(gates):
        before = path.read_text(encoding="utf-8", errors="replace")
        after = clean(before)
        if after != before:
            path.write_text(after, encoding="utf-8")
rows = ["# Receipts", "", f"Head `{head}`, tree `{tree}`.", "", "| File | Bytes | sha256 |", "|---|---:|---|"]
for path in sorted(receipts.rglob("*")):
    if path.is_file() and path.name != "INDEX.md":
        data = path.read_bytes()
        rows.append(f"| `{path.relative_to(receipts).as_posix()}` | {len(data)} | `{hashlib.sha256(data).hexdigest()[:16]}` |")
(receipts / "INDEX.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(f"{len(rows) - 6} files indexed")
