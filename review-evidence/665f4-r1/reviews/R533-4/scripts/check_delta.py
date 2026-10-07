#!/usr/bin/env python3
"""Record the exact delta and run focused style/document checks concurrently."""
import argparse, concurrent.futures, json, os, pathlib, subprocess, time
p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--packet',type=pathlib.Path,required=True);p.add_argument('--jobs',type=int,default=4);a=p.parse_args()
assert 1<=a.jobs<=4
repo=a.repo.resolve();out=a.packet.resolve()/'receipts';env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(a.packet.resolve()/'scratch'),GIT_NO_REPLACE_OBJECTS='1')
def git(*args):return subprocess.check_output(['git',*args],cwd=repo,env=env,text=True)
base='db9aa8c9b135b34ff3d070a979dee70440b37cc6'; prior='c1049de1970e93d2c36ace62891ee9d947cd3191'; head='6f7deea15a9160761b30aaa93fe152f20d416695';dev='d51b373ad7e8e8381af2797be3ebb8ee45c62e3c'
paths=['sw/firmware/ctrl/srp/README.md','sw/firmware/ctrl/test/srp_mbx.cpp','sw/firmware/ctrl/test/srp_mutants.py']
assert git('rev-parse','HEAD').strip()==head
assert git('rev-parse','HEAD^').strip()==prior
assert git('diff','--name-only',prior,head).splitlines()==paths
assert not git('diff','--name-only',dev,head,'--','hdl','sw/litex','configs','syn','constraints')
metadata={'head':head,'tree':git('rev-parse','HEAD^{tree}').strip(),'round3':prior,'source_base':base,'validation_dev_reference':dev,'round4_changed':paths,'production_changes_since_round3':False,'rtl_build_shipping_paths_changed_from_dev':False,'full_delta_stat':git('diff','--stat',base,head),'history':git('log','--format=%H %P %s',base+'..'+head),'raw_round4':git('diff','--raw','--no-abbrev',prior,head)}
(out/'scope-proof.json').write_text(json.dumps(metadata,indent=2)+'\n')
checks=[['git','diff','--check',prior,head],['python3','-B','scripts/docs_check.py'],['python3','-B','scripts/check_doc_paths.py'],['python3','-B','scripts/check_doc_style.py'],['python3','-B','scripts/check_cpp_idiom.py'],['python3','-B','scripts/check_py_idiom.py'],['python3','-B','sw/mailbox/gen_mailbox.py','--check']]
def work(pair):
    n,cmd=pair; start=time.monotonic();r=subprocess.run(cmd,cwd=repo,env=env,capture_output=True,text=True,timeout=500)
    (out/f'delta-check-{n}.log').write_text(r.stdout+r.stderr);(out/f'delta-check-{n}.rc').write_text(str(r.returncode)+'\n')
    return {'command':cmd,'rc':r.returncode,'seconds':round(time.monotonic()-start,3),'log':f'delta-check-{n}.log'}
with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as pool:results=list(pool.map(work,enumerate(checks,1)))
(out/'delta-checks.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2));raise SystemExit(int(any(x['rc'] for x in results)))
