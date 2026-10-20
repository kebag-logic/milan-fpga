"""Fetch selected public evidence, checking each payload against its Git blob."""
import base64, concurrent.futures, hashlib, json, pathlib, subprocess
P = pathlib.Path(__file__).resolve().parent
REV = "4d31fa3d8b9bd09b15b2f4b78ed7b8f2c2d04a47"
PREFIX = "review-evidence/637-r1/"
def api(endpoint):
    return json.loads(subprocess.check_output(["gh", "api", "repos/kebag-logic/milan-fpga/"+endpoint]))
tree = api("git/trees/"+REV+"?recursive=1")
assert not tree.get("truncated")
(P/"scratch/evidence-tree.json").write_text(json.dumps(tree))
commit = api("commits/"+REV)
(P/"evidence-commit.json").write_text(json.dumps(commit, indent=2))
selected=[]
for t in tree["tree"]:
    s=t["path"]
    if t["type"] != "blob" or not s.startswith(PREFIX): continue
    r=s[len(PREFIX):]
    take = r == "MANIFEST.json" or r in ("author-r3/HANDOFF.md", "author-r3/PR-BODY.md")
    if r.startswith("author-r3/receipts/round3/"):
        take = ("/docs/" not in r and "/scripts/" not in r) or r.endswith(("docs/rc.tsv", "docs/identity.txt", "docs/d0-43-check_cpp_idiom.log", "docs/d0-40-measure_test_evidence.log"))
    if r.startswith("author-r3/receipts/round2/campaign/") and ("af5eefc6" in r): take=True
    if take: selected.append((r,t))
def fetch(item):
    r,t=item
    b=base64.b64decode(api("git/blobs/"+t["sha"])["content"])
    sha=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
    assert sha==t["sha"]
    f=P/"published"/r; f.parent.mkdir(parents=True,exist_ok=True); f.write_bytes(b)
    return {"path":r,"git_blob":sha,"sha256":hashlib.sha256(b).hexdigest(),"bytes":len(b)}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool: receipts=list(pool.map(fetch,selected))
(P/"evidence-provenance.json").write_text(json.dumps({"revision":REV,"receipts":receipts},indent=2))
print("Fetched and Git-blob-verified",len(receipts),"public artifacts")
print("Signature verification:",commit["commit"]["verification"]["verified"],commit["commit"]["verification"]["reason"])
