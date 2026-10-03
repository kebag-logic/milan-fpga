#!/usr/bin/env python3
"""Rough use-before-declaration scan of one SystemVerilog module file.

Not xvlog: a textual approximation for evidence only. Comments and strings are
blanked; a module-scope `logic`/`wire`/`reg` declaration (including
comma-separated names and packed/unpacked dimensions) records each declared
name's line; any earlier whole-word occurrence of the name in code is reported.
Port declarations (in the module header) count as declared at the header.
usage: ubd_scan.py <file.sv>
"""
import re
import sys

src = open(sys.argv[1]).read()
# blank comments and strings, keeping newlines so line numbers hold
def blank(m):
    return re.sub(r"[^\n]", " ", m.group(0))
code = re.sub(r"//[^\n]*|/\*.*?\*/|\"(?:\\.|[^\"\\])*\"", blank, src, flags=re.S)
lines = code.split("\n")

# end of the module header: the first ");" after "module"
hdr_end = None
m = re.search(r"\bmodule\b", code)
depth = 0
for i in range(m.end(), len(code)):
    c = code[i]
    if c == "(":
        depth += 1
    elif c == ")":
        depth -= 1
        if depth == 0 and code[i + 1:].lstrip().startswith(";"):
            hdr_end = code.count("\n", 0, i) + 1
            break

decl = {}
stmt_re = re.compile(r"^\s*(?:logic|wire|reg)\b([^;]*);", re.M)
for mm in stmt_re.finditer(code):
    line = code.count("\n", 0, mm.start()) + 1
    if hdr_end and line <= hdr_end:
        continue
    body = mm.group(1)
    body = re.sub(r"\[[^\]]*\]", " ", body)          # dimensions
    body = re.sub(r"\bsigned\b|\bunsigned\b", " ", body)
    body = re.sub(r"=[^,]*", " ", body)               # initialisers
    for name in re.findall(r"\b([A-Za-z_][A-Za-z0-9_$]*)\b", body):
        decl.setdefault(name, line)

late = []
for name, dline in sorted(decl.items(), key=lambda kv: kv[1]):
    pat = re.compile(r"(?<![A-Za-z0-9_$.])" + re.escape(name) + r"(?![A-Za-z0-9_$])")
    for i in range(0, dline - 1):
        if (hdr_end is None or i + 1 > hdr_end) and pat.search(lines[i]):
            late.append((name, i + 1, dline))
            break
for name, use, d in late:
    print(f"{name}: used at {use}, declared at {d}")
print(f"{len(late)} identifier(s) used before declaration, {len(decl)} module-scope declarations scanned")
