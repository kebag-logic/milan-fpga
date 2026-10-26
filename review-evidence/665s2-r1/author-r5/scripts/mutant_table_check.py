#!/usr/bin/env python3
"""Every row of the README's mutant table names a mutant the self-test caught, and the check that
caught it first; every caught mutant has a row. A row naming a refusal ("refused: <where>: ...")
matches a refusal at the same place. Usage: mutant_table_check.py README SELFTEST_LOG"""
import re
import sys
from pathlib import Path

readme, log = Path(sys.argv[1]).read_text(), Path(sys.argv[2]).read_text()
start = readme.index('| Mutant | Caught by |')
rows = {}
for line in readme[start:].splitlines()[2:]:
    if not line.startswith('|'):
        break
    mutant, caught = (c.strip() for c in line.strip('|').split(' | '))
    rows[mutant] = caught
caught = {}
for line in log.splitlines():
    m = re.match(r'MUTANT caught: (.*)', line)
    if m:
        body = m.group(1)
        name = next((r for r in sorted(rows, key=len, reverse=True) if body.startswith(r + ': ')), None)
        if name is None:
            print(f'NO ROW: {body[:160]}')
            continue
        caught[name] = body[len(name) + 2:]
bad = 0
for name, check in rows.items():
    got = caught.get(name)
    want = ': '.join(check.split(': ')[:2]) + ': ' if check.startswith('refused: ') else check
    ok = got is not None and got.startswith(want)
    bad += not ok
    print(f"{'ok ' if ok else 'BAD'} {name} -> {check}" + ('' if ok else f' (self-test: {got})'))
print(f'{len(rows)} rows, {len(caught)} caught mutants matched, {bad} mismatches, '
      f"{sum(1 for l in log.splitlines() if l.startswith('MUTANT caught'))} MUTANT caught lines")
raise SystemExit(1 if bad or len(caught) != len(rows) else 0)
