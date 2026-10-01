#!/usr/bin/env python3
"""R425-5: withheld every-channel capture sizes in the evidence archive.

Usage: r425_5_archive_scan.py <repo> <old-rev> <archive-git-dir> <commit>...
From the old page at <old-rev> it reads the three every-channel byte sizes and
derives, in memory, the capture channel-count candidates (never printed).
For each archive commit, over every text file under review-evidence/b5-r1:
  A1 lines carrying a withheld size literally (plain or with separators);
  A2 lines carrying an integer equal to duration x 48000 x sample-bytes x a
     derived count, for the durations the page states.
Prints paths and line numbers only.
"""
import re, subprocess, sys

repo, old, G = sys.argv[1:4]
commits = sys.argv[4:]
PAGE = 'docs/findings/117_AUDIO_CONTINUITY.md'
page = subprocess.run(['git', '-C', repo, 'show', f'{old}:{PAGE}'], capture_output=True, text=True, check=True).stdout
rows = re.findall(r'^\| [^|]*every channel, (\d+) s \| (\d+) \|', page, re.M)
sizes = [b for _, b in rows]
pats = set(sizes) | {f'{int(s):,}' for s in sizes}
counts = {int(b) // (int(d) * 48000 * k) for d, b in rows for k in (3, 4) if int(b) % (int(d) * 48000 * k) == 0}
targets = {d * 48000 * k * c for d in (3, 10, 15, 25, 40, 660) for k in (3, 4) for c in counts}
print(f'{len(rows)} withheld sizes and {len(counts)} channel-count candidates derived in memory (not printed)')
for c in commits:
    files = subprocess.run(['git', '-C', G, 'ls-tree', '-r', '--name-only', c, 'review-evidence/b5-r1'],
                           capture_output=True, text=True, check=True).stdout.split()
    a1, a2 = [], []
    for f in files:
        if f.endswith(('.gz', '.u16')):
            continue
        b = subprocess.run(['git', '-C', G, 'show', f'{c}:{f}'], capture_output=True).stdout.decode('utf-8', 'replace')
        for i, line in enumerate(b.splitlines(), 1):
            if any(re.search(r'(?<![\d,])' + re.escape(p) + r'(?![\d,])', line) for p in pats):
                a1.append(f'{f}:{i}')
            if any(int(t.replace(',', '')) in targets for t in re.findall(r'(?<![\w.])\d[\d,]*\d(?![\w.])', line)):
                a2.append(f'{f}:{i}')
    print(f'{c[:8]} {len(files)} files: A1 literal withheld size lines {len(a1)}; A2 exact derivation lines {len(a2)}')
    for h in a1:
        print('  A1', h)
    for h in a2:
        print('  A2', h)
