#!/usr/bin/env python3
"""Verify generated ROM scope, digest, source identity, and downloaded public blobs."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
p = Path(__file__).resolve().parents[1]
def git(*args):
    return subprocess.check_output(['git', '-C', str(root), *args])
head = '51f88c7e14e7e2527c09ff9a23b93dd6b857fd50'
assert git('rev-parse', 'HEAD').decode().strip() == head
assert git('rev-parse', 'HEAD^{tree}').decode().strip() == '438b7967df80fabeef960173e28bc1334de30cec'
assert git('diff', '--raw') == b'' and git('diff', '--cached', '--raw') == b''
entries = git('ls-files', '--stage', '-z').split(b'\0')
count = 0
links = []
for ent in filter(None, entries):
    attr, name = ent.split(b'\t', 1)
    mode, oid, stage = attr.decode().split()
    assert stage == '0'
    path = root / name.decode()
    if mode == '160000':
        links.append((name.decode(), oid)); continue
    raw = path.readlink().as_posix().encode() if mode == '120000' else path.read_bytes()
    digest = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    assert digest == oid, name
    if mode != '120000':
        assert bool(path.stat().st_mode & 0o111) == (mode == '100755'), name
    count += 1
print('HEAD and tree exact; tracked blobs/modes/index verified:', count, '; gitlinks:', links)
base = p / 'scratch/base-generator'
base.mkdir(exist_ok=True)
shutil.copytree(root/'hdl/aecp/ucode', base, dirs_exist_ok=True)
(base/'gen_ucode.py').write_bytes(git('show', '08023123:hdl/aecp/ucode/gen_ucode.py'))
for name, generator in [('base', base/'gen_ucode.py'), ('head', root/'hdl/aecp/ucode/gen_ucode.py')]:
    subprocess.run([sys.executable, '-B', str(generator), '-o', str(p/'scratch'/f'{name}.hex')], check=True)
a = (p/'scratch/base.hex').read_bytes()
b = (p/'scratch/head.hex').read_bytes()
words = [i for i,(x,y) in enumerate(zip(a.splitlines(), b.splitlines())) if x != y]
assert words == list(range(1859,1874)), words
assert len(a.splitlines()) == len(b.splitlines()) == 2048
digest = hashlib.sha256(b).hexdigest()
record = json.loads((root/'tb/aecp_cmds/decode.json').read_text())
assert digest in json.dumps(record)
print('Changed ROM word indices:', words)
print('Base ROM SHA256:', hashlib.sha256(a).hexdigest())
print('Head ROM SHA256:', digest, '; decode.json matches')
assert git('diff', '0b0974604f770412abea610c3ac819858c7dc708', head, '--', 'hdl') == b''
print('hdl/ identical at decode re-record and final head')
changed = git('diff', '--name-only', '08023123', head).decode().splitlines()
assert [f for f in changed if f.startswith('hdl/')] == ['hdl/aecp/ucode/gen_ucode.py']
print('No RTL interface, parameter, register-map, or other generated-program word changes')
tree = json.loads((p/'receipts/public-archive-tree.json').read_text())
expected = {x['path']:x['sha'] for x in tree['tree'] if x['type']=='blob'}
verified = 0
for f in sorted((p/'receipts/public').rglob('*')):
    if not f.is_file(): continue
    raw = f.read_bytes(); rel=f.relative_to(p/'receipts/public').as_posix()
    digest = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    assert digest == expected[rel], (rel, digest, expected[rel])
    verified += 1
print('Public archive files verified against published Git blob IDs:', verified)
