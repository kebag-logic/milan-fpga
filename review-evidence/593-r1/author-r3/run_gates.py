#!/usr/bin/env python3
"""Run the assigned gates synchronously and retain bounded receipts."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path('$LANES/593-mr-tu-soak')
OUT = Path(__file__).resolve().parent
BASE = '6d5ebd7357c1e468e446f18a61527c5be6118a04'
COMMANDS = [
 ['python3', '-B', 'tb/tools/torture_campaign.py', '--self-test'],
 ['python3', '-B', 'tb/tools/torture_release_mutants.py'],
 ['python3', '-B', '-m', 'behave', 'tests/features/torture_campaign_plan.feature', '-f', 'progress'],
 ['python3', '-B', '-m', 'behave', 'tests/features', '--tags=@torture', '-f', 'progress'],
 ['python3', 'scripts/ci_scope.py', '--selftest'],
 ['python3', 'scripts/check_baremetal_only.py', '--check'],
 ['python3', 'scripts/check_baremetal_only.py', '--selftest'],
 ['git', 'diff', '--check'],
 ['git', 'diff', BASE, 'HEAD', '--check'],
]
for script, options in [
 ('docs_check.py', [[]]),
 ('check_em_dash.py', [['--base', BASE], ['--selftest']]),
 ('check_doc_style.py', [[], ['--selftest']]),
 ('check_feature_status.py', [['--self-test']]),
 ('check_doc_paths.py', [[]]),
 ('check_archive.py', [[], ['--selftest']]),
 ('gen_toc.py', [['--selftest'], ['--verify-anchors'], ['--check']]),
 ('check_gptp_docs.py', [['--with-submodule'], ['--selftest']]),
 ('check_solution_docs.py', [[], ['--selftest']]),
 ('check_submodule_docs.py', [[], ['--selftest']]),
 ('check_py_idiom.py', [[], ['--selftest']]),
 ('check_hygiene.py', [['--check'], ['--selftest']]),
 ('check_todo_ownership.py', [[], ['--selftest']]),
]:
 for option in options:
  COMMANDS.append(['python3', 'scripts/' + script, *option])
COMMANDS.append(['python3', 'docs/traceability/gen_module_matrix.py', '--check'])
COMMANDS.append(['python3', '-B', 'tb/tools/torture_campaign.py', '--coverage-by-area', '--areas', 'soak,power'])

def run(label, command):
 head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
 started = time.monotonic()
 result = subprocess.run(['rtk', 'proxy', *command], cwd=ROOT, env=dict(os.environ, PYTHONPATH='/tmp/milan-593-markdown', PYTHONDONTWRITEBYTECODE='1'), capture_output=True, timeout=1800)
 data = result.stdout + result.stderr
 receipt = {'command': ['rtk', 'proxy', *command], 'cwd': str(ROOT), 'head': head, 'rc': result.returncode, 'seconds': round(time.monotonic()-started, 3), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
 if len(data) <= 200000:
  receipt['log'] = label + '.log'
  (OUT / receipt['log']).write_bytes(data)
 print(label, 'rc', result.returncode, 'bytes', len(data), flush=True)
 return receipt

if __name__ == '__main__':
 results = []
 for index, command in enumerate(COMMANDS, 1):
  results.append(run(f'gate-{index:02}', command))
  (OUT / 'gates.json').write_text(json.dumps(results, indent=2)+'\n')
  if results[-1]['rc']:
   sys.exit(results[-1]['rc'])
