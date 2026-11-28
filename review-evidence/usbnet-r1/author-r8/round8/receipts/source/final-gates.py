"""Run the focused final-head gates with their CI arguments and removal auditing."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

OUT = Path(__file__).resolve().parent.parent
AUDIT = str(OUT / 'source/audited-python.py')
MD = '$VALIDATION_STORAGE/usbnet-a855/round6/markdown-venv/bin/python3'
PY = sys.executable
env = dict(os.environ, TMPDIR='$VALIDATION_STORAGE/usbnet-a855/round8/tmp', PYTHONDONTWRITEBYTECODE='1',
           CCACHE_DIR='$VALIDATION_STORAGE/ccache')
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
jobs = [
    ('ledger-selftest', PY, ['tb/verilator/ctrl_service_budget/egress_ledger.py', '--selftest']),
    ('docs-check', PY, ['scripts/docs_check.py']),
    ('contents-selftest', MD, ['scripts/gen_toc.py', '--selftest']),
    ('contents-anchors', MD, ['scripts/gen_toc.py', '--verify-anchors']),
    ('contents-check', MD, ['scripts/gen_toc.py', '--check']),
    ('doc-paths', PY, ['scripts/check_doc_paths.py']),
    ('inventory-check', PY, ['scripts/docs_inventory.py', '--check']),
    ('inventory-selftest', PY, ['scripts/docs_inventory.py', '--selftest']),
    ('python-idiom', PY, ['scripts/check_py_idiom.py']),
    ('fail-fast', PY, ['scripts/measure_fail_fast.py', '--check']),
    ('hygiene', PY, ['scripts/check_hygiene.py', '--check']),
    ('naming', PY, ['scripts/measure_naming.py', '--check']),
    ('test-evidence', PY, ['scripts/measure_test_evidence.py', '--check']),
    ('em-dash', MD, ['scripts/check_em_dash.py', '--base', 'a4f00496fdaede7a6e6baee46e360f7cbc7f0c95']),
]

def one(job):
    name, interpreter, args = job
    command = [interpreter, '-B', AUDIT, *args]
    path = OUT / (name + '.log')
    started = time.monotonic()
    with path.open('w') as log:
        result = subprocess.run(command, env=env, stdout=log, stderr=subprocess.STDOUT)
    record = dict(name=name, head=head, ci_arguments=[interpreter, *args], actual_command=command,
                  returncode=result.returncode, seconds=time.monotonic() - started,
                  log=path.name, log_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    print(name, result.returncode, flush=True)
    return record

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    records = list(pool.map(one, jobs))
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() == head
(OUT / 'final-gates.json').write_text(json.dumps(records, indent=2) + '\n')
raise SystemExit(any(r['returncode'] for r in records))
