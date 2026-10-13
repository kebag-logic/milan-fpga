#!/usr/bin/env python3
"""Run focused documentation/resource/shard gates without builder banks."""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys
source, packet = map(lambda s: Path(s).resolve(), sys.argv[1:3])
python = packet / 'scratch/docs-env/bin/python3'
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(packet/'scratch'))
tasks = [
 ('docs-check', 'scripts/docs_check.py'),
 ('doc-style', 'scripts/check_doc_style.py'),
 ('doc-style-selftest', 'scripts/check_doc_style.py', '--selftest'),
 ('feature-status', 'scripts/check_feature_status.py', '--self-test'),
 ('solution-docs', 'scripts/check_solution_docs.py'),
 ('solution-docs-selftest', 'scripts/check_solution_docs.py', '--selftest'),
 ('gptp-docs', 'scripts/check_gptp_docs.py', '--with-submodule'),
 ('gptp-docs-selftest', 'scripts/check_gptp_docs.py', '--selftest'),
 ('submodule-docs', 'scripts/check_submodule_docs.py'),
 ('submodule-docs-selftest', 'scripts/check_submodule_docs.py', '--selftest'),
 ('module-matrix', 'docs/traceability/gen_module_matrix.py', '--check'),
 ('toc-check', 'scripts/gen_toc.py', '--check'),
 ('toc-anchors', 'scripts/gen_toc.py', '--verify-anchors'),
 ('em-dash-requested-base', 'scripts/check_em_dash.py', '--base', 'c6bd08c6f52632c6d33d834ce842ac3cf63f29cc'),
 ('em-dash-imported-base', 'scripts/check_em_dash.py', '--base', 'e81ce82f9aa3e4dcaffa5bcdf7e60f0c7cffd80c'),
 ('resource-baseline', 'syn/ooc/pp_resource_gate.py', 'check-baseline'),
 ('suite-shards', 'scripts/suite_shards.py', '--selftest'),
]
def run(item):
    name, *args = item
    cmd = [str(python), *args]
    result = subprocess.run(cmd, cwd=source, env=env, capture_output=True, text=True)
    text = 'COMMAND: python3 ' + ' '.join(args) + '\n' + result.stdout + result.stderr
    text += f'\nEXIT_STATUS={result.returncode}\n'
    text = text.replace(str(source), '<source>').replace(str(packet), '<packet>')
    (packet / 'receipts' / (name+'.log')).write_text(text)
    (packet / 'receipts' / (name+'.rc')).write_text(str(result.returncode)+'\n')
    print(name, result.returncode, flush=True)
    return result.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results=list(pool.map(run, tasks))
raise SystemExit(int(any(results)))
