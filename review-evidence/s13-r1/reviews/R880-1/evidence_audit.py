#!/usr/bin/env python3
"""Audit the public evidence inventory and reported bit deltas; does not recreate absent binaries."""
import hashlib
import json
from pathlib import Path
import re
import sys
root=Path(sys.argv[1])
manifest=json.loads((root/'MANIFEST.json').read_text())
for item in manifest:
 path=root/item['file']
 assert hashlib.sha256(path.read_bytes()).hexdigest()==item['published_sha256'],item['file']
print('PASS public manifest hashes:',len(manifest))
r=root/'author-r1/receipts'
for shape, total in [('1x1',22),('8x8',15)]:
 text=(r/f'identity/{shape}/bitstream-bitdiff.txt').read_text()
 heads=[int(x) for x in re.findall(r'header\s+offset\s+(\d+)',text)]
 # The two rendered design-name strings contain SW_CRC and SW_HDR_SHA256.
 strings=[x for x in text.splitlines() if x.startswith('alinx_ax7101;')]
 assert len(strings)==2 and len(strings[0])==len(strings[1])
 changed=sum(a!=b for a,b in zip(*strings))
 other=[x for x in heads if x>155]
 bits=sum(map(int,re.findall(r'^\s+frame\s+\d+:.*?, (\d+) bit\(s\)',text,re.M)))
 assert bits==total
 print(shape,'reported header differing bytes',len(heads),'rendered design-name differences',changed,
       'other header offsets',other,'frame changed bits',bits)
 assert len(heads)==changed+len(other)
 for p in sorted((r/f'identity/{shape}').glob('signoff-*.txt')):
  corners=re.findall(r'^(\w+): WNS ([+-][\d.]+) ns \(0 failing\), WHS ([+-][\d.]+) ns \(0 failing\)',p.read_text(),re.M)
  assert len(corners)==4
  print(shape,p.stem,'floor',all(float(a)>=.030 and float(b)>=0 for _,a,b in corners))
text=(r/'budget/harness-images-vs-measured.txt').read_text()
assert text.count('loaded bytes differing: 6')==16
assert text.count('parts.json identical')==16
print('PASS receipt inventory: 16 arm comparisons, each reports six changed loaded bytes and unchanged partition')
text=(r/'budget/descriptor-groups-remeasured.txt').read_text()
assert len(re.findall(r'^.*probes, IDENTICAL$',text,re.M))==13
print('PASS receipt inventory: 13 descriptor/control groups reported identical')
files=[p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()]
missing_types={ext:sum(p.endswith(ext) for p in files) for ext in ('.bit','.elf','.init','.dcp','.cells','.nets','.bram')}
print('Public comparison input counts:',json.dumps(missing_types,sort_keys=True))
print('Subset comparison driver hcompare2.py present:',any(p.endswith('/hcompare2.py') for p in files))
print('Subset driver hsubset.sh present:',any(p.endswith('/hsubset.sh') for p in files))
print('LIMIT: this audit validates reported arithmetic and inventory, not the absent binary inputs or result leaves')
