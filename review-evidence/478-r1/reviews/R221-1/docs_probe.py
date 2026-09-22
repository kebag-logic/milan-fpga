"""R221 reproduce docs gate with and without the pinned submodule files."""
from pathlib import Path
import io
import json
import os
import subprocess
import sys
import tarfile

src = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
scratch = out / 'scratch'
receipts = out / 'receipts/docs-probe'
receipts.mkdir(parents=True, exist_ok=True)
head = 'd81a302760b84f32d2aa019643f57682bb6e052c'
base = 'ec34fcdee0ca9ffa63564a9af8ad70a3a618de29'
env = {**os.environ, 'GIT_NO_REPLACE_OBJECTS': '1', 'GIT_OPTIONAL_LOCKS': '0',
       'PYTHONDONTWRITEBYTECODE': '1'}


def command(args, cwd=src):
    return subprocess.check_output(['rtk', 'proxy', *args], cwd=cwd, env=env)


def export(ref, destination, source=src):
    destination.mkdir(parents=True, exist_ok=True)
    data = command(['git', 'archive', ref], source)
    with tarfile.open(fileobj=io.BytesIO(data)) as tar:
        tar.extractall(destination, filter='data')


gitroot = scratch / 'docs-git'
if not gitroot.exists():
    command(['git', 'clone', '--quiet', '--no-hardlinks', '--no-checkout', str(src), str(gitroot)])
    command(['git', 'checkout', '--quiet', '--detach', head], gitroot)
assert command(['git', 'rev-parse', 'HEAD'], gitroot).decode().strip() == head
nogit = scratch / 'docs-nogit'
old = scratch / 'docs-integrated-base-nogit'
export(head, nogit)
export(base, old)
target = 'protocol-processor/docs/architecture/07_memory_maps.md'
assert all(not (p / target).exists() for p in (gitroot, nogit, old))
rows = []


def gate(label, root, expected):
    args = ['rtk', 'proxy', 'python3', '-B', 'scripts/docs_check.py']
    result = subprocess.run(args, cwd=root, env=env, capture_output=True, text=True)
    output = result.stdout + result.stderr
    (receipts / (label + '.log')).write_text(output)
    assert result.returncode == expected, (label, result.returncode, output)
    if expected:
        assert 'docs/ENDSTATION_BUILDER.md:963' in output
        assert '../protocol-processor/docs/architecture/07_memory_maps.md' in output
    rows.append({'label': label, 'command': args, 'cwd': str(root),
                 'exit_code': result.returncode, 'expected_exit_code': expected,
                 'log': label + '.log'})
    print(label, 'exit', result.returncode)
    print(output)


gate('current-git-no-submodules', gitroot, 1)
gate('current-no-git-no-submodules', nogit, 1)
gate('integrated-base-no-git-no-submodules', old, 0)
for dst in (gitroot, nogit):
    export('424c688fa2205b934a7689a58f2aa766420f2326', dst / 'protocol-processor', src / 'protocol-processor')
gate('current-git-processor-populated', gitroot, 0)
gate('current-no-git-processor-populated', nogit, 0)
(receipts / 'results.json').write_text(json.dumps({'head': head, 'base': base,
    'target': target, 'results': rows,
    'conclusion': 'The added relative link causes the failure in both supported no-submodule documentation jobs; populating the pinned processor masks it.'}, indent=2) + '\n')
