import json, os, shlex, shutil, subprocess, sys
from pathlib import Path
repo=Path(sys.argv[1]).resolve()
work=Path(sys.argv[2]).resolve(); work.mkdir(parents=True,exist_ok=True)
assert shutil.disk_usage(work).free > 30*1024**3
python='<litex-env>/bin/python3'
sdk=Path('<sdk>')
env=dict(os.environ,TMPDIR=str(work),PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0',LITEX_ENV_CC_TRIPLE='riscv32-linux',MILAN_RV32_CC=str(sdk/'bin/riscv32-linux-gcc'))
env['PATH']=str(Path(python).parent)+os.pathsep+str(sdk/'bin')+os.pathsep+env['PATH']
rows=[]
def run(name,args,cwd=repo):
 print('START',name,flush=True)
 with (work/(name+'.log')).open('w') as log:
  rc=subprocess.run(args,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
 (work/(name+'.rc')).write_text(str(rc)+'\n')
 rows.append(dict(name=name,argv=list(map(str,args)),rc=rc))
 (work/'prepare-results.json').write_text(json.dumps(rows,indent=2)+'\n')
 if rc:raise SystemExit(rc)
run('sdk',['python3','scripts/ci_rv32_sdk.py','--destination',str(sdk),'--verify-only'])
run('recipe-selftest',['python3','syn/ooc/pp_baseline.py','--selftest'])
for d in ['builder','roms']:(work/d).mkdir(exist_ok=True)
for target,link in [(work/'builder',repo/'sw/builder/out'),(work/'roms/ltn_rom.hex',repo/'configs/generated/ltn_rom.hex'),(work/'roms/ucode.hex',repo/'configs/generated/ucode.hex')]:
 assert not link.exists() and not link.is_symlink(),link
 link.symlink_to(target)
for shape in ['ax7101','ax8x8']:
 run(shape+'-dry-run',['bash','sw/litex/build.sh',shape,'--dry-run'])
 lines=[l for l in (work/(shape+'-dry-run.log')).read_text().splitlines() if 'exec python3 milan_soc.py ' in l]
 assert len(lines)==1
 argv=shlex.split(lines[0].split('exec python3 ',1)[1]);argv.remove('--build')
 argv[argv.index('--output-dir')+1]=str(work/shape)
 (work/(shape+'-argv.json')).write_text(json.dumps(argv,indent=2)+'\n')
 run(shape+'-elaboration',[python,*argv],repo/'sw/litex')
 run(shape+'-recipe',['python3','syn/ooc/pp_baseline.py',str(work/shape/'gateware'),'--single-thread-synthesis',*(['--synthesis-only'] if shape=='ax8x8' else [])])
print('shipping exports prepared',flush=True)
