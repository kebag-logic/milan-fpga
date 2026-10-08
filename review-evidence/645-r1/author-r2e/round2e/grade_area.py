import hashlib,json,re,sys
from pathlib import Path
w=Path(__file__).resolve().parent
area=w/"area-ooc"
rows={}
for name in ("settle_base","settle_head","cmc_base","cmc_head"):
 assert (w/"logs"/("own-"+name+".rc")).read_text().strip()=="0",name
 t=(area/("util_"+name+".rpt")).read_text();values={}
 for label in ("Slice LUTs","Slice Registers"):
  matches=re.findall(r"^\| "+re.escape(label)+r"\*?\s*\|\s*(\d+)\s*\|",t,re.M);assert len(matches)==1,(name,label,matches)
  values[label]=int(matches[0])
 rows[name]=values
delta={k:rows["settle_head"][k]-rows["settle_base"][k]+rows["cmc_head"][k]-rows["cmc_base"][k] for k in rows["settle_base"]}
inputs={p.name:dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(area.iterdir()) if p.suffix in (".sv",".svh",".tcl")}
rc=int(any(x>120 for x in delta.values()))
report=dict(head="85db353400c6bf3965d279a9f5b5d47e08a0d1ed",base="99e4eb6c14462aafa84bb1ac597fd241abc1a240",rows=rows,combined_delta=delta,limit=120,rc=rc,inputs=inputs)
(area/"comparison.json").write_text(json.dumps(report,indent=2)+"\n")
(area/"comparison.rc").write_text(str(rc)+"\n")
print(json.dumps(report,indent=2));raise SystemExit(rc)
