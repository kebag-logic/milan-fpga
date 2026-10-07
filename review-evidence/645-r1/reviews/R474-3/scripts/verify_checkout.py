"""Verify a checkout equals its HEAD: tracked bytes/modes vs index, index tree vs HEAD tree, gitlinks, clean status.

usage: python3 -I verify_checkout.py <repo> <expected-head> <expected-tree>
"""
import json, os, stat, subprocess, sys
repo, want_head, want_tree = sys.argv[1:4]
def git(*a):
    return subprocess.run(["git", "-C", repo, *a], check=True, capture_output=True).stdout
out = {"head": git("rev-parse", "HEAD").decode().strip(),
       "head_tree": git("rev-parse", "HEAD^{tree}").decode().strip(),
       "index_tree": git("write-tree").decode().strip()}
bad, n, links = [], 0, {}
for rec in git("ls-files", "-s", "-z").split(b"\0"):
    if not rec:
        continue
    meta, path = rec.split(b"\t", 1)
    mode, sha, stage = meta.decode().split()
    path = path.decode()
    if stage != "0":
        bad.append(("stage", path)); continue
    if mode == "160000":
        # an uninitialised submodule (no .git of its own) has no checkout to compare
        init = os.path.exists(os.path.join(repo, path, ".git"))
        sub = git("-C", path, "rev-parse", "HEAD").decode().strip() if init else None
        links[path] = {"gitlink": sha, "checkout": sub, "initialised": init, "match": sub == sha if init else None}
        continue
    n += 1
    full = os.path.join(repo, path)
    st = os.lstat(full)
    if mode == "120000":
        ok = stat.S_ISLNK(st.st_mode)
        h = subprocess.run(["git", "hash-object", "--stdin"], input=os.readlink(full).encode(), capture_output=True).stdout.decode().strip() if ok else None
    else:
        ok = stat.S_ISREG(st.st_mode) and (("100755" if st.st_mode & 0o111 else "100644") == mode)
        h = subprocess.run(["git", "hash-object", "--no-filters", full], capture_output=True).stdout.decode().strip()
    if not ok or h != sha:
        bad.append(("blob", path))
out.update(blobs=n, mismatches=bad, gitlinks=links,
           status_ignored=git("status", "--porcelain", "--ignored").decode())
out["pass"] = (out["head"] == want_head and out["head_tree"] == want_tree == out["index_tree"]
               and not bad and all(v["match"] for k, v in links.items() if v["checkout"])
               and out["status_ignored"] == "")
print(json.dumps(out, indent=1))
sys.exit(0 if out["pass"] else 1)
