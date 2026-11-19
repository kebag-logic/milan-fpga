import hashlib,json,pathlib,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve()
out=pathlib.Path(__file__).resolve().parent
rev="f9f1e85d91749fbba4506b54236e63f3eeba7ca6"
prefix="review-evidence/943-r1/"
def git(*args): return subprocess.check_output(["git","-C",str(root),*args])
manifest=json.loads(git("show",rev+":"+prefix+"MANIFEST.json"))
selected=[r for r in manifest if r["file"].startswith(("author-r1/","author-r2/"))]
for r in selected:
    data=git("show",rev+":"+prefix+r["file"])
    digest=hashlib.sha256(data).hexdigest()
    assert digest==r["published_sha256"],r["file"]
    dest=out/"scratch"/"archive"/r["file"]
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
    print(digest,r["file"],"PASS")
print("Verified",len(selected),"published author files against MANIFEST.json; review reports not read.")
print("Archive signature status:",git("show","-s","--format=%G?",rev).decode().strip())
print("SHA256 is integrity evidence, not a cryptographic signer identity.")
