#!/usr/bin/env python3
"""Run only affected lightweight gates, concurrently. Usage: focused_gates.py CHECKOUT PACKET."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys

root, packet = map(lambda s: Path(s).resolve(), sys.argv[1:])
out=packet/'receipts'
env=dict(os.environ, TMPDIR=str(packet/'scratch'), PYTHONDONTWRITEBYTECODE='1')
gates={
 'ci-events-check':['python3','scripts/ci_events.py','--check'],
 'ci-events-selftest':['python3','scripts/ci_events.py','--selftest'],
 'suite-tally':['python3','scripts/suite_tally.py','--selftest'],
 'cancellation':['python3','scripts/test_suite_cancellation.py'],
 'python-idiom':['python3','scripts/check_py_idiom.py'],
 'test-evidence':['python3','scripts/measure_test_evidence.py','--check'],
 'docs-check':['python3','scripts/docs_check.py'],
 'doc-style':['python3','scripts/check_doc_style.py'],
 'doc-paths':['python3','scripts/check_doc_paths.py'],
 'toc':['python3','scripts/gen_toc.py','--check'],
 'em-dash':['python3','scripts/check_em_dash.py','--base','c6bd08c6'],
 'diff-check':['git','diff','--check','c6bd08c6','HEAD'],
}
def run(item):
 name,cmd=item
 p=subprocess.run(cmd,cwd=root,env=env,capture_output=True,text=True,timeout=540)
 (out/(name+'.log')).write_text(p.stdout+p.stderr)
 (out/(name+'.rc')).write_text(str(p.returncode)+'\n')
 return name,{'command':cmd,'rc':p.returncode}
with ThreadPoolExecutor(max_workers=6) as pool:
 results=dict(pool.map(run,gates.items()))
(out/'focused-gates.json').write_text(json.dumps(results,indent=2)+'\n')
for name,r in results.items(): print(name,r['rc'])
sys.exit(1 if any(r['rc'] for r in results.values()) else 0)
