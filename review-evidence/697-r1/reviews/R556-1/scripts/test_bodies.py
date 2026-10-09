#!/usr/bin/env python3
"""Compare GoogleTest case bodies between a source and an exported test file.

Usage: test_bodies.py SRC EXP
Prints dropped, added and changed cases. REQ annotation lines are ignored.
"""
import re, sys

HEAD = re.compile(r'^(TEST|TEST_F|TEST_P|TYPED_TEST)\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)')

def cases(path):
    lines = open(path, encoding='utf-8').read().splitlines()
    out, cur, depth, body = {}, None, 0, []
    for ln in lines:
        if cur is None:
            m = HEAD.match(ln)
            if m:
                cur = m.group(2) + '.' + m.group(3)
                body, depth, opened = [ln], ln.count('{') - ln.count('}'), '{' in ln
                if opened and depth == 0:
                    out[cur] = body; cur = None
            continue
        body.append(ln)
        depth += ln.count('{') - ln.count('}')
        if depth <= 0 and any('{' in b for b in body):
            out[cur] = [b for b in body if not b.strip().startswith('// REQ:')]
            cur = None
    return out

s, e = cases(sys.argv[1]), cases(sys.argv[2])
print(f'source cases {len(s)} exported cases {len(e)}')
for k in sorted(set(s) - set(e)):
    print('DROPPED', k)
for k in sorted(set(e) - set(s)):
    print('ADDED', k)
for k in sorted(set(s) & set(e)):
    if s[k] != e[k]:
        print('CHANGED', k)
