#!/usr/bin/env python3
"""Run focused exact-source checks concurrently, keeping all builds in scratch."""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import io

PACKET = Path(__file__).resolve().parent
SOURCE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
HEAD = '6ddfcda4c3170b8f463c8623833f7541ca8c1faf'
SIM = os.environ.get('REVIEW_SIM', '$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=SOURCE, text=True).strip() == HEAD
version = subprocess.check_output([SIM, '--version'], text=True)
assert 'Verilator 5.050' in version
(PACKET/'simulator-identity.txt').write_text(version)
TREE = PACKET/'scratch'/'focused'
TREE.mkdir(parents=True, exist_ok=True)
data = subprocess.check_output(['git', 'archive', HEAD], cwd=SOURCE)
with tarfile.open(fileobj=io.BytesIO(data)) as archive:
    archive.extractall(TREE, filter='data')

def run(pair):
    suite, group = pair
    cmd = ['make', '-j16', '-C', str(TREE/'tb'/suite), 'VERILATOR='+SIM+' -j 4', 'RUN_ARGS='+group]
    # The last -j takes precedence; replace the recipe's unlimited build jobs.
    makefile = TREE/'tb'/suite/'Makefile'
    makefile.write_text(makefile.read_text().replace('--build -j 0', '--build -j 4'))
    name = suite+'-'+group
    with (PACKET/(name+'.log')).open('w') as log:
        log.write('source '+HEAD+'\ncommand '+repr(cmd)+'\n'); log.flush()
        result = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT)
    (PACKET/(name+'.rc')).write_text(str(result.returncode)+'\n')
    return name, result.returncode

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    for name, rc in pool.map(run, [('srp_stream_fsms','suite'), ('srp_top','share')]):
        print(name, rc, flush=True)
