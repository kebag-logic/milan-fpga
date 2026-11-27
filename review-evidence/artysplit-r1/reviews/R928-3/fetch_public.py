"""Read the pinned public evidence, excluding all reviewers' report contents.

Usage: python3 fetch_public.py SCRATCH
Requires an authenticated read-only-capable gh CLI and about 1.5 GB of storage.
"""
import concurrent.futures
import hashlib
import json
import subprocess
import sys
from pathlib import Path

out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
repo = 'repos/kebag-logic/milan-fpga'
commit = '7ae7427b0d5a021db3387fa50833abde7bf18a82'

def api(path, raw=False):
    command = ['gh', 'api', f'{repo}/{path}']
    if raw:
        command += ['-H', 'Accept: application/vnd.github.raw+json']
    return subprocess.check_output(command)

def tree(oid, recursive=False):
    return json.loads(api(f'git/trees/{oid}' + ('?recursive=1' if recursive else '')))

def child(oid, name):
    return next(r['sha'] for r in tree(oid)['tree'] if r['path'] == name)

root = child(child(commit, 'review-evidence'), 'artysplit-r1')
manifest_oid = child(root, 'MANIFEST.json')
(out / 'packet-manifest.json').write_bytes(api(f'git/blobs/{manifest_oid}', True))
(out / 'evidence-commit.json').write_bytes(api(f'git/commits/{commit}'))
requests = []
for folder in ('author-r8', 'author-r7'):
    listing = tree(child(root, folder), True)
    assert not listing['truncated']
    (out / ('r8-tree.json' if folder == 'author-r8' else 'r7-tree.json')).write_text(json.dumps(listing))
    for row in listing['tree']:
        path = row['path']
        wanted = folder == 'author-r8' or (
            path.startswith('receipts/FILES') or path.endswith('INDEX.md') or
            path.startswith('receipts/recipes') or 'qualification' in path or 'derive' in path)
        if row['type'] == 'blob' and wanted:
            requests.append((folder, row))

def get(item):
    folder, row = item
    path = out / folder / row['path']
    path.parent.mkdir(parents=True, exist_ok=True)
    data = path.read_bytes() if path.exists() else api(f'git/blobs/{row["sha"]}', True)
    assert len(data) == row['size'], row['path']
    assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == row['sha'], row['path']
    if not path.exists():
        path.write_bytes(data)

with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
    for n, _ in enumerate(pool.map(get, requests), 1):
        if n % 100 == 0:
            print('Git-blob-verified files:', n, flush=True)
print('Downloaded/verified:', len(requests))
