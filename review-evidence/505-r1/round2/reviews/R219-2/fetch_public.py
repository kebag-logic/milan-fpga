import base64
import concurrent.futures
import hashlib
import json
import pathlib
import subprocess

OUT = pathlib.Path(__file__).resolve().parent
PREFIX = 'review-evidence/505-r1/'
tree = json.loads((OUT / 'public/archive-tree.json').read_text())['tree']
exact = {
    'MANIFEST.json', 'README.md', 'act-draft-fast/results.json', 'act-draft-fast/01.log',
    'round2/manager-builder-spec.json', 'round2/manager/candidate-before-push.json',
    'round2/author/before/results.json', 'round2/author/after/results.json',
    'round2/author/before/definitions.json', 'round2/author/after/M5b.patch',
    'round2/author/controls/results.json',
}
rows = [r for r in tree if r['type'] == 'blob' and r['path'].startswith(PREFIX)
        and (r['path'][len(PREFIX):] in exact or r['path'][len(PREFIX):].startswith(
            ('ac5/', 'ac5-act/', 'round2/manager-builder/')))]

def fetch(row):
    rel = row['path'][len(PREFIX):]
    raw = subprocess.check_output(['gh', 'api',
        'repos/kebag-logic/milan-fpga/git/blobs/' + row['sha']])
    data = base64.b64decode(json.loads(raw)['content'])
    oid = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert oid == row['sha'], rel
    dst = OUT / 'public/archive' / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(data)
    return {'path': rel, 'blob': oid, 'sha256': hashlib.sha256(data).hexdigest(),
            'bytes': len(data)}

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(fetch, rows))
(OUT / 'receipts/public-downloads.json').write_text(json.dumps(results, indent=2) + '\n')
print(f'Downloaded and verified {len(results)} public blobs; no reviewer files read.')
