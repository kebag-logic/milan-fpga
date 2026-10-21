#!/usr/bin/env python3
"""Download only public round-2 author receipts and verify published hashes."""
import concurrent.futures, hashlib, json, pathlib, urllib.request, time
ROOT = pathlib.Path(__file__).resolve().parent
DEST = ROOT / 'scratch/evidence'
BASE = 'https://raw.githubusercontent.com/kebag-logic/milan-fpga/cbc4bd9f9b7348d6298adbd5c505bf138e0012eb/review-evidence/pp193-r1/'
DEST.mkdir(parents=True, exist_ok=True)
manifest = urllib.request.urlopen(BASE+'MANIFEST.json').read()
(DEST/'MANIFEST.json').write_bytes(manifest)
entries = [e for e in json.loads(manifest) if e['file'].startswith('author-r2/receipts/round2/') or e['file'] in ('author-r2/HANDOFF.md','author-r2/PR-BODY.md')]
def fetch(e):
    p=DEST/e['file']; p.parent.mkdir(parents=True,exist_ok=True)
    for attempt in range(4):
        try:
            data=p.read_bytes() if p.exists() else urllib.request.urlopen(BASE+e['file'],timeout=60).read()
            assert hashlib.sha256(data).hexdigest()==e['published_sha256'], e['file']
            p.write_bytes(data)
            return 'PASS '+e['published_sha256']+' '+e['file']
        except Exception:
            if attempt==3: raise
            time.sleep(1)
with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
    lines=list(pool.map(fetch, entries))
(ROOT/'evidence-hashes.txt').write_text('\n'.join(lines)+'\n')
print('Verified',len(lines),'public files against published_sha256; archive commit is unsigned.')
