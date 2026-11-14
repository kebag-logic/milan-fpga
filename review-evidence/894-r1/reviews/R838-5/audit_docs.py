#!/usr/bin/env python3
"""Check the published index, workflow step table, and current row cells."""
from pathlib import Path
import hashlib
import json
import re
import sys

repo, packet = (Path(x).resolve() for x in sys.argv[1:3])
a = packet/'scratch/review-evidence/894-r1/author-r10'
rows = re.findall(r'^\| `([^`]+)` \| ([\d,]+) \| `([0-9a-f]{64})` \|$', (a/'INDEX.md').read_text(), re.M)
bad = [{'path':n,'listed_bytes':int(s.replace(',','')),'actual_bytes':len((a/n).read_bytes()),
        'listed_sha256':h,'actual_sha256':hashlib.sha256((a/n).read_bytes()).hexdigest()}
       for n,s,h in rows if len((a/n).read_bytes())!=int(s.replace(',','')) or hashlib.sha256((a/n).read_bytes()).hexdigest()!=h]
counts = {}
for line in (a/'receipts/gates/workflows-verify.md').read_text().splitlines():
    if not line.startswith('| ') or line.startswith('| Workflow'):
        continue
    fields = [x.strip() for x in line.strip('|').split('|')]
    assert len(fields)==6 and fields[4] in ('0','NOT RUN') and fields[5]
    counts[fields[4]] = counts.get(fields[4],0)+1
assert counts=={'0':139,'NOT RUN':226}
doc = (repo/'docs/design/SPLIT_CONTROL_MEMORY.md').read_text()
tables=[]
for point,log in [('1x1/1if','flip-1x1.log'),('8x8/2if','flip-8x8.log')]:
    values={}
    for line in (packet/log).read_text().splitlines():
        f=[x.strip() for x in line.strip('|').split('|')]
        if len(f)>=3 and f[0]==point:
            values[f[1]]=f[2]
    expected=[values[x] for x in ('R4','R5','R6','first','last')]
    lines=[l for l in doc.splitlines() if l.startswith('| '+point+' |') and all(v in l for v in expected)]
    assert len(lines)==1
    cells=[c.strip() for c in lines[0].strip('|').split('|')][2:]
    actual=[re.match(r'\d+\.\d+',c).group() for c in cells]
    assert actual==expected
    tables.append({'point':point,'grader_values':expected,'document_values':actual})
assert 'under the tiers every 1x1/1if row holds by every source, R4 12.85 ms' in doc
out={'index_entries':len(rows),'index_mismatches':bad,'workflow_statuses':counts,'table':tables,'summary_R4':'12.85'}
(packet/'docs-and-receipts.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
