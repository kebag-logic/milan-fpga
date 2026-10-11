#!/usr/bin/env python3
"""edit_once.py FILE OLD NEW: replace OLD with NEW in FILE, refusing unless OLD occurs exactly once."""
import sys
from pathlib import Path

path, old, new = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
text = path.read_text()
count = text.count(old)
if count != 1:
    sys.exit(f"edit_once: {path}: expected 1 occurrence, found {count}: {old!r}")
path.write_text(text.replace(old, new))
print(f"edit_once: {path}: applied")
