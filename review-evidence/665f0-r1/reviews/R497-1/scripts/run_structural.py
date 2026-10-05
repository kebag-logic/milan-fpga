#!/usr/bin/env python3
import pathlib,subprocess,sys,os,concurrent.futures,shlex
p=pathlib.Path(__file__).resolve().parents[1];r=pathlib.Path(sys.argv[1]).resolve();v=sys.argv[2];env=dict(os.environ,TMPDIR=str(p/'scratch'),PYTHONDONTWRITEBYTECODE='1');rtl=r/'hdl/milan/mailbox';x=p/'scratch/xvlog';x.mkdir(exist_ok=True)
files=[str(rtl/n) for n in ['KL_mbx_pkg.sv','KL_mbx_ring.sv','KL_mbx_rx.sv','KL_mbx_tx.sv','KL_mbx_evt.sv','KL_mbx.sv','KL_mbx_wb.sv','KL_mbx_axil.sv']]
def run(name,cmd,cwd):
 with (p/'receipts'/f'{name}.log').open('w') as f:
  print('COMMAND: '+shlex.join(cmd),file=f,flush=True);rc=subprocess.run(cmd,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=550).returncode
 (p/'receipts'/f'{name}.rc').write_text(str(rc)+'\n');print(name,rc,flush=True);return rc
# Vendor analysis is isolated from all other heavy builds.
run('xvlog',['flock','$VIVADO_LOCK',sys.argv[3],'-sv',*files],x)
def probe():
 cmd=[v,'--cc','--exe','--build','-j','4','--top-module','KL_mbx_axil','--Mdir',str(p/'scratch/axil'),'--prefix','VKL_mbx_axil',files[0],files[-1],str(p/'scripts/axil_probe.cpp'),'-o','probe']
 if run('axil-probe-build',cmd,r)==0:run('axil-probe',[str(p/'scratch/axil/probe')],r)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 tasks=[pool.submit(probe),pool.submit(run,'focused-yosys',['bash','syn/yosys/run.sh','--top','KL_mbx','--top','KL_mbx_wb','--top','KL_mbx_axil','--no-structural','--results',str(p/'scratch/yosys-results')],r),pool.submit(run,'focused-lint',[v,'--lint-only','-Wall','-Wno-fatal','--top-module','KL_mbx',*files],r)]
 for t in tasks:t.result()
