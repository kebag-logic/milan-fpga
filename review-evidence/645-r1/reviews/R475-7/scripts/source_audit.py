#!/usr/bin/env python3
"""Audit the immutable delta, timing arithmetic and unchanged build inputs."""
import hashlib,json,pathlib,re,subprocess,sys
source=pathlib.Path(sys.argv[1]);packet=pathlib.Path(sys.argv[2])
def git(*args):return subprocess.check_output(['git','-C',str(source),*args])
head='8e4b1e53e9b5a8ef5f9854095347436ab84259b6';base='6aa25dec977c6ad78bf4ff6275de47fb81d0c246';parent='1e79ebdc06528edff74c0a7f530f20f99e3326a2'
assert git('rev-parse','HEAD').decode().strip()==head
paths=git('diff','--name-only',parent,head).decode().splitlines()
assert len(git('rev-list',parent+'..'+head).splitlines())==1
forbidden=['hdl/','configs/','constraints/','syn/']
assert not any(p.startswith(tuple(forbidden)) for p in paths)
retained={}
for path in ('scripts/run_all_suites.sh','scripts/measure_test_evidence.py','docs/testing/CI_WORKFLOWS.md','syn/ooc/pp_resource_baseline.json'):
 a=git('show',parent+':'+path);b=git('show',head+':'+path);assert a==b;retained[path]=hashlib.sha256(b).hexdigest()
for path in ('tb/verilator/follow_ring/Makefile','tb/verilator/milan_dp_render/Makefile'):
 texts=[git('show',r+':'+path).decode() for r in (parent,head)]
 targets=[re.findall(r'^([A-Za-z0-9_./% -]+):',t,re.M) for t in texts]
 assert targets[0]==targets[1],path
 if 'milan_dp_render' in path:
  bodies=['\n'.join(l for l in t.splitlines() if not l.startswith('#')) for t in texts]
  assert bodies[0]==bodies[1]
assert not git('diff','--name-only','4640d995',head,'--','hdl','configs','constraints','syn','sw')
figures=[]
for name,previous,replica_prior,replica_new,ratio in [('follow_ring',1422.5,800.2,437.204,1.78),('milan_dp_render',1093.9,826.7,793.308,1.324)]:
 projection=replica_new*ratio
 figures.append(dict(suite=name,previous_hosted=previous,prior_local=replica_prior,ratio_unrounded=previous/replica_prior,ratio_used=ratio,new_local_claim=replica_new,projection=round(projection,1),margin1440=round(1440-projection,1),margin1800=round(1800-projection,1)))
result=dict(head=head,tree=git('rev-parse','HEAD^{tree}').decode().strip(),parent=parent,base=base,delta_files=paths,commit_count=1,rtl_config_resource_changes=False,targets_unchanged=True,suite_discovery_unchanged=True,retained_files=retained,resource_input_scope_unchanged_since='4640d995',full_diff_sha256=hashlib.sha256(git('diff',base,head)).hexdigest(),figures=figures)
(packet/'receipts/source-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
