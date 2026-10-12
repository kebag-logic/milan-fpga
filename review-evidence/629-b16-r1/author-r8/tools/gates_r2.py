"""Round 2 documentation gates on the committed head, with the hosted-parity tools.

Markdown gates run under the Markdown venv (the renderer pins). Every other
`python3` resolves to CPython 3.12.3 through a shim directory placed first on
PATH; pyyaml, which the hosted job installs, is made importable by a path entry
that exposes only the system's pure-Python yaml package. make is GNU make 4.3
under MAKEFLAGS=w. Each gate's output goes to its own log; nothing is piped.
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
SHIM = Path(sys.argv[3])
BASE = sys.argv[4]
OUT.mkdir(parents=True, exist_ok=True)
MD = '$VALIDATION_TOOLS/md-venv/bin/python'
MAKE = '$VALIDATION_STORAGE/641-a573/make-4.3/make'
ENV = dict(os.environ, PATH=f'{SHIM}/bin:' + os.environ['PATH'], PYTHONPATH=f'{SHIM}/yaml',
           PYTHONDONTWRITEBYTECODE='1', MAKEFLAGS='w', TMPDIR=str(SHIM / 'tmp'))
(SHIM / 'tmp').mkdir(exist_ok=True)
MD_ENV = dict(ENV)
MD_ENV.pop('PYTHONPATH')
GATES = [
    ('tool-python3', ['python3', '--version'], {}),
    ('tool-md', [MD, '--version'], {'md': True}),
    ('tool-make', [MAKE, '--version'], {}),
    ('docs-check', [MD, 'scripts/docs_check.py'], {'md': True}),
    ('docs-check-no-git', [MD, 'scripts/docs_check.py'], {'md': True, 'env': {'GIT_DIR': '/dev/null'}}),
    ('feature-status-no-git', [MD, 'scripts/check_feature_status.py'], {'md': True, 'env': {'GIT_DIR': '/dev/null'}}),
    ('feature-status-selftest', [MD, 'scripts/check_feature_status.py', '--self-test'], {'md': True}),
    ('em-dash', [MD, 'scripts/check_em_dash.py', '--base', BASE], {'md': True}),
    ('em-dash-selftest', [MD, 'scripts/check_em_dash.py', '--selftest'], {'md': True}),
    ('doc-style', [MD, 'scripts/check_doc_style.py'], {'md': True}),
    ('doc-style-selftest', [MD, 'scripts/check_doc_style.py', '--selftest'], {'md': True}),
    ('gptp-docs', [MD, 'scripts/check_gptp_docs.py'], {'md': True}),
    ('gptp-docs-selftest', [MD, 'scripts/check_gptp_docs.py', '--selftest'], {'md': True}),
    ('gptp-docs-with-submodule', [MD, 'scripts/check_gptp_docs.py', '--with-submodule'], {'md': True}),
    ('doc-paths', [MD, 'scripts/check_doc_paths.py'], {'md': True}),
    ('toc-selftest', [MD, 'scripts/gen_toc.py', '--selftest'], {'md': True}),
    ('toc-verify-anchors', [MD, 'scripts/gen_toc.py', '--verify-anchors'], {'md': True}),
    ('toc-check', [MD, 'scripts/gen_toc.py', '--check'], {'md': True}),
    ('archive', [MD, 'scripts/check_archive.py'], {'md': True}),
    ('archive-selftest', [MD, 'scripts/check_archive.py', '--selftest'], {'md': True}),
    ('doc-map-check', [MD, 'docs/DOC_MAP.gen.py', '--check'], {'md': True}),
    ('doc-map-selftest', [MD, 'docs/DOC_MAP.gen.py', '--selftest'], {'md': True}),
    ('timesync-chain-check', [MD, 'docs/diagrams/timesync_chain.gen.py', '--check'], {'md': True}),
    ('timesync-chain-selftest', [MD, 'docs/diagrams/timesync_chain.gen.py', '--selftest'], {'md': True}),
    ('module-matrix-check', [MD, 'docs/traceability/gen_module_matrix.py', '--check'], {'md': True}),
    ('solution-docs', [MD, 'scripts/check_solution_docs.py'], {'md': True}),
    ('solution-docs-selftest', [MD, 'scripts/check_solution_docs.py', '--selftest'], {'md': True}),
    ('submodule-boundaries-check', ['python3', 'docs/diagrams/submodule_boundaries.gen.py', '--check'], {}),
    ('submodule-docs', ['python3', 'scripts/check_submodule_docs.py'], {}),
    ('baremetal-only-check', ['python3', 'scripts/check_baremetal_only.py', '--check'], {}),
    ('baremetal-only-selftest', ['python3', 'scripts/check_baremetal_only.py', '--selftest'], {}),
    ('gptp-docs-make', [MAKE, '-C', 'gptp-processor', 'docs'], {}),
    ('ci-scope-selftest', ['python3', 'scripts/ci_scope.py', '--selftest'], {}),
    ('ci-events-check', ['python3', 'scripts/ci_events.py', '--check'], {}),
    ('git-diff-check-worktree', ['git', 'diff', '--check'], {}),
    ('git-diff-check-range', ['git', 'diff', '--check', BASE, 'HEAD'], {}),
]
rows = []
for name, argv, opts in GATES:
    start = time.time()
    env = dict(MD_ENV if opts.get('md') else ENV, **opts.get('env', {}))
    with (OUT / (name + '.log')).open('w') as log:
        run = subprocess.run(argv, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
    rows.append(dict(name=name, command=argv, rc=run.returncode, seconds=round(time.time() - start, 2)))
    print(name, run.returncode, flush=True)
(OUT / 'results.json').write_text(json.dumps(rows, indent=2) + '\n')
rc = int(any(r['rc'] for r in rows))
(OUT / 'rc').write_text(f'{rc}\n')
raise SystemExit(rc)
