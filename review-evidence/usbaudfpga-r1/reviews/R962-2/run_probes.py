#!/usr/bin/env python3
"""Focused review checks; all child work is joined before this foreground driver returns."""
import concurrent.futures,json,os,pathlib,subprocess,sys
import yaml
OUT=pathlib.Path(__file__).resolve().parent
ROOT=pathlib.Path.cwd()
ENGINE=sys.argv[1] if len(sys.argv)>1 else "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator"
SCRATCH=OUT/"scratch/probes";SCRATCH.mkdir(parents=True,exist_ok=True)
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE="1",TMPDIR=str(SCRATCH))
def run(name,cmd):
 with (OUT/(name+".log")).open("w") as log:
  r=subprocess.run(cmd,cwd=ROOT,env=ENV,stdout=log,stderr=subprocess.STDOUT)
 (OUT/(name+".rc")).write_text(str(r.returncode)+"\n")
 print(name,r.returncode,flush=True)
 return {"name":name,"command":cmd,"exit":r.returncode}
def campaign(name,plants):
 cmd=[sys.executable,"-B","tb/verilator/usbaudio/transport_mutations.py","--engine",ENGINE,"--out",str(SCRATCH/name),"--jobs","8","--cleanup-ledger",str(SCRATCH/"cleanup.txt"),"--temporary-suffix",".tmp"]
 for p in plants:cmd += ["--only",p]
 result=run(name,cmd)
 for f in (SCRATCH/name).glob("*/run.log"):
  dest=OUT/"probe-runtime"/name/f.parent.name;dest.mkdir(parents=True,exist_ok=True)
  (dest/"run.log").write_bytes(f.read_bytes())
 results=SCRATCH/name/"results.json"
 if results.exists():(OUT/(name+"-results.json")).write_bytes(results.read_bytes())
 return result
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 fs=[pool.submit(campaign,"epoch-controls",["bridge_applied_epoch","bridge_capture_abort","bridge_packet_fence","bridge_status_epoch","bridge_published_epoch"]),pool.submit(campaign,"grid-controls",["media_grid_transition","media_walk_transition"])]
 results.extend(f.result() for f in fs)
workflow=yaml.safe_load((ROOT/".github/workflows/docs.yml").read_text())
for gate in ("gate_11","gate_32","gate_35"):
 step=next(s for s in workflow["jobs"]["docs-gates-0"]["steps"] if s.get("id")==gate)
 results.append(run(gate,["bash","--noprofile","--norc","-e","-o","pipefail","-c",step["run"]]))
(OUT/"probe-results.json").write_text(json.dumps(results,indent=2)+"\n")
raise SystemExit(int(any(r["exit"] for r in results)))
