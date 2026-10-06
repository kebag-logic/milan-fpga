#!/usr/bin/env python3
"""Check merge preservation and elaborated counter-stamp sizes without source edits."""
import hashlib, json, pathlib, re, subprocess, sys, types
src=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(sys.argv[2]).resolve()
sim=sys.argv[3] if len(sys.argv)>3 else "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator"
receipts=out/"receipts";scratch=out/"scratch"/"delta";scratch.mkdir(parents=True,exist_ok=True)
head="669ded57b1fabc2bbf274b8ad05493c7593e0a0a";old="75c4eee4589e9317aca3d07b91f94a38b4cc86af";main="2ad2f845dd583f8310075fa2380cb60a04fd091a"
def git(*a):return subprocess.check_output(["git","-C",str(src),*a])
def blob(ref,path):return git("show",ref+":"+path)
def campaign(ref,name):
 m=types.ModuleType(name);m.__file__=str(src/"tb/pp_top/notify_mutants.py");sys.modules[name]=m
 exec(compile(blob(ref,"tb/pp_top/notify_mutants.py"),m.__file__,"exec"),m.__dict__)
 return m
now=campaign(head,"current_campaign");prior=campaign(old,"prior_campaign");parent=campaign(main,"main_campaign")
def records(ms):return {x.name:x._asdict() for x in ms}
n=records(now.MUTANTS);o=records(prior.MUTANTS);d=records(parent.DOMAIN_NOTIFY)
assert len(n)==86 and len(o)==77 and len(d)==9
assert set(n)==set(o)|set(d)
assert all(n[k]==v for k,v in (o|d).items())
unchanged=["hdl","tb/aecp_notify","tb/adp_engine","tb/pp_top/interface_phases.hpp","tb/pp_top/if_guards.py","tb/pp_top/Makefile","tb/pp_top/pp_top_wrap.sv"]
for path in unchanged:assert git("diff","--name-only",old,head,"--",path)==b"",path
assert blob(head,"tb/pp_top/notify_phases.hpp")==blob(main,"tb/pp_top/notify_phases.hpp")
readme=blob(head,"tb/pp_top/README.md").decode()
for name in n:assert "`"+name+"`" in readme,name
main_readme=blob(main,"tb/pp_top/README.md").decode();old_readme=blob(old,"tb/pp_top/README.md").decode()
def section(text,start,end=None):
 begin=text.index(start);return text[begin:text.index(end,begin) if end else None]
assert section(readme,"### Section DN:","### Mutation record:")==section(main_readme,"### Section DN:","### Mutation record:")
assert section(readme,"## Section IF:")==section(old_readme,"## Section IF:")
(receipts/"readme-merge.json").write_text(json.dumps({"DN_README_bytes_equal_main":True,"IF_README_bytes_equal_round2":True},indent=2)+"\n")
assert git("rev-list","--parents","-n","1","600ef13").decode().split()[1:]==[old,main]
assert git("diff","--name-only","df40cec3",head).decode().splitlines()==["docs/architecture/06_aecp_engine.md"]
doc=blob(head,"docs/architecture/06_aecp_engine.md").decode()
row=next(line for line in doc.splitlines() if "| GET_COUNTERS stamps `ctr_last_r`" in line)
assert "(streams in + out + 1 + P-N-AVB-INTERFACES) × 32 bits" in row
main_text=blob(head,"tb/pp_top/sim_main.cpp").decode()
main_lines=len(main_text[main_text.index("int main("):].splitlines())
assert main_lines==100
sizes=[]
for streams in (1,8):
 for interfaces in (1,2):
  xml=scratch/f"shape-{streams}-{interfaces}.json"
  args=[sim,"--json-only","--json-only-output",str(xml),"--Mdir",str(scratch/f"obj-{streams}-{interfaces}"),"--top-module","KL_aecp_notify","-Wno-fatal",f"-GN_STREAM_IN_P={streams}",f"-GN_STREAM_OUT_P={streams}",f"-GN_IF_P={interfaces}","hdl/common/pp_pkg.sv","hdl/aecp/KL_aecp_notify.sv"]
  log=receipts/f"counter-shape-{streams}-{interfaces}.log"
  with log.open("w") as f:rc=subprocess.run(args,cwd=src,stdout=f,stderr=subprocess.STDOUT).returncode
  assert rc==0,(streams,interfaces,rc)
  root=json.loads(xml.read_text())
  def walk(value):
   if isinstance(value,dict):
    yield value
    for v in value.values():yield from walk(v)
   elif isinstance(value,list):
    for v in value:yield from walk(v)
  objects=list(walk(root))
  v=next(x for x in objects if x.get("name")=="N_CTR_DESC_C")
  count=int(v["valuep"][0]["name"].split("h")[1],16)
  assert count==2*streams+1+interfaces
  stamp=next(x for x in objects if x.get("name")=="ctr_last_r")
  dtype=next(x for x in objects if x.get("addr")==stamp["dtypep"])
  assert dtype["declRange"]==f"[0:{count-1}]"
  elem=next(x for x in objects if x.get("addr")==dtype["refDTypep"])
  width=32
  assert elem.get("range") == "31:0",elem
  sizes.append({"streams_in":streams,"streams_out":streams,"interfaces":interfaces,"N_CTR_DESC_C":count,"stamp_bits":count*width})
record={"head":head,"old":old,"main":main,"main_physical_lines":main_lines,"campaign_count":len(n),"prior_controls_unchanged":len(o),"DN_controls_unchanged":len(d),"all_readme_rows_present":True,"round2_paths_byte_identical":unchanged,"DN_file_byte_identical_to_main":True,"merge_parents_verified":True,"final_commit_docs_only":True,"storage_row":row,"elaborated_shapes":sizes}
(receipts/"delta-check.json").write_text(json.dumps(record,indent=2)+"\n");print(json.dumps(record,indent=2))
