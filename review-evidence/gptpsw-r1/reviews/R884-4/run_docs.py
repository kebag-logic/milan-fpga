#!/usr/bin/env python3
"""Run independent documentation gates concurrently, with a foreground coordinator."""
from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
import subprocess
import sys

repo, out = map(Path, sys.argv[1:3])
python = out / 'scratch/docs-venv/bin/python3'
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_NO_REPLACE_OBJECTS='1')
commands = {
    'docs_check': ['scripts/docs_check.py'],
    'doc_style': ['scripts/check_doc_style.py'],
    'doc_paths': ['scripts/check_doc_paths.py'],
    'docs_inventory': ['scripts/docs_inventory.py', '--check'],
    'em_dash': ['scripts/check_em_dash.py', '--base', '8267b8951616cfd570baf690835d4b0d38f14596'],
    'toc': ['scripts/gen_toc.py', '--check'],
}
def run(item):
    name, args = item
    with (out / (name + '.log')).open('w') as log:
        log.write('COMMAND python3 ' + ' '.join(args) + '\n')
        log.flush()
        result = subprocess.run([str(python), '-B', *args], cwd=repo, env=env, stdout=log, stderr=subprocess.STDOUT)
    (out / (name + '.rc')).write_text(str(result.returncode) + '\n')
    return name, result.returncode
with ThreadPoolExecutor(max_workers=6) as pool:
    results = list(pool.map(run, commands.items()))
for name, rc in results:
    print(name, 'rc=' + str(rc))
sys.exit(int(any(rc for _, rc in results)))
