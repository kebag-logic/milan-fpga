#!/usr/bin/env python3
"""Does the published random stimulus detect skipping all remaining type words?"""
import argparse, concurrent.futures, importlib.util, json, shutil, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode=True
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--packet',type=Path,required=True)
    ap.add_argument('--jobs',type=int,default=2);a=ap.parse_args();repo=a.repo.resolve();packet=a.packet.resolve()
    spec=importlib.util.spec_from_file_location('differential',repo/'tests/check_differential.py')
    d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
    work=packet/'scratch/type-word-control';work.mkdir(parents=True,exist_ok=True)
    shutil.copytree(repo/'src',work/'src',dirs_exist_ok=True)
    p=work/'src/core/mrp_mad.c';s=p.read_text();old='            type |= 31u;\n'
    assert s.count(old)==1
    p.write_text(s.replace(old,'            type = 255u; /* Fault: skip all later words, even occupied ones. */\n'))
    def run(profile):
        name=profile.lower();exe=d.build(work,'skip-later-words-'+name,work/'src','mad',d.END_STATION,profile)
        if not exe:return {'milan':profile,'build_failed':True}
        reference=packet/('scratch/differential-'+name+'/mad-end-station')
        matched=0;first=None
        for seed in range(1,201):
            expected=d.trace(reference,seed,3000);actual=d.trace(exe,seed,3000)
            if expected==actual and actual[0]==0:matched+=1
            elif first is None:first=seed
        boundary=work/('boundary-'+name)
        sources=['core/mrp_mad.c','core/mrp_pdu.c','ports/timer.c','ports/alloc.c','modules/msrp.c','modules/mvrp.c','modules/mmrp.c']
        cmd=['cc','-O2','-std=c11',*d.END_STATION,'-DLWSRP_MILAN='+str(profile=='ON'),
             '-I'+str(work/'src'),'-I'+str(work/'src/include'),str(packet/'boundary_probe.c'),
             *[str(work/'src'/x) for x in sources],'-o',str(boundary)]
        # Use numeric preprocessor values.
        cmd=[x.replace('LWSRP_MILAN=True','LWSRP_MILAN=1').replace('LWSRP_MILAN=False','LWSRP_MILAN=0') for x in cmd]
        with (packet/'receipts'/('type-word-control-'+name+'.log')).open('w') as log:
            log.write('Mutation: type |= 31u -> type = 255u\nPublished stimulus: seeds 1..200, 3000 steps, end-station switches\n')
            log.write('Identical full traces: '+str(matched)+'; first difference: '+str(first)+'\n');log.flush()
            rc=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT).returncode
            build=rc
            if rc==0:rc=subprocess.run([str(boundary)],stdout=log,stderr=subprocess.STDOUT).returncode
        return {'milan':profile,'identical_traces':matched,'first_difference':first,'boundary_build_rc':build,'boundary_run_rc':rc}
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(a.jobs,2)) as pool:rows=list(pool.map(run,['OFF','ON']))
    (packet/'receipts/type-word-control.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows))
if __name__=='__main__':main()
