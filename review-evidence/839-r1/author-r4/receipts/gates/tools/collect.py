#!/usr/bin/env python3
"""collect.py <src dir> <dest dir>: copy each log and rc file, with the scratch, home and data prefixes replaced by
<scratch>, <home> and <data>. A file over 200 KB is not copied: LARGE-LOGS.txt records its size and sha256 (of the
original bytes) and the copy keeps its last 20,000 bytes as <name>.tail. ORIGINALS.sha256 lists every source file."""
import hashlib, sys
from pathlib import Path
src, dst = Path(sys.argv[1]), Path(sys.argv[2]); dst.mkdir(parents=True, exist_ok=True)
subs = [(b"$VALIDATION_STORAGE/839-a731d", b"<scratch>"), (b"$WORKSPACE_HOME", b"<home>"), (b"$VALIDATION_STORAGE", b"<data>")]
large, sums = [], []
for p in sorted(src.iterdir()):
    if not p.is_file(): continue
    data = p.read_bytes(); h = hashlib.sha256(data).hexdigest(); sums.append(f"{h}  {p.name}")
    if len(data) > 200_000:
        large.append(f"{p.name} {len(data)} bytes sha256 {h}"); name, data = p.name + ".tail", data[-20000:]
    else:
        name = p.name
    for a, b in subs: data = data.replace(a, b)
    (dst / name).write_bytes(data)
(dst / "ORIGINALS.sha256").write_text("\n".join(sums) + "\n")
if large: (dst / "LARGE-LOGS.txt").write_text("\n".join(large) + "\n")
print(f"{len(sums)} files, {len(large)} large")
