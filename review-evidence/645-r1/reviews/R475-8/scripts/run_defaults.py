#!/usr/bin/env python3
"""Run two isolated cold defaults concurrently; all children are joined."""
import argparse, concurrent.futures, hashlib, io, json, os, pathlib, shutil, subprocess, tarfile, time
p=argparse.ArgumentParser()
p.add_argument("source",type=pathlib.Path);p.add_argument("packet",type=pathlib.Path);p.add_argument("simulator",type=pathlib.Path)
a=p.parse_args();src=a.source.resolve();packet=a.packet.resolve();sim=a.simulator.resolve()
scratch=packet/"scratch"; receipts=packet/"receipts/defaults";receipts.mkdir(parents=True,exist_ok=True)
version=subprocess.check_output([str(sim),"--version"],text=True)
assert "5.050" in version,version
(receipts/"identity.json").write_text(json.dumps({"head":subprocess.check_output(["git","-C",str(src),"rev-parse","HEAD"],text=True).strip(),"simulator_version":version.strip(),"launcher_sha256":hashlib.sha256(sim.read_bytes()).hexdigest(),"compiler_workers_per_build":2,"campaign_jobs":2},indent=2)+"\n")
cpus=sorted(os.sched_getaffinity(0));assert len(cpus)>=8
# Apply a uniform build-worker cap even to the controller driver, whose own
# recipe requests sixteen. No source file or test assertion is changed.
shim=scratch/"bounded-simulator.py"
shim.write_text("#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\nfor i,x in enumerate(a[:-1]):\n if x == '-j': a[i+1]='2'\nos.execv(os.environ['REVIEW_SIM'],[os.environ['REVIEW_SIM'],*a])\n")
shim.chmod(0o755)
archive=subprocess.check_output(["git","-C",str(src),"archive","HEAD","hdl","configs/generated/endstation_ax7101_1x1_tdm8","tb/common","tb/verilator/mmcm_servo/mmcm_model.h","tb/verilator/follow_ring"])
def run(name,parallel,cpu):
 tree=scratch/name;tree.mkdir()
 with tarfile.open(fileobj=io.BytesIO(archive)) as tf:tf.extractall(tree,filter="data")
 env=os.environ.copy();env.pop("MAKEFLAGS",None);env.pop("MFLAGS",None);env["REVIEW_SIM"]=str(sim);env["VERILATOR"]=str(shim);env["VERILATOR_JOBS"]="2";env["SWEEP_JOBS"]="2";env["PYTHONDONTWRITEBYTECODE"]="1"
 argv=["taskset","-c",','.join(map(str,cpu)),"timeout","1800","make"]+(["-j16"] if parallel else [])+["-C",str(tree/"tb/verilator/follow_ring")]
 (receipts/(name+".command.json")).write_text(json.dumps({"argv":argv,"MAKEFLAGS":"unset","VERILATOR_JOBS":2,"SWEEP_JOBS":2,"uniform_compile_cap":2},indent=2)+"\n")
 start=time.monotonic()
 with (receipts/(name+".log")).open("w") as log:r=subprocess.run(argv,env=env,stdout=log,stderr=subprocess.STDOUT)
 elapsed=time.monotonic()-start
 (receipts/(name+".rc")).write_text(str(r.returncode)+"\n")
 (receipts/(name+".time.json")).write_text(json.dumps({"elapsed_s":elapsed})+"\n")
 suite=tree/"tb/verilator/follow_ring"
 for base in [suite/"obj_dir_fine/results",suite/"obj_dir_control"]:
  for f in base.rglob("*"):
   if f.is_file() and f.suffix in (".log",".rc",".json") and "obj_dir" not in f.relative_to(base).parts:
    dest=receipts/name/base.name/f.relative_to(base);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,dest)
 print(name,"rc",r.returncode,"elapsed_s",round(elapsed,3),flush=True)
 return r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 fs=[pool.submit(run,"serial",False,cpus[:4]),pool.submit(run,"outer-j16",True,cpus[4:8])]
 results=[f.result() for f in fs]
raise SystemExit(int(any(results)))
