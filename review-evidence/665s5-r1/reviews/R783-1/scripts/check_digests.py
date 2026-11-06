#!/usr/bin/env python3
"""Compare every checkout-relative input digest recorded in the published build.json receipts with the bytes of
the tree under review, and recompute the firmware and configuration tree digests with the CPU budget harness's
own tree_digest (imported read only from the checkout).

Usage: python3 -I check_digests.py <checkout> <receipts dir>
"""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

root, rec = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
spec = importlib.util.spec_from_file_location('budget_build', root / 'tb/verilator/ctrl_service_budget/build.py')
b = importlib.util.module_from_spec(spec)
sys.modules['budget_build'] = b
spec.loader.exec_module(b)
bad = 0
for run in sorted((rec / 'runs').iterdir()) + [rec / 'merge']:
    d = json.loads((run / 'build.json').read_text())
    n = 0
    for k, v in d['inputs'].items():
        if k.startswith('checkout:'):
            got = hashlib.sha256((root / k.split(':', 1)[1]).read_bytes()).hexdigest()
            n += 1
            if got != v:
                bad += run.name != 'merge'
                print(f'DIFFERS  {run.name} {k}')
    fw = b.tree_digest([root / t for t in b.FIRMWARE_TREES])
    cfg = b.tree_digest([root / 'configs' / (d['shape'] + '.yaml')])
    ok_fw, ok_cfg = fw == d['inputs']['tree:firmware'], cfg == d['inputs']['tree:config']
    if run.name != 'merge':
        bad += (not ok_fw) + (not ok_cfg)
    print(f"{run.name:9s} cpu_clock {d['cpu_clock']} cpu_hz {d['cpu_hz']} sys_hz {d['sys_hz']} milan_hz {d['milan_hz']} "
          f"arm {d['arm']} point {d['point']} ledgered {d['ledgered']} plant {d['plant']}: {n} checkout inputs; "
          f"tree:firmware {'equal' if ok_fw else 'DIFFERS'}; tree:config {'equal' if ok_cfg else 'DIFFERS'}")
print('differences at the head (merge receipt excluded, it is another tree):', bad)
sys.exit(1 if bad else 0)
