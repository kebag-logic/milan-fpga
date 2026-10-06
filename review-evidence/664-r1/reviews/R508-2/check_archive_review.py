#!/usr/bin/env python3
"""Repeat the two relevant gates in a disposable metadata-free source archive."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile

ap = argparse.ArgumentParser()
ap.add_argument('repo', type=Path)
args = ap.parse_args()
packet = Path(__file__).resolve().parent
scratch = packet/'scratch'
root = Path(tempfile.mkdtemp(prefix='source-archive-', dir=scratch))
head = '8fb296e3e02985aee27ef04cb08278836b734a14'
blob = subprocess.check_output(['git', '-C', str(args.repo), 'archive', head])
with tarfile.open(fileobj=io.BytesIO(blob)) as archive:
    archive.extractall(root, filter='data')
env = {**os.environ, 'PYTHONPATH': str(scratch/'markdown-deps'),
       'PYTHONDONTWRITEBYTECODE': '1', 'TMPDIR': str(scratch)}


def run(name):
    with (packet/f'archive-{name}.log').open('w') as log:
        log.write(f'head {head}\nmetadata-free git archive; no imported submodule files\n')
        log.write(f'command python3 scripts/{name}.py\n')
        log.flush()
        result = subprocess.run([sys.executable, f'scripts/{name}.py'], cwd=root,
                                env=env, stdout=log, stderr=subprocess.STDOUT, timeout=480)
    (packet/f'archive-{name}.rc').write_text(f'{result.returncode}\n')
    print(f'{name}: rc {result.returncode}', flush=True)
    return {'check': name, 'rc': result.returncode}


with ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(run, ['docs_check', 'check_feature_status']))
(packet/'archive-results.json').write_text(json.dumps(results, indent=2)+'\n')
sys.exit(any(result['rc'] for result in results))
