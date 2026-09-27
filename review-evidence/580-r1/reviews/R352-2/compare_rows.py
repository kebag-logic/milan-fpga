#!/usr/bin/env python3
"""Compare reviewer-reproduced capture rows with the receipt arm, field by field."""
import json, re, sys
receipt, log, shape, hz, traffic = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5]
arm = next(a for a in json.load(open(receipt))['measurements']
           if (a['shape'], a['cpu_hz'], a['traffic']) == (shape, hz, traffic))
rows = [dict((k, int(v)) for k, v in re.findall(r'(\w+)=(\d+)', m))
        for m in re.findall(r'CAPTURE index=[^\n]*', open(log).read())]
equal = sum(r == arm['rows'][r['index']] for r in rows)
print(f'{shape} {hz} {traffic}: reproduced {len(rows)}/{len(arm["rows"])} rows; equal {equal}/{len(rows)}')
for r in rows:
    if r != arm['rows'][r['index']]:
        print('DIFF', r, arm['rows'][r['index']])
print('max reproduced sys_cycles', max(r['sys_cycles'] for r in rows),
      'receipt arm max_ms', arm['maximum_ms'])
sys.exit(0 if rows and equal == len(rows) else 1)
