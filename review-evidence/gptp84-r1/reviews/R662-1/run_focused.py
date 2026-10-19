#!/usr/bin/env python3
"""Focused source review: isolated builds, explicit mutant failures, raw logs.

Usage: python3 run_focused.py SOURCE_ROOT --jobs 16
All temporary sources and builds stay in this packet's scratch directory.
"""
import argparse
import concurrent.futures
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
sys.dont_write_bytecode = True

ap = argparse.ArgumentParser()
ap.add_argument('source', type=Path)
ap.add_argument('--jobs', type=int, default=16)
ap.add_argument('--simulator', default='$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
a = ap.parse_args()
assert 1 <= a.jobs <= 16
root = a.source.resolve()
packet = Path(__file__).resolve().parent
work = packet / 'scratch/focused'
work.mkdir(parents=True, exist_ok=True)
logs = packet / 'focused'
logs.mkdir(exist_ok=True)
sim = a.simulator
env = os.environ.copy()
env['TMPDIR'] = str(work)

def command(tag, argv, cwd=root):
    with (logs / (tag + '.log')).open('w') as f:
        r = subprocess.run(argv, cwd=cwd, env=env, stdout=f, stderr=subprocess.STDOUT)
    (logs / (tag + '.rc')).write_text(str(r.returncode) + '\n')
    return r.returncode

assert command('simulator-identity', [sim, '--version']) == 0
assert '5.050' in (logs / 'simulator-identity.log').read_text()
spec = importlib.util.spec_from_file_location('mutants', root / 'tb/verilator/engine/mutants.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def build(tag, mutation=None):
    src = m.stage(work, tag, mutation)
    obj = work / ('obj_' + tag)
    flags = list(m.VFLAGS)
    flags[flags.index('-j') + 1] = str(max(1, a.jobs // 2))
    argv = [sim, *flags, '--Mdir', str(obj), '-CFLAGS', '-std=c++17 -O2 -Wall -Wextra',
            *[str(src / s) for s in m.RTL_SOURCES], str(m.HERE / 'sim_main.cpp'), '-o', 'engine']
    assert command(tag + '-build', argv) == 0
    return src, obj / 'engine'

def generate(src, tag, args):
    run = work / ('run_' + tag)
    run.mkdir(exist_ok=True)
    assert command(tag + '-generate', [sys.executable, str(src / m.GENERATOR),
                   *m.GENARGS, *args, '-o', str(run / 'gptp_ucode.hex')]) == 0
    return run

def run_case(exe, src, tag, args=(), plus=(), breaks=None):
    run = generate(src, tag, args)
    rc = command(tag, [str(exe), *plus], run)
    out = (logs / (tag + '.log')).read_text()
    v = m.verdict(rc, out)
    if breaks is not None:
        # Only this ordinary pass is run for mutants; exclude separately
        # prefixed priority-255 checks from this pass's required failures.
        required = [x for x in breaks.split(' | ') if not x.startswith('p1 255 ')]
        failed = [line for line in out.splitlines() if line.startswith('FAIL ')]
        missing = [x for x in required if not any(x in line for line in failed)]
        assert v == 'caught' and not missing, (tag, v, missing)
    else:
        assert v == 'pass', (tag, v)
    return {'case': tag, 'rc': rc, 'verdict': v, 'tally': m.TALLY.search(out).group(0)}

# These lightweight gates run concurrently with the control build. No
# source-generating make target runs in the reviewed checkout.
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
    gates = ex.submit(command, 'docs-contract', ['make', '-j16', 'docs', 'contract'])
    clean_src, exe = build('control')
    assert gates.result() == 0

rows = []
passes = [('control', (), ()), ('request-seed', ('--seq-seed','0x200000'), ()),
          ('sync-seed', ('--sync-seq-seed','0x10000'), ()),
          ('priority255', ('--p1','255'), ('+not-gm-capable',))]
with concurrent.futures.ThreadPoolExecutor(max_workers=min(a.jobs, 4)) as ex:
    futs = [ex.submit(run_case, exe, clean_src, t, g, p) for t,g,p in passes]
    rows.extend(f.result() for f in futs)

names = ['becoming grandmaster clears sync-ok',
         "a queued receipt timeout clears a master's sync-ok",
         'the received path is published without thisClock',
         'the appended entry is the announcing source']
selected = [next(x for x in m.MUTATIONS if x[0] == n) for n in names]
def mutant(i, row):
    name, file, pattern, replacement, breaks = row
    assert (m.HDL / file).read_text().count(pattern) == 1
    tag = 'mutant-' + str(i)
    if file == m.GENERATOR:
        src = m.stage(work, tag, (file, pattern, replacement))
        binary = exe
    else:
        src, binary = build(tag, (file, pattern, replacement))
    result = run_case(binary, src, tag, breaks=breaks)
    result['mutation'] = name
    return result
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
    rows.extend(ex.map(lambda x: mutant(*x), enumerate(selected)))

# Regenerate every committed image into disposable storage and compare bytes.
images = [('syn/ooc/work/gptp_ucode.hex', []),
          ('tb/verilator/ucpu/gptp_ucode.hex', []),
          ('tb/tsngen/gptp_ucode.hex', ['--clk-hz','2000000']),
          ('tb/verilator/engine/gptp_ucode.hex', list(m.GENARGS))]
for i, (path, args) in enumerate(images):
    out = work / ('image-' + str(i) + '.hex')
    assert command('image-' + str(i), [sys.executable, str(m.HDL / m.GENERATOR), *args, '-o', str(out)]) == 0
    assert out.read_bytes() == (root / path).read_bytes(), path
    rows.append({'image': path, 'byte_match': True})
(logs / 'summary.json').write_text(json.dumps(rows, indent=2) + '\n')
print(json.dumps(rows, indent=2))
