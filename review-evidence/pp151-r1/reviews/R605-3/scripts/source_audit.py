#!/usr/bin/env python3
"""Audit the review revision and compare production tokens independently."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import stat
import subprocess

BASE = '2cbed0a987c1e68402658d69459ab7e5aa571adc'
HEAD = '02063dc1b593d422406991bf0bc60e5cc47828ff'
TREE = '2fd23c4ce9d7f23f73d6b4440b494e62d88a2682'


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('root', type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    def git(*argv):
        return subprocess.check_output(['git', '-C', str(root), *argv])
    assert git('rev-parse', 'HEAD').decode().strip() == HEAD
    assert git('rev-parse', 'HEAD^{tree}').decode().strip() == TREE
    expected = git('ls-tree', '-rz', HEAD)
    records, gitlinks = [], []
    for entry in expected.split(b'\0'):
        if not entry:
            continue
        meta, rawpath = entry.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        path = rawpath.decode()
        if mode == '160000':
            gitlinks.append({'path': path, 'sha': oid})
            assert git('-C', path, 'rev-parse', 'HEAD').decode().strip() == oid
            continue
        p = root / path
        data = p.readlink().as_posix().encode() if mode == '120000' else p.read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        actual_mode = ('120000' if p.is_symlink() else
                       '100755' if p.stat().st_mode & stat.S_IXUSR else '100644')
        assert (blob, actual_mode) == (oid, mode), path
        records.append({'path': path, 'mode': mode, 'blob': blob})
    assert git('diff', '--cached', '--raw', HEAD) == b''
    assert git('diff', '--raw', HEAD) == b''
    def stripped(text):
        return re.sub(r'/\*.*?\*/|//[^\n]*', '', text, flags=re.S)
    def normalized(text):
        text = stripped(text)
        text = text.replace('$error(', '$fatal(1, ')
        text = re.sub(r'initial\s+begin\s*:\s*parameter_checks\s*'
                      r'if\s*\(STRM_TIMEOUT_CYC_P == 0\)',
                      'if (STRM_TIMEOUT_CYC_P == 0) begin : g_strm_tmo_check', text)
        return re.findall(r'"(?:\\.|[^"\\])*"|[A-Za-z_$][\w$]*|\d+|[^\s]', text)
    changed = git('diff', '--name-only', BASE, HEAD, '--', 'hdl').decode().splitlines()
    for path in changed:
        if path.endswith('.sv'):
            assert normalized(git('show', BASE + ':' + path).decode()) == normalized(
                git('show', HEAD + ':' + path).decode()), path
    tasks = []
    for p in sorted((root / 'hdl').rglob('*.sv')):
        text = stripped(p.read_text())
        for match in re.finditer(r'\$(fatal|error|warning|info|finish|stop)\b|\bassert\b', text):
            line = text.count('\n', 0, match.start()) + 1
            tasks.append({'path': str(p.relative_to(root)), 'line': line,
                          'task': match.group(0)})
    assert len(tasks) == 31 and all(t['task'] == '$fatal' for t in tasks)
    print(json.dumps({'head': HEAD, 'tree': TREE, 'tracked_files_verified': len(records),
                      'tracked_bytes_modes_index': 'PASS', 'submodule_gitlinks': gitlinks,
                      'production_token_comparison': 'PASS: severity and listener placement only',
                      'changed_production_files': [p for p in changed if p.endswith('.sv')],
                      'tasks': tasks, 'tracked': records}, indent=2))


if __name__ == '__main__':
    main()
