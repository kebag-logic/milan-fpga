#!/usr/bin/env python3
"""Read-only focused documentation and budget gates; run from the candidate root."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import os
import subprocess
import sys

packet = Path(__file__).resolve().parent
receipts = packet / 'receipts'
receipts.mkdir(exist_ok=True)
python = sys.executable
docs_python = os.environ.get('REVIEW_DOCS_PYTHON', python)
checks = {
    'docs': [docs_python, '-B', 'scripts/docs_check.py'],
    'em-dash': [docs_python, '-B', 'scripts/check_em_dash.py', '--base', 'dd163e41'],
    'flip-1x1': [python, '-I', 'tb/verilator/ctrl_service_budget/flip_grade.py', '--check', '--point', '1x1/1if'],
    'flip-8x8': [python, '-I', 'tb/verilator/ctrl_service_budget/flip_grade.py', '--check', '--point', '8x8/1if'],
    'load': [python, '-I', 'tb/verilator/ctrl_service_budget/load_grade.py', '--check'],
    'shape': [python, '-I', 'tb/verilator/ctrl_service_budget/shape_costs.py', '--check'],
    'diff-check': ['git', 'diff', '--check', 'dd163e41', 'HEAD'],
}


def run(item):
    name, args = item
    with (receipts / (name + '.log')).open('w') as out:
        out.write('COMMAND ' + ' '.join(args).replace(docs_python, 'python3').replace(python, 'python3') + '\n')
        out.flush()
        result = subprocess.run(args, stdout=out, stderr=subprocess.STDOUT, timeout=300)
    (receipts / (name + '.rc')).write_text(str(result.returncode) + '\n')
    return name, result.returncode


with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, checks.items()))
for name, rc in results:
    print(name, rc)
sys.exit(any(rc for _, rc in results))
