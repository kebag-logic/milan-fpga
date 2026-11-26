#!/usr/bin/env python3
"""Only the four LED cases and eight LED plants, in isolated copies."""
import argparse, concurrent.futures, json, pathlib, shutil, sys
sys.dont_write_bytecode=True
ap=argparse.ArgumentParser(); ap.add_argument("repo",type=pathlib.Path); ap.add_argument("--jobs",type=int,default=2); ap.add_argument("--only-arty",action="store_true"); a=ap.parse_args()
r=a.repo.resolve(); p=pathlib.Path(__file__).resolve().parent; sys.path.insert(0,str(r/"sw/firmware/ctrl/test"))
import aecp_arms, aecp_mutants, aecp_leds_mutants
from ctrl_build import Tree, CTRL, STACK, fw_gtest, Refusal
out=p/"firmware"; out.mkdir(exist_ok=True)
aecp_mutants.controls()
rows=[("baseline-shipping",None,"endstation_ax7101_1x1_tdm8.yaml"),("baseline-arty",None,"endstation_arty_1x1.yaml")]
rows=[("baseline-shipping",None,"endstation_ax7101_1x1_tdm8.yaml")]+[("baseline-"+c.stem,None,c.name) for c in sorted((r/"configs").glob("endstation_arty_*.yaml"))]
rows += [(d.name,d,"endstation_ax7101_1x1_tdm8.yaml") for d in aecp_mutants.DEFECTS if d.name.startswith("leds-")]
if a.only_arty: rows=[row for row in rows if row[0].startswith("baseline-endstation_arty")]
def run(row):
 name,d,config=row; work=p/"scratch/fw"/name; src=work/"ctrl"; shutil.copytree(CTRL,src,dirs_exist_ok=True,ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
 if d:
  f=src/d.path; s=f.read_text(); assert s.count(d.old)==1; f.write_text(s.replace(d.old,d.new))
 tree=Tree(src,work/"build",work/"reuse",fw_gtest.Build(jobs=2),STACK)
 try:
  result=aecp_arms.core_arm(tree,r/"configs"/config,1,"core","Leds.*")
  good=result.rc==0 if not d else all(aecp_mutants.caught(t,w,result) for t,w in d.checks)
  log=result.log; rc=result.rc
 except Exception as e: good=False; log=str(e); rc=2
 (out/(name+".log")).write_text(log.replace(str(r),"$REPO").replace(str(p),"$PACKET")); (out/(name+".rc")).write_text(str(rc)+"\n")
 print(name,"PASS" if good else "FAIL",flush=True); return {"name":name,"rc":rc,"pass":good,"config":config}
with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as pool: results=list(pool.map(run,rows))
(out/("arty-summary.json" if a.only_arty else "summary.json")).write_text(json.dumps(results,indent=2)+"\n")
raise SystemExit(not all(x["pass"] for x in results))
