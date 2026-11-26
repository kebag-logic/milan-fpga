#!/usr/bin/env python3
"""Audit exact bytes, gitlinks, image-input continuity and public receipt hashes."""
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

PACKET = Path(__file__).resolve().parent
HEAD = 'e5d8a71b6fa90352eca72314c7bd2275a1b20285'
EVIDENCE = '4b3b21e2104d37db96040622edfe75a5acbf2a76'
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], env=ENV)

def entries(data, index=False):
    result = {}
    for row in data.split(b'\0'):
        if not row:
            continue
        meta, name = row.split(b'\t', 1)
        a, b, c = meta.split()
        if index:
            assert c == b'0', row
            result[name] = (a, b)
        else:
            result[name] = (a, c)
    return result

def integrity(root, expected=None, probe=False):
    head = git(root, 'rev-parse', 'HEAD').decode().strip()
    if expected:
        assert head == expected
    tree = entries(git(root, 'ls-tree', '-rz', 'HEAD'))
    index = entries(git(root, 'ls-files', '--stage', '-z'), True)
    assert tree == index, 'index differs from HEAD'
    files = links = absent = 0
    for name, (mode, oid) in tree.items():
        path = root / os.fsdecode(name)
        if mode == b'160000':
            if not (path / '.git').exists():
                assert name == b'external' or (probe and name not in (b'gptp-processor', b'third_party/verilog-axis')), name
                absent += 1
                continue
            assert (path / '.git').is_file(), 'registered submodule required'
            integrity(path, oid.decode())
            links += 1
            continue
        st = path.lstat()
        if mode == b'120000':
            assert stat.S_ISLNK(st.st_mode)
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), name
            actual_mode = b'100755' if st.st_mode & 0o111 else b'100644'
            assert mode == actual_mode, name
            data = path.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert digest == oid, name
        files += 1
    label = root.name if root.name != 'r938-2-pins1125' else 'review-source'
    print(f'PASS integrity {label}: head={head}; files={files}; initialized gitlinks={links}; excluded uninitialized gitlinks={absent}; index/modes/raw blobs exact')

def evidence(root):
    signature = git(root, 'show', '--no-patch', '--format=%G?', EVIDENCE).decode().strip()
    print(f'Evidence commit {EVIDENCE}: signature status={signature}; N means unsigned, no cryptographic signature claim')
    for round_name in ('pins1125-r1', 'pins1125-r2'):
        base = 'review-evidence/' + round_name
        manifest = json.loads(git(root, 'show', EVIDENCE + ':' + base + '/MANIFEST.json'))
        count = 0
        for row in manifest:
            if not row['file'].startswith('author/'):
                continue
            data = git(root, 'show', EVIDENCE + ':' + base + '/' + row['file'])
            assert hashlib.sha256(data).hexdigest() == row['published_sha256'], row['file']
            path = PACKET / 'scratch' / 'public' / round_name / row['file']
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            count += 1
        print(f'PASS {round_name}: {count} author files match published SHA-256 manifest')
    for path in ('hdl', 'syn', 'sw', 'configs', 'constraints', 'avdecc', 'gptp-processor', 'third_party/tsn-c-stack', 'protocol-processor', 'third_party/verilog-axis'):
        before = git(root, 'ls-tree', 'a6864a49', '--', path)
        after = git(root, 'ls-tree', HEAD, '--', path)
        assert before == after, path
        print('PASS unchanged input: ' + after.decode().strip())
    for path in ('scripts/py_idiom.budget', 'scripts/test_evidence.budget'):
        assert git(root, 'show', 'c34e7d8b:' + path) == git(root, 'show', HEAD + ':' + path)
        print('PASS unchanged budget ' + path)
    donor = root / 'gptp-processor'
    for path in ('hdl', 'syn'):
        before = git(donor, 'rev-parse', '3009f9a2:' + path).decode().strip()
        after = git(donor, 'rev-parse', '3ce71b76:' + path).decode().strip()
        assert before == after
        print(f'PASS donor {path} tree identical: {after}')
    routes = PACKET / 'scratch/public/pins1125-r1/author/receipts/routes'
    for pair in ('1x1-ExtraPostPlacementOpt', '8x8-ExtraPostPlacementOpt', '8x8-ExtraTimingOpt'):
        head = (routes / ('head-' + pair + '-signoff.txt')).read_text()
        base = (routes / ('base-' + pair + '-signoff.txt')).read_text()
        pattern = r'^(?:Slow|Fast)_.*$'
        assert re.findall(pattern, head, re.M) == re.findall(pattern, base, re.M)
        assert len(re.findall(pattern, head, re.M)) == 4
        for row in re.findall(pattern, head, re.M):
            print('PAIR ' + pair + ': ' + row)
        hu = (routes / ('head-' + pair + '-utilization.txt')).read_text().splitlines()[1:]
        bu = (routes / ('base-' + pair + '-utilization.txt')).read_text().splitlines()[1:]
        # The head first line prefixes gateware with the shape/build path.
        hu[0] = hu[0][hu[0].index('gateware '):]
        bu[0] = bu[0][bu[0].index('gateware '):]
        assert hu == bu
        print('PASS matched timing and utilization: ' + pair)
    assert not (routes / 'base-8x8-AltSpreadLogic_high-signoff.txt').exists()
    print('UNPAIRED head-8x8-AltSpreadLogic_high; no equality claimed')
    for pair in ('1x1-ExtraPostPlacementOpt', '8x8-ExtraTimingOpt'):
        text = (routes / ('head-' + pair + '-signoff.txt')).read_text()
        corners = re.findall(r'WNS ([+-][0-9.]+) ns \(0 failing\), WHS ([+-][0-9.]+) ns \(0 failing\)', text)
        assert len(corners) == 4
        assert all(float(setup) >= .030 and float(hold) >= 0 for setup, hold in corners)
        print('PASS selected route governing floors: ' + pair)
    for name in ('gptp_shadow.log', 'gptp_plane.log', 'milan_dp-gptp-legs.log', 'old-generator-red.log', 'image-inputs.txt', 'docs-workflow-steps.log'):
        data = (PACKET / 'scratch/public/pins1125-r2/author/receipts' / name).read_bytes()
        (PACKET / 'receipts' / ('published-' + name)).write_bytes(data)

if __name__ == '__main__':
    root = Path(sys.argv[1]).resolve()
    if sys.argv[2] == 'evidence':
        evidence(root)
    else:
        integrity(root, HEAD, probe=sys.argv[2] == 'probe-integrity')
