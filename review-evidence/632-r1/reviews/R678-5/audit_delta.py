#!/usr/bin/env python3
"""Verify the review delta, executable identity, and all tracked bytes and modes."""
import ast
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tokenize

HEAD = '24a292a0321df6f3516f25cb6e92e24fb1988e65'
BASE = '417ec528'
REQUIRED = ['protocol-processor', 'gptp-processor', 'third_party/verilog-axis', 'third_party/tsn-c-stack', 'third_party/lwSRP']

def git(*args, cwd=None):
    return subprocess.check_output(['git', '--no-replace-objects', *args], cwd=cwd)

def blob(ref, path):
    return git('show', f'{ref}:{path}').decode()

def cpp_tokens(source):
    # Preserve string/character literals while discarding only comments and whitespace.
    pattern = r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\s+|.'
    return [m.group() for m in re.finditer(pattern, source)
            if not m.group().isspace() and not m.group().startswith(('//', '/*'))]

def py_tokens(source):
    ignored = {tokenize.COMMENT, tokenize.NL, tokenize.ENCODING}
    return [(t.type, t.string) for t in tokenize.generate_tokens(io.StringIO(source).readline)
            if t.type not in ignored]

def verify_tree(root, ref):
    tree = git('ls-tree', '-rz', ref, cwd=root)
    expected_index = []
    count = 0
    links = {}
    for record in tree.split(b'\0'):
        if not record:
            continue
        meta, name = record.split(b'\t', 1)
        mode, kind, oid = meta.split()
        expected_index.append(mode + b' ' + oid + b' 0\t' + name)
        path = Path(root) / os.fsdecode(name)
        if mode == b'160000':
            links[os.fsdecode(name)] = oid.decode()
            continue
        info = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(info.st_mode), str(path)
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(info.st_mode), str(path)
            actual_mode = b'100755' if info.st_mode & 0o111 else b'100644'
            assert actual_mode == mode, str(path)
            data = path.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert digest == oid.decode(), str(path)
        count += 1
    actual_index = git('ls-files', '--stage', '-z', cwd=root).split(b'\0')
    assert sorted(filter(None, actual_index)) == sorted(expected_index), 'index mismatch'
    return {'blobs_verified': count, 'index_and_modes_exact': True, 'gitlinks': links}

def main():
    root = Path(sys.argv[1]).resolve()
    os.chdir(root)
    assert git('rev-parse', 'HEAD').decode().strip() == HEAD
    changed = git('diff', '--name-only', BASE, HEAD).decode().splitlines()
    executable = {}
    for path in changed:
        if path.endswith('.md'):
            continue
        a, b = blob(BASE, path), blob(HEAD, path)
        if path.endswith('.py'):
            assert py_tokens(a) == py_tokens(b), path
            assert ast.dump(ast.parse(a)) == ast.dump(ast.parse(b)), path
            compile(b, path, 'exec')
        elif path.endswith('.cpp'):
            assert cpp_tokens(a) == cpp_tokens(b), path
        else:
            raise AssertionError(path)
        executable[path] = 'identical non-comment tokens'
    assert not git('diff', BASE, HEAD, '--', 'hdl', 'syn', 'configs')
    result = {'head': HEAD, 'tree': git('rev-parse', 'HEAD^{tree}').decode().strip(),
              'changed_paths': changed, 'executable_identity': executable,
              'hdl_syn_configs_delta_empty': True, 'root': verify_tree(root, HEAD)}
    result['submodules'] = {}
    for name in REQUIRED:
        pin = result['root']['gitlinks'][name]
        sub = root / name
        assert (sub / '.git').is_file(), name
        assert git('rev-parse', 'HEAD', cwd=sub).decode().strip() == pin, name
        result['submodules'][name] = {'head': pin, **verify_tree(sub, pin)}
    diff = git('diff', '-U0', 'e26f1816', HEAD).decode()
    result['added_2020_citations'] = [l for l in diff.splitlines() if l.startswith('+') and '802.1AS-2020' in l]
    assert len(result['added_2020_citations']) == 1
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
