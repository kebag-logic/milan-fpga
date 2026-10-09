#!/usr/bin/env python3
import concurrent.futures,json,os,pathlib,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve(); p=pathlib.Path(sys.argv[2]).resolve(); repo=p/"scratch/public-evidence"; rev="fc3d8ef2f113c6ca8bfdfcc6355d6c82d2747856"; w=p/"scratch/early-probes"; w.mkdir(parents=True,exist_ok=True); (w/"legacy/receipts").mkdir(parents=True,exist_ok=True)
commands=[]; rows=json.loads((p/"receipts/prior-provenance.json").read_text())
for name in ("gate_probes.sh","driver_probes.sh","r557_probe_comments.py"):
 source="review-evidence/697-r1/reviews/R556-3/scripts/round2-unchanged/"+name; target=p/"scripts/prior/early"/name; target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(subprocess.check_output(["git","-C",str(repo),"show",rev+":"+source]))
 blob=subprocess.check_output(["git","-C",str(repo),"rev-parse",rev+":"+source],text=True).strip(); rows.append({"file":str(target.relative_to(p)),"source_commit":rev,"source_path":source,"blob":blob,"unchanged":subprocess.check_output(["git","hash-object",str(target)],text=True).strip()==blob})
 commands.append((name,[sys.executable,str(target),str(root),str(w/"legacy")] if name.endswith(".py") else ["bash",str(target),str(root),"6bb706e2c75c7a437d9a0b2e44eb9ebb6d7f54d5",str(w)]))
(p/"receipts/prior-provenance.json").write_text(json.dumps(rows,indent=2)+"\n")
def run(item):
 name,cmd=item
 with (p/"receipts/prior"/(name+".log")).open("w") as log: r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
 (p/"receipts/prior"/(name+".rc")).write_text(str(r.returncode)+"\n"); print(name,r.returncode,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(run,commands))
