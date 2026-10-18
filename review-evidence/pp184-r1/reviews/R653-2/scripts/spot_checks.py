#!/usr/bin/env python3
"""Run concurrent, joined checks in disposable trees. No background shell jobs."""
import concurrent.futures,hashlib,os,pathlib,subprocess,sys
OUT=pathlib.Path(__file__).resolve().parents[1]
SRC=pathlib.Path(sys.argv[1]).resolve()
WORK=OUT/"scratch/spot-checks";WORK.mkdir(parents=True,exist_ok=True)
PUB=OUT/"receipts/public/author-r2/r2-receipts/probe"
VL=pathlib.Path(os.environ.get("REVIEW_VERILATOR","$VALIDATION_TOOLS/pinned-verilator-5.050/verilator"))
env=os.environ.copy();env["TMPDIR"]=str(WORK);env["PYTHONDONTWRITEBYTECODE"]="1"
def run(cmd,cwd,log):
 log.write("COMMAND "+" ".join(map(str,cmd))+"\n");log.flush()
 return subprocess.run(list(map(str,cmd)),cwd=cwd,stdout=log,stderr=subprocess.STDOUT,env=env).returncode
def probe(label):
 work=WORK/label;work.mkdir(exist_ok=True)
 rtl=work/"hdl/srp/KL_srp_domain.sv";rtl.parent.mkdir(parents=True,exist_ok=True)
 rtl.write_bytes((SRC/"hdl/srp/KL_srp_domain.sv").read_bytes())
 cpp=work/"probe.cpp";cpp.write_bytes((PUB/"probe.cpp").read_bytes())
 path=OUT/f"receipts/local-{label}.log"
 with path.open("w") as log:
  log.write("HEAD 88cb206135c23eb86488ad110fe19cfca5f341cf\n")
  if label!="golden":
   assert run(["git","apply",PUB/f"mut-{label}.patch"],work,log)==0
  log.write("SOURCE SHA256 "+hashlib.sha256(rtl.read_bytes()).hexdigest()+"\n")
  cmd=[VL,"--cc","--exe","--build","-j","1","-Wno-fatal","--top-module","KL_srp_domain","-Mdir",work/"obj",rtl,cpp]
  assert run(cmd,work,log)==0
  rc=run([work/"obj/VKL_srp_domain"],work,log)
 (OUT/f"receipts/local-{label}.rc").write_text(str(rc)+"\n")
 s=path.read_text()
 expected={"refresh-while-waiting":"FAIL: B1b", "enqueue-next-state":"FAIL: B3b", "pop-without-ready":"FAIL: B1b"}
 assert rc==(0 if label=="golden" else 1)
 if label=="golden": assert "probe: 12 PASS, 0 FAIL" in s
 else: assert expected[label] in s
 return label+": verified expected rc "+str(rc)
def docs():
 work=WORK/"docs-clone"
 path=OUT/"receipts/local-docs.log"
 with path.open("w") as log:
  if not work.exists(): assert run(["git","clone","--shared","--no-checkout",SRC,work],WORK,log)==0
  assert run(["git","checkout","--detach","88cb206135c23eb86488ad110fe19cfca5f341cf"],work,log)==0
  rc=run(["make","-j16","check"],work,log)
 (OUT/"receipts/local-docs.rc").write_text(str(rc)+"\n")
 assert rc==0
 return "docs: rc 0"
with (OUT/"receipts/local-identity.log").open("w") as log:
 assert run([VL,"--version"],SRC,log)==0
 log.write("SHA256 "+hashlib.sha256(VL.read_bytes()).hexdigest()+"\n")
# Four single-job tiny builds plus <=11 documentation targets: <=15 active jobs.
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 tasks=[pool.submit(probe,l) for l in ["golden","refresh-while-waiting","enqueue-next-state","pop-without-ready"]]+[pool.submit(docs)]
 for f in tasks: print(f.result(),flush=True)
