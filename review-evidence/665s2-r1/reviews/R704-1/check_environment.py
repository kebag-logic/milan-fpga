#!/usr/bin/env python3
"""Record execution identities and the reviewed delta without account metadata."""
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(os.environ['REVIEW_ROOT'])
packet = Path(os.environ['REVIEW_PACKET'])
def run(argv):
    return subprocess.check_output(argv, cwd=root, text=True).strip()
out = {'python': sys.version, 'simulator': run(['verilator', '--version']),
       'compiler': run([os.environ['MILAN_RV32_CC'], '--version']).splitlines()[0],
       'head': run(['git', 'rev-parse', 'HEAD']),
       'tree': run(['git', 'rev-parse', 'HEAD^{tree}']),
       'base': run(['git', 'rev-parse', 'e76a755a']),
       'delta': run(['git', 'diff', '--name-status', 'e76a755a', 'HEAD']).splitlines(),
       'commit_subjects': run(['git', 'log', '--format=%s', 'e76a755a..HEAD']).splitlines(),
       'diff_check': run(['git', 'diff', '--check', 'e76a755a', 'HEAD']),
       'max_parallel_simulations': 16, 'native_build_jobs': 16,
       'execution': 'Foreground drivers joined all children; no detached jobs'}
assert out['simulator'].startswith('Verilator 5.050 ')
assert all(line.startswith('A\ttb/verilator/ctrl_service_budget/') for line in out['delta'])
(packet / 'environment.json').write_text(json.dumps(out, indent=2) + '\n')
print(out['simulator'], out['compiler'], len(out['delta']), 'new files')
