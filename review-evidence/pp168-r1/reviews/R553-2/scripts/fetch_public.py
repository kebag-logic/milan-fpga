#!/usr/bin/env python3
"""Read public authority and immutable implementation receipts; no remote writes."""
import concurrent.futures
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import urllib.request

packet = Path(sys.argv[1]).resolve()
out = packet/'receipts'
repo = 'Mister-M-alt/protocol-processor-control-plane-avb-milan'
commit = '1570e00395c98ed4ea1c21e6abde28948346c82b'
prefix = 'review-evidence/pp168-r1/author/'
names = ['REVIEW-READY-RECEIPT.json', 'round2-recovery/head-source.json',
    'round2-recovery/area-summary.json', 'round2-recovery/head-logs/suites.log',
    'round2-recovery/head-logs/check.log', 'round2-recovery/head-logs/pp_top-acmp_mutants.log',
    'round2-recovery/head-logs/matrix.log', 'round2-recovery/parent-head-pin.json',
    'round2-recovery/parent-head-completed.json', 'round2-recovery/head-logs/suites-receipt.json',
    'round2-recovery/area/base/result.json', 'round2-recovery/area/compare-byte/result.json']
def api(path):
    return json.loads(subprocess.check_output(['gh', 'api', path], text=True))
tree = api(f'repos/kebag-logic/milan-fpga/git/trees/{commit}?recursive=1')
assert not tree.get('truncated')
objects = {r['path']: r['sha'] for r in tree['tree']}
def fetch(name):
    url = f'https://raw.githubusercontent.com/kebag-logic/milan-fpga/{commit}/{prefix}{name}'
    data = urllib.request.urlopen(url, timeout=60).read()
    blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert blob == objects[prefix+name], name
    dest = out/'public'/name
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return {'path': str(dest.relative_to(packet)), 'url': url, 'git_blob': blob,
            'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    rows = list(pool.map(fetch, names))
(out/'public-source-index.json').write_text(json.dumps(rows, indent=2)+'\n')
issue = api(f'repos/{repo}/issues/168')
comments = api(f'repos/{repo}/issues/168/comments?per_page=100')
ids = {6050429859,6050554601,6053709015,6076502893,6086157264,6085166708,6086365354}
selected = [{k:c[k] for k in ['id','html_url','created_at','updated_at','body']}
            for c in comments if c['id'] in ids]
scope = {'issue': {k:issue[k] for k in ['number','title','html_url','body','updated_at']},
         'comments': selected}
(out/'public-scope.json').write_text(json.dumps(scope, indent=2)+'\n')
pr = api(f'repos/{repo}/pulls/171')
prsafe = {k:pr[k] for k in ['number','html_url','title','body','updated_at','state']}
prsafe.update({'head': pr['head']['sha'], 'base': pr['base']['sha'],
               'observed_utc': datetime.now(timezone.utc).isoformat()})
(out/'public-pr.json').write_text(json.dumps(prsafe, indent=2)+'\n')
reviews = api(f'repos/{repo}/pulls/171/reviews?per_page=100')
inline = api(f'repos/{repo}/pulls/171/comments?per_page=100')
(out/'public-review-surfaces.json').write_text(json.dumps({'reviews':reviews,'inline':inline},indent=2)+'\n')
print(f'{len(rows)} immutable public receipts verified against their published git blobs')
print(f'PR head: {prsafe["head"]}; submitted reviews: {len(reviews)}; inline comments: {len(inline)}')
