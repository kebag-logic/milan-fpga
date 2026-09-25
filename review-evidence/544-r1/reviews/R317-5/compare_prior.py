#!/usr/bin/env python3
"""Read published round-2 verdicts and compare unchanged probe runs.
Uses only read-only API calls. No prior r2e compiler-free receipt exists.
"""
import hashlib,json,subprocess,sys
from pathlib import Path
p=Path(sys.argv[1]);out=[]
ref='4c97887dc83f46703b8d767dec671afcb9ebe206'
for tag in ('r2','r2b','r2c','r2d','r2e'):
 for mode in ('sdk','absent'):
  if (tag,mode)==('r2e','absent'):continue
  src=f'review-evidence/544-r1/reviews/R317-2/receipts/probes-r2/{tag}-head-{mode}.json'
  b=subprocess.check_output(['gh','api','-H','Accept: application/vnd.github.raw+json',f'repos/kebag-logic/milan-fpga/contents/{src}?ref={ref}'])
  prior=json.loads(b)['rows'];now=json.loads((p/f'receipts/cases_544_{tag}-{mode}.json').read_text())['rows']
  assert [x['label'] for x in prior]==[x['label'] for x in now]
  delta=[{'label':x['label'],'old':x['verdict'],'new':y['verdict'],'new_reason':y.get('reason')} for x,y in zip(prior,now) if x['verdict']!=y['verdict']]
  out.append({'source':src,'sha256':hashlib.sha256(b).hexdigest(),'mode':mode,'rows':len(now),'delta':delta})
for mode in ('sdk','absent'):
 src=f'review-evidence/544-r1/reviews/R316-2/receipts/r2set-head-{mode}.json'
 b=subprocess.check_output(['gh','api','-H','Accept: application/vnd.github.raw+json',f'repos/kebag-logic/milan-fpga/contents/{src}?ref={ref}'])
 prior=json.loads(b)['results'];now=json.loads((p/f'receipts/probe2-{mode}.json').read_text())['results']
 assert [x['id'] for x in prior]==[x['id'] for x in now]
 delta=[{'id':x['id'],'old':x['verdict'],'new':y['verdict'],'new_reason':y.get('reason')} for x,y in zip(prior,now) if x['verdict']!=y['verdict']]
 out.append({'source':src,'sha256':hashlib.sha256(b).hexdigest(),'mode':mode,'rows':len(now),'delta':delta})
assert all(not x['delta'] for x in out if x['mode']=='absent')
for x in out:
 for d in x['delta']:assert d['old']=='ACCEPTED' and d['new']=='REFUSED' and 'boot-unit asm allowlist rule' in d['new_reason']
(p/'round2-comparison.json').write_text(json.dumps(out,indent=2)+'\n')
print('Compared',sum(x['rows'] for x in out),'published head verdicts; every available absent result unchanged')
for x in out:
 if x['delta']:print(x['source'],x['delta'])
