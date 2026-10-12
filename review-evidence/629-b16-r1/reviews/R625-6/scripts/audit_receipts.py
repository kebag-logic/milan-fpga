#!/usr/bin/env python3
"""Independent arithmetic and public transcript audit. Usage: audit_receipts.py AUTHOR_PACKET OUTPUT_JSON"""
import collections,csv,hashlib,json,statistics,sys
from pathlib import Path
p=Path(sys.argv[1]);out=Path(sys.argv[2]); result={}
def j(f):return json.loads((p/f).read_text())
def jl(f):return [json.loads(x) for x in (p/f).read_text().splitlines()]
def signed(v,bits=32):return v-(1<<bits) if v&(1<<(bits-1)) else v
raw={x["path"]:x for x in j("RAW-ARTIFACTS.json")["files"]}
result["grades"]={}
for run in ("b0-2","bcrf","baaf"):
 g=j(f"summary/{run}/c-b9-grade.json");blocks=g["blocks"]
 med=[statistics.median(b[f"ch{k}"]["thdn_db"] for b in blocks) for k in (0,1)]
 floor=[b for b in blocks if not b["events"] and all(b[f"ch{k}"]["thdn_db"]<=med[k]+3 for k in (0,1))]
 degraded=[b["block"] for b in blocks if b not in floor]
 assert len(floor)==g["summary"]["blocks_at_floor"]
 assert degraded==g["summary"]["degraded_event_free_blocks"]
 result["grades"][run]=dict(blocks=len(blocks),floor=len(floor),degraded=degraded,all_medians=[round(x,2) for x in med],floor_medians=[round(statistics.median(b[f"ch{k}"]["thdn_db"] for b in floor),2) for k in (0,1)],events=len(g["events"]),phase_frames=g["phase_net_frames"],alignments={})
 for pt in ("a","b"):
  a=j(f"summary/{run}/align-{pt}-c.json");assert a["frames_differing"]==0 and not a["slips"]
  result["grades"][run]["alignments"][pt]=dict(equal=a["compared_equal"],seconds=a["compared_equal"]/48000)
 if run=="b0-2":
  end=min(j(f"summary/{run}/align-{pt}-c.json")["covered_recording_frames"][1] for pt in ("a","b"))//48000
  inside=[x for x in degraded if x<end]
  assert len(inside)==23 and len(degraded)-len(inside)==108
  result["b0_overlap"]=dict(whole_blocks=end,inside=inside,beyond=len(degraded)-len(inside))
result["positive_controls"]={}
for run in ("pts2","b0-2","bcrf","baaf"):
 d=j(f"summary/{run}/d-extcap-pair.json");tones=[d["rows"][k][f"tone_{f}"]["per_block"] for k,f in ((0,997),(1,9973))]
 decode=j(f"summary/{run}/d-loop-decode.json")
 full=[i for i in range(len(tones[0])) if i*48000>=decode["first_decoded_frame"] and (i+1)*48000-1<=decode["last_decoded_frame"]]
 floor=[i for i in full if all(t[i]["thdn_db"] < -140 for t in tones)]
 silent=[i for i in range(len(tones[0])) if all(t[i]["level_dbfs"] < -400 for t in tones)]
 assert silent==[0,1]
 assert len(full)==(13 if run=="pts2" else 303)
 assert len(floor)==(11 if run=="pts2" else 303)
 result["positive_controls"][run]=dict(whole_playback=len(full),at_floor=len(floor),silent=silent,off_floor_inside=[i for i in full if i not in floor],decode=j(f"summary/{run}/d-loop-decode.json"))
result["polls"]={}; states={0:"IDLE",1:"VERIFY",2:"REPAIR",3:"ACQUIRE",4:"LOCKED",5:"HOLDOVER",6:"FAULT"}
for run in ("bcrf","baaf"):
 receipt=j(f"r2/{run}-poll-receipt.json")
 assert receipt["raw"]["sha256"]==raw[f"{run}/poll-run.jsonl"]["sha256"]
 assert receipt["events"]["sha256"]==hashlib.sha256((p/f"runs/{run}/events.jsonl").read_bytes()).hexdigest()
 trace=list(csv.DictReader((p/f"r2/{run}-poll-trace.tsv").read_text().splitlines(),delimiter="\t"))
 for x in trace:
  for k in list(x):x[k]=int(x[k],16) if k.startswith("0x") else float(x[k])
 mark=receipt["marks_after_set_s"]
 win=[x for x in trace if mark["window-start"]<=x["start_after_set_s"] and x["start_after_set_s"]+x["length_ms"]/1000<=mark["window-end"]]
 assert len(win)==596 and all(x["0x8f8"]&7==4 for x in win)
 got=dict(count=len(win),states=dict(collections.Counter(states[x["0x8f8"]&7] for x in win)),trim_ppm=[min(signed(x["0x8f8"]>>16,16)/16 for x in win),max(signed(x["0x8f8"]>>16,16)/16 for x in win)],crf_rate_ppm=[min(signed(x["0x748"])/512 for x in win),max(signed(x["0x748"])/512 for x in win)],aaf_rate_ppm=[min(signed(x["0x8e4"])/512 for x in win),max(signed(x["0x8e4"])/512 for x in win)],servo_low16=dict(collections.Counter("{:04x}".format(x["0x8f8"]&65535) for x in win)),aaf_status=sorted({"{:08x}".format(x["0x8e0"]) for x in win}),slip_tdm=sorted({x["0x8d8"] for x in win}))
 expected=receipt["spans"]["window-start..window-end"]
 for k in ("trim_ppm","crf_rate_ppm"):assert got[k]==expected[k]
 assert got["servo_low16"]==expected["mcsrv_stat_lo16"]
 first=next(i for i,x in enumerate(trace) if x["0x8f8"]&7==4)
 got["lock_bracket_s"]=[trace[first-1]["start_after_set_s"],round(trace[first]["start_after_set_s"]+trace[first]["length_ms"]/1000,3)]
 steps=[]
 for a,b in zip(trace,trace[1:]):
  if a["0x8d4"]!=b["0x8d4"]:
   steps.append(dict(polls=[int(a["n"]),int(b["n"])],counts=[a["0x8d4"],b["0x8d4"]],states=[states[a["0x8f8"]&7],states[b["0x8f8"]&7]],bracket_s=[a["start_after_set_s"],round(b["start_after_set_s"]+b["length_ms"]/1000,3)]))
 assert len(steps)==(6 if run=="bcrf" else 7)
 for x,y in zip(steps,receipt["slip_lb_steps"]):
  assert x["polls"]==y["polls"] and x["states"]==y["servo"] and x["counts"]==y["dups"]
 got["slip_steps"]=steps;result["polls"][run]=got
result["clock_sets"]={}
for run in ("bcrf","baaf"):
 ctl=[x.get("line",x) for x in jl(f"runs/{run}/ctl.jsonl")];pairs=[]
 for i,x in enumerate(ctl):
  if x.get("cmd")!="SET_CLOCK_SOURCE":continue
  y=next(t for t in ctl[i+1:] if t.get("cmd")=="GET_CLOCK_SOURCE" and t["role"]==x["role"])
  a=int(x["payload"][8:12],16);b=int(y["payload"][8:12],16)
  assert x["status"]==y["status"]=="SUCCESS" and a==b
  pairs.append(dict(role=x["role"],set=a,readback=b))
 assert pairs==[dict(role="peer",set=0,readback=0),dict(role="dut",set=1 if run=="bcrf" else 2,readback=1 if run=="bcrf" else 2),dict(role="dut",set=0,readback=0),dict(role="peer",set=1,readback=1)]
 result["clock_sets"][run]=pairs
result["censuses"]={}
def census(f):
 return [{k:v for k,v in x.items() if k not in ("t","t_rx","t_tx","rtt_ms","seq")} for x in jl(f) if "what" in x]
for suffix in ("","b","c"):
 a=census(f"restore/census-start{suffix}.jsonl");b=census(f"restore/census-end{suffix}.jsonl")
 differing=[x["what"] for x,y in zip(a,b) if x!=y]
 assert len(a)==len(b)==45 and differing==["avb"]
 result["censuses"]["B16"+suffix]=dict(reads=len(a),equal=len(a)-len(differing),differing=differing)
result["source_reads"]={}
src=j("r2/source-receipt.json")
for name,r in src["reads"].items():assert r["sha256"]==raw[f"source/{name}.json"]["sha256"]
result["source_reads"]=dict(hash_bindings=len(src["reads"]),class_map_sha256=src["class_map_sha256"],comparisons=src["compare"])
a=j("summary/loop2/acmp-peer-tap.json");probes=[x for x in a["acmp"] if x["msg"]=="CONNECT_TX_COMMAND"]
assert len(probes)==2 and not any(x["msg"]=="CONNECT_TX_RESPONSE" for x in a["acmp"])
result["loopback"]=dict(probes=len(probes),separation_ms=round((probes[1]["t"]-probes[0]["t"])*1000,3),probe_responses=0)
for run in ("loop1","loop2"):
 for name in ("a-peer-tap","b-dut-tap"):
  d=j(f"summary/{run}/{name}.json");assert d["frames"]==0
result["status"]="PASS: public receipt arithmetic and transcript assertions"
out.write_text(json.dumps(result,indent=2)+"\n");print(result["status"])
