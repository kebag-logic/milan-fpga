#!/usr/bin/env python3
"""Collect completed raw native logs and compare all frame bytes without masking."""
import collections
import gzip
import hashlib
import json
import shutil
import sys
from pathlib import Path
packet=Path(sys.argv[1]).resolve()
summaries=[]
def observable(log):
    wire=[]
    pub=collections.defaultdict(list)
    txc=collections.Counter()
    for line in log.splitlines():
        if line.startswith('WIRE '):
            fields=line.split()
            wire.append(tuple(fields[2:]))
        elif line.startswith('PASS ') and ' W ' in line:
            for word in line.split(' W ',1)[1].split():
                parts=word.split(':')
                if len(parts)==3 and 0x200<=int(parts[1],16)<0x280:
                    pub[parts[1]].append(parts[2])
        elif line.startswith('TXC '):
            txc[line.split()[2]]+=1
    return wire,dict(pub),dict(txc)
for arm in ('ap','do','1x1'):
    pair=[]
    for side in ('base','head'):
        label=f'native-{side}-{arm}'
        results=packet/'scratch'/label/'results'
        if side=='base':
            record=json.loads((packet/f'{label}-results.json').read_text())
        else:
            record=json.loads((results/'results.json').read_text())
            (packet/f'{label}-results.json').write_text(json.dumps(record,indent=2)+'\n')
        assert not record['refusals'] and not record['misses']
        raw=(results/'aecp-largest-notice.log').read_bytes()
        assert raw.rstrip().endswith(b'RESULT: PASS')
        (packet/f'{label}.log.gz').write_bytes(gzip.compress(raw,mtime=0))
        shutil.copy2(results/'aecp-largest-notice.txt',packet/f'{label}-stimulus.txt')
        measured=record['results'][0]
        share=measured['passes']['share']
        probes={p['probe']:(p.get('status'),p.get('within_budget'),p.get('within_ceiling')) for p in measured['probes']}
        summary=dict(run=label,passes=share['passes'],over=share['over'],
                     longest=measured['passes']['worst']['cycles'],raw_sha256=hashlib.sha256(raw).hexdigest(),
                     strict_verdict_rc=1 if share['over'] else 0)
        summaries.append(summary)
        pair.append((observable(raw.decode()),probes))
    assert pair[0]==pair[1],arm
    summaries.append(dict(pair=arm,wire_publications_txc_and_probe_verdicts_identical=True,
                          frames=len(pair[0][0][0]),masked_frame_fields=0))
(packet/'native-summary.json').write_text(json.dumps(summaries,indent=2)+'\n')
print(json.dumps(summaries,indent=2))
