#!/usr/bin/env python3
"""Compare two revisions of RTL files with // and /* */ comments and blank lines removed.
Usage: code_only_diff.py <repo> <base> <head> <path>..."""
import re, subprocess, sys, difflib
repo, base, head, *paths = sys.argv[1:]
def strip(txt):
    txt = re.sub(r'/\*(?!\s*verilator).*?\*/', '', txt, flags=re.S)
    out = []
    for ln in txt.splitlines():
        ln = re.sub(r'//.*$', '', ln).rstrip()
        if ln.strip():
            out.append(ln)
    return out
rc = 0
for p in paths:
    a = strip(subprocess.run(['git','-C',repo,'show',f'{base}:{p}'],capture_output=True,text=True,check=True).stdout)
    b = strip(subprocess.run(['git','-C',repo,'show',f'{head}:{p}'],capture_output=True,text=True,check=True).stdout)
    d = list(difflib.unified_diff(a,b,f'{base[:9]}:{p}',f'{head[:9]}:{p}',lineterm='',n=1))
    print(f'## {p}: {"IDENTICAL CODE" if not d else "CODE DIFFERS"}')
    for l in d: print(l)
