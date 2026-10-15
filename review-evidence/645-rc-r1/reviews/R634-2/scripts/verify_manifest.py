import json, hashlib, os, sys, subprocess
root = sys.argv[1]
m = json.load(open(os.path.join(root, 'MANIFEST.json')))
bad = []; red = set(); ok = 0
for e in m:
    p = os.path.join(root, e['file'])
    if not os.path.isfile(p):
        bad.append(('missing', e['file'])); continue
    h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    if h != e['published_sha256']: bad.append(('pubhash', e['file']))
    else: ok += 1
    if e['path_redacted'] or e['original_sha256'] != e['published_sha256']: red.add(e['file'])
listed = {e['file'] for e in m}
on_disk = set()
for d, _, fs in os.walk(root):
    for f in fs:
        on_disk.add(os.path.relpath(os.path.join(d, f), root))
print('entries', len(m), 'published-hash ok', ok, 'bad', len(bad), bad[:5])
print('unlisted on disk', sorted(on_disk - listed - {'MANIFEST.json'})[:10])
print('redacted', len(red))
# author-r2 sha256sum mismatches vs redacted set
out = subprocess.run(['sha256sum', '-c', 'MANIFEST.sha256'], cwd=os.path.join(root, 'author-r2'), capture_output=True, text=True).stdout
fail = {'author-r2/' + l.split(':')[0] for l in out.splitlines() if l.endswith('FAILED')}
print('author-r2 sha256sum FAILED', len(fail), 'all redacted:', fail <= red, sorted(fail - red))
