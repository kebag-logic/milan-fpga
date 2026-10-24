#!/usr/bin/env python3
"""Summarize hash-verified public gate receipts and retain selected originals."""
import json,re,shutil,sys
from pathlib import Path
packet=Path(sys.argv[1]).resolve()
root=packet/'scratch/public/author-r2/receipts/round2'
dest=packet/'published_receipts';dest.mkdir(exist_ok=True)
def retain(path):
    target=dest/path.relative_to(root);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,target)
summary={'shards':[]}
for shard in range(4):
    directory=root/f'sweep-c2a080ae/shard-{shard}/spec'
    result=json.loads((directory/'results.json').read_text())
    log=(directory/'01.log').read_text()
    tally=re.search(r'checks:\s*(\d+)\s+in-suite failures:\s*(\d+)',log)
    summary['shards'].append({'shard':shard,'head':result['head'],'rc':result['results'][0]['exit_code'],
        'suites':re.findall(r'^PASS\s+(\S+)',log,re.M),'checks':int(tally[1]),'failures':int(tally[2]),
        'skips':[line.strip() for line in log.splitlines() if 'SKIPPED' in line]})
    retain(directory/'results.json');retain(directory/'01.log')
docs=root/'docs-c2a080ae/receipts.json'; d=json.loads(docs.read_text());retain(docs)
summary['docs']={'head':d['head'],'head_after':d['head_after'],'steps':len(d['steps']),
                 'executed':sum(s['rc'] is not None for s in d['steps']),
                 'skipped':[s for s in d['steps'] if s['rc'] is None],
                 'rcs':sorted(set(s['rc'] for s in d['steps'] if s['rc'] is not None)),
                 'make_versions':sorted(set(s['make'] for s in d['steps'] if 'make' in s)),
                 'remaining_metadata':{k:v for k,v in d.items() if k not in ('head','head_after','steps')}}
summary['suites']=sum(len(s['suites']) for s in summary['shards'])
summary['checks']=sum(s['checks'] for s in summary['shards'])
for rel in ['static-c2a080ae/HEAD.txt','static-c2a080ae/gates.tsv','static-c2a080ae/lint_rtl.log',
            'rtl-comment-only/comment-only.txt','probe_lock_settle/SUMMARY.txt','probes/SUMMARY.txt',
            'suites-c2a080ae/env.txt','suites-c2a080ae/avtp_rxmon.log']:
    p=root/rel
    if p.exists():retain(p)
(packet/'public_gate_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
