from pathlib import Path
import hashlib
import json
import os
import stat
import subprocess

lane = Path('$LANES/502-pending-live-write')
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=lane, text=True).strip()
assert head == '5d4cf33e3709c35d4f5bc90d3c5a2334ef3bfd8e'
projects = [('', head),
            ('protocol-processor', '870ff88ad35bbd532244e4c7e6d7661b9f6e1366'),
            ('gptp-processor', '5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d'),
            ('third_party/verilog-axis', '48ff7a7e2ef782cf778d47910cf85835c64b1bce')]
results = []
for relative, revision in projects:
    repo = lane / relative
    actual = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo, text=True).strip()
    assert actual == revision
    count = 0
    for entry in subprocess.check_output(['git', 'ls-tree', '-rz', revision], cwd=repo).split(b'\0'):
        if not entry:
            continue
        metadata, name = entry.split(b'\t', 1)
        mode, kind, oid = metadata.split()
        if kind != b'blob':
            continue
        path = repo / os.fsdecode(name)
        if mode == b'120000':
            assert path.is_symlink(), str(path)
            data = os.fsencode(os.readlink(path))
        else:
            assert not path.is_symlink() and path.is_file(), str(path)
            assert bool(path.stat().st_mode & stat.S_IXUSR) == (mode == b'100755'), str(path)
            data = path.read_bytes()
        assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == oid.decode(), str(path)
        count += 1
    results.append({'project': relative, 'revision': revision, 'verified_blobs': count})
assert not subprocess.check_output(['git', 'status', '--porcelain'], cwd=lane)
assert subprocess.check_output(['git', 'show', '-s', '--format=%B', 'HEAD'], cwd=lane, text=True).strip() == 'fix(nvm): preserve map write priority with minimal predicates'
assert subprocess.check_output(['git', 'rev-list', '--count', '220c9d56..HEAD'], cwd=lane, text=True).strip() == '1'
print(json.dumps({'head': head, 'projects': results, 'clean_tree': True, 'one_resume_commit': True, 'single_subject_no_body_or_trailers': True}, indent=2))
