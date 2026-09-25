"""Run assigned gates sequentially in the foreground, preserving exit codes.

Set MILAN_SOURCE and MILAN_GATE_ENV to the candidate and gate environment.
Tree exports are temporary directories under /tmp, never receipt artifacts.
"""
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile
import time

SOURCE = Path(os.environ['MILAN_SOURCE']).resolve()
OUT = Path(__file__).resolve().parent.parent
ENV = dict(os.environ)
ENV['PATH'] = os.environ['MILAN_GATE_ENV'] + '/bin:' + ENV['PATH']
ENV['PYTHONDONTWRITEBYTECODE'] = '1'
RESULTS = []


def run(name, command, cwd=SOURCE, expected_rc=0, require_empty=False):
    log = OUT / 'receipts' / f'{name}.log'
    start = time.monotonic()
    print(f'RUN {name}: {" ".join(command)}', flush=True)
    with log.open('w') as stream:
        result = subprocess.run(['rtk', 'proxy', *command], cwd=cwd, env=ENV,
                                stdout=stream, stderr=subprocess.STDOUT,
                                timeout=1800)
    ok = result.returncode == expected_rc
    if require_empty:
        ok = ok and log.stat().st_size == 0
    RESULTS.append(dict(name=name, command=command, cwd=str(cwd),
                        rc=result.returncode, expected_rc=expected_rc,
                        pass_gate=ok, seconds=round(time.monotonic() - start, 2),
                        log=f'receipts/{name}.log'))
    (OUT / 'gate-results.json').write_text(json.dumps(RESULTS, indent=2) + '\n')
    print(f'{"PASS" if ok else "FAIL"} {name}: rc={result.returncode} '
          f'(expected {expected_rc}), {RESULTS[-1]["seconds"]}s', flush=True)
    if not ok:
        print(log.read_text(), flush=True)
        raise SystemExit(1)


run('behave', ['behave', '--no-capture', '-f', 'plain'], SOURCE / 'tests')
run('bdd-mutants', ['python3', 'scripts/bdd_mutants.py'], OUT)
run('obsolete-wording', ['grep', '-rnE', 'Residual|pending fix|previous slope',
                        'tests/'], expected_rc=1, require_empty=True)
print('PASS absence assertion: rc=0 (grep returned 1, no matches).', flush=True)
run('docs-git', ['python3', '-B', 'scripts/docs_check.py'])
with tempfile.TemporaryDirectory(prefix='milan-551-docs-', dir='/tmp') as name:
    scratch = Path(name)
    archive = scratch / 'candidate.tar'
    with archive.open('wb') as stream:
        subprocess.run(['rtk', 'proxy', 'git', 'archive', '--format=tar', 'HEAD'],
                       cwd=SOURCE, stdout=stream, check=True, timeout=300)
    tree = scratch / 'tree'
    tree.mkdir()
    with tarfile.open(archive) as stream:
        stream.extractall(tree, filter='data')
    assert not (tree / '.git').exists()
    run('docs-no-git', ['python3', '-B', 'scripts/docs_check.py'], tree)
run('em-dash', ['python3', 'scripts/check_em_dash.py', '--base',
                '864b36f5e9450ef64f75ca3f0d68c44330e447d7'])
run('doc-style', ['python3', 'scripts/check_doc_style.py'])
run('toc-check', ['python3', 'scripts/gen_toc.py', '--check'])
run('toc-anchors', ['python3', 'scripts/gen_toc.py', '--verify-anchors'])
run('doc-paths', ['python3', 'scripts/check_doc_paths.py'])
run('test-evidence', ['python3', 'scripts/measure_test_evidence.py', '--check'])
run('diff-check', ['git', 'diff', '--check'])
run('commit-diff-check', ['git', 'diff', '--check', 'HEAD^', 'HEAD'])
print('PASS: all assigned gates satisfied.', flush=True)
