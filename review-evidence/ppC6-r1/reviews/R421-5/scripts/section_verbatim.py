#!/usr/bin/env python3
"""Check that a validation section is carried verbatim from one PR body to another.

Extracts the text of the heading HEADING (any level) up to the next heading of the
same or higher level, from each body, and compares them byte for byte; on a
mismatch prints a line diff.

usage: section_verbatim.py SRC.md DST.md HEADING [HEADING_IN_DST]
"""
import difflib
import re
import sys


def section(text, heading):
    m = re.search(r"(?m)^(#+) " + re.escape(heading) + r"\s*$", text)
    if not m:
        return None
    lvl = len(m.group(1))
    rest = text[m.end():]
    n = re.search(r"(?m)^#{1,%d} " % lvl, rest)
    return rest[: n.start()] if n else rest


src, dst = open(sys.argv[1]).read(), open(sys.argv[2]).read()
h1 = sys.argv[3]
h2 = sys.argv[4] if len(sys.argv) > 4 else h1
a, b = section(src, h1), section(dst, h2)
print(f"{sys.argv[1]} [{h1}] vs {sys.argv[2]} [{h2}]")
if a is None or b is None:
    print("  heading missing:", a is None, b is None)
    sys.exit(2)
print(f"  chars {len(a)} vs {len(b)}; table rows {a.count(chr(10)+'|')} vs {b.count(chr(10)+'|')}; identical: {a == b}")
if a != b:
    for l in difflib.unified_diff(a.split("\n"), b.split("\n"), lineterm="", n=0):
        print("   " + l[:220])
sys.exit(0 if a == b else 1)
