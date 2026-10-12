#!/usr/bin/env python3
"""Feed three real AAF packets and grade snapshots before/after publication."""
import argparse, os, pathlib, re, shlex, subprocess, sys, json
p=argparse.ArgumentParser();p.add_argument('repo',type=pathlib.Path);p.add_argument('packet',type=pathlib.Path);a=p.parse_args()
repo=a.repo.resolve(); packet=a.packet.resolve(); work=packet/'scratch/snapshot'; work.mkdir(parents=True,exist_ok=True)
suite=repo/'tb/verilator/avtp_rxmon'
src=(suite/'sim_main_nx.cpp').read_text().replace('../../common/verilator_harness.hpp',str(repo/'tb/common/verilator_harness.hpp'))
anchor='        first_valid_pdu_locks_and_seeds_seq();'
assert src.count(anchor)==1
src=src.replace(anchor, r'''        align_iv();
        for (unsigned n=0; n<3; ++n) { AafCfg c; c.seq=n; feed(build_aaf(stim,c)); }
        const auto tv=lctx_rd(0,W_TV), tnv=lctx_rd(0,W_TNV), frx=lctx_rd(0,W_FRX);
        ck("three accepted packets update TV",tv,3);
        ck("no invalid timestamp packets",tnv,0);
        ck("publication pending",frx,0);
        printf("SNAPSHOT,before,%ld,%ld,%ld\n",tv,tnv,frx);
        flush_iv();
        const auto after=lctx_rd(0,W_FRX);
        ck("published total",after,3);
        printf("SNAPSHOT,after,%ld,%ld,%ld\n",lctx_rd(0,W_TV),lctx_rd(0,W_TNV),after);
        return fails ? 1 : 0;
''')
cpp=work/'snapshot.cpp'; cpp.write_text(src)
recipe=subprocess.check_output(['make','-s','--eval','review-print: ; @echo \'$(NXFLAGS)\'; echo \'$(NXSRCS)\'','review-print'],cwd=suite,text=True).splitlines()
flags=shlex.split(recipe[0]); flags[flags.index('-j')+1]='2'
flags=[f.replace('../../../',str(repo)+'/') for f in flags]
sources=[str((suite/f).resolve()) for f in shlex.split(recipe[1])]
with (packet/'receipts/snapshot-build.log').open('w') as log:
    subprocess.run([os.environ.get('VERILATOR','$VALIDATION_TOOLS/pinned-verilator-5.050/verilator'),*flags,'--Mdir',str(work/'obj'),*sources,str(cpp),'-o','snapshot'],cwd=work,stdout=log,stderr=subprocess.STDOUT,check=True)
r=subprocess.run([str(work/'obj/snapshot')],text=True,capture_output=True,check=True)
(packet/'receipts/snapshot-rtl.log').write_text(r.stdout+r.stderr)
print(r.stdout)
sys.path.insert(0,str(repo/'tb/tools')); import torture_campaign as tc
failed=False
for line in r.stdout.splitlines():
    if line.startswith('SNAPSHOT,'):
        _,phase,tv,tnv,frx=line.split(',')
        sample=dict(TIMESTAMP_VALID=int(tv),TIMESTAMP_NOT_VALID=int(tnv),FRAMES_RX=int(frx))
        verdict,detail=tc.check_tv_tnv(sample)
        expected='INFO' if phase=='before' else 'PASS'
        print(json.dumps(dict(phase=phase,sample=sample,actual=verdict,expected=expected,detail=detail)))
        failed |= verdict!=expected
print('snapshot diagnostic contract:', 'FAIL' if failed else 'PASS')
raise SystemExit(int(failed))
