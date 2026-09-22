#!/usr/bin/env python3
"""Verify final tracked bytes, modes, index, flags, and detached identity."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

ROOT = Path('$VALIDATION_STORAGE/reviews/r219-505-r3')
OUT = Path(__file__).resolve().parent

def git(*args):
    return subprocess.check_output(['rtk', 'proxy', 'git', '--no-replace-objects',
                                    *args], cwd=ROOT)

assert git('rev-parse', 'HEAD').decode().strip() == '5d45ecc0cf2dc572d538cbc534b5d9f95c8688e7'
index = git('ls-files', '--stage')
assert index == (OUT / 'initial-index.txt').read_bytes()
assert git('ls-tree', '-r', 'HEAD') == (OUT / 'initial-tree.txt').read_bytes()
assert not git('diff', '--raw', 'HEAD')
status = git('status', '--porcelain=v2', '--untracked-files=all', '--ignored').decode()
assert not status, status
flags = git('ls-files', '-v').decode()
assert all(line.startswith('H ') for line in flags.splitlines()), flags
entries = []
for row in git('ls-files', '--stage', '-z').split(b'\0'):
    if not row:
        continue
    meta, name = row.split(b'\t', 1)
    mode, oid, stage = meta.decode().split()
    assert stage == '0'
    path = ROOT / os.fsdecode(name)
    if mode == '160000':
        continue
    info = path.lstat()
    if mode == '120000':
        assert stat.S_ISLNK(info.st_mode)
        data = os.fsencode(os.readlink(path))
    else:
        assert stat.S_ISREG(info.st_mode), path
        actual_mode = '100755' if info.st_mode & 0o111 else '100644'
        assert actual_mode == mode, (path, mode, actual_mode)
        data = path.read_bytes()
    actual_oid = hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()
    assert actual_oid == oid, (path, oid, actual_oid)
    entries.append({'path': os.fsdecode(name), 'mode': mode, 'blob': oid})
submodules = git('submodule', 'status').decode()
assert len(submodules.splitlines()) == 4
assert all(line.startswith('-') for line in submodules.splitlines())
result = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'head': git('rev-parse', 'HEAD').decode().strip(),
          'tree': git('rev-parse', 'HEAD^{tree}').decode().strip(),
          'status_including_untracked_ignored': status,
          'index_equals_initial': True, 'head_tree_equals_initial': True,
          'tracked_non_gitlinks_hashed': len(entries),
          'mode_mismatches': 0, 'content_mismatches': 0,
          'index_sha256': hashlib.sha256(index).hexdigest(),
          'all_index_flags_H': True, 'submodules': submodules,
          'entries': entries}
(OUT / 'final-integrity.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({key: value for key, value in result.items() if key != 'entries'}, indent=2))
