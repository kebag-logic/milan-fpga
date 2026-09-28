#!/usr/bin/env python3
"""Compare merge-dev and round-3 service receipts and bind them to the exact head.

Usage: compare_receipts.py <evidence 590-r1 dir> <repo> <head> <r3 head> <out.json>
For each service receipt: every field except build_hashes/input_hashes must be
equal between rounds; the differing hash keys are listed; every repo-relative
hash key in the merge-dev receipt must equal SHA-256 of that path at <head>
(and the round-3 one at <r3 head>); gitlinked sources are read from the
submodule object store at the pinned commit.
"""
import gzip, hashlib, json, subprocess, sys
from pathlib import Path

base, repo, head, r3head, out = Path(sys.argv[1]), Path(sys.argv[2]), *sys.argv[3:6]
PK = {'md': base / 'author-mergedev', 'r3': base / 'author-r3'}

def art(key, name):
    arts = {a['name']: a for a in json.loads((PK[key] / 'native-artifacts.json').read_text())}
    a = arts.get(name) or arts.get(name + '.gz')
    for s in a['stored']:
        p = PK[key] / s['path']
        if p.is_file():
            d = p.read_bytes()
            d = gzip.decompress(d) if p.suffix == '.gz' else d
        else:
            rel = s['path'][:-3] if s['path'].endswith('.gz') else s['path']
            cands = [PK[key] / rd / rel for rd in ('raw', 'native-evidence-raw')] + \
                    [PK[key] / rd / Path(rel).name for rd in ('raw', 'native-evidence-raw')]
            d = next(c.read_bytes() for c in cands if c.is_file())
        assert hashlib.sha256(d).hexdigest() == a['raw_sha256'], name
        return json.loads(d)

def blob_sha(rev, path):
    """SHA-256 of path at rev, descending into gitlinked submodules."""
    parts = path.split('/')
    for sub in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis'):
        if path.startswith(sub + '/'):
            pin = subprocess.run(['git', '-C', repo, 'rev-parse', f'{rev}:{sub}'], capture_output=True, text=True).stdout.strip()
            r = subprocess.run(['git', '-C', str(Path(repo) / sub), 'show', f'{pin}:{path[len(sub)+1:]}'], capture_output=True)
            return hashlib.sha256(r.stdout).hexdigest() if r.returncode == 0 else None
    r = subprocess.run(['git', '-C', repo, 'show', f'{rev}:{path}'], capture_output=True)
    return hashlib.sha256(r.stdout).hexdigest() if r.returncode == 0 else None

names = sorted(a['name'].removesuffix('.gz') for a in json.loads((PK['md'] / 'native-artifacts.json').read_text())
               if a['name'].removesuffix('.gz').endswith('-receipt.json'))
report, fail = {}, []
for n in names:
    m, r = art('md', n), art('r3', n)
    fields = sorted(set(m) | set(r))
    unequal = [f for f in fields if f not in ('build_hashes', 'input_hashes') and m.get(f) != r.get(f)]
    rows = {}
    for f in ('build_hashes', 'input_hashes'):
        a, b = m.get(f, {}), r.get(f, {})
        rows[f] = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
    bind = {}
    for f in ('build_hashes', 'input_hashes'):
        for k, v in m.get(f, {}).items():
            if k.startswith(('build/', 'external/')):
                continue
            ok_md = blob_sha(head, k) == v
            ok_r3 = (r.get(f, {}).get(k) is None) or blob_sha(r3head, k) == r[f][k]
            if not (ok_md and ok_r3):
                bind[f + ':' + k] = dict(md_head=ok_md, r3_head=ok_r3)
    report[n] = dict(unequal_fields=unequal, differing_hash_keys=rows, head_binding_failures=bind,
                     n_build=len(m.get('build_hashes', {})), n_input=len(m.get('input_hashes', {})))
    if unequal or bind:
        fail.append(n)
    print(n, 'unequal fields:', unequal or 'none', '| differing keys:',
          sorted(set(rows['build_hashes']) | set('input:' + k for k in rows['input_hashes'])),
          '| head binding failures:', len(bind))
json.dump(report, open(out, 'w'), indent=1)
print('RESULT', 'FAIL ' + ' '.join(fail) if fail else 'PASS', len(names), 'receipts')
sys.exit(1 if fail else 0)
