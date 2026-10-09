#!/usr/bin/env python3
import concurrent.futures,io,json,os,pathlib,shutil,subprocess,sys,tarfile,time
r=pathlib.Path(sys.argv[1]).resolve();p=pathlib.Path(sys.argv[2]).resolve();w=p/"scratch/round8-replay";w.mkdir(exist_ok=True)
e=dict(os.environ);e.update(json.loads((p/"scratch/environment.json").read_text()))
for k in ("CPATH","CPLUS_INCLUDE_PATH","C_INCLUDE_PATH","LIBRARY_PATH","PKG_CONFIG_ALLOW_SYSTEM_CFLAGS","PKG_CONFIG_ALLOW_SYSTEM_LIBS"):e.pop(k,None)
head=subprocess.check_output(["git","rev-parse","HEAD"],cwd=r,text=True).strip()
old=w/"old";old.mkdir(exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(["git","archive","68070cb5"],cwd=r))) as t:t.extractall(old,filter="data")
plain=p/"scratch/sdk/gtest/lib/pkgconfig";system=w/"pkgconfig";shutil.copytree(plain,system,dirs_exist_ok=True)
for path in system.glob("*.pc"):path.write_text(path.read_text().replace("-I${includedir}","-isystem ${includedir}"))
e.update(PC_PLAIN=str(plain),PC_ISYSTEM=str(system))
s=p/"scratch/prior-public/R556-7/scripts";rows=[]
def run(name,cmd,legacy=False):
 env=dict(e)
 if legacy:env.update(CPLUS_INCLUDE_PATH=str(p/"scratch/sdk/gtest/include"),LIBRARY_PATH=str(p/"scratch/sdk/gtest/lib"))
 start=time.monotonic()
 with (w/(name+".log")).open("w") as log:rc=subprocess.run(cmd,cwd=r,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
 (w/(name+".rc")).write_text(str(rc)+"\n");row=dict(name=name,rc=rc,seconds=round(time.monotonic()-start,2));rows.append(row);print(row,flush=True)
commands=[("assertions",[sys.executable,str(s/"probe_assertions.py"),str(r),str(old),str(w/"assertions")],False),("comments",[sys.executable,str(s/"probe_comment_gate.py"),str(r),str(old),str(w/"comments")],False),("dependencies",["sh",str(s/"probe_dependency.sh"),str(r),str(w/"dependencies")],False),("spi-tree",["sh",str(s/"probe_spi_tree.sh"),str(r),head,str(w/"spi-tree")],True)]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(lambda x:run(*x),commands))
(w/"results.json").write_text(json.dumps(rows,indent=2)+"\n")
