#!/usr/bin/env python3
"""Reconcile public round-seven receipts against the exact reviewed source."""
import hashlib, json, os, subprocess, sys
from pathlib import Path
root=Path(os.environ.get('CHECKOUT',os.getcwd())).resolve()
p=Path(__file__).resolve().parent
sys.path[:0]=[str(root/'scripts'),str(root/'ci/image')]
import audit_population as population
import ci_differential as differential
import build
def read(path): return json.loads(path.read_text())
def git(*args): return subprocess.check_output(['git',*args],cwd=root,text=True).strip()
head=git('rev-parse','HEAD'); image=read(root/'ci/image/image.lock.json')
r=read(root/'ci/image/exec-audit-receipt.json')
reached=population.reached_steps(root)
keys={f"{s['workflow']}#{s['job']}#{s['index']}" for s in reached}
assert keys=={s['step'] for s in r['reconciliation']}
assert len(keys)==98 and len(r['steps'])==94
assert {s['step'] for s in r['steps']}=={s['step'] for s in r['reconciliation'] if s['traced']}
assert all(s['exit_status']==0 and not s['findings'] and s['clean'] for s in r['steps'])
assert r['image']==image['image_digest']
assert r['source']['tree']==git('rev-parse',r['source']['commit']+'^{tree}')
for s,row in zip(reached,r['reconciliation']):
 text,reason,removed=population.image_form(s['name'],s['run'])
 assert row['text_sha256']==hashlib.sha256((text or '').encode()).hexdigest()
 assert row['image_form']==reason and row['removed']==removed
assert len(r['commands'])==115 and all(x['instances'] for x in r['commands'])
author=p/'scratch/public/author-r7'
cold=[read(author/f'round7-cold-build-{k}.receipt.json') for k in 'ab']
for c in cold:
 assert c['image_digest']==image['image_digest'] and c['recipe_sha256']==build.recipe_digest()
 assert c['size_bytes']==3930997226
assert all(cold[0][k]==cold[1][k] for k in cold[0] if k!='build_ms')
summary=read(author/'round7-population-receipt.json')
assert summary['committed_receipt']['sha256']==hashlib.sha256((root/'ci/image/exec-audit-receipt.json').read_bytes()).hexdigest()
assert summary['instances']==sum(s['instances'] for s in r['steps'])==183845
retraced=read(author/'round7-head-retrace-docs-check.json')
assert retraced['source']['commit']==head and retraced['image']==image['image_digest']
assert len(retraced['steps'])==46 and all(s['clean'] and s['exit_status']==0 for s in retraced['steps'])
checks=read(author/'round7-final-checks.json')
assert checks['head']==head and len(checks['checks'])==26 and all(c['rc']==0 for c in checks['checks'])
census=read(root/'ci/image/syntax-census.json')['shapes']
diff=read(root/'ci/image/differential-receipt.json')
assert len(census)==177 and len(diff['fixtures'])==188
assert diff['binding']==differential.binding(read(root/'ci/image/syntax-census.json'))
assert all(v['expect']==v['outcome'] for v in diff['fixtures'].values())
prior={k:{'outcome':v['outcome'],'refusal':v['refusal'],'statuses':v['statuses'],'real_count':len(v['real'])} for k,v in diff['fixtures'].items() if k.startswith(('R638-6-','R639-6-'))}
table=read(root/'ci/image/command-table.json')
pin=hashlib.sha256((root/'scripts/check_baremetal_only.py').read_bytes()).hexdigest()
assert pin==table['scripts']['scripts/check_baremetal_only.py']['sha256']
old=json.loads(git('show','6918d4f9:ci/image/tool-inventory.json'))
inventory=read(root/'ci/image/tool-inventory.json')
old_lock=json.loads(git('show','6918d4f9:ci/image/image.lock.json'))
print('inventory keys',inventory.keys(),'lock keys',image.keys())
source_changes=set(git('diff','--name-only','fa7347fc..HEAD').splitlines())
dev_changes=set(git('diff','--name-only','fa7347fc..84f9e3001b7d9b77835c4a9a599dbe6230a8031b').splitlines())
merge=subprocess.run(['git','merge-tree','--write-tree','84f9e3001b7d9b77835c4a9a599dbe6230a8031b',head],cwd=root,capture_output=True,text=True)
report={'head':head,'source_tree':git('rev-parse','HEAD^{tree}'),'image_digest':image['image_digest'],'recipe':build.recipe_digest(),'cold_builds':cold,'baremetal_declaration_sha256':pin,'differential_tools':diff['tools'],'census_shapes':len(census),'fixtures':len(diff['fixtures']),'prior_probe_receipts':prior,'population':{'source':r['source']['commit'],'reached':98,'traced':94,'instances':183845,'exit_nonzero':0,'findings':0,'omitted':[s for s in r['reconciliation'] if not s['traced']],'commands':115,'argument_differences':summary['argument_differences']},'head_retrace_docs':{'steps':46,'clean':True},'head_retrace_all_author_comparison':read(author/'round7-head-retrace-comparison.json'),'final_checks':checks,'merge_shape':{'base':'84f9e3001b7d9b77835c4a9a599dbe6230a8031b','overlap':sorted(source_changes & dev_changes),'rc':merge.returncode,'tree':merge.stdout.strip(),'validation':'shape only; no candidate banks run'}}
for k in ['tools','residue']:
 report[k+'_equal_round6']=old.get(k)==inventory.get(k)
report['tool_records']=len(inventory.get('tools',[]))
report['residue_delta']={'before':len(old['residue']),'after':len(inventory['residue']),
 'added':sorted(set(inventory['residue'])-set(old['residue'])),
 'removed':sorted(set(old['residue'])-set(inventory['residue']))}
report['payload_layers_changed']=[a['tool'] for a,b in zip(image['layers'],old_lock['layers']) if a['oci_digest']!=b['oci_digest']]
smoke=[]
for line in (author/'round7-image-smoke.log').read_text().splitlines():
 try: entry=json.loads(line)
 except ValueError: continue
 if isinstance(entry,dict): smoke.append(entry)
report['smoke']={'json_records':len(smoke),'command_records':sum('rc' in e for e in smoke),
 'nonzero':sum(e.get('rc',0)!=0 for e in smoke),'final_line':(author/'round7-image-smoke.log').read_text().splitlines()[-1]}
(p/'receipt-reconciliation.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS receipt reconciliation')
