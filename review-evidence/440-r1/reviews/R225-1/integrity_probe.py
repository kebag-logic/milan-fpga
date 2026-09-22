"""Final tracked-byte, index and detached-head integrity, without product writes."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

OUT = Path(__file__).resolve().parent
REPO = Path('$VALIDATION_STORAGE/reviews/r225-507-r1')
def run(*args):
    p = subprocess.run(['git', '-C', str(REPO), *args], capture_output=True, text=True)
    return dict(command=['git', *args], exit=p.returncode, stdout=p.stdout, stderr=p.stderr)

initial = json.loads((OUT / 'initial-integrity.json').read_text())
index = run('ls-files', '-s')
old_index = next(r['stdout'] for r in initial if r['command'] == ['git', 'ls-files', '-s'])
files = []
submodules = []
for line in index['stdout'].splitlines():
    meta, rel = line.split('\t', 1)
    mode, oid, stage = meta.split()
    path = REPO / rel
    if mode == '160000':
        submodules.append(dict(path=rel, pin=oid, exists=path.exists(),
                               empty_directory=path.is_dir() and not any(path.iterdir())))
        continue
    if not path.exists() and not path.is_symlink():
        files.append(dict(path=rel, error='missing'))
        continue
    data = os.fsencode(os.readlink(path)) if path.is_symlink() else path.read_bytes()
    actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    actual_mode = '120000' if path.is_symlink() else ('100755' if path.stat().st_mode & stat.S_IXUSR else '100644')
    files.append(dict(path=rel, blob_matches=actual == oid, mode_matches=actual_mode == mode,
                      sha256=hashlib.sha256(data).hexdigest()))
result = dict(head=run('rev-parse', 'HEAD'), symbolic_head=run('symbolic-ref', '-q', 'HEAD'),
              tree=run('rev-parse', 'HEAD^{tree}'), status=run('status', '--porcelain=v1'),
              worktree_diff=run('diff', '--raw'), index_diff=run('diff', '--cached', '--raw'),
              index_entries_identical=index['stdout'] == old_index,
              index_entries_sha256=hashlib.sha256(index['stdout'].encode()).hexdigest(),
              submodule_status=run('submodule', 'status'), submodules=submodules,
              tracked_files_verified=len(files),
              bad_files=[r for r in files if not r.get('blob_matches') or not r.get('mode_matches')])
(OUT / 'tracked-sha256.json').write_text(json.dumps(files, indent=2) + '\n')
(OUT / 'final-integrity.json').write_text(json.dumps(result, indent=2) + '\n')
assert result['head']['stdout'].strip() == '0d43ff25d38917e77bb5c3d2ddb6473013cea3ba'
assert result['symbolic_head']['exit'] == 1
assert result['index_entries_identical'] and not result['bad_files']
assert result['status']['stdout'] == result['worktree_diff']['stdout'] == result['index_diff']['stdout'] == ''
print(json.dumps(result, indent=2))
