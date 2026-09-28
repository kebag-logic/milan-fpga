"""Repeat the reviewers' current-contract scan over tracked first-party text."""
from pathlib import Path
import re
import subprocess

ROOT = Path('$LANES/602-phc-step-mr')
OUT = Path(__file__).resolve().parent
pattern = re.compile(r"(step|settime|adjtime|re-?base)[^|]{0,80}\b(mr\b|MEDIA_RESET|media.clock restart)|(\bmr\b|MEDIA_RESET)[^|]{0,80}(PHC step|settime|adjtime|re-?base)", re.I)
files = subprocess.check_output(['rtk', 'proxy', 'git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
lines = []
for rel in files:
    if not rel or rel.startswith(('docs/history/', 'external/', 'third_party/', 'protocol-processor/', 'gptp-processor/')):
        continue
    p = ROOT / rel
    if p.suffix not in ('.md', '.py', '.sv', '.cpp') and p.name != 'Makefile':
        continue
    for n, line in enumerate(p.read_text().splitlines(), 1):
        if pattern.search(line):
            lines.append(f'{rel}:{n}:{line}')
text = '\n'.join(lines) + '\n'
assert len(text.encode()) < 190000
(OUT/'stale_doc_scan.txt').write_text(text)
print(text)
print(f'{len(lines)} candidate lines; each requires contextual classification, not an automatic stale verdict.')
