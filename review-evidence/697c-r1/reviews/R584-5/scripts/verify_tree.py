"""Verify a checkout against its HEAD: the index equals HEAD's tree (paths, modes, blob ids and gitlinks), every
tracked regular file and symbolic link on disk hashes to its blob with its mode, and each initialised submodule's
HEAD equals its gitlink. usage: python3 -I verify_tree.py <checkout>"""
import hashlib, os, stat, subprocess, sys
root = sys.argv[1]
def git(*a): return subprocess.run(["git", "-C", root, *a], capture_output=True, check=True).stdout
tree = {}
for e in git("ls-tree", "-r", "-z", "--full-tree", "HEAD").split(b"\0"):
    if e:
        meta, path = e.split(b"\t", 1); mode, kind, oid = meta.split(); tree[path.decode()] = (mode.decode(), oid.decode())
index = {}
for e in git("ls-files", "-s", "-z").split(b"\0"):
    if e:
        meta, path = e.split(b"\t", 1); mode, oid, stage = meta.split(); index[path.decode()] = (mode.decode(), oid.decode())
bad = [f"index differs: {p}" for p in sorted(set(tree) | set(index)) if tree.get(p) != index.get(p)]
links = 0
for path, (mode, oid) in sorted(tree.items()):
    full = os.path.join(root, path)
    if mode == "160000":
        head = subprocess.run(["git", "-C", full, "rev-parse", "HEAD"], capture_output=True, text=True)
        if head.returncode == 0 and os.path.exists(os.path.join(full, ".git")):
            links += 1
            if head.stdout.strip() != oid: bad.append(f"submodule {path} at {head.stdout.strip()} not {oid}")
        continue
    st = os.lstat(full)
    data = os.readlink(full).encode() if stat.S_ISLNK(st.st_mode) else open(full, "rb").read()
    want = "120000" if stat.S_ISLNK(st.st_mode) else ("100755" if st.st_mode & 0o111 else "100644")
    if want != mode: bad.append(f"mode {path}: {want} not {mode}")
    if hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest() != oid: bad.append(f"bytes {path}")
print(f"{len(tree)} tracked entries, {links} initialised gitlinks checked, {len(bad)} difference(s)")
print("\n".join(bad[:50]))
sys.exit(1 if bad else 0)
