#!/usr/bin/env python3
"""Probe: apply the CPU budget harness's own variant arms (build.variant_fixture) and
control plants (build.mutated_source) to a checkout's sources, outside the checkout.
usage: probe_harness_anchors.py <checkout> <out>"""
import sys
from pathlib import Path
root, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path[:0] = [str(root / 'tb/verilator/ctrl_service_budget')]
import build
for v in build.VARIANTS:
    try:
        build.variant_fixture(out / f'v-{v}', v); print('VARIANT', v, 'APPLIES')
    except Exception as e:
        print('VARIANT', v, 'FAILS', e)
for m in build.MUTATIONS:
    try:
        build.mutated_source(out / f'm-{m}', m); print('MUTATION', m, 'APPLIES')
    except Exception as e:
        print('MUTATION', m, 'FAILS', e)
