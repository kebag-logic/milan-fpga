import json
import os
import shlex
import subprocess
import tarfile
import time
from pathlib import Path

ROOT = Path('$LANES/508-pp-pin-adopt')
OUT = Path(__file__).resolve().parent
RECEIPTS = OUT / 'round4-final'
RECEIPTS.mkdir(exist_ok=True)
HEAD = '9d66cfe0dc87ffe4a5f45691d5c86b041b050b38'
BASE = 'c266432dcb0cdd464205823a3d82cad260eedde2'
START = '224ec0e9a9fa129924bf8f0433cf70b4140f7bd2'
ENV = os.environ.copy()
ENV.pop('GIT_DIR', None)
ENV.pop('GIT_WORK_TREE', None)
ENV['PYTHONPATH'] = str(OUT / 'markdown-deps')
ENV['PYTHONDONTWRITEBYTECODE'] = '1'
LEDGER = RECEIPTS / 'gates.jsonl'
if LEDGER.exists():
    raise SystemExit('Refusing to overwrite existing final-head receipts')

def run(label, args, cwd=ROOT, extra_env=None):
    env = ENV | (extra_env or {})
    started = time.monotonic()
    print(f'START {label}: {shlex.join(args)}', flush=True)
    log_path = RECEIPTS / f'{label}.log'
    with log_path.open('w') as log:
        result = subprocess.run(['rtk', 'proxy', *args], cwd=cwd, env=env,
                                stdout=log, stderr=subprocess.STDOUT,
                                timeout=1200, check=False)
    row = dict(label=label, head=HEAD, argv=args,
               cwd='archive' if cwd != ROOT else 'lane',
               env={k: ('<lane-git-dir>' if k == 'GIT_DIR' and v.startswith('/data/')
                        else '<archive>' if k == 'GIT_WORK_TREE' else v)
                    for k, v in (extra_env or {}).items()},
               rc=result.returncode, seconds=round(time.monotonic()-started, 3),
               log=log_path.name)
    with LEDGER.open('a') as ledger:
        ledger.write(json.dumps(row) + '\n')
    print(f'END {label}: rc {result.returncode}, {row["seconds"]} s', flush=True)
    print(log_path.read_text()[-1800:], flush=True)
    if result.returncode:
        raise SystemExit(result.returncode)
    return log_path.read_text().strip()

actual_head = run('head', ['git', 'rev-parse', 'HEAD'])
assert actual_head == HEAD
assert not run('status', ['git', 'status', '--porcelain'])
for label, args in [
    ('verify-anchors', ['python3', 'scripts/gen_toc.py', '--verify-anchors']),
    ('toc-check', ['python3', 'scripts/gen_toc.py', '--check']),
    ('docs-git', ['python3', 'scripts/docs_check.py']),
    ('doc-paths', ['python3', 'scripts/check_doc_paths.py']),
    ('em-dash', ['python3', 'scripts/check_em_dash.py', '--base', BASE]),
    ('test-evidence-check', ['python3', 'scripts/measure_test_evidence.py', '--check']),
    ('test-evidence-selftest', ['python3', 'scripts/measure_test_evidence.py', '--selftest']),
    ('python-idiom', ['python3', 'scripts/check_py_idiom.py']),
    ('diff-check', ['git', 'diff', '--check']),
    ('committed-diff-check', ['git', 'diff', '--check', START, HEAD]),
]:
    run(label, args)
run('docs-no-git', ['python3', 'scripts/docs_check.py'],
    extra_env={'GIT_DIR': '/nonexistent-508-a299-git'})

archive_tar = RECEIPTS / 'head.tar'
archive = RECEIPTS / 'archive'
assert not archive.exists()
run('archive-create', ['git', 'archive', '--format=tar',
                       '--output=' + str(archive_tar), HEAD])
archive.mkdir()
with tarfile.open(archive_tar) as source:
    source.extractall(archive, filter='data')
gitlinks = run('gitlinks', ['git', 'ls-files', '--stage'])
submodules = [line.split('\t', 1)[1] for line in gitlinks.splitlines()
              if line.startswith('160000 ')]
assert submodules
for name in submodules:
    path = archive / name
    assert not path.exists() or (path.is_dir() and not list(path.iterdir())), name
assert not (archive / '.git').exists()
(RECEIPTS / 'archive-shape.json').write_text(json.dumps({
    'head': HEAD, 'git_metadata_present': False,
    'empty_or_absent_submodules': submodules,
}, indent=2) + '\n')
run('archive-docs-no-git', ['python3', 'scripts/docs_check.py'], cwd=archive)
git_dir = run('git-dir', ['git', 'rev-parse', '--absolute-git-dir'])
run('archive-docs-git', ['python3', 'scripts/docs_check.py'], cwd=archive,
    extra_env={'GIT_DIR': git_dir, 'GIT_WORK_TREE': str(archive)})
assert not run('final-status', ['git', 'status', '--porcelain'])
assert run('final-head', ['git', 'rev-parse', 'HEAD']) == HEAD
print('All requested round-4 gates passed at the committed head.', flush=True)
