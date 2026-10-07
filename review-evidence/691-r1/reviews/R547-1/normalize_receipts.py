#!/usr/bin/env python3
"""Replace installation roots in publishable logs; preserve raw originals in scratch."""
import hashlib
import json
from pathlib import Path
import re

packet=Path(__file__).resolve().parent
rows=[]
pattern=re.compile(r"/[^ \t\r\n\"']+/diff/usr/share/verilator")
for path in sorted(packet.glob('*.log')):
    before=path.read_bytes()
    text=pattern.sub('$SIMULATOR_ROOT',before.decode())
    after=text.encode()
    if after==before:
        continue
    raw=packet/'scratch'/path.name
    rows.append({'file':path.name,'raw_scratch_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),
                 'published_sha256':hashlib.sha256(after).hexdigest(),
                 'change':'Installation-root path replaced by $SIMULATOR_ROOT; complete diagnostics and results retained'})
    path.write_bytes(after)
if rows:
    (packet/'receipt-normalization.json').write_text(json.dumps(rows,indent=2)+'\n')
print(f'PASS: {len(rows)} installation-root substitutions; raw originals remain in scratch')
