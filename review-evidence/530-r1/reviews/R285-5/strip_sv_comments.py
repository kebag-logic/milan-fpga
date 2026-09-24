#!/usr/bin/env python3
"""Strip // and /* */ comments from SystemVerilog (string-aware), normalise
whitespace, print sha256 of the result per git revision.

usage: strip_sv_comments.py <repo> <path> <rev> [<rev> ...]
"""
import hashlib
import subprocess
import sys


def strip(src: str) -> str:
    out = []
    i, n = 0, len(src)
    while i < n:
        c = src[i]
        if c == '"':
            j = i + 1
            while j < n and src[j] != '"':
                j += 2 if src[j] == '\\' else 1
            out.append(src[i:j + 1])
            i = j + 1
        elif src.startswith('//', i):
            j = src.find('\n', i)
            i = n if j < 0 else j
        elif src.startswith('/*', i):
            j = src.find('*/', i + 2)
            i = n if j < 0 else j + 2
            out.append(' ')
        else:
            out.append(c)
            i += 1
    return '\n'.join(' '.join(l.split()) for l in ''.join(out).splitlines()
                     if l.strip())


def main() -> int:
    repo, path, revs = sys.argv[1], sys.argv[2], sys.argv[3:]
    for rev in revs:
        blob = subprocess.run(['git', '-C', repo, 'show', f'{rev}:{path}'],
                              check=True, capture_output=True).stdout
        h = hashlib.sha256(strip(blob.decode('utf-8')).encode()).hexdigest()
        print(f'{rev} {path} stripped-sha256 {h}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
