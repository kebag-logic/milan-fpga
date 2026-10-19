import hashlib,json,pathlib,subprocess,sys
root=pathlib.Path(sys.argv[1]); out=pathlib.Path(sys.argv[2])
commit="32af21b0d0ae35008fa65c3199b282419f171274"
prefix="review-evidence/761-r1/"
def show(path): return subprocess.check_output(["git","-C",str(root),"show",commit+":"+prefix+path])
manifest=json.loads(show("MANIFEST.json"))
selected=[r for r in manifest if r["file"].startswith("author-r2/receipts/r2b-") or r["file"]=="author-r2/receipts/INDEX.md"]
for row in selected:
 data=show(row["file"]); digest=hashlib.sha256(data).hexdigest()
 assert digest==row["published_sha256"],row["file"]
 dest=out/"scratch/public"/row["file"];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
 print(digest, row["file"], "OK", "redacted="+str(row["path_redacted"]))
print("PASS",len(selected),"published receipts verified against published_sha256 at",commit)
