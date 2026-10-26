#!/usr/bin/env python3
"""Apply one exact single-occurrence replacement to a file copy.

Usage: python3 -I apply_mutant.py <file> <old> <new>
"""
import sys

path, old, new = sys.argv[1:4]
text = open(path, encoding="utf-8").read()
if text.count(old) != 1:
    sys.exit(f"anchor occurs {text.count(old)} times")
open(path, "w", encoding="utf-8").write(text.replace(old, new))
print("applied")
