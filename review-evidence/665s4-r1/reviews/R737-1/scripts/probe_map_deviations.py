#!/usr/bin/env python3
"""Reviewer probe: does split_soc.map_deviations refuse every other placement?

Usage: probe_map_deviations.py CLONE TEST_SOC_CSR_CSV FLASH_MAP_DIR

Runs the checkout's own map_deviations on the test SoC's csr.csv as built
(must be empty), then on planted copies: each register the port uses moved
one word, removed, the flash window moved, resized, duplicated and removed.
Each plant must yield at least one deviation. Prints one line per check and
exits 0 only when every check holds. Reads only; writes nothing.
"""
import json
import sys
from pathlib import Path

clone, csv_path, flash_map = (Path(a).resolve() for a in sys.argv[1:4])
sys.path.insert(0, str(clone / 'tb/verilator/ctrl_service_budget'))
import split_soc  # noqa: E402

text = csv_path.read_text()
port = json.loads((flash_map / 'flash_port.json').read_text())
fails = 0


def check(label, ok, detail):
    global fails
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} {label}: {detail}")


base = split_soc.map_deviations(text, flash_map)
check('as built: no deviation', base == [], base)
lines = text.splitlines()
for name in port['registers']:
    idx = [i for i, l in enumerate(lines) if l.split(',')[:2] == ['csr_register', name]]
    check(f'{name} present once in the test SoC csr.csv', len(idx) == 1, idx)
    if len(idx) != 1:
        continue
    row = lines[idx[0]].split(',')
    moved = list(lines)
    moved[idx[0]] = ','.join([row[0], row[1], f'0x{int(row[2], 16) + 4:08x}', *row[3:]])
    got = split_soc.map_deviations('\n'.join(moved) + '\n', flash_map)
    check(f'{name} moved one word is refused', any(name in d for d in got), got)
    dropped = [l for i, l in enumerate(lines) if i != idx[0]]
    got = split_soc.map_deviations('\n'.join(dropped) + '\n', flash_map)
    check(f'{name} absent is refused', any(name in d for d in got), got)
win = [i for i, l in enumerate(lines) if l.split(',')[:2] == ['memory_region', 'spiflash']]
check('flash window present once', len(win) == 1, win)
row = lines[win[0]].split(',')
for label, new in (('moved', [row[0], row[1], f'0x{int(row[2], 16) + 0x100_0000:08x}', *row[3:]]),
                   ('resized', [row[0], row[1], row[2], str(int(row[3]) // 2), *row[4:]])):
    edit = list(lines)
    edit[win[0]] = ','.join(new)
    got = split_soc.map_deviations('\n'.join(edit) + '\n', flash_map)
    check(f'flash window {label} is refused', any('flash window' in d for d in got), got)
got = split_soc.map_deviations('\n'.join([*lines, lines[win[0]]]) + '\n', flash_map)
check('flash window mapped twice is refused', any('flash window' in d for d in got), got)
got = split_soc.map_deviations('\n'.join(l for i, l in enumerate(lines) if i != win[0]) + '\n', flash_map)
check('flash window absent is refused', any('flash window' in d for d in got), got)
print(f'checks failed: {fails}')
sys.exit(1 if fails else 0)
