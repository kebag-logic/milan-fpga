#!/usr/bin/env python3
"""Read-only source and image-evidence invariants for review R585-9."""
import argparse
import hashlib
import re
import subprocess
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('root', type=Path)
ap.add_argument('packet', type=Path)
args = ap.parse_args()
root = args.root.resolve()

def git(*argv):
    return subprocess.check_output(['git', '-C', str(root), *argv])

lexer = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|/\*.*?\*/|//[^\n]*|\w+|[^\w\s]', re.S)
def tokens(data):
    return [s for s in lexer.findall(data.decode()) if not s.startswith(('/*', '//'))]

mapping = {'src/adp.c': 'adp/adp.c', 'src/acmp.c': 'acmp/acmp.c', 'src/maap.c': 'maap/maap.c',
           'include/adp.h': 'adp/adp.h', 'include/acmp.h': 'acmp/acmp.h',
           'include/maap.h': 'maap/maap.h', 'include/wire.h': 'wire/wire.h'}
for new, old in mapping.items():
    before = tokens(git('show', 'aef7ac66:sw/firmware/ctrl/' + old))
    after = tokens((root / 'third_party/tsn-c-stack' / new).read_bytes())
    assert before == after, new
    print('TOKEN IDENTITY', new, len(after), 'tokens')
wire = 'sw/firmware/ctrl/mbx/mbx_wire.h'
assert tokens(git('show', 'aef7ac66:' + wire)) == tokens((root / wire).read_bytes())
print('SURVIVING HEADER mbx_wire.h: comment-only change')
for path in ['hdl', 'syn', 'tb/common', 'sw/mailbox']:
    assert not git('diff', '--name-only', '8b61b709..HEAD', '--', path), path
    print('UNCHANGED FROM SOURCE BASE', path)
for path in ['gptp-processor', 'protocol-processor', 'third_party/verilog-axis', 'third_party/lwSRP']:
    assert git('ls-tree', '8b61b709', '--', path) == git('ls-tree', 'HEAD', '--', path), path
    print('UNCHANGED GITLINK', path)
changed = git('diff', '--name-only', 'feed95bb..HEAD').decode().splitlines()
expected = ['sw/firmware/ctrl/README.md', 'sw/firmware/ctrl/test/ctrl_boundary.py',
            'sw/firmware/ctrl/test/ctrl_build.py', 'sw/firmware/ctrl/test/ctrl_pin.py']
assert changed == expected
print('DELTA EXACTLY', changed)
manifests = [args.packet / p for p in ['public/round2b/images-dev.sha256',
             'public/round9/images-head.sha256', 'public/round10/images-head.sha256']]
data = [p.read_bytes() for p in manifests]
assert len(data[0].splitlines()) == 35 and len(set(data)) == 1
print('35/35 IMAGE HASH ROWS IDENTICAL', hashlib.sha256(data[0]).hexdigest())
print('Image result is comparison of published author manifests, not a local rebuild.')
make = args.packet / 'public/round10/logs'
assert (make / 'make-reading-feed95bb.json').read_bytes() == (make / 'make-reading-head.json').read_bytes()
print('Published make readings: byte-identical')
