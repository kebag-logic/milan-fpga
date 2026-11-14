#!/usr/bin/env python3
"""Check post-scrub public receipt indexes; argument: extracted evidence root."""
from pathlib import Path
import hashlib
import re
import sys
root=Path(sys.argv[1])
for round_name in ('author-r2','author-r5'):
    base=root/round_name/'receipts'
    count=0
    mismatches=[]
    directory=None
    for line in (base/'INDEX.md').read_text().splitlines():
        if line.startswith('## '):
            directory=line[3:].strip().strip('`')
        m=re.fullmatch(r'\| (.+) \| ([\d,]+) \| `([0-9a-f]{16,64})` \|',line)
        if m:
            name,size,digest=m.groups()
            path=base/name.strip('`') if round_name=='author-r2' else base/directory/name
            data=path.read_bytes()
            count+=1
            if len(data)!=int(size.replace(',','')) or not hashlib.sha256(data).hexdigest().startswith(digest):
                mismatches.append(str(path.relative_to(root))+' expected '+size+' bytes '+digest+'; actual '+str(len(data))+' bytes '+hashlib.sha256(data).hexdigest())
    print(round_name, count, 'entries;',len(mismatches),'mismatches')
    for name in mismatches: print('MISMATCH',name)
    assert count>0
    if round_name=='author-r5': current_bad=len(mismatches)
print('CURRENT INDEX MISMATCHES:',current_bad)
sys.exit(1 if current_bad else 0)
