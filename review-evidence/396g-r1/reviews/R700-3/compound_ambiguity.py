#!/usr/bin/env python3
"""Prove the two ambiguous compound captures equal their reported alternatives."""
import hashlib
import json
from pathlib import Path
import sys

out=Path(__file__).resolve().parent
exec((out/'delta_probes.py').read_text().split('rows=[]')[0])
rows=[]
for mask,alternative in [(0x100,[('shift',3005,4096)]),
                         (0x80000,[('shift',3001,-1024),('shift',3002,5120)])]:
    raw=capture([('shift',3000,4096),('xor',3001,1,2,mask)])
    other=bytearray(capture([('shift',3000,4096)]))
    column=capture(alternative)
    for i in range(N):
        other[16*i+8:16*i+12]=column[16*i+8:16*i+12]
    rows.append(dict(mask=hex(mask),original=[['shift',3000,4096],['xor',3001,1,2,mask]],
                     channel2_alternative=alternative,equal=raw==other,
                     original_sha256=hashlib.sha256(raw).hexdigest(),
                     alternative_sha256=hashlib.sha256(other).hexdigest()))
(out/'compound-ambiguity.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
assert all(r['equal'] for r in rows)
