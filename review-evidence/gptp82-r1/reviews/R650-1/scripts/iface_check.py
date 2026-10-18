#!/usr/bin/env python3
"""Compare the KL_gptp_engine parameter/port header of two RTL files with
comments and whitespace removed. Prints both normalised headers' SHA-256 and
any difference; exit 0 when they are identical.

usage: iface_check.py BASE_ENGINE_SV HEAD_ENGINE_SV
"""
import hashlib
import re
import sys


def header(path):
    text = open(path, encoding="utf-8").read()
    start = text.index("module KL_gptp_engine")
    end = text.index(");", text.index("output logic  [4:0] dbg_status_o", start)) + 2
    h = text[start:end]
    h = re.sub(r"/\*.*?\*/", "", h, flags=re.S)
    h = re.sub(r"//[^\n]*", "", h)
    return [" ".join(l.split()) for l in h.splitlines() if l.strip()]


a, b = header(sys.argv[1]), header(sys.argv[2])
for tag, h in (("base", a), ("head", b)):
    print(tag, hashlib.sha256("\n".join(h).encode()).hexdigest(), len(h), "lines")
if a == b:
    print("IDENTICAL parameter/port header (comments stripped)")
    sys.exit(0)
import difflib
print("\n".join(difflib.unified_diff(a, b, "base", "head", lineterm="")))
sys.exit(1)
