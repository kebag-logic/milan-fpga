"""Run bounded independent offline checks concurrently and retain raw receipts.

Usage: python3 -B run_checks.py CHECKOUT PUBLIC_PACKET OUTPUT [PYTHON]
All subprocess calls are foreground and joined before this command returns.
"""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess
import sys
import time

repo, packet, output = map(lambda p: Path(p).resolve(), sys.argv[1:4])
python = sys.argv[4] if len(sys.argv) > 4 else sys.executable
scratch = output / 'scratch'
cases = {
    'checkout-initial': [sys.executable, '-B', str(output / 'verify_checkout.py'), str(repo)],
    'startup-replay': [sys.executable, '-B', str(packet / 'check_startup.py'), str(packet)],
    'startup-decode': [sys.executable, '-B', str(packet / 'startup_decode.py'), str(packet / 'startup-headers.json')],
    'restore-replay': [sys.executable, '-B', str(packet / 'restore_compare.py'), str(packet / 'restore-start.json'), str(packet / 'restore-end.json')],
    'restore-controls': [sys.executable, '-B', str(packet / 'check_restore.py'), str(packet), str(scratch / 'restore-controls')],
    'docs': [python, '-B', 'scripts/docs_check.py'],
    'style': [python, '-B', 'scripts/check_doc_style.py'],
    'contents': [python, '-B', 'scripts/gen_toc.py', '--check'],
    'punctuation': [python, '-B', 'scripts/check_em_dash.py', '--base', 'fa450d301805881ad713b67521477bf042ddadfd'],
    'paths': [python, '-B', 'scripts/check_doc_paths.py'],
    'policy': [sys.executable, '-B', 'scripts/check_baremetal_only.py', '--check'],
    'whitespace': ['git', 'diff', '--check', 'fa450d301805881ad713b67521477bf042ddadfd..2263c6288956a5edd841df62252326780edd4870'],
}

def run(item):
    name, argv = item
    before = time.monotonic()
    try:
        with (output / (name + '.log')).open('wb') as log:
            result = subprocess.run(argv, cwd=repo, stdout=log, stderr=subprocess.STDOUT, timeout=480)
        rc = result.returncode
    except subprocess.TimeoutExpired:
        rc = 124
    (output / (name + '.rc')).write_text(str(rc) + '\n')
    print(f'{name}: rc={rc}', flush=True)
    safe = ['<packet>' if x == str(packet) else x.replace(str(packet), '<packet>').replace(str(output), '<review-output>').replace(str(repo), '<checkout>') for x in argv]
    return dict(name=name, command=safe, rc=rc, elapsed_seconds=round(time.monotonic() - before, 3))

with ThreadPoolExecutor(max_workers=6) as executor:
    results = list(executor.map(run, cases.items()))
(output / 'execution.json').write_text(json.dumps(results, indent=2) + '\n')
sys.exit(0 if all(r['rc'] == 0 for r in results) else 1)
