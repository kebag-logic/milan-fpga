#!/usr/bin/env python3
"""Compile focused boundary probes and compare default object bytes with main."""
import argparse, concurrent.futures, hashlib, json, shutil, subprocess
from pathlib import Path

BASE='d1bb4f4e5954af6dabe7f210a6bf7adbb76bdd6b'
SOURCES=['core/mrp_mad.c','core/mrp_pdu.c','ports/timer.c','ports/alloc.c','modules/msrp.c','modules/mvrp.c','modules/mmrp.c']
CONFIGS={'default':[], 'key':['-DLWSRP_ATTR_KEY=1'], 'wheel':['-DLWSRP_TIMER_SLOTS=64'],
         'buckets':['-DLWSRP_ATTR_BUCKETS=16'], 'merge':['-DLWSRP_TX_MERGE=1'],
         'one-port':['-DLWSRP_ONE_PORT_MAP=1'], 'lean-validate':['-DLWSRP_LEAN_VALIDATE=1'],
         'rapid':['-DLWSRP_RAPID_REPLACE=1'], 'lean-copy':['-DLWSRP_LEAN_COPY=1'],
         'lean-tx':['-DLWSRP_LEAN_TX=1']}
CONFIGS['all']=[d for defs in CONFIGS.values() for d in defs]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--packet',type=Path,required=True)
    ap.add_argument('--jobs',type=int,default=4);a=ap.parse_args()
    repo=a.repo.resolve();packet=a.packet.resolve();scratch=packet/'scratch'/'probes';scratch.mkdir(parents=True,exist_ok=True)
    receipts=packet/'receipts';receipts.mkdir(exist_ok=True)
    base=scratch/'base';base.mkdir(exist_ok=True)
    subprocess.run(['git','archive','-o',str(scratch/'base.tar'),BASE,'src'],cwd=repo,check=True)
    subprocess.run(['tar','-xf',str(scratch/'base.tar'),'-C',str(base)],check=True)
    def boundary(name,defs,profile,source):
        label=name+'-'+str(profile);exe=scratch/label
        cmd=['cc','-O2','-std=c11','-Wall','-Wextra','-Werror','-DLWSRP_MILAN='+str(profile),*defs,
             '-I'+str(source/'src'),'-I'+str(source/'src/include'),str(packet/'boundary_probe.c'),
             *[str(source/'src'/s) for s in SOURCES],'-o',str(exe)]
        with (receipts/('boundary-'+label+'.log')).open('w') as log:
            log.write('$ '+' '.join(cmd)+'\n');log.flush()
            rc=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT).returncode
            build=rc
            if rc==0:rc=subprocess.run([str(exe)],stdout=log,stderr=subprocess.STDOUT,timeout=30).returncode
        return {'config':name,'milan':profile,'build':build,'run':rc}
    def objects():
        rows=[]
        paths=[p for p in subprocess.check_output(['git','ls-files','src'],cwd=repo,text=True).splitlines() if p.endswith('.c')]
        for opt in ['-O0','-O2','-Os']:
            for p in paths:
                hashes=[]
                for label,source in [('base',base),('head',repo)]:
                    out=scratch/(label+'-'+opt[1:]+'-'+p.replace('/','_')+'.o')
                    cmd=['cc',opt,'-std=c11','-Isrc','-Isrc/include','-c',p,'-o',str(out)]
                    r=subprocess.run(cmd,cwd=source,capture_output=True)
                    if r.returncode:
                        hashes.append('build failed: '+r.stderr.decode());continue
                    hashes.append(hashlib.sha256(out.read_bytes()).hexdigest())
                rows.append({'optimization':opt,'path':p,'equal':hashes[0]==hashes[1], 'base_sha256':hashes[0],'head_sha256':hashes[1]})
        (receipts/'default-objects.json').write_text(json.dumps(rows,indent=2)+'\n')
        return {'object_comparisons':len(rows),'different':[{k:r[k] for k in ('optimization','path')} for r in rows if not r['equal']]}
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(a.jobs,12)) as pool:
        fs=[pool.submit(boundary,name,defs,profile,repo) for name,defs in CONFIGS.items() for profile in (0,1)]
        fs += [pool.submit(boundary,'base',[],profile,base) for profile in (0,1)]
        obj=pool.submit(objects)
        rows=[f.result() for f in fs]
        print(json.dumps(obj.result()),flush=True)
    (receipts/'boundaries.json').write_text(json.dumps(rows,indent=2)+'\n')
    print(json.dumps(rows),flush=True)

if __name__=='__main__':main()
