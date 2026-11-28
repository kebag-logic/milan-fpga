# Usage: python3 -I manifest_check.py <evidence-checkout> <commit>: recompute author-r3 hashes against MANIFEST.json
import json, subprocess, sys, hashlib
repo, commit = sys.argv[1], sys.argv[2]
m = json.loads(subprocess.check_output(['git', '-C', repo, 'show', f'{commit}:review-evidence/pbtsn-r1/MANIFEST.json']))
ok = True
for e in m:
    if not e['file'].startswith('author-r3/'):
        continue
    data = subprocess.check_output(['git', '-C', repo, 'show', f"{commit}:review-evidence/pbtsn-r1/{e['file']}"])
    h = hashlib.sha256(data).hexdigest()
    good = h == e['published_sha256']
    ok &= good
    print('OK ' if good else 'BAD', e['file'], h)
listed = {e['file'] for e in m}
tree = subprocess.check_output(['git', '-C', repo, 'ls-tree', '-r', '--name-only', commit, 'review-evidence/pbtsn-r1/author-r3/']).decode().split()
for p in tree:
    rel = p.split('review-evidence/pbtsn-r1/', 1)[1]
    if rel not in listed:
        ok = False; print('UNLISTED', rel)
print('manifest author-r3:', 'pass' if ok else 'FAIL')
