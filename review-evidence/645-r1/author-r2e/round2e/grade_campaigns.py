import hashlib,json,re
from collections import Counter
from pathlib import Path
w=Path(__file__).resolve().parent
old=w.parent/"round2d/candidate"
rows=[]
margin=re.compile(r"^MARGINS: (.+) empty ([\d.]+) full ([\d.]+) ticks$",re.M)
actions=re.compile(r"settle recentre fired \((\d+) pulse\(s\), render recentre executed (\d+)\); slips before it (\d+), after it (\d+);")
for p in sorted((w/"arrival").glob("*/b8_*.log")):
 assert p.with_suffix(".rc").read_text().strip()=="0",p
 t=p.read_text();m=margin.findall(t);a=actions.findall(t)
 assert len(m)==3 and len(a)==3,p
 assert all(float(empty)>=1 and float(full)>=1 for _,empty,full in m),p
 assert all(int(pulses)==1 and int(render)==1 and int(post)==0 for pulses,render,pre,post in a),p
 twin=old/"campaigns"/p.relative_to(w/"arrival")
 rows.append(dict(case=str(p.relative_to(w/"arrival")),rc=0,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),identical_to_round2d=twin.exists() and twin.read_bytes()==p.read_bytes(),margins=[dict(window=n,empty_ticks=float(e),full_ticks=float(f)) for n,e,f in m]))
assert len(rows)==128,len(rows)
pulls=[]
pullin_classifications=Counter()
for p in sorted((w/"follow-pullin").glob("pullin_*.log")):
 assert p.with_suffix(".rc").read_text().strip()=="0",p
 result=next(l for l in p.read_text().splitlines() if l.startswith("RESULT-647:"))
 pullin_classifications[result.rsplit(": ",1)[-1]]+=1
 counter=re.search(r"recentres (\d+), loopback slips (\d+) before the settle and (\d+) after",result)
 assert counter and counter[1]=="1" and counter[3]=="0",p
 twin=old/"pullin"/p.name
 pulls.append(dict(case=p.name,rc=0,pre_settle_slips=int(counter[2]),post_settle_slips=int(counter[3]),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),identical_to_round2d=twin.exists() and twin.read_bytes()==p.read_bytes()))
assert len(pulls)==32,len(pulls)
quiet=json.loads((w/"quiet.json").read_text())
prior=old/"quiet-distributions.json"
report=dict(head="85db353400c6bf3965d279a9f5b5d47e08a0d1ed",rc=0,arrival_cases=len(rows),arrival_identical_to_round2d=sum(r["identical_to_round2d"] for r in rows),post_settle_windows=3*len(rows),minimum_empty_ticks=min(m["empty_ticks"] for r in rows for m in r["margins"]),minimum_full_ticks=min(m["full_ticks"] for r in rows for m in r["margins"]),pullin_cases=len(pulls),pullin_classifications=dict(pullin_classifications),pullin_pre_settle_slips=sum(r["pre_settle_slips"] for r in pulls),pullin_cases_with_pre_settle_slips=sum(r["pre_settle_slips"]>0 for r in pulls),pullin_post_settle_slips=sum(r["post_settle_slips"] for r in pulls),pullin_identical_to_round2d=sum(r["identical_to_round2d"] for r in pulls),quiet_identical_to_round2d=prior.exists() and json.loads(prior.read_text())==quiet,arrival=rows,pullin=pulls)
(w/"campaign-summary.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps({k:v for k,v in report.items() if k not in ("arrival","pullin")},indent=2))
