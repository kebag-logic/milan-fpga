#!/usr/bin/env python3
"""Reproduce this review's small, read-only checks from the candidate checkout.

Prerequisites: Python 3, Git, GCC; candidate HEAD and evidence commit fetched.
All extracted files stay in this packet's scratch directory.
"""
from pathlib import Path
import subprocess
import sys

PACKET = Path(__file__).resolve().parent
ARCHIVE = '1a0955730171f3fdc32387098b4beec60788c0ce'
PREFIX = 'review-evidence/894-r1/'

def command(args, receipt):
    with (PACKET / receipt).open('wb') as log:
        result = subprocess.run(args, stdout=log, stderr=subprocess.STDOUT)
    (PACKET / (receipt + '.rc')).write_text(str(result.returncode) + '\n')
    if result.returncode:
        raise SystemExit(f'{receipt}: exit {result.returncode}')

paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', ARCHIVE, PREFIX + 'author-r14']).decode().splitlines()
paths += [PREFIX + 'MANIFEST.json']
paths += [PREFIX + 'author-r13/' + p for p in (
    'receipts/images/image-sha256-c274b9f5.txt',
    'receipts/images/harness-elf-sha256.txt',
    'receipts/model/flip-1x1-ed0df35b.txt',
    'receipts/model/flip-selftest-ed0df35b.txt')]
for name in paths:
    target = PACKET / 'scratch' / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(subprocess.check_output(['git', 'show', f'{ARCHIVE}:{name}']))
command([sys.executable, '-B', str(PACKET / 'verify_review.py'), 'identity', 'receipts'], 'verification.txt')
command([sys.executable, '-B', 'tb/verilator/ctrl_service_budget/flip_grade.py', '--check', '--point', '1x1/1if'], 'flip-check.txt')
command([sys.executable, '-B', 'tb/verilator/ctrl_service_budget/load_grade.py', '--check'], 'load-check.txt')
command([sys.executable, '-B', str(PACKET / 'scratch' / PREFIX / 'author-r14/scripts/stale_grep.py')], 'stale-grep.txt')
command(['git', 'grep', '-n', '-E', r'725|33[.]01|900 (us|µs)|0[.]515|0[.]511|13[.]05|132[.]71', '--',
         'docs/design/SPLIT_CONTROL_MEMORY.md', 'docs/reference/FR_NFR.md', '*README*', '*.c', '*.h', '*.cpp', '*.hpp', '*.py', '*.sv'], 'independent-grep.txt')
command(['git', 'diff', '--check', '234bc149', 'HEAD'], 'diff-check.txt')
command([sys.executable, '-B', str(PACKET / 'verify_review.py'), 'integrity'], 'integrity-final.txt')
print('All focused checks completed; raw logs and exit receipts written beside this script.')
