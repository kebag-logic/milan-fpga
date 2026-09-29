#!/usr/bin/env bash
# Verify the review clone is at the exact head with unmodified tracked bytes,
# modes, index and gitlinks. Usage: verify_clone.sh <repo>
set -uo pipefail
cd "$1"
H=d62b1e1a3a37283ebad039880163873698a011db; T=b4a1f5ed6a5b00ecde3dcba7781f45fb72480b59
echo "HEAD $(git rev-parse HEAD) expect $H"; echo "tree $(git rev-parse HEAD^{tree}) expect $T"
echo "status-lines $(git status --porcelain --untracked-files=all --ignore-submodules=none | wc -l)"
git diff --quiet && echo "worktree==index" || echo "WORKTREE DIFFERS"
git diff --cached --quiet HEAD && echo "index==HEAD" || echo "INDEX DIFFERS"
python3 - <<'EOF'
import subprocess,hashlib,os
ls=subprocess.run(['git','ls-files','-s'],capture_output=True,text=True,check=True).stdout.splitlines()
tree={}
for l in subprocess.run(['git','ls-tree','-r','HEAD'],capture_output=True,text=True,check=True).stdout.splitlines():
    m,path=l.split('\t',1); mode,typ,sha=m.split(); tree[path]=(mode,sha)
bad=0;n=0
for l in ls:
    m,path=l.split('\t',1); mode,sha,stage=m.split()
    if tree.get(path)!=(mode,sha): bad+=1; print('INDEX/TREE MISMATCH',path)
    if mode=='160000': continue
    n+=1
    if mode=='120000': data=os.readlink(path).encode()
    else:
        data=open(path,'rb').read()
        ex=os.access(path,os.X_OK)
        if (mode=='100755')!=ex: bad+=1; print('MODE MISMATCH',path)
    h=hashlib.sha1(b'blob %d\0'%len(data)+data).hexdigest()
    if h!=sha: bad+=1; print('BYTE MISMATCH',path)
print('index-entries',len(ls),'tree-entries',len(tree),'rehashed',n,'mismatches',bad)
EOF
echo "gitlinks:"; git ls-tree HEAD | awk '$2=="commit"{print $3, $4}'
git submodule status 2>&1
