#!/usr/bin/env python3
"""Read-only review audit. Usage: audit.py SOURCE PACKET. Fetch evidence commit first."""
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

src, out = map(lambda p: Path(p).resolve(), sys.argv[1:])
HEAD = 'fc6870cab13f74149864b80b6480ddb3641cb936'
OLD = 'f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21'
EVID = '1fe0516af44a9d94eb1f5667d32eb67919851eba'
PREFIX = 'review-evidence/gptppin-r1/'
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1', PYTHONDONTWRITEBYTECODE='1')

def git(*args, root=src):
    return subprocess.check_output(['git', *args], cwd=root, env=env)

def entries(root, rev):
    result = {}
    for row in git('ls-tree', '-rz', rev, root=root).split(b'\0'):
        if row:
            info, name = row.split(b'\t')
            mode, kind, oid = info.decode().split()
            result[os.fsdecode(name)] = (mode, kind, oid)
    return result

log = []
assert git('rev-parse', 'HEAD').decode().strip() == HEAD
assert git('rev-parse', 'HEAD^{tree}').decode().strip() == '47c0ec30481efe50fd892060ebeb61ef9bc423c2'
log.append('Exact source head and tree: PASS')
manifest = json.loads(git('show', EVID + ':' + PREFIX + 'MANIFEST.json'))
counts = {}
for row in manifest:
    group = row['file'].split('/')[0]
    if group not in ('author', 'author-r2', 'author-r3'):
        continue
    data = git('show', EVID + ':' + PREFIX + row['file'])
    assert hashlib.sha256(data).hexdigest() == row['published_sha256'], row['file']
    counts[group] = counts.get(group, 0) + 1
log.append('Published manifest SHA-256 matches: ' + json.dumps(counts, sort_keys=True))
commit = git('cat-file', 'commit', EVID)
log.append('Evidence commit signature header present: ' + str(b'\ngpgsig ' in commit.split(b'\n\n')[0]))
log.append('Content hashes verified; no cryptographic signer authentication claimed.')
before, after = entries(src, OLD), entries(src, HEAD)
changed = [p for p in sorted(before.keys() | after.keys()) if before.get(p) != after.get(p)]
assert changed == ['CHANGELOG.md', 'docs/reference/SUBMODULES.md', 'tb/verilator/gptp_shadow/README.md', 'tb/verilator/gptp_shadow/mutants.py', 'tb/verilator/gptp_shadow/sim_main.cpp', 'tb/verilator/gptp_shadow/test_mutant_lifecycle.py']
log.append('Delta: ' + ', '.join(changed))
images = [p for p, v in after.items() if p.endswith(('.png', '.svg', '.drawio')) or v[0] == '160000']
assert len(images) == 291
assert all(before[p] == after[p] for p in images)
log.append('291 image/gitlink entries identical: PASS')
for p in ['docs/diagrams/submodule_boundaries.png', 'docs/diagrams/timesync_chain.png', 'gptp-processor/syn/ooc/work/gptp_ucode.hex']:
    if (src / p).exists():
        log.append(hashlib.sha256((src / p).read_bytes()).hexdigest() + '  ' + p)
rom = out / 'scratch/default-gptp.hex'
rom.parent.mkdir(parents=True, exist_ok=True)
subprocess.check_output(['python3', '-B', 'gptp-processor/hdl/ucode/gen_gptp_ucode.py', '-o', str(rom)], cwd=src, env=env)
assert hashlib.sha256(rom.read_bytes()).hexdigest() == '4eb21cefc8d769df4a764402aead970b59be96cb3fa267d25af9d1857935f083'
assert rom.read_bytes() == (src / 'gptp-processor/syn/ooc/work/gptp_ucode.hex').read_bytes()
log.append('Independent default ROM regeneration equals tracked default image and ledger: PASS')

def evidence(path):
    return git('show', EVID + ':' + PREFIX + path).decode()

def image_hashes(text):
    return {m[2]: m[1] for m in re.finditer(r'^([0-9a-f]{64})\s+(\./\S+)', text, re.M)}

old_hashes = image_hashes(evidence('author-r2/receipts/ledger/image-hashes-vs-round1.txt'))
new_hashes = image_hashes(evidence('author-r3/receipts/ledger/images-unchanged.txt'))
assert len(old_hashes) == len(new_hashes) == 24 and old_hashes == new_hashes
log.append('24 published firmware hashes equal across rounds: PASS (receipt comparison, no firmware rebuild)')
dry = subprocess.check_output(['make', '-n', '-B', '--no-print-directory', 'build-gptp', 'build-gptp-lat'], cwd=src / 'tb/verilator/milan_dp', env=env).decode()
inputs = set()
for word in dry.split():
    p = (src / 'tb/verilator/milan_dp' / word).resolve()
    if p.is_file() and p.is_relative_to(src):
        inputs.add(str(p.relative_to(src)))
assert not inputs.intersection(changed)
log.append(f'milan_dp expanded recipe existing file inputs: {len(inputs)}; intersection with delta: empty')
local_text = '\n'.join(p.read_text(errors='replace') for p in (src / 'tb/verilator/milan_dp').iterdir() if p.is_file())
assert 'tb/verilator/gptp_shadow' not in local_text
log.append('No milan_dp local file references changed shadow harness directory: PASS')
for path in ['author-r2/receipts/rtl/milan_dp-gptp-f97e49fe.log', 'author-r2/receipts/rtl/milan_dp-gptp-lat-f97e49fe.log']:
    data = evidence(path)
    lines = [x for x in data.splitlines() if re.search(r'212|FAIL|RESULT|\[CA\]', x)]
    log.extend([path, *lines])
for path in ['author-r3/receipts/rtl/gptp_shadow-run.log', 'author-r3/receipts/probes/probe-order-stall.log', 'author-r3/receipts/probes/probe-r915-p106-nocredit.log']:
    data = evidence(path)
    log.extend([path, *[x for x in data.splitlines() if re.search(r'^FAIL |^\d+ checks:|last beat|INFO #106 reserve', x)]])
(out / 'artifact-audit.log').write_text('\n'.join(log) + '\n')
(out / 'milan-inputs.txt').write_text('\n'.join(sorted(inputs)) + '\n')

integrity = []
def check_tree(root, rev, label):
    tree = entries(root, rev)
    index = {}
    for row in git('ls-files', '--stage', '-z', root=root).split(b'\0'):
        if row:
            info, name = row.split(b'\t')
            mode, oid, stage = info.decode().split()
            assert stage == '0'
            index[os.fsdecode(name)] = (mode, oid)
    assert index == {p: (m, oid) for p, (m, _, oid) in tree.items()}
    checked = 0
    for name, (mode, kind, oid) in tree.items():
        if mode == '160000':
            continue
        p = root / name
        st = p.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(st.st_mode)
            data = os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(st.st_mode)
            assert bool(st.st_mode & 0o111) == (mode == '100755'), name
            data = p.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid, name
        checked += 1
    integrity.append(f'{label}: {checked} tracked blob bytes/modes and entire index match {rev}')
    return tree

tree = check_tree(src, HEAD, 'source')
for sub, (mode, _, oid) in tree.items():
    if mode != '160000':
        continue
    if sub == 'external':
        integrity.append(f'{sub}: unused uninitialized gitlink unchanged {oid}')
        continue
    root = src / sub
    assert (root / '.git').is_file(), sub
    assert git('rev-parse', 'HEAD', root=root).decode().strip() == oid
    assert Path(git('rev-parse', '--show-superproject-working-tree', root=root).decode().strip()).resolve() == src
    check_tree(root, oid, sub)
integrity.append('git status --porcelain: ' + repr(git('status', '--porcelain').decode()))
(out / 'integrity.log').write_text('\n'.join(integrity) + '\n')
print('\n'.join(log[:12] + integrity))
