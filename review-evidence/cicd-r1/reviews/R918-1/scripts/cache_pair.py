#!/usr/bin/env python3
"""Compare CRF unit output from uncached, cold-cache and warm-cache builds."""
import pathlib,subprocess,os,json,hashlib,sys,time
P=pathlib.Path(__file__).resolve().parents[1];S=P/'scratch';T=S/'head';D=S/'cache-unit';D.mkdir(exist_ok=True)
env=dict(os.environ,OBJCACHE='ccache',CCACHE_DIR=str(S/'cache-store'),CCACHE_CONFIGPATH=str(S/'cache-config'),MAKEFLAGS='--no-print-directory')
(S/'cache-config').write_text('max_size = 1G\n')
R=P/'receipts';rows=[]
def run(name,argv,cwd):
 with (R/(name+'.log')).open('w') as f:
  start=time.monotonic();rc=subprocess.run(argv,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
 rows.append({'name':name,'argv':argv,'rc':rc,'wall_seconds':time.monotonic()-start});assert rc==0,rows[-1]
run('cache-uncached-output',[str(T/'tb/verilator/crf_rx/obj_dir/Vcrf_rx_sim')],T/'tb/verilator/crf_rx')
run('cache-cold-build',['make','-j16','unit-build','UNIT_MDIR='+str(D),'VERILATOR='+str(S/'simulator'),'OBJCACHE=ccache'],T/'tb/verilator/crf_rx')
run('cache-cold-output',[str(D/'Vcrf_rx_sim')],T/'tb/verilator/crf_rx')
run('cache-cold-stats',['ccache','--show-stats'],D)
for f in D.glob('*.o'):f.unlink()
for f in D.glob('*.a'):f.unlink()
(D/'Vcrf_rx_sim').unlink()
run('cache-warm-build',['make','-j2','-f','VKL_crf_rx.mk','Vcrf_rx_sim','OBJCACHE=ccache'],D)
run('cache-warm-output',[str(D/'Vcrf_rx_sim')],T/'tb/verilator/crf_rx')
run('cache-warm-stats',['ccache','--show-stats'],D)
outputs=[(R/('cache-'+v+'-output.log')).read_bytes() for v in ('uncached','cold','warm')]
assert outputs[0]==outputs[1]==outputs[2]
(R/'cache-replay.json').write_text(json.dumps({'identical':True,'sha256':hashlib.sha256(outputs[0]).hexdigest(),'commands':rows},indent=2)+'\n')
print('Cache replay: uncached, cold and warm outputs byte-identical')
