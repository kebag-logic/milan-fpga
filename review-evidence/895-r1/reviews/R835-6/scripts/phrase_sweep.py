#!/usr/bin/env python3
"""phrase_sweep.py REPO BASE HEAD

Reviewer sweep: for every markdown line HEAD adds or changes against BASE (git diff -U0), print each clause that
uses a present-time marker ("this head", "the head", "at the head", "head's", "now", "currently", "today"), with
file:line and the section heading it sits under, so each can be classed by hand against the image it describes.
Read-only."""
import re
import subprocess
import sys

repo, base, head = sys.argv[1:4]
PAT = re.compile(r"\b(this head|the head|at the head|head's|now|currently|today)\b", re.I)
diff = subprocess.run(['git', '-C', repo, 'diff', '-U0', '--no-color', f'{base}..{head}', '--', '*.md'],
                      capture_output=True, text=True, check=True).stdout
path = None
added = {}
for line in diff.splitlines():
    if line.startswith('+++ '):
        path = line[6:] if line.startswith('+++ b/') else None
    elif line.startswith('@@'):
        n = int(re.search(r'\+(\d+)', line).group(1))
    elif line.startswith('+') and path:
        added.setdefault(path, []).append(n)
        n += 1
total = 0
for path, lines in sorted(added.items()):
    text = subprocess.run(['git', '-C', repo, 'show', f'{head}:{path}'], capture_output=True, text=True,
                          check=True).stdout.splitlines()
    for ln in lines:
        heading = next((text[i] for i in range(ln - 1, -1, -1) if text[i].startswith('#')), '(none)')
        for m in PAT.finditer(text[ln - 1]):
            total += 1
            s = text[ln - 1]
            ctx = re.sub(r'\s+', ' ', s[max(0, m.start() - 140):m.end() + 140])
            print(f'{path}:{ln} [{heading[:70]}] <{m.group(0)}>\n    ...{ctx}...')
print(f'{total} hits in {sum(map(len, added.values()))} added markdown lines over {len(added)} files')
