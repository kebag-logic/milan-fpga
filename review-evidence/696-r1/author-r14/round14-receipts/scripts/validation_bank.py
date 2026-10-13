import concurrent.futures,json,os,shutil,signal,subprocess,time
from pathlib import Path
for sig in (signal.SIGHUP,signal.SIGINT,signal.SIGQUIT): signal.signal(sig,signal.SIG_DFL)
w=Path(__file__).resolve().parent;repo=w/'candidate';out=w/'validation';out.mkdir(exist_ok=True)
env=dict(os.environ,TMPDIR=str(w/'tmp'),PYTHONDONTWRITEBYTECODE='1',PYTHON_CPU_COUNT='4',VERILATOR=str(w/'bin/verilator'),VERILATOR_JOBS='2',MAKEFLAGS='-j8',JOBS='4',POOL='2',SIM_JOBS='2',LAW_BOUNDARY_JOBS='4',START_JOBS='4',MILAN_RV32_CC='$RV32_SDK/bin/riscv32-linux-gcc')
env['PATH']=str(w/'bin')+':$DOC_ENV/bin:$RV32_SDK/bin:'+env['PATH']
while not (w/'resource-bank.rc').exists():time.sleep(10)
if (w/'resource-bank.rc').read_text().strip()!='0':raise SystemExit('resource validation did not pass')
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()
assert head=='e2cd089ce2d902c73a5f7c6ae5bcee3aa84461bd'
for sub in ('protocol-processor','gptp-processor','third_party/verilog-axis','third_party/lwSRP','third_party/tsn-c-stack'):
 p=repo/sub;assert Path(subprocess.check_output(['git','-C',str(p),'rev-parse','--show-toplevel'],text=True).strip())==p

def run(name,cmd,cwd=repo):
 assert shutil.disk_usage(w).free>30*1024**3
 start=time.time();print('START',name,time.strftime('%H:%M:%S'),flush=True)
 with (out/(name+'.log')).open('w') as f:r=subprocess.run(cmd,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT)
 (out/(name+'.rc')).write_text(str(r.returncode)+'\n')
 row=dict(name=name,argv=list(map(str,cmd)),cwd=str(cwd),head=head,rc=r.returncode,seconds=round(time.time()-start,1))
 (out/(name+'.json')).write_text(json.dumps(row,indent=2)+'\n');print('END',name,r.returncode,flush=True)
 return row

def execute(steps):
 rows=[]
 for name,cmd,cwd in steps:
  row=run(name,cmd,cwd);rows.append(row)
  if row['rc']: break
 return rows

def focus():
 steps=[
  ('lint',['python3','scripts/lint_rtl.py','--check','--self-test','--jobs','2'],repo),
  ('maap',['make','-j8','-C','tb/verilator/maap','MDIR='+str(out/'unit')],repo),
  ('maap-integration-build',['make','-j8','-C','tb/verilator/maap','integration-build','DP_MDIR='+str(out/'integration')],repo),
  ('maap-integration',[str(out/'integration/maap_integration')],out/'integration'),
  ('maap-coverage',['make','-j8','-C','tb/verilator/maap','coverage','COV_MDIR='+str(out/'coverage')],repo),
  ('maap-differential',['python3','sw/firmware/ctrl/test/maap_differential.py','--self-test','--keep',str(out/'differential')],repo),
 ]
 steps += [(suite,['make','-j8','-C','tb/verilator/'+suite],repo) for suite in ['milan_dp','mbx','pp_shadow','capture_coherence','milan_dp_mclk','milan_dp_render']]
 steps += [('portability',['bash','syn/yosys/run.sh','--results',str(out/'portability-results')],repo)]
 return execute(steps)

def firmware():
 return execute([
  ('firmware',['python3','sw/firmware/ctrl/test/test_ctrl_firmware.py','--require-rv32','--self-test','--jobs','2'],repo),
  ('store',['python3','sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py','--require-rv32','--jobs','2'],repo),
  ('coverage-selftest',['python3','sw/firmware/gtest/fw_coverage.py','--selftest'],repo),
  ('firmware-coverage',['python3','sw/firmware/gtest/fw_coverage.py','--check','--jobs','2'],repo),
  ('boundary',['python3','sw/firmware/ctrl/test/ctrl_boundary.py','--require-rv32','--selftest'],repo),
  ('control-memory',['$BUILD_ENV/bin/python3','sw/litex/test_ctrl_memory.py'],repo),
  ('firmware-shards',['python3','sw/firmware/ctrl/test/test_ctrl_firmware_shards.py'],repo),
  ('builder',['python3','sw/builder/test_builder.py','--require-rv32','--require-elaboration'],repo),
  ('behaviour',['python3','-m','behave','--no-capture','-f','plain'],repo/'tests'),
 ])
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 a=pool.submit(focus);b=pool.submit(firmware);rows=[*a.result(),*b.result()]
(out/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
raise SystemExit(any(r['rc'] for r in rows))
