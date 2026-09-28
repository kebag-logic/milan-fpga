"""Run each assigned gate in the foreground at the committed candidate."""
from pathlib import Path
import json
import subprocess
import sys

OUT = Path(__file__).resolve().parent
ROOT = Path('$LANES/602-phc-step-mr')
RUNNER = OUT / 'run_gate.py'
checks = [
    ('short-gates', '3600', ['python3', str(OUT/'final_checks.py')]),
    ('milan-dp', '10800', ['make', '-C', str(ROOT/'tb/verilator/milan_dp'), 'run']),
    ('tkdiag', '1800', ['make', '-C', str(ROOT/'tb/verilator/tkdiag')]),
    ('gmstep-mutants', '7200', ['make', '-C', str(ROOT/'tb/verilator/milan_dp'), 'gmstep-mutants']),
    ('builder-rv32', '10800', ['python3', 'sw/builder/test_builder.py', '--require-rv32']),
    ('builder-absent', '10800', ['python3', str(OUT/'builder_absent.py')]),
    ('ooc-after', '14400', ['python3', str(OUT/'ooc_measure.py'), 'after']),
    ('artifact-identity', '1200', ['python3', str(OUT/'check_artifact_identity.py')]),
    ('stale-doc-rescan', '180', ['python3', str(OUT/'stale_doc_scan.py')]),
]
completed = []
for name, seconds, command in checks:
    print('START', name, flush=True)
    result = subprocess.run(['rtk', 'proxy', 'python3', str(RUNNER), name, seconds, *command], cwd=ROOT, check=False)
    completed.append({'gate':name, 'rc':result.returncode})
    (OUT/'campaign-progress.json').write_text(json.dumps(completed, indent=2)+'\n')
    print('FINISH', name, result.returncode, flush=True)
    if result.returncode:
        sys.exit(result.returncode)
print('All assigned gate groups returned 0.', flush=True)
