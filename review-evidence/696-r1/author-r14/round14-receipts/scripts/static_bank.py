import json,os,subprocess,time
from pathlib import Path
w=Path(__file__).resolve().parent;repo=Path('$LANE');out=w/'static';out.mkdir(exist_ok=True)
env=dict(os.environ,TMPDIR=str(w/'tmp'),PYTHONDONTWRITEBYTECODE='1')
P='$DOC_ENV/bin/python3'
steps=[['scripts/'+name,*args] for name,args in [
 ('docs_check.py',[]),('check_doc_style.py',[]),('check_doc_paths.py',[]),('gen_toc.py',['--check']),('gen_toc.py',['--verify-anchors']),
 ('check_em_dash.py',['--base','e81ce82f']),('check_baremetal_only.py',['--check']),('check_sv_idiom.py',[]),('check_cpp_idiom.py',[]),('check_py_idiom.py',[]),('check_sh_idiom.py',[]),
 ('check_hygiene.py',['--check']),('measure_test_evidence.py',['--check']),('measure_fail_fast.py',['--check']),('measure_naming.py',['--check']),('check_todo_ownership.py',[]),('check_port_contracts.py',[]),('check_soc_sources.py',[]),('check_rtl_source_lists.py',[]),('ci_events.py',['--check']),('ci_events.py',['--selftest']),('ci_scope.py',['--selftest']),('suite_shards.py',['--selftest']),('check_feature_status.py',['--self-test']),('check_submodule_docs.py',[]),('pp_srcs.py',['--check','--selftest'])]]
steps += [['docs/traceability/gen_module_matrix.py','--check'],['syn/ooc/pp_resource_gate.py','check-baseline']]
rows=[]
for i,args in enumerate(steps):
 name=f'{i:02d}-'+Path(args[0]).stem;start=time.time()
 with (out/(name+'.log')).open('w') as log:r=subprocess.run([P,*args],cwd=repo,env=env,stdout=log,stderr=subprocess.STDOUT)
 (out/(name+'.rc')).write_text(str(r.returncode)+'\n');rows.append(dict(name=name,argv=[P,*args],rc=r.returncode,seconds=round(time.time()-start,1)))
 (out/'results.json').write_text(json.dumps(rows,indent=2)+'\n');print(name,r.returncode,flush=True)
bad=[r for r in rows if r['rc']];print('failed',len(bad),flush=True);raise SystemExit(bool(bad))
