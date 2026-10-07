#!/usr/bin/env python3
"""R474-2: verify every tracked blob's bytes and mode in a checkout against its
index, the index tree against HEAD's tree, and the submodule gitlinks against
expected pins. Usage: verify_checkout.py REPO EXPECTED_TREE path=sha ..."""
import json, os, stat, subprocess, sys
repo, want_tree, pins = sys.argv[1], sys.argv[2], dict(a.split("=") for a in sys.argv[3:])
def git(*a, inp=None):
    return subprocess.run(["git", "-C", repo, *a], capture_output=True, input=inp, check=True).stdout
entries = git("ls-files", "-s", "-z").split(b"\0")
bad, n, links = [], 0, {}
paths, shas = [], []
for e in filter(None, entries):
    meta, path = e.split(b"\t", 1)
    mode, sha, stage = meta.split()
    path = path.decode()
    if mode == b"160000":
        links[path] = sha.decode(); continue
    n += 1
    full = os.path.join(repo, path)
    st = os.lstat(full)
    if mode == b"120000":
        ok = stat.S_ISLNK(st.st_mode)
        data = os.readlink(full).encode()
        got = git("hash-object", "--stdin", inp=data).strip().decode()
    else:
        exe = bool(st.st_mode & 0o100)
        ok = stat.S_ISREG(st.st_mode) and exe == (mode == b"100755")
        paths.append(path); shas.append(sha.decode()); continue
    if not ok or got != sha.decode():
        bad.append(path)
out = git("hash-object", "--", *paths).decode().split() if paths else []
for p, want, got in zip(paths, shas, out):
    if want != got: bad.append(p)
for p in paths:
    st = os.lstat(os.path.join(repo, p))
mode_bad = []
for e in filter(None, entries):
    meta, path = e.split(b"\t", 1); mode = meta.split()[0]; path = path.decode()
    if mode in (b"100644", b"100755"):
        st = os.lstat(os.path.join(repo, path))
        if bool(st.st_mode & 0o100) != (mode == b"100755"): mode_bad.append(path)
tree = git("write-tree").strip().decode()
head_tree = git("rev-parse", "HEAD^{tree}").strip().decode()
res = {"blobs_checked": n, "content_mismatch": bad, "mode_mismatch": mode_bad,
       "index_tree": tree, "head_tree": head_tree, "expected_tree": want_tree,
       "gitlinks": links, "gitlink_pins_ok": all(links.get(k) == v for k, v in pins.items()),
       "result": "PASS" if not bad and not mode_bad and tree == head_tree == want_tree
                 and all(links.get(k) == v for k, v in pins.items()) else "FAIL"}
print(json.dumps(res, indent=1))
