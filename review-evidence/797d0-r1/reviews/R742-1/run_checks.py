#!/usr/bin/env python3
"""Run focused read-only documentation checks, with bounded parallelism."""
import concurrent.futures
import os
from pathlib import Path
import shlex
import subprocess
import sys
import time

root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
scratch = out / 'scratch'
scratch.mkdir(exist_ok=True)
logs = out / 'checks'
logs.mkdir(exist_ok=True)
commands = []
for script, args in [
    ('docs_check', ['']), ('check_em_dash', ['--base 1e80128f', '--selftest']),
    ('check_doc_style', ['', '--selftest']), ('check_doc_paths', ['']),
    ('check_gptp_docs', ['', '--selftest', '--with-submodule']),
    ('check_solution_docs', ['', '--selftest']), ('check_submodule_docs', ['', '--selftest']),
    ('check_diagram_pngs', ['', '--selftest']), ('check_feature_status', ['--self-test']),
    ('check_baremetal_only', ['--check', '--selftest']),
    ('check_archive', ['', '--selftest']), ('gen_toc', ['--selftest', '--verify-anchors', '--check']),
    ('docs_inventory', ['--check', '--selftest']), ('ci_gate_workflows', ['--check']),
    ('ci_events', ['--check', '--selftest']),
    ('check_py_idiom', ['', '--selftest']), ('check_sh_idiom', ['', '--selftest']),
    ('check_hygiene', ['--check', '--selftest']),
    ('check_todo_ownership', ['', '--selftest']),
]:
    commands.extend(['python3', f'scripts/{script}.py', *shlex.split(a)] for a in args)
for name in ['docs/DOC_MAP.gen.py', 'docs/diagrams/timesync_chain.gen.py',
             'docs/diagrams/submodule_boundaries.gen.py']:
    commands.extend(['python3', name, a] for a in ['--check', '--selftest'])
commands.append(['python3', 'docs/traceability/gen_module_matrix.py', '--check'])
commands.append(['bash', 'scripts/run_litex_sims.sh', '--list'])
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1')
env['PATH'] = str(Path(sys.executable).parent) + os.pathsep + env['PATH']

def run(item):
    i, cmd = item
    start = time.monotonic()
    p = subprocess.run(cmd, cwd=root, env=env, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, text=True, timeout=540)
    body = '$ ' + shlex.join(cmd) + '\n' + p.stdout
    body = body.replace(str(root), '<checkout>').replace(str(out), '<packet>')
    body = body.replace(str(Path.home()), '<home>')
    (logs / f'{i:03}.log').write_text(body)
    (logs / f'{i:03}.rc').write_text(str(p.returncode) + '\n')
    return i, p.returncode, round(time.monotonic() - start, 2), shlex.join(cmd)

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    results = sorted(pool.map(run, enumerate(commands, 1)))
(out / 'checks.tsv').write_text('id\trc\tseconds\tcommand\n' + ''.join(
    '\t'.join(map(str, row)) + '\n' for row in results))
print(f'{len(results)} focused checks; {sum(r[1] != 0 for r in results)} nonzero exits')
for row in results:
    if row[1]:
        print(row)
