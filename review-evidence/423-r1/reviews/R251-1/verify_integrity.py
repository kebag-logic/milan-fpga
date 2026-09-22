#!/usr/bin/env python3
"""Read-only exact-pin and tracked-byte verification, ignoring index shortcuts."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

OUT = Path(__file__).resolve().parent
SOURCE = Path('$VALIDATION_STORAGE/reviews/r251-423-locale-retry')
HEAD = 'df53dfa116b34816db0193230ad9833e67bf46dd'
REQUIRED = ('third_party/verilog-axis', 'protocol-processor', 'gptp-processor')
records = []
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1', GIT_OPTIONAL_LOCKS='0')


def git(repo, *args):
    command = ['rtk', 'proxy', 'git', '--no-replace-objects', '-C', str(repo), *args]
    result = subprocess.run(command, env=env, capture_output=True)
    records.append({'argv': command, 'returncode': result.returncode,
                    'stdout_hex': result.stdout.hex(), 'stderr_hex': result.stderr.hex()})
    result.check_returncode()
    return result.stdout


def verify(repo, expected):
    actual = git(repo, 'rev-parse', 'HEAD').decode().strip()
    status = git(repo, 'status', '--porcelain=v1', '--untracked-files=all')
    entries = git(repo, 'ls-tree', '-rz', '--full-tree', expected)
    mismatches, gitlinks, checked = [], {}, 0
    for record in entries.split(b'\0'):
        if not record:
            continue
        header, relative = record.split(b'\t', 1)
        mode, kind, oid = header.split()
        if kind == b'commit':
            gitlinks[os.fsdecode(relative)] = oid.decode('ascii')
            continue
        path = os.fsencode(repo) + b'/' + relative
        try:
            metadata = os.lstat(path)
            if mode == b'120000':
                assert stat.S_ISLNK(metadata.st_mode), 'expected symlink'
                data = os.readlink(path)
            else:
                assert stat.S_ISREG(metadata.st_mode), 'expected regular file'
                assert bool(metadata.st_mode & 0o111) == (mode == b'100755'), 'executable mode differs'
                with open(path, 'rb') as stream:
                    data = stream.read()
            digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            assert digest == oid.decode(), 'blob bytes differ'
            checked += 1
        except (OSError, AssertionError) as exc:
            mismatches.append({'path': os.fsdecode(relative), 'error': str(exc)})
    result = {'repository': str(repo), 'expected': expected, 'actual': actual,
              'status_hex': status.hex(), 'tracked_files_verified': checked,
              'mismatches': mismatches, 'gitlinks': gitlinks,
              'pass': actual == expected and not status and not mismatches}
    return result


root = verify(SOURCE, HEAD)
results = [root]
for name in REQUIRED:
    repo = SOURCE / name
    row = verify(repo, root['gitlinks'][name])
    row['registered_superproject'] = git(repo, 'rev-parse', '--show-superproject-working-tree').decode().strip()
    row['path_is_symlink'] = repo.is_symlink()
    row['pass'] = row['pass'] and row['registered_superproject'] == str(SOURCE) and not row['path_is_symlink']
    results.append(row)
git(SOURCE, 'submodule', 'status', '--recursive')
locale = subprocess.run(['rtk', 'proxy', 'locale', '-a'], capture_output=True)
(OUT / 'receipts/final-installed-locales.txt').write_bytes(locale.stdout)
report = {'head': HEAD, 'results': results, 'git_commands': records,
          'pass': all(row['pass'] for row in results)}
(OUT / 'receipts/final-integrity.json').write_text(json.dumps(report, indent=2) + '\n')
for row in results:
    print(row['repository'], row['actual'], 'files', row['tracked_files_verified'],
          'PASS' if row['pass'] else 'FAIL', row['mismatches'])
raise SystemExit(not report['pass'])
