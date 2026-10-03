#!/usr/bin/env python3
"""Count files in an evidence tree that still carry the capture values the packet's redaction
masks as <capture-channels> and <capture-format>. Prints only paths, counts and page line numbers,
never the values. The format token is read at run time from a private file, so this script does
not spell it. usage: privacy_capture_scan.py <tree> <format-token-file> [page.md ...]"""
import os, re, sys
root, tokfile, pages = sys.argv[1], sys.argv[2], sys.argv[3:]
fmt = open(tokfile, 'rb').read().strip()
TOKENS = {'channel-count filename': re.compile(rb'cap-all-\d+ch\.raw'),
          'capture sample format': re.compile(rb'\b' + re.escape(fmt) + rb'\b')}
hits = {}
for d, _, fs in os.walk(root):
    for f in fs:
        p = os.path.join(d, f)
        b = open(p, 'rb').read()
        for k, rx in TOKENS.items():
            n = len(rx.findall(b))
            if n:
                hits.setdefault(k, []).append((os.path.relpath(p, root), n))
for k in TOKENS:
    L = hits.get(k, [])
    print(f'{k}: {len(L)} file(s)')
    for p, n in sorted(L):
        print(f'  {p} x{n}')
for page in pages:
    for i, line in enumerate(open(page, encoding='utf-8'), 1):
        for k, rx in TOKENS.items():
            if rx.search(line.encode()):
                print(f'page {os.path.basename(page)}:{i}: {k}')
