# SPDX-License-Identifier: Apache-2.0
import os, pathlib, subprocess, json, threading, time
PACKET=pathlib.Path(__file__).resolve().parents[1]
SOURCE=pathlib.Path(os.environ.get("REVIEW_SOURCE",os.getcwd())).resolve()
SCRATCH=PACKET/"scratch"
PREFIX=SCRATCH/"prefix"
BUILD_LOCK=threading.Lock()
LOG_LOCK=threading.Lock()
ENV=os.environ.copy()
ENV.update(PYTHONDONTWRITEBYTECODE="1",LD_LIBRARY_PATH=str(PREFIX/"lib")+":"+ENV.get("LD_LIBRARY_PATH",""))
def clean(x):
 return str(x).replace(str(SOURCE),"$SOURCE").replace(str(PACKET),"$PACKET").replace(str(pathlib.Path.home()),"$USER")
def run(label,cmd,cwd=SOURCE,env=None,expected=0,timeout=500):
 cmd=list(map(str,cmd)); start=time.time()
 p=subprocess.run(cmd,cwd=cwd,env=env or ENV,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=timeout)
 out=clean(p.stdout)
 (PACKET/"receipts"/(label+".log")).write_text(out)
 (PACKET/"receipts"/(label+".rc")).write_text(str(p.returncode)+"\n")
 with LOG_LOCK:
  with (PACKET/"receipts/executions.jsonl").open("a") as f: f.write(json.dumps(dict(label=label,command=[clean(c) for c in cmd],cwd=clean(cwd),rc=p.returncode,seconds=round(time.time()-start,3)))+"\n")
 print(label+": rc="+str(p.returncode),flush=True)
 if expected is not None and p.returncode!=expected: raise RuntimeError(label+" failed: "+out[-1500:])
 return p.returncode,out
def build(label,directory):
 with BUILD_LOCK: return run(label,["make","-j16","-C",directory])
