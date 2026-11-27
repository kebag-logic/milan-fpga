#!/usr/bin/env python3
"""Configure concurrently, share one 16-job build pool, then run each suite."""
import argparse, concurrent.futures, json, os, subprocess
from pathlib import Path
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--packet',type=Path,required=True)
    ap.add_argument('--jobs',type=int,default=16);a=ap.parse_args();repo=a.repo.resolve();packet=a.packet.resolve()
    work=packet/'scratch/units';work.mkdir(parents=True,exist_ok=True);receipts=packet/'receipts'
    prefix=packet/'scratch/cgreen-prefix'
    profiles={'default':[], 'milan':['-DLWSRP_MILAN=ON'], 'scale':['-DLWSRP_SCALE=ON'],
              'milan-scale':['-DLWSRP_MILAN=ON','-DLWSRP_SCALE=ON'], 'key-only':['-DCMAKE_C_FLAGS=-DLWSRP_ATTR_KEY=1']}
    def configure(item):
        name,extra=item
        with (receipts/('unit-configure-'+name+'.log')).open('w') as log:
            cmd=['cmake','-S',str(repo),'-B',str(work/name),'-DCMAKE_BUILD_TYPE=Debug','-DCMAKE_PREFIX_PATH='+str(prefix),*extra]
            rc=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT).returncode
        return name,rc
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:configured=dict(pool.map(configure,profiles.items()))
    assert not any(configured.values()),configured
    (work/'Makefile').write_text('.PHONY: all '+' '.join(profiles)+'\nall: '+' '.join(profiles)+'\n'+
        ''.join(name+':\n\t+$(MAKE) -C '+name+'\n' for name in profiles))
    with (receipts/'unit-builds.log').open('w') as log:
        rc=subprocess.run(['make','-C',str(work),'-j'+str(min(a.jobs,16))],stdout=log,stderr=subprocess.STDOUT).returncode
    assert rc==0,rc
    def check(name):
        env=os.environ.copy();env['LD_LIBRARY_PATH']=str(prefix/'lib')+':'+str(prefix/'lib64')+':'+env.get('LD_LIBRARY_PATH','')
        with (receipts/('unit-'+name+'.log')).open('w') as log:
            rc=subprocess.run([str(work/name/'unit_tests')],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=60).returncode
        return {'name':name,'rc':rc}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:rows=list(pool.map(check,profiles))
    (receipts/'units.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows))
if __name__=='__main__':main()
