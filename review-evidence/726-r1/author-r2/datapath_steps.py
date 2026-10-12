import argparse,json,os,shlex,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--suite",type=Path,required=True);p.add_argument("--logs",type=Path,required=True);p.add_argument("--list",action="store_true");p.add_argument("indices",type=int,nargs="*");a=p.parse_args()
a.logs.mkdir(parents=True,exist_ok=True)
raw=subprocess.check_output(["make","-s","-n","run"],cwd=a.suite,text=True)
commands=[]
for line in raw.replace("\\\n"," ").splitlines():
 v=shlex.split(line)
 if not v:continue
 if v[0]=="verilator":commands.append(("build",v))
 elif v[0].startswith("./"):commands.append(("run",v))
 elif v[:3]==["exec","python3","sim_pool.py"]:
  commands.extend(("run",[x]) for x in v if x.startswith("./"))
 elif v[0]=="python3" and v[1] in ("gen_divergent_shape.py","render_mutants.py"):
  commands.append(("aux",v))
 elif v[0].startswith("VERILATOR=") and v[1:3]==["python3","stream_counters.py"]:
  commands.append(("aux",["env",*v]))
(a.logs/"commands.json").write_text(json.dumps(commands,indent=2)+"\n")
if a.list:
 for i,(kind,v) in enumerate(commands):
  label=v[v.index("-o")+1] if "-o" in v else " ".join(v)
  print(i,kind,label)
else:
 for i in a.indices:
  kind,v=commands[i]
  with (a.logs/f"{i:02d}-{kind}.log").open("w") as log:
   result=subprocess.run(v,cwd=a.suite,stdout=log,stderr=subprocess.STDOUT)
  (a.logs/f"{i:02d}-{kind}.rc").write_text(str(result.returncode)+"\n")
  print(i,kind,"rc",result.returncode,flush=True)
  if result.returncode:raise SystemExit(result.returncode)
