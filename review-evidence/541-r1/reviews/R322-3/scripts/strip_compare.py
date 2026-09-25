#!/usr/bin/env python3
"""Compare a SystemVerilog file at two commits with comments and whitespace
removed. Usage: strip_compare.py <repo> <rev_a> <rev_b> <path>
Exit 0 when the stripped token streams are identical, 1 otherwise."""
import re, subprocess, sys, hashlib

def strip(text: str) -> str:
    out, i, n = [], 0, len(text)
    while i < n:
        if text.startswith('"', i):
            j = i + 1
            while j < n and text[j] != '"':
                j += 2 if text[j] == '\\' else 1
            out.append(text[i:j + 1]); i = j + 1
        elif text.startswith('//', i):
            j = text.find('\n', i); i = n if j < 0 else j
        elif text.startswith('/*', i):
            j = text.find('*/', i + 2); i = n if j < 0 else j + 2
        else:
            out.append(text[i]); i += 1
    return re.sub(r'\s+', ' ', ''.join(out)).strip()

repo, a, b, path = sys.argv[1:5]
res = []
for rev in (a, b):
    blob = subprocess.run(['git', '-C', repo, 'show', f'{rev}:{path}'],
                          check=True, capture_output=True, text=True).stdout
    s = strip(blob)
    res.append(s)
    print(f'{rev} {path} raw_sha256={hashlib.sha256(blob.encode()).hexdigest()} '
          f'stripped_sha256={hashlib.sha256(s.encode()).hexdigest()} stripped_len={len(s)}')
same = res[0] == res[1]
print('IDENTICAL' if same else 'DIFFERENT')
sys.exit(0 if same else 1)
