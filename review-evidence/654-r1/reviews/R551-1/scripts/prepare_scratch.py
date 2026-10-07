#!/usr/bin/env python3
"""Prepare isolated inputs without changing the selected source or dependencies."""
import argparse
import json
import os
from pathlib import Path
import subprocess

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--root', required=True)
p.add_argument('--packet', required=True)
p.add_argument('--python', required=True)
args = p.parse_args()
root, packet = Path(args.root).resolve(), Path(args.packet).resolve()
scratch = packet / 'scratch'
(scratch / 'tmp').mkdir(parents=True, exist_ok=True)
(scratch / 'cpu').mkdir(exist_ok=True)
(packet / 'receipts').mkdir(exist_ok=True)
env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}
query = 'import json, pythondata_cpu_naxriscv as n, pythondata_cpu_vexiiriscv as v; print(json.dumps({"naxriscv":n.data_location,"vexiiriscv":v.data_location}))'
locations = json.loads(subprocess.check_output([args.python, '-c', query], env=env))
for family, source in locations.items():
    target = scratch / 'cpu' / family
    if target.exists():
        raise SystemExit('Use a fresh packet scratch directory')
    subprocess.run(['cp', '-a', '--reflink=auto', source, str(target)], check=True)
tree = scratch / 'export-tree'
subprocess.run(['git', 'clone', '--quiet', '--shared', str(root), str(tree)], check=True)
for name in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis'):
    subprocess.run(['git', '-C', str(tree), 'config', f'submodule.{name}.url', str(root / name)], check=True)
subprocess.run(['git', '-C', str(tree), '-c', 'protocol.file.allow=always', 'submodule',
                'update', '--init', '--jobs', '4', 'protocol-processor', 'gptp-processor',
                'third_party/verilog-axis'], check=True)
print('Prepared isolated CPU data and exact source clone')
