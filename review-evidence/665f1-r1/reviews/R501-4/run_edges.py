#!/usr/bin/env python3
"""Independent agreement patterns, persistent HELD, and exact clock arithmetic.

Usage: python3 run_edges.py CHECKOUT [--jobs 6]
Only disposable host fault injection is changed; production source is hashed.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import traceback

P = Path(__file__).resolve().parent

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('checkout', type=Path)
    ap.add_argument('--jobs', type=int, default=6)
    args = ap.parse_args()
    root = args.checkout.resolve()
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(root/'sw/firmware/ctrl_nvm/test'))
    import nvm_bench as nb
    from nvm_checks import state_matches, rid_payloads, SLOT_A, SLOT_B
    from nvm_checks_write import changed_frames
    scratch = P/'scratch/edges'
    receipts = P/'receipts/edges'
    receipts.mkdir(parents=True, exist_ok=True)
    stems = ['endstation_ax7101_1x1_tdm8','endstation_ax7101_8x8','endstation_arty_current']
    inputs = {s: nb.shape_inputs(root/'configs'/f'{s}.yaml',scratch/'inputs'/s) for s in stems}
    production = ['nvm_store.c','nvm_klj2.c','plat/nvm_flash_litespi.c']
    def task(item):
        stem, masks = item
        name = stem+'-'+''.join(f'{x:02x}' for x in masks)
        log=[]; cases=[]; rc=0
        try:
            work=scratch/name
            tree=work/'tree'
            shutil.copytree(nb.TREE,tree,ignore=shutil.ignore_patterns('__pycache__'),dirs_exist_ok=True)
            f=tree/'host/nvm_fmodel.c'
            text=f.read_text()
            old='dst[fm.fault_at - addr] ^= (uint8_t)(0x08u << (fm.varied++ % 5u));'
            assert text.count(old)==1
            new='{ static const uint8_t masks[3] = {'+','.join(map(str,masks))+'}; '+\
                'dst[fm.fault_at - addr] ^= masks[fm.varied++ % 3u]; }'
            f.write_text(text.replace(old,new))
            for source in production:
                h=lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
                assert h(tree/source)==h(nb.TREE/source)
                log.append('PRODUCTION '+source+' '+h(tree/source))
            b=nb.make_bench(inputs[stem],work/'bench',tree)
            def run(*argv):
                r=b.run(*argv)
                log.append('COMMAND '+json.dumps([str(x).replace(str(work),'<scratch>') for x in argv]))
                log.append(r.out)
                return r
            for slot in (0,1):
                for seq in (1,5,0x80000000,0xffffffff):
                    frames,_=changed_frames(b,96+slot)
                    img=b.assemble(frames,seq)
                    saved=rid_payloads(b,img)
                    for where in (0,0x100):
                        base=(SLOT_A,SLOT_B)[slot]
                        r=run('--slot-a' if slot==0 else '--slot-b',b.file('gold.bin',img),
                              '--boot-fault',f'read-vary-at:3:0:{base+where:#x}',
                              '--boot','--dump-state','state.txt','--dump-slot-a','a.bin',
                              '--dump-slot-b','b.bin')
                        held=len(set(masks))==3 and masks[-1]!=0
                        restored=masks[-1]==0
                        expect_unread=(1<<slot) if held else 0
                        assert r.s['unread']==expect_unread, r.s
                        assert r.s['phase']==(10 if held else 1), r.s
                        assert r.s['read_faults']==(2 if held else 1), r.s
                        assert r.s['releases']==1, r.s
                        assert not state_matches(b,b.work/'state.txt',saved if restored else {}), r.s
                        assert (b.work/('a.bin' if slot==0 else 'b.bin')).read_bytes()[:len(img)]==img
                        cases.append({'slot':slot,'seq':seq,'offset':where,'masks':masks,
                                      'unread':r.s['unread'],'read_faults':r.s['read_faults'],
                                      'phase':r.s['phase'],'restored':restored})
            # A permanently failed read returns, reports HELD, and keeps reporting
            # dirty through 120 seconds even after the fault is cleared at runtime.
            rid=max(b.frames); payload=bytes(len(b.frames[rid])-8)
            r=run('--slot-a',b.file('held.bin',b.assemble(b.frames,5)),
                  '--boot-fault','read-fail:999999:0','--boot',
                  '--set',f'{rid}:{payload.hex()}','--commit-try','--run-ms','60000',
                  '--fault','none','--run-ms','60000','--commit-try')
            assert r.s['unread']==3 and r.s['phase']==10 and r.s['dirty']==1, r.s
            assert r.s['erases']==r.s['programs']==0 and r.s['commit_refused']==2, r.s
            assert r.s['read_faults']==6 and r.s['releases']==1 and r.s['calls']>=1200000, r.s
            log.append('HELD PASS '+json.dumps(r.s,sort_keys=True))
        except Exception:
            rc=1; log.append(traceback.format_exc())
        (receipts/(name+'.log')).write_text('\n'.join(log)+'\n')
        (receipts/(name+'.json')).write_text(json.dumps(cases,indent=2)+'\n')
        (receipts/(name+'.rc')).write_text(str(rc)+'\n')
        print(name,rc,flush=True)
        return rc
    items=[(s,m) for s in stems for m in [(8,16,0),(8,16,32),(8,16,8)]]
    with ThreadPoolExecutor(max_workers=min(16,max(1,args.jobs))) as pool:
        results=list(pool.map(task,items))
    clock_log=[]; clock_rc=0
    try:
        for hz in [83333000,100000000]:
            w=scratch/f'clock-{hz}'; w.mkdir(parents=True,exist_ok=True)
            nb.write_headers(w/'gen', nb.shape_header(inputs[stems[0]].shape,
                inputs[stems[0]].donor,inputs[stems[0]].ident), hz)
            cmd=['gcc','-std=c11','-O1',f'-I{nb.TREE}',f'-I{nb.TREE}/host/stubs',
                 f'-I{w}/gen',str(P/'probe_clock.c'),'-o',str(w/'probe')]
            compiled=subprocess.run(cmd,capture_output=True,text=True)
            clock_log.append(compiled.stdout+compiled.stderr)
            assert compiled.returncode==0
            out=subprocess.check_output([str(w/'probe')],text=True)
            clock_log.append(out)
            for line in out.splitlines():
                parts=line.split()
                if parts[0]=='TIME':
                    _,freq,ticks,actual=parts
                    assert int(actual)==int(ticks)*1000000//int(freq), line
                else:
                    _,freq,ticks,delta,late=parts
                    assert int(ticks)==2000*int(freq)//1000000, line
                    assert int(late)==int(int(delta)>0), line
    except Exception:
        clock_rc=1;clock_log.append(traceback.format_exc())
    (receipts/'clock.log').write_text('\n'.join(clock_log))
    (receipts/'clock.rc').write_text(str(clock_rc)+'\n')
    summary={'agreement_cases':len(items)*16,'shape_patterns':len(items),
             'held_runs':len(items),'clock_rc':clock_rc,'nonzero_tasks':sum(bool(r) for r in results)}
    (receipts/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary),flush=True)
    return int(bool(clock_rc or any(results)))

if __name__=='__main__':
    sys.exit(main())
