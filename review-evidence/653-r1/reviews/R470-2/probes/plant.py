#!/usr/bin/env python3
"""Reviewer probe helper: replace one exact text occurrence in a file copy.

Usage: plant.py FILE OLD_TEXT_FILE NEW_TEXT_FILE
Refuses unless OLD occurs exactly once, so a probe never mutates nothing.
"""
import sys
from pathlib import Path

path, old_f, new_f = (Path(a) for a in sys.argv[1:4])
text = path.read_text()
old = old_f.read_text()
new = new_f.read_text()
count = text.count(old)
if count != 1:
    sys.exit(f"REFUSED: pattern occurs {count} times in {path}")
path.write_text(text.replace(old, new))
print(f"planted in {path}")
