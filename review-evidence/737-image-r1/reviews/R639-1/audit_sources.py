#!/usr/bin/env python3
"""Read-only scope and source-lock checks with no image execution."""
import hashlib,json,re,subprocess,sys,urllib.parse
from collections import Counter
from pathlib import Path
root=Path(sys.argv[1]);base="fa7347fc59173f90e4feec2df207692e6e6e72ec";head="2b2e4d2c5b7f43cfc9df5347d99f9fee2c1fb895"
def git(*args):return subprocess.check_output(["git","--no-replace-objects","-C",str(root),*args])
diff=git("diff","--no-ext-diff","--no-textconv",base+".."+head)
paths=git("diff","--name-only",base+".."+head).decode().splitlines()
assert not any(p.startswith((".github/workflows/","hdl/","sw/firmware/")) for p in paths)
pins=json.loads((root/"ci/image/sources.lock.json").read_text());lock=json.loads((root/"ci/image/image.lock.json").read_text());inv=json.loads((root/"ci/image/tool-inventory.json").read_text())
rows=pins["sources"]+pins["packages"]
for row in rows:
 u=urllib.parse.urlparse(row["url"])
 assert u.scheme=="https" and not u.username and not u.password and not u.query and not u.fragment,row["tool"]
 assert re.fullmatch("[0-9a-f]{64}",row["sha256"]) and row["size"]>0 and row["version"],row["tool"]
assert len({row["tool"].lower() for row in rows})==len(rows)
assert sorted((row["tool"],row["version"],row["sha256"]) for row in rows)==sorted((row["tool"],row["version"],row["source_digest"]) for layer in lock["layers"] for row in layer["tools"])
for name,digest in inv["inputs"].items():assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,name
assert (root/"ci/image/Dockerfile").read_text().splitlines()[0]==f"FROM {pins['base']} AS system-tools"
assert pins["base"]==lock["base"] and pins["platform"]==lock["platform"]
print(json.dumps({"head":head,"base":base,"diff_sha256":hashlib.sha256(diff).hexdigest(),"paths":paths,"workflow_diff_empty":True,"rtl_firmware_diff_empty":True,"gitlink_diff":git("diff","--raw",base+".."+head,"--","protocol-processor","gptp-processor","third_party").decode(),"commits":git("log","--format=%H %s",base+".."+head).decode().splitlines(),"inventory_input_count":len(inv["inputs"]),"inventory_inputs_match_disk":True,"requested_tool_rows":len(inv["tools"]),"package_artifacts":len(pins["packages"]),"source_artifacts":len(pins["sources"]),"source_kinds":dict(Counter(r.get("kind","native") for r in pins["sources"])),"total_artifact_bytes":sum(r["size"] for r in rows),"origins":sorted({urllib.parse.urlparse(r["url"]).hostname for r in rows}),"url_userinfo_absent":True,"all_source_rows_in_lock_exactly_once":True,"base_pinned_and_consistent":True,"image_digest":lock["image_digest"],"recipe_digest":lock["recipe_digest"],"limitations":"Checks verify declaration consistency, not remote artifact availability or built image layer privacy."},indent=2,sort_keys=True))
