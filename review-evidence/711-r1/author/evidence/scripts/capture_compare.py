"""Compare base and candidate capture campaigns run with the receipt's recipe (scratch).

Usage: python3 capture_compare.py REPORT_JSON [--plant]
For every arm and control: exit status, capture.log bytes (SHA-256), rows; then the bounds:
every production row at most 24.5 ms, byte-only rows above 1.5 times the same side's 8x8 / 50 MHz ON
maximum, and the published margins against the 49 ms floor. --plant appends one byte to one candidate
log in memory, a negative control that must make the comparison fail.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path('$SCRATCH/capture')
LABELS = ('1x1-50-on', '1x1-50-off', '8x8-50-on', '8x8-50-off', '8x8-100-on', '8x8-100-off',
          'skip-copy', 'no-traffic', 'byte-only')
SYS_HZ = 100_000_000


def rows(text):
    return [dict((k, int(v)) for k, v in re.findall(r'(\w+)=(\d+)', line))
            for line in text.splitlines() if line.startswith('CAPTURE index=')]


def main():
    plant = '--plant' in sys.argv
    report, ok = {'runs': {}}, True
    logs = {}
    for label in LABELS:
        entry = {}
        for side in ('base', 'cand'):
            raw = (ROOT / side / f'capture-{label}' / 'capture.log').read_bytes()
            if plant and side == 'cand' and label == '8x8-100-on':
                raw += b'\n'
            logs[side, label] = raw
            entry[side] = {'rc': int((ROOT / side / f'{label}.rc').read_text()),
                           'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
                           'rows': len(rows(raw.decode(errors='replace')))}
        entry['identical'] = logs['base', label] == logs['cand', label]
        entry['same_rc'] = entry['base']['rc'] == entry['cand']['rc']
        ok = ok and entry['identical'] and entry['same_rc']
        report['runs'][label] = entry
    bounds = {}
    for side in ('base', 'cand'):
        worst = max(r['sys_cycles'] for label in LABELS[:6] for r in rows(logs[side, label].decode()))
        on_max = max(r['sys_cycles'] for r in rows(logs[side, '8x8-50-on'].decode()))
        byte = [r['sys_cycles'] for r in rows(logs[side, 'byte-only'].decode())]
        maxima = {label: max(r['sys_cycles'] for r in rows(logs[side, label].decode())) / SYS_HZ * 1000
                  for label in LABELS[:6]}
        bounds[side] = {'worst_production_ms': worst / SYS_HZ * 1000,
                        'production_bound_ok': worst * 2000 <= 49 * SYS_HZ,
                        'byte_only_ms': [c / SYS_HZ * 1000 for c in byte],
                        'byte_only_min_ratio': min(byte) / on_max,
                        'byte_only_ratio_ok': min(byte) > 1.5 * on_max,
                        'maxima_ms': maxima,
                        'margins': {k: 49 / v for k, v in maxima.items()}}
        ok = ok and bounds[side]['production_bound_ok'] and bounds[side]['byte_only_ratio_ok']
    report['bounds'] = bounds
    report['verdict'] = 'PASS' if ok else 'FAIL'
    Path(sys.argv[1]).write_text(json.dumps(report, indent=1) + '\n')
    for label, e in report['runs'].items():
        print(f"{label:12} rc {e['base']['rc']}/{e['cand']['rc']} rows {e['base']['rows']}/{e['cand']['rows']} "
              f"bytes {e['base']['bytes']}/{e['cand']['bytes']} {'IDENTICAL' if e['identical'] else 'DIFFERENT'} "
              f"{e['cand']['sha256'][:16]}")
    for side, b in bounds.items():
        print(side, f"worst {b['worst_production_ms']:.5f} ms, byte-only min ratio {b['byte_only_min_ratio']:.4f}",
              {k: round(v, 5) for k, v in b['maxima_ms'].items()})
    print('verdict:', report['verdict'])
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
