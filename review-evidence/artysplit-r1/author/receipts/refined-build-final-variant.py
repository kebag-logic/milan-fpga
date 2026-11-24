"""Build a fresh variant, recording any independently benchmarked native-only optimization."""
import hashlib,json,sys
from pathlib import Path
root=Path.cwd();r=Path('$VALIDATION_STORAGE/artysplit-a829/r4/refined')
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'))
import build
from harness_slots import slot
out=Path(sys.argv[1]);variant=sys.argv[2]
benchmark=r/'native-optimization/result.json'
flags=[];receipt=None
if benchmark.exists():
 result=json.loads(benchmark.read_text())
 if result['status']=='PASS' and result['identical'] and result['speedup']>1.05:
  flags=['OPT_FAST=-O3','OPT_SLOW=-O3','OPT_GLOBAL=-O3']
  receipt=dict(path=str(benchmark),sha256=hashlib.sha256(benchmark.read_bytes()).hexdigest())
original=build.run
commands=[]
def native_only(argv,log,cwd=None):
 if argv[0]=='make' and argv[-3:]==['-f','Vsim.mk','Vsim']:
  argv=[*argv,*flags];commands.append(argv)
 return original(argv,log,cwd)
build.run=native_only
build.JOBS=8
with slot('service build '+variant):
 spec=build.build(out,'endstation_arty_current',1,variant=variant)
 spec['native_compilation']=dict(commands=commands,optimization_flags=flags,benchmark=receipt,
                                 scope='Host native code only; RV32 firmware and RTL inputs unchanged')
 (out/'build.json').write_text(json.dumps(spec,indent=2)+'\n')
 build.reused(out)
