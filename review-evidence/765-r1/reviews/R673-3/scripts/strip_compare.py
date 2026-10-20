#!/usr/bin/env python3
"""Compare two SystemVerilog blobs token-by-token with // and /* */ comments removed."""
import re, subprocess, sys
def toks(rev, path):
    src = subprocess.run(["git", "show", f"{rev}:{path}"], check=True, capture_output=True, text=True).stdout
    src = re.sub(r"/\*.*?\*/", " ", src, flags=re.S)
    src = re.sub(r"//[^\n]*", " ", src)
    return re.findall(r"\w+|[^\w\s]", src)
a, b, path = sys.argv[1:4]
ta, tb = toks(a, path), toks(b, path)
print(f"{path}: {a} tokens={len(ta)} {b} tokens={len(tb)} identical={ta == tb}")
sys.exit(0 if ta == tb else 1)
