"""Run the remaining assigned gates sequentially, preserving every exit."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path('$LANES/571-pp-unit-counts')
OUTPUT = Path(__file__).resolve().parent
WORK = Path('/tmp/571-a371')
GATES = [
    ('builder-absent', [sys.executable, '-u', str(OUTPUT / 'builder_absent.py')]),
    ('entity-shape-final', [sys.executable, '-u', 'scripts/check_entity_shape.py', '--self-test']),
    ('python-idiom-final', [sys.executable, 'scripts/check_py_idiom.py']),
    ('diff-check', ['git', 'diff', '--check']),
]
rows = []
for name, command in GATES:
    print('START', name, flush=True)
    started = time.monotonic()
    log = WORK / f'{name}.log'
    with log.open('w') as stream:
        result = subprocess.run(['rtk', 'proxy', *command], cwd=ROOT, stdout=stream,
                                stderr=subprocess.STDOUT, timeout=7200)
    rows.append({'name': name, 'command': ['rtk', 'proxy', *command],
                 'rc': result.returncode, 'seconds': round(time.monotonic()-started, 2),
                 'log': str(log), 'bytes': log.stat().st_size,
                 'sha256': hashlib.sha256(log.read_bytes()).hexdigest()})
    (WORK / 'gate-results.json').write_text(json.dumps(rows, indent=2) + '\n')
    print('END', name, result.returncode, flush=True)
    if result.returncode:
        print(log.read_text()[-8000:], flush=True)
        raise SystemExit(result.returncode)
