#!/usr/bin/env python3
"""R837-13-S1's retired-artifact sweep: every file this PR deletes (git diff --diff-filter=D base..HEAD), named by its
path, its file name and its stem, and the prose names the documents give it (PROSE), and every line in the sweep's
scope that names one: figure_sweep.py's file set at the head (every Markdown file the PR changes, every first-party
README, every first-party source line under sw/ and tb/) and the PR body. Removed constants are removed_constants.py's.
usage: retired_artifacts.py <repo-root> <base-sha> <pr-body.md> <out.tsv>"""
import re
import subprocess
import sys
from pathlib import Path

root, base, body, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
#: the prose names section 13 and FR_NFR give the one file this PR deletes, ctrl_retry_search.py (THE TIERS, 3f469cef)
PROSE = {'sw/firmware/ctrl/test/ctrl_retry_search.py': [r"THE RETRY's search", r'\bretry search\b', r'\bloop search\b',
                                                       r"search of the loop's choices"]}


def git(*a):
    return subprocess.run(['git', '-C', str(root), *a], capture_output=True, text=True, check=True).stdout


deleted = git('diff', '--diff-filter=D', '--name-only', f'{base}..HEAD').split()
pats = []
for f in deleted:
    name = f.rsplit('/', 1)[-1]
    stem = name.rsplit('.', 1)[0]
    pats += [(f, re.escape(f)), (f, r'(?<![\w/])' + re.escape(name)), (f, r'\b' + re.escape(stem) + r'\b')]
    pats += [(f, p) for p in PROSE.get(f, [])]
SRC = ('.c', '.h', '.py', '.cpp', '.hpp', '.sv', '.svh', '.ld', '.yaml', '.txt', '.sh', '.mk')
SKIP = ('third_party/', 'protocol-processor/', 'gptp-processor/', 'external/')
changed = git('diff', '--name-only', f'{base}..HEAD').split()
tracked = git('ls-files').split()
files = set(p for p in changed if p.endswith('.md'))
files |= set(p for p in tracked if p.endswith('README.md') and not p.startswith(SKIP))
files |= set(p for p in tracked if p.startswith(('sw/', 'tb/')) and p.endswith(SRC) and not p.startswith(SKIP))
rows = []
for rel in sorted(files) + ['PR-BODY']:
    p = body if rel == 'PR-BODY' else root / rel
    try:
        text = p.read_text()
    except (UnicodeDecodeError, FileNotFoundError):
        continue
    for no, line in enumerate(text.splitlines(), 1):
        hit = sorted({f for f, pat in pats if re.search(pat, line)})
        for f in hit:
            rows.append((rel, no, f, line.strip()[:300]))
with out.open('w') as fh:
    fh.write('# deleted: ' + ' '.join(deleted) + '\n')
    for r in rows:
        fh.write('\t'.join(map(str, r)) + '\n')
print(f'{len(deleted)} files deleted, {len(rows)} lines naming one')
