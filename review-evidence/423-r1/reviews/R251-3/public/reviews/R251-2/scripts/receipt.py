"""Record unfiltered command bytes, argv, environment overrides and exit."""
import argparse, datetime, json, os, pathlib, subprocess, time
p=argparse.ArgumentParser()
p.add_argument('--out',type=pathlib.Path,required=True)
p.add_argument('--cwd',type=pathlib.Path,required=True)
p.add_argument('command',nargs=argparse.REMAINDER)
a=p.parse_args()
cmd=a.command[1:] if a.command[:1]==['--'] else a.command
assert cmd and cmd[0]=='rtk',cmd
a.out.parent.mkdir(parents=True,exist_ok=True)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
t=time.monotonic()
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with a.out.with_suffix('.stdout').open('wb') as o,a.out.with_suffix('.stderr').open('wb') as e:
 r=subprocess.run(cmd,cwd=a.cwd,env=env,stdout=o,stderr=e)
d={'argv':cmd,'cwd':str(a.cwd),'started_at':start,'duration_seconds':time.monotonic()-t,'exit':r.returncode,'environment_overrides':{'PYTHONDONTWRITEBYTECODE':'1'}}
a.out.with_suffix('.json').write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps(d))
raise SystemExit(r.returncode)
