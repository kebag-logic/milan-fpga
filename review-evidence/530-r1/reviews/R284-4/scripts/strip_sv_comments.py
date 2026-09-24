#!/usr/bin/env python3
"""Print sha256 of a SystemVerilog blob with // and /* */ comments removed
(string-literal aware) and whitespace runs collapsed, for each git revision.
Usage: strip_sv_comments.py <repo> <path> <rev>..."""
import hashlib, subprocess, sys

def strip(src: str) -> str:
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if c == '"':
            j = i + 1
            while j < n and src[j] != '"':
                j += 2 if src[j] == '\\' else 1
            out.append(src[i:j + 1]); i = j + 1
        elif src.startswith('//', i):
            j = src.find('\n', i); i = n if j < 0 else j
        elif src.startswith('/*', i):
            j = src.find('*/', i + 2); i = n if j < 0 else j + 2; out.append(' ')
        else:
            out.append(c); i += 1
    return ' '.join(''.join(out).split())

repo, path, revs = sys.argv[1], sys.argv[2], sys.argv[3:]
for r in revs:
    blob = subprocess.run(['git', '-C', repo, 'show', f'{r}:{path}'], capture_output=True, check=True).stdout.decode()
    s = strip(blob)
    print(r, hashlib.sha256(s.encode()).hexdigest(), len(s))
