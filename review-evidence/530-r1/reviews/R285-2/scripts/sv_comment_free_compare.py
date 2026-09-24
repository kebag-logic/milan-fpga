#!/usr/bin/env python3
"""Compare SystemVerilog sources at two git revisions with comments removed.

Usage: sv_comment_free_compare.py <repo> <rev_a> <rev_b> [pathspec...]

For every file under the pathspecs that differs between the two revisions,
strips // and /* */ comments (string-literal aware), collapses whitespace
into single-space token separators, and reports whether the comment-free
token streams are identical. Also reports every changed diff line that is not
a pure comment line. Exit 0 only if every changed file is comment-free
identical.
"""
import hashlib
import subprocess
import sys


def strip_comments(src: str) -> str:
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
            out.append(' ')
            i = n if j < 0 else j + 2
        else:
            out.append(c)
            i += 1
    return ' '.join(''.join(out).split())


def show(repo, rev, path):
    return subprocess.run(['git', '-C', repo, 'show', f'{rev}:{path}'],
                          check=True, capture_output=True).stdout.decode()


def main():
    repo, a, b, *spec = sys.argv[1:]
    names = subprocess.run(['git', '-C', repo, 'diff', '--name-only', a, b,
                            '--', *spec], check=True, capture_output=True,
                           text=True).stdout.split()
    ok = True
    for p in names:
        sa, sb = strip_comments(show(repo, a, p)), strip_comments(show(repo, b, p))
        ha = hashlib.sha256(sa.encode()).hexdigest()
        hb = hashlib.sha256(sb.encode()).hexdigest()
        same = sa == sb
        ok &= same
        print(f'{p}: comment-free sha256 {a[:12]}={ha} {b[:12]}={hb} '
              f'{"IDENTICAL" if same else "DIFFERENT"}')
    diff = subprocess.run(['git', '-C', repo, 'diff', '-U0', '--no-color', a, b,
                           '--', *spec], check=True, capture_output=True,
                          text=True).stdout.splitlines()
    changed = [l for l in diff if l[:1] in '+-' and not l.startswith(('+++', '---'))]
    noncomment = [l for l in changed if l[1:].strip() and not l[1:].lstrip().startswith('//')]
    print(f'changed lines: {len(changed)}; not starting with //: {len(noncomment)}')
    for l in noncomment:
        print('  NONCOMMENT:', l)
    print('RESULT:', 'PASS' if ok and not noncomment else 'FAIL')
    return 0 if ok and not noncomment else 1


if __name__ == '__main__':
    sys.exit(main())
