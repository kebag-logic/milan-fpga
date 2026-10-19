#!/usr/bin/env python3
"""Read-only audit: audit_delta.py CHECKOUT PACKET. No source execution."""
import ast, collections, hashlib, json, pathlib, re, subprocess, sys
repo, packet = map(pathlib.Path, sys.argv[1:])
head="07c6c72fce79e705bcf28a70071497d0ce7040e4"
base="e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f"
evidence="687310c882ef2f6275650ac267018e682e5bf7b2"
prefix="review-evidence/763-r1/"
def git(*args): return subprocess.check_output(["git","-C",str(repo),*args])
def sha(b): return hashlib.sha256(b).hexdigest()
assert git("rev-parse","HEAD").decode().strip()==head
assert git("rev-parse","HEAD^{tree}").decode().strip()=="c70d7afe29d34724474bfc05053fe3cb43801026"
changed=git("diff","--name-only",base,head).decode().splitlines()
assert len(changed)==4
inventory=json.loads((repo/"ci/image/tool-inventory.json").read_text())
stale={}
for f,h in inventory["inputs"].items():
 actual=sha((repo/f).read_bytes())
 if actual!=h:
  old=sha(git("show",f"{base}:{f}"))
  stale[f]={"recorded":h,"head":actual,"base":old,"inherited":actual==old}
assert len(stale)==4
inputs_changed=sorted(set(changed)&set(inventory["inputs"]))
assert inputs_changed==["sw/firmware/ctrl/test/aecp_arms.py","sw/firmware/ctrl/test/aecp_mutants.py"]
manifest=json.loads((packet/"receipts/public-MANIFEST.json").read_text())
verified=collections.Counter()
for row in manifest:
 f=row["file"]
 if not f.startswith(("author/receipts/","author-r2/receipts/")): continue
 b=git("show",f"{evidence}:{prefix}{f}")
 assert sha(b)==row["published_sha256"], f
 verified[f.split("/")[0]]+=1
published=packet/"receipts/published"
index=(published/"INDEX.md").read_text()
rows=re.findall(r"^\| `([^`]+)` \| (\d+) \| `([a-f0-9]{64})` \|$",index,re.M)
for f,n,h in rows:
 b=(published/f).read_bytes(); assert len(b)==int(n) and sha(b)==h,f
assert {f for f,_,_ in rows}=={str(p.relative_to(published)) for p in published.rglob("*") if p.is_file()}-{"INDEX.md"}
log=(published/"round-b/gates/test_ctrl_firmware/extract.log").read_text()
lines=[s[5:] for s in log.splitlines() if s.startswith("[ok] ")]
counts=collections.Counter(); named=[]
for s in lines:
 if s.startswith("arm "): counts["normal arm outcome"]+=1
 elif s.startswith("mutant "): counts["control-source mutant"]+=1
 elif s.startswith("lwSRP pin, "): counts["dependency-pin refusal control"]+=1
 else: named.append(s)
def literals(path):
 return {n.value for n in ast.walk(ast.parse(path.read_text())) if isinstance(n,ast.Constant) and isinstance(n.value,str)}
test=repo/"sw/firmware/ctrl/test"
aecp=literals(test/"aecp_mutants.py")
srp=set().union(*(literals(p) for p in test.glob("srp*mutants.py")))
# Separate the ordered campaign blocks, then prove every name against source literals.
# The shared reentry name must stay in its own block; no line is discarded.
assert len(named)==356
for i,s in enumerate(named):
 cls="AECP mutant" if i<78 else "SRP mutant"
 assert s.split(":",1)[0] in (aecp if i<78 else srp),s
 counts[cls]+=1
expected={"AECP mutant":78,"SRP mutant":278,"control-source mutant":520,"dependency-pin refusal control":2,"normal arm outcome":61}
assert dict(counts)==expected
for f in ["round-2/count/classify.json","round-2/count/classify-full-log.json"]:
 c=json.loads((published/f).read_text());assert c["classes"]==expected and c["source_mutant_executions"]==876
summary=(published/"round-b/gates/test_ctrl_firmware/summary.txt").read_text()
body=json.loads((packet/"receipts/pr766.json").read_text())["body"]
assert "876 source-mutant executions caught" in body and "876 source-mutant executions caught" in summary
assert "two commits at published head" in body and "to be assigned" not in body and "not yet pushed" not in body
assert log.rstrip().endswith("test_ctrl_firmware: PASS")
# The unchanged head and public evidence provide the round-1 basis; no bank rerun.
report={"head":head,"tree":git("rev-parse","HEAD^{tree}").decode().strip(),"changed_files":changed,"changed_inventory_inputs":inputs_changed,"stale_inputs":stale,"verified_public_receipts":dict(verified),"verified_index_rows":len(rows),"gate_counts":dict(counts),"top_level_ok":len(lines),"source_mutant_executions":876,"signature":json.loads((packet/"receipts/evidence-signature.json").read_text())["verification"],"status":"PASS"}
(packet/"receipts/delta-audit.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2))
