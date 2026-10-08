#!/usr/bin/env python3
"""Copy CTRL to DEST and replace one unique OLD text with NEW in PATH (relative to CTRL).

usage: plant.py CTRL DEST PATH OLD NEW
"""
import shutil, sys
from pathlib import Path
src, dest, rel, old, new = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5]
if dest.exists():
    shutil.rmtree(dest)
shutil.copytree(src, dest, ignore=shutil.ignore_patterns("__pycache__"))
f = dest / rel
text = f.read_text()
assert text.count(old) == 1, f"plant site not unique: {text.count(old)}"
f.write_text(text.replace(old, new))
print("planted", rel, repr(old), "->", repr(new))
