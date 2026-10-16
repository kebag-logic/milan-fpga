#!/usr/bin/env python3
"""Compare two git revisions of C/C++/SystemVerilog files with comments removed.

Usage: strip_compare.py <repo> <rev-a> <rev-b> <path>...
Exit 0 when every path's comment-stripped token stream is identical and no
line in either revision ends in a backslash inside a // comment (which would
splice the next line into the comment in C/C++). Exit 1 otherwise.
"""
import subprocess
import sys


def strip(src: str) -> str:
    out, i, n = [], 0, len(src)
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
    return ' '.join(''.join(out).split())


def show(repo, rev, path):
    return subprocess.run(['git', '-C', repo, 'show', f'{rev}:{path}'],
                          check=True, capture_output=True, text=True).stdout


def main():
    repo, a, b, *paths = sys.argv[1:]
    bad = 0
    for p in paths:
        sa, sb = show(repo, a, p), show(repo, b, p)
        same = strip(sa) == strip(sb)
        splice = [k + 1 for k, line in enumerate(sb.splitlines())
                  if '//' in line and line.rstrip().endswith('\\')]
        print(f'{p}: stripped-identical={same} comment-splice-lines={splice}')
        bad |= (not same) or bool(splice)
    print('RESULT:', 'IDENTICAL' if not bad else 'DIFFERENT')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
