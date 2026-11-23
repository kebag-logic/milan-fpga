#!/usr/bin/env python3
"""disposition_regrade.py CHECKOUT BUILD-DIR SUMMARY: run.py's #977 disposition (kept_grade.Disposition) at the
checkout, on a finished run's srp-kept and srp-bound logs and grades: the STATED lines of that run's summary (its OWED
lines, their disposition stripped) and run.share_misses of its grades, each owed or still failing."""
import json, sys
from pathlib import Path
root, build, summary = (Path(p).resolve() for p in sys.argv[1:4])
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import kept_grade, run
spec = json.loads((build / 'build.json').read_text())
out = build / 'results'
results = [json.loads((out / f'{name}.json').read_text()) for name in kept_grade.OWED_KINDS]
tail = f', owed to {kept_grade.DISPOSITION}'
stated = [line[5:-len(tail)] for line in summary.read_text().splitlines()
          if line.startswith('OWED srp-') and line.endswith(tail) and "'s registrations" not in line]
d = kept_grade.Disposition(results, out, spec)
left, shares = d.stated(list(stated)), run.share_misses(results)
share_left = d.shares(shares)
print(f'STATED lines of the run: {len(stated)}; still failing: {len(left)}')
print(f'SHARE lines of the run: {len(shares)}; still failing: {len(share_left)}')
for line in d.owed:
    print(f'OWED {line}')
for line in left + share_left:
    print(f'FAIL {line}')
print(f'disposition findings: {len(d.findings)}' + ''.join(f'\nFINDING {f}' for f in d.findings))
sys.exit(1 if left or share_left or d.findings else 0)
