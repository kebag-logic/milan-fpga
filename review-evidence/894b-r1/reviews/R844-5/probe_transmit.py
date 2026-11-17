#!/usr/bin/env python3
"""Probe the actual flip CLI in a disposable exact-head tree.
Usage: python3 -B probe_transmit.py REPOSITORY PACKET_DIRECTORY
"""
import io
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile

repo, packet = (Path(p).resolve() for p in sys.argv[1:])
copy = packet / 'scratch' / 'transmit-probe'
copy.mkdir(parents=True, exist_ok=True)
archive = subprocess.check_output(['git', '-C', str(repo), 'archive', 'HEAD'])
with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
    tar.extractall(copy, filter='data')
for sub in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis', 'third_party/tsn-c-stack', 'third_party/lwSRP'):
    archive = subprocess.check_output(['git', '-C', str(repo / sub), 'archive', 'HEAD'])
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        tar.extractall(copy / sub, filter='data')
sys.path.insert(0, str(copy / 'tb/verilator/ctrl_service_budget'))
import rows_tiers
import shape_costs

point = '8x8/1if'
i = rows_tiers.point_inputs(copy, point)
w, terms = rows_tiers.solve('tx', i, rows_tiers.BUILT)
print('tx row', w, 'ms; stated', i.tx_stated, 'ms; notices', i.s['notices'])
print('terms', sorted(terms.items()))
assert i.s['notices'] == 40 and 74.25 < w < 74.27 and i.tx_stated == 75
join = int(re.search(r'^#define CTRL_LOOP_JOIN_CS (\d+)u',
                    (copy / 'sw/firmware/ctrl/loop/ctrl_loop.h').read_text(), re.M)[1])
hold = 2000 + join + (i.tx_stated + 9) // 10
remaining = hold * 10 - join * 10 - w
print('hold-off', hold, 'cs; remaining', remaining, 'ms; minimum 20000 ms')
assert hold == 2027 and remaining >= 20000
for row in rows_tiers.bounds_at(i):
    value = rows_tiers.solve(row, i, rows_tiers.BUILT)[0]
    print('ROW', row, value)
header = copy / 'sw/firmware/ctrl/loop/ctrl_loop.h'
original = header.read_text()
shape = shape_costs.of_point(point, copy)
grader = 'tb/verilator/ctrl_service_budget/flip_grade.py'
for value, expected_rc in ((75, 0), (60, 1), (69, 1), (70, 1), (74, 1), (76, 0)):
    header.write_text(shape_costs.planted_at(original, shape, shape_costs.TX, value))
    run = subprocess.run([sys.executable, '-B', grader, '--check', '--point', point], cwd=copy,
                         env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}, capture_output=True, text=True)
    (packet / f'probe-tx-{value}.log').write_text(run.stdout + run.stderr)
    print('CLI constant', value, 'exit', run.returncode)
    assert run.returncode == expected_rc
    if expected_rc:
        message = f'OVER 8x8/1if: CTRL_LOOP_TX_MS states {value} ms, under the built design\'s tx row 74.26 ms'
        assert message in run.stdout
        print(message)
header.write_text(original)
# A higher real cost must move the derived row, not leave a mirrored 74.26.
# Use the model directly for this sensitivity control; the CLI controls above alter actual source bytes.
changed = i._replace(c={**i.c, 'base': i.c['base'] + 100})
larger = rows_tiers.solve('tx', changed, rows_tiers.BUILT)[0]
print('poll base +100 us: tx row', larger, 'ms')
assert larger is None or larger > w
print('RESULT: PASS')
