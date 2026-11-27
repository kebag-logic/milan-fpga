#!/usr/bin/env python3
"""Retain diagnostics while exercising the lean validation path and its control."""
import argparse,concurrent.futures,importlib.util,json,os,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--packet',type=Path,required=True)
    ap.add_argument('--jobs',type=int,default=2);a=ap.parse_args();repo=a.repo.resolve();packet=a.packet.resolve()
    spec=importlib.util.spec_from_file_location('differential',repo/'tests/check_differential.py');d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
    work=packet/'scratch/memory';work.mkdir(parents=True,exist_ok=True)
    shutil.copytree(repo/'src',work/'mutant/src',dirs_exist_ok=True)
    _,path,old,new=d.LEAN_READ;p=work/'mutant/src'/path;assert old in p.read_text();p.write_text(p.read_text().replace(old,new,1))
    def run(profile):
        row={'milan':profile}
        for name,src in [('head',repo/'src'),('control',work/'mutant/src')]:
            exe=work/(name+'-'+profile)
            cmd=['clang',*d.MSAN,*d.END_STATION,'-DLWSRP_MILAN='+str(int(profile=='ON')),
                 '-I'+str(src),'-I'+str(src/'include'),'-o',str(exe),str(repo/d.PROGRAMS['mad'][0]),
                 *[str(src/s) for s in d.PROGRAMS['mad'][1]]]
            with (packet/'receipts'/('memory-'+profile.lower()+'-'+name+'.log')).open('w') as log:
                log.write('$ '+' '.join(cmd)+'\n');log.flush()
                build=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT).returncode
                result={'build_rc':build,'passed':0,'first_failure':None}
                if build==0:
                    for seed in range(1,201):
                        env=os.environ.copy();env['MSAN_OPTIONS']='exitcode=86'
                        r=subprocess.run([str(exe),str(seed),'3000'],capture_output=True,env=env,timeout=120)
                        if r.returncode:
                            result['first_failure']={'seed':seed,'rc':r.returncode,'uninitialized_report':b'use-of-uninitialized-value' in r.stderr}
                            log.write('seed='+str(seed)+' rc='+str(r.returncode)+'\n'+r.stderr.decode(errors='replace'));break
                        result['passed']+=1
                log.write(json.dumps(result)+'\n')
                row[name]=result
        return row
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(a.jobs,2)) as pool:rows=list(pool.map(run,['OFF','ON']))
    (packet/'receipts/memory.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows))
if __name__=='__main__':main()
