#!/usr/bin/env python3
"""Recheck the two small count-one suites at the frozen source base."""
import argparse, concurrent.futures, io, json, os, pathlib, re, subprocess, tarfile
p=argparse.ArgumentParser(); p.add_argument('--repo',required=True); p.add_argument('--verilator',required=True); a=p.parse_args()
packet=pathlib.Path(__file__).resolve().parents[1]; tree=packet/'scratch/base-suites'; tree.mkdir(exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['git','archive','e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8'],cwd=a.repo))) as tf: tf.extractall(tree,filter='data')
logs=packet/'receipts/base-suites'; logs.mkdir(parents=True,exist_ok=True); wrapper=packet/'scratch/bounded-verilator.py'
env=os.environ.copy(); env.update(VERILATOR=str(wrapper),R513_VERILATOR=str(pathlib.Path(a.verilator).resolve()),TMPDIR=str(packet/'scratch/tmp'),MAKEFLAGS='-j16',R513_COMPILE_JOBS='3')
def run(suite):
 cmd=['make','-j16','-C',str(tree/'tb'/suite),'run','VERILATOR='+str(wrapper)]
 with (logs/(suite+'.log')).open('w') as f:
  f.write('command: '+repr(cmd)+'\n'); f.flush(); r=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT)
 (logs/(suite+'.rc')).write_text(str(r.returncode)+'\n'); text=(logs/(suite+'.log')).read_text(); row=dict(suite=suite,rc=r.returncode,tallies=[x for x in text.splitlines() if re.match(r'(\[build|\d+ checks:)',x)]); print(json.dumps(row),flush=True); return row
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: results=list(pool.map(run,['adp_engine','aecp_notify']))
(logs/'results.json').write_text(json.dumps(results,indent=2)+'\n'); raise SystemExit(any(r['rc'] for r in results))
