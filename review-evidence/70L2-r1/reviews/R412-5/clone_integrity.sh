#!/bin/sh
# Verify the review clone is byte-exact at the exact head: HEAD, tree, empty
# status (untracked and ignored included), index entries, every tracked blob's
# bytes and mode, and the submodule gitlinks.  Usage: clone_integrity.sh <clone>
set -u
C=${1:?clone}
HEAD_EXP=b3ae17233eb9dd5934255f4018da7d45a159b5ac
TREE_EXP=02d9741fb9f57d81c758ae42adea26ed9694f647
cd "$C" || exit 2
ok=1
[ "$(git rev-parse HEAD)" = "$HEAD_EXP" ] || { echo "HEAD mismatch"; ok=0; }
[ "$(git rev-parse HEAD^{tree})" = "$TREE_EXP" ] || { echo "tree mismatch"; ok=0; }
[ "$(git write-tree)" = "$TREE_EXP" ] || { echo "index tree mismatch"; ok=0; }
st=$(git status --porcelain --ignored --untracked-files=all | wc -l)
[ "$st" -eq 0 ] || { echo "status not empty ($st)"; git status --porcelain --ignored --untracked-files=all | head; ok=0; }
python3 - "$C" <<'PY' || ok=0
import os, subprocess, sys, stat
c = sys.argv[1]
out = subprocess.run(["git", "-C", c, "ls-files", "-s", "-z"], capture_output=True, check=True).stdout
bad = n = 0
for rec in out.split(b"\0"):
    if not rec:
        continue
    meta, path = rec.split(b"\t", 1)
    mode, sha, stage = meta.split()
    n += 1
    p = os.path.join(c, path.decode())
    if mode == b"160000":
        got = subprocess.run(["git", "-C", c, "ls-tree", "HEAD", path.decode()], capture_output=True, text=True).stdout.split()[2]
        if got != sha.decode(): bad += 1; print("gitlink", path, got, sha)
        if os.path.isdir(os.path.join(p, "")) and os.path.exists(os.path.join(p, ".git")):
            h = subprocess.run(["git", "-C", p, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
            d = subprocess.run(["git", "-C", p, "status", "--porcelain"], capture_output=True, text=True).stdout.strip()
            print(f"submodule {path.decode()} checkout={h} gitlink={sha.decode()} {'clean' if not d else 'DIRTY'}")
            if h != sha.decode() or d: bad += 1
        else:
            print(f"submodule {path.decode()} not initialised, gitlink={sha.decode()}")
        continue
    st = os.lstat(p)
    want = {b"100644": 0o100644, b"100755": 0o100755, b"120000": 0o120000}[mode]
    if stat.S_ISLNK(st.st_mode):
        got_mode = 0o120000
        data = os.readlink(p).encode()
    else:
        got_mode = 0o100755 if st.st_mode & 0o111 else 0o100644
        data = open(p, "rb").read()
    h = subprocess.run(["git", "hash-object", "--stdin", "--no-filters"], input=data, capture_output=True).stdout.decode().strip()
    if h != sha.decode() or got_mode != want:
        bad += 1; print("MISMATCH", path.decode(), h, sha.decode(), oct(got_mode), mode)
print(f"index entries {n}, mismatches {bad}")
sys.exit(1 if bad else 0)
PY
[ $ok -eq 1 ] && echo "INTEGRITY OK $HEAD_EXP $TREE_EXP" || { echo "INTEGRITY FAIL"; exit 1; }
