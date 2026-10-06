#!/usr/bin/env python3
"""Run bounded independent documentation checks under one foreground process."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
receipt = packet / 'receipts'
scratch = packet / 'scratch'
env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'TMPDIR': str(scratch), 'GIT_NO_REPLACE_OBJECTS': '1', 'GIT_OPTIONAL_LOCKS': '0'}
checks = {
    'docs': ['scripts/docs_check.py'],
    'style': ['scripts/check_doc_style.py'],
    'paths': ['scripts/check_doc_paths.py'],
    'toc': ['scripts/gen_toc.py', '--check'],
    'anchors': ['scripts/gen_toc.py', '--verify-anchors'],
    'traceability': ['docs/traceability/gen_module_matrix.py', '--check'],
    'em-dash': ['scripts/check_em_dash.py', '--base', '30e3c018b9add0cb182d8f1229eeec062218130d'],
    'mailbox-contract': ['sw/mailbox/gen_mailbox.py', '--check', '--crosscheck'],
    'mailbox-controls': ['sw/mailbox/gen_mailbox.py', '--selftest'],
}


def run(item):
    name, arguments = item
    start = time.monotonic()
    with (receipt / (name + '.log')).open('w') as log:
        log.write('COMMAND: python3 ' + ' '.join(arguments) + '\n')
        log.flush()
        result = subprocess.run([sys.executable, *arguments], cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=480)
    record = {'check': name, 'rc': result.returncode, 'seconds': round(time.monotonic() - start, 3)}
    (receipt / (name + '.rc')).write_text(str(result.returncode) + '\n')
    return record


with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, checks.items()))
(receipt / 'focused-results.json').write_text(json.dumps(results, indent=2) + '\n')
for result in results:
    print(json.dumps(result))
sys.exit(int(any(result['rc'] for result in results)))
