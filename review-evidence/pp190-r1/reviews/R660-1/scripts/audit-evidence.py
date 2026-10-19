#!/usr/bin/env python3
import csv, hashlib, json, pathlib, re, sys
p=pathlib.Path(sys.argv[1]); root=p/"scratch/public-evidence"
manifest=json.loads((root/"MANIFEST.json").read_text()); mapping={i["file"]:i for i in manifest}
errors=[]
for i in manifest:
 f=root/i["file"]
 if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest()!=i["published_sha256"]: errors.append(i["file"])
actual={str(f.relative_to(root)) for f in root.rglob("*") if f.is_file()}-{"MANIFEST.json"}
index=[]; missing=[]; incorrect=[]; redacted=[]
for rel,size,sha in re.findall(r"^- `([^`]+)`  (\d+) bytes  sha256 ([a-f0-9]{64})$",(root/"author/INDEX.md").read_text(),re.M):
 key="author/"+rel; index.append(key); f=root/key
 if not f.exists(): missing.append(key); continue
 data=f.read_bytes()
 if (len(data),hashlib.sha256(data).hexdigest())!=(int(size),sha):
  m=mapping.get(key,{})
  if m.get("path_redacted") and m.get("original_sha256")==sha: redacted.append(key)
  else: incorrect.append(key)
print(json.dumps({"manifest_entries":len(manifest),"manifest_hash_errors":errors,"manifest_missing":sorted(set(mapping)-actual),"manifest_unlisted":sorted(actual-set(mapping)),"index_entries":len(index),"index_missing":missing,"index_unexplained_mismatches":incorrect,"index_documented_redactions":redacted,"index_unlisted_author_files":sorted({k for k in actual if k.startswith("author/")}-set(index)-{"author/INDEX.md"})},indent=2))
