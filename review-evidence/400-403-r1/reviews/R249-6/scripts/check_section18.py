#!/usr/bin/env python3
"""Cross-check section 18 table and prose figures against measurements.json.

Usage: check_section18.py <repo>   (exit 0 when every figure agrees)
"""
import json
import re
import sys
from pathlib import Path

repo = Path(sys.argv[1])
receipt = json.loads((repo / 'tb/verilator/nvm_capture_cpu/measurements.json').read_text())
doc = (repo / 'docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md').read_text()
fail = 0


def expect(label, needle):
    global fail
    ok = needle in doc
    fail |= not ok
    print(('OK   ' if ok else 'MISS ') + label + ': ' + needle)


names = {'endstation_ax7101_8x8': '8x8', 'endstation_ax7101_1x1_tdm8': '1x1'}
arm_max = {}
for arm in receipt['measurements']:
    cyc = [r['sys_cycles'] for r in arm['rows']]
    assert len(cyc) == 16 == arm['captures']
    lo, hi = min(cyc), max(cyc)
    ms = lambda c: f"{c / arm['sys_hz'] * 1000:.5f}"
    basis = 'contract' if arm['cpu_hz'] == 50_000_000 else 'non-contract'
    row = (f"| {names[arm['shape']]} | {arm['cpu_hz'] // 1_000_000} / 100, {basis} | "
           f"{arm['traffic'].upper()} | {lo:,} to {hi:,} | {ms(lo)} to {ms(hi)} | "
           f"{49 / (hi / arm['sys_hz'] * 1000):.4f}x |")
    expect('table row', row)
    arm_max[(names[arm['shape']], arm['cpu_hz'], arm['traffic'])] = hi / arm['sys_hz'] * 1000

w8 = max(arm_max[('8x8', 50_000_000, a)] for a in ('on', 'off'))
w1 = max(arm_max[('1x1', 50_000_000, a)] for a in ('on', 'off'))
w100 = max(arm_max[('8x8', 100_000_000, a)] for a in ('on', 'off'))
expect('8x8 worst', f'**The worst 8x8 measurement is {w8:.5f} ms.**')
expect('8x8 margin', f'This gives {49 / w8:.4f}x margin against the guaranteed floor.')
expect('8x8 slack', f'It leaves {24.5 - w8:.5f} ms below the assigned limit.')
expect('U6 worst', f'The worst 8x8 copy is {w8:.5f} ms across both arms.')
expect('U6 margin', f'Its margin against the guaranteed 49 ms floor is {49 / w8:.4f}x.')
expect('1x1 worst', f'The 1x1 overall maximum is {w1:.5f} ms ({49 / w1:.4f}x floor margin).')
expect('U6 1x1', f'The 1x1 maximum is {w1:.5f} ms ({49 / w1:.4f}x floor margin).')
expect('U6 100', f'non-contract: {w100:.5f} ms maximum.')
d8 = arm_max[('8x8', 50_000_000, 'on')] - arm_max[('8x8', 50_000_000, 'off')]
expect('8x8 ON-OFF', f'8x8 ON exceeds OFF by {d8:.5f} ms.')
expect('8x8 ON-OFF pct', f'That is {100 * d8 / arm_max[("8x8", 50_000_000, "off")]:.3f}% between their maxima.')
d1 = arm_max[('1x1', 50_000_000, 'on')] - arm_max[('1x1', 50_000_000, 'off')]
expect('1x1 ON-OFF', f'The 1x1 difference is {d1:.5f} ms ({100 * d1 / arm_max[("1x1", 50_000_000, "off")]:.3f}%).')
d100 = arm_max[('8x8', 100_000_000, 'off')] - arm_max[('8x8', 100_000_000, 'on')]
expect('100 OFF-ON', f'At 100 MHz, ON is {d100:.5f} ms faster than OFF.')
expect('capture count', f"contains all {sum(len(a['rows']) for a in receipt['measurements'])} captures")
m = {(x['shape'], x['cpu_hz']): x['maximum_ms'] for x in receipt['maxima']}
ok = (abs(m[('endstation_ax7101_8x8', 50_000_000)] - w8) < 1e-12 and w8 <= 24.5)
print(('OK   ' if ok else 'MISS ') + f'receipt maxima 8x8@50 = {w8} <= 24.5')
fail |= not ok
print('RESULT', 'FAIL' if fail else 'PASS')
sys.exit(1 if fail else 0)
