#!/usr/bin/env python3
"""R575-2: check the page's Evidence-section identity claims against the archive.
Usage: check_evidence_identity.py <archive-root review-evidence/608-b14-r1>"""
import hashlib, json, sys, os
root = sys.argv[1]
a = os.path.join(root, 'author')
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
print('MANIFEST.sha256', sha(os.path.join(a,'MANIFEST.sha256')))
print('RAW-ARTIFACTS.json', sha(os.path.join(a,'RAW-ARTIFACTS.json')))
print('MANIFEST.json', sha(os.path.join(root,'MANIFEST.json')))
m = json.load(open(os.path.join(root,'MANIFEST.json')))
print('MANIFEST.json entries', len(m))
print('path_redacted True', sum(1 for e in m if e['path_redacted']))
print('original!=published', sum(1 for e in m if e['original_sha256']!=e['published_sha256']))
for e in m:
    if e['file']=='author/raw-index/soak.jsonl': print('soak.jsonl manifest', e)
# every manifest file present with its published digest
bad=0
for e in m:
    p=os.path.join(root,e['file'])
    if not os.path.exists(p) or sha(p)!=e['published_sha256']: bad+=1
print('manifest published digest mismatches', bad)
# MANIFEST.sha256 self-check
bad=0;n=0
for line in open(os.path.join(a,'MANIFEST.sha256')):
    if line.startswith('#') or not line.strip(): continue
    h,f=line.rstrip('\n').split('  ',1); n+=1
    p=os.path.join(a,f)
    if not os.path.exists(p) or sha(p)!=h: bad+=1
print('MANIFEST.sha256 entries',n,'mismatches',bad)
orig={e['file'][len('author/'):]:e['original_sha256'] for e in m}
for line in open(os.path.join(a,'MANIFEST.sha256')):
    if line.startswith('#') or not line.strip(): continue
    h,f=line.rstrip('\n').split('  ',1)
    if sha(os.path.join(a,f))!=h: print('  mismatch',f,'equals the pre-redaction digest in MANIFEST.json:',orig.get(f)==h)
# capture counts per group
for g in ('item2','item3','item4','soak','other'):
    rows=[json.loads(l) for l in open(os.path.join(a,'raw-index',g+'.jsonl')) if l.strip()]
    caps=[r for r in rows if str(r['path']).endswith(('.pcap','.pcapng'))]
    print(g,'rows',len(rows),'captures',len(caps),'capture bytes',sum(int(r['bytes']) for r in caps), 'keys', sorted(rows[0].keys()))
