"""Put the instruction-cache section into the harness README, its tables from readme_tables.py.

usage: assemble_readme.py README DRAFT TABLE_DIR [KEY=TEXT_FILE ...]
DRAFT holds @@KEY@@ placeholders; each table key reads TABLE_DIR/tbl-<section>.md, and each
KEY=TEXT_FILE pair fills a prose placeholder. The section replaces an earlier copy of itself, or
goes in before "## Controls and self-test".
"""
import re
import sys
from pathlib import Path

readme, draft, tables = Path(sys.argv[1]), Path(sys.argv[2]).read_text(), Path(sys.argv[3])
fills = {'SWEEP': 'sweep', 'CPU': 'cpu', 'BACKLOG': 'backlog', 'FANOUT': 'fanout', 'STILL': 'still_missing',
         'AREA': 'area', 'XIP': 'xip', 'COUNTS': 'counts'}
for key, section in fills.items():
    path = tables / f'tbl-{section}.md'
    if path.exists():
        draft = draft.replace(f'@@{key}@@', path.read_text().strip('\n'))
for pair in sys.argv[4:]:
    key, _, text = pair.partition('=')
    draft = draft.replace(f'@@{key}@@', Path(text).read_text().strip('\n'))
left = re.findall(r'@@\w+@@', draft)
if left:
    raise SystemExit(f'unfilled placeholders: {left}')
text = readme.read_text()
section = draft.strip('\n') + '\n\n'
start = text.find('## The instruction cache\n')
if start >= 0:
    end = text.index('## Controls and self-test\n')
    text = text[:start] + section + text[end:]
else:
    at = text.index('## Controls and self-test\n')
    text = text[:at] + section + text[at:]
readme.write_text(text)
print('README section written')
