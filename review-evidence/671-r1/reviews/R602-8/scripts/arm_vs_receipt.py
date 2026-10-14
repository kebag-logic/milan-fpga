"""Match published per-arm measurement.json rows (and capture-log CAPTURE lines) to the receipt.

Usage: python3 -I arm_vs_receipt.py <receipt.json> <evidence-dir>
"""
import hashlib
import json
import re
import sys
from pathlib import Path

receipt = json.load(open(sys.argv[1]))
ev = Path(sys.argv[2])
ok = True
for arm in receipt['measurements']:
    tag = '%s-%d-%s' % ('8x8' if '8x8' in arm['shape'] else '1x1', arm['cpu_hz'] // 1_000_000, arm['traffic'])
    m = json.load(open(ev / f'capture-{tag}.measurement.json'))
    rows_eq = m['rows'] == arm['rows']
    log = (ev / f'capture52-{tag}.log').read_text(errors='replace')
    cycles = [int(x) for x in re.findall(r'CAPTURE\b[^\n]*?sys_cycles=(\d+)', log)]
    log_eq = cycles == [r['sys_cycles'] for r in arm['rows']]
    diff_keys = sorted(k for k in set(m) | set(arm) if m.get(k) != arm.get(k))
    print(tag, 'rows_equal=%s' % rows_eq, 'log_capture_cycles=%d equal=%s' % (len(cycles), log_eq),
          'arm_keys_differing=%s' % diff_keys,
          'sha256=%s' % hashlib.sha256((ev / f'capture-{tag}.measurement.json').read_bytes()).hexdigest()[:16])
    ok &= rows_eq
print('ALL_ROWS_EQUAL' if ok else 'ROWS_DIFFER')
