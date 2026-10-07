#!/usr/bin/env python3
"""Run arithmetic defects through the repository's self-test without editing it.

Usage: python3 helper_mutations.py REPOSITORY SCRATCH COMPILER
"""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys

repo, work, cc = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
work.mkdir(parents=True, exist_ok=True)
source = (repo / 'sw/firmware/ctrl/test/rv32_image/image_arith.c').read_text()
plants = [
    ('multiply32-low-bit', '\treturn p;', '\treturn p ^ 1u;', '__mulsi3'),
    ('multiply64-carry', '(lo < add ? 1u : 0u)', '0u', '__muldi3'),
    ('divide32-equality', 'if (r >= d)', 'if (r > d)', '__udivsi3'),
    ('divide64-equality', 'if (r >= d)', 'if (r > d)', '__udivdi3'),
    ('shift64-upper-half', 'lo = hi >> (b - 32);', 'lo = (hi >> (b - 32)) ^ 1u;', '__lshrdi3'),
    ('signed-remainder', 'return (int32_t)(a < 0 ? 0u - r : r);', 'return (int32_t)r;', '__modsi3'),
]
driver = '''import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import ctrl_image_selftest as test
test.ctrl_image.HELPERS = Path(sys.argv[2])
sys.exit(test.main(["--require-rv32", "--out", sys.argv[3]]))
'''
def run(plant):
    name, old, new, helper = plant
    changed = source
    if name.startswith('divide'):
        begin = changed.index('static uint' + ('32' if '32' in name else '64') + '_t image_udivmod')
        end = changed.index('\n}', begin) + 2
        body = changed[begin:end]
        assert body.count(old) == 1
        changed = changed[:begin] + body.replace(old, new) + changed[end:]
    else:
        assert changed.count(old) == 1
        changed = changed.replace(old, new)
    target = work / name
    target.mkdir(exist_ok=True)
    (target / 'image_arith.c').write_text(changed)
    env = {**os.environ, 'MILAN_RV32_CC': cc, 'PYTHONDONTWRITEBYTECODE': '1'}
    command = [sys.executable, '-c', driver, str(repo / 'sw/firmware/ctrl/test'),
               str(target / 'image_arith.c'), str(target / 'selftest')]
    result = subprocess.run(command, capture_output=True, text=True, env=env, timeout=120)
    log = result.stdout + result.stderr
    (target / 'raw.log').write_text(log)
    assert result.returncode == 1 and 'MISMATCH ' + helper in log, (name, result.returncode, log)
    return name, result.returncode, log

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    for name, rc, log in pool.map(run, plants):
        print(f'CAUGHT {name}: self-test exit {rc}')
        print(log)
print('PASS: 6/6 arithmetic defects rejected by the self-test; no repository edits')
