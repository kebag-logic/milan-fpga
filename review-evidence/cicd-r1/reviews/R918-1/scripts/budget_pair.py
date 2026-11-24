#!/usr/bin/env python3
"""Build one 8x8/1if CPU fixture and compare its output with two host optimisation levels."""
import os,pathlib,sys,subprocess,json,hashlib,concurrent.futures
if os.environ.get('PYTHONHASHSEED') != '0':
 os.environ['PYTHONHASHSEED']='0';os.execv(sys.executable,[sys.executable,*sys.argv])
P=pathlib.Path(__file__).resolve().parents[1];S=P/'scratch';T=S/'head'
# Arguments are existing product dependencies; the CPU package is copied into scratch before use.
litex=pathlib.Path(sys.argv[1]);sdk=pathlib.Path(sys.argv[2]);simulator=pathlib.Path(sys.argv[3])
os.environ.update(PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0',COURSIER_MODE='offline',SBT_OPTS='-Dsbt.offline=true -Dsbt.task.cpus=2',JAVA_TOOL_OPTIONS='-XX:ActiveProcessorCount=2 -Xmx2g',LITEX_ENV_CC_TRIPLE='riscv32-buildroot-linux-gnu',OBJCACHE='',TMPDIR=str(S/'tmp'))
os.environ['PYTHONPATH']=':'.join([str(S/'deps/pythondata-cpu-vexiiriscv')]+[str(x) for x in litex.iterdir() if x.is_dir() and x.name!='pythondata-cpu-vexiiriscv'])
os.environ['PATH']=str(sdk/'bin')+':'+str(simulator.parent)+':'+os.environ['PATH']
sys.path[:0]=[str(T/'tb/verilator/ctrl_service_budget')]+os.environ['PYTHONPATH'].split(':')
import build, scenario
build.JOBS=2
D=S/'budget';spec=build.build(D,'endstation_ax7101_8x8',1)
# Firmware/model inputs are unchanged by this PR. Recompile only the host testbench object.
N=D/'native';(N/'Vsim').rename(N/'Vsim-O3')
(N/'sim_main.o').unlink()
with (P/'receipts/budget.Os-build.log').open('w') as f:
 r=subprocess.run(['make','-j2','-C',str(N),'-f','Vsim.mk','Vsim','OPT_FAST=-Os'],stdout=f,stderr=subprocess.STDOUT)
assert r.returncode==0
(N/'Vsim').rename(N/'Vsim-Os')
point=scenario.point('8x8-1if',spec)
group=scenario.fixture_groups(point)[0]
script=D/'fixture.txt';script.write_text(group.script())
# Match the driver's initial flash selection.
flash=spec.get('flash_image') or '-'
def run(level):
 out=P/'receipts'/('budget.'+level+'.output.log')
 with out.open('w') as f:
  proc=subprocess.run([str(N/('Vsim-'+level)),str(script),flash],cwd=D/'gateware',stdout=f,stderr=subprocess.STDOUT)
 return {'level':level,'rc':proc.returncode,'md5':hashlib.md5(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:results=list(ex.map(run,['Os','O3']))
(P/'receipts/budget-comparison.json').write_text(json.dumps(results,indent=2)+'\n')
assert all(x['rc']==0 for x in results),results
assert results[0]['md5']==results[1]['md5'],results
print(json.dumps(results),flush=True)
