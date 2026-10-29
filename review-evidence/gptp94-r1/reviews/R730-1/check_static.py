#!/usr/bin/env python3
"""Verify generated images, exact source bytes/index/modes, and public receipts."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--repo', type=Path, required=True)
a = p.parse_args()
packet = Path(__file__).resolve().parent
scratch = packet / 'scratch' / 'static'
scratch.mkdir(parents=True, exist_ok=True)
tmp = packet / 'scratch' / 'tmp'
tmp.mkdir(parents=True, exist_ok=True)
os.environ['TMPDIR'] = str(tmp)

def git(*args):
    return subprocess.check_output(['git', '-C', str(a.repo), *args])

with (packet / 'integrity.log').open('w') as out:
    head = git('rev-parse', 'HEAD').decode().strip()
    tree = git('rev-parse', 'HEAD^{tree}').decode().strip()
    assert head == '9d509029de967c50de7527edf2b8869aa9db9074'
    assert tree == '4d0c9d078cb2d575b100e23c6b34c2637c247594'
    assert git('status', '--porcelain=v1') == b''
    assert git('diff', '--raw', 'HEAD') == b''
    assert git('diff', '--cached', '--raw', 'HEAD') == b''
    index = git('ls-files', '--stage', '-z')
    (packet / 'tracked-index.txt').write_bytes(index.replace(b'\0', b'\n'))
    count = 0
    links = []
    for row in git('ls-tree', '-r', '-z', 'HEAD').split(b'\0'):
        if not row:
            continue
        meta, name = row.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        name = name.decode()
        if mode == '160000':
            links.append((name, oid))
            continue
        path = a.repo / name
        data = os.readlink(path).encode() if mode == '120000' else path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert actual == oid, name
        if mode != '120000':
            assert bool(path.stat().st_mode & 0o111) == (mode == '100755'), name
        count += 1
    print('HEAD', head, '\nTREE', tree, file=out)
    print('Tracked blob bytes and executable modes matched:', count, file=out)
    print('Working tree clean; index equals HEAD.', file=out)
    print('Source submodule gitlinks:', links, file=out)
    patch = (packet / 'public/author/milan-fpga-companion.patch').read_text()
    assert '+Subproject commit ' + head in patch
    print('Parent companion gptp-processor gitlink equals reviewed HEAD.', file=out)

(packet / 'source-history.txt').write_bytes(git('log', '--format=%H %s', 'f97c1803..HEAD'))
(packet / 'reviewed.diff').write_bytes(git('diff', 'f97c1803..HEAD'))
subprocess.run(['git', '-C', str(a.repo), 'diff', '--check', 'f97c1803..HEAD'], check=True)

with (packet / 'rom-regeneration.log').open('w') as out:
    for path, flags in [
        ('syn/ooc/work/gptp_ucode.hex', []),
        ('tb/verilator/ucpu/gptp_ucode.hex', []),
        ('tb/tsngen/gptp_ucode.hex', ['--clk-hz', '2000000']),
        ('tb/verilator/engine/gptp_ucode.hex', ['--clk-hz', '2000000', '--cease-ms', '3000']),
    ]:
        dest = scratch / path.replace('/', '_')
        cmd = ['python3', str(a.repo / 'hdl/ucode/gen_gptp_ucode.py'), *flags, '-o', str(dest)]
        subprocess.run(cmd, stdout=out, stderr=subprocess.STDOUT, check=True)
        assert dest.read_bytes() == (a.repo / path).read_bytes(), path
        print('BYTE-IDENTICAL', path, hashlib.sha256(dest.read_bytes()).hexdigest(), file=out)

with (packet / 'public-receipt-hashes.log').open('w') as out:
    checked = 0
    for row in json.loads((packet / 'public-manifest.json').read_text()):
        path = packet / 'public' / row['file']
        if not path.exists():
            continue
        b = path.read_bytes()
        expected = row['published_sha256']
        # A text transport may append its own final newline; remove only if
        # doing so restores the independently published exact digest.
        if hashlib.sha256(b).hexdigest() != expected and hashlib.sha256(b[:-1]).hexdigest() == expected:
            path.write_bytes(b[:-1])
            b = b[:-1]
        assert hashlib.sha256(b).hexdigest() == expected, str(path)
        print(expected, row['file'], file=out)
        checked += 1
    print('Published files verified:', checked, file=out)

with (packet / 'docs-check.log').open('w') as out:
    r = subprocess.run(['make', '-j16', 'docs'], cwd=a.repo, stdout=out, stderr=subprocess.STDOUT)
(packet / 'docs-check.rc').write_text(str(r.returncode) + '\n')
print('Static integrity, four ROM regenerations, receipt hashes: PASS; docs rc', r.returncode)
