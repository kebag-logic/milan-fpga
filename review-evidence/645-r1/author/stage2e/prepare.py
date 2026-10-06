import os, json, shlex, subprocess, hashlib, re
from pathlib import Path
root=Path(os.environ['REPO'])
work=Path(os.environ['STAGE_ROOT'])/'route'
work.mkdir(parents=True,exist_ok=True)
env=os.environ.copy()
env['PYTHONDONTWRITEBYTECODE']='1'
env['PYTHONHASHSEED']='0'
env['MAKEFLAGS']='-j16'
def run(name,argv,cwd=root):
    with (work/(name+'.log')).open('w') as log:
        rc=subprocess.run(argv,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
    (work/(name+'.rc')).write_text(str(rc)+'\n')
    print(name,rc,flush=True)
    if rc: raise SystemExit(rc)
for sub in ['protocol-processor','gptp-processor','third_party/verilog-axis']:
    where=root/sub
    top=subprocess.check_output(['git','-C',str(where),'rev-parse','--show-toplevel'],text=True).strip()
    assert Path(top)==where
    print(sub,subprocess.check_output(['git','-C',str(where),'rev-parse','HEAD'],text=True).strip(),flush=True)
run('sdk-verify',['python3','-B','scripts/ci_rv32_sdk.py','--destination',os.environ['SDK'],'--verify-only'])
run('baseline-selftest',['python3','-B','syn/ooc/pp_baseline.py','--selftest'])
env['LITEX_ENV_CC_TRIPLE']=subprocess.check_output(['python3','-B','-c', 'import sys; sys.path.insert(0,"scripts"); from ci_rv32_sdk import COMPILER; print(COMPILER.removeprefix("bin/").removesuffix("-gcc"))'],cwd=root,text=True,env=env).strip()
(work/'builder').mkdir(exist_ok=True)
(work/'roms').mkdir(exist_ok=True)
for link,target in [(root/'sw/builder/out',work/'builder'),(root/'configs/generated/ltn_rom.hex',work/'roms/ltn_rom.hex'),(root/'configs/generated/ucode.hex',work/'roms/ucode.hex')]:
    assert not link.exists() and not link.is_symlink(),link
    link.symlink_to(target)
run('ax7101-dry-run',['bash','sw/litex/build.sh','ax7101','--dry-run'])
lines=[x for x in (work/'ax7101-dry-run.log').read_text().splitlines() if 'exec python3 milan_soc.py ' in x]
assert len(lines)==1
argv=shlex.split(lines[0].split('exec python3 ',1)[1]); argv.remove('--build')
argv[argv.index('--output-dir')+1]=str(work/'ax7101')
(work/'ax7101-argv.json').write_text(json.dumps(argv,indent=2)+'\n')
run('ax7101-elaboration',[os.environ['LITEX_PYTHON'],*argv],root/'sw/litex')
run('baseline-prepare',['python3','-B','syn/ooc/pp_baseline.py',str(work/'ax7101/gateware')])
print('PREPARED; keep image links through synthesis',flush=True)
