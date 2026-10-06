#!/usr/bin/env python3
"""Complete the notification campaign and focused unit/document checks concurrently."""
import argparse,concurrent.futures,json,os,pathlib,subprocess,time,types,sys
P=pathlib.Path
ap=argparse.ArgumentParser();ap.add_argument('--packet',type=P,required=True);a=ap.parse_args();p=a.packet.resolve();s=p/'scratch';r=p/'receipts'
path=s/'campaign-tree/tb/pp_top/notify_mutants.py';m=types.ModuleType('notify_remainder');m.__file__=str(path);sys.modules[m.__name__]=m;exec(compile(path.read_text(),str(path),'exec'),m.__dict__)
focus={x.name for x in m.DOMAIN_NOTIFY+m.INTERFACE_ROWS+m.INTERFACE_DEPTH_PROBES};other=[x.name for x in m.MUTANTS if x.name not in focus];assert len(other)==56
env=dict(os.environ,TMPDIR=str(s),PYTHONDONTWRITEBYTECODE='1',MAKEFLAGS='-j16');wrapper=s/'compiler-cap'
items=[('notify-remainder',s/'campaign-tree',['python3',str(path),'--output',str(r/'notify-remainder'),'--verilator',str(wrapper),'--jobs','2','--only',*other]),('aecp-notify',s/'guards-tree/tb/aecp_notify',['make','-j16','run','VERILATOR='+str(wrapper)])]
def run(item):
 name,cwd,cmd=item;t=time.time()
 with (r/(name+'.log')).open('w') as f:rc=subprocess.run(cmd,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
 (r/(name+'.rc')).write_text(str(rc)+'\n');row={'name':name,'rc':rc,'seconds':round(time.time()-t,2),'cwd':str(cwd),'command':cmd};(r/(name+'-run.json')).write_text(json.dumps(row,indent=2)+'\n');print(json.dumps(row),flush=True);return rc
with concurrent.futures.ThreadPoolExecutor(3) as pool: codes=list(pool.map(run,items))
raise SystemExit(any(codes))
