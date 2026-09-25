#!/usr/bin/env python3
"""Compare capture.log rows against the published receipt, index for index.

Usage: compare_rows.py <measurements.json> <label> <capture.log> <shape> <cpu_hz> <on|off> [<other capture.log>]
With a second capture log, the two logs are compared with each other instead of the receipt
(used when the capture count differs from the receipt's 16, which changes the BIOS).
"""
import json
import re
import sys


def rows(path):
    out = []
    for line in open(path, encoding='utf-8', errors='replace'):
        if line.startswith('CAPTURE index='):
            out.append({k: int(v) for k, v in re.findall(r'(\w+)=(\d+)', line)})
    return out


def main():
    receipt, label, log, shape, cpu_hz, traffic = sys.argv[1:7]
    got = rows(log)
    if len(sys.argv) > 7:
        ref, ref_name = rows(sys.argv[7]), sys.argv[7]
    else:
        arm = [a for a in json.load(open(receipt))['measurements']
               if a['shape'] == shape and a['cpu_hz'] == int(cpu_hz) and a['traffic'] == traffic]
        assert len(arm) == 1, 'receipt arm not found'
        ref, ref_name = arm[0]['rows'], f'receipt {shape} {cpu_hz} {traffic}'
    if not got:
        print(f'{label}: NO ROWS'); return 1
    diff = 0
    for row in got:
        other = ref[row['index']] if row['index'] < len(ref) else None
        same = other == row
        diff += not same
        print(f"{label} index={row['index']} sys_cycles={row['sys_cycles']} "
              f"ref_sys_cycles={other and other['sys_cycles']} {'IDENTICAL' if same else 'DIFFERENT'}")
    print(f'{label}: {len(got)} row(s) vs {ref_name}: {len(got) - diff} identical, {diff} different')
    return 1 if diff else 0


if __name__ == '__main__':
    sys.exit(main())
