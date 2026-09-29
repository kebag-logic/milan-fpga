#!/usr/bin/env bash
# Portable delta check for R404-6. Usage: delta_check.sh <repo> ; writes to stdout.
set -euo pipefail
R=${1:-.}
cd "$R"
HEAD=${HEAD_OVERRIDE:-d62b1e1a3a37283ebad039880163873698a011db}
PR=5c57927413e0dae279f06a75d2a58e3fec8a2bb0
OLDDEV=13eda870d1a6cf3f946fc228a98862366b08d102
DEV=79c36963660c10e4c1c11a744fb5bff41a552b8b
echo "== identities"
git rev-parse "$HEAD" "$HEAD^{tree}" "$HEAD^1" "$HEAD^2" "$PR" "$OLDDEV" "$DEV"
echo "== merge-base(PR, DEV) (expect OLDDEV)"; git merge-base "$PR" "$DEV"
echo "== OLDDEV ancestor of DEV"; git merge-base --is-ancestor "$OLDDEV" "$DEV" && echo yes
echo "== (1) files: PR content  git diff OLDDEV PR"
git diff --name-status "$OLDDEV" "$PR" | sort > /tmp/r404_6_a.$$
cat /tmp/r404_6_a.$$
echo "== (1) files: merged delta git diff DEV HEAD"
git diff --name-status "$DEV" "$HEAD" | sort > /tmp/r404_6_b.$$
cat /tmp/r404_6_b.$$
echo "== (1) file-list equality"; diff /tmp/r404_6_a.$$ /tmp/r404_6_b.$$ && echo FILE-LIST-EQUAL
echo "== (1) per-file patch equality (index lines stripped)"
while read -r st f rest; do
  p1=$(git diff "$OLDDEV" "$PR" -- "$f" | grep -v '^index ' | sed 's/^@@ .* @@/@@/' | sha256sum | cut -c1-16 || true)
  p2=$(git diff "$DEV" "$HEAD" -- "$f" | grep -v '^index ' | sed 's/^@@ .* @@/@@/' | sha256sum | cut -c1-16 || true)
  b1=$(git rev-parse "$PR:$f" 2>/dev/null || echo none)
  b2=$(git rev-parse "$HEAD:$f" 2>/dev/null || echo none)
  m1=$(git ls-tree "$PR" -- "$f" | cut -d' ' -f1); m2=$(git ls-tree "$HEAD" -- "$f" | cut -d' ' -f1)
  echo "$f patch_hunks_equal=$([ "$p1" = "$p2" ] && echo Y || echo N) blob_equal=$([ "$b1" = "$b2" ] && echo Y || echo N) mode=$m1/$m2"
done < /tmp/r404_6_a.$$
echo "== (2) git diff PR HEAD outside docs/findings/README.md vs git diff OLDDEV DEV"
git diff --name-status "$PR" "$HEAD" | sort > /tmp/r404_6_c.$$
git diff --name-status "$OLDDEV" "$DEV" | sort > /tmp/r404_6_d.$$
echo "-- PR..HEAD files:"; cat /tmp/r404_6_c.$$
echo "-- OLDDEV..DEV files:"; cat /tmp/r404_6_d.$$
diff /tmp/r404_6_c.$$ /tmp/r404_6_d.$$ && echo FILE-LIST-EQUAL
echo "-- per-file: blob at HEAD == blob at DEV (outside README)"
while read -r st f rest; do
  [ "$f" = docs/findings/README.md ] && continue
  b1=$(git rev-parse "$DEV:$f" 2>/dev/null || echo none); b2=$(git rev-parse "$HEAD:$f" 2>/dev/null || echo none)
  m1=$(git ls-tree "$DEV" -- "$f" | cut -d' ' -f1); m2=$(git ls-tree "$HEAD" -- "$f" | cut -d' ' -f1)
  echo "$f blob_equal=$([ "$b1" = "$b2" ] && echo Y || echo N) mode=$m1/$m2"
done < /tmp/r404_6_c.$$
echo "== whole-tree: every path at HEAD equals DEV or PR (except README)"
git ls-tree -r "$HEAD" | sort -k4 > /tmp/r404_6_h.$$
git ls-tree -r "$DEV" | sort -k4 > /tmp/r404_6_v.$$
git ls-tree -r "$PR" | sort -k4 > /tmp/r404_6_p.$$
python3 - /tmp/r404_6_h.$$ /tmp/r404_6_v.$$ /tmp/r404_6_p.$$ <<'EOF'
import sys
def load(p):
    d={}
    for l in open(p):
        meta,path=l.rstrip('\n').split('\t',1); d[path]=meta
    return d
h,v,p=(load(x) for x in sys.argv[1:4])
bad=[]
for k in sorted(set(h)|set(v)|set(p)):
    if k=='docs/findings/README.md': continue
    hv=h.get(k); vv=v.get(k); pv=p.get(k)
    if hv==vv or hv==pv: continue
    bad.append((k,hv,vv,pv))
print("paths", len(h), "anomalies", len(bad))
for b in bad: print("ANOMALY", b)
EOF
echo "== gitlinks HEAD vs DEV vs PR"
for t in "$HEAD" "$DEV" "$PR" "$OLDDEV"; do echo "$t"; git ls-tree "$t" | awk '$2=="commit"'; done
echo "== README three-way"
git diff "$OLDDEV" "$DEV" -- docs/findings/README.md
echo "-- PR side"
git diff "$OLDDEV" "$PR" -- docs/findings/README.md
echo "-- merged vs DEV"
git diff "$DEV" "$HEAD" -- docs/findings/README.md
echo "-- merged vs PR"
git diff "$PR" "$HEAD" -- docs/findings/README.md
echo "-- remerge-diff"
git show --remerge-diff --format=%H "$HEAD" || true
echo "== VERDICT checks"
python3 - "$OLDDEV" "$DEV" "$PR" "$HEAD" <<'PYEOF'
import subprocess,sys
o,v,p,h=sys.argv[1:5]
def git(*a): return subprocess.run(['git',*a],capture_output=True,text=True,check=True).stdout
def show(r,f):
    r2=subprocess.run(['git','show',f'{r}:{f}'],capture_output=True)
    return r2.stdout if r2.returncode==0 else None
fails=[]
# (1) PR content reproduced file for file
for f in git('diff','--name-only',o,p).split():
    if f=='docs/findings/README.md': continue
    if show(h,f)!=show(p,f): fails.append('PR file differs at head: '+f)
if sorted(git('diff','--name-only',o,p).split())!=sorted(git('diff','--name-only',v,h).split()): fails.append('merged delta file list != PR file list')
# (2) every other path at head equals dev (ls-tree meta incl. mode, gitlinks)
def lt(r):
    d={}
    for l in git('ls-tree','-r',r).splitlines():
        m,path=l.split('\t',1); d[path]=m
    return d
H,V,P=lt(h),lt(v),lt(p)
prfiles=set(git('diff','--name-only',o,p).split())
for k in set(H)|set(V):
    if k in prfiles: continue
    if H.get(k)!=V.get(k): fails.append('non-PR path differs from dev: '+k)
# README: PR README with dev's added row(s) inserted above the #75 row
R='docs/findings/README.md'
ol=show(o,R).decode().splitlines(True); vl=show(v,R).decode().splitlines(True); pl=show(p,R).decode().splitlines(True); hl=show(h,R).decode().splitlines(True)
added=[l for l in vl if l not in ol]; removed=[l for l in ol if l not in vl]
if removed: fails.append('dev removed README lines: %r'%removed)
i=[n for n,l in enumerate(pl) if l.startswith('| [75_RECONNECT_RESTART_MEASUREMENT.md]')]
if len(i)!=1: fails.append('PR 75 row not unique')
else:
    exp=pl[:i[0]]+added+pl[i[0]:]
    if exp!=hl: fails.append('README != PR README with dev rows above the 75 row')
print('dev-added README rows:',len(added))
print('FAILURES',len(fails))
for f in fails: print('FAIL',f)
print('DELTA-CHECK', 'PASS' if not fails else 'FAIL')
PYEOF
rm -f /tmp/r404_6_*.$$
