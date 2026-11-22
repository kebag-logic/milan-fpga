#!/usr/bin/env python3
"""Run independent light gates concurrently; no hardware or full build bank.

Usage: run_small_gates.py CHECKOUT PACKET --litex-python PYTHON --markdown-python PYTHON
The two interpreters must provide the repository's documented dependencies.
"""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('checkout', type=Path)
p.add_argument('packet', type=Path)
p.add_argument('--litex-python', required=True)
p.add_argument('--markdown-python', required=True)
a = p.parse_args()
root, packet = a.checkout.resolve(), a.packet.resolve()
tmp = packet / 'scratch/tmp'
tmp.mkdir(parents=True, exist_ok=True)
commands = {
    'flip-1x1': ['python3', '-I', 'tb/verilator/ctrl_service_budget/flip_grade.py', '--check', '--point', '1x1/1if'],
    'flip-8x8': ['python3', '-I', 'tb/verilator/ctrl_service_budget/flip_grade.py', '--check', '--point', '8x8/1if'],
    'load': ['python3', '-I', 'tb/verilator/ctrl_service_budget/load_grade.py', '--check'],
    'shape-costs': ['python3', '-I', 'tb/verilator/ctrl_service_budget/shape_costs.py', '--check'],
    'memory': [a.litex_python, '-B', 'sw/litex/test_ctrl_memory.py'],
    'docs': ['python3', '-B', 'scripts/docs_check.py'],
    'em-dash': [a.markdown_python, '-B', 'scripts/check_em_dash.py', '--base', 'dd163e41'],
}
def run(item):
    name, cmd = item
    with (packet / (name + '.log')).open('w') as out:
        out.write('COMMAND ' + json.dumps(cmd) + '\n')
        out.flush()
        rc = subprocess.run(cmd, cwd=root, env={**os.environ, 'TMPDIR': str(tmp)}, stdout=out,
                            stderr=subprocess.STDOUT, check=False).returncode
    (packet / (name + '.rc')).write_text(str(rc) + '\n')
    return [name, rc]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(run, commands.items()))
(packet / 'small-gate-results.json').write_text(json.dumps(results, indent=2) + '\n')
raise SystemExit(any(rc for _, rc in results))
