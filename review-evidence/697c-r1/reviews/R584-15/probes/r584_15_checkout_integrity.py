# Reviewer check (R584-15): the clone's tracked bytes, modes and index equal the exact head, and the gitlinks the
# gates read are at their pins. Usage: python3 -I r584_15_checkout_integrity.py <clone-root> <expected-head>
import hashlib, os, stat, subprocess, sys
from pathlib import Path
root, want = Path(sys.argv[1]).resolve(), sys.argv[2]
def git(*a): return subprocess.run(["git", "-C", str(root), *a], capture_output=True, check=True).stdout
head = git("rev-parse", "HEAD").decode().strip()
tree = {}
for e in git("ls-tree", "-r", "-z", "--full-tree", "HEAD").split(b"\0"):
    if e:
        meta, path = e.split(b"\t", 1); mode, _, oid = meta.decode().split(); tree[path] = (mode, oid)
index = {}
for e in git("ls-files", "-s", "-z").split(b"\0"):
    if e:
        meta, path = e.split(b"\t", 1); mode, oid, stage = meta.decode().split(); index[path] = (mode, oid, stage)
bad = [p for p in tree if index.get(p, ("", "", ""))[:2] != tree[p] or index[p][2] != "0"] + [p for p in index if p not in tree]
disk_bad = []
for p, (mode, oid) in tree.items():
    if mode == "160000":
        continue
    f = root / os.fsdecode(p)
    st = f.lstat()
    data = os.readlink(f).encode() if stat.S_ISLNK(st.st_mode) else f.read_bytes()
    m = "120000" if stat.S_ISLNK(st.st_mode) else ("100755" if st.st_mode & stat.S_IXUSR else "100644")
    if m != mode or hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest() != oid:
        disk_bad.append(p)
links = {p.decode(): oid for p, (mode, oid) in tree.items() if mode == "160000"}
print(f"head {head} expected {want}: {'OK' if head == want else 'MISMATCH'}")
print(f"tree entries {len(tree)}; index records {len(index)}; index differs from HEAD: {len(bad)}")
print(f"tracked files whose disk bytes or mode differ from HEAD: {len(disk_bad)} {[os.fsdecode(p) for p in disk_bad][:5]}")
for path, oid in sorted(links.items()):
    sub = root / path
    try:
        at = subprocess.run(["git", "-C", str(sub), "rev-parse", "HEAD"], capture_output=True, check=True).stdout.decode().strip() \
            if (sub / ".git").exists() else "uninitialised"
    except subprocess.CalledProcessError:
        at = "unreadable"
    print(f"gitlink {path} {oid}: checkout {at} {'OK' if at == oid else ('-' if at == 'uninitialised' else 'DIFFERS')}")
untracked = git("status", "--porcelain", "--ignored", "--untracked-files=all").decode().splitlines()
print(f"untracked or ignored entries: {len(untracked)} {untracked[:5]}")
sys.exit(0 if head == want and not bad and not disk_bad else 1)
