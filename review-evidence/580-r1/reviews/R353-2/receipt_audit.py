#!/usr/bin/env python3
"""Independent audit of the capture receipt, without the repository's graders.

Usage: receipt_audit.py <repo> <head>
Checks, from raw rows only: six arms with 16 rows each, per-row success flags,
census per shape, traffic counters by arm, recomputed maxima and margins, the
8x8 contract maximum against 24.5 ms, and receipt provenance (base commit tree,
recorded tree, and each processor_pins entry against the base and head gitlinks).
"""
import json
import subprocess
import sys
from fractions import Fraction

BAR_MS = Fraction(49, 2)
CENSUS = {'endstation_ax7101_8x8': (12634, 156), 'endstation_ax7101_1x1_tdm8': (3218, 53)}


def git(repo: str, *args: str) -> str:
    return subprocess.check_output(['git', '-C', repo, *args], stderr=subprocess.DEVNULL,
                                   text=True).strip()


def main() -> int:
    repo, head = sys.argv[1:3]
    receipt = json.loads(git(repo, 'show', f'{head}:tb/verilator/nvm_capture_cpu/measurements.json'))
    errors = []
    arms = receipt['measurements']
    keys = sorted((a['shape'], a['cpu_hz'], a['traffic']) for a in arms)
    print('arms:', keys)
    if len(arms) != 6 or len(set(keys)) != 6:
        errors.append('expected six distinct arms')
    worst = {}
    for arm in arms:
        rows = arm['rows']
        tag = f"{arm['shape']}@{arm['cpu_hz']}/{arm['traffic']}"
        if len(rows) != 16 or [r['index'] for r in rows] != list(range(16)):
            errors.append(f'{tag}: rows are not indices 0..15')
        for r in rows:
            if (r['ok'], r['mismatches'], r['open']) != (1, 0, 0):
                errors.append(f'{tag}[{r["index"]}]: not a clean capture')
            if (r['raw'], r['records']) != CENSUS[arm['shape']]:
                errors.append(f'{tag}[{r["index"]}]: census differs')
            counts = (r['requests'], r['responses'], r['reads'])
            if arm['traffic'] == 'on' and min(counts) <= 0:
                errors.append(f'{tag}[{r["index"]}]: ON row without traffic')
            if arm['traffic'] == 'off' and any(counts):
                errors.append(f'{tag}[{r["index"]}]: OFF row with traffic')
        ms = [Fraction(r['sys_cycles'] * 1000, arm['sys_hz']) for r in rows]
        print(f'{tag}: sys_hz={arm["sys_hz"]} min={float(min(ms)):.5f} ms '
              f'max={float(max(ms)):.5f} ms role={arm.get("clock_role")}')
        key = (arm['shape'], arm['cpu_hz'])
        worst[key] = max(worst.get(key, Fraction(0)), max(ms))
    for m in receipt['maxima']:
        key = (m['shape'], m['cpu_hz'])
        mine = worst[key]
        margin = Fraction(49) / mine
        print(f'maximum {key}: recomputed {float(mine):.5f} ms, published {m["maximum_ms"]}; '
              f'margin recomputed {float(margin):.6f}, published {m["margin"]:.6f}')
        if abs(float(mine) - m['maximum_ms']) > 1e-9 or abs(float(margin) - m['margin']) > 1e-9:
            errors.append(f'{key}: published maximum or margin differs')
    contract = worst[('endstation_ax7101_8x8', 50_000_000)]
    print(f'8x8 at 50 MHz: {float(contract):.5f} ms; headroom to 24.5 ms = '
          f'{float(BAR_MS - contract):.5f} ms')
    if contract > BAR_MS:
        errors.append('8x8 contract maximum exceeds 24.5 ms')
    base = receipt['base']
    base_tree = git(repo, 'rev-parse', f'{base}^{{tree}}')
    print(f'base {base} tree {base_tree}; recorded tree {receipt["tree"]}')
    if base_tree != receipt['tree']:
        errors.append('recorded tree is not the base commit tree')
    if git(repo, 'merge-base', '--is-ancestor', base, head) != '':
        errors.append('unexpected output from ancestry check')
    for path, pin in receipt['processor_pins'].items():
        at_base = git(repo, 'rev-parse', f'{base}:{path}')
        at_head = git(repo, 'rev-parse', f'{head}:{path}')
        print(f'pin {path}: recorded {pin}; base gitlink {at_base}; head gitlink {at_head}')
        if not pin == at_base == at_head:
            errors.append(f'{path}: recorded pin differs from a measured or head gitlink')
    for e in errors:
        print('ERROR:', e)
    print('RESULT:', 'FAIL' if errors else 'PASS')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
