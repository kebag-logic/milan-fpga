#!/usr/bin/env python3
"""Focused dependency judgments and the source-owned pin controls, in disposable copies."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import sys

ap = argparse.ArgumentParser()
ap.add_argument('checkout', type=Path)
ap.add_argument('scratch', type=Path)
a = ap.parse_args()
root, scratch = a.checkout.resolve(), a.scratch.resolve()
os.environ['TMPDIR'] = str(scratch)
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
sys.dont_write_bytecode = True
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import ctrl_boundary as b
import ctrl_capture as c
import ctrl_configs as cfg
import ctrl_pin as pin
import ctrl_plants as plants
import ctrl_runs as runs

# These exercise dependency judgments with real compiles. They do not replace
# the full gate's required-builder population check or its hosted invocation.
indices = [6, 20, 31, 42, 49, 60, 61, 62, 63, 64, 65, 68, 71, 73, 75, 101, 102]
nothing = c.Capture((), (), (), ())

def one(index):
    plant = plants.PLANTS[index]
    work = scratch / 'selected-controls' / str(index)
    copy = b.mirror(plant, work)
    _, own = runs.control_capture(plant, copy, nothing, work / 'run')
    places = b.Places((copy, root), b.targets(own, (copy, root)))
    found = list(b.judged(own, places)) + b.shadows((copy,))
    errors = cfg.unlisted(own) + cfg.expanded(own, cfg.places((copy, root)))
    assert not errors, errors
    compiled = [s for inv in own.invocations for s in inv.sources if s.deps is not None and not s.error]
    ok = any(plant.needle in f for f in found) if plant.needle else not found
    row = {'control': plant.name, 'compiled_sources': len(compiled),
           'expected': plant.needle or 'PASS', 'findings': found, 'ok': bool(ok)}
    assert compiled, row
    print(json.dumps(row), flush=True)
    return bool(ok)

def pins():
    where = scratch / 'selected-pin-controls'
    where.mkdir(parents=True, exist_ok=True)
    bad, count = pin.pin_controls(where, cfg.makefiles())
    print(json.dumps({'pin_controls': count, 'misbehaved': bad}), flush=True)
    return bad == 0

# Three compile workers and one pin-control lane; make recipes use -j16 only
# on refused poison inputs, so those controls reach no heavy parallel build.
with ThreadPoolExecutor(max_workers=4) as pool:
    pin_result = pool.submit(pins)
    results = list(pool.map(one, indices))
    results.append(pin_result.result())
print('focused dependency and pin controls:', 'PASS' if all(results) else 'FAIL')
sys.exit(not all(results))
