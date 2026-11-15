#!/usr/bin/env python3
"""text_identity.py REPO BASE HEAD PATH...: for each PATH, compare BASE and HEAD
(1) the word sequence of the whole file with comment markers (//, #:, #) removed and
whitespace collapsed, and (2) the non-comment lines exactly. Prints one line a file."""
import hashlib, re, subprocess, sys

def show(repo, rev, path):
    return subprocess.run(['git', '-C', repo, 'show', f'{rev}:{path}'], check=True,
                          capture_output=True, text=True).stdout

def words(text):
    out = []
    for line in text.splitlines():
        s = line.strip()
        s = re.sub(r'^(//+|#:|#)\s?', '', s)
        out.extend(s.split())
    return ' '.join(out)

def code(text):
    return [l.rstrip() for l in text.splitlines()
            if l.strip() and not re.match(r'\s*(//|#)', l)]

repo, base, head, *paths = sys.argv[1:]
bad = 0
for p in paths:
    a, b = show(repo, base, p), show(repo, head, p)
    wa, wb = words(a), words(b)
    ha, hb = (hashlib.sha256(w.encode()).hexdigest() for w in (wa, wb))
    same_code = code(a) == code(b)
    ok = ha == hb and same_code
    bad += not ok
    print(f'{p} words {ha[:16]} {hb[:16]} code-lines {"EQUAL" if same_code else "DIFFER"} '
          f'lines {len(a.splitlines())}->{len(b.splitlines())} {"IDENTICAL-TEXT" if ok else "CHANGED"}')
sys.exit(1 if bad else 0)
