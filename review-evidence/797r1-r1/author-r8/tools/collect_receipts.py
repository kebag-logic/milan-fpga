#!/usr/bin/env python3
"""Copy this round's docs.yml run logs into the receipts, replace host paths in every receipt,
keep a log over 190 KB as its digest, size and tail, and index the files present.
Usage: collect_receipts.py <receipts> <head>"""
import hashlib
import re
import shutil
import sys
from pathlib import Path

receipts, head = Path(sys.argv[1]), sys.argv[2]
RUN = Path("$VALIDATION_STORAGE/797-a711h/run1")
LIMIT = 190_000
PATHS = (
    (r"$VALIDATION_STORAGE/797-a711h/run1/[a-z0-9-]+/wt", "<clone>"),
    (r"$VALIDATION_STORAGE/797-a711h/plants", "<plant-clone>"),
    (r"$VALIDATION_STORAGE/797-a711h/[A-Za-z0-9_./-]*", "<scratch>"),
    (r"$VALIDATION_STORAGE/797-a711g/gates/venv", "<venv>"),
    (r"$VALIDATION_STORAGE/797-a711g/gates/home", "<scratch-home>"),
    (r"$VALIDATION_STORAGE/797-a711g/[A-Za-z0-9_./-]*", "<scratch>"),
    (r"$VALIDATION_TOOLS/pinned-verilator-5.050", "<pinned-verilator>"),
    (r"$VALIDATION_TOOLS/sv2v-v0.0.12", "<sv2v>"),
    (r"$VALIDATION_STORAGE/scratch/a662/make43/bin", "<make>"),
    (r"$LANES/797-r1-regref", "<lane>"),
    (r"$HOME/milan-fpga-management/tools/tsn-gen-deca300c", "<tsn-gen>"),
    (r"$HOME/milan-fpga-management/2026-09-23/797-a711h", "<packet>"),
    (r"$HOME", "<home>"),
)


def clean(text: str) -> str:
    """The text with every host path replaced by its placeholder."""
    for pattern, placeholder in PATHS:
        text = re.sub(pattern, placeholder, text)
    return text


def put(source: Path, target: Path) -> None:
    """Copy one file, cleaned; a large one is kept as digest, size and tail."""
    target.parent.mkdir(parents=True, exist_ok=True)
    raw = source.read_bytes()
    text = clean(raw.decode("utf-8", "replace"))
    if len(raw) > LIMIT:
        tail = "\n".join(text.splitlines()[-60:])
        target.with_name(target.name + ".tail").write_text(
            f"sha256 {hashlib.sha256(raw).hexdigest()} size {len(raw)}; the whole log stays out of the packet.\n{tail}\n")
    else:
        target.write_text(text)


logs = receipts / "run/logs"
if logs.exists():
    shutil.rmtree(logs)
for source in sorted((RUN / "logs").iterdir()):
    if source.is_file():
        put(source, logs / source.name)
put(RUN / "memory.txt", receipts / "run/memory.txt")
for path in sorted(receipts.rglob("*")):
    if path.is_file() and path.name != "INDEX.md" and not path.is_relative_to(logs):
        raw = path.read_bytes()
        text = raw.decode("utf-8", "replace")
        if clean(text) != text:
            path.write_text(clean(text))
(receipts / "HEAD.txt").write_text(f"{head}\n")
rows = ["# Receipts", "", f"Head `{head}`. Generated from the files present.", "",
        "| File | Bytes | sha256 |", "|---|---:|---|"]
for path in sorted(receipts.rglob("*")):
    if path.is_file() and path.name != "INDEX.md":
        data = path.read_bytes()
        rows.append(f"| `{path.relative_to(receipts).as_posix()}` | {len(data)} | `{hashlib.sha256(data).hexdigest()}` |")
(receipts / "INDEX.md").write_text("\n".join(rows) + "\n")
print(f"{len(rows) - 6} files indexed")
