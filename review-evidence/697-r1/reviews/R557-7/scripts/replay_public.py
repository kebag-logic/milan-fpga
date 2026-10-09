#!/usr/bin/env python3
"""Replay published probe bytes with bounded concurrent execution."""
import concurrent.futures,hashlib,io,json,os,pathlib,shutil,subprocess,sys,tarfile,time
root=pathlib.Path(sys.argv[1]).resolve();p=pathlib.Path(sys.argv[2]).resolve();w=p/"scratch/replays";w.mkdir(parents=True,exist_ok=True)
env=dict(os.environ);env.update(json.loads((p/"scratch/environment.json").read_text()));py=sys.executable
s=p/"scratch/prior-public/R557-6/scripts/prior";legacy=w/"legacy5"
for d in ["scripts","receipts","scratch"]:(legacy/d).mkdir(parents=True,exist_ok=True)
(legacy/"scratch/clang18").symlink_to(p/"scratch/sdk/root",target_is_directory=True)
for name in ["independent_probes.py","preservation_and_probe.py"]:shutil.copyfile(s/"R557-5/scripts"/name,legacy/"scripts"/name)
pristine=w/"pristine";pristine.mkdir(exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(["git","archive","HEAD"],cwd=root))) as t:t.extractall(pristine,filter="data")
adapter=w/"adapter";adapter.mkdir(exist_ok=True)
head=subprocess.check_output(["git","rev-parse","HEAD"],cwd=root,text=True).strip()
git=adapter/"git";git.write_text("#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\nif a==[\"checkout\",\"-q\",\"--detach\",\"60c911b92825a720044e78bed540752c7dd0368e\"]: a[-1]="+repr(head)+"\nos.execv(\"/usr/bin/git\",[\"git\",*a])\n");git.chmod(0o755)
# A shared compilation cap applies even to historical scripts with fixed -j16.
locks=w/"compiler-slots";locks.mkdir(exist_ok=True)
wrapper=adapter/"compiler-wrapper"
wrapper.write_text("#!/usr/bin/env python3\nimport fcntl,os,pathlib,subprocess,sys,time\nd=pathlib.Path("+repr(str(locks))+")\nwhile True:\n for i in range(8):\n  f=open(d/str(i),\"w\")\n  try: fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)\n  except BlockingIOError: f.close();continue\n  sys.exit(subprocess.run([\"/usr/bin/\"+pathlib.Path(sys.argv[0]).name,*sys.argv[1:]]).returncode)\n time.sleep(.03)\n")
wrapper.chmod(0o755)
for name in ["gcc","g++","clang","clang++","riscv64-elf-gcc"]:(adapter/name).symlink_to(wrapper)
env["PATH"]=str(adapter)+os.pathsep+env["PATH"]
for sub in ["legacy6","early"]:
 (w/sub/"receipts").mkdir(parents=True,exist_ok=True)
rows=[]
def run(name,args):
 start=time.monotonic()
 with (w/(name+".log")).open("w") as log:rc=subprocess.run(args,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
 (w/(name+".rc")).write_text(str(rc)+"\n");row={"name":name,"rc":rc,"seconds":round(time.monotonic()-start,2)};rows.append(row);print(json.dumps(row),flush=True)
def light():
 commands=[
 ("R556-3-comments",[py,str(s/"R556-3/scripts/comment_probes.py"),str(root)]),
 ("R556-3-needles",[py,str(s/"R556-3/scripts/needle_probes.py"),str(root)]),
 ("R556-4-comments",[py,str(s/"R556-4/scripts/comment_bypass_probe.py"),str(pristine),str(w/"r5564")]),
 ("R556-4-fragments",[py,str(s/"R556-4/scripts/needle_default_fragments.py"),str(root)]),
 ("R556-4-specificity",[py,str(s/"R556-4/scripts/needle_specificity.py"),str(root),str(p/"scratch/local/mutations")]),
 ("R556-5-hidden",[py,str(s/"R556-5/probes/hidden_text_probe.py"),str(root),str(w/"r5565-hidden")]),
 ("R557-4-full",[py,str(s/"R557-4/scripts/full_comment_bypass.py"),"--repo",str(root),"--work",str(w/"r5574-full"),"--output",str(w/"r5574-full.json")]),
 ("R557-4-comments",[py,str(s/"R557-4/scripts/independent_comment_probes.py"),"--repo",str(root),"--work",str(w/"r5574-comments")]),
 ("R557-4-ownership",[py,str(s/"R557-4/scripts/needle_ownership_probes.py"),"--repo",str(root),"--output",str(w/"r5574-ownership.json")]),
 ("R557-5-controls",[py,str(legacy/"scripts/independent_probes.py"),str(root)]),
 ("R557-5-full",[py,str(legacy/"scripts/preservation_and_probe.py"),str(root)]),
 ("R557-6-controls",[py,str(p/"scratch/prior-public/R557-6/scripts/independent_probes.py"),str(root),str(w/"r5576-controls")]),
 ("R557-6-full",[py,str(p/"scratch/prior-public/R557-6/scripts/full_assertion_probe.py"),str(root),str(w/"legacy6")]),
 ("early-comments",[py,str(s/"early/r557_probe_comments.py"),str(root),str(w/"early")])]
 for name,args in commands:run(name,args)
def heavy():
 run("R556-6-contract",[py,str(p/"scratch/prior-public/R556-6/scripts/r556_6_probes.py"),str(root),str(w/"r5566")])
 run("R556-5-tree",["sh",str(s/"R556-5/probes/plant_tree_probe.sh"),str(root),str(w/"r5565-tree")])
 run("early-gates",["bash",str(s/"early/gate_probes.sh"),str(root),head,str(w/"early-gates")])
 run("early-driver",["bash",str(s/"early/driver_probes.sh"),str(root),head,str(w/"early-driver")])
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 futures=[pool.submit(light),pool.submit(heavy)]
 for f in futures:f.result()
(w/"results.json").write_text(json.dumps({"head":head,"results":rows,"adaptation":"Published scripts unchanged. Historical fixed checkout redirected to exact head. Legacy relative dependency location supplied by a scratch symlink. Compiler processes limited to eight."},indent=2)+"\n")
