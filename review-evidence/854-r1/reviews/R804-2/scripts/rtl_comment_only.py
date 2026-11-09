#!/usr/bin/env python3
"""Show that the RTL delta between two commits is comments only.
Usage: rtl_comment_only.py <repo> <old> <new> [paths...]
Strips // and /* */ comments plus whitespace from each SystemVerilog file at
both commits and compares the token streams. Exit 0 iff every file is equal."""
import re, subprocess, sys
repo, old, new, *paths = sys.argv[1:]
if not paths:
    paths = subprocess.run(["git","-C",repo,"diff","--name-only",old,new,"--","*.sv","*.v","*.svh","*.vh"],
                           capture_output=True,text=True,check=True).stdout.split()
def strip(src):
    src = re.sub(r"/\*.*?\*/", " ", src, flags=re.S)
    src = re.sub(r"//[^\n]*", " ", src)
    return src.split()
rc = 0
for p in paths:
    a = subprocess.run(["git","-C",repo,"show",f"{old}:{p}"],capture_output=True,text=True,check=True).stdout
    b = subprocess.run(["git","-C",repo,"show",f"{new}:{p}"],capture_output=True,text=True,check=True).stdout
    same = strip(a) == strip(b)
    print(f"{'COMMENT-ONLY' if same else 'LOGIC-CHANGED'} {p} ({len(strip(b))} tokens)")
    rc |= (not same)
print("RESULT", "PASS" if rc == 0 else "FAIL", old, new)
sys.exit(rc)
