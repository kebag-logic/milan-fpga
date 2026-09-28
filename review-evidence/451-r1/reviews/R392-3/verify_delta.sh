#!/usr/bin/env bash
# R392-3 delta verification for PR #616 (issue #451).
# Usage: verify_delta.sh <repo>   (read-only; writes nothing into <repo>)
set -u
REPO=${1:?repo path}
HEAD_EXP=0e5ae9c82bbdb5abc3feba84f07d0e6481254906
TREE_EXP=38f7ca763a9713bea02d78ff865e0c02ea240445
MERGE=f4bb2bd71fff5bec778f1281db1183f0c154ca16
LANE=335e55c4135979a554dc0281d6980ac1e2158aee
DEV=7390b43627032c71c470e2aa8d0845eb5b740663
BASE=6d5ebd7357c1e468e446f18a61527c5be6118a04
IDX=docs/findings/README.md
g(){ git -C "$REPO" "$@" 2>/dev/null; }
fail=0; chk(){ if [ "$1" = "$2" ]; then echo "OK   $3"; else echo "FAIL $3 (got '$1' want '$2')"; fail=1; fi; }

chk "$(g rev-parse HEAD)" "$HEAD_EXP" "head"
chk "$(g rev-parse HEAD^{tree})" "$TREE_EXP" "tree"
chk "$(g rev-parse HEAD^)" "$MERGE" "head parent is the merge"
chk "$(g rev-list --parents -n1 $MERGE | cut -d' ' -f2-)" "$LANE $DEV" "merge parents lane,dev"
chk "$(g merge-base $LANE $DEV)" "$BASE" "merge base is the lane base"

echo "-- (1) conflict set and resolution"
AUTO=$(g merge-tree --write-tree --name-only $LANE $DEV | sed -n '1p')
CONF=$(g merge-tree --write-tree --name-only $LANE $DEV | awk 'NR>1 && NF==0{exit} NR>1{print}')
chk "$CONF" "$IDX" "only conflicted path"
chk "$(g diff --name-only $AUTO $MERGE)" "$IDX" "merge differs from automatic merge only in the index"
chk "$(g diff --name-only $DEV $MERGE | sort | tr '\n' ' ')" "docs/findings/451_TDM8_FIRST_LIGHT.md $IDX " "merge vs dev: page and index only"
chk "$(g diff --name-only $LANE $MERGE -- docs/findings/451_TDM8_FIRST_LIGHT.md)" "" "page blob unchanged by merge"
rows(){ g show "$1:$IDX" | grep '^| \[' ; }
L=$(rows $LANE); D=$(rows $DEV); M=$(rows $MERGE); H=$(rows HEAD)
chk "$(printf '%s\n%s\n' "$L" "$D" | sort -u | sha256sum)" "$(printf '%s\n' "$M" | sort | sha256sum)" "merged rows = union of both sides"
chk "$(printf '%s\n' "$M" | sort | uniq -d | wc -l)" "0" "no duplicate row"
chk "$(g show $MERGE:$IDX | grep -cE '^(<<<<<<<|=======|>>>>>>>)')" "0" "no conflict marker"
chk "$(printf '%s\n' "$M" | sed -n '2,$p')" "$D" "dev rows keep dev order below the new row"
chk "$(printf '%s\n' "$M" | sed -n '1p')" "$(printf '%s\n' "$L" | sed -n '1p')" "#451 row first (newest-first practice)"
chk "$(printf '%s\n' "$H")" "$(printf '%s\n' "$M")" "index unchanged after merge"
echo "   index rows: $(printf '%s\n' "$H" | wc -l)"
g show HEAD:$IDX | awk -F'|' '/^\|/{n=NF-2; if(n!=3){print "BAD cells line " NR ": " n; b=1}} END{if(!b) print "OK   index: 3 cells in every table line"}'
g show HEAD:docs/reference/MILAN_COMPLIANCE_MATRIX.md | awk -F'|' 'NR>=195&&NR<=215&&/^\|/{n=NF-2; if(n!=3){print "BAD cells line " NR ": " n; b=1}} END{if(!b) print "OK   matrix lines 195-215: 3 cells"}'

echo "-- (2) gitlinks"
for c in $BASE $LANE $DEV $MERGE HEAD; do echo "   $c $(g ls-tree $c | awk '$2=="commit"{printf "%s=%s ", $4, substr($3,1,8)}')"; done
chk "$(g ls-tree HEAD protocol-processor | awk '{print $3}')" "c951a9ff0cb5851fb159d33e966e5a2a9a188fe3" "protocol-processor = dev c951a9ff"
chk "$(g ls-tree -r HEAD | awk '$2=="commit"' | sha256sum)" "$(g ls-tree -r $DEV | awk '$2=="commit"' | sha256sum)" "all gitlinks equal dev"
chk "$(g diff --name-only $BASE $LANE | grep -cvE '^docs/')" "0" "lane (pre-merge) touches docs only"

echo "-- (3) rewording commit"
chk "$(g diff --name-only $MERGE HEAD | tr '\n' ' ')" "docs/litex/CLOCK_DOMAINS.md docs/reference/MILAN_COMPLIANCE_MATRIX.md " "reword touches two files"
chk "$(g diff --numstat $MERGE HEAD | awk '{a+=$1;d+=$2} END{print a"/"d}')" "2/2" "reword is one line per file"
g diff -U0 $MERGE HEAD | grep -E '^[-+]' | grep -vE '^(\+\+\+|---) ' | cut -c1-600
chk "$(g log --format=%B -n1 HEAD | sed '/^$/d' | wc -l)" "1" "head message one line"
chk "$(g log --format=%B -n1 $MERGE | sed '/^$/d' | wc -l)" "1" "merge message one line"

echo "-- (4) net change against dev"
g diff --stat $DEV HEAD | tail -1
chk "$(g diff --name-only $DEV HEAD | wc -l)" "4" "four files differ from dev"
exit $fail
