#!/usr/bin/env python3
"""Collect the four published portability receipts and prove their tree."""
import argparse, concurrent.futures, hashlib, io, json, re, subprocess, zipfile
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);a=ap.parse_args();p=a.packet.resolve()
api='repos/kebag-logic/milan-fpga/';run=37964014621
def get(path):return subprocess.check_output(['gh','api','--allow-escape-sequences',api+path])
artifacts=json.loads(get(f'actions/runs/{run}/artifacts'))['artifacts']
items=[v for v in artifacts if v['name'].startswith('yosys-results-')];assert len(items)==4
def fetch(v):
 raw=get('actions/artifacts/'+str(v['id'])+'/zip');z=zipfile.ZipFile(io.BytesIO(raw));out=p/'receipts/hosted-artifacts'/v['name'];out.mkdir(parents=True,exist_ok=True)
 files=[]
 for name in z.namelist():
  if name.endswith('/'):continue
  assert Path(name).name==name,name
  data=z.read(name);(out/name).write_bytes(data);files.append({'name':name,'sha256':hashlib.sha256(data).hexdigest()})
 return {'id':v['id'],'name':v['name'],'files':files}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(fetch,items))
jobs=json.loads(get(f'actions/runs/{run}/jobs?per_page=100'))['jobs']
ys=[j for j in jobs if j['name'].startswith('Yosys shard')];assert len(ys)==4
def logs(j):
 raw=get('actions/jobs/'+str(j['id'])+'/logs').decode()
 # Retain result and checkout lines only; omit hosted machine paths and setup identities.
 lines=[x for x in raw.splitlines() if re.search(r'HEAD is now at|\[PASS\].*cells=|RESULT:|TAP-PURITY RESULT:|target_sha=',x) and not '\x1b' in x]
 (p/'receipts'/('hosted-yosys-'+str(j['id'])+'.log')).write_text('\n'.join(lines)+'\n')
 return {'job':j['name'],'id':j['id'],'conclusion':j['conclusion'],'pass_records':len(re.findall(r'\[PASS\].*cells=',raw)),'cached_records':len(re.findall(r'\[PASS\].*cells=.*\(result cache\)',raw))}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:workers=list(pool.map(logs,ys))
sha='21a40e975a5e37453dd8089f80d5ea1b681eddc1';c=json.loads(get('git/commits/'+sha))
assert c['tree']['sha']=='6bdddb24ad611a450350c00131f64468631b889b'
assert [x['sha'] for x in c['parents']]==['5603c353137e90c1fa95429f6d00ef7a2298d9ee','614b4aa5f408d75673b546ce6efb6ef126437be2']
assert sum(x['pass_records'] for x in workers)==58
result={'workflow_run':run,'synthetic_merge':sha,'parents':[x['sha'] for x in c['parents']],'tree':c['tree']['sha'],'source_tree_equal':True,'workers':workers,'artifacts':rows}
(p/'receipts/hosted-tree-proof.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='artifacts'},indent=2))
