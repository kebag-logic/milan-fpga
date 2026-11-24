#!/usr/bin/env python3
"""Run identical small mutation campaigns at base/head, cold/warm, in private trees."""
import concurrent.futures, hashlib, io, json, os, pathlib, resource, shutil, subprocess, sys, tarfile, time
root=pathlib.Path(sys.argv[1]).resolve(); packet=pathlib.Path(__file__).resolve().parents[1]
scratch=packet/'scratch/cache-probe';scratch.mkdir(parents=True,exist_ok=True)
verilator=sys.argv[2] if len(sys.argv)>2 else '$VALIDATION_TOOLS/pinned-verilator-5.050/verilator'
version=subprocess.check_output([verilator,'--version'],text=True).strip(); assert 'Verilator 5.050' in version
print(version,flush=True)
# A local wrapper bounds the unchanged campaign's explicit -j 0 request.
binpath=scratch/'bin';binpath.mkdir(exist_ok=True)
wrapper=binpath/'verilator';wrapper.write_text('#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\nfor i in range(len(a)-1):\n if a[i]=="-j" and a[i+1]=="0": a[i+1]="4"\nos.execv('+repr(verilator)+',['+repr(verilator)+',*a])\n');wrapper.chmod(0o755)
paths=['hdl/ieee8021q/filtering','tb/verilator/tcam','tb/common','scripts']
for arm,ref in [('base','fcbc31f3'),('head','13e6d869')]:
 tree=scratch/arm; tree.mkdir(exist_ok=True)
 data=subprocess.check_output(['git','archive',ref,'--',*paths],cwd=root)
 with tarfile.open(fileobj=io.BytesIO(data)) as archive: archive.extractall(tree,filter='data')
def run(arm):
 tree=scratch/arm;tmp=scratch/(arm+'-tmp');tmp.mkdir(exist_ok=True);cache=scratch/(arm+'-cache');cache.mkdir(exist_ok=True)
 env=dict(os.environ,TMPDIR=str(tmp),PATH=str(binpath)+':'+os.environ['PATH'],CCACHE_DIR=str(cache),OBJCACHE='ccache',MAKEFLAGS='-j16 --no-print-directory',VERILATOR_JOBS='4',PYTHONDONTWRITEBYTECODE='1')
 for flag in ('CCACHE_BASEDIR','CCACHE_NOHASHDIR'):env.pop(flag,None)
 records=[]
 for mode in ('cold','warm'):
  subprocess.run(['ccache','--zero-stats'],env=env,check=True,stdout=subprocess.DEVNULL)
  begin=time.monotonic()
  with (packet/'receipts'/f'tcam-{arm}-{mode}.log').open('w') as log:
   proc=subprocess.run([sys.executable,'mutants.py'],cwd=tree/'tb/verilator/tcam',env=env,stdout=log,stderr=subprocess.STDOUT,timeout=300)
  stats=subprocess.check_output(['ccache','--print-stats'],env=env,text=True)
  (packet/'receipts'/f'tcam-{arm}-{mode}.stats').write_text(stats)
  data=dict(line.split() for line in stats.splitlines())
  record=dict(arm=arm,mode=mode,returncode=proc.returncode,wall_seconds=round(time.monotonic()-begin,3),direct_hits=int(data['direct_cache_hit']),preprocessed_hits=int(data['preprocessed_cache_hit']),misses=int(data['cache_miss']))
  print(json.dumps(record),flush=True); records.append(record);assert proc.returncode==0
 return records
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: records=list(pool.map(run,['base','head']))
logs=[(packet/'receipts'/f'tcam-{a}-{m}.log').read_bytes() for a in ('base','head') for m in ('cold','warm')]
assert all(log==logs[0] for log in logs)
print(json.dumps(dict(probe='tcam-exact-output-identity',identical=True,sha256=hashlib.sha256(logs[0]).hexdigest())),flush=True)
(packet/'receipts/cache-probe.json').write_text(json.dumps(records,indent=2)+'\n')
