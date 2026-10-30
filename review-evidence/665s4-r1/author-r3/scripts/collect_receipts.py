#!/usr/bin/env python3
"""Copy one run's small text artefacts into a receipts directory, list every other file by size and sha256,
and write the commit case's service steps (from its SPAN and CALL lines) as a CSV a reviewer can re-sum.

Usage: collect_receipts.py RESULTS_DIR RECEIPTS_DIR
Files of 200 KB or more, and binary journals, are listed in large-files.txt and never copied.
"""
import csv
import hashlib
import io
import shutil
import sys
from pathlib import Path

LIMIT = 200_000
TEXT = ('.md', '.json', '.txt', '.log')

src, dst = Path(sys.argv[1]), Path(sys.argv[2])
dst.mkdir(parents=True, exist_ok=True)
listed = []
for path in sorted(p for p in src.rglob('*') if p.is_file()):
    rel = path.relative_to(src)
    size = path.stat().st_size
    if path.suffix in TEXT and size < LIMIT and 'shape' not in rel.parts:
        (dst / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, dst / rel)
    elif 'shape' not in rel.parts:
        listed.append(f'{rel}\t{size}\t{hashlib.sha256(path.read_bytes()).hexdigest()}')
(dst / 'large-files.txt').write_text('file\tbytes\tsha256\n' + '\n'.join(listed) + '\n')
commit = src / 'commit.log'
if commit.is_file():
    spans, calls = [], []
    for line in commit.read_text().splitlines():
        fields = line.split()
        if fields[:1] == ['SPAN']:
            spans.append([int(fields[1]), int(fields[2]), int(fields[3]), fields[5], []])
        elif fields[:1] == ['CALL']:
            calls.append((int(fields[2]), fields[3]))
    for cpu, name in calls:
        for span in spans:
            if span[1] <= cpu <= span[1] + span[2]:
                span[4].append(name)
    out = io.StringIO()
    writer = csv.writer(out, lineterminator='\n')
    writer.writerow(['sys_cycle', 'cpu_cycle', 'cpu_cycles', 'function', 'calls'])
    for sys_cycle, cpu, cycles, name, inside in spans:
        writer.writerow([sys_cycle, cpu, cycles, name, ' '.join(inside)])
    (dst / 'commit-steps.csv').write_text(out.getvalue())
print(f'{dst}: copied the small text files, listed {len(listed)} others')
