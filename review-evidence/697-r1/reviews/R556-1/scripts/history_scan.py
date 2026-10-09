#!/usr/bin/env python3
"""Scan every commit message, identity and reachable blob for privacy terms.

Usage: history_scan.py REPO REV [EXTRA_TERMS_FILE]
EXTRA_TERMS_FILE holds one private term per line (personal names, product names,
device and instrument names, hosts); it is kept with the reviewer and not published.
Prints per-pattern hit counts and up to 3 sample hits per pattern.
"""
import re, subprocess, sys, collections
repo, rev = sys.argv[1], sys.argv[2]
def git(*a):
    return subprocess.check_output(['git', '-C', repo, *a])
P = {
 'ai-words': r'(?i)\b(AI[- ]generated|co-authored-by|generated with|assistant|chatbot)\b',
 'network-and-devices': r'(/dev/tty\w+|192\.168\.\d+\.\d+|\b10\.\d+\.\d+\.\d+\b)',
 'host-paths': r'(/home/|/Users/|/data/|/tmp/|/mnt/|/opt/|C:\\\\|~/)',
 'emails': r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}',
 'lane-labels': r'\b(lane [A-Z0-9]+|[AR]\d{3}(-\d+)?(-F\d+)?)\b',
 'issue-refs': r'#\d{3,}',
 'secrets': r'(gh[pousr]_[A-Za-z0-9]{20,}|BEGIN [A-Z ]*PRIVATE KEY)',
 'milan-paths': r'sw/firmware|third_party|milan-fpga',
}
if len(sys.argv) > 3:
    terms = [l.strip() for l in open(sys.argv[3]) if l.strip()]
    P['private-terms'] = r'(?i)\b(' + '|'.join(re.escape(x) for x in terms) + r')\b'
hits = collections.defaultdict(list)
commits = git('rev-list', rev).decode().split()
ids = collections.Counter()
for c in commits:
    meta = git('show', '-s', '--format=%an <%ae>|%cn <%ce>|%B', c).decode()
    ids[meta.split('|')[0] + ' / ' + meta.split('|')[1]] += 1
    for k, p in P.items():
        for m in re.finditer(p, meta):
            hits[k].append(('commit ' + c[:9], m.group(0)))
objs = git('rev-list', '--objects', rev).decode().splitlines()
paths = {}
for line in objs:
    oid, _, path = line.partition(' ')
    paths.setdefault(oid, path)
blobs = 0
for oid, path in paths.items():
    if git('cat-file', '-t', oid).strip() != b'blob':
        continue
    blobs += 1
    text = git('cat-file', 'blob', oid).decode('utf-8', 'replace')
    for k, p in P.items():
        for m in re.finditer(p, text):
            hits[k].append((f'{path}@{oid[:9]}', m.group(0)))
print('commits', len(commits), 'blobs', blobs)
print('identities', dict(ids))
for k in P:
    h = hits.get(k, [])
    vals = collections.Counter(v for _, v in h)
    print(f'{k}: {len(h)} hits; distinct {dict(vals.most_common(15))}')
    for loc, v in h[:3]:
        print('    ', loc, repr(v))
