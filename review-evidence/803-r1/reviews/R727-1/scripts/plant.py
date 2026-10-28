#!/usr/bin/env python3
"""plant.py <file> <old> <new>: replace exactly one occurrence, refuse otherwise."""
import sys
path, old, new = sys.argv[1], sys.argv[2], sys.argv[3]
text = open(path, encoding="utf-8").read()
n = text.count(old)
if n != 1:
    sys.exit(f"REFUSED: {n} occurrences in {path}")
open(path, "w", encoding="utf-8").write(text.replace(old, new))
print(f"planted in {path}")
