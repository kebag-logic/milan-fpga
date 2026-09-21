import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path('/data/milan/reviews/r218-503-r2')
SCRATCH = ROOT.with_name(ROOT.name + '-scratch')
EVIDENCE = SCRATCH / 'evidence'
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], env=ENV)

def verify(root, rev):
    rows = git(root, 'ls-tree', '-rz', rev).split(b'\0')
    total = 0
    errors = []
    for row in rows:
        if not row:
            continue
        meta, name = row.split(b'\t', 1)
        mode, kind, oid = meta.split()
        if kind != b'blob':
            continue
        total += 1
        path = root / name.decode()
        data = os.readlink(path).encode() if mode == b'120000' else path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        if actual != oid.decode():
            errors.append(name.decode())
    return {'files': total, 'mismatches': errors}

result = {}
for label, root in [('page', ROOT), ('evidence', EVIDENCE)]:
    result[label] = verify(root, 'HEAD')
    for sub in ['protocol-processor', 'gptp-processor', 'third_party/verilog-axis']:
        pin = git(root, 'rev-parse', f'HEAD:{sub}').decode().strip()
        assert git(root / sub, 'rev-parse', 'HEAD').decode().strip() == pin
        result[label + ':' + sub] = verify(root / sub, pin)

base = 'design-evidence/500-materialization'
record = git(EVIDENCE, 'show', 'HEAD:' + base + '/COMMAND_RESULTS.md').decode()
digests = re.findall(r'^\| `([^`]+)` \| `([0-9a-f]{64})` \|$', record, re.M)
published = set(git(EVIDENCE, 'ls-tree', '-r', '--name-only', 'HEAD', base).decode().splitlines())
covered = set()
for rel, digest in digests:
    if rel.startswith(('proposal-evidence/', 'tickets/')):
        path = base + '/' + rel
        assert path in published
        data = git(EVIDENCE, 'show', 'HEAD:' + path)
        covered.add(path)
    elif rel.startswith('protocol-processor/'):
        path = rel
        pin = git(EVIDENCE, 'rev-parse', 'HEAD:protocol-processor').decode().strip()
        data = git(EVIDENCE / 'protocol-processor', 'show', pin + ':' + rel.split('/', 1)[1])
    else:
        path = rel
        data = git(EVIDENCE, 'show', 'HEAD:' + path)
    assert hashlib.sha256(data).hexdigest() == digest, rel
assert covered == published - {base + '/COMMAND_RESULTS.md'}
result['receipts'] = {'verified': len(digests), 'evidence_files': len(covered), 'repository_inputs': len(digests) - len(covered)}
assert all(not v['mismatches'] for k,v in result.items() if k != 'receipts')
print(json.dumps(result, indent=2))
(SCRATCH / 'byte-verification.json').write_text(json.dumps(result, indent=2) + '\n')
