"""mutant_table.py <results.json> [...]: the mutant evidence as Markdown, one row per (mutant, suite), each named
check with the exact FAIL line its suite printed for it (the log lines, host paths removed)."""
import json
import re
import sys
from pathlib import Path


def fail_line(log_text, check):
    for line in log_text.splitlines():
        s = line.strip()
        if ('[FAIL]' in s or s.startswith('FAIL')) and check in s:
            return re.sub(r'\s{2,}', ' ', s)
    return '(not found)'


rows = []
for arg in sys.argv[1:]:
    path = Path(arg)
    for row in json.loads(path.read_text()):
        if 'suites' not in row:
            rows.append(f"| {row['mutant']} | - | rc {row['rc']}, FAIL lines {len(row['all_failed'])} | "
                        f"{row['verdict']} |")
            continue
        tag = row['mutant'].split()[0]
        for suite, res in row['suites'].items():
            log = (path.parent / f'{tag}-{suite}.log').read_text(errors='replace')
            words = '<br>'.join(f'`{fail_line(log, c)}`' for c in res['named'])
            rows.append(f"| {row['mutant']} (`{row['file']}`) | {suite} | {len(res['failed_named'])}/{len(res['named'])} "
                        f"named; {len(res['all_failed'])} FAIL lines; rc {res['rc']}<br>{words} | {row['verdict']} |")
print('| Mutant (file) | Suite | Named checks failed, and the words printed | Verdict |')
print('|---|---|---|---|')
print('\n'.join(rows))
