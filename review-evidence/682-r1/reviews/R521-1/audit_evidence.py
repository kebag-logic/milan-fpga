#!/usr/bin/env python3
"""Reconstruct pin-revert and cross-check public receipts without private files."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT=Path.cwd();PACKET=Path(__file__).resolve().parent
HEAD='5428b044176f95248e6916dc00dd89c0df154078'
BASE='e21c1ca024d37ea188ad15b5c8f9c2dae18628df'
EVIDENCE='8d4e0732588d09f1f94f41aea7c7c39110da09a2'
PREFIX='review-evidence/682-r1/'
def git(*args,extra=None):
    return subprocess.check_output(['git',*args],env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')|(extra or {}))
def raw(path):return git('show',EVIDENCE+':'+PREFIX+path)
def read(name):return json.loads(raw('author/'+name))
def sha(data):return hashlib.sha256(data).hexdigest()

out={'head':HEAD,'evidence_commit':EVIDENCE}
manifest=json.loads(raw('MANIFEST.json'))
assert isinstance(manifest,list)
for row in manifest:
    assert sha(raw(row['file']))==row['published_sha256'],row['file']
out['public_payload_hashes_verified']=len(manifest)

diff=read('round2-render-differential.json')
adopt=diff['records']['adopted'];prior=diff['records']['prior']
measured=adopt['context']['head']
with tempfile.TemporaryDirectory(dir=PACKET/'scratch',prefix='render-index-') as tmp:
    env={'GIT_INDEX_FILE':str(Path(tmp)/'index')}
    git('read-tree',measured,extra=env)
    for patch in ('parent-adoption-148-6c22d3ca.patch','parent-adoption-22-28f9666f.patch'):
        file=Path(tmp)/patch;file.write_bytes(raw('author/'+patch))
        git('apply','-R','--cached',str(file),extra=env)
    git('update-index','--cacheinfo','160000,ead8036035affd53ef4b29979190f2f4f67084c0,protocol-processor',extra=env)
    reverted=git('write-tree',extra=env).decode().strip()
    assert reverted==prior['context']['parent_index_tree']
    changes=git('diff','--name-only',measured,reverted).decode().splitlines()
    assert changes==prior['context']['changed']
    patch=git('diff',measured,reverted)
    assert len(patch)==prior['context']['difference_bytes'] and sha(patch)==prior['context']['difference_sha256']
out['render_reconstruction']={'measured_head':measured,'reverted_tree':reverted,'changed_paths':changes,'diff_sha256':sha(patch)}

a=read('round2-render-adopted-32-leg-receipts.json');b=read('round2-render-prior-32-leg-receipts.json')
assert len(a)==len(b)==32
rows=[]
for i,(x,y) in enumerate(zip(a,b)):
    assert x['index']==y['index']==i
    keys=set(x)-{'executable'}
    assert keys==set(y)-{'executable'}
    assert all(x[k]==y[k] for k in keys),(i,x,y)
    if x['required_failure'] is not None:
        tokens=x['required_failure'] if isinstance(x['required_failure'],list) else [x['required_failure']]
        passed=x['rc']!=0 and all(any(token in z for z in x['failures']) for token in tokens)
    else:
        passed=x['rc']==0
    rows.append({k:x[k] for k in ('index','caller','name','mode','rc','counts','failures','sha256')}|{'campaign_pass':passed})
assert sum(r['campaign_pass'] for r in rows)==28
assert [r['index'] for r in rows if not r['campaign_pass']]==[2,8,9,15]
epoch=raw('author/round2-render-adopted-clean-epoch.log')
assert epoch==raw('author/round2-render-prior-clean-epoch.log')
assert sha(epoch)==adopt['epoch_sha256']==prior['epoch_sha256'] and len(epoch)==3746
out['render_32_legs']=rows
out['epoch']={'bytes':len(epoch),'sha256':sha(epoch),'campaign_result':'28/32 on both pins'}

closure=read('round2-final-merge-closure.json')
scopes=[]
for s in closure['scopes']:
    actual=git('diff','--name-status',measured,HEAD,'--',*s['paths']).decode().splitlines()
    assert actual==s['changes'] and (not actual)==s['identical'],s['scope']
    if s['scope'] in ('render-parent-source-list','parent-hdl-headers','render-harness-and-recipes','configuration','all-dependency-pins'):
        # Reverted measurement and live source base must have the same inputs.
        assert not git('diff','--name-only',reverted,BASE,'--',*s['paths']).strip(),s['scope']
    scopes.append({'scope':s['scope'],'identical':not actual,'changes':actual})
out['independently_checked_dependency_scopes']=scopes

baseline=json.loads(Path('syn/ooc/pp_resource_baseline.json').read_text())
records=read('round2-resource-records.json')
for ep,r in records.items():assert r==baseline['endpoints'][ep]['record'],ep
out['resource_records_exactly_match_committed_baseline']=True
out['resource']={ep:{'inputs_sha256':r['inputs_sha256'],'figures':r['figures'],'identity':r['identity']} for ep,r in records.items()}

timing=read('round2-timing-directives.json');signoff=read('round2-signoff-details.json')
out['timing']={}
for directive,r in timing['directives'].items():
    assert len(r['corners'])==4
    for corner,c in r['corners'].items():
        assert c['WNS_ns']>=.03 and c['WHS_ns']>=0
        assert all(signoff[directive]['corners'][corner][k]==v for k,v in c.items())
        assert signoff[directive]['corners'][corner]['TNS_ns']==0 and signoff[directive]['corners'][corner]['THS_ns']==0
    assert r['worst']=={k:min(c[k] for c in r['corners'].values()) for k in ('WNS_ns','WHS_ns')}
    assert r['route_status']['routable nets']==r['route_status']['fully routed nets']
    assert r['route_status']['nets with routing errors']==0
    assert not signoff[directive]['rejected_constraints']
    out['timing'][directive]={'corners':r['corners'],'worst':r['worst'],'artifacts':r['artifacts'],'route_status':r['route_status']}
best=max(timing['directives'],key=lambda d:timing['directives'][d]['worst']['WNS_ns'])
assert best==timing['best']=='ExtraPostPlacementOpt'
assert not signoff[best]['critical_warnings']
assert all(records['route-1x1']['figures'][k]==v for k,v in timing['directives'][best]['utilization'].items())
image=read('round2-complete-image-evidence.json')
assert image['best']==best and image['preflight']['rc']==0
assert image['manifest_regeneration']['before_sha256']==image['manifest_regeneration']['after_sha256']
out['complete_image']={k:image[k] for k in ('best','complete_image','preflight','manifest_regeneration','artifacts')}
retention=read('round2-artifact-retention.json')
assert retention['head']==HEAD and len(retention['artifacts'])==185
retained={r['path']:r for r in retention['artifacts']}
for r in image['artifacts']:
    assert r['path'] in retained and r['sha256']==retained[r['path']]['sha256'] and r['bytes']==retained[r['path']]['bytes']
out['image_retention_bindings_verified']=len(image['artifacts'])
out['synthesis_counts']={}
for ep,all_rows in read('round2-synth-86901.json').items():
    rows={k:v for k,v in all_rows.items() if k.startswith('protocol-processor/')}
    assert all_rows['hdl/milan/milan_datapath.sv']==1
    assert len(rows)==46 and all(v==0 for v in rows.values())
    out['synthesis_counts'][ep]={'sources':len(rows),'processor_8_6901':sum(rows.values())}

sweep=read('round2-final-sweep-evidence.json')
assert sweep['head']=='591a5752e6a587b28b501e2d02d6a9d0293f3ba2'
assert sweep['passing']==sweep['completed_suites']==60 and sweep['sweep_rc']==sweep['tally_rc']==0
gates=read('round2-gate-receipts.json')
fresh=[r for r in gates if r['head']==HEAD]
out['retained_full_sweep']={k:v for k,v in sweep.items() if k not in ('suite_logs','commands')}
out['fresh_gate_receipts']=[{k:r[k] for k in ('bank','head','rc','bytes','sha256')} | {'name':r.get('id',r.get('step'))} for r in fresh]
assert fresh and all(r['rc']==0 for r in fresh)
out['limitations']='Public receipts and retained report hashes audited; private report bytes and physical hardware not examined.'
print(json.dumps(out,indent=2))
