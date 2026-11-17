#!/usr/bin/env python3
"""Supplement manual prose review and validate the four new fragment links."""
from pathlib import Path
import re
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'scripts'))
import gen_toc
import check_doc_style

paths = ['CONTRIBUTING.md', 'AGENTS.md', 'docs/testing/CI_WORKFLOWS.md']
anchors = {a for _, _, a in gen_toc.headings((root / 'CONTRIBUTING.md').read_text())}
assert '23-batched-merges' in anchors
links = []
for path in paths:
    for number, line in enumerate((root / path).read_text().splitlines(), 1):
        for label, target in re.findall(r'\[([^]]+)\]\(([^)]+)\)', line):
            if '#23-batched-merges' not in target:
                continue
            file, fragment = target.split('#', 1)
            actual = (root / path).parent / file if file else root / path
            assert actual.resolve() == root / 'CONTRIBUTING.md'
            assert fragment in anchors
            links.append((path, number, target))
            print('RESOLVES', path, number, target)
assert len(links) == 4
assert '23-batched-mergez' not in anchors
print('Negative fragment control: rejected 23-batched-mergez')

paragraphs = {
 'CONTRIBUTING.md': [(189,190),(425,427),(429,430)],
 'AGENTS.md': [(298,300),(302,303),(305,306),(401,402),(404,405),(407,408)],
 'docs/testing/CI_WORKFLOWS.md': [(273,274),(276,277),(279,281)],
}
for path, ranges in paragraphs.items():
    lines = (root/path).read_text().splitlines()
    for first,last in ranges:
        text = ' '.join(lines[first-1:last])
        text = re.sub(r'\[([^]]+)\]\([^)]+\)', r'\1', text)
        text = re.sub(r'[*`]', '', text)
        words = len(check_doc_style.WORD.findall(text))
        assert words <= 30, (path, first, words)
        print(f'{path}:{first}-{last}: {words} words: {text.strip()}')
assert not subprocess.check_output(['git','diff','--ignore-all-space','--ignore-blank-lines','490d54ee..HEAD'],cwd=root)
print('Second commit: whitespace-only change confirmed.')
