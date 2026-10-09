#!/usr/bin/env python3
"""Report unlinked file/standard references and long sentences in Markdown docs.

Usage: doc_lint.py REPO
Code fences are skipped. Link targets are checked for existence when relative.
"""
import re, sys
from pathlib import Path
root = Path(sys.argv[1])
REF = re.compile(r'(\b[\w./-]+\.(?:md|py|c|h|cpp|hpp|json|yml|ratchet)\b|IEEE 1722(?:\.1)?-20\d\d|Milan v1\.2|issue \d+)')
LINK = re.compile(r'\[[^\]]*\]\([^)]*\)')
files = [root / 'README.md', root / 'CONTRIBUTING.md', root / 'SECURITY.md', root / 'CHANGELOG.md', *sorted((root / 'docs').glob('*.md'))]
for f in files:
    text = f.read_text()
    fence = False
    for n, line in enumerate(text.splitlines(), 1):
        if line.startswith('```'):
            fence = not fence; continue
        if fence:
            continue
        for m in LINK.finditer(line):
            target = re.search(r'\(([^)]*)\)', m.group(0)).group(1).split('#')[0]
            if target and not target.startswith(('http', 'mailto')):
                if not (f.parent / target).exists():
                    print(f'{f.relative_to(root)}:{n}: BROKEN LINK {target}')
        bare = LINK.sub('', line)
        bare = re.sub(r'`[^`]*`', lambda m: m.group(0) if not REF.search(m.group(0)) else m.group(0), bare)
        for m in REF.finditer(bare):
            print(f'{f.relative_to(root)}:{n}: UNLINKED {m.group(0)!r}')
        if f.name not in ('TESTS.md', 'TRACEABILITY.md', 'COVERAGE.md') and not line.startswith('|'):
            for s in re.split(r'(?<=[.!?])\s+', LINK.sub('L', line)):
                if len(s.split()) > 25:
                    print(f'{f.relative_to(root)}:{n}: LONG({len(s.split())}) {s[:80]}')
