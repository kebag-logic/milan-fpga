import base64,concurrent.futures,hashlib,json,pathlib,subprocess
P=pathlib.Path(__file__).resolve().parent
if not (P/'scratch/evidence-tree.json').exists():
 (P/'scratch').mkdir(parents=True,exist_ok=True)
 (P/'scratch/evidence-tree.json').write_bytes(subprocess.check_output(['gh','api','repos/kebag-logic/milan-fpga/git/trees/08802d050fdd4d66f29378c470dfe9093985ab8a?recursive=1']))
T=json.loads((P/"scratch/evidence-tree.json").read_text())["tree"]
prefix="review-evidence/pp203-r1/"
selected=[]
for a in T:
 p=a["path"]
 if a["type"]!="blob" or not p.startswith(prefix): continue
 rel=p[len(prefix):]
 yes=rel=="MANIFEST.json" or rel in ["reviews/R732-2/post-departure-probe.patch","reviews/R732-2/nonadvertising-probe.patch","reviews/R732-2/run-probes.py","reviews/R731-1/probes/window-after-notification-round.patch"]
 if rel.startswith("author-r3/receipts/"):
  yes=("/processor/head-" in rel and not rel.endswith(".mem")) or ("/processor/tx-arbiter-plants/" in rel and not rel.endswith("INDEX.md")) or ("/campaigns/" in rel and "013ee63/" in rel and (rel.endswith((".rc",".cmd")) or rel.endswith(".log") and ("/out/" not in rel or "/rbt-" in rel))) or any(s in rel for s in ["/parent/full-tally/","/parent/static-docs-","/parent/rom-digests/"]) or rel.endswith(("processor-records.txt","parent-records.txt"))
 if rel.startswith('author-r3/receipts/parent/') and ('ooc-area/' in rel and rel.endswith('.log') or 'sweep-b63bd18a/' in rel and rel.endswith(('summary.json','complete.json','results.json'))): yes=True
 if yes: selected.append((a,rel))
def fetch(item):
 a,rel=item
 out=P/"public"/rel; out.parent.mkdir(parents=True,exist_ok=True)
 if not out.exists():
  raw=subprocess.check_output(["gh","api","repos/kebag-logic/milan-fpga/git/blobs/"+a["sha"]])
  out.write_bytes(base64.b64decode(json.loads(raw)["content"]))
 data=out.read_bytes(); assert hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()==a["sha"]
 return {"path":rel,"blob":a["sha"],"sha256":hashlib.sha256(data).hexdigest()}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex: result=list(ex.map(fetch,selected))
(P/"evidence-download-audit.json").write_text(json.dumps(result,indent=2)+"\n")
print("Verified",len(result),"public Git blobs; no review reports fetched")
