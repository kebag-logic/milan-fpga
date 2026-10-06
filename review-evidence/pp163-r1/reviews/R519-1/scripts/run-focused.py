#!/usr/bin/env python3
"""Run independent scoped campaigns concurrently; all subprocesses are joined."""
import argparse,concurrent.futures,hashlib,json,os,pathlib,subprocess,tarfile,time
ap=argparse.ArgumentParser(); ap.add_argument("--repo",type=pathlib.Path,required=True); ap.add_argument("--compiler",required=True); args=ap.parse_args()
p=pathlib.Path(__file__).resolve().parents[1]; scratch=p/"scratch"; scratch.mkdir(exist_ok=True); (scratch/"tmp").mkdir(exist_ok=True)
head=subprocess.check_output(["git","rev-parse","HEAD"],cwd=args.repo,text=True).strip()
assert head=="cd9825c947cf67b735d26cc1c42541ccd9d7f637",head
archive=scratch/"head.tar"
with archive.open("wb") as f: subprocess.run(["git","archive",head],cwd=args.repo,stdout=f,check=True)
tree=scratch/"head"; tree.mkdir(exist_ok=True)
with tarfile.open(archive) as tf: tf.extractall(tree,filter="data")
env=os.environ.copy(); env.update(REVIEW_HDL_COMPILER=str(pathlib.Path(args.compiler).resolve()),TMPDIR=str(scratch/"tmp"),MAKEFLAGS="-j16",VERILATOR_JOBS="2",PYTHONDONTWRITEBYTECODE="1")
compiler=str(p/"scripts/compiler-cap.py")
identity=subprocess.check_output([args.compiler,"--version"],text=True).strip(); assert "5.050" in identity,identity
(p/"receipts/compiler-identity.txt").write_text(identity+"\nlauncher sha256 "+hashlib.sha256(pathlib.Path(args.compiler).read_bytes()).hexdigest()+"\n")
jobs=[("withdraw-campaign",["python3","tb/pp_top/notify_mutants.py","--output",str(p/"receipts/withdraw-campaign"),"--verilator",compiler,"--jobs","2","--only","withdraw_unregistered","withdraw_abort_ignored","cancel_one_clock_late"],tree),
("tx-arbiter",["make","-j16","VERILATOR="+compiler],tree/"tb/tx_arbiter"),
("originator",["make","-j16","VERILATOR="+compiler],tree/"tb/originator")]
def run(job):
 name,cmd,cwd=job; t=time.monotonic(); print("START",name,flush=True)
 with (p/"receipts"/(name+".log")).open("w") as f: r=subprocess.run(cmd,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT)
 (p/"receipts"/(name+".rc")).write_text(str(r.returncode)+"\n")
 rec=dict(name=name,command=cmd,cwd=str(cwd.relative_to(p)),rc=r.returncode,seconds=round(time.monotonic()-t,3)); print(json.dumps(rec),flush=True); return rec
with concurrent.futures.ThreadPoolExecutor(3) as ex: records=list(ex.map(run,jobs))
(p/"receipts/focused-runs.json").write_text(json.dumps(records,indent=2)+"\n")
raise SystemExit(int(any(x["rc"] for x in records)))
