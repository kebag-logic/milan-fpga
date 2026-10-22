#!/usr/bin/env python3
"""Usage: port_diff.py OLD_FILE NEW_FILE MODULE - prints the module header (parameters and ports,
comments stripped, whitespace normalised) diff between two versions of a SystemVerilog file."""
import re, sys, difflib
def header(path, mod):
    s = open(path).read()
    s = re.sub(r'//[^\n]*', '', s); s = re.sub(r'/\*.*?\*/', '', s, flags=re.S)
    m = re.search(r'\bmodule\s+' + re.escape(mod) + r'\b(.*?\));', s, flags=re.S)
    if not m: sys.exit(f"module {mod} not found in {path}")
    items = [re.sub(r'\s+', ' ', x).strip() for x in re.split(r'[,;]', m.group(1))]
    return [x for x in items if x]
a, b = header(sys.argv[1], sys.argv[3]), header(sys.argv[2], sys.argv[3])
d = list(difflib.unified_diff(a, b, 'old', 'new', lineterm='', n=0))
print(f"{sys.argv[3]}: {len(a)} -> {len(b)} header items; {'IDENTICAL' if not d else 'DIFFERS'}")
for line in d: print(line)
