#!/usr/bin/env python3
"""Crude scan: module-level `logic`/`tk_rec_t`/enum-typed names referenced on
an earlier line than their declaration (comments stripped). Usage: file.sv"""
import re
import sys

text = open(sys.argv[1]).read()
text = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group().count("\n"), text, flags=re.S)
lines = [re.sub(r"//.*", "", l) for l in text.splitlines()]
decl = {}
pat = re.compile(r"^\s*(?:logic|state_e|evc_e|dk_e|tk_rec_t|pp_txn_t)\b[^;(]*?((?:\w+\s*,\s*)*\w+)\s*;")
for n, l in enumerate(lines, 1):
    m = pat.match(l)
    if m:
        for name in re.split(r"\s*,\s*", m.group(1)):
            decl.setdefault(name.strip(), n)
for name, dline in sorted(decl.items(), key=lambda kv: kv[1]):
    rx = re.compile(r"\b%s\b" % re.escape(name))
    for n, l in enumerate(lines[: dline - 1], 1):
        if rx.search(l):
            print(f"{sys.argv[1]}:{n}: '{name}' used before its declaration at line {dline}")
            break
