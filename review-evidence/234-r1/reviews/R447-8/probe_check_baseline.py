#!/usr/bin/env python3
"""Disposable probes: mutate a copy of the committed baseline and confirm check-baseline rejects it.
Usage: probe_check_baseline.py REPO SCRATCHDIR"""
import copy, json, pathlib, subprocess, sys
repo, scratch = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
scratch.mkdir(parents=True, exist_ok=True)
base = json.loads((repo / 'syn/ooc/pp_resource_baseline.json').read_text())
def run(name, mutate, expect_fail=True):
    b = copy.deepcopy(base); mutate(b)
    p = scratch / f'{name}.json'; p.write_text(json.dumps(b, indent=1) + '\n')
    r = subprocess.run(['python3', 'syn/ooc/pp_resource_gate.py', 'check-baseline', '--baseline', str(p)],
                       cwd=repo, capture_output=True, text=True)
    ok = (r.returncode != 0) == expect_fail
    msg = (r.stdout + r.stderr).strip().splitlines()
    print(f'{"PASS" if ok else "FAIL"} {name}: rc={r.returncode} :: {msg[-1][:220] if msg else ""}')
    return ok
E = lambda b, ep: b['endpoints'][ep]
results = [
    run('control-unchanged', lambda b: None, expect_fail=False),
    run('route-LUT-tolerance-501', lambda b: E(b, 'route-1x1')['tolerance'].__setitem__('LUT', 501)),
    run('route-FF-tolerance-599', lambda b: E(b, 'route-1x1')['tolerance'].__setitem__('FF', 599)),
    run('ooc8x8-LUT-tolerance-315', lambda b: E(b, 'ooc-8x8')['tolerance'].__setitem__('LUT', 315)),
    run('route-WNS-floor-0.02', lambda b: E(b, 'route-1x1')['floor'].__setitem__('WNS_ns', 0.02)),
    run('route-BRAM-ceiling-122', lambda b: E(b, 'route-1x1')['ceiling'].__setitem__('BRAM_TILE', 122)),
    run('route-record-WNS-below-floor', lambda b: E(b, 'route-1x1')['record']['figures'].__setitem__('WNS_ns', 0.02)),
    run('route-record-BRAM-over-ceiling', lambda b: E(b, 'route-1x1')['record']['figures'].__setitem__('BRAM_TILE', 122.0)),
    run('route-record-digest-not-hex', lambda b: E(b, 'route-1x1')['record'].__setitem__('inputs_sha256', 'x' * 64)),
    run('route-measured-note-removed', lambda b: E(b, 'route-1x1').pop('measured')),
]
print('ALL PROBES BEHAVED' if all(results) else 'SOME PROBE MISBEHAVED')
