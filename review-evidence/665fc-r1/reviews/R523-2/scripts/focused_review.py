#!/usr/bin/env python3
"""Portable focused review. Run from the exact source checkout; all builds stay in packet/scratch."""
import argparse, concurrent.futures, importlib.util, json, os, pathlib, subprocess, sys, time
ap=argparse.ArgumentParser();ap.add_argument("--source",type=pathlib.Path,default=pathlib.Path.cwd());ap.add_argument("--packet",type=pathlib.Path,required=True);ap.add_argument("--verilator",required=True);ap.add_argument("--jobs",type=int,default=3);a=ap.parse_args()
src=a.source.resolve(); packet=a.packet.resolve(); scratch=packet/"scratch"; receipts=packet/"receipts"
os.environ["TMPDIR"]=str(scratch);os.environ["PYTHONDONTWRITEBYTECODE"]="1";os.environ["VERILATOR"]=a.verilator
sys.dont_write_bytecode=True
sys.path.insert(0,str(src/"tb/verilator/mbx"));import mutants as rtl
sys.path.insert(0,str(src/"sw/firmware/ctrl/test"));import ctrl_mutants as model, ctrl_arms, ctrl_build
sys.path.insert(0,str(src/"sw/mailbox"));import gen_mailbox as gen

def save(name,log,rc):
 (receipts/(name+".log")).write_text(log);(receipts/(name+".rc")).write_text(str(rc)+"\n")
 print(name,"rc",rc,flush=True)

def run(name,argv,cwd=src):
 p=subprocess.run([str(x) for x in argv],cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=590)
 save(name,p.stdout,p.returncode);return p.returncode

def build_rtl(name,host,arm=None,variant=False):
 root=scratch/"rtl-probes";root.mkdir(exist_ok=True)
 d=rtl.plant(arm,root) if arm else src/"hdl/milan/mailbox"
 work=root/name;work.mkdir(parents=True,exist_ok=True)
 files=[d/f for f in rtl.RTL_FILES]
 recipe=rtl.recipe(); recipe[recipe.index("-j")+1]="4"
 if variant:
  files=[scratch/"if2-gen"/f.name if f.name in ("KL_mbx.sv","KL_mbx_pkg.sv") else f for f in files]
  recipe=[x.replace(str(src/"sw/firmware/ctrl/mbx"),str(scratch/"if2-gen")) for x in recipe]
 argv=recipe+[f"-GHOST_P={host}","--Mdir",str(work/"obj"),*[str(f) for f in files],"tb_mbx_top.sv","sim_main.cpp","-o","Vmbx"]
 p=subprocess.run(argv,cwd=rtl.HERE,capture_output=True,text=True,timeout=590)
 save(name+"-build",p.stdout+p.stderr,p.returncode)
 if p.returncode:return (name,False,"build failure")
 p=subprocess.run([str(work/"obj/Vmbx"),str(host)],capture_output=True,text=True,timeout=590)
 log=p.stdout+p.stderr;save(name,log,p.returncode)
 matched=[x for x in log.splitlines() if "[FAIL]" in x and arm and arm.needle in x]
 ok=(p.returncode==1 and bool(matched)) if arm else p.returncode==0
 return (name,ok,matched if arm else [x for x in log.splitlines() if "checks:" in x])

def model_campaign():
 build=ctrl_build.fw_gtest.Build(jobs=4);root=scratch/"model-probes";root.mkdir(exist_ok=True)
 out=ctrl_arms.arm_model(ctrl_build.Tree(ctrl_build.CTRL,root/"control",root/"reuse",build))
 save("model-control",out.log,out.rc); results=[("model-control",out.rc==0,"")]
 selected={"model-msg-type-off-by-one","model-tuple-msg-type-ignored","model-msg-type-refusal-uncounted","model-defend-any-unicast"}
 for m in model.MUTANTS:
  if m.name not in selected:continue
  copy=model.plant(m,root);out=ctrl_arms.arm_model(ctrl_build.Tree(copy,root/m.name/"out",root/"reuse",build))
  save(m.name,out.log,out.rc);results.append((m.name,model.caught(m.test,m.needle,out),[x for x in out.log.splitlines() if model.names(x,m.test,m.needle)]))
 # Recheck the unchanged production API additions from the full PR.
 for name,fn in (("port-control",ctrl_arms.arm_port),("unit-control",ctrl_arms.arm_unit)):
  out=fn(ctrl_build.Tree(ctrl_build.CTRL,root/name,root/"reuse",build));save(name,out.log,out.rc);results.append((name,out.rc==0,""))
 return results

assert subprocess.check_output(["git","rev-parse","HEAD"],cwd=src,text=True).strip()=="db9aa8c9b135b34ff3d070a979dee70440b37cc6"
run("compiler-identity",[a.verilator,"--version"])
run("generator-check",[sys.executable,"-B","sw/mailbox/gen_mailbox.py","--check","--crosscheck"])
run("generator-selftest",[sys.executable,"-B","sw/mailbox/gen_mailbox.py","--selftest"])
run("generator-if2",[sys.executable,"-B","sw/mailbox/gen_mailbox.py","--variant-interfaces","2","--out",scratch/"if2-gen"])
regenerated=scratch/"regenerated";gen.write_all(gen.load(),regenerated)
for f in gen.generate(gen.load()):assert (src/f).read_bytes()==(regenerated/f).read_bytes(),f
save("regeneration", "All four --write outputs reproduce exact tracked bytes.\n",0)
# Every table arm must plant, including the pre-existing exact-text arms.
for m in rtl.ARMS:assert (rtl.RTL/m.path).read_text().count(m.old)==1,m.name
for m in model.MUTANTS:assert (model.CTRL/m.path).read_text().count(m.old)==1,m.name
save("plant-audit",f"Unique anchors: {len(rtl.ARMS)} RTL arms; {len(model.MUTANTS)} firmware arms.\n",0)
newnames={"pkg-maap-defend-tuple-dropped","rx-msg-type-off-by-one","rx-classified-before-msg-type","rx-tuple-msg-type-ignored","rx-own-unicast-never-counted","rx-defend-any-unicast","rx-short-frame-never-classified"}
arms=[m for m in rtl.ARMS if m.name.removesuffix("-axil") in newnames or m.name=="rx-subtype-ignored"]
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=min(a.jobs,3)) as pool:
 futs=[pool.submit(build_rtl,f"control-{h}",h) for h in (0,1)]
 futs.append(pool.submit(model_campaign))
 for h in (0,1):futs.append(pool.submit(build_rtl,f"if2-control-{h}",h,variant=True))
 for m in arms:futs.append(pool.submit(build_rtl,m.name,m.host,m))
 for f in concurrent.futures.as_completed(futs):
  r=f.result();results.extend(r if isinstance(r,list) else [r])
(packet/"receipts/focused-results.json").write_text(json.dumps(results,indent=2)+"\n")
bad=[r for r in results if not r[1]]
print("FOCUSED COMPLETE",len(results),"results; failures",len(bad),flush=True)
sys.exit(bool(bad))
