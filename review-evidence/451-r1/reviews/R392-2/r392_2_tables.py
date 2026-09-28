#!/usr/bin/env python3
"""Reviewer probe (R392-2): compare every Markdown table row of the page
between two commits. Prints rows present in only one side, per table heading.
Usage: r392_2_tables.py <clone> <old-commit> <new-commit> <path>"""
import json, subprocess, sys
clone, old, new, path = sys.argv[1:5]
def tables(rev):
    txt = subprocess.run(["git", "-C", clone, "show", f"{rev}:{path}"], check=True,
                         capture_output=True, text=True).stdout
    rows = [l for l in txt.splitlines() if l.startswith("|")]
    return rows, sum(1 for l in txt.splitlines() if l.startswith("|---") or l.startswith("|--"))
o, on = tables(old); n, nn = tables(new)
json.dump({"old_rows": len(o), "new_rows": len(n), "old_tables": on, "new_tables": nn,
           "only_old": [r for r in o if r not in n], "only_new": [r for r in n if r not in o]},
          sys.stdout, indent=1); print()
