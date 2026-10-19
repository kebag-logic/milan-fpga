#!/usr/bin/env python3
"""Reconcile publication hashes, index entries and retained gate outcomes."""
import hashlib
import json
from pathlib import Path
import re
import sys

packet=Path(sys.argv[1]); dest=packet/'scratch/public-evidence'
manifest=json.loads((dest/'MANIFEST.json').read_text()); by={r['file']:r for r in manifest}
rows=re.findall(r'^\| `([^`]+)` \| (\d+) \| ([a-f0-9]+) \|',
                (dest/'author/receipts/INDEX.md').read_text(),re.M)
results=[]
for rel,size,sha in rows:
    row=by['author/'+rel]; data=(dest/'author'/rel).read_bytes()
    digest=hashlib.sha256(data).hexdigest()
    assert digest==row['published_sha256']
    assert row['original_sha256'].startswith(sha)
    if not row['path_redacted']:assert len(data)==int(size) and digest.startswith(sha)
    results.append({'file':rel,'original_hash_matches':True,'published_hash_matches':True,
        'path_redaction':row['path_redacted'],'index_bytes':int(size),'published_bytes':len(data)})
assert {'author/'+r[0] for r in rows}==set(by)-{'author/receipts/INDEX.md'}
(packet/'receipts/index-audit.json').write_text(json.dumps(results,indent=2)+'\n')
out=[]
for bucket in ['gates/base','gates/head','campaigns/base','campaigns/head',
               'campaigns/head-bacfb90','consumers/base','consumers/head',
               'consumers/ooc-base','consumers/ooc-head']:
    for path in sorted((dest/'author/receipts'/bucket).glob('*.rc')):
        out.append({'record':str(path.relative_to(dest)), 'rc':int(path.read_text())})
(packet/'receipts/author-return-codes.json').write_text(json.dumps(out,indent=2)+'\n')
print(f'PASS: {len(manifest)} published files, {len(rows)} indexed files; '
      f'{sum(r["path_redaction"] for r in results)} declared path redactions')
