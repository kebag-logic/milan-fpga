import base64, concurrent.futures, hashlib, json, pathlib, subprocess
PACKET=pathlib.Path(__file__).resolve().parent
REV="67e05179f28bc777a18f136cfdb759e2adf9750c"
PREFIX="review-evidence/744-r1/"
def api(path):
    return json.loads(subprocess.check_output(["gh","api","repos/kebag-logic/milan-fpga/"+path]))
def fetch(name):
    data=base64.b64decode(api("contents/"+PREFIX+name+"?ref="+REV)["content"])
    dest=PACKET/"public"/name
    dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(data)
    return name,hashlib.sha256(data).hexdigest()
manifest=api("contents/"+PREFIX+"MANIFEST.json?ref="+REV)
raw=base64.b64decode(manifest["content"])
(PACKET/"public").mkdir(exist_ok=True)
(PACKET/"public/MANIFEST.json").write_bytes(raw)
rows=json.loads(raw)
selected=[r for r in rows if r["file"].startswith("author-r2/evidence/")]
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    hashes=dict(pool.map(fetch,[r["file"] for r in selected]))
for r in selected:
    assert hashes[r["file"]]==r["published_sha256"],r["file"]
commit=api("commits/"+REV)
verification=commit["commit"]["verification"]
(PACKET/"public/commit-verification.json").write_text(json.dumps(verification,indent=2)+"\n")
print("Public evidence commit:",REV)
print("GitHub signature verification:",verification["verified"],verification["reason"])
print("Checked published SHA-256:",len(selected),"of",len(selected),"author execution receipts; no handoff or reviewer reports read")
for r in selected: print(hashes[r["file"]],r["file"])
