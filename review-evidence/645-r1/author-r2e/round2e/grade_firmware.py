import hashlib,json,re,sys
from pathlib import Path
w=Path(__file__).resolve().parent
sys.path.insert(0,str(w/"functional/physical/sw/firmware/ctrl/test"))
import ctrl_mutants
expected=[m.name for m in ctrl_mutants.MUTANTS]
rows=[];seen=[]
for i in range(4):
 name="fw-mutants-shard-"+str(i);p=w/"logs"/(name+".log");t=p.read_text()
 assert (w/"logs"/(name+".rc")).read_text().strip()=="0",name
 names=re.findall(r"^\[ok\] mutant (\S+) ",t,re.M)
 assert names==expected[i*118:(i+1)*118],(name,len(names))
 assert "[ESCAPED]" not in t and "test_ctrl_firmware: PASS" in t,name
 assert re.search(r"^mutants: "+str(len(names))+r" of "+str(len(names))+r" caught",t,re.M),name
 rows.append(dict(name=name,slice=str(i+1)+"/4",caught=len(names),rc=0,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
 seen.extend(names)
assert seen==expected and len(set(seen))==469,len(seen)
result=dict(head="85db353400c6bf3965d279a9f5b5d47e08a0d1ed",rc=0,total_caught=len(seen),complete_disjoint_coverage=True,runs=rows,names=seen)
(w/"firmware-summary.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({k:v for k,v in result.items() if k!="names"},indent=2))
