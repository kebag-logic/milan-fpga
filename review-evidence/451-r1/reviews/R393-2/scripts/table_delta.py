#!/usr/bin/env python3
"""Compare every Markdown table row of one file between two commits.
Rows are taken in order (lines starting with '|'); reports rows removed, rows
added, and whether the numeric content of each table is unchanged.
Usage: table_delta.py <repo> <old-commit> <new-commit> <path>"""
import difflib
import json
import re
import subprocess
import sys

repo, old, new, path = sys.argv[1:5]


def rows(rev):
    t = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], check=True,
                       capture_output=True, text=True).stdout
    return [ln for ln in t.splitlines() if ln.startswith("|")]


a, b = rows(old), rows(new)
sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
ops = [{"op": op, "old": a[i1:i2], "new": b[j1:j2]}
       for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal"]
num = re.compile(r"\d[\d,.]*")
changed_numbers = [{"old": num.findall(" ".join(o["old"])), "new": num.findall(" ".join(o["new"]))}
                   for o in ops]
print(json.dumps({"old_rows": len(a), "new_rows": len(b), "changes": ops,
                  "numbers_in_changed_rows": changed_numbers}, indent=1))
