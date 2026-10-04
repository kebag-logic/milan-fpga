#!/usr/bin/env python3
"""Plant one textual defect: replace exactly one occurrence of OLD by NEW in FILE.
Usage: plant.py FILE OLD NEW   (OLD and NEW are Python string literals' bodies, \\n allowed)"""
import sys
from pathlib import Path
path, old, new = Path(sys.argv[1]), sys.argv[2].encode().decode("unicode_escape"), sys.argv[3].encode().decode("unicode_escape")
text = path.read_text(encoding="utf-8")
if text.count(old) != 1:
    sys.exit(f"plant: anchor occurs {text.count(old)} times in {path}")
path.write_text(text.replace(old, new), encoding="utf-8")
print(f"planted in {path}: {old!r} -> {new!r}")
