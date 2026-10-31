#!/bin/sh
# Usage: verify_delta.sh <repo>  -- checks the R731-7 delta claims and the evidence manifest.
set -u; cd "$1" || exit 2
H=455a3953bf49efda23be4e73447a25b66a5c4bf7; PREV=86a349d5399d8abc40b819d09806fc8245682609; DEV=e5b8405db4c1f7cbdafb5df92b15b580142e0232
echo "head=$(git rev-parse $H) tree=$(git rev-parse $H^{tree})"
echo "prev_tree=$(git rev-parse $PREV^{tree}) cbc7c604_tree=$(git rev-parse cbc7c604^{tree})"
echo "parents=$(git rev-list --parents -1 $H | cut -d' ' -f2-)"
echo "subject=$(git log -1 --format=%s $H)"; echo "body_bytes=$(git log -1 --format=%b $H | tr -d '\n' | wc -c)"
echo "merge_tree_recomputed=$(git merge-tree --write-tree $PREV $DEV)"
echo "bases_prev_dev=$(git merge-base --all $PREV $DEV | tr '\n' ' ')"
echo "bases_head_dev=$(git merge-base --all $H $DEV | tr '\n' ' ')"
echo "new_from_dev=$(git rev-list $PREV..$DEV | tr '\n' ' ')"
echo "diff_prev_head_files=$(git diff --name-only $PREV $H | wc -l)"
echo "gitlinks:"; git ls-tree -r $H | awk '$2=="commit"{print "  "$3" "$4}'
echo "manifest:"; git show a16caad409edb65f5864f2c328b844ebc27d7d42:review-evidence/787-r1/MANIFEST.json | python3 -I -c '
import json,sys,subprocess,hashlib
m=json.load(sys.stdin); ok=bad=0
for e in m:
    b=subprocess.run(["git","show","a16caad409edb65f5864f2c328b844ebc27d7d42:review-evidence/787-r1/"+e["file"]],capture_output=True).stdout
    if hashlib.sha256(b).hexdigest()==e["published_sha256"]: ok+=1
    else: bad+=1; print("  MISMATCH",e["file"])
print("  entries",len(m),"ok",ok,"bad",bad)'
