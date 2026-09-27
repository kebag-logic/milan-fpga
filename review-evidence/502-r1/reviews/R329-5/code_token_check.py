#!/usr/bin/env python3
"""Compare SystemVerilog files between two commits with // comments and whitespace removed."""
import re, subprocess, sys

def tokens(rev, path):
    text = subprocess.run(["git", "show", f"{rev}:{path}"], check=True,
                          capture_output=True, text=True).stdout
    text = re.sub(r"//[^\n]*", "", text)
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return re.sub(r"\s+", " ", text).strip()

old, new, *paths = sys.argv[1:]
status = 0
for path in paths:
    same = tokens(old, path) == tokens(new, path)
    blob = lambda r: subprocess.run(["git", "rev-parse", f"{r}:{path}"], check=True,
                                    capture_output=True, text=True).stdout.strip()
    print(f"{path}: blob {blob(old)[:12]} -> {blob(new)[:12]}; code tokens identical: {same}")
    status |= 0 if same else 1
sys.exit(status)
