"""Materialize committed archives, including pinned inputs, without checkout."""
import io
from pathlib import Path
import subprocess
import tarfile
import sys

source = Path('$LANES/573-builder-refusals')
revision, label = sys.argv[1:]
dest = Path('/tmp/573-a352') / label
dest.mkdir()

def archive(repo, rev, target):
    blob = subprocess.check_output(['git', '-C', str(repo), 'archive', rev])
    with tarfile.open(fileobj=io.BytesIO(blob)) as tar:
        tar.extractall(target, filter='data')

head = subprocess.check_output(['git', '-C', str(source), 'rev-parse', revision], text=True).strip()
archive(source, head, dest)
for path in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis'):
    line = subprocess.check_output(['git', '-C', str(source), 'ls-tree', head, path], text=True)
    pin = line.split()[2]
    archive(source/path, pin, dest/path)
# Reviewer scripts query tracked filenames and HEAD. Supply read-only source
# objects and a disposable index; no checkout or worktree operation is used.
subprocess.run(['git', 'init', '-q', str(dest)], check=True)
objects = subprocess.check_output(['git', '-C', str(source), 'rev-parse',
                                   '--path-format=absolute', '--git-path', 'objects'], text=True).strip()
(dest/'.git/objects/info/alternates').write_text(objects+'\n')
subprocess.run(['git', '-C', str(dest), 'update-ref', 'HEAD', head], check=True)
subprocess.run(['git', '-C', str(dest), 'read-tree', head], check=True)
print(head, dest)
