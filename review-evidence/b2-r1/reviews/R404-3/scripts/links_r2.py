#!/usr/bin/env python3
"""Resolve every relative link and fragment on the three changed pages with
the repository's own heading/anchor reader (scripts/gen_toc.py headings()).
Usage (pinned Markdown env): links_r2.py <clone>"""
import re, sys
from pathlib import Path
repo = Path(sys.argv[1]); sys.path.insert(0, str(repo / 'scripts'))
import gen_toc as G
ok = bad = ext = 0
for rel in ('docs/findings/606_FIRST_BIND_MEASUREMENT.md', 'docs/findings/608_75_WITHDRAWAL_AND_RESTART.md',
            'docs/findings/README.md'):
    page = repo / rel
    for m in re.finditer(r"\]\(([^)\s]+)\)", page.read_text()):
        link = m.group(1)
        if link.startswith(('http://', 'https://', 'mailto:')):
            ext += 1; continue
        path, _, frag = link.partition('#')
        tgt = page if not path else (page.parent / path)
        good = tgt.exists()
        if good and frag:
            good = frag in {a for _, _, a in G.headings(tgt.read_text())}
        ok += good; bad += not good
        if not good:
            print('  MISS', rel, '->', link)
print(f'relative links/fragments: {ok} resolve, {bad} do not; external links skipped: {ext}')
sys.exit(1 if bad else 0)
