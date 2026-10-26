import hashlib,json,pathlib,subprocess,sys
out=pathlib.Path(sys.argv[1]); rev="2d88c87ca36b521ac875b6299c2a3204040e942b"; prefix="review-evidence/665s1-r1/"
def blob(p): return subprocess.check_output(["git","show",rev+":"+prefix+p])
manifest=json.loads(blob("MANIFEST.json")); checks=[]
for x in manifest:
 p=x["file"]; data=blob(p); digest=hashlib.sha256(data).hexdigest()
 checks.append({"file":p,"sha256":digest,"matches":digest==x["published_sha256"]})
 if p.startswith(("author-r4/receipts/","author-r4/probes/")) or p.endswith(("probe_ack.py","response_probe.py")):
  dest=out/"scratch"/"evidence"/p; dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
commit=subprocess.check_output(["git","cat-file","commit",rev])
files=subprocess.check_output(["git","ls-tree","-r","--name-only",rev,prefix],text=True).splitlines()
result={"evidence_commit":rev,"files_checked":len(checks),"all_match":all(c["matches"] for c in checks),"commit_signature_header":b"gpgsig " in commit,"signature_files":[p for p in files if p.endswith((".sig",".asc",".sign"))],"checks":checks}
(out/"evidence-hashes.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({k:v for k,v in result.items() if k!="checks"},indent=2))
