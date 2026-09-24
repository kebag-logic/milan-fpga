#!/usr/bin/env python3
"""Compare comment-free token streams of RTL files between two commits.

Usage: rtl_comment_free_equiv.py <repo> <base> <head> <path>...
Exit 0 when every path is identical after removing // and /* */ comments
and collapsing whitespace; exit 1 otherwise.
"""
import hashlib
import re
import subprocess
import sys


def strip_comments(text):
    out, i, n = [], 0, len(text)
    while i < n:
        c = text[i]
        if c == '"':
            j = i + 1
            while j < n and text[j] != '"':
                j += 2 if text[j] == '\\' else 1
            out.append(text[i:j + 1])
            i = j + 1
        elif text.startswith('//', i):
            j = text.find('\n', i)
            i = n if j < 0 else j
        elif text.startswith('/*', i):
            j = text.find('*/', i + 2)
            i = n if j < 0 else j + 2
            out.append(' ')
        else:
            out.append(c)
            i += 1
    return ' '.join(re.split(r'\s+', ''.join(out))).strip()


def blob(repo, rev, path):
    return subprocess.run(['git', '-C', repo, 'show', f'{rev}:{path}'],
                          check=True, capture_output=True, text=True).stdout


def main():
    repo, base, head, *paths = sys.argv[1:]
    rc = 0
    for p in paths:
        a, b = strip_comments(blob(repo, base, p)), strip_comments(blob(repo, head, p))
        ha, hb = (hashlib.sha256(x.encode()).hexdigest() for x in (a, b))
        same = a == b
        print(f'{p}: base={ha} head={hb} {"IDENTICAL" if same else "DIFFERENT"}')
        rc |= 0 if same else 1
    return rc


if __name__ == '__main__':
    sys.exit(main())
