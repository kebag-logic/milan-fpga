#!/usr/bin/env python3
"""collect.py <src-dir> <dst-dir> [name-prefix...]: copy one run directory's gate records (cmd, rc, start, end,
log, txt, json, stat, md) into a receipts directory with host paths scrubbed to symbolic roots. A file whose
scrubbed copy would exceed 200 KB is not copied: its sha256 and size are recorded beside its last 60 lines."""
import hashlib, sys
from pathlib import Path
ROOTS = [("$VALIDATION_STORAGE/scratch/pp217-a755", "$SCRATCH"), ("$VALIDATION_STORAGE/scratch/pp217-parent", "$PARENT"),
         ("$VALIDATION_STORAGE/scratch/pp217-665twin-base", "$TWIN_BASE"), ("$VALIDATION_STORAGE/scratch/pp217-665twin", "$TWIN"),
         ("$LANES/pp217-avail-index", "$LANE"), ("$VALIDATION_TOOLS", "$TOOLS"),
         ("$LANES", "$LANES"), ("$VALIDATION_STORAGE/scratch", "$SCRATCH_ROOT"),
         ("$HOME/milan-fpga-management/2026-09-23/pp217-a755", "$OUT"), ("$HOME", "~"), ("/tmp/", "$TMP/")]
SUFFIXES = {".cmd", ".rc", ".start", ".end", ".log", ".txt", ".json", ".stat", ".md", ".sha256"}
LIMIT = 200_000
src, dst = Path(sys.argv[1]), Path(sys.argv[2])
prefixes = sys.argv[3:]
dst.mkdir(parents=True, exist_ok=True)
def scrub(text: str) -> str:
    for a, b in ROOTS:
        text = text.replace(a, b)
    return text
for f in sorted(p for p in src.iterdir() if p.is_file()):
    if f.suffix not in SUFFIXES or (prefixes and not any(f.name.startswith(x) for x in prefixes)):
        continue
    raw = f.read_bytes()
    text = scrub(raw.decode("utf-8", "replace"))
    if len(text.encode()) <= LIMIT:
        (dst / f.name).write_text(text)
    else:
        (dst / (f.name + ".sha256")).write_text(f"{hashlib.sha256(raw).hexdigest()}  {f.name}\nbytes {len(raw)}\n")
        (dst / (f.name + ".tail.txt")).write_text("".join(text.splitlines(True)[-60:]))
