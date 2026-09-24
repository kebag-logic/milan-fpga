#!/usr/bin/env python3
"""[A261] scratch: print the count lines of a gate 1b log."""
import re
import sys

PATTERNS = (
    r"\d+/\d+ character-closure cells.*?GCC recorded them"
    r"(?:, and re-measured on [\w-]+|; NOT re-measured)",
    r"\d+/\d+ mutations rejected",
    r"\d+/\d+ directive spellings \([^)]*\) read as the pinned GCC recorded "
    r"them(?:, and re-measured on [\w-]+|; NOT re-measured)?",
    r"\d+/\d+ legitimate firmware edits and \d+/\d+ legitimate Makefile edits "
    r"accepted",
    r"\(\d+ out-of-subset constructs refused by name, \d+ within-S controls "
    r"accepted\)",
    r"TEXT RULES \+ INSTRUMENTS|TEXT RULES ONLY, AND WEAKER",
    r"GATE 1b PASS[^\n]*",
    r"exit=\d+",
)
for path in sys.argv[1:]:
    text = open(path, encoding="utf-8").read()
    print(f"== {path}")
    for pattern in PATTERNS:
        found = re.search(pattern, text, re.S)
        print("  ", found.group(0) if found else f"MISSING {pattern[:40]}")
