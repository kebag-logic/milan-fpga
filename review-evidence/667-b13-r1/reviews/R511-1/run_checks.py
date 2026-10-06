#!/usr/bin/env python3
"""Run independent read-only gates concurrently and wait in the foreground.

Usage: python3 run_checks.py REPOSITORY PACKET_DIRECTORY [DOCS_PYTHON]
"""
import concurrent.futures
import json
from pathlib import Path
import subprocess
import sys

repo, packet = map(lambda s: Path(s).resolve(), sys.argv[1:3])
py = sys.argv[3] if len(sys.argv)>3 else sys.executable
logs=packet/'receipts'
logs.mkdir(exist_ok=True)
checks = {
    'docs-check': [py,'scripts/docs_check.py'],
    'doc-style': [py,'scripts/check_doc_style.py'],
    'toc': [py,'scripts/gen_toc.py','--check'],
    'em-dash': [py,'scripts/check_em_dash.py','--base','423ac5d910d09ab189b3acc39ae3ae1d10d50b19'],
    'doc-paths': [py,'scripts/check_doc_paths.py'],
    'baremetal': [py,'scripts/check_baremetal_only.py','--check'],
    'diff-check': ['git','diff','--check','423ac5d910d09ab189b3acc39ae3ae1d10d50b19..HEAD'],
    'evidence-audit': [sys.executable,str(packet/'audit_evidence.py'),str(repo),str(packet/'scratch/public')],
}
def run(item):
    name,cmd=item
    with (logs/(name+'.log')).open('w') as f:
        r=subprocess.run(cmd,cwd=repo,stdout=f,stderr=subprocess.STDOUT,timeout=300)
    (logs/(name+'.rc')).write_text(str(r.returncode)+'\n')
    return name,r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results=dict(pool.map(run,checks.items()))
(logs/'checks.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
sys.exit(any(results.values()))
