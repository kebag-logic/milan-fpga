#!/usr/bin/env python3
"""Hash and summarize the exact public receipt set, without author handoff files."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

repo=Path(sys.argv[1]).resolve()
commit='8f1028e5a0fb979b3c6c33496655dd15059825eb'
prefix='review-evidence/773-r1/author/receipts/'
def blob(path):
    return subprocess.check_output(['git','-C',str(repo),'show',commit+':'+prefix+path])
index=blob('INDEX.md').decode()
rows=re.findall(r'^\| `([^`]+)` \| [0-9,]+ \| `([0-9a-f]{64})` \|$',index,re.M)
envelope=json.loads(subprocess.check_output(['git','-C',str(repo),'show',commit+':review-evidence/773-r1/MANIFEST.json']))
published={r['file']:r for r in envelope}
for path,digest in rows:
    item=published['author/receipts/'+path]
    assert item['original_sha256']==digest,path
    assert hashlib.sha256(blob(path)).hexdigest()==item['published_sha256'],path
print('Public evidence commit:',commit)
print('Verified published receipt hashes:',len(rows))
for path in ['sweep/shard-0/results.json','sweep/shard-1/results.json','sweep/shard-2/results.json','sweep/shard-3/results.json']:
    data=json.loads(blob('round1b/final/'+path))
    print(path,'head='+data['head'],'returncodes='+str([r['exit_code'] for r in data['results']]))
for path in ['sweep/aaf_alone_13d8f1e8/HEAD.txt','sweep/aaf_alone_13d8f1e8/rc','yosys/HEAD.txt','yosys/rc','xvlog/HEAD.txt','xvlog/rc','docs/nogit_summary.txt']:
    print(path,blob('round1b/final/'+path).decode().strip())
print('Only change between sweep head and reviewed head:')
print(subprocess.check_output(['git','-C',str(repo),'diff','--stat','bf2d96f9..13d8f1e8'],text=True))
for path in ['campaigns/tdm8render_mutants/log.txt','campaigns/gmstep/log.txt','campaigns/pullin/legs.txt','vivado/route-1x1/gate_check.log','vivado/ooc-1x1/gate_check.log','vivado/ooc-8x8/gate_check.log']:
    value=blob('round1b/final/'+path).decode()
    print('ARTIFACT:',path)
    for line in value.splitlines():
        if any(k in line for k in ['checks:', 'checks: ', 'RESULT:', 'WNS_ns','WHS_ns','SLICE','0 FAIL-lines']):
            print(line)
delta=subprocess.check_output(['git','-C',str(repo),'diff','a032c6d6..13d8f1e8','--','hdl','tb'],text=True)
bad=[]
for line in delta.splitlines():
    if line.startswith('+') and not line.startswith('+++') and re.search(r'//|^\+\s*#',line):
        if re.search(r'\bB\d+\b|\bR\d+(?:-\d+)?\b|issuecomment-|review round|bench lane',line):
            bad.append(line)
print('New source-comment prohibited provenance matches:',len(bad))
for line in bad: print(line)
