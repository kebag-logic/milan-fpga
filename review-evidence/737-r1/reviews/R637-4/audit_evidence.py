#!/usr/bin/env python3
"""Recheck public exact-head receipts and measured workflow arithmetic."""
import copy,hashlib,json,pathlib,subprocess,sys
from datetime import datetime
root=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(root/'scripts'))
import ci_builder_legs as b
from ci_gate_workflows import load_template,case_inventory,worker_id,worker_legs
from ci_gate_receipts import Collected,StepContext,record,verify
p=out/'scratch/public/author-r4';read=lambda name:json.loads((p/name).read_text())
head='08adb21af0a72d839ce30b6c461503dad269d4d6';tree='e5cc5d163c974aaf1b6cb888dae9881267d787e6'
r=read('round4-s3-receipt-f-e1-unsharded.json');legs=[read('round4-s3-receipt-f-e'+s+'.json') for s in ['2-leg0','3-leg1']]
result=b.compare(r,legs,head,tree);names=b.inventory()
# Independent equality check, including exact per-gate rows and order.
rows={x['gate']:x for leg in legs for x in leg['driver']['gates']}
assert len(rows)==103 and [rows[n] for n in names]==r['driver']['gates']
assert [item for n in names for item in rows[n]['not_run']]==result['not_run']
source=load_template(root,'elaborate');cases=case_inventory('elaborate',source)
digest=hashlib.sha256((root/'.github/ci-templates/elaborate.yml').read_bytes()).hexdigest()
actual={c['id']:{'outcome':'success','conclusion':'success'} for c in cases}
receipts=[record('elaborate',n,source,(head,tree),digest,StepContext(actual,'true')) for n in worker_legs('elaborate',source)]
needs={worker_id('elaborate',n):{'result':'success'} for n in worker_legs('elaborate',source)}
assert verify('elaborate',source,(head,tree),digest,Collected(receipts,legs),needs)==[c['id'] for c in cases]
# Explicit non-flag leg refusal with otherwise complete, equal real observations.
changed=copy.deepcopy(legs);changed[1]['driver']['requirements'].remove('--require-elaboration');changed[1]['driver']['require_elaboration']=None
try:b.union(changed,head,tree)
except ValueError as e:refusal=str(e);assert 'test_every_recipe_elaborates' in refusal and 'without the flag' in refusal
else:raise AssertionError('non-flag elaboration leg accepted')
published=read('round4-s3-equality.json');final=published['final_head'];assert final['head']==head
for run in final['runs'].values():
 assert run['source']['run_head']==head and run['source']['tree']==tree and run['returncode']==0
 assert all(int(v)==0 for v in run['memory_events'].values())
base=read('baseline-elaborate.json')['jobs'][0]
def seconds(row):return (datetime.fromisoformat(row['completed_at'])-datetime.fromisoformat(row['started_at'])).total_seconds()
windows={r['name']:seconds(r) for r in base['steps']}
assert seconds(base)==2144 and windows['Elaboration gates']==1441 and windows['Standalone LiteX simulation aggregate']==593
scale=1441/1292.671
scaled=[round(published['runs'][k]['seconds']*scale) for k in ['e2-leg0','e3-leg1']]
assert scaled==[1146,409]
workers=[2144-593-3-1441+scaled[0]+60,2144-1441+scaled[1]+60]
assert workers==[1313,1172] and all(t<=45*60*.6 for t in workers) and max(workers)+270==1583
summary={'head':head,'tree':tree,'per_gate_rows_equal':103,'leg_sizes':[len(l['driver']['gates']) for l in legs],
 'not_run_rows_equal':len(result['not_run']),'not_run_gate_ids':[r[0] for r in result['not_run']],
 'production_union':'PASS','production_aggregate':'PASS (synthetic successful step contexts with real published builder receipts)',
 'nonflag_leg_refusal':refusal,'published_receipt_verdict_digest':result['verdicts_sha256'],
 'original_execution_verdict_digest':final['comparison']['verdicts_sha256'],
 'digest_note':'Public receipts redact the calibration path; public-byte digest differs from the original execution digest. Equality was rerun on published bytes, not claimed to reproduce the original byte digest.',
 'author_execution_seconds':{k:v['seconds'] for k,v in final['runs'].items()},
 'author_image':published['image'],'baseline_run':38495894212,'baseline_seconds':2144,'baseline_builder_seconds':1441,'scale':scale,
 'projected_workers_seconds':workers,'worker_bound_seconds':1620,'margins_seconds':[1620-t for t in workers],
 'projected_workflow_seconds':1583,'projected_workflow_minutes':1583/60,
 'limits':'No full builder bank or shipping image was executed by this reviewer. Timing is a projection, not exact-head hosted evidence.'}
(out/'public-evidence-audit.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
