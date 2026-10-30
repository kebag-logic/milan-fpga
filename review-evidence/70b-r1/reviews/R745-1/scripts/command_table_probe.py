#!/usr/bin/env python3
"""For every changed declared script in REPO between BASE and HEAD, compare the
command-table sha256 with the file bytes at BASE and at HEAD. Usage: REPO BASE"""
import hashlib, json, subprocess, sys
repo, base = sys.argv[1], sys.argv[2]
def show(rev, path):
    r = subprocess.run(['git', '-C', repo, 'show', f'{rev}:{path}'], capture_output=True)
    return r.stdout if r.returncode == 0 else None
def table(rev):
    d = json.loads(show(rev, 'ci/image/command-table.json'))
    out = {}
    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if isinstance(v, dict) and 'sha256' in v and '/' in k: out[k] = v['sha256']
                walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(d); return out
tb, th = table(base), table('HEAD')
changed = subprocess.run(['git', '-C', repo, 'diff', '--name-only', base, 'HEAD'], capture_output=True, text=True).stdout.split()
for p in changed:
    if p in th or p in tb:
        b, h = show(base, p), show('HEAD', p)
        sb = hashlib.sha256(b).hexdigest() if b is not None else None
        sh = hashlib.sha256(h).hexdigest() if h is not None else None
        print(f'{p}: base_in_sync={tb.get(p)==sb} head_in_sync={th.get(p)==sh}')
stale_base = sum(1 for p, s in tb.items() if (lambda b: b is not None and hashlib.sha256(b).hexdigest() != s)(show(base, p)))
stale_head = sum(1 for p, s in th.items() if (lambda b: b is not None and hashlib.sha256(b).hexdigest() != s)(show('HEAD', p)))
print('declared', len(th), 'stale at base', stale_base, 'stale at head', stale_head)
