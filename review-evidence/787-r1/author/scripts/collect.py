"""collect.py <dest-dir> <source> [<name>]: copy one text receipt into the output directory with host paths replaced by
placeholders (<scratch>, <lane>, <home>, <tmp>). A receipt over 200 KB after the replacement, or a binary, is not
copied: its size and SHA-256 are appended to <dest-dir>/RAW-RECORDS.txt instead."""
import hashlib
import sys
from pathlib import Path

LIMIT = 200 * 1024
SUBST = (("$VALIDATION_STORAGE/scratch/787-a700c", "<scratch>"), ("$LANES/787-reboot-reset", "<lane>"),
         ("$LANES/", "<lanes>/"), ("$VALIDATION_STORAGE/scratch/", "<scratch-root>/"),
         ("$VALIDATION_TOOLS/", "<tools>/"), ("$WORKSPACE_HOME", "<home>"), ("/tmp/", "<tmp>/"))

dest, source = Path(sys.argv[1]), Path(sys.argv[2])
name = sys.argv[3] if len(sys.argv) > 3 else source.name
dest.mkdir(parents=True, exist_ok=True)
raw = source.read_bytes()
digest = hashlib.sha256(raw).hexdigest()
try:
    text = raw.decode("utf-8")
except UnicodeDecodeError:
    text = None
if text is not None:
    for old, new in SUBST:
        text = text.replace(old, new)
if text is None or len(text.encode()) > LIMIT:
    with (dest / "RAW-RECORDS.txt").open("a") as f:
        f.write(f"{name}\t{len(raw)} bytes\tsha256 {digest}\t{'binary' if text is None else 'over 200 KB'}, not copied\n")
    print(f"recorded {name} ({len(raw)} bytes)")
else:
    (dest / name).write_text(text)
    print(f"copied {name}")
