import json, os, shutil, subprocess, sys, time
from pathlib import Path
w=Path(__file__).resolve().parent
repo=w/'candidate'
shipping=w/'shipping-candidate'
vendor='$SYNTHESIS_INSTALL/bin/vivado'
env=dict(os.environ,TMPDIR=str(w/'tmp'),PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0')
env['PATH']='$SYNTHESIS_INSTALL/bin:$BUILD_ENV/bin:'+env['PATH']
(w/'tmp').mkdir(exist_ok=True)
rows=[]
def run(name,args,cwd=repo,required=True):
    assert shutil.disk_usage(w).free > 30*1024**3
    start=time.time();print('START',name,time.strftime('%H:%M:%S'),flush=True)
    with (w/(name+'.log')).open('w') as log:
        rc=subprocess.run(args,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
    (w/(name+'.rc')).write_text(str(rc)+'\n')
    rows.append(dict(name=name,argv=list(map(str,args)),cwd=str(cwd),rc=rc,seconds=round(time.time()-start,1)))
    (w/'resource-results.json').write_text(json.dumps(rows,indent=2)+'\n')
    print('END',name,rc,flush=True)
    if required and rc: raise SystemExit(rc)
    return rc

def vendor_run(name,folder,script):
    return run(name,['flock','$SYNTHESIS_LOCK',vendor,'-mode','batch','-source',script,'-nojournal','-log','baseline.log'],folder)

assert (w/'prepare-candidate.rc').read_text().strip()=='0'
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()
assert head=='e2cd089ce2d902c73a5f7c6ae5bcee3aa84461bd'
instrument=w/'maap-ooc-candidate';instrument.mkdir()
(instrument/'run.tcl').write_text(f'set_param general.maxThreads 1\nset_param synth.maxThreads 1\nsource {{{repo}/syn/ooc/milan_datapath_ooc.tcl}}\nquit\n')
vendor_run('maap-ooc-candidate',instrument,'run.tcl')
lines=(instrument/'util_hier_base.rpt').read_text().splitlines()
hdr=next([c.strip() for c in l.split('|')][1:-1] for l in lines if 'Instance' in l and 'Total LUTs' in l)
r=next(r for r in ([c.strip() for c in l.split('|')][1:-1] for l in lines if 'maap_engine' in l) if r[0]=='g_maap.maap_engine')
lut,ff=int(r[hdr.index('Total LUTs')]),int(r[hdr.index('FFs')])
ceiling=dict(head=head,lut=lut,ff=ff,base_lut=439,base_ff=280,delta_lut=lut-439,delta_ff=ff-280,pass_ceiling=lut<=499 and ff<=340)
(w/'maap-ceiling.json').write_text(json.dumps(ceiling,indent=2)+'\n');print(ceiling,flush=True)
if not ceiling['pass_ceiling']:raise SystemExit(10)
# Only the actual vendor invocation holds the exclusive lock.
run('parser',['flock','$SYNTHESIS_LOCK','python3','scripts/xvlog_gate.py','--check'])
gate=shipping/'ax7101/gateware'
vendor_run('candidate-route',gate,'baseline_integrated.tcl')
run('candidate-route-check',['python3','syn/ooc/pp_resource_gate.py','check',str(gate),'--endpoint','route-1x1'])
eight=shipping/'ax8x8/gateware';rtl=shipping/'ax8x8-rtl';rtl.mkdir()
for p in eight.iterdir():
    if p.suffix in ('.xdc','.init'):shutil.copy2(p,rtl/p.name)
lines=(eight/'baseline_integrated.tcl').read_text().splitlines();idx=next(i for i,l in enumerate(lines) if l.startswith('synth_design '))
(rtl/'rtl.tcl').write_text('\n'.join(lines[:idx]+[lines[idx]+' -rtl -rtl_skip_mlo','quit'])+'\n')
vendor_run('rtl-8x8',rtl,'rtl.tcl')
for shape,integrated,endpoint in [('ax7101',gate,'ooc-1x1'),('ax8x8',rtl,'ooc-8x8')]:
    out=shipping/(shape+'-ooc')
    run(shape+'-prepare-ooc',['python3','syn/ooc/pp_baseline.py',str(shipping/shape/'gateware'),'--single-thread-synthesis','--integrated-clock','--output',str(out),'--integrated-log',str(integrated/'baseline.log')])
    vendor_run(shape+'-ooc',out,'baseline_ooc.tcl')
    run('candidate-'+endpoint+'-check',['python3','syn/ooc/pp_resource_gate.py','check',str(out),'--endpoint',endpoint])
print("all resource measurements passed",flush=True)
