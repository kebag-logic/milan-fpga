"""Verify public evidence against GitHub blob identities and preserve its published manifest verdict."""
import hashlib,json,subprocess
from pathlib import Path
out=Path(__file__).resolve().parent
ref="b9a05dc9a31825fdbd7ffc5eb638dc9fe751fc6c"
base="review-evidence/517-r1/followups/523-readiness"
rows=[]
def check(path):
    entries=json.loads(subprocess.check_output(["gh","api",f"repos/kebag-logic/milan-fpga/contents/{path}?ref={ref}"]))
    for e in entries:
        if e["type"]=="dir":check(e["path"])
        else:
            data=(out/"original-public"/e["path"]).read_bytes()
            blob=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
            assert blob==e["sha"],e["path"]
            rows.append(dict(path=e["path"],blob=blob,sha256=hashlib.sha256(data).hexdigest(),size=len(data)))
check(base)
result=subprocess.run(["sha256sum","-c","SHA256SUMS"],cwd=out/"original-public"/base,capture_output=True,text=True,check=False)
(out/"published-manifest-verdict.log").write_text(result.stdout+result.stderr)
record=dict(public_ref=ref,verified_public_blobs=rows,published_sha256_manifest_exit=result.returncode,
            published_sha256_manifest_output=result.stdout+result.stderr)
(out/"public-evidence-verification.json").write_text(json.dumps(record,indent=2)+"\n")
print("Verified",len(rows),"downloaded files against exact public Git blob IDs.")
print("Published SHA256SUMS exit:",result.returncode)
print(result.stdout+result.stderr)
