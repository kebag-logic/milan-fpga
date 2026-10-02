#!/usr/bin/env python3
"""Diff a module's parameter and port header between two source files."""
import re, sys
def strip(t):
    t = re.sub(r'/\*.*?\*/', '', t, flags=re.S)
    return re.sub(r'//[^\n]*', '', t)
def groups(t, mod):
    i = re.search(r'\bmodule\s+%s\b' % mod, t).end()
    out = []
    while True:
        while t[i].isspace(): i += 1
        m = re.match(r'import\s+[\w:*,\s]+;', t[i:])
        if m: i += m.end(); continue
        if t[i] == '#': i += 1; continue
        if t[i] != '(': break
        d = 0; j = i
        while True:
            if t[j] == '(': d += 1
            elif t[j] == ')':
                d -= 1
                if d == 0: break
            j += 1
        out.append(t[i+1:j]); i = j + 1
    return out
def split(s):
    parts, d, cur = [], 0, ''
    for ch in s:
        if ch in '([{': d += 1
        if ch in ')]}': d -= 1
        if ch == ',' and d == 0: parts.append(cur); cur = ''
        else: cur += ch
    parts.append(cur)
    return [' '.join(p.split()) for p in parts if p.strip()]
def parse(path, mod):
    g = groups(strip(open(path).read()), mod)
    params, ports = {}, {}
    if len(g) == 2:
        last = ''
        for p in split(g[0]):
            m = re.match(r'(.*?)\b(\w+)\s*(?:\[[^\]]*\]\s*)*=\s*(.*)$', p)
            decl = m.group(1).strip() or last; last = decl
            params[m.group(2)] = (decl, m.group(3).strip())
    last = ''
    for p in split(g[-1]):
        m = re.match(r'(.*?)\b(\w+)\s*((?:\[[^\]]*\]\s*)*)$', p)
        decl = (m.group(1).strip() or last); last = decl
        ports[m.group(2)] = decl + (' ' + m.group(3) if m.group(3) else '')
    return params, ports
mod, a, b = sys.argv[1:4]
pa, oa = parse(a, mod); pb, ob = parse(b, mod)
print('params %d -> %d, ports %d -> %d' % (len(pa), len(pb), len(oa), len(ob)))
for k in pb:
    if k not in pa: print('PARAM ADDED', k, pb[k])
    elif pa[k] != pb[k]: print('PARAM CHANGED', k, pa[k], '->', pb[k])
for k in pa:
    if k not in pb: print('PARAM REMOVED', k)
for k in ob:
    if k not in oa: print('PORT ADDED', k, ob[k])
    elif oa[k] != ob[k]: print('PORT CHANGED', k, oa[k], '->', ob[k])
for k in oa:
    if k not in ob: print('PORT REMOVED', k)
