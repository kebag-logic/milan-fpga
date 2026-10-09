#!/usr/bin/env python3
"""Check public receipt hashes and bindings without executing packet code."""
import argparse,hashlib,json,pathlib,subprocess
from decimal import Decimal as D
p=argparse.ArgumentParser();p.add_argument("source",type=pathlib.Path);p.add_argument("packet",type=pathlib.Path);a=p.parse_args()
def blob(rev,path):return subprocess.check_output(["git","-C",str(a.source),"show",rev+":"+path])
def load(rev,path):return json.loads(blob(rev,path))
result={}
for name,rev,head in [("author-r2h","5c575da7157c814088ea4df12aab6c5877841f4b","8e4b1e53e9b5a8ef5f9854095347436ab84259b6"),("author-r2i","49a9c79c43ae9b7d54011b148a1cbeea113cae4c","7426045c94c317363e5589856e6f3f9fde1a2d21")]:
 prefix="review-evidence/645-r1/"+name+"/"
 entries=blob(rev,prefix+"MANIFEST.sha256").decode().splitlines()
 for line in entries:
  digest,path=line.split("  ",1)
  assert hashlib.sha256(blob(rev,prefix+path)).hexdigest()==digest,path
 bindings=(load(rev,prefix+"measured-source-binding.json") if name.endswith('h') else load(rev,prefix+"source-binding.json")["files"])
 for row in bindings:
  assert hashlib.sha256(blob(head,row["path"])).hexdigest()==row.get("candidate_sha256",row.get("sha256")),row["path"]
 jobs={}
 for label in (["follow-default","render-default","follow-outer-j16","follow-mutants","builder"] if name.endswith('h') else ["builder","trace-duplicate","trace-pullin","trace-skip"]):
  receipt=load(rev,prefix+"jobs/"+label+".result.json");assert receipt["rc"]==0;assert blob(rev,prefix+"jobs/"+label+".rc").strip()==b"0";jobs[label]=receipt
 if name.endswith('i'):
  summary=load(rev,prefix+'validation-summary.json')
  for row in summary['results']:
   assert row['rc']==0 and blob(rev,prefix+'jobs/'+row['name']+'.rc').strip()==b'0',row
  assert len(summary['results'])==48
 result[name]={"archive":rev,"head":head,"manifest_entries":len(entries),"candidate_source_bindings":len(bindings),"jobs":jobs,"pass":True}
rev="49a9c79c43ae9b7d54011b148a1cbeea113cae4c";prefix="review-evidence/645-r1/author-r2i/"
timings=load(rev,prefix+"hosted-timings.json")
for w in timings["windows"]:
 def stamp(s):
  h,m,second=s.split('T')[1].rstrip('Z').split(':');return D(h)*3600+D(m)*60+D(second)
 actual=stamp(w['end'])-stamp(w['start']);rounded=actual.quantize(D('.1'))
 assert rounded==D(str(w['seconds']))
 assert D('1440')-rounded==D(str(w['margin_to_1440']))
 assert D('1800')-rounded==D(str(w['margin_to_1800']))
 w['independent_decimal_seconds']=str(actual)
result['hosted_windows']=timings
for path in ['docs/testing/TESTING.md','tb/verilator/follow_ring/Makefile','tb/verilator/milan_dp_render/Makefile']:
 content=blob('HEAD',path).decode()
 for token in ['37892515345','113696564335']:
  assert token in content,(path,token)
 fields=['1114.2','325.8','685.8'] if '/follow_ring/' in path else ['1218.7','221.3','581.3'] if '/milan_dp_render/' in path else ['1114.2','325.8','685.8','1218.7','221.3','581.3']
 for token in fields:assert token in content,(path,token)
result['three_timing_records_match']=True
out=a.packet/'receipts/public-verification.json';out.write_text(json.dumps(result,indent=2)+'\n')
print('Public manifests, source bindings, command results and all three timing records: PASS')
