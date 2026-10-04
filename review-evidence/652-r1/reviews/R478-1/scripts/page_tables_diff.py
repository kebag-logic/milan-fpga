#!/usr/bin/env python3
"""Compare every delimited table block of the #649 findings page at two
commits of the review clone. Usage: page_tables_diff.py <clone> <base> <head>"""
import re
import subprocess
import sys

clone, base, head = sys.argv[1:4]
PAGE = "docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md"
BLOCK = re.compile(r"<!-- table: ([^ ]+) -->\n(.*?)<!-- end table: \1 -->", re.S)


def blocks(rev):
    text = subprocess.run(["git", "-C", clone, "show", f"{rev}:{PAGE}"], capture_output=True,
                          text=True, check=True).stdout
    return dict(BLOCK.findall(text))


a, b = blocks(base), blocks(head)
print(f"tables: base {len(a)}, head {len(b)}; same names: {sorted(a) == sorted(b)}")
changed = sorted(n for n in a if a[n] != b.get(n))
print(f"unchanged: {len(a) - len(changed)}; changed: {changed}")
