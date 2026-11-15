# Copied unchanged from the R837-11 review's packet (review-evidence/894-r1/reviews/R837-11/scripts/constant_history.py), by its reviewer; run here by the author (R837-11-F3).
"""Every value each stated constant took over a PR's commits, and the ones the head no longer states.

Usage: python3 -I -B constant_history.py <repo-root> <base-sha> <out.txt>

Firmware: every `#define NAME <expr>` with a numeric literal in sw/firmware/ctrl/**/*.h and *.c. Model: the stated
tables' literal `name=value` / `'name': value` pairs in poll_grade.py, load_grade.py, rows_tiers.py, edit_rows.py and
tier1_rows.py, keyed by the enclosing assignment. Read at the base and at every commit that touches one of them.
"""
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

root, base, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
MODEL = ['tb/verilator/ctrl_service_budget/' + f for f in
         ('poll_grade.py', 'load_grade.py', 'rows_tiers.py', 'edit_rows.py', 'tier1_rows.py')]


def git(*a):
    return subprocess.run(['git', '-C', str(root), *a], capture_output=True, text=True, check=True).stdout


commits = [base] + git('rev-list', '--reverse', f'{base}..HEAD', '--', 'sw/firmware/ctrl', *MODEL).split()
head = git('rev-parse', 'HEAD').strip()
if commits[-1] != head:
    commits.append(head)
DEF = re.compile(r'^#define\s+([A-Z][A-Z0-9_]+)\s+(.*\d.*)$', re.M)
ASSIGN = re.compile(r'^([A-Z][A-Z0-9_]+)\s*(?::[^=]+)?=\s*', re.M)
PAIR = re.compile(r"""(?:'([^']+)'|\b([a-z_][a-z0-9_.]*))\s*[:=]\s*(\d+(?:\.\d+)?)\b""")


def snapshot(c):
    vals = {}
    files = [f for f in git('ls-tree', '-r', '--name-only', c, '--', 'sw/firmware/ctrl').split()
             if f.endswith(('.h', '.c'))]
    for f in files:
        for m in DEF.finditer(git('show', f'{c}:{f}')):
            vals[m.group(1)] = re.sub(r'\s*//.*$', '', m.group(2)).strip()
    for f in MODEL:
        try:
            text = git('show', f'{c}:{f}')
        except subprocess.CalledProcessError:
            continue
        starts = [(m.start(), m.group(1)) for m in ASSIGN.finditer(text)]
        for i, (s, name) in enumerate(starts):
            end = starts[i + 1][0] if i + 1 < len(starts) else len(text)
            block = text[s:end]
            block = block[:block.find('\n\n')] if '\n\n' in block else block
            for line_no, line in enumerate(block.splitlines()):
                if line.lstrip().startswith('#'):
                    continue
                for p in PAIR.finditer(re.sub(r'#.*$', '', line)):
                    key = p.group(1) or p.group(2)
                    vals[f'{Path(f).stem}.{name}[{key}]@{line_no}'] = p.group(3)
    return vals


hist = defaultdict(list)
for c in commits:
    for k, v in snapshot(c).items():
        if not hist[k] or hist[k][-1][1] != v:
            hist[k].append((c[:8], v))
final = snapshot(head)
with out.open('w') as fh:
    for k in sorted(hist):
        if len(set(v for _, v in hist[k])) > 1:
            cur = final.get(k, '(gone)')
            fh.write(f'{k}: head {cur}; history ' + ', '.join(f'{v}@{c}' for c, v in hist[k]) + '\n')
print(f'{len(commits)} snapshots, {sum(1 for k in hist if len(set(v for _, v in hist[k])) > 1)} constants moved')
