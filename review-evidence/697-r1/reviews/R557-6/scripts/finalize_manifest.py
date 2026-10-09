#!/usr/bin/env python3
import hashlib,json,pathlib,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve(); p=pathlib.Path(sys.argv[2]).resolve()
subprocess.run([sys.executable,str(p/"scripts/verify_checkout.py"),str(root),str(p/"receipts/checkout-integrity.json")],check=True)
report=(p/"REPORT.md").read_text()
assert report.splitlines()[0]=="[R557] NEGATIVE - exact head 6bb706e2c75c7a437d9a0b2e44eb9ebb6d7f54d5"
assert report.splitlines()[-1]=="R557-6 FINISHED" and "SKELETON" not in report
for entry in json.loads((p/"receipts/prior-provenance.json").read_text()):
 assert subprocess.check_output(["git","hash-object",str(p/entry["file"])],text=True).strip()==entry["blob"]
paths=[p/"REPORT.md",*sorted((p/"scripts").rglob("*")),*sorted((p/"receipts").rglob("*"))]
paths=[x for x in paths if x.is_file()]
assert all("scratch" not in x.relative_to(p).parts and "__pycache__" not in x.parts for x in paths)
manifest="".join(hashlib.sha256(x.read_bytes()).hexdigest()+"  "+x.relative_to(p).as_posix()+"\n" for x in paths)
(p/"MANIFEST.sha256").write_text(manifest)
for line in manifest.splitlines():
 digest,name=line.split("  ",1); assert hashlib.sha256((p/name).read_bytes()).hexdigest()==digest
print("Manifest verified:",len(paths),"publishable files;",sum(x.stat().st_size for x in paths),"bytes; scratch excluded; original probe blobs unchanged")
