"""Verify immutable public receipts without reading any other review."""
import hashlib,json,subprocess
from pathlib import Path
P=Path(__file__).resolve().parent
REV="707462eaa175afedaeb6acd2e3fded6073e0d51d"
BASE="review-evidence/665s4-r1/"
def blob(path):
    return subprocess.check_output(["git","show",f"{REV}:{BASE}{path}"])
manifest=json.loads(blob("MANIFEST.json"))
count=0
for row in manifest:
    name=row["file"]
    if not name.startswith("author-r3/receipts/"): continue
    data=blob(name)
    assert hashlib.sha256(data).hexdigest()==row["published_sha256"],name
    target=P/"scratch/public"/name
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(data)
    count+=1
print(f"PASS: {count} author current-round receipts match published SHA256 manifest at {REV}")
print("Commit signature status: "+subprocess.check_output(["git","show","-s","--format=%G?",REV],text=True).strip()+" (N means no commit signature; hashes do not authenticate a signer)")
for group in ("gates-short","gates-long"):
    root=P/"scratch/public/author-r3/receipts"/group
    print(group,"HEAD",(root/"HEAD.txt").read_text().strip())
    for f in root.glob("summary*.md"): print(f.read_text())
