#!/usr/bin/env python3
"""Prove a checkout is exactly its committed head: every index record equals
HEAD's tree, every tracked file's on-disk bytes hash to its blob id with the
recorded mode, and each required submodule is checked out at its gitlink with
the same proof applied inside it. Reads only; Git replace refs are disabled.
Usage: clone_integrity.py <repo> <expected-head> [required-submodule ...]"""
import hashlib, json, os, stat, subprocess, sys
from pathlib import Path
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV['GIT_NO_REPLACE_OBJECTS'] = '1'
def git(root, *a):
    return subprocess.check_output(['git', '--no-optional-locks', '-C', str(root), *a], env=ENV)
def records(raw, tree):
    out = {}
    for row in raw.split(b'\0'):
        if not row: continue
        meta, name = row.split(b'\t', 1); f = meta.split()
        if not tree and f[2] != b'0': raise SystemExit(f'unmerged {name!r}')
        out[os.fsdecode(name)] = (f[0].decode(), (f[2] if tree else f[1]).decode())
    return out
def prove(root, head):
    problems = []
    actual = git(root, 'rev-parse', 'HEAD').decode().strip()
    if actual != head: problems.append(f'{root}: HEAD {actual} != {head}')
    tree = records(git(root, 'ls-tree', '-rz', 'HEAD'), True)
    index = records(git(root, 'ls-files', '--stage', '-z'), False)
    if tree != index: problems.append(f'{root}: index differs from HEAD tree')
    flags = [l for l in git(root, 'ls-files', '-v', '-z').split(b'\0') if l and not l.startswith(b'H ')]
    if flags: problems.append(f'{root}: index flags {flags[:5]}')
    links = {}
    for name, (mode, blob) in tree.items():
        p = Path(root) / name
        if mode == '160000': links[name] = blob; continue
        try: info = p.lstat()
        except FileNotFoundError: problems.append(f'missing {p}'); continue
        if mode == '120000':
            data = os.readlink(p).encode()
            ok = stat.S_ISLNK(info.st_mode)
        else:
            ok = stat.S_ISREG(info.st_mode) and bool(info.st_mode & stat.S_IXUSR) == (mode == '100755')
            data = p.read_bytes() if stat.S_ISREG(info.st_mode) else b''
        h = hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()
        if not ok or h != blob: problems.append(f'changed {p} mode={oct(info.st_mode)} blob={h} expected={mode} {blob}')
    return problems, links, len(tree)
repo, head, required = Path(sys.argv[1]), sys.argv[2], sys.argv[3:]
problems, links, n = prove(repo, head)
result = {'head': head, 'tracked': n, 'gitlinks': links, 'submodules': {}}
for sub in required:
    if sub not in links: problems.append(f'no gitlink {sub}'); continue
    sp, sl, sn = prove(repo / sub, links[sub]); problems += sp
    result['submodules'][sub] = {'head': links[sub], 'tracked': sn}
result['problems'] = problems; result['result'] = 'PASS' if not problems else 'FAIL'
print(json.dumps(result, indent=1)); sys.exit(0 if not problems else 1)
