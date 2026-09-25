from pathlib import Path
import subprocess

ROOT = Path('$LANES/400-403-declaration-truth')
START = '7463ab0889da9a95fce7c921e386d6035d69778e'
HEAD = 'e122f3302cf8a8e89de960233a8638b9dd1387dc'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


assert git('rev-parse', 'HEAD') == HEAD
assert git('branch', '--show-current') == '400-403-declaration-truth'
assert git('remote', 'get-url', 'origin') == 'https://github.com/kebag-logic/milan-fpga.git'
assert not git('status', '--porcelain')
for line in git('submodule', 'status', '--recursive').splitlines():
    assert not line.startswith(('-', '+', 'U'))
commits = git('rev-list', START + '..HEAD').splitlines()
assert len(commits) == 2
for commit in commits:
    body = git('show', '-s', '--format=%B', commit)
    assert len(body.splitlines()) == 1
assert not Path('/tmp/declaration-review-y7zd9geg').exists()
print('Head, branch, origin, clean checkout, pinned submodules, commit subjects and scratch removal verified.')
