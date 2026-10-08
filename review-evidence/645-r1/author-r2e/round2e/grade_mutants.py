import hashlib,json,re
from pathlib import Path
w=Path(__file__).resolve().parent
rows=[]
for name,head,total in (("dev-render-mutants","99e4eb6c14462aafa84bb1ac597fd241abc1a240",32),("render-mutants","85db353400c6bf3965d279a9f5b5d47e08a0d1ed",34)):
 p=w/"logs"/(name+".log");t=p.read_text()
 rc=int((w/"logs"/(name+".rc")).read_text())
 failures=re.findall(r"^\[FAIL\].*$",t,re.M)
 passes=re.findall(r"^\[PASS\].*$",t,re.M)
 summary=re.findall(r"^"+str(total)+r" checks: "+str(total-4)+r" PASS, 4 FAIL.*$",t,re.M)
 assert rc==2 and len(failures)==4 and len(passes)==total-4 and len(summary)==1,(name,rc,failures,summary)
 assert any("unmutated gateware" in s and "epoch-only" in s for s in failures),failures
 assert sum("clean control" in s for s in failures)==2,failures
 assert any("uncounted repeat" in s and "SURVIVED" in s for s in failures),failures
 rows.append(dict(name=name,head=head,rc=rc,total=total,passed=len(passes),summary=summary[0],failures=failures,passes=passes,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
assert rows[0]["failures"]==rows[1]["failures"],rows
extra=[s for s in rows[1]["passes"] if s not in rows[0]["passes"]]
assert len(extra)==2 and any("unmutated gateware" in s and "--pullin" in s for s in extra) and any("settle recentre never pulses" in s for s in extra),extra
assert [s for s in rows[1]["passes"] if s not in extra]==rows[0]["passes"],rows
out=dict(issue=657,expected_failures_match=True,common_checks_match=True,additional_lane_controls=extra,regression=False,runs=rows)
(w/"mutation-comparison.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({k:v for k,v in out.items() if k!="runs"},indent=2))
print("dev:",rows[0]["summary"],"; candidate:",rows[1]["summary"])
