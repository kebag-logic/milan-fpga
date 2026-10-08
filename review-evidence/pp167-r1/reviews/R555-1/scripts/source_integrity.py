#!/usr/bin/env python3
"""Check index, tracked blob bytes and executable modes against the requested commit."""
import hashlib, json, os, pathlib, stat, subprocess, sys
root = pathlib.Path(sys.argv[1]).resolve()
head = "f3fef22448ce4f9bed8fd249a21a5d472148bd3d"
def git(*a): return subprocess.check_output(["git", "-C", str(root), *a])
assert git("rev-parse", "HEAD").decode().strip() == head
assert git("rev-parse", "HEAD^{tree}").decode().strip() == "38da2da1e826d053d384380e202617054a1ef218"
entries = git("ls-tree", "-rz", "--full-tree", head).split(b"\0")
rows=[]; links=[]
for entry in entries:
    if not entry: continue
    metadata, name = entry.split(b"\t", 1)
    mode, kind, blob = metadata.decode().split()
    rel = name.decode(); f = root / rel
    if kind == "commit":
        links.append({"path":rel,"gitlink":blob}); continue
    data = os.readlink(f).encode() if mode == "120000" else f.read_bytes()
    actual=hashlib.sha1(b"blob " + str(len(data)).encode()+b"\0"+data).hexdigest()
    actualmode = "120000" if f.is_symlink() else ("100755" if f.stat().st_mode & stat.S_IXUSR else "100644")
    assert actual==blob and actualmode==mode, rel
    rows.append({"path":rel,"mode":mode,"blob":blob})
assert not git("diff", "--cached", "--name-only", head).strip()
assert not git("diff", "--name-only", head).strip()
print(json.dumps({"head":head,"tree":git("rev-parse","HEAD^{tree}").decode().strip(),"tracked_count":len(rows),"tracked_bytes_modes_match":True,"index_matches":True,"submodule_gitlinks":links,"status":git("status","--short").decode(),"entries":rows},indent=2))
