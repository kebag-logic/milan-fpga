#!/usr/bin/env python3
import argparse,concurrent.futures,json,os,pathlib,subprocess,time
p=argparse.ArgumentParser();p.add_argument("source",type=pathlib.Path);p.add_argument("packet",type=pathlib.Path);a=p.parse_args();r=a.packet;s=r/"scratch";prior=r/"scripts/prior";results=[]
env={k:v for k,v in os.environ.items() if not k.startswith("GTEST_")};env["TMPDIR"]=str(s/"temp")
def run(n,cmd):
 t=time.monotonic()
 with (r/"receipts"/(n+".log")).open("w") as f: rc=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
 (r/"receipts"/(n+".rc")).write_text(str(rc)+"\n");row={"name":n,"rc":rc,"seconds":round(time.monotonic()-t,2)};results.append(row);print(json.dumps(row),flush=True)
def contract():
 run("contract",["python3",str(prior/"full_suite_probe.py"),"--repo",str(a.source),"--work",str(s/"contract"),"--plants",str(r/"scripts/plants-contract.json"),"--jobs","4","--control","--out",str(r/"receipts/contract-results.json")])
def historical():
 run("escape-probe",["python3",str(prior/"escape_probe.py"),"--tree",str(s/"head-export"),"--work",str(s/"escape"),"--jobs","2"])
 ms=json.loads((a.source/"tests/mutations.json").read_text());names=[m["name"] for m in ms if m["name"].startswith(("dafresh-","g-expiry-","x-zero-")) and m["kills"][0]["test"].startswith("AcmpFresh.")]
 for i in range(0,len(names),2):
  run("physical-"+str(i//2),["python3",str(prior/"physical_removal.py"),"--tree",str(s/"head-export"),"--work",str(s/("physical-"+str(i//2))),"--plants",",".join(names[i:i+2])])
 run("gap-mutants",["python3",str(prior/"gap_mutants.py"),"--tree",str(s/"head-export"),"--work",str(s/"gap-mutants"),"--jobs","2"])
 run("r630-3-full-suite",["python3",str(prior/"full_suite_probe.py"),"--repo",str(a.source),"--work",str(s/"r630-3-full-suite"),"--plants",str(prior/"plants_gap.json"),"--jobs","2","--out",str(r/"receipts/r630-3-full-suite.json")])
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(lambda f:f(),[contract,historical]))
(r/"receipts/probe-runs.json").write_text(json.dumps(results,indent=2)+"\n")
raise SystemExit(any(x["rc"] for x in results))
