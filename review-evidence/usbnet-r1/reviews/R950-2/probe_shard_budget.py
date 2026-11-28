#!/usr/bin/env python3
"""Compare the published source and dependency scheduling arithmetic without running suites."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import types

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
source = root / 'scripts/suite_shards.py'
spec = importlib.util.spec_from_file_location('review_shards', source)
current = importlib.util.module_from_spec(spec)
spec.loader.exec_module(current)
def git(ref, path):
    return subprocess.check_output(['git', '-C', str(root), 'show', ref + ':' + path], text=True)
base = types.ModuleType('dependency_shards')
base.__file__ = str(source)
exec(compile(git('640699e6', 'scripts/suite_shards.py'), str(source), 'exec'), base.__dict__)
suites = current.expand_suites(current.sweep_suites(root/'tb/verilator'))
results = {}
for label, module, inventory, workflow in [
    ('head', current, suites, (root/'.github/workflows/rtl.yml').read_text()),
    ('dependency_without_added_usbnet', base, [s for s in suites if s != 'usbnet'], git('640699e6', '.github/workflows/rtl.yml')),
]:
    problems, load, bounds = module.headroom_problems(inventory, workflow)
    owners, _ = module.balance(inventory, len(load))
    results[label] = dict(problems=problems, load_seconds=load, timeout_bounds_seconds=bounds,
                         absolute_cap_seconds=module.CI_BUDGET_SECONDS,
                         worker25=[s for s in inventory if owners[s] == 25],
                         usbnet_worker=owners.get('usbnet'))
before = set(base.sweep_suites(root/'tb/verilator')) - {'usbnet'}
tracked = subprocess.check_output(['git', '-C', str(root), 'ls-tree', '-r', '--name-only', '640699e6', '--', 'tb/verilator'], text=True).splitlines()
results['dependency_inventory_check'] = sorted(s for s in before if f'tb/verilator/{s}/Makefile' not in tracked)
(packet/'shard-budget-differential.json').write_text(json.dumps(results, indent=2)+'\n')
print(json.dumps(results, indent=2))
