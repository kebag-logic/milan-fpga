#!/usr/bin/env python3
"""Compare public operands without importing any packet comparison code.

Usage: python3 independent_compare.py EXTRACTED_S13_ROOT
"""
import gzip
import hashlib
import json
import lzma
import re
import sys
from pathlib import Path

archive = Path(sys.argv[1])
root = archive / 'author-r3/receipts/identity'
sha = lambda b: hashlib.sha256(b).hexdigest()

def unpack(p):
    b = p.read_bytes()
    return lzma.decompress(b) if p.suffix == '.xz' else gzip.decompress(b)

def manifest(p):
    return {n: h for h, n in (line.split(None, 1) for line in p.read_text().splitlines())}

listed = manifest(root / 'MANIFEST.sha256')
assert len(listed) == 230
assert set(listed) == {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()} - {'MANIFEST.sha256'}
for n,h in listed.items():
    assert sha((root/n).read_bytes()) == h, n
print('PASS exact manifest population and bytes: 230 entries')
content = manifest(root/'MANIFEST.content.sha256')
for n,h in content.items():
    assert sha(unpack(root/n)) == h, n
print('PASS decompressed content manifest:',len(content))
pub = json.loads((archive/'MANIFEST.json').read_text())
rows = [r for r in pub if r['file'].startswith('author-r3/receipts/')]
for r in rows:
    assert sha((archive/r['file']).read_bytes()) == r['published_sha256'], r['file']
print('PASS archive published hashes:',len(rows))
old = manifest(archive/'author-r2/receipts/identity/MANIFEST.sha256')
binding = json.loads((root/'binding.json').read_text())
assert len(binding['reencoded']) == 5
for row in binding['reencoded']:
    n=row['path']; b=unpack(root/n)
    assert row['round2_sha256'] == old[n]
    assert row['sha256'] == listed[n]
    assert row['content_sha256'] == content[n] == sha(b)
    # The old packer copied measured gzip files; their header metadata and
    # compressor version cannot be inferred from a decompressed stream.
    # Bind the old published digest to the explicit re-encoding provenance.
    print('PASS REENCODE BINDING',n,'old',old[n],'content',sha(b))
    if n.endswith('.xz'):
        assert sha(lzma.compress(b,preset=9))==old[n]
        print('PASS old xz bytes independently reconstructed')

for shape, count, nets, wantbits, wantcells in [('1x1',86465,95172,22,8),('8x8',109093,119085,15,14)]:
    d=root/'shipping'/shape/'dump'
    a=unpack(d/'bench.cells.xz').decode().splitlines()
    b=unpack(d/'flip.cells.xz').decode().splitlines()
    assert len(a)==len(b)==count
    changed=[]; total=0
    for x,y in zip(a,b):
        if x==y: continue
        tx,ty=x.split(),y.split()
        assert len(tx)==len(ty)
        bits=0
        for u,v in zip(tx,ty):
            if u==v: continue
            pat=r'(INIT[A-Z_0-9]*)=(\d+)\x27h([0-9A-Fa-f]+)'
            p,q=re.fullmatch(pat,u),re.fullmatch(pat,v)
            assert p and q and p.group(1,2)==q.group(1,2),(u,v)
            bits+=(int(p[3],16)^int(q[3],16)).bit_count()
        assert tx[:4]==ty[:4] and tx[1].startswith('RAMB')
        assert '/csr/' in tx[0] or 'rom_bank' in tx[0]
        changed.append((tx[0],bits));total+=bits
    assert (total,len(changed))==(wantbits,wantcells)
    na,nb=unpack(d/'bench.nets.xz'),unpack(d/'flip.nets.xz')
    assert na==nb and len(na.splitlines())==nets
    print('PASS',shape,'cells',count,'routes',nets,'INIT bits',total,'changed cells',changed)

groups=list(sorted((root/'groups').glob('*/*/*.measured.json')))
assert len(groups)==13
for p in groups:
    q=p.with_name(p.name.replace('.measured.','.head.'))
    # Exact JSON bytes is stronger than ignoring any leaf or field.
    assert p.read_bytes()==q.read_bytes(),p
    a=unpack(p.with_name(p.name.replace('.json','.log.gz'))).decode().splitlines()
    b=unpack(q.with_name(q.name.replace('.json','.log.gz'))).decode().splitlines()
    assert len(a)==len(b)
    diff=[]
    for i,(x,y) in enumerate(zip(a,b),1):
        if x==y: continue
        tx,ty=x.split(),y.split()
        if tx[0]=='WIRE':
            assert tx[:-1]==ty[:-1]
            bx,by=bytes.fromhex(tx[-1]),bytes.fromhex(ty[-1])
        else:
            assert tx[0]=='PASS' and 'W' in tx
            k=tx.index('W'); assert tx[:k+1]==ty[:k+1]
            wx=[t.split(':') for t in tx[k+1:]];wy=[t.split(':') for t in ty[k+1:]]
            assert [w[:2] for w in wx]==[w[:2] for w in wy]
            bx=b''.join(int(w[2],16).to_bytes(4,'little') for w in wx)
            by=b''.join(int(w[2],16).to_bytes(4,'little') for w in wy)
        assert bx.count(b'2.96.0\0')==1 and by.count(b'3.96.0\0')==1
        assert bx.replace(b'2.96.0\0',b'3.96.0\0')==by
        diff.append((i,tx[0],bx.index(b'2.96.0\0')))
    print('PASS GROUP',p.relative_to(root),'JSON byte-identical; raw lines',len(a),'version-only differences',diff)
print('PASS independent public-operand comparison complete')
