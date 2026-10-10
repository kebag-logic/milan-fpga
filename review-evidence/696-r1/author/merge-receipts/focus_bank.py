"""Lint, behaviour, focused MAAP checks, firmware bank and portability at one exact head, one at a time.

Verilator builds go through the lane's two-slot build semaphore (merge/bin/verilator), shared with the
parent sweep, so no more than two compilations run at once across this lane's jobs.
"""
import json,os,shutil,signal,subprocess,sys,time
from pathlib import Path
signal.signal(signal.SIGHUP,signal.SIG_DFL)
w=Path(__file__).resolve().parent
repo=Path(sys.argv[1]).resolve(); tag=sys.argv[2]
f=w/('focus-'+tag);f.mkdir(exist_ok=True);(f/'tmp').mkdir(exist_ok=True)
head=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()
env=dict(os.environ,TMPDIR=str(f/'tmp'),PYTHONDONTWRITEBYTECODE='1',VERILATOR=str(w/'bin/verilator'),VERILATOR_JOBS='2',MAKEFLAGS='-j8',JOBS='4',POOL='2',SIM_JOBS='2',MILAN_RV32_CC='<sdk>/bin/riscv32-linux-gcc')
env['PATH']=str(w/'bin')+os.pathsep+'<sdk>/bin'+os.pathsep+'<litex-env>/bin'+os.pathsep+env['PATH']
lint_env=dict(env,PATH='<pinned-compiler>'+os.pathsep+env['PATH'])
rows=[]
def run(name,args,cwd=repo,e=env):
 assert shutil.disk_usage(f).free>30*1024**3
 print('START',name,time.strftime('%H:%M:%S'),flush=True);start=time.time()
 with (f/(name+'.log')).open('w') as out:
  rc=subprocess.run(args,cwd=cwd,env=e,stdout=out,stderr=subprocess.STDOUT).returncode
 (f/(name+'.rc')).write_text(str(rc)+'\n')
 rows.append(dict(name=name,argv=[str(a) for a in args],cwd=str(cwd),rc=rc,seconds=round(time.time()-start,1),head=head))
 (f/'results.json').write_text(json.dumps(rows,indent=2)+'\n');print(name,rc,flush=True)
 return rc
steps=[
 ('lint',['python3','scripts/lint_rtl.py','--check','--self-test','--jobs','2'],repo,lint_env),
 ('behave',['behave','--no-capture','-f','plain'],repo/'tests',env),
 ('maap-unit',['make','-j8','-C','tb/verilator/maap','run','MDIR='+str(f/'unit-build')],repo,env),
 ('maap-integration-build',['make','-j8','-C','tb/verilator/maap','integration-build','DP_MDIR='+str(f/'integration-build')],repo,env),
 ('maap-integration',[str(f/'integration-build/maap_integration')],None,env),
 ('maap-mutants',['python3','tb/verilator/maap/mutants.py'],repo,env),
 ('maap-coverage',['make','-j8','-C','tb/verilator/maap','coverage','COV_MDIR='+str(f/'coverage-build')],repo,env),
 ('maap-differential',['python3','sw/firmware/ctrl/test/maap_differential.py','--self-test','--keep',str(f/'differential')],repo,env),
 ('firmware',['python3','sw/firmware/ctrl/test/test_ctrl_firmware.py','--require-rv32','--self-test','--jobs','2'],repo,env),
 ('portability',['bash','syn/yosys/run.sh','--results',str(f/'portability-results')],repo,env),
 ('field-campaigns',['make','-j8','-C','tb/verilator/tsn_fuzz'],repo,dict(env,TSN_GEN_ROOT='<field-generator>')),
]
# The field generator must be the clean revision rtl.yml pins.
import hashlib,re
gen=Path('<field-generator>')
pin=re.search(r'TSN_GEN_REV:\s*([0-9a-f]{40})',(repo/'.github/workflows/rtl.yml').read_text()).group(1)
assert subprocess.check_output(['git','-C',str(gen),'rev-parse','--show-toplevel'],text=True).strip()==str(gen)
generator=dict(pin=pin,revision=subprocess.check_output(['git','-C',str(gen),'rev-parse','HEAD'],text=True).strip(),
 clean=not subprocess.check_output(['git','-C',str(gen),'status','--short'],text=True).strip(),
 files={p:hashlib.sha256((gen/p).read_bytes()).hexdigest() for p in ['build/traffic-gen/packet_gen','build/traffic-gen/libtraffic_gen.so.0','build/logic/libprotocol_logic.so.0','build/parser/libprotocol_parser.so.0']})
(f/'field-generator.json').write_text(json.dumps(generator,indent=2)+'\n')
assert generator['revision']==pin and generator['clean'],generator
only=set(sys.argv[3:])
for name,args,cwd,e in steps:
 if only and name not in only:continue
 run(name,args,cwd or f/'integration-build',e)
status=subprocess.run(['git','-C',str(repo),'status','--short'],capture_output=True,text=True).stdout
(f/'tree-status.txt').write_text(status)
bad=[r['name'] for r in rows if r['rc']]
print('FAILED:',bad) if bad else print('all',len(rows),'rc 0')
raise SystemExit(1 if bad or status else 0)
