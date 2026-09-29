"""Record a bounded foreground command; lock each bench action."""
import json,subprocess,sys,time
from pathlib import Path
name,limit,mode,*args=sys.argv[1:];limit=int(limit)
p=Path(__file__).resolve().parent.parent
command=["rtk","proxy","timeout",str(limit)+"s"]
if mode=="bench":command += ["flock","-w","5","/tmp/milan-bench.lock","timeout",str(limit-6)+"s"]
command+=args
t0=time.time();r=subprocess.run(command,capture_output=True,timeout=limit+2);t1=time.time()
text=r.stdout.decode(errors="replace")+r.stderr.decode(errors="replace")
for value in args:
 if value.startswith("<private-host-prefix>"):text=text.replace(value,"<remote-role>")
text=text.replace("<host-iface>","<controller-interface>")
(p/name).write_text(text)
with (p/"actions.jsonl").open("a") as f:f.write(json.dumps(dict(artifact=name,start=t0,end=t1,rc=r.returncode))+"\n")
print(text);print("return code",r.returncode)
sys.exit(r.returncode)
