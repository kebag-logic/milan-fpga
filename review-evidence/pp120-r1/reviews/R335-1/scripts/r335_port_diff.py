#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Diff the ANSI port list (direction, type/width, name) of one module
between two trees. Usage: r335_port_diff.py <base-file> <head-file> <module>"""
import re, sys

def ports(path, module):
    text = open(path).read()
    m = re.search(r'\bmodule\s+' + module + r'\b(.*?)\)\s*;', text, re.S)
    hdr = m.group(1)
    hdr = re.sub(r'//[^\n]*', '', hdr)
    hdr = re.sub(r'/\*.*?\*/', '', hdr, flags=re.S)
    body = hdr[hdr.rfind('#(') if False else 0:]
    # the port list follows the parameter list's closing ") ("
    idx = [mm.end() for mm in re.finditer(r'\)\s*\(', body)]
    body = body[idx[0]:] if idx else body
    out, cur = [], None
    for chunk in body.split(','):
        c = ' '.join(chunk.split())
        if not c:
            continue
        mm = re.match(r'(input|output|inout)\s+(.*?)\s*(\w+)$', c)
        if mm:
            cur = (mm.group(1), mm.group(2))
            out.append((mm.group(1), mm.group(2), mm.group(3)))
        elif re.match(r'^\w+$', c) and cur:
            out.append((cur[0], cur[1], c))
    return out

b, h = ports(sys.argv[1], sys.argv[3]), ports(sys.argv[2], sys.argv[3])
bs, hs = set(b), set(h)
print(f"{sys.argv[3]}: base {len(b)} ports, head {len(h)} ports")
for p in b:
    if p not in hs: print("REMOVED/CHANGED", p)
for p in h:
    if p not in bs: print("ADDED", p)
bo = [p for p in b if p in hs]; ho = [p for p in h if p in bs]
print("common-port order identical:", bo == ho)
