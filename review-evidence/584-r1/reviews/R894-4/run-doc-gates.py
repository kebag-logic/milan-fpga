#!/usr/bin/env python3
"""Run bounded documentation checks concurrently, keeping raw outputs and exits."""
import concurrent.futures
import pathlib
import subprocess
import sys

repo = pathlib.Path(sys.argv[1]).resolve()
out = pathlib.Path(__file__).resolve().parent
commands = {
    'docs-check': ['python3', 'scripts/docs_check.py'],
    'toc-check': ['python3', 'scripts/gen_toc.py', '--check'],
    'anchors': ['python3', 'scripts/gen_toc.py', '--verify-anchors'],
    'em-dash': ['python3', 'scripts/check_em_dash.py', '--base', '599c79af9cfe242bc3d60dd1c80f3e8d57cca12e'],
}
def run(item):
    name, command = item
    command[0] = sys.executable
    with (out / (name + '.log')).open('wb') as log:
        log.write(('Command: ' + ' '.join(command) + '\n').encode())
        log.flush()
        result = subprocess.run(command, cwd=repo, stdout=log, stderr=subprocess.STDOUT)
    (out / (name + '.rc')).write_text(str(result.returncode) + '\n')
    return name, result.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, commands.items()))
for name, code in results:
    print(name, code)
sys.exit(any(code for _, code in results))
