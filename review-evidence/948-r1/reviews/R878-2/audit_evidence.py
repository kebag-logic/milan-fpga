#!/usr/bin/env python3
"""Hash all public packet entries and extract relevant gate/route receipts.
Usage: python3 audit_evidence.py CLONE (fetch the evidence commit first).
Does not execute candidate gates or interpret another review report.
"""
import gzip,hashlib,json,pathlib,re,subprocess,sys
P=pathlib.Path(__file__).resolve().parent;R=pathlib.Path(sys.argv[1]).resolve()
COMMIT="463845aade1ba97e40e11ffcf279e56925e37581"
ROOT="review-evidence/948-r1/"
def get(path):return subprocess.check_output(["git","-C",str(R),"show",COMMIT+":"+ROOT+path])
rows=json.loads(get("MANIFEST.json"));bad=[]
for row in rows:
 if hashlib.sha256(get(row["file"])).hexdigest()!=row["published_sha256"]:bad.append(row["file"])
assert not bad,bad
commit=subprocess.check_output(["git","-C",str(R),"cat-file","commit",COMMIT])
count=sum(r["file"].startswith("author-r2/") for r in rows)
signed=b"gpgsig " in commit
(P/"packet-verification.txt").write_text(f"Public packet commit: {COMMIT}\nAll {len(rows)} published_sha256 manifest entries verified; mismatches: 0.\nRound-2 author entries: {count}.\nEmbedded commit signature present: {signed}.\nHash consistency verified against the named public commit; no signer authentication claimed.\n")
b="author-r2/receipts/round2b/";lines=[]
for shape in ["8x8","1x1"]:
 for directive in ["ExtraPostPlacementOpt","ExtraTimingOpt","AltSpreadLogic_high"]:
  prefix=b+"fit/"+shape+"-"+directive+"/"
  sign=get(prefix+"signoff.txt").decode()
  vals=re.findall(r"(Slow_85C|Slow_0C|Fast_85C|Fast_0C): WNS ([+0-9.-]+).*?WHS ([+0-9.-]+)",sign)
  assert len(vals)==4 and all(float(w)>=.030 and float(h)>=0 for _,w,h in vals)
  for name in ["recipe.txt","build.rc","signoff.txt","identity.log","utilization.txt","hier-lut-moves-vs-round2.txt"]:
   t=get(prefix+name).decode()
   if name.startswith("hier-"):t="\n".join(t.splitlines()[:6]+[x for x in t.splitlines() if "aaf_rx_depkt" in x])
   lines.extend([prefix+name,t])
(P/"fit-audit.txt").write_text("\n".join(lines))
lines=[]
for name in ["gates/gates-64e55a59.txt","gates/docs-steps-64e55a59.txt","sweep/small-suites-SUMMARY-64e55a59.txt","sweep/render_mutants-64e55a59.log","sweep/milan_dp-64e55a59-excerpt.txt.gz","rtl/avtp_rxmon-suite-64e55a59.log.gz","twin/twin-gate-64e55a59.log.gz"]:
 data=get(b+name);t=gzip.decompress(data).decode() if name.endswith(".gz") else data.decode()
 if name.endswith(".gz"):
  t="\n".join(x for x in t.splitlines() if re.search(r"^# |^milan_dp rc|^checks:|^tally rc|^FANOUT|^DEPKT|^[0-9]+ checks:|^twin:|^fanout:|^caught|^RESULT|^.PASS. mutant",x))
 lines.extend([b+name,t])
(P/"published-gate-audit.txt").write_text("\n".join(lines))
print((P/"packet-verification.txt").read_text())
