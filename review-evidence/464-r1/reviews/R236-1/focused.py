import os,sys,subprocess,json,shutil,ast
from pathlib import Path
out=Path(__file__).parent; scratch=out/'scratch'; logs=out/'focused-logs';logs.mkdir(exist_ok=True)
results=[]
def run(name,root,py,args,expected=0):
 p=subprocess.run(['rtk','proxy',py,'-B',*args],cwd=root,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','JOBS':'8'},stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 (logs/(name+'.log')).write_text(p.stdout)
 ok=(p.returncode==0) if expected==0 else (p.returncode!=0)
 results.append({'name':name,'interpreter':py,'cwd':str(root),'args':args,'returncode':p.returncode,'expected_zero':expected==0,'expectation_met':ok,'ok_arms':p.stdout.count('[ok  ]'),'fail_arms':p.stdout.count('[FAIL]')})
 assert 'FileNotFoundError' not in p.stdout, (name, 'invalid fixture dependency')
 print(name,p.returncode,'EXPECTED' if ok else 'UNEXPECTED',flush=True)
 return p
for py in ['python3.14','python3.12']:
 for name,expect in [('head',0),('base',1),('historical-good',0),('historical-bad',1)]:
  run(py+'-'+name,scratch/name,py,['avdecc/gen_aem_store.py','--self-test'],expect)
run('ci-check',scratch/'head','python3',['scripts/ci_events.py','--check'])
run('ci-selftest',scratch/'head','python3',['scripts/ci_events.py','--selftest'])
# Each mutation is applied alone to a clean two-module copy of the exact head.
root=scratch/'mutant';shutil.copytree(scratch/'head'/'avdecc',root/'avdecc',dirs_exist_ok=True)
shutil.copytree(scratch/'head'/'hdl/common/csr',root/'hdl/common/csr',dirs_exist_ok=True)
for py in ['python3.14','python3.12']:
 p=run(py+'-mutant-pristine',root,py,['avdecc/gen_aem_store.py','--self-test'])
 assert p.returncode==0 and p.stdout.count('[ok  ]')==20
original={n:(root/'avdecc'/n).read_text() for n in ['aem_maps.py','gen_aem_store.py']}
def edit_guard(text,guard):
 assert text.count(guard)==1,guard
 return text.replace(guard,'if False: # R236 planted guard loss',1)
mutations=[
 ('cluster-offset','aem_maps.py','if co >= port["clusters"]:',None),
 ('base-map','aem_maps.py','if not 0 <= bm < len(maps):',None),
 ('map-count','aem_maps.py','if port["maps"] != 1:',None),
 ('cluster-channel','aem_maps.py','if cc >= SMAP_CLUSTER_CHANNELS:',None),
 ('stream-index','aem_maps.py','if si >= side.n_streams:',None),
 ('input-duplicate','aem_maps.py','if (co, cc) in seen:',None),
 ('output-duplicate','aem_maps.py','if (si, sc) in cfg_stream_ch:',None),
 ('row-count','aem_maps.py','if len(rows) > SMAP_MAX_ROWS:',None),
 ('crf-refusal','aem_maps.py','if not chans:',None),
 ('input-rule-both','aem_maps.py','if side.direction == "INPUT":','if True:'),
 ('output-rule-both','aem_maps.py','if side.direction == "INPUT":','if False:'),
 ('stale-deviation-index','aem_maps.py','"STREAM_PORT_OUTPUT[0] AUDIO_MAP[0] mapping','"STREAM_PORT_OUTPUT[0] AUDIO_MAP[1] mapping'),
 ('widen-deviations','aem_maps.py','for c in range(2, 8)','for c in range(2, 9)'),
 ('drop-deviation','aem_maps.py','for c in range(2, 8)','for c in range(3, 8)'),
 ('ignore-new-deviation','aem_maps.py','if new:',None),
 ('directory-gate','gen_aem_store.py','def _selftest_two_level():','def check_two_level(*args):\n    return None\n\ndef _selftest_two_level():'),
 ('name-gate','gen_aem_store.py','def _selftest_two_level():','def check_named(*args):\n    return None\n\ndef _selftest_two_level():'),
 ('base-format-gate','gen_aem_store.py','def _selftest_base_formats():','def base_channel_cover(*args):\n    return set(MILAN_BASE_CHANNELS)\n\ndef _selftest_base_formats():'),
 ('lost-callable','gen_aem_store.py','from collections.abc import Callable',''),
 ('builtin-instead-of-fixture','gen_aem_store.py','spec = _map_fixture()','spec = builtin_spec()'),
]
for py in ['python3.14','python3.12']:
 for label,file,old,new in mutations:
  for n,t in original.items(): (root/'avdecc'/n).write_text(t)
  t=original[file];assert t.count(old)==1,(label,t.count(old));t=edit_guard(t,old) if new is None else t.replace(old,new)
  (root/'avdecc'/file).write_text(t)
  # Python 3.14 deliberately defers the unimported annotation.
  expect=0 if label=='lost-callable' and py=='python3.14' else 1
  run(py+'-mutant-'+label,root,py,['avdecc/gen_aem_store.py','--self-test'],expect)
for n,t in original.items(): (root/'avdecc'/n).write_text(t)
(out/'focused-results.json').write_text(json.dumps(results,indent=2)+'\n')
assert all(r['expectation_met'] for r in results)
