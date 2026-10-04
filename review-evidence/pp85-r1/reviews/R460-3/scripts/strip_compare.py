#!/usr/bin/env python3
"""Compare two SystemVerilog files with comments removed (string-literal aware).

usage: strip_compare.py OLD NEW   -> prints both stripped hashes; rc 0 iff equal
Whitespace runs are collapsed so a re-flowed comment cannot hide or fake a change.
"""
import hashlib
import re
import sys


def strip(text):
    out, i, n = [], 0, len(text)
    while i < n:
        if text.startswith("//", i):
            j = text.find("\n", i)
            i = n if j < 0 else j
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            i = n if j < 0 else j + 2
            out.append(" ")
        elif text[i] == '"':
            j = i + 1
            while j < n and text[j] != '"':
                j += 2 if text[j] == "\\" else 1
            out.append(text[i:j + 1])
            i = j + 1
        else:
            out.append(text[i])
            i += 1
    return re.sub(r"\s+", " ", "".join(out)).strip()


a, b = (strip(open(p, encoding="utf-8").read()) for p in sys.argv[1:3])
for p, s in zip(sys.argv[1:3], (a, b)):
    print(f"{hashlib.sha256(s.encode()).hexdigest()}  {p} (comments stripped, {len(s)} chars)")
print("IDENTICAL" if a == b else "DIFFERENT")
sys.exit(0 if a == b else 1)
