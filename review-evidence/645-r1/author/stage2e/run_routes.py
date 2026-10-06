import os, json, subprocess, importlib.util, shutil, hashlib
from pathlib import Path
root=Path(os.environ['REPO']); work=Path(os.environ['STAGE_ROOT']); route=work/'route'
gate=route/'ax7101/gateware'
spec=importlib.util.spec_from_file_location('baseline',root/'syn/ooc/pp_baseline.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
source=(gate/'alinx_ax7101.tcl').read_text()
_,tail=b.split_once(source,'# Add pre-optimize commands')
tail,_=b.split_once(tail,'# Bitstream generation')
old='place_design -directive ExtraPostPlacementOpt';assert tail.count(old)==1
jobs=[('ExtraPostPlacementOpt',gate,'baseline_integrated.tcl')]
for directive in ('AltSpreadLogic_high','ExtraTimingOpt'):
    output=route/('ax7101-'+directive);output.mkdir(exist_ok=True)
    shutil.copy2(gate/'alinx_ax7101.xdc',output)
    script='set_param general.maxThreads 32\n'
    script+=f'open_checkpoint {{{gate}/alinx_ax7101_synth.dcp}}\n'
    script+=tail.replace(old,'place_design -directive '+directive)
    script+=b.REPORTS+b.PP_REPORTS+b.SCOPE_TIMING+'\nquit\n'
    (output/'baseline_implementation.tcl').write_text(script)
    jobs.append((directive,output,'baseline_implementation.tcl'))
for directive,cwd,script in jobs:
    print('START',directive,flush=True)
    argv=['flock','$VIVADO_LOCK',os.environ['VIVADO_EXE'],'-mode','batch','-source',script,'-nojournal','-log','baseline.log']
    with (work/(directive+'.log')).open('w') as log:
        rc=subprocess.run(argv,cwd=cwd,stdout=log,stderr=subprocess.STDOUT).returncode
    (work/(directive+'.rc')).write_text(str(rc)+'\n')
    print('DONE',directive,rc,flush=True)
    if rc: raise SystemExit(rc)
print('All three baseline implementation processes completed',flush=True)
