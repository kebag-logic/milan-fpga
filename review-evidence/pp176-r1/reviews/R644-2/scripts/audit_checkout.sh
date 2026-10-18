#!/usr/bin/env bash
# audit_checkout.sh REPO HEAD TREE : verify a checkout is byte-exact at HEAD/TREE
set -u
R=$1; H=$2; T=$3
cd "$R" || exit 2
echo "HEAD $(git rev-parse HEAD) expect $H"
echo "TREE $(git rev-parse HEAD^{tree}) expect $T"
echo "index-tree $(git write-tree 2>/dev/null || echo n/a)"
echo "status-lines $(git status --porcelain --ignored | wc -l)"
echo "gitlinks $(git ls-files -s | awk '$1=="160000"' | wc -l)"
n=0; bad=0
git ls-tree -r -z HEAD | python3 -I -c '
import sys,subprocess,os,stat
data=sys.stdin.buffer.read().split(b"\0")
n=bad=0
for e in data:
    if not e: continue
    meta,path=e.split(b"\t",1); mode,typ,sha=meta.split()
    n+=1
    p=path.decode()
    if typ!=b"blob": bad+=1; print("NONBLOB",p); continue
    st=os.lstat(p)
    if mode==b"120000":
        ok=stat.S_ISLNK(st.st_mode) and subprocess.run(["git","hash-object","--stdin"],input=os.readlink(p).encode(),capture_output=True).stdout.strip()==sha
    else:
        h=subprocess.run(["git","hash-object",p],capture_output=True).stdout.strip()
        ex=bool(st.st_mode & 0o100)
        ok=h==sha and ex==(mode==b"100755")
    if not ok: bad+=1; print("MISMATCH",p)
print("blobs",n,"mismatch",bad)
'
git diff-index --cached --quiet HEAD && echo "index==HEAD yes" || echo "index==HEAD NO"
