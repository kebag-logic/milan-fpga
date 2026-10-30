#!/usr/bin/env python3
"""Fetch only public author evidence and pinned measurement reports."""
import base64, concurrent.futures, hashlib, json, pathlib, subprocess
P = pathlib.Path(__file__).resolve().parent
REF = "2f8fce3af1d658c6b558bf6b26598c5698144a6c"
REPO = "kebag-logic/milan-fpga"
def api(path):
    return json.loads(subprocess.check_output(["gh", "api", path]))
def contents(path, ref=REF):
    return api(f"repos/{REPO}/contents/{path}?ref={ref}")
manifest = contents("review-evidence/gptp96-r1/MANIFEST.json")
manifest = json.loads(base64.b64decode(manifest["content"]))
selected = [x for x in manifest if x["file"].startswith("author-r3/")]
def fetch(item):
    obj = contents("review-evidence/gptp96-r1/" + item["file"])
    data = base64.b64decode(obj["content"])
    digest = hashlib.sha256(data).hexdigest()
    git_blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    target = P / "scratch/public" / item["file"]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return {"file":item["file"], "sha256":digest, "manifest_match":digest == item["published_sha256"], "git_blob_match":git_blob == obj["sha"]}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    results = list(pool.map(fetch, selected))
commit=api(f"repos/{REPO}/commits/{REF}")
(P/"evidence-integrity.json").write_text(json.dumps({"ref":REF,"verification":commit["commit"]["verification"],"files":results},indent=2)+"\n")
assert results and all(x["manifest_match"] and x["git_blob_match"] for x in results)
print("Public author files checked:",len(results),"; commit signature:",commit["commit"]["verification"]["reason"])
reports=[]
for name in ["baseline-engine_util.rpt","candidate-engine_util.rpt","baseline-engine_timing.rpt","candidate-engine_timing.rpt"]:
    ref="4999d8d6344e373e0204995cb36c93cf616e8f9e"
    obj=contents("review-evidence/gptp75-r1/author/"+name,ref)
    data=base64.b64decode(obj["content"])
    (P/"scratch"/name).write_bytes(data)
    lines=data.decode().splitlines()
    excerpts=[{"line":i+1,"text":s} for i,s in enumerate(lines) if any(t in s for t in ["Slice LUTs", "Slice Registers", "LUT as Memory", "Block RAM Tile", "DSPs", "WNS(ns)"])]
    for i,s in enumerate(lines):
        if "WNS(ns)" in s: excerpts += [{"line":j+1,"text":lines[j]} for j in range(i+1,min(i+5,len(lines)))]
    reports.append({"name":name,"ref":ref,"blob":obj["sha"],"sha256":hashlib.sha256(data).hexdigest(),"excerpts":excerpts})
(P/"report-link-check.json").write_text(json.dumps(reports,indent=2)+"\n")
print("Report targets verified:",len(reports))
