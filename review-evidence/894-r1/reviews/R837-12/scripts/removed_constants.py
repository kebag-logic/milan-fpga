"""Every #define in sw/firmware/ctrl at the base that the head no longer defines anywhere in sw/, and each line of the
sweep's scope (figure_sweep.py's file set at the head, and the PR body) that names one.
Usage: python3 -I -B removed_constants.py <repo-root> <base-sha> <pr-body.md> <out.tsv>"""
import re
import subprocess
import sys
from pathlib import Path

root, base, body, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])


def git(*a):
    return subprocess.run(['git', '-C', str(root), *a], capture_output=True, text=True, check=True).stdout


DEF = re.compile(r'^#define\s+([A-Z][A-Z0-9_]+)\b', re.M)
names = set()
for f in git('ls-tree', '-r', '--name-only', base, '--', 'sw/firmware/ctrl').split():
    if f.endswith(('.h', '.c')):
        names |= set(DEF.findall(git('show', f'{base}:{f}')))
now = set()
for f in git('ls-files', 'sw').split():
    if f.endswith(('.h', '.c')):
        try:
            now |= set(DEF.findall((root / f).read_text()))
        except (UnicodeDecodeError, FileNotFoundError):
            pass
gone = sorted(names - now)
SRC = ('.c', '.h', '.py', '.cpp', '.hpp', '.sv', '.svh', '.ld', '.yaml', '.txt', '.sh', '.mk')
SKIP = ('third_party/', 'protocol-processor/', 'gptp-processor/', 'external/')
changed = git('diff', '--name-only', f'{base}..HEAD').split()
tracked = git('ls-files').split()
files = set(p for p in changed if p.endswith('.md'))
files |= set(p for p in tracked if p.endswith('README.md') and not p.startswith(SKIP))
files |= set(p for p in tracked if p.startswith(('sw/', 'tb/')) and p.endswith(SRC) and not p.startswith(SKIP))
pat = re.compile(r'\b(' + '|'.join(map(re.escape, gone)) + r')\b') if gone else None
rows = []
for rel in sorted(files) + ['PR-BODY']:
    p = body if rel == 'PR-BODY' else root / rel
    try:
        text = p.read_text()
    except (UnicodeDecodeError, FileNotFoundError):
        continue
    for no, line in enumerate(text.splitlines(), 1):
        for m in set(pat.findall(line)) if pat else ():
            rows.append((rel, no, m, line.strip()[:300]))
with out.open('w') as fh:
    fh.write('# gone: ' + ' '.join(gone) + '\n')
    for r in rows:
        fh.write('\t'.join(map(str, r)) + '\n')
print(f'{len(gone)} constants gone, {len(rows)} lines naming one')
