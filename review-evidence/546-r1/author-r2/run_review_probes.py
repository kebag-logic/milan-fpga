import hashlib
import importlib.util
import subprocess
import sys
from pathlib import Path

source = Path('/tmp/546-a271-review-4gbqea6u/review-evidence/546-r1/reviews/R302-1')
spec = importlib.util.spec_from_file_location('review_probes', source / 'probes/run_probes.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
# Only bind the archived runner's pinned revision to this round's candidate.
# Scenarios, mutations, builds, grading and every archived source byte stay unchanged.
module.HEAD = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
print('Candidate', module.HEAD, flush=True)
for p in sorted((source / 'probes').iterdir()):
    if not p.is_file():
        continue
    print(p.name, hashlib.sha256(p.read_bytes()).hexdigest(), flush=True)
sys.argv = [str(source / 'probes/run_probes.py'), str(Path.cwd()), str(source)]
raise SystemExit(module.main())
