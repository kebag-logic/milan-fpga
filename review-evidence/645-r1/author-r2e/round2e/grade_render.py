import hashlib,json,re
from pathlib import Path
w=Path(__file__).resolve().parent
for name in ("render-pullin","render-boundary"):
 assert (w/"logs"/(name+".rc")).read_text().strip()=="0",name
rows=[]
root=w/"functional/render-pullin/tb/verilator/milan_dp_render/obj_pullin"
for p in sorted(root.glob("pullin_*.log")):
 t=p.read_text();phase=int(p.stem.split("_")[-1])
 counts=re.findall(r"== tdm8_render: checks: (\d+) +failures: (\d+) ==",t)
 assert len(counts)==1 and counts[0][1]=="0" and "RESULT: PASS" in t,p
 actions=re.findall(r"the settle recentre came (\d+) axis cycles \(([^)]+)\) after the hold; loopback slips (\d+) during the pull, (\d+) after the settle",t)
 assert len(actions)==1 and actions[0][2:]==("0","0"),(p,actions)
 rows.append(dict(phase=phase,checks=int(counts[0][0]),not_gradable="NOT GRADABLE" in t,settle_axis_cycles=int(actions[0][0]),settle_time=actions[0][1],bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
assert sorted(r["phase"] for r in rows)==[0,130,260,391,521,651,781,911,927,1042,1156,1172,1302,1432,1562,1693,1823,1953]
p=w/"logs/render-boundary.log";t=p.read_text();counts=re.findall(r"^(\d+) checks: (\d+) PASS, (\d+) FAIL.*$",t,re.M)
assert counts and counts[-1][0]==counts[-1][1] and counts[-1][2]=="0",counts
result=dict(head="85db353400c6bf3965d279a9f5b5d47e08a0d1ed",rc=0,pullin_phases=len(rows),pullin_checks=sum(r["checks"] for r in rows),pullin_not_gradable=sum(r["not_gradable"] for r in rows),pullin=rows,boundary_checks=int(counts[-1][0]),boundary_bytes=p.stat().st_size,boundary_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),boundary_details=[l for l in t.splitlines() if "largest walk" in l or "ambiguity window" in l])
(w/"render-summary.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({k:v for k,v in result.items() if k!="pullin"},indent=2))
