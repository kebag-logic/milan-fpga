#!/usr/bin/env bash
# Judge the round-4 merge commit's composition from git objects alone.
# Usage: 10-merge-composition.sh <repo>   (read-only; writes nothing in <repo>)
set -euo pipefail
R=${1:?repo}; cd "$R"
HEAD_C=47afa74d5cb7cf67ec1f606a0b8ea05fda3e3346
LANE=921fff59d6e1243284e477f7a368173018420d35
MAIN=0451d83d9d3f2ed5f4513c59ac5ac219ad9dd7ff
echo "head=$(git rev-parse $HEAD_C) tree=$(git rev-parse $HEAD_C^{tree})"
echo "parents=$(git log -1 --format=%P $HEAD_C)"
MB=$(git merge-base $LANE $MAIN); echo "merge-base=$MB"
t=$(mktemp -d)
git diff --name-only "$MB" "$LANE" | sort >"$t/lane"
git diff --name-only "$MB" "$MAIN" | sort >"$t/main"
git diff --name-only "$MAIN" "$HEAD_C" | sort >"$t/merged"
echo "lane files=$(wc -l <"$t/lane") main files=$(wc -l <"$t/main") main..head files=$(wc -l <"$t/merged")"
if cmp -s "$t/lane" "$t/merged"; then echo "FILESET main..head == merge-base..lane : YES"; else echo "FILESET: NO"; diff "$t/lane" "$t/merged" || true; fi
echo "both-sided files:"; comm -12 "$t/lane" "$t/main" | sed 's/^/  /'
bad=0; n=0
for f in $(comm -23 "$t/lane" "$t/main"); do
  n=$((n+1)); [ "$(git ls-tree $LANE -- "$f")" = "$(git ls-tree $HEAD_C -- "$f")" ] || { echo "  LANE-ONLY DIFFERS: $f"; bad=1; }
done; echo "lane-only files byte+mode equal to $LANE: $n checked, bad=$bad"
m=0
for f in $(comm -13 "$t/lane" "$t/main"); do
  m=$((m+1)); [ "$(git ls-tree $MAIN -- "$f")" = "$(git ls-tree $HEAD_C -- "$f")" ] || { echo "  MAIN-ONLY DIFFERS: $f"; bad=1; }
done; echo "main-only files byte+mode equal to $MAIN: $m checked, bad=$bad"
AUTO=$(git merge-tree --write-tree $LANE $MAIN | head -1) || true
AUTO=$(git merge-tree --write-tree $LANE $MAIN | head -1 || true)
echo "replayed-merge tree (with conflict markers)=$AUTO"
git merge-tree --write-tree --name-only $LANE $MAIN | sed -n '2,/^$/p' | sed 's/^/  conflicted: /' || true
echo "=== replayed merge -> head (the hand resolution, and nothing else)"
git -c core.pager=cat diff --no-color --stat "$AUTO" "$HEAD_C"
git -c core.pager=cat diff --no-color "$AUTO" "$HEAD_C"
echo "=== HDL: lane side vs main side"
git diff --stat "$MB" "$LANE" -- hdl; git diff --stat "$MB" "$MAIN" -- hdl
echo "=== mutation patch targets"
for d in tb/maap/mutations tb/adp_engine/mutations; do echo "$d: $(ls $d/*.patch | wc -l) patches"; git show $HEAD_C:$d >/dev/null; grep -h '^+++ ' $d/*.patch | sort | uniq -c; done
echo "=== patch targets touched by the merge resolution? (files differing replayed->head)"
git diff --name-only "$AUTO" "$HEAD_C" | grep '^hdl/' || echo "  none under hdl/"
echo "=== git apply --check of every MAAP and ADP patch at head (index untouched)"
ok=0; fl=0
for p in tb/maap/mutations/*.patch tb/adp_engine/mutations/*.patch; do
  if git apply --check "$p" 2>/dev/null; then ok=$((ok+1)); else fl=$((fl+1)); echo "  FAIL $p"; fi
done; echo "apply-check ok=$ok fail=$fl"
echo "=== C3 config-valid flag fan-out at head"
git grep -n 'aecp_cur_cfg_v_w\|adp_cur_cfg_w\|dyn_cur_config_v' $HEAD_C -- hdl | sed "s/^$HEAD_C://"
echo "=== KL_pp_maap references to any config/ADP/AECP net at head"
git grep -n -i 'cur_cfg\|cur_config\|aecp\|adp_' $HEAD_C -- hdl/maap/KL_pp_maap.sv | sed "s/^$HEAD_C://" || echo "  none"
echo "=== git diff --check (whitespace) main..head and lane..head"
git diff --check $MAIN $HEAD_C && echo "  main..head clean"; git diff --check $LANE $HEAD_C && echo "  lane..head clean"
rm -rf "$t"; echo "bad=$bad"; exit $bad
