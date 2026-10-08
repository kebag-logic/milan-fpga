"""Fresh source exports of one lane commit for the round-2e gates.

  python3 -B make_exports.py COMMIT NAME...
Each NAME becomes round2e/functional/NAME: `git archive` of COMMIT plus each
initialised gitlink at its pinned commit, and a minimal .git (objects through
alternates into the lane, detached HEAD, index read from the tree) so tools
that ask git about tracked files work. No checkout, no lane switch. Each
dependency's repository root is verified before any git command inside it.
"""
import json
import subprocess
import sys
from pathlib import Path

lane = Path('$REPO')
w = Path(__file__).resolve().parent / 'functional'
commit = subprocess.check_output(['git', '-C', str(lane), 'rev-parse', sys.argv[1]], text=True).strip()


def git(*args, cwd=lane, text=True):
    return subprocess.check_output(['git', '-C', str(cwd), *args], text=text)


def archive(repo: Path, rev: str, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    tar = subprocess.Popen(['git', '-C', str(repo), 'archive', '--format=tar', rev], stdout=subprocess.PIPE)
    subprocess.run(['tar', '-x', '-C', str(dest)], stdin=tar.stdout, check=True)
    assert tar.wait() == 0


def metadata(dest: Path, objects: Path, rev: str) -> None:
    subprocess.run(['git', 'init', '-q', str(dest)], check=True)
    assert Path(git('rev-parse', '--show-toplevel', cwd=dest).strip()).resolve() == dest.resolve()
    (dest / '.git/objects/info/alternates').write_text(str(objects) + '\n')
    git('update-ref', '--no-deref', 'HEAD', rev, cwd=dest)
    git('read-tree', 'HEAD', cwd=dest)
    subprocess.run(['git', '-C', str(dest), 'update-index', '-q', '--refresh'], check=False)


report_path = w / ('exports-' + commit[:8] + '.json')
report = json.loads(report_path.read_text()) if report_path.exists() else {'commit': commit, 'exports': {}}
gitlinks = [line.split(None, 3) for line in git('ls-tree', '-r', commit).splitlines() if line.startswith('160000 ')]
for name in sys.argv[2:]:
    dest = w / name
    assert not dest.exists(), dest
    archive(lane, commit, dest)
    metadata(dest, lane / '.git/objects', commit)
    deps = []
    for _, _, sha, path in gitlinks:
        sub = lane / path
        top = subprocess.run(['git', '-C', str(sub), 'rev-parse', '--show-toplevel'],
                             capture_output=True, text=True).stdout.strip()
        if not top or Path(top).resolve() != sub.resolve():
            (dest / path).mkdir(parents=True, exist_ok=True)
            deps.append(dict(path=path, gitlink=sha, initialised=False))
            continue
        archive(sub, sha, dest / path)
        objects = Path(git('rev-parse', '--git-common-dir', cwd=sub).strip())
        if not objects.is_absolute():
            objects = (sub / objects).resolve()
        metadata(dest / path, objects / 'objects', sha)
        deps.append(dict(path=path, gitlink=sha, initialised=True, root_verified=True))
    status = git('status', '--porcelain', '--ignore-submodules=none', cwd=dest)
    report['exports'][name] = dict(dependencies=deps, status=status)
    print(name, 'status clean' if not status else 'STATUS:\n' + status, flush=True)
(w / ('exports-' + commit[:8] + '.json')).write_text(json.dumps(report, indent=2) + '\n')
raise SystemExit(int(any(e['status'] for e in report['exports'].values())))
