#!/usr/bin/env python3
"""Reviewer-owned: for every relative link whose label names C identifiers, verify each identifier
occurs in the target file (inside the linked line range when one is given). Also list prose tokens
that look like unlinked references the shipped checker does not pattern-match.
Usage: check_link_labels.py <clone>"""
import re, sys
from pathlib import Path
root = Path(sys.argv[1])
LINK = re.compile(r"\[([^\]\n]+)\]\(([^\s)]+)\)")
pages = sorted(list(root.glob('*.md')) + list((root / 'doc').rglob('*.md')))
bad = 0; checked = 0; cand = []
for page in pages:
    infence = False
    for n, line in enumerate(page.read_text().splitlines(), 1):
        if re.match(r'^\s*(~~~|```)', line):
            infence = not infence; continue
        if infence: continue
        for label, href in LINK.findall(line):
            if href.startswith('http'): continue
            path, _, frag = href.partition('#')
            target = (page.parent / path).resolve() if path else page
            if not target.is_file() or target.suffix not in ('.c', '.h', '.txt', '.zephyr', '.py', '.yml'):
                continue
            idents = [w for w in re.findall(r'\b[A-Za-z_][A-Za-z0-9_]*\b', label) if '_' in w]
            if not idents: continue
            text = target.read_text().splitlines()
            m = re.fullmatch(r'L(\d+)(?:-L(\d+))?', frag)
            if m:
                a = int(m[1]); b = int(m[2] or m[1]); text = text[a - 1:b]
            body = '\n'.join(text)
            for w in idents:
                checked += 1
                if not re.search(r'\b' + re.escape(w) + r'\b', body):
                    bad += 1; print(f'MISS {page.relative_to(root)}:{n}: label "{w}" not in {href}')
        prose = LINK.sub(' ', line)
        for tok in re.findall(r'\bC11\b|\bSPDX\b|\bKconfig\b|\bWest\b|\bctypes\b|\bvenv\b|\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b|\b\w+\.(?:txt|json|toml|cfg)\b', prose):
            cand.append(f'{page.relative_to(root)}:{n}: {tok}')
print(f'# identifier labels checked: {checked}; missing: {bad}')
print('# prose tokens for manual reference review:')
for c in cand: print('CAND ' + c)
