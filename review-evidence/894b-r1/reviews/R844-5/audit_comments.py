#!/usr/bin/env python3
"""Check added non-Markdown delta lines for prohibited source-comment identifiers.
Usage: python3 -B audit_comments.py REPOSITORY
The narrow diff is also manually inspected to distinguish comments from runtime text.
"""
import re
import subprocess
import sys

diff = subprocess.check_output(['git', '-C', sys.argv[1], 'diff', '--unified=0', '8883d499..d0a2a160',
                               '--', 'sw', 'tb'], text=True)
path = ''
found = []
for line in diff.splitlines():
    if line.startswith('+++ b/'):
        path = line[6:]
    elif line.startswith('+') and not path.endswith('.md'):
        if re.search(r'issuecomment-\d+|\[?[AR]\d+-\d+|\bround[ -]+\d+|\bB\d{2}\b|\b894b\b', line):
            found.append((path, line))
for path, line in found:
    print(path, line)
print('Added source identifier matches:', len(found))
raise SystemExit(bool(found))
