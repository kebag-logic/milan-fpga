#!/usr/bin/env python3
"""Check a JSON-verdict campaign (d3, notify, acmp drivers) against a README table.

Usage: compare_json_campaign.py README SECTION_HEADING_PREFIX DRIVER_LOG OUTDIR
DRIVER_LOG holds one JSON object per mutant ({"mutant", "verdict", ...}); OUTDIR
holds <mutant>.log. A README row "| `name` | ... | N ..." records N failing checks;
a mutant's count is its log's number of lines starting with "FAIL".
Every mutant must be KILLED (goldens PASS); every README row must match its count.
"""
import json
import re
import sys
from pathlib import Path

readme, heading, driver_log, outdir = sys.argv[1:5]
text = open(readme).read()
start = text.index(heading)
nxt = re.search(r'^#{2,3} ', text[start + len(heading):], re.M)
section = text[start:start + len(heading) + (nxt.start() if nxt else len(text))]
expected = {}
for line in section.splitlines():
    if not line.startswith('| `'):
        continue
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
    names = re.findall(r'`([A-Za-z0-9_.-]+)`', cells[0])
    m = re.match(r'^(\d+)\b', cells[-1])
    if names and m:
        expected[names[0]] = int(m.group(1))
verdicts = {}
for line in open(driver_log):
    line = line.strip()
    if line.startswith('{'):
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if 'mutant' in obj:
            verdicts[obj['mutant']] = obj.get('verdict')
bad = 0
goldens = {k: v for k, v in verdicts.items() if k.startswith('golden')}
arms = {k: v for k, v in verdicts.items() if not k.startswith('golden')}
for k, v in goldens.items():
    ok = v == 'PASS'
    bad += not ok
    print(f"{'OK' if ok else 'BAD'} {k} {v}")
for k, v in arms.items():
    log = Path(outdir) / f'{k}.log'
    count = sum(1 for x in log.read_text(errors='replace').splitlines()
                if x.startswith('FAIL')) if log.exists() else None
    # an arm run in another suite (name@suite) is recorded in that suite's README
    exp = (expected.get(k, expected.get(k.split('@')[0]))
           if '@' not in k or k.endswith('@pp_top') else None)
    ok = v == 'KILLED' and (exp is None or exp == count)
    bad += not ok
    note = 'readme=' + (str(exp) if exp is not None else 'not in this table')
    print(f"{'OK' if ok else 'MISMATCH'} {k} verdict={v} failures={count} {note}")
missing = sorted(set(expected) - {a.split('@')[0] for a in arms} - set(arms))
print(f"goldens {len(goldens)}, arms {len(arms)}, KILLED "
      f"{sum(v == 'KILLED' for v in arms.values())}, README rows {len(expected)}, "
      f"README rows without a run {missing}, problems {bad}")
sys.exit(1 if bad or missing else 0)
