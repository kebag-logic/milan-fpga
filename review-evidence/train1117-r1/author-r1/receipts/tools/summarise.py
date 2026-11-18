#!/usr/bin/env python3
"""summarise.py BUDGET LOGS: one line per part (its run's last summary line and exit status), every budget miss by
name, every STATED and REFUSED line, the longest queued notice, the saves and the aged windows' least margin."""
import re
import sys
from pathlib import Path

budget, logs = Path(sys.argv[1]), Path(sys.argv[2])
rows, misses, stated, refused, notices, saves, aged = [], [], [], [], [], [], []
for log in sorted(logs.glob('p*-*.log')):
    text = log.read_text(errors='replace')
    rc = (log.parent / (log.name + '.rc')).read_text().strip() if (log.parent / (log.name + '.rc')).is_file() else '?'
    graded = [l for l in text.splitlines() if 'groups graded' in l]
    rows.append(f'{log.stem}: rc={rc}; {graded[-1] if graded else "no summary"}')
    for line in text.splitlines():
        if line.startswith('BUDGET'):
            misses.append(f'{log.stem}: {line[:200]}')
        elif line.startswith('STATED'):
            stated.append(f'{log.stem}: {line[:220]}')
        elif line.startswith('REFUSED'):
            refused.append(f'{log.stem}: {line[:220]}')
        elif line.startswith('NOTICE'):
            m = re.search(r'committed ([0-9.]+) ms .* \(bound ([0-9]+) ms\)', line)
            if m:
                notices.append((float(m[1]), int(m[2]), log.stem, line[:160]))
        elif line.startswith('SAVE'):
            saves.append(f'{log.stem}: {line[:200]}')
        elif line.startswith('AGED'):
            aged.append(f'{log.stem}: {line[:200]}')
print('## Parts'); print('\n'.join(rows))
print(f'\n## Budget misses: {len(misses)}'); print('\n'.join(sorted(set(misses))))
print(f'\n## STATED: {len(stated)}'); print('\n'.join(sorted(set(stated))))
print(f'\n## REFUSED: {len(refused)}'); print('\n'.join(sorted(set(refused))))
if notices:
    top = max(notices)
    print(f'\n## Queued notices: {len(notices)} measured; the longest {top[0]:.3f} ms against {top[1]} ms ({top[2]})')
print(f'\n## Saves: {len(saves)}'); print('\n'.join(sorted(set(saves))))
print(f'\n## Aged windows: {len(aged)}'); print('\n'.join(sorted(set(aged))))
