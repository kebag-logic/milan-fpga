#!/usr/bin/env python3
"""Run independent read-only review checks concurrently in one foreground process.
Usage: python3 run_checks.py REPO PACKET PINNED_PYTHON
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json, subprocess, sys, time
repo, out = [Path(x).resolve() for x in sys.argv[1:3]]
py = Path(sys.argv[3]).absolute()
log = out / 'public/author-r2/receipts/round2/sweep/excerpts/capture_coherence.txt'
checks = {
 'bounds': [str(out/'check_bounds.py'), str(repo), str(log)],
 'evidence-audit': [str(out/'verify_evidence.py'), str(repo), str(out)],
 'tree-audit': [str(out/'audit_tree.py'), str(repo)],
 'docs-check': ['scripts/docs_check.py'],
 'doc-style': ['scripts/check_doc_style.py'],
 'em-dash': ['scripts/check_em_dash.py', '--base', 'a032c6d6'],
 'doc-paths': ['scripts/check_doc_paths.py'],
 'toc-anchors': ['scripts/gen_toc.py', '--verify-anchors'],
 'toc-check': ['scripts/gen_toc.py', '--check'],
}
def run(item):
 name, args = item
 t = time.monotonic()
 result = subprocess.run([str(py), *args], cwd=repo, capture_output=True, timeout=300)
 (out/(name+'.log')).write_bytes(result.stdout+result.stderr)
 (out/(name+'.rc')).write_text(str(result.returncode)+'\n')
 public_args = [str(a).replace(str(repo),'<repo>').replace(str(out),'<packet>') for a in args]
 return dict(name=name, command=['pinned-python',*public_args], rc=result.returncode, seconds=round(time.monotonic()-t,3))
with ThreadPoolExecutor(max_workers=6) as pool:
 rows=list(pool.map(run,[(k,v) for k,v in checks.items() if len(sys.argv)==4 or k in sys.argv[4:]]))
record = out/'checks.json'
prior = json.loads(record.read_text()) if record.exists() else []
prior = [row for row in prior if row['name'] not in {r['name'] for r in rows}]
record.write_text(json.dumps(prior+rows,indent=2)+'\n')
for row in rows: print(row['name'], 'rc='+str(row['rc']), str(row['seconds'])+'s')
sys.exit(any(row['rc'] for row in rows))
