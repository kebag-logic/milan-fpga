#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""For core files whose line positions are preserved, check every clause reference
left in a head comment against the original comment on the same line, or, for
references with no same-line origin, anywhere in the original file's comments.
usage: refcheck.py <repo> <old-rev> <new-rev>"""
import re, subprocess, sys
repo, old, new = sys.argv[1:4]
TOK = re.compile(r'R"([^ ()\\\t\r\n]*)\(.*?\)\1"|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*.*?\*/', re.S)
NUM = re.compile(r'(?:(Table|Figure|Annex) )?(B(?:\.\d+)*|\d+(?:[.-]\d+)+|\d+)')
def comments(text):
    out = {}
    for m in TOK.finditer(text):
        if m[0].startswith(('//', '/*')):
            line = text.count('\n', 0, m.start()) + 1
            out.setdefault(line, []).append(m[0])
    return out
files = 'src/adp.c src/acmp.c src/maap.c include/adp.h include/acmp.h include/maap.h include/wire.h'.split()
total = same = elsewhere = 0
missing = []
for f in files:
    a = subprocess.check_output(['git', '-C', repo, 'show', f'{old}:{f}'], text=True)
    b = subprocess.check_output(['git', '-C', repo, 'show', f'{new}:{f}'], text=True)
    ca, cb = comments(a), comments(b)
    alltext = ' '.join(' '.join(v) for v in ca.values())
    for line, toks in cb.items():
        for t in toks:
            body = t.strip('/* ')
            if body.startswith('SPDX') or body.startswith('REQ:'):
                continue
            for ref in re.split(r';\s*', body):
                std = re.match(r'(IEEE 1722\.1-2021|IEEE 1722-2016|Milan v1\.2) (.*)', ref)
                if not std:
                    missing.append((f, line, ref, 'unparsed')); continue
                for kind, num in NUM.findall(std[2]):
                    total += 1
                    key = (kind + ' ' if kind else '') + num
                    orig = ' '.join(ca.get(line, []))
                    if num in orig:
                        same += 1
                    elif num in alltext:
                        elsewhere += 1
                    else:
                        missing.append((f, line, std[1] + ' ' + key, 'not in original comments'))
print(f'references {total}: same line {same}; elsewhere in original comments {elsewhere}; new {len(missing)}')
for m in missing:
    print('NEW', *m)
