#!/usr/bin/env python3
"""Bounded elaboration check at both accepted pins and both lowering releases.
Usage: probe_nvm_guard.py CHECKOUT PACKET SIMULATOR SV2V12 SV2V13
"""
import concurrent.futures,os,pathlib,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve(); packet=pathlib.Path(sys.argv[2]).resolve(); sim=sys.argv[3]
versions={'012':pathlib.Path(sys.argv[4]).resolve(),'013':pathlib.Path(sys.argv[5]).resolve()}
for label,exe in versions.items(): print(label,subprocess.check_output([str(exe),'--version'],text=True).strip(),flush=True)
pins={'old':'2ad2f845','current':'2cbed0a9'}
paths=['hdl/packet_engine/KL_pp_nvm_port.sv','tb/nvm_port/elab_bounds.sh']
for path in paths:
 vals=[subprocess.check_output(['git','-C',str(root/'protocol-processor'),'show',pin+':'+path]) for pin in pins.values()]
 assert vals[0]==vals[1];print('byte-identical at both pins',path,flush=True)
def run(item):
 name,pin,label,exe=item; work=packet/'scratch'/('nvm-'+name+'-'+label);work.mkdir(exist_ok=True)
 for path in paths:
  dest=work/path;dest.parent.mkdir(parents=True,exist_ok=True)
  dest.write_bytes(subprocess.check_output(['git','-C',str(root/'protocol-processor'),'show',pin+':'+path]))
 bindir=work/'bin';bindir.mkdir(exist_ok=True)
 if not (bindir/'sv2v').exists():(bindir/'sv2v').symlink_to(exe)
 env=dict(os.environ,VERILATOR=sim,PATH=str(bindir)+':'+os.environ['PATH'],TMPDIR=str(packet/'scratch'))
 result=subprocess.run(['bash','elab_bounds.sh'],cwd=work/'tb/nvm_port',env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (packet/('nvm-'+name+'-'+label+'.log')).write_text(result.stdout)
 (packet/('nvm-'+name+'-'+label+'.rc')).write_text(str(result.returncode)+'\n')
 print(name,label,'rc',result.returncode,flush=True)
 assert result.returncode==(1 if label=='012' else 0)
 assert ('failed, but not at the guard' in result.stdout) if label=='012' else ('stops at the guard' in result.stdout)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 list(pool.map(run,[(n,p,l,e) for n,p in pins.items() for l,e in versions.items()]))
print('PASS pre-existing lowering-version difference reproduced at both pins')
