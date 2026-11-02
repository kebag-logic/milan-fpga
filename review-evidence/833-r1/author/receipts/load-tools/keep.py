#!/usr/bin/env python3
"""usage: keep.py <src dir> <dst dir>  Copy every file at or under 200 KB; record the sha256 and size of larger ones in LARGE-LOGS.txt."""
import hashlib, shutil, sys
from pathlib import Path
src, dst = Path(sys.argv[1]), Path(sys.argv[2]); dst.mkdir(parents=True, exist_ok=True)
large = []
for f in sorted(p for p in src.rglob("*") if p.is_file()):
    rel = f.relative_to(src)
    if f.stat().st_size > 200_000:
        large.append(f"{hashlib.sha256(f.read_bytes()).hexdigest()} {f.stat().st_size} {f}")
    else:
        (dst / rel).parent.mkdir(parents=True, exist_ok=True); shutil.copy2(f, dst / rel)
(dst / "LARGE-LOGS.txt").write_text("\n".join(large) + ("\n" if large else ""))
print(dst.name, "large files", len(large))
