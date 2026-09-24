#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Print the ANSI port header of a module (from 'module NAME' to the closing ');')
with comments stripped and whitespace normalised, one port declaration per line."""
import re, sys
text = sys.stdin.read()
name = sys.argv[1]
m = re.search(r'^\s*module\s+' + re.escape(name) + r'\b', text, re.M)
body = text[m.start():]
body = re.sub(r'//[^\n]*', '', body)
body = re.sub(r'/\*.*?\*/', '', body, flags=re.S)
# skip parameter list #( ... ) then take the port list ( ... );
i = body.index('(')
if body[:i].rstrip().endswith('#'):
    depth = 0
    for j in range(i, len(body)):
        depth += body[j] == '('; depth -= body[j] == ')'
        if depth == 0: break
    i = body.index('(', j + 1)
depth = 0
for j in range(i, len(body)):
    depth += body[j] == '('; depth -= body[j] == ')'
    if depth == 0: break
ports = body[i + 1:j]
for p in ports.split(','):
    p = ' '.join(p.split())
    if p: print(p)
