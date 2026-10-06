#!/usr/bin/env python3
"""Require the two completed partitions to cover exactly the 86 source controls."""
import argparse
import json
from pathlib import Path
import sys
import types

ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
ap.add_argument('--packet', type=Path, required=True)
a = ap.parse_args()
p = a.packet.resolve()
source = a.repo.resolve() / 'tb/pp_top/notify_mutants.py'
m = types.ModuleType('final_campaign_catalog')
m.__file__ = str(source)
sys.modules[m.__name__] = m
exec(compile(source.read_text(), str(source), 'exec'), m.__dict__)
known = {x.name for x in m.MUTANTS}
records = []
for partition in ['notify-focus', 'notify-remainder']:
    for row in json.loads((p / 'receipts' / partition / 'results.json').read_text()):
        row['partition'] = partition
        records.append(row)
goldens = [x for x in records if x['mutant'].startswith('golden-')]
mutants = [x for x in records if not x['mutant'].startswith('golden-')]
names = [x['mutant'] for x in mutants]
ok = (len(names) == len(set(names)) == len(known) == 86 and set(names) == known and
      all(x['verdict'] == 'PASS' and x['run_rc'] == 0 and x['completed'] and not x['failing_checks'] for x in goldens) and
      all(x['verdict'] == 'KILLED' and x['build_rc'] == 0 and
          x['run_rc'] == (2 if x['suite'].startswith('make ') else 1) and
          x['completed'] and not x['missing'] for x in mutants))
summary = {'head': '669ded57b1fabc2bbf274b8ad05493c7593e0a0a', 'pass': ok,
           'controls': len(mutants), 'killed': sum(x['verdict'] == 'KILLED' for x in mutants),
           'goldens': len(goldens), 'passing_goldens': sum(x['verdict'] == 'PASS' for x in goldens),
           'missing_controls': sorted(known - set(names)), 'records': records}
(p / 'receipts/notify-combined.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps({k: v for k, v in summary.items() if k != 'records'}))
raise SystemExit(not ok)
