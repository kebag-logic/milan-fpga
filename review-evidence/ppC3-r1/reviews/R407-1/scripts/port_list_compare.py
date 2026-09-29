#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer receipt: compare a module's comment-stripped header (parameters and
ports) between two commits. Usage: port_list_compare.py <repo> <base> <head> <path> <module>"""
import re
import subprocess
import sys

repo, base, head, path, mod = sys.argv[1:6]


def header(rev: str) -> str:
    """The comment-stripped, whitespace-normalised text from `module` to the port list's `);`."""
    src = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], check=True,
                         capture_output=True, text=True).stdout
    src = re.sub(r"/\*.*?\*/", " ", src, flags=re.S)
    src = re.sub(r"//[^\n]*", " ", src)
    m = re.search(r"\bmodule\s+" + re.escape(mod) + r"\b(.*?)\)\s*;", src, flags=re.S)
    return " ".join(m.group(1).split())


b, h = header(base), header(head)
print(f"{mod} {path}: header tokens base={len(b.split())} head={len(h.split())} "
      f"identical={b == h}")
if b != h:
    import difflib
    for line in difflib.unified_diff(b.split(" "), h.split(" "), lineterm="", n=3):
        print(line)
sys.exit(0 if b == h else 1)
