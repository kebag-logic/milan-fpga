#!/usr/bin/env python3
"""Foreground focused review campaigns; isolated exports, bounded concurrent builds."""
import concurrent.futures,hashlib,json,os,pathlib,subprocess,sys,tarfile,time
root=pathlib.Path(sys.argv[1]).resolve(); packet=pathlib.Path(__file__).resolve().parents[1]
scratch=packet/"scratch"; receipt=packet/"receipts"; scratch.mkdir(exist_ok=True); receipt.mkdir(exist_ok=True)
env=os.environ.copy();env.update(TMPDIR=str(scratch),PYTHONDONTWRITEBYTECODE="1",REVIEW_LOCKDIR=str(scratch/"build-locks"),MAKEFLAGS="-j16")
wrapper=packet/"scripts/bounded-verilator.py"
assert subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip()=="ad670a71b4d2f38f59672d51d8309d59ffed0808"
assert "Verilator 5.050" in subprocess.check_output([env.get("REVIEW_VERILATOR","$VALIDATION_TOOLS/pinned-verilator-5.050/verilator"),"--version"],text=True)
source=scratch/"source"
if not source.exists():
 source.mkdir(); archive=scratch/"source.tar"
 with archive.open("wb") as f: subprocess.run(["git","-C",str(root),"archive","HEAD"],stdout=f,check=True)
 with tarfile.open(archive) as f: f.extractall(source,filter="data")
def run(name,command,cwd):
 start=time.time();print("START",name,flush=True)
 with (receipt/(name+".log")).open("w") as f:
  f.write("COMMAND "+json.dumps(command)+"\n");f.flush()
  r=subprocess.run(command,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT)
 (receipt/(name+".rc")).write_text(str(r.returncode)+"\n")
 out={"name":name,"rc":r.returncode,"seconds":round(time.time()-start,2)}
 print(json.dumps(out),flush=True);return out
def suite(name):return run(name,["make","-j16","VERILATOR="+str(wrapper)],source/"tb"/name)
def pp():
 out=[run("pp-build",["make","-j16","gsi-build","VERILATOR="+str(wrapper)],source/"tb/pp_top")]
 if out[0]["rc"]:return out
 for tag,arg in [("domain-notify","--domain-notify-only"),("notify","--notify-only"),("spacing","--spacing-only")]:
  out.append(run(tag,["./obj_dir/Vpp_top_sim",arg],source/"tb/pp_top"))
 return out
def mutants():
 names=["avb_domain_term_dropped","avb_link_term_dropped","asp_takes_domain","avb_notify_not_interface","domain_same_readopted","adoption_no_strobe","revert_strobes_at_defaults","registry_never_claims","restore_never_done"]
 return run("domain-mutants",[sys.executable,"tb/pp_top/notify_mutants.py","--output",str(receipt/"domain-mutants"),"--verilator",str(wrapper),"--jobs","2","--only",*names],source)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
 futures=[pool.submit(pp),pool.submit(mutants),*[pool.submit(suite,n) for n in ("srp_stream_fsms","srp_top","originator","rx_validator")]]
 records=[f.result() for f in futures]
(receipt/"focused-summary.json").write_text(json.dumps(records,indent=2)+"\n")
def good(x):return all(good(y) for y in x) if isinstance(x,list) else x["rc"]==0
sys.exit(0 if good(records) else 1)
