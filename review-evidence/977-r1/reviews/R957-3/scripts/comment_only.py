#!/usr/bin/env python3
"""Usage: python3 -I comment_only.py <repo> <old> <new> <path>...: for each C/C++ source or header, compare the token
streams of the two revisions with comments and whitespace removed (string and char literals kept); for '#'-comment text
files, compare the lines that are not comments. Prints SAME or DIFF per path; exit 1 on any DIFF."""
import re, subprocess, sys
repo, old, new, paths = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
TOK = re.compile(r'//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|\s+|.', re.S)
def show(rev, p):
    return subprocess.run(['git', '-C', repo, 'show', f'{rev}:{p}'], capture_output=True, text=True, check=True).stdout
def c_tokens(text):
    return [t for t in TOK.findall(text) if not (t.startswith('//') or t.startswith('/*') or t.isspace())]
def hash_lines(text):
    return [l.strip() for l in text.splitlines() if l.strip() and not l.lstrip().startswith('#')]
bad = 0
for p in paths:
    a, b = show(old, p), show(new, p)
    f = c_tokens if re.search(r'\.(c|h|cpp|hpp)$', p) else hash_lines
    same = f(a) == f(b)
    bad |= not same
    print(('SAME ' if same else 'DIFF ') + p)
sys.exit(1 if bad else 0)
