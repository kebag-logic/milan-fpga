#!/usr/bin/env python3
"""Replant the five documented arbiter faults in disposable exact-head copies."""
import argparse,concurrent.futures,json,os,pathlib,shutil,subprocess,time
ap=argparse.ArgumentParser(); ap.add_argument("--compiler",required=True); ap.add_argument("--jobs",type=int,default=3); ap.add_argument("--only",nargs="*"); a=ap.parse_args(); assert 1<=a.jobs<=3
p=pathlib.Path(__file__).resolve().parents[1]; root=p/"scratch/head"; rel="hdl/packet_engine/KL_pp_tx_arbiter.sv"
env=os.environ.copy(); env.update(REVIEW_HDL_COMPILER=a.compiler,MAKEFLAGS="-j16")
variants={
"M1": [("{~aged_w[i], PRIO_MAP_P[2*i +: 2]}","{1'b1, PRIO_MAP_P[2*i +: 2]}")],
"M2": [("(pace_nonsol_r && sol_pend_w)","(1'b0)")],
"M3": [("(key_w[j] <= key_w[i])","(key_w[j] >= key_w[i])"),("(key_w[j] < key_w[i])","(key_w[j] > key_w[i])")],
"M4": [("assign eof_w     = consume_w && ser_last_i;","assign eof_w     = consume_w;")],
"M5": [("&& !start_sent_r\n                     && !start_abort_i;","&& !start_sent_r;"),("&& !start_sent_r\n                     && start_abort_i;","&& !start_sent_r\n                     && 1'b0;"),("&& (start_sent_r || !start_abort_i);","&& 1'b1;")]}
def run(item):
 name,edits=item; tree=p/"scratch"/("arb-"+name); tree.mkdir(exist_ok=True)
 for folder in ("hdl","tb/common","tb/tx_arbiter"):
  shutil.copytree(root/folder,tree/folder,ignore=shutil.ignore_patterns("obj*","__pycache__"),dirs_exist_ok=True)
 source=(tree/rel).read_text()
 for old,new in edits:
  assert source.count(old)==1,(name,old,source.count(old));source=source.replace(old,new,1)
 (tree/rel).write_text(source)
 log=p/"receipts"/("arb-"+name+".log")
 with log.open("w") as f: r=subprocess.run(["make","-j16","VERILATOR="+str(p/"scripts/compiler-cap.py")],cwd=tree/"tb/tx_arbiter",env=env,stdout=f,stderr=subprocess.STDOUT)
 text=log.read_text(); fails=[x for x in text.splitlines() if x.startswith("FAIL:")]; tally=[x for x in text.splitlines() if "checks:" in x and " PASS," in x]
 ok=r.returncode!=0 and bool(tally) and bool(fails)
 (p/"receipts"/("arb-"+name+".rc")).write_text(str(r.returncode)+"\n")
 result=dict(name=name,rc=r.returncode,tally=tally,failing_checks=fails,verdict="KILLED" if ok else "UNCONFIRMED");print(json.dumps(result),flush=True);return result
with concurrent.futures.ThreadPoolExecutor(a.jobs) as ex: records=list(ex.map(run,[(n,e) for n,e in variants.items() if not a.only or n in a.only]))
if a.only and (p/"receipts/arbiter-mutants.json").exists():
 records=[x for x in json.loads((p/"receipts/arbiter-mutants.json").read_text()) if x["name"] not in a.only]+records
(p/"receipts/arbiter-mutants.json").write_text(json.dumps(records,indent=2)+"\n")
raise SystemExit(int(any(r["verdict"]!="KILLED" for r in records)))
